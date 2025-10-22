"""
RAG (Retrieval-Augmented Generation) system for 0% hallucination
Uses vector database to retrieve relevant information and answer only based on knowledge base
"""
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import os
import logging
from typing import List, Dict, Optional
import json

logger = logging.getLogger(__name__)


class RAGSystem:
    """
    Retrieval-Augmented Generation system
    Ensures 0% hallucination by only using information from knowledge base
    """
    
    def __init__(
        self,
        chroma_db_path: str = "chroma_db",
        embedding_model: str = "all-MiniLM-L6-v2",
        collection_name: str = "knowledge_base"
    ):
        """
        Initialize RAG system
        
        Args:
            chroma_db_path: Path to ChromaDB storage
            embedding_model: Sentence transformer model for embeddings
            collection_name: Name of the collection in ChromaDB
        """
        self.chroma_db_path = chroma_db_path
        self.collection_name = collection_name
        
        # Initialize embedding model
        logger.info(f"Loading embedding model: {embedding_model}")
        self.embedding_model = SentenceTransformer(embedding_model)
        
        # Initialize ChromaDB
        logger.info(f"Initializing ChromaDB at {chroma_db_path}")
        self.client = chromadb.PersistentClient(path=chroma_db_path)
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        logger.info(f"Collection '{collection_name}' ready with {self.collection.count()} documents")
    
    def add_document(self, text: str, metadata: Optional[Dict] = None, doc_id: Optional[str] = None):
        """
        Add a document to the knowledge base
        
        Args:
            text: Document text
            metadata: Optional metadata for the document
            doc_id: Optional document ID (auto-generated if not provided)
        """
        if not text.strip():
            logger.warning("Empty text provided, skipping")
            return
        
        # Generate embedding
        embedding = self.embedding_model.encode(text).tolist()
        
        # Generate ID if not provided
        if doc_id is None:
            doc_id = f"doc_{self.collection.count()}"
        
        # Add to collection
        self.collection.add(
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata or {}],
            ids=[doc_id]
        )
        logger.info(f"Added document with ID: {doc_id}")
    
    def add_documents_from_file(self, file_path: str, chunk_size: int = 500, chunk_overlap: int = 50):
        """
        Add documents from a text file with chunking
        
        Args:
            file_path: Path to text file
            chunk_size: Size of each chunk in characters
            chunk_overlap: Overlap between chunks
        """
        logger.info(f"Loading documents from {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Split into chunks
        chunks = self._create_chunks(text, chunk_size, chunk_overlap)
        logger.info(f"Created {len(chunks)} chunks from {file_path}")
        
        # Add each chunk
        for i, chunk in enumerate(chunks):
            metadata = {
                "source": file_path,
                "chunk_index": i
            }
            self.add_document(chunk, metadata, f"{os.path.basename(file_path)}_chunk_{i}")
    
    def _create_chunks(self, text: str, chunk_size: int, overlap: int) -> List[str]:
        """Create overlapping chunks from text"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            start = end - overlap
        
        return chunks
    
    def query(self, query: str, top_k: int = 3, similarity_threshold: float = 0.7) -> Dict:
        """
        Query the knowledge base
        
        Args:
            query: Query text
            top_k: Number of top results to return
            similarity_threshold: Minimum similarity score (0-1)
            
        Returns:
            Dictionary with query results and generated answer
        """
        logger.info(f"Querying: {query}")
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # Query collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # Process results
        documents = results['documents'][0] if results['documents'] else []
        distances = results['distances'][0] if results['distances'] else []
        metadatas = results['metadatas'][0] if results['metadatas'] else []
        
        # Filter by similarity threshold (ChromaDB returns distances, convert to similarity)
        filtered_results = []
        for doc, dist, meta in zip(documents, distances, metadatas):
            similarity = 1 - dist  # Convert distance to similarity
            if similarity >= similarity_threshold:
                filtered_results.append({
                    "document": doc,
                    "similarity": similarity,
                    "metadata": meta
                })
        
        logger.info(f"Found {len(filtered_results)} relevant documents")
        
        # Generate answer based on retrieved documents
        answer = self._generate_answer(query, filtered_results)
        
        return {
            "query": query,
            "answer": answer,
            "sources": filtered_results,
            "num_sources": len(filtered_results)
        }
    
    def _generate_answer(self, query: str, results: List[Dict]) -> str:
        """
        Generate answer based on retrieved documents
        This ensures 0% hallucination by only using retrieved information
        """
        if not results:
            return "I don't have information about that in my knowledge base. Please provide more context or ask about topics I've been trained on."
        
        # Combine relevant documents
        context = "\n\n".join([r["document"] for r in results])
        
        # For now, return the most relevant document
        # In a production system, this could use a lightweight model for summarization
        # while staying grounded in the retrieved context
        answer = f"Based on my knowledge base:\n\n{results[0]['document']}"
        
        if len(results) > 1:
            answer += f"\n\n(Found {len(results)} relevant information sources)"
        
        return answer
    
    def clear_collection(self):
        """Clear all documents from the collection"""
        self.client.delete_collection(self.collection_name)
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        logger.info("Collection cleared")
    
    def get_stats(self) -> Dict:
        """Get statistics about the knowledge base"""
        return {
            "total_documents": self.collection.count(),
            "collection_name": self.collection_name,
            "embedding_model": self.embedding_model
        }

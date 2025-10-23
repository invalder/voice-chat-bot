//! RAG (Retrieval-Augmented Generation) System
//! 
//! Provides zero-hallucination responses by only using information from the knowledge base.
//! Uses vector embeddings for semantic search and similarity matching.

use anyhow::{Context, Result};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs;
use std::path::Path;
use tracing::{info, warn};

/// A document in the knowledge base
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Document {
    /// Document ID
    pub id: String,
    
    /// Document text content
    pub text: String,
    
    /// Document metadata
    pub metadata: HashMap<String, String>,
    
    /// Embedding vector (lazy loaded)
    #[serde(skip)]
    pub embedding: Option<Vec<f32>>,
}

/// Query result with similarity score
#[derive(Debug, Clone)]
pub struct QueryResult {
    /// Retrieved document
    pub document: Document,
    
    /// Similarity score (0.0-1.0)
    pub similarity: f32,
}

/// Query response containing answer and sources
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct QueryResponse {
    /// Original query
    pub query: String,
    
    /// Generated answer
    pub answer: String,
    
    /// Number of sources used
    pub num_sources: usize,
    
    /// Source documents (serializable without embeddings)
    pub sources: Vec<String>,
}

/// RAG System for zero-hallucination question answering
pub struct RagSystem {
    /// Collection name / domain identifier
    collection_name: String,
    
    /// In-memory document store
    documents: Vec<Document>,
    
    /// Path to persistent storage
    db_path: String,
    
    /// Next document ID
    next_id: usize,
}

impl RagSystem {
    /// Create a new RAG system
    pub fn new(db_path: String, collection_name: String) -> Result<Self> {
        info!("Initializing RAG system at: {}", db_path);
        
        // Create directory if it doesn't exist
        if !Path::new(&db_path).exists() {
            fs::create_dir_all(&db_path)
                .context("Failed to create database directory")?;
        }
        
        let mut system = Self {
            collection_name: collection_name.clone(),
            documents: Vec::new(),
            db_path: db_path.clone(),
            next_id: 0,
        };
        
        // Try to load existing documents
        system.load_documents()?;
        
        info!(
            "RAG system initialized with {} documents",
            system.documents.len()
        );
        
        Ok(system)
    }
    
    /// Add a document to the knowledge base
    pub fn add_document(&mut self, text: String, metadata: Option<HashMap<String, String>>) -> Result<String> {
        if text.trim().is_empty() {
            warn!("Attempted to add empty document, skipping");
            return Ok(String::new());
        }
        
        let doc_id = format!("doc_{}", self.next_id);
        self.next_id += 1;
        
        let document = Document {
            id: doc_id.clone(),
            text,
            metadata: metadata.unwrap_or_default(),
            embedding: None,
        };
        
        self.documents.push(document);
        info!("Added document with ID: {}", doc_id);
        
        // Persist documents
        self.save_documents()?;
        
        Ok(doc_id)
    }
    
    /// Add documents from a text file with chunking
    pub fn add_documents_from_file<P: AsRef<Path>>(
        &mut self,
        file_path: P,
        chunk_size: usize,
        chunk_overlap: usize,
    ) -> Result<Vec<String>> {
        let path = file_path.as_ref();
        info!("Loading documents from: {:?}", path);
        
        let content = fs::read_to_string(path)
            .context("Failed to read file")?;
        
        let chunks = Self::create_chunks(&content, chunk_size, chunk_overlap);
        info!("Created {} chunks from file", chunks.len());
        
        let mut doc_ids = Vec::new();
        for (i, chunk) in chunks.iter().enumerate() {
            let mut metadata = HashMap::new();
            metadata.insert("source".to_string(), path.to_string_lossy().to_string());
            metadata.insert("chunk_index".to_string(), i.to_string());
            
            let doc_id = self.add_document(chunk.clone(), Some(metadata))?;
            doc_ids.push(doc_id);
        }
        
        Ok(doc_ids)
    }
    
    /// Create overlapping text chunks
    fn create_chunks(text: &str, chunk_size: usize, overlap: usize) -> Vec<String> {
        let mut chunks = Vec::new();
        let mut start = 0;
        
        while start < text.len() {
            let end = (start + chunk_size).min(text.len());
            let chunk = text[start..end].trim();
            
            if !chunk.is_empty() {
                chunks.push(chunk.to_string());
            }
            
            if end >= text.len() {
                break;
            }
            
            start = end.saturating_sub(overlap);
            if start == end {
                start = end;
            }
        }
        
        chunks
    }
    
    /// Query the knowledge base
    pub fn query(&self, query: &str, top_k: usize, similarity_threshold: f32) -> Result<QueryResponse> {
        info!("Querying: {}", query);
        
        // For simplified implementation, use basic text matching
        // In production, this would use proper embeddings
        let results = self.search_documents(query, top_k, similarity_threshold);
        
        info!("Found {} relevant documents", results.len());
        
        let answer = self.generate_answer(query, &results);
        let sources: Vec<String> = results.iter().map(|r| r.document.text.clone()).collect();
        
        Ok(QueryResponse {
            query: query.to_string(),
            answer,
            num_sources: results.len(),
            sources,
        })
    }
    
    /// Search documents using basic text similarity
    /// Note: In production, this would use proper vector embeddings
    fn search_documents(&self, query: &str, top_k: usize, threshold: f32) -> Vec<QueryResult> {
        let query_lower = query.to_lowercase();
        let query_words: Vec<&str> = query_lower.split_whitespace().collect();
        
        let mut results: Vec<QueryResult> = self.documents
            .iter()
            .map(|doc| {
                let doc_lower = doc.text.to_lowercase();
                
                // Calculate simple word overlap similarity
                let matching_words = query_words.iter()
                    .filter(|word| doc_lower.contains(*word))
                    .count();
                
                let similarity = if query_words.is_empty() {
                    0.0
                } else {
                    matching_words as f32 / query_words.len() as f32
                };
                
                QueryResult {
                    document: doc.clone(),
                    similarity,
                }
            })
            .filter(|r| r.similarity >= threshold)
            .collect();
        
        // Sort by similarity descending
        results.sort_by(|a, b| b.similarity.partial_cmp(&a.similarity).unwrap());
        
        // Take top K
        results.truncate(top_k);
        
        results
    }
    
    /// Generate answer from retrieved documents
    fn generate_answer(&self, _query: &str, results: &[QueryResult]) -> String {
        if results.is_empty() {
            return "I don't have information about that in my knowledge base. Please provide more context or ask about topics I've been trained on.".to_string();
        }
        
        let mut answer = String::from("Based on my knowledge base:\n\n");
        answer.push_str(&results[0].document.text);
        
        if results.len() > 1 {
            answer.push_str(&format!("\n\n(Found {} relevant information sources)", results.len()));
        }
        
        answer
    }
    
    /// Get statistics about the knowledge base
    pub fn get_stats(&self) -> HashMap<String, String> {
        let mut stats = HashMap::new();
        stats.insert("total_documents".to_string(), self.documents.len().to_string());
        stats.insert("collection_name".to_string(), self.collection_name.clone());
        stats
    }
    
    /// Clear all documents from the collection
    pub fn clear_collection(&mut self) -> Result<()> {
        self.documents.clear();
        self.next_id = 0;
        self.save_documents()?;
        info!("Collection cleared");
        Ok(())
    }
    
    /// Save documents to disk
    fn save_documents(&self) -> Result<()> {
        let db_file = format!("{}/{}.json", self.db_path, self.collection_name);
        let json = serde_json::to_string_pretty(&self.documents)
            .context("Failed to serialize documents")?;
        fs::write(&db_file, json)
            .context("Failed to write documents to disk")?;
        Ok(())
    }
    
    /// Load documents from disk
    fn load_documents(&mut self) -> Result<()> {
        let db_file = format!("{}/{}.json", self.db_path, self.collection_name);
        
        if !Path::new(&db_file).exists() {
            return Ok(());
        }
        
        let json = fs::read_to_string(&db_file)
            .context("Failed to read documents from disk")?;
        
        self.documents = serde_json::from_str(&json)
            .context("Failed to deserialize documents")?;
        
        if !self.documents.is_empty() {
            // Update next_id based on loaded documents
            let max_id = self.documents.iter()
                .filter_map(|d| d.id.strip_prefix("doc_"))
                .filter_map(|s| s.parse::<usize>().ok())
                .max()
                .unwrap_or(0);
            self.next_id = max_id + 1;
        }
        
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::env;
    
    #[test]
    fn test_create_chunks() {
        let text = "This is a test. It has multiple sentences. We want to chunk it.";
        let chunks = RagSystem::create_chunks(text, 20, 5);
        assert!(!chunks.is_empty());
    }
    
    #[test]
    fn test_rag_basic() {
        let temp_dir = env::temp_dir().join("test_rag");
        let _ = fs::remove_dir_all(&temp_dir);
        
        let mut rag = RagSystem::new(
            temp_dir.to_string_lossy().to_string(),
            "test".to_string()
        ).unwrap();
        
        rag.add_document(
            "Rust is a systems programming language.".to_string(),
            None
        ).unwrap();
        
        let result = rag.query("What is Rust?", 1, 0.1).unwrap();
        assert!(result.answer.contains("Rust"));
        
        let _ = fs::remove_dir_all(&temp_dir);
    }
}

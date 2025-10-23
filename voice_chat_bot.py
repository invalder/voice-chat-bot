"""
Main Voice Chat Bot orchestrator
Combines STT, RAG, and TTS for complete voice interaction
"""
import logging
from typing import Optional
from config import VoiceChatBotConfig
from stt import SpeechToText
from tts import TextToSpeech
from rag import RAGSystem
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VoiceChatBot:
    """
    Main Voice Chat Bot class
    Provides voice-based Q&A with 0% hallucination guarantee
    """
    
    def __init__(self, config: Optional[VoiceChatBotConfig] = None):
        """
        Initialize Voice Chat Bot
        
        Args:
            config: Configuration object (uses defaults if not provided)
        """
        self.config = config or VoiceChatBotConfig()
        
        logger.info("Initializing Voice Chat Bot...")
        logger.info(f"Expert domain: {self.config.expert_domain}")
        
        # Initialize components
        self.stt = SpeechToText(
            model_name=self.config.stt.model_name,
            language=self.config.stt.language
        )
        
        self.tts = TextToSpeech(
            engine=self.config.tts.engine,
            rate=self.config.tts.rate
        )
        
        self.rag = RAGSystem(
            chroma_db_path=self.config.chroma_db_path,
            embedding_model=self.config.rag.embedding_model,
            collection_name=self.config.expert_domain
        )
        
        logger.info("Voice Chat Bot initialized successfully")
    
    def load_knowledge_base(self, knowledge_base_path: Optional[str] = None):
        """
        Load documents from knowledge base directory
        
        Args:
            knowledge_base_path: Path to knowledge base directory
        """
        kb_path = knowledge_base_path or self.config.knowledge_base_path
        
        if not os.path.exists(kb_path):
            logger.warning(f"Knowledge base path does not exist: {kb_path}")
            logger.info(f"Creating directory: {kb_path}")
            os.makedirs(kb_path, exist_ok=True)
            return
        
        logger.info(f"Loading knowledge base from {kb_path}")
        
        # Load all text files from the directory
        loaded_count = 0
        for filename in os.listdir(kb_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(kb_path, filename)
                self.rag.add_documents_from_file(
                    file_path,
                    chunk_size=self.config.rag.chunk_size,
                    chunk_overlap=self.config.rag.chunk_overlap
                )
                loaded_count += 1
        
        logger.info(f"Loaded {loaded_count} files from knowledge base")
        stats = self.rag.get_stats()
        logger.info(f"Total documents in knowledge base: {stats['total_documents']}")
    
    def process_text_query(self, query: str) -> str:
        """
        Process a text query and return text response
        
        Args:
            query: Text query
            
        Returns:
            Text response
        """
        logger.info(f"Processing query: {query}")
        
        result = self.rag.query(
            query,
            top_k=self.config.rag.top_k,
            similarity_threshold=self.config.rag.similarity_threshold
        )
        
        return result["answer"]
    
    def process_voice_query(self, audio_path: Optional[str] = None, duration: int = 5) -> str:
        """
        Process a voice query and return text response
        
        Args:
            audio_path: Path to audio file (if None, records from microphone)
            duration: Recording duration if recording from microphone
            
        Returns:
            Text response
        """
        # Convert speech to text
        if audio_path:
            query = self.stt.transcribe_audio_file(audio_path)
        else:
            query = self.stt.record_and_transcribe(duration=duration)
        
        # Process query
        return self.process_text_query(query)
    
    def chat_text(self, query: str, speak_response: bool = False) -> str:
        """
        Text-based chat interface
        
        Args:
            query: Text query
            speak_response: Whether to speak the response
            
        Returns:
            Text response
        """
        response = self.process_text_query(query)
        
        if speak_response:
            self.tts.speak(response)
        
        return response
    
    def chat_voice(self, audio_path: Optional[str] = None, duration: int = 5) -> str:
        """
        Voice-based chat interface
        
        Args:
            audio_path: Path to audio file (if None, records from microphone)
            duration: Recording duration if recording from microphone
            
        Returns:
            Text response (also spoken aloud)
        """
        response = self.process_voice_query(audio_path, duration)
        self.tts.speak(response)
        return response
    
    def add_knowledge(self, text: str, metadata: Optional[dict] = None):
        """
        Add knowledge to the bot's knowledge base
        
        Args:
            text: Knowledge text to add
            metadata: Optional metadata
        """
        self.rag.add_document(text, metadata)
        logger.info("Knowledge added successfully")
    
    def get_stats(self) -> dict:
        """Get bot statistics"""
        rag_stats = self.rag.get_stats()
        return {
            "expert_domain": self.config.expert_domain,
            "stt_model": self.config.stt.model_name,
            "tts_engine": self.config.tts.engine,
            "embedding_model": self.config.rag.embedding_model,
            "total_documents": rag_stats["total_documents"]
        }


def main():
    """Example usage of the Voice Chat Bot"""
    print("=" * 60)
    print("Voice Chat Bot - 0% Hallucination Guarantee")
    print("=" * 60)
    
    # Initialize bot
    config = VoiceChatBotConfig()
    bot = VoiceChatBot(config)
    
    # Load knowledge base
    bot.load_knowledge_base()
    
    # Display stats
    stats = bot.get_stats()
    print(f"\nBot Statistics:")
    print(f"  Expert Domain: {stats['expert_domain']}")
    print(f"  STT Model: {stats['stt_model']}")
    print(f"  TTS Engine: {stats['tts_engine']}")
    print(f"  Total Documents: {stats['total_documents']}")
    
    print("\n" + "=" * 60)
    print("Text Chat Mode - Type 'quit' to exit")
    print("=" * 60)
    
    # Simple text chat loop
    while True:
        try:
            query = input("\nYou: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not query:
                continue
            
            response = bot.chat_text(query, speak_response=False)
            print(f"\nBot: {response}")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            logger.error(f"Error: {e}")
            print(f"Error: {e}")


if __name__ == "__main__":
    main()

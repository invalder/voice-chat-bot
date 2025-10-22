"""
Configuration for the voice chat bot
"""
from pydantic import BaseModel, Field
from typing import Optional
import yaml
import os


class SpeechToTextConfig(BaseModel):
    """Configuration for speech-to-text"""
    model_name: str = Field(default="tiny", description="Whisper model size: tiny, base, small, medium, large")
    language: Optional[str] = Field(default="en", description="Language code for transcription")
    

class TextToSpeechConfig(BaseModel):
    """Configuration for text-to-speech"""
    engine: str = Field(default="pyttsx3", description="TTS engine: pyttsx3 or gtts")
    rate: int = Field(default=150, description="Speech rate (words per minute)")
    

class RAGConfig(BaseModel):
    """Configuration for Retrieval-Augmented Generation"""
    embedding_model: str = Field(default="all-MiniLM-L6-v2", description="Sentence transformer model")
    chunk_size: int = Field(default=500, description="Document chunk size in characters")
    chunk_overlap: int = Field(default=50, description="Overlap between chunks")
    top_k: int = Field(default=3, description="Number of documents to retrieve")
    similarity_threshold: float = Field(default=0.7, description="Minimum similarity score for retrieval")
    

class VoiceChatBotConfig(BaseModel):
    """Main configuration for voice chat bot"""
    stt: SpeechToTextConfig = Field(default_factory=SpeechToTextConfig)
    tts: TextToSpeechConfig = Field(default_factory=TextToSpeechConfig)
    rag: RAGConfig = Field(default_factory=RAGConfig)
    knowledge_base_path: str = Field(default="knowledge_base", description="Path to knowledge base directory")
    chroma_db_path: str = Field(default="chroma_db", description="Path to ChromaDB storage")
    expert_domain: str = Field(default="general", description="Expert domain for the bot")
    
    @classmethod
    def from_yaml(cls, path: str) -> "VoiceChatBotConfig":
        """Load configuration from YAML file"""
        if os.path.exists(path):
            with open(path, 'r') as f:
                data = yaml.safe_load(f)
                return cls(**data)
        return cls()
    
    def to_yaml(self, path: str):
        """Save configuration to YAML file"""
        with open(path, 'w') as f:
            yaml.dump(self.model_dump(), f, default_flow_style=False)

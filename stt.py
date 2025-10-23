"""
Speech-to-Text module using OpenAI Whisper
Optimized for low resource consumption and high speed
"""
import whisper
import sounddevice as sd
import soundfile as sf
import numpy as np
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class SpeechToText:
    """
    Speech-to-Text converter using Whisper
    Uses tiny model by default for fast, low-resource operation
    """
    
    def __init__(self, model_name: str = "tiny", language: Optional[str] = "en"):
        """
        Initialize STT with specified model
        
        Args:
            model_name: Whisper model size (tiny, base, small, medium, large)
            language: Language code for transcription
        """
        self.model_name = model_name
        self.language = language
        logger.info(f"Loading Whisper model: {model_name}")
        self.model = whisper.load_model(model_name)
        logger.info(f"Whisper model loaded successfully")
        
    def transcribe_audio_file(self, audio_path: str) -> str:
        """
        Transcribe audio from file
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Transcribed text
        """
        logger.info(f"Transcribing audio file: {audio_path}")
        result = self.model.transcribe(
            audio_path,
            language=self.language,
            fp16=False  # Use FP32 for compatibility
        )
        text = result["text"].strip()
        logger.info(f"Transcription: {text}")
        return text
    
    def transcribe_audio_data(self, audio_data: np.ndarray, sample_rate: int = 16000) -> str:
        """
        Transcribe audio from numpy array
        
        Args:
            audio_data: Audio data as numpy array
            sample_rate: Sample rate of audio
            
        Returns:
            Transcribed text
        """
        # Save to temporary file for Whisper
        temp_file = "/tmp/temp_audio.wav"
        sf.write(temp_file, audio_data, sample_rate)
        return self.transcribe_audio_file(temp_file)
    
    def record_and_transcribe(self, duration: int = 5, sample_rate: int = 16000) -> str:
        """
        Record audio from microphone and transcribe
        
        Args:
            duration: Recording duration in seconds
            sample_rate: Sample rate for recording
            
        Returns:
            Transcribed text
        """
        logger.info(f"Recording for {duration} seconds...")
        audio_data = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype='float32'
        )
        sd.wait()
        logger.info("Recording complete")
        
        return self.transcribe_audio_data(audio_data.flatten(), sample_rate)

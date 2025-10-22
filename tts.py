"""
Text-to-Speech module
Supports multiple TTS engines with focus on low resource consumption
"""
import pyttsx3
from gtts import gTTS
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class TextToSpeech:
    """
    Text-to-Speech converter
    Supports pyttsx3 (offline, fast) and gTTS (online, better quality)
    """
    
    def __init__(self, engine: str = "pyttsx3", rate: int = 150):
        """
        Initialize TTS engine
        
        Args:
            engine: TTS engine to use ("pyttsx3" or "gtts")
            rate: Speech rate (words per minute)
        """
        self.engine_type = engine
        self.rate = rate
        
        if engine == "pyttsx3":
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', rate)
            logger.info("Initialized pyttsx3 TTS engine")
        else:
            self.engine = None
            logger.info("Using gTTS engine")
    
    def speak(self, text: str, save_to_file: Optional[str] = None):
        """
        Convert text to speech
        
        Args:
            text: Text to convert to speech
            save_to_file: Optional path to save audio file
        """
        if not text:
            logger.warning("Empty text provided for TTS")
            return
        
        logger.info(f"Speaking: {text}")
        
        if self.engine_type == "pyttsx3":
            if save_to_file:
                self.engine.save_to_file(text, save_to_file)
                self.engine.runAndWait()
            else:
                self.engine.say(text)
                self.engine.runAndWait()
        else:
            # Use gTTS
            tts = gTTS(text=text, lang='en', slow=False)
            if save_to_file:
                tts.save(save_to_file)
                logger.info(f"Saved speech to {save_to_file}")
            else:
                temp_file = "/tmp/temp_speech.mp3"
                tts.save(temp_file)
                # Play the file (platform-dependent)
                os.system(f"mpg123 -q {temp_file} 2>/dev/null || afplay {temp_file} 2>/dev/null || echo 'Audio saved to {temp_file}'")
    
    def set_rate(self, rate: int):
        """Set speech rate"""
        self.rate = rate
        if self.engine_type == "pyttsx3":
            self.engine.setProperty('rate', rate)
    
    def set_voice(self, voice_id: int = 0):
        """Set voice (for pyttsx3)"""
        if self.engine_type == "pyttsx3":
            voices = self.engine.getProperty('voices')
            if voice_id < len(voices):
                self.engine.setProperty('voice', voices[voice_id].id)

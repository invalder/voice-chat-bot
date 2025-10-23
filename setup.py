"""
Setup script for voice-chat-bot
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="voice-chat-bot",
    version="1.0.0",
    author="Voice Chat Bot Contributors",
    description="A voice chat bot with 0% hallucination, low resource consumption, and high speed",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/invalder/voice-chat-bot",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
    ],
    python_requires=">=3.8",
    install_requires=[
        "openai-whisper>=20231117",
        "numpy>=1.21.0",
        "torch>=2.0.0",
        "torchaudio>=2.0.0",
        "pyttsx3>=2.90",
        "gTTS>=2.4.0",
        "chromadb>=0.4.22",
        "sentence-transformers>=2.3.1",
        "sounddevice>=0.4.6",
        "soundfile>=0.12.1",
        "scipy>=1.11.4",
        "python-dotenv>=1.0.0",
        "pydantic>=2.5.3",
        "pyyaml>=6.0.1",
    ],
)

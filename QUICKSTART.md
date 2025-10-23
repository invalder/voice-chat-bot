# Voice Chat Bot - Quick Start Guide

## Installation Steps

### 1. Prerequisites
- Python 3.8 or higher
- pip package manager
- (Optional) Microphone for voice input
- (Optional) Speakers/headphones for voice output

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all necessary packages including:
- Whisper (speech-to-text)
- Sentence Transformers (embeddings)
- ChromaDB (vector database)
- pyttsx3 (text-to-speech)
- And other supporting libraries

### 3. First Run

Create a simple test:

```python
# test_bot.py
from voice_chat_bot import VoiceChatBot

# Initialize
bot = VoiceChatBot()

# Add knowledge
bot.add_knowledge("The sky appears blue due to Rayleigh scattering.")

# Query
response = bot.chat_text("Why is the sky blue?")
print(response)
```

Run it:
```bash
python test_bot.py
```

## Common Use Cases

### Case 1: FAQ Bot

```python
from voice_chat_bot import VoiceChatBot

bot = VoiceChatBot()

# Add FAQ entries
bot.add_knowledge("Our support hours are Monday-Friday, 9 AM to 5 PM EST.")
bot.add_knowledge("To reset your password, click 'Forgot Password' on the login page.")
bot.add_knowledge("We offer free shipping on orders over $50.")

# Query
print(bot.chat_text("What are your support hours?"))
print(bot.chat_text("How do I reset my password?"))
```

### Case 2: Document-Based Bot

```python
from voice_chat_bot import VoiceChatBot
import os

# Create knowledge base
os.makedirs("knowledge_base", exist_ok=True)

# Add a document
with open("knowledge_base/company_info.txt", "w") as f:
    f.write("""
    Our company was founded in 2020 with a mission to provide innovative solutions.
    We specialize in AI and machine learning technologies.
    Our team consists of 50+ experienced engineers and researchers.
    """)

# Initialize and load
bot = VoiceChatBot()
bot.load_knowledge_base()

# Query
print(bot.chat_text("When was the company founded?"))
print(bot.chat_text("How many employees do you have?"))
```

### Case 3: Expert Domain Bot

```python
from voice_chat_bot import VoiceChatBot
from config import VoiceChatBotConfig

# Configure for medical domain
config = VoiceChatBotConfig(
    expert_domain="medical",
    knowledge_base_path="kb/medical"
)

bot = VoiceChatBot(config)

# Add medical knowledge
bot.add_knowledge("Hypertension is high blood pressure, defined as 130/80 mmHg or higher.")
bot.add_knowledge("Treatment for hypertension includes lifestyle changes and medications.")

# Query
response = bot.chat_text("What is hypertension?")
print(response)
```

## Configuration Tips

### Speed Optimization

For fastest response, use:
```yaml
stt:
  model_name: "tiny"  # Fastest Whisper model
rag:
  embedding_model: "all-MiniLM-L6-v2"  # Fast, lightweight
  top_k: 1  # Retrieve fewer documents
```

### Accuracy Optimization

For best accuracy, use:
```yaml
stt:
  model_name: "base"  # More accurate than tiny
rag:
  similarity_threshold: 0.8  # Stricter matching
  top_k: 5  # Retrieve more context
```

### Memory Optimization

For lowest memory usage:
```yaml
stt:
  model_name: "tiny"  # Smallest model (39MB)
rag:
  embedding_model: "all-MiniLM-L6-v2"  # Compact (80MB)
  chunk_size: 300  # Smaller chunks
```

## Troubleshooting

### Issue: "No module named 'whisper'"
**Solution**: Install dependencies
```bash
pip install openai-whisper
```

### Issue: "Could not find model 'tiny'"
**Solution**: Download model manually
```python
import whisper
whisper.load_model("tiny")
```

### Issue: "No audio device found"
**Solution**: For text-only mode, avoid voice methods
```python
# Use text chat instead
response = bot.chat_text("Your question")
```

### Issue: TTS not working
**Solution**: Check TTS engine
```python
# Try alternative engine
from config import VoiceChatBotConfig
config = VoiceChatBotConfig()
config.tts.engine = "gtts"  # Use online TTS
bot = VoiceChatBot(config)
```

## Performance Expectations

| Setup | Response Time | Memory Usage |
|-------|--------------|--------------|
| Minimum (tiny) | <2 seconds | ~200MB |
| Recommended (base) | <3 seconds | ~300MB |
| High Accuracy (small) | <5 seconds | ~500MB |

## Next Steps

1. **Add your domain knowledge**: Create text files in `knowledge_base/`
2. **Customize configuration**: Edit `config.yaml`
3. **Run examples**: `python examples.py`
4. **Test voice mode**: `python voice_chat_bot.py`

## Getting Help

- Check examples.py for more usage patterns
- Read the full README.md for detailed documentation
- Review config.yaml for all configuration options

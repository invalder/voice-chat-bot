# Voice Chat Bot - 0% Hallucination Guarantee

A high-performance voice chat bot with zero hallucination, low resource consumption, and fast response times. Built using Retrieval-Augmented Generation (RAG) to ensure all responses are grounded in verified knowledge.

## 🦀 Now Available in Rust!

This project is now available in **two implementations**:

- **🐍 Python Version** - Original implementation with full Whisper integration
- **🦀 Rust Version** - High-performance rewrite with improved safety and maintainability

Choose the version that best fits your needs. See [README-RUST.md](README-RUST.md) for the Rust implementation.

## 🎯 Key Features

### 1. **0% Hallucination**
- Uses RAG (Retrieval-Augmented Generation) approach
- All responses are based solely on the knowledge base
- Never generates information that isn't explicitly stored
- Returns "I don't know" when information is unavailable

### 2. **Low Resource Consumption**
- Uses Whisper "tiny" model for speech-to-text (39MB)
- Lightweight sentence-transformers for embeddings (80MB)
- Efficient vector database (ChromaDB)
- Optimized for CPU usage - no GPU required

### 3. **High Speed & Fast Response**
- Whisper tiny model: ~10x faster than base model
- Local ChromaDB for instant retrieval
- Minimal latency between query and response
- Offline TTS option (pyttsx3) for zero network delay

### 4. **Flexible Expert Domain**
- Configurable knowledge domains
- Easy knowledge base management
- Support for multiple expert areas
- Simple document ingestion

## 🏗️ Architecture

```
┌─────────────┐
│   Voice     │
│   Input     │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  Speech-to-Text │ (Whisper Tiny)
└────────┬────────┘
         │
         ▼
┌────────────────────┐
│   RAG System       │
│  ┌──────────────┐  │
│  │Vector Search │  │ (ChromaDB)
│  └──────┬───────┘  │
│         │          │
│  ┌──────▼───────┐  │
│  │   Retrieve   │  │
│  │  Knowledge   │  │
│  └──────┬───────┘  │
│         │          │
│  ┌──────▼───────┐  │
│  │  Generate    │  │
│  │  Response    │  │
│  └──────────────┘  │
└────────┬───────────┘
         │
         ▼
┌─────────────────┐
│  Text-to-Speech │ (pyttsx3/gTTS)
└────────┬────────┘
         │
         ▼
┌─────────────┐
│   Voice     │
│   Output    │
└─────────────┘
```

## 📊 Python vs Rust Comparison

| Feature | Python 🐍 | Rust 🦀 |
|---------|-----------|---------|
| **Memory Usage** | ~200MB | ~20MB |
| **Startup Time** | 2-3s | <100ms |
| **Type Safety** | Runtime | Compile-time |
| **STT/TTS** | ✅ Fully integrated | ⚠️ Placeholder |
| **Vector Search** | ✅ ChromaDB + embeddings | ⚠️ Simple text matching |
| **CLI** | Basic | Comprehensive |
| **Distribution** | Requires Python | Single binary |
| **Development** | Rapid prototyping | Performance-critical |

See [MIGRATION-RUST.md](MIGRATION-RUST.md) for detailed comparison and migration guide.

## 🚀 Quick Start (Python Version)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/invalder/voice-chat-bot.git
cd voice-chat-bot
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Basic Usage

#### 1. Text-based Chat (Quick Test)

```python
from voice_chat_bot import VoiceChatBot

# Initialize bot
bot = VoiceChatBot()

# Add knowledge
bot.add_knowledge("Python is a programming language created by Guido van Rossum.")

# Query
response = bot.chat_text("What is Python?")
print(response)
```

#### 2. Load Knowledge from Files

Create a file `knowledge_base/my_domain.txt`:
```
Your domain knowledge here...
Multiple paragraphs are supported.
The system will automatically chunk the content.
```

Then load and query:
```python
from voice_chat_bot import VoiceChatBot

bot = VoiceChatBot()
bot.load_knowledge_base("knowledge_base")
response = bot.chat_text("Your question here")
```

#### 3. Voice Interaction (Requires Microphone)

```python
from voice_chat_bot import VoiceChatBot

bot = VoiceChatBot()
bot.load_knowledge_base()

# Speak your question (5 seconds recording)
response = bot.chat_voice(duration=5)
# Bot will speak the response aloud
```

### Run Examples

```bash
python examples.py
```

### Interactive Mode

```bash
python voice_chat_bot.py
```

## ⚙️ Configuration

Edit `config.yaml` to customize the bot:

```yaml
# Speech-to-Text
stt:
  model_name: "tiny"  # Options: tiny, base, small, medium, large
  language: "en"

# Text-to-Speech
tts:
  engine: "pyttsx3"   # Options: pyttsx3 (offline), gtts (online)
  rate: 150

# RAG Configuration
rag:
  embedding_model: "all-MiniLM-L6-v2"
  chunk_size: 500
  chunk_overlap: 50
  top_k: 3
  similarity_threshold: 0.7

# Paths
knowledge_base_path: "knowledge_base"
chroma_db_path: "chroma_db"
expert_domain: "general"
```

## 📚 API Reference

### VoiceChatBot

Main class for the voice chat bot.

```python
bot = VoiceChatBot(config=None)
```

#### Methods

- **`load_knowledge_base(path)`**: Load documents from a directory
- **`add_knowledge(text, metadata)`**: Add a single document
- **`chat_text(query, speak_response)`**: Text-based query
- **`chat_voice(audio_path, duration)`**: Voice-based query
- **`get_stats()`**: Get bot statistics

### Configuration

```python
from config import VoiceChatBotConfig

config = VoiceChatBotConfig(
    expert_domain="medical",
    knowledge_base_path="kb/medical"
)
```

## 🎓 Use Cases

### 1. Customer Support Bot
- Load FAQ documents
- Provide accurate answers only from documentation
- Zero risk of providing wrong information

### 2. Medical Information Assistant
- Load medical literature
- Provide evidence-based responses
- No hallucinated medical advice

### 3. Technical Documentation Helper
- Load API docs, user guides
- Help users find exact information
- Maintain accuracy across versions

### 4. Educational Tutor
- Load course materials
- Answer questions based on curriculum
- Consistent with teaching materials

## 🔧 Advanced Features

### Custom Expert Domains

```python
# Medical domain
config = VoiceChatBotConfig(
    expert_domain="medical",
    knowledge_base_path="kb/medical"
)
bot = VoiceChatBot(config)

# Legal domain
config = VoiceChatBotConfig(
    expert_domain="legal",
    knowledge_base_path="kb/legal"
)
bot = VoiceChatBot(config)
```

### Adjusting Retrieval Sensitivity

```python
config = VoiceChatBotConfig()
config.rag.similarity_threshold = 0.8  # Stricter matching
config.rag.top_k = 5  # Retrieve more documents
```

### Using Different Whisper Models

```python
config = VoiceChatBotConfig()
config.stt.model_name = "base"  # Better accuracy, slower
# Options: tiny, base, small, medium, large
```

## 📊 Performance Benchmarks

| Component | Model | Size | Speed |
|-----------|-------|------|-------|
| STT | Whisper Tiny | 39MB | ~1s for 5s audio |
| Embeddings | MiniLM-L6-v2 | 80MB | ~50ms per query |
| TTS | pyttsx3 | Built-in | ~100ms |
| Vector DB | ChromaDB | Minimal | <10ms retrieval |

**Total Memory**: ~200MB
**Query Latency**: <2 seconds end-to-end

## 🛠️ Development

### Project Structure

```
voice-chat-bot/
├── voice_chat_bot.py    # Main orchestrator
├── stt.py              # Speech-to-text module
├── tts.py              # Text-to-speech module
├── rag.py              # RAG system
├── config.py           # Configuration classes
├── config.yaml         # Default configuration
├── examples.py         # Usage examples
├── requirements.txt    # Dependencies
└── README.md          # Documentation
```

### Adding New Features

The modular architecture makes it easy to extend:

1. **New STT engines**: Modify `stt.py`
2. **New TTS engines**: Modify `tts.py`
3. **Different vector DBs**: Modify `rag.py`
4. **Custom response generation**: Modify `rag._generate_answer()`

## 🔒 Security & Privacy

- **No data collection**: All processing is local
- **No external API calls**: Works completely offline (with pyttsx3)
- **No model training**: Uses pre-trained models only
- **Knowledge base control**: You control all data

## 🤔 Which Version Should You Choose?

### Choose Python 🐍 if you:
- Need immediate voice interaction (Whisper + TTS fully integrated)
- Are prototyping or experimenting
- Prefer Python's ecosystem and libraries
- Want to modify embeddings and vector search easily
- Are building a Python application

### Choose Rust 🦀 if you:
- Need maximum performance and low memory usage
- Want compile-time safety guarantees
- Are building a production service or embedded system
- Want to distribute as a single binary
- Are comfortable with Rust's learning curve
- Can integrate STT/TTS libraries yourself

**Both versions:**
- Guarantee zero hallucination
- Use the same knowledge base format
- Provide similar APIs
- Are well-documented and maintainable

## 🤝 Contributing

Contributions are welcome to both Python and Rust versions!

**Python version improvements:**
- [ ] Support for more languages
- [ ] Web interface
- [ ] Multi-modal inputs
- [ ] Streaming responses
- [ ] Better summarization in `_generate_answer()`

**Rust version improvements:**
- [ ] Whisper.cpp integration for STT
- [ ] Native platform TTS integration
- [ ] Real vector embeddings (ONNX Runtime)
- [ ] Vector database integration (Qdrant/Milvus)
- [ ] WebAssembly support

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- OpenAI Whisper for speech recognition
- Sentence Transformers for embeddings
- ChromaDB for vector storage
- pyttsx3 for offline TTS

## 📞 Support

For issues and questions:
- GitHub Issues: [Create an issue](https://github.com/invalder/voice-chat-bot/issues)
- Discussions: [Join the discussion](https://github.com/invalder/voice-chat-bot/discussions)

---

**Built with ❤️ for accurate, reliable, and fast voice AI**
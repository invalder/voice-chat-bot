# Quick Start - Rust Version

Get up and running with the Rust Voice Chat Bot in under 5 minutes!

## Prerequisites

- **Rust 1.70+**: Install from [rustup.rs](https://rustup.rs)
- **Git**: For cloning the repository

```bash
# Install Rust (if not already installed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/invalder/voice-chat-bot.git
cd voice-chat-bot
```

### 2. Build the Project

```bash
# Build release version (optimized)
cargo build --release

# Or use the example script to build and test
chmod +x examples-rust.sh
./examples-rust.sh
```

Build time: ~10-20 seconds (first time), <1 second (incremental)

## Quick Test

### Create Sample Knowledge Base

```bash
mkdir -p knowledge_base

cat > knowledge_base/sample.txt << 'EOF'
Rust is a systems programming language that focuses on safety, speed, and concurrency.
It prevents memory errors without needing a garbage collector.
Rust is commonly used for web servers, command-line tools, and embedded systems.
EOF
```

### Load Knowledge

```bash
cargo run --release -- load-knowledge knowledge_base
```

Expected output:
```
INFO Initializing Voice Chat Bot...
INFO Expert domain: general
INFO Loading knowledge base from: knowledge_base
INFO Loaded 1 files from knowledge base
Knowledge base loaded successfully!
Total documents: 2
```

### Query the Bot

```bash
cargo run --release -- query "What is Rust?"
```

Expected output:
```
Bot: Based on my knowledge base:

Rust is a systems programming language that focuses on safety, speed, and concurrency.
It prevents memory errors without needing a garbage collector.
```

### Interactive Chat

```bash
cargo run --release
```

Then type your questions:
```
You: What is Rust?
Bot: Based on my knowledge base: ...

You: Tell me about memory safety
Bot: Based on my knowledge base: ...

You: quit
Goodbye!
```

## Basic Commands

### Interactive Mode (Default)

```bash
cargo run --release
# or
cargo run --release -- chat
```

### Single Query

```bash
cargo run --release -- query "Your question here"
```

### Load Knowledge Base

```bash
cargo run --release -- load-knowledge path/to/knowledge
```

### Show Statistics

```bash
cargo run --release -- stats
```

### Custom Configuration

```bash
cargo run --release -- --config my-config.yaml
```

### Help

```bash
cargo run --release -- --help
```

## Configuration

Create or edit `config-rust.yaml`:

```yaml
# Speech-to-Text (placeholder)
stt:
  model_name: "tiny"
  language: "en"

# Text-to-Speech (placeholder)
tts:
  engine: "native"
  rate: 150

# RAG System
rag:
  embedding_model: "all-MiniLM-L6-v2"
  chunk_size: 500
  chunk_overlap: 50
  top_k: 3
  similarity_threshold: 0.7

# Paths
knowledge_base_path: "knowledge_base"
db_path: "vector_db"
expert_domain: "general"
```

## Running Tests

```bash
# Run all tests
cargo test

# Run with output
cargo test -- --nocapture

# Run specific test
cargo test test_rag_basic
```

Expected: **9 tests passing**

## Development Workflow

### Check Code (Fast)

```bash
cargo check
```

### Format Code

```bash
cargo fmt
```

### Lint Code

```bash
cargo clippy
```

### Build Documentation

```bash
cargo doc --open
```

### Build for Production

```bash
cargo build --release
```

Binary location: `target/release/voice-chat-bot`

### Install Globally

```bash
cargo install --path .
voice-chat-bot --help
```

## Creating Your Own Knowledge Base

### 1. Create Directory

```bash
mkdir -p my_knowledge
```

### 2. Add Text Files

```bash
cat > my_knowledge/topic1.txt << 'EOF'
Your knowledge content here.
Multiple paragraphs are supported.
The system will automatically chunk the content.
EOF

cat > my_knowledge/topic2.txt << 'EOF'
More knowledge content.
Add as many files as you need.
Each file can be about a different topic.
EOF
```

### 3. Load and Query

```bash
# Load
cargo run --release -- load-knowledge my_knowledge

# Query
cargo run --release -- query "Your question about the content"
```

## Customizing the Domain

### Medical Domain Example

```yaml
# config-medical.yaml
expert_domain: "medical"
knowledge_base_path: "knowledge_base/medical"
db_path: "vector_db/medical"
```

```bash
cargo run --release -- --config config-medical.yaml load-knowledge knowledge_base/medical
```

### Legal Domain Example

```yaml
# config-legal.yaml
expert_domain: "legal"
knowledge_base_path: "knowledge_base/legal"
db_path: "vector_db/legal"
```

## Troubleshooting

### Build Fails

```bash
# Update Rust
rustup update

# Clean and rebuild
cargo clean
cargo build --release
```

### Can't Find Knowledge

Check that:
1. Files are in the correct directory
2. Files have `.txt` extension
3. Knowledge was loaded: `cargo run --release -- load-knowledge knowledge_base`

### Low Similarity Scores

Adjust in `config-rust.yaml`:
```yaml
rag:
  similarity_threshold: 0.3  # Lower = more lenient (was 0.7)
  top_k: 5                   # More results (was 3)
```

## Performance Tips

### Optimize Binary Size

```bash
# Strip symbols (Linux/macOS)
strip target/release/voice-chat-bot

# Result: ~1MB binary
```

### Cross-Compilation

```bash
# Install target
rustup target add x86_64-pc-windows-gnu

# Build
cargo build --release --target x86_64-pc-windows-gnu
```

## Next Steps

1. **Add More Knowledge**: Create text files in `knowledge_base/`
2. **Customize Config**: Edit `config-rust.yaml`
3. **Read Documentation**: Check [README-RUST.md](README-RUST.md)
4. **Migrate from Python**: See [MIGRATION-RUST.md](MIGRATION-RUST.md)
5. **Integrate Audio**: Follow integration guides in source code

## Common Use Cases

### Customer Support Bot

```bash
# Load FAQ documents
cargo run --release -- load-knowledge knowledge_base/faq

# Query
cargo run --release -- query "How do I reset my password?"
```

### Technical Documentation Helper

```bash
# Load API docs
cargo run --release -- load-knowledge knowledge_base/api_docs

# Interactive queries
cargo run --release
```

### Educational Tutor

```bash
# Load course materials
cargo run --release -- load-knowledge knowledge_base/course

# Start teaching
cargo run --release
```

## Getting Help

- **Documentation**: `cargo doc --open`
- **Examples**: `./examples-rust.sh`
- **Issues**: [GitHub Issues](https://github.com/invalder/voice-chat-bot/issues)
- **Source Code**: Well-commented, check `src/` directory

## Benchmarks

| Metric | Value |
|--------|-------|
| Binary Size | 1.5MB |
| Memory Usage | ~20MB |
| Startup Time | <100ms |
| Query Time | <50ms |
| Build Time | ~10s (clean) |

---

**Ready to build? Start with: `cargo build --release`**

**Questions? Check [README-RUST.md](README-RUST.md) for detailed documentation!**

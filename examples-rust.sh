#!/bin/bash
# Examples for the Rust Voice Chat Bot

set -e

echo "=================================================="
echo "Voice Chat Bot - Rust Examples"
echo "=================================================="
echo ""

# Build the project first
echo "1. Building the project..."
cargo build --release
echo "✓ Build complete"
echo ""

# Create sample knowledge base
echo "2. Creating sample knowledge base..."
mkdir -p knowledge_base

cat > knowledge_base/rust.txt << 'EOF'
Rust is a systems programming language that focuses on safety, speed, and concurrency. It was created by Graydon Hoare and is now maintained by the Rust Foundation.

Rust provides memory safety without using a garbage collector. This is achieved through its unique ownership system with rules that the compiler checks at compile time.

Key features of Rust include:
- Zero-cost abstractions
- Memory safety without garbage collection
- Concurrency without data races
- Pattern matching and type inference
- Efficient C bindings
- Minimal runtime

Rust is commonly used for systems programming, web servers, command-line tools, embedded systems, and WebAssembly applications.
EOF

cat > knowledge_base/python.txt << 'EOF'
Python is a high-level, interpreted programming language known for its simple and readable syntax. It was created by Guido van Rossum and first released in 1991.

Python emphasizes code readability with its use of significant indentation. It supports multiple programming paradigms including procedural, object-oriented, and functional programming.

Python is widely used for:
- Web development (Django, Flask)
- Data science and machine learning
- Automation and scripting
- Scientific computing
- Artificial intelligence applications

Python has a large standard library and a vast ecosystem of third-party packages available through PyPI.
EOF

echo "✓ Sample knowledge base created"
echo ""

# Load knowledge base
echo "3. Loading knowledge base..."
cargo run --release -- load-knowledge knowledge_base
echo ""

# Show statistics
echo "4. Showing bot statistics..."
cargo run --release -- stats
echo ""

# Run sample queries
echo "5. Running sample queries..."
echo ""

echo "Query 1: What is Rust?"
cargo run --release -- query "What is Rust programming language?"
echo ""

echo "Query 2: Tell me about Python"
cargo run --release -- query "Tell me about Python programming"
echo ""

echo "Query 3: Compare memory safety"
cargo run --release -- query "How does Rust handle memory safety?"
echo ""

# Run tests
echo "6. Running tests..."
cargo test
echo ""

echo "=================================================="
echo "Examples completed successfully!"
echo "=================================================="
echo ""
echo "Try interactive mode:"
echo "  cargo run --release"
echo ""
echo "Or see more options:"
echo "  cargo run --release -- --help"

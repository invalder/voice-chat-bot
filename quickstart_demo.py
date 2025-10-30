#!/usr/bin/env python3
"""
Quick start demonstration script for Voice Chat Bot
Shows how to use the example knowledge base
"""
import os
import sys

def main():
    print("=" * 70)
    print("Voice Chat Bot - Quick Start Demo")
    print("=" * 70)
    
    # Check if knowledge base exists
    kb_path = "knowledge_base"
    if not os.path.exists(kb_path):
        print(f"\n✗ Error: Knowledge base not found at '{kb_path}'")
        sys.exit(1)
    
    # List knowledge base files
    txt_files = [f for f in os.listdir(kb_path) if f.endswith('.txt')]
    print(f"\n✓ Found example knowledge base with {len(txt_files)} files:")
    for i, filename in enumerate(txt_files, 1):
        filepath = os.path.join(kb_path, filename)
        with open(filepath, 'r') as f:
            first_line = f.readline().strip()
        print(f"  {i}. {filename}")
    
    print("\n" + "=" * 70)
    print("Example Usage:")
    print("=" * 70)
    
    print("""
To use the Voice Chat Bot with the example knowledge base:

1. Install dependencies:
   pip install -r requirements.txt

2. Run the example script:
   python examples.py

3. Or use it in your own code:

   from voice_chat_bot import VoiceChatBot
   
   # Initialize bot
   bot = VoiceChatBot()
   
   # Load the example knowledge base
   bot.load_knowledge_base()
   
   # Ask questions
   response = bot.chat_text("What is the Voice Chat Bot?")
   print(response)
   
   response = bot.chat_text("How does zero hallucination work?")
   print(response)

4. Try these example queries:
   - "What is the Voice Chat Bot?"
   - "How does zero hallucination work?"
   - "What are the system requirements?"
   - "Can the bot work offline?"
   - "How do I add my own knowledge?"
   - "What languages are supported?"

5. Add your own knowledge:
   - Create new .txt files in the knowledge_base directory
   - Run bot.load_knowledge_base() to load them
   - Start querying!

For more information, see:
   - README.md - Complete documentation
   - knowledge_base/README.md - Knowledge base guide
   - QUICKSTART.md - Quick start guide
""")
    
    print("=" * 70)
    print("✓ Ready to start! Follow the instructions above.")
    print("=" * 70)

if __name__ == "__main__":
    main()

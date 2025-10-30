# Example Knowledge Base

This directory contains example knowledge files that demonstrate the Voice Chat Bot's capabilities.

## Included Files

- **voice_chat_bot_overview.txt** - General overview of the Voice Chat Bot system, its core principles, and architecture
- **technical_specifications.txt** - Detailed technical specifications including system requirements, model configurations, and performance benchmarks
- **usage_guide.txt** - Comprehensive guide on how to install, configure, and use the Voice Chat Bot
- **faq.txt** - Frequently asked questions and answers about the Voice Chat Bot

## How to Use

These files are automatically loaded when you run:

```python
from voice_chat_bot import VoiceChatBot

bot = VoiceChatBot()
bot.load_knowledge_base()  # Loads all .txt files from this directory
```

## Adding Your Own Knowledge

To add your own knowledge:

1. Create new `.txt` files in this directory
2. Write your content in clear, plain text format
3. Run `bot.load_knowledge_base()` to load the files
4. Start querying your custom knowledge!

## Example Queries

Try asking the bot questions like:

- "What is the Voice Chat Bot?"
- "How does zero hallucination work?"
- "What are the system requirements?"
- "How do I add my own knowledge?"
- "What languages are supported?"
- "Can the bot work offline?"

## File Format

- Use plain text files with `.txt` extension
- Write in clear, complete sentences
- Organize information into logical paragraphs
- The system will automatically chunk large documents
- Each file can contain multiple related topics

## Customization

You can organize knowledge files by topic, domain, or any other categorization that makes sense for your use case. The bot will search across all files to find relevant information.

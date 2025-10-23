"""
Example script showing how to use the Voice Chat Bot
"""
from voice_chat_bot import VoiceChatBot
from config import VoiceChatBotConfig


def example_text_chat():
    """Example of text-based chat"""
    print("=" * 60)
    print("Example 1: Text-based Chat")
    print("=" * 60)
    
    # Initialize bot with default config
    config = VoiceChatBotConfig.from_yaml("config.yaml")
    bot = VoiceChatBot(config)
    
    # Load knowledge base
    bot.load_knowledge_base()
    
    # Add some example knowledge
    bot.add_knowledge(
        "Python is a high-level, interpreted programming language known for its simplicity and readability.",
        metadata={"topic": "python"}
    )
    bot.add_knowledge(
        "Python supports multiple programming paradigms including procedural, object-oriented, and functional programming.",
        metadata={"topic": "python"}
    )
    
    # Query the bot
    queries = [
        "What is Python?",
        "What programming paradigms does Python support?",
        "Tell me about Java"  # This should return "no information"
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        response = bot.chat_text(query)
        print(f"Response: {response}\n")


def example_custom_domain():
    """Example with custom expert domain"""
    print("=" * 60)
    print("Example 2: Custom Expert Domain (Medical)")
    print("=" * 60)
    
    # Create custom config
    config = VoiceChatBotConfig(
        expert_domain="medical",
        knowledge_base_path="knowledge_base/medical"
    )
    
    bot = VoiceChatBot(config)
    
    # Add medical knowledge
    bot.add_knowledge(
        "Aspirin is a nonsteroidal anti-inflammatory drug (NSAID) used to reduce pain, fever, or inflammation.",
        metadata={"category": "medication"}
    )
    bot.add_knowledge(
        "Common side effects of aspirin include stomach upset, heartburn, and increased bleeding risk.",
        metadata={"category": "medication"}
    )
    
    # Query medical information
    query = "What is aspirin?"
    print(f"\nQuery: {query}")
    response = bot.chat_text(query)
    print(f"Response: {response}")
    
    # Show stats
    stats = bot.get_stats()
    print(f"\nBot Stats: {stats}")


def example_adding_from_file():
    """Example of loading knowledge from files"""
    print("=" * 60)
    print("Example 3: Loading from Knowledge Base Files")
    print("=" * 60)
    
    import os
    
    # Create knowledge base directory with sample file
    kb_dir = "knowledge_base"
    os.makedirs(kb_dir, exist_ok=True)
    
    sample_file = os.path.join(kb_dir, "sample_knowledge.txt")
    with open(sample_file, 'w') as f:
        f.write("""
Voice Chat Bot is an advanced conversational AI system designed with three key principles:

1. Zero Hallucination: The bot only provides information from its knowledge base, ensuring 100% accuracy.

2. Low Resource Consumption: Uses lightweight models (Whisper tiny for STT, efficient embeddings for RAG) to minimize memory and CPU usage.

3. High Speed Response: Optimized for fast processing with minimal latency between query and response.

The system uses Retrieval-Augmented Generation (RAG) to ground all responses in verified information, preventing the generation of false or misleading information.
""")
    
    # Initialize and load
    config = VoiceChatBotConfig()
    bot = VoiceChatBot(config)
    bot.load_knowledge_base(kb_dir)
    
    # Query
    query = "What are the key principles of the Voice Chat Bot?"
    print(f"\nQuery: {query}")
    response = bot.chat_text(query)
    print(f"Response: {response}")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Voice Chat Bot - Usage Examples")
    print("=" * 60 + "\n")
    
    try:
        example_text_chat()
        print("\n" + "=" * 60 + "\n")
        
        example_custom_domain()
        print("\n" + "=" * 60 + "\n")
        
        example_adding_from_file()
        
    except Exception as e:
        print(f"Error running examples: {e}")
        import traceback
        traceback.print_exc()

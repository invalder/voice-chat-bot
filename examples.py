"""
Example script showing how to use the Voice Chat Bot
"""
from voice_chat_bot import VoiceChatBot
from config import VoiceChatBotConfig


def example_knowledge_base():
    """Example using the included example knowledge base"""
    print("=" * 60)
    print("Example 1: Using the Example Knowledge Base")
    print("=" * 60)
    
    # Initialize bot with default config
    bot = VoiceChatBot()
    
    # Load the example knowledge base (included in the repository)
    print("\nLoading example knowledge base...")
    bot.load_knowledge_base()
    
    # Show stats
    stats = bot.get_stats()
    print(f"Loaded {stats['total_documents']} documents from knowledge base")
    
    # Query the bot about the Voice Chat Bot itself
    queries = [
        "What is the Voice Chat Bot?",
        "How does zero hallucination work?",
        "What are the system requirements?",
        "Can the bot work offline?"
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        response = bot.chat_text(query)
        # Show only first part of response for readability
        preview = response[:200] + "..." if len(response) > 200 else response
        print(f"Response: {preview}\n")


def example_text_chat():
    """Example of text-based chat"""
    print("=" * 60)
    print("Example 2: Text-based Chat with Custom Knowledge")
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
    print("Example 3: Custom Expert Domain (Medical)")
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
    """Example of adding custom knowledge from files"""
    print("=" * 60)
    print("Example 4: Adding Custom Knowledge")
    print("=" * 60)
    
    import os
    import tempfile
    
    # Create a temporary directory for custom knowledge
    temp_kb_dir = tempfile.mkdtemp(prefix="custom_kb_")
    
    # Add a custom knowledge file
    custom_file = os.path.join(temp_kb_dir, "custom_facts.txt")
    with open(custom_file, 'w') as f:
        f.write("""
Machine Learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed.

Deep Learning is a type of machine learning based on artificial neural networks with multiple layers.

Natural Language Processing (NLP) is a branch of AI that helps computers understand, interpret and manipulate human language.
""")
    
    print(f"\nCreated custom knowledge base in: {temp_kb_dir}")
    
    # Initialize and load
    config = VoiceChatBotConfig()
    bot = VoiceChatBot(config)
    bot.load_knowledge_base(temp_kb_dir)
    
    # Query
    query = "What is Machine Learning?"
    print(f"\nQuery: {query}")
    response = bot.chat_text(query)
    print(f"Response: {response}")
    
    # Cleanup
    import shutil
    shutil.rmtree(temp_kb_dir)
    print(f"\n(Cleaned up temporary directory)")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Voice Chat Bot - Usage Examples")
    print("=" * 60 + "\n")
    
    try:
        # Start with the example knowledge base
        example_knowledge_base()
        print("\n" + "=" * 60 + "\n")
        
        example_text_chat()
        print("\n" + "=" * 60 + "\n")
        
        example_custom_domain()
        print("\n" + "=" * 60 + "\n")
        
        example_adding_from_file()
        
    except Exception as e:
        print(f"Error running examples: {e}")
        import traceback
        traceback.print_exc()

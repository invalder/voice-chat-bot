"""
Basic tests for the Voice Chat Bot
Run with: python test_bot.py
"""
import os
import sys
import tempfile
import shutil


def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    try:
        from config import VoiceChatBotConfig
        from rag import RAGSystem
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False


def test_config():
    """Test configuration system"""
    print("\nTesting configuration...")
    try:
        from config import VoiceChatBotConfig
        
        # Test default config
        config = VoiceChatBotConfig()
        assert config.expert_domain == "general"
        assert config.stt.model_name == "tiny"
        
        # Test custom config
        config2 = VoiceChatBotConfig(expert_domain="medical")
        assert config2.expert_domain == "medical"
        
        print("✓ Configuration tests passed")
        return True
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False


def test_rag_system():
    """Test RAG system without requiring Whisper"""
    print("\nTesting RAG system...")
    try:
        from rag import RAGSystem
        
        # Create temporary directory for test
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Initialize RAG
            rag = RAGSystem(
                chroma_db_path=os.path.join(temp_dir, "test_db"),
                embedding_model="all-MiniLM-L6-v2"
            )
            
            # Add test documents
            rag.add_document(
                "Python is a high-level programming language.",
                metadata={"topic": "python"}
            )
            rag.add_document(
                "Java is an object-oriented programming language.",
                metadata={"topic": "java"}
            )
            
            # Test query
            result = rag.query("What is Python?", top_k=1)
            
            assert "answer" in result
            assert "sources" in result
            assert len(result["sources"]) > 0
            assert "Python" in result["answer"]
            
            # Test stats
            stats = rag.get_stats()
            assert stats["total_documents"] == 2
            
            print("✓ RAG system tests passed")
            return True
            
        finally:
            # Cleanup
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            
    except Exception as e:
        print(f"✗ RAG test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_knowledge_loading():
    """Test loading knowledge from files"""
    print("\nTesting knowledge base loading...")
    try:
        from rag import RAGSystem
        
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Create test knowledge file
            kb_file = os.path.join(temp_dir, "test_knowledge.txt")
            with open(kb_file, 'w') as f:
                f.write("The Earth orbits around the Sun. This takes approximately 365.25 days.")
            
            # Initialize RAG and load file
            rag = RAGSystem(
                chroma_db_path=os.path.join(temp_dir, "test_db")
            )
            
            rag.add_documents_from_file(kb_file, chunk_size=100, chunk_overlap=20)
            
            # Query
            result = rag.query("How long does Earth take to orbit the Sun?")
            assert "answer" in result
            
            print("✓ Knowledge loading tests passed")
            return True
            
        finally:
            # Cleanup
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            
    except Exception as e:
        print(f"✗ Knowledge loading test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_zero_hallucination():
    """Test that bot doesn't hallucinate"""
    print("\nTesting zero hallucination guarantee...")
    try:
        from rag import RAGSystem
        
        temp_dir = tempfile.mkdtemp()
        
        try:
            rag = RAGSystem(chroma_db_path=os.path.join(temp_dir, "test_db"))
            
            # Add specific knowledge
            rag.add_document("The capital of France is Paris.")
            
            # Query about something NOT in knowledge base
            result = rag.query("What is the capital of Germany?", similarity_threshold=0.7)
            
            # Should indicate lack of knowledge
            assert "don't have information" in result["answer"].lower() or len(result["sources"]) == 0
            
            # Query about something IN knowledge base
            result2 = rag.query("What is the capital of France?", similarity_threshold=0.7)
            assert "Paris" in result2["answer"]
            
            print("✓ Zero hallucination tests passed")
            return True
            
        finally:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            
    except Exception as e:
        print(f"✗ Zero hallucination test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Voice Chat Bot - Test Suite")
    print("=" * 60)
    
    results = []
    
    # Run tests that don't require heavy models
    results.append(("Imports", test_imports()))
    results.append(("Configuration", test_config()))
    results.append(("RAG System", test_rag_system()))
    results.append(("Knowledge Loading", test_knowledge_loading()))
    results.append(("Zero Hallucination", test_zero_hallucination()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n❌ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())

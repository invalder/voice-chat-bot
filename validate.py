#!/usr/bin/env python3
"""
Validation script for Voice Chat Bot
Checks code structure and syntax without requiring dependencies
"""
import ast
import os
import sys


def validate_file(filepath):
    """Validate a Python file"""
    try:
        with open(filepath, 'r') as f:
            code = f.read()
        ast.parse(code)
        return True, None
    except SyntaxError as e:
        return False, str(e)


def check_module_structure(filepath, required_items):
    """Check if module has required classes/functions"""
    with open(filepath, 'r') as f:
        code = f.read()
    
    tree = ast.parse(code)
    
    found_items = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            found_items.add(node.name)
        elif isinstance(node, ast.FunctionDef):
            found_items.add(node.name)
    
    missing = set(required_items) - found_items
    return len(missing) == 0, missing


def main():
    """Run validation checks"""
    print("=" * 60)
    print("Voice Chat Bot - Code Validation")
    print("=" * 60)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    files_to_check = {
        'config.py': ['VoiceChatBotConfig', 'SpeechToTextConfig', 'TextToSpeechConfig', 'RAGConfig'],
        'stt.py': ['SpeechToText'],
        'tts.py': ['TextToSpeech'],
        'rag.py': ['RAGSystem'],
        'voice_chat_bot.py': ['VoiceChatBot', 'main'],
        'examples.py': ['example_text_chat', 'example_custom_domain'],
        'test_bot.py': ['test_config', 'test_rag_system', 'run_all_tests'],
    }
    
    all_passed = True
    
    for filename, required_items in files_to_check.items():
        filepath = os.path.join(base_dir, filename)
        
        print(f"\nChecking {filename}...")
        
        # Check syntax
        valid, error = validate_file(filepath)
        if not valid:
            print(f"  ✗ Syntax error: {error}")
            all_passed = False
            continue
        else:
            print(f"  ✓ Syntax valid")
        
        # Check structure
        has_items, missing = check_module_structure(filepath, required_items)
        if not has_items:
            print(f"  ✗ Missing: {missing}")
            all_passed = False
        else:
            print(f"  ✓ Structure valid")
    
    # Check required files exist
    print("\nChecking required files...")
    required_files = [
        'requirements.txt',
        'README.md',
        'QUICKSTART.md',
        'LICENSE',
        'config.yaml',
        '.gitignore',
        'setup.py'
    ]
    
    for filename in required_files:
        filepath = os.path.join(base_dir, filename)
        if os.path.exists(filepath):
            print(f"  ✓ {filename}")
        else:
            print(f"  ✗ {filename} missing")
            all_passed = False
    
    # Check documentation
    print("\nChecking documentation...")
    readme_path = os.path.join(base_dir, 'README.md')
    with open(readme_path, 'r') as f:
        readme_content = f.read()
    
    doc_sections = [
        '0% Hallucination',
        'Low Resource Consumption',
        'High Speed',
        'Quick Start',
        'Configuration',
        'API Reference'
    ]
    
    for section in doc_sections:
        if section in readme_content:
            print(f"  ✓ {section} documented")
        else:
            print(f"  ✗ {section} not found in README")
            all_passed = False
    
    # Summary
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All validation checks passed!")
        print("\nThe voice chat bot is properly structured and ready to use.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run tests: python test_bot.py")
        print("3. Try examples: python examples.py")
        print("4. Start interactive mode: python voice_chat_bot.py")
        return 0
    else:
        print("✗ Some validation checks failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())

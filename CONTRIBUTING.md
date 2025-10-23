# Contributing to Voice Chat Bot

Thank you for your interest in contributing to the Voice Chat Bot project! This document provides guidelines and instructions for contributing.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Making Changes](#making-changes)
5. [Testing](#testing)
6. [Submitting Changes](#submitting-changes)
7. [Coding Standards](#coding-standards)
8. [Areas for Contribution](#areas-for-contribution)

## Code of Conduct

This project follows a simple code of conduct:

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what's best for the community
- Show empathy towards others

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Familiarity with the project architecture (see ARCHITECTURE.md)

### Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR-USERNAME/voice-chat-bot.git
cd voice-chat-bot

# Add upstream remote
git remote add upstream https://github.com/invalder/voice-chat-bot.git
```

## Development Setup

1. **Create a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Install development tools (optional):**

```bash
pip install pytest black flake8 mypy
```

4. **Validate installation:**

```bash
python validate.py
```

## Making Changes

### Branch Strategy

- `main` - Stable release branch
- `develop` - Development branch
- `feature/*` - Feature branches
- `bugfix/*` - Bug fix branches
- `hotfix/*` - Urgent fixes for production

### Creating a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### Commit Messages

Use clear, descriptive commit messages:

```
Add: New feature description
Fix: Bug description
Update: Changes to existing feature
Docs: Documentation changes
Test: Test additions or changes
Refactor: Code improvements
```

Examples:
```
Add: Support for multilingual TTS
Fix: Memory leak in RAG system
Update: Improve embedding model performance
Docs: Add deployment guide for Docker
```

## Testing

### Running Tests

```bash
# Run all tests
python test_bot.py

# Run validation
python validate.py

# Run examples
python examples.py
```

### Writing Tests

Add tests to `test_bot.py`:

```python
def test_your_feature():
    """Test description"""
    # Arrange
    setup_code()
    
    # Act
    result = function_under_test()
    
    # Assert
    assert result == expected_value
    print("✓ Your feature test passed")
    return True
```

### Test Coverage

Aim for:
- Core modules: 80%+ coverage
- New features: 100% coverage
- Bug fixes: Add regression tests

## Submitting Changes

### Before Submitting

1. **Run validation:**
```bash
python validate.py
```

2. **Run tests:**
```bash
python test_bot.py
```

3. **Check code style:**
```bash
black *.py  # Auto-format
flake8 *.py  # Check style
```

4. **Update documentation:**
- Update README.md if needed
- Add docstrings to new functions
- Update ARCHITECTURE.md for structural changes

### Pull Request Process

1. **Update your branch:**
```bash
git fetch upstream
git rebase upstream/main
```

2. **Push to your fork:**
```bash
git push origin feature/your-feature-name
```

3. **Create Pull Request:**
- Go to GitHub
- Click "New Pull Request"
- Select your branch
- Fill in the template

4. **PR Description Template:**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
How was this tested?

## Checklist
- [ ] Tests pass
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No breaking changes
```

## Coding Standards

### Python Style

Follow PEP 8 with these preferences:

```python
# Use descriptive names
def calculate_similarity_score(query, document):
    """
    Calculate similarity between query and document.
    
    Args:
        query: Query string
        document: Document string
        
    Returns:
        float: Similarity score (0-1)
    """
    # Implementation
    pass

# Type hints when helpful
from typing import List, Dict

def process_documents(docs: List[str]) -> Dict[str, float]:
    pass

# Constants in UPPERCASE
MAX_CHUNK_SIZE = 500
DEFAULT_THRESHOLD = 0.7

# Classes in PascalCase
class VoiceChatBot:
    pass

# Functions in snake_case
def load_knowledge_base():
    pass
```

### Documentation

```python
"""
Module-level docstring.

Describes the module's purpose and key components.
"""

class MyClass:
    """
    Class docstring.
    
    Describes the class purpose and usage.
    """
    
    def my_method(self, param: str) -> bool:
        """
        Method docstring.
        
        Args:
            param: Description
            
        Returns:
            Description of return value
            
        Raises:
            ValueError: When something is wrong
        """
        pass
```

### Error Handling

```python
import logging

logger = logging.getLogger(__name__)

def safe_function():
    """Function with proper error handling"""
    try:
        # Risky operation
        result = risky_operation()
        return result
    except SpecificError as e:
        logger.error(f"Specific error occurred: {e}")
        # Handle or re-raise
    except Exception as e:
        logger.exception("Unexpected error")
        raise
```

## Areas for Contribution

### High Priority

1. **Multi-language Support**
   - Add language-specific embeddings
   - Extend TTS for more languages
   - Test with non-English content

2. **Performance Optimization**
   - Optimize embedding generation
   - Improve vector search speed
   - Reduce memory usage

3. **Better Response Generation**
   - Implement lightweight summarization
   - Add citation support
   - Improve answer formatting

### Medium Priority

4. **Web Interface**
   - REST API server
   - WebSocket support for streaming
   - React/Vue frontend

5. **Additional Features**
   - Document format support (PDF, DOCX)
   - Conversation history
   - Multi-turn dialogue

6. **Testing & CI/CD**
   - Expand test coverage
   - Add integration tests
   - Set up GitHub Actions

### Low Priority (Nice to Have)

7. **Alternative Models**
   - Support for other STT engines
   - Different embedding models
   - Custom TTS voices

8. **Monitoring & Analytics**
   - Query logging
   - Performance metrics
   - Usage analytics

9. **Deployment Tools**
   - Docker containers
   - Kubernetes configs
   - Cloud deployment guides

## Specific Contribution Examples

### Example 1: Add New STT Engine

```python
# In stt.py
class CustomSTT:
    def __init__(self):
        # Initialize your STT engine
        pass
    
    def transcribe_audio_file(self, path: str) -> str:
        # Your implementation
        pass
```

### Example 2: Add PDF Support

```python
# In rag.py
def add_documents_from_pdf(self, pdf_path: str):
    """Load documents from PDF file"""
    import PyPDF2
    
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    
    self.add_documents_from_text(text)
```

### Example 3: Add Metrics

```python
# In voice_chat_bot.py
class VoiceChatBot:
    def __init__(self):
        self.metrics = {
            'queries': 0,
            'successful': 0,
            'failed': 0,
            'avg_response_time': 0
        }
    
    def process_text_query(self, query: str) -> str:
        start_time = time.time()
        self.metrics['queries'] += 1
        
        try:
            result = self.rag.query(query)
            self.metrics['successful'] += 1
            return result["answer"]
        except Exception as e:
            self.metrics['failed'] += 1
            raise
        finally:
            elapsed = time.time() - start_time
            self.metrics['avg_response_time'] = (
                (self.metrics['avg_response_time'] * (self.metrics['queries'] - 1) + elapsed)
                / self.metrics['queries']
            )
```

## Questions?

- Open an issue for questions
- Join discussions on GitHub
- Check existing issues and PRs

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- GitHub contributors page

Thank you for contributing to Voice Chat Bot! 🎉

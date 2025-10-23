# Deployment Guide

## Overview

This guide covers deploying the Voice Chat Bot in various environments and configurations.

## System Requirements

### Minimum Requirements
- **CPU**: 2 cores, 2.0 GHz
- **RAM**: 2 GB available
- **Storage**: 500 MB for dependencies + space for knowledge base
- **OS**: Linux, macOS, Windows 10+
- **Python**: 3.8 or higher

### Recommended Requirements
- **CPU**: 4 cores, 2.5 GHz
- **RAM**: 4 GB available
- **Storage**: 2 GB
- **OS**: Ubuntu 20.04+, macOS 12+, Windows 11

### Optional
- Microphone (for voice input)
- Speakers/headphones (for voice output)
- GPU (for faster processing, but not required)

## Installation

### Option 1: Basic Installation (Recommended)

```bash
# Clone repository
git clone https://github.com/invalder/voice-chat-bot.git
cd voice-chat-bot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Validate installation
python validate.py
```

### Option 2: Development Installation

```bash
# Clone repository
git clone https://github.com/invalder/voice-chat-bot.git
cd voice-chat-bot

# Install in development mode
pip install -e .

# Install dev dependencies (if any)
pip install pytest black flake8
```

### Option 3: Docker Deployment (Coming Soon)

```bash
docker pull voice-chat-bot:latest
docker run -v ./knowledge_base:/app/knowledge_base voice-chat-bot
```

## Configuration

### 1. Basic Configuration

Edit `config.yaml`:

```yaml
expert_domain: "your_domain"
knowledge_base_path: "path/to/knowledge"
```

### 2. Advanced Configuration

For production deployment:

```yaml
stt:
  model_name: "base"  # Better accuracy
  language: "en"

tts:
  engine: "pyttsx3"   # Offline, fast
  rate: 150

rag:
  embedding_model: "all-MiniLM-L6-v2"
  chunk_size: 500
  chunk_overlap: 50
  top_k: 3
  similarity_threshold: 0.75  # Adjust based on use case

knowledge_base_path: "/var/lib/voice-chat-bot/kb"
chroma_db_path: "/var/lib/voice-chat-bot/db"
```

## Deployment Scenarios

### Scenario 1: Local Desktop Application

**Use Case**: Personal assistant, learning tool

```python
# app.py
from voice_chat_bot import VoiceChatBot
from config import VoiceChatBotConfig

config = VoiceChatBotConfig.from_yaml("config.yaml")
bot = VoiceChatBot(config)
bot.load_knowledge_base()

# Interactive mode
python voice_chat_bot.py
```

### Scenario 2: REST API Server

**Use Case**: Web application backend

```python
# server.py
from flask import Flask, request, jsonify
from voice_chat_bot import VoiceChatBot

app = Flask(__name__)
bot = VoiceChatBot()
bot.load_knowledge_base()

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    query = data.get('query', '')
    response = bot.chat_text(query)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Scenario 3: Command Line Tool

**Use Case**: Server administration, automation

```bash
#!/bin/bash
# query.sh
python -c "
from voice_chat_bot import VoiceChatBot
bot = VoiceChatBot()
bot.load_knowledge_base()
print(bot.chat_text('$1'))
"
```

Usage: `./query.sh "What is Python?"`

### Scenario 4: Embedded System

**Use Case**: Raspberry Pi, IoT devices

```python
# Optimize for low resources
from config import VoiceChatBotConfig

config = VoiceChatBotConfig(
    stt={"model_name": "tiny"},
    rag={
        "embedding_model": "all-MiniLM-L6-v2",
        "chunk_size": 300,
        "top_k": 1
    }
)
```

## Production Deployment

### 1. Prepare Knowledge Base

```bash
mkdir -p /var/lib/voice-chat-bot/kb
# Add your domain knowledge files
cp domain_knowledge.txt /var/lib/voice-chat-bot/kb/
```

### 2. Configure for Production

```yaml
# config.prod.yaml
stt:
  model_name: "base"
rag:
  similarity_threshold: 0.8  # Stricter for production
knowledge_base_path: "/var/lib/voice-chat-bot/kb"
chroma_db_path: "/var/lib/voice-chat-bot/db"
```

### 3. Set Up as System Service (Linux)

```ini
# /etc/systemd/system/voice-chat-bot.service
[Unit]
Description=Voice Chat Bot Service
After=network.target

[Service]
Type=simple
User=chatbot
WorkingDirectory=/opt/voice-chat-bot
ExecStart=/opt/voice-chat-bot/venv/bin/python server.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable voice-chat-bot
sudo systemctl start voice-chat-bot
```

### 4. Logging Configuration

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/voice-chat-bot.log'),
        logging.StreamHandler()
    ]
)
```

## Performance Tuning

### Memory Optimization

```python
# Use the smallest effective model
config = VoiceChatBotConfig(
    stt={"model_name": "tiny"},
    rag={"embedding_model": "all-MiniLM-L6-v2"}
)

# Limit document cache
import gc
gc.collect()  # Force garbage collection
```

### Speed Optimization

```python
# Reduce retrieval time
config = VoiceChatBotConfig(
    rag={
        "top_k": 1,  # Retrieve fewer documents
        "chunk_size": 300  # Smaller chunks for faster indexing
    }
)
```

### Accuracy Optimization

```python
# Increase model size and retrieval
config = VoiceChatBotConfig(
    stt={"model_name": "base"},
    rag={
        "top_k": 5,
        "similarity_threshold": 0.85
    }
)
```

## Monitoring

### Health Check Endpoint

```python
@app.route('/health')
def health():
    stats = bot.get_stats()
    return jsonify({
        'status': 'healthy',
        'documents': stats['total_documents'],
        'domain': stats['expert_domain']
    })
```

### Metrics to Track

1. **Response Time**: Average query processing time
2. **Query Volume**: Number of queries per hour
3. **Success Rate**: Percentage of queries with valid responses
4. **Memory Usage**: RAM consumption
5. **Document Count**: Size of knowledge base

## Security

### Best Practices

1. **Input Validation**: Sanitize all user inputs
2. **Rate Limiting**: Prevent abuse
3. **Access Control**: Authenticate API requests
4. **Secure Storage**: Encrypt sensitive data
5. **Regular Updates**: Keep dependencies updated

### Example with Rate Limiting

```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/query', methods=['POST'])
@limiter.limit("10 per minute")
def query():
    # ... implementation
```

## Backup and Recovery

### Backup Knowledge Base

```bash
# Backup script
#!/bin/bash
BACKUP_DIR="/backup/voice-chat-bot"
DATE=$(date +%Y%m%d_%H%M%S)

tar -czf $BACKUP_DIR/kb_$DATE.tar.gz /var/lib/voice-chat-bot/kb
tar -czf $BACKUP_DIR/db_$DATE.tar.gz /var/lib/voice-chat-bot/db
```

### Restore

```bash
tar -xzf kb_backup.tar.gz -C /var/lib/voice-chat-bot/
tar -xzf db_backup.tar.gz -C /var/lib/voice-chat-bot/
```

## Troubleshooting

### Common Issues

#### Issue: Out of Memory
**Solution**: Use smaller models
```yaml
stt:
  model_name: "tiny"  # Smallest model
```

#### Issue: Slow Response
**Solution**: Reduce retrieval
```yaml
rag:
  top_k: 1
  chunk_size: 300
```

#### Issue: Poor Accuracy
**Solution**: Increase model size and similarity threshold
```yaml
stt:
  model_name: "base"
rag:
  similarity_threshold: 0.85
```

## Scaling

### Horizontal Scaling

Deploy multiple instances behind a load balancer:

```
Load Balancer
    ├── Instance 1 (bot 1)
    ├── Instance 2 (bot 2)
    └── Instance 3 (bot 3)
```

Each instance can share the same knowledge base (read-only).

### Vertical Scaling

Upgrade to larger models as resources allow:
- tiny → base (2x memory, 2x speed)
- base → small (6x memory, better accuracy)

## Updates and Maintenance

### Updating Knowledge Base

```python
# Add new documents without downtime
bot.add_knowledge("New information...", metadata={"date": "2025-01-01"})
```

### Rolling Updates

1. Deploy new version to staging
2. Test thoroughly
3. Update production instances one at a time
4. Monitor for issues

## Example Production Setup

```bash
# Directory structure
/opt/voice-chat-bot/
├── venv/
├── config.yaml
├── server.py
└── knowledge_base/
    ├── domain1.txt
    ├── domain2.txt
    └── ...

/var/lib/voice-chat-bot/
├── kb/
└── db/

/var/log/
└── voice-chat-bot.log
```

## Support

For deployment assistance:
- GitHub Issues: https://github.com/invalder/voice-chat-bot/issues
- Documentation: See README.md and ARCHITECTURE.md

## Checklist

- [ ] System requirements met
- [ ] Dependencies installed
- [ ] Configuration customized
- [ ] Knowledge base prepared
- [ ] Validation tests passed
- [ ] Security measures implemented
- [ ] Monitoring configured
- [ ] Backup strategy in place
- [ ] Documentation reviewed
- [ ] Production deployment tested

## Next Steps

1. Start with local testing
2. Configure for your use case
3. Load your domain knowledge
4. Test thoroughly
5. Deploy to production
6. Monitor and maintain

---

**Ready to deploy? Run `python validate.py` to ensure everything is set up correctly!**

# Quick Start Guide

## Installation

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 3. Run the application
streamlit run frontend/app.py
```

## Or use the setup script (Windows)

```powershell
.\setup_and_run.ps1
```

## First Time Usage

1. Click "Load Mock Inbox" to import 18 sample emails
2. Click "Process All Emails" to run AI analysis
3. Explore the inbox and see categorization results
4. Navigate to other pages to configure prompts and chat with the agent

## Configuration

Edit `.env` file:

```env
# Choose your LLM provider
LLM_PROVIDER=openai

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini

# Or Anthropic
# LLM_PROVIDER=anthropic
# ANTHROPIC_API_KEY=sk-ant-...

# Or Ollama (local)
# LLM_PROVIDER=ollama
# OLLAMA_MODEL=llama3
```

## Troubleshooting

**API Key Error**: Ensure your API key is valid and has credits

**Module Not Found**: Run `pip install -r requirements.txt`

**Database Locked**: Close other instances of the app

**Port Already in Use**: Run `streamlit run frontend/app.py --server.port 8502`

## Documentation

See `README.md` for complete documentation
See `DEMO_GUIDE.md` for demo instructions

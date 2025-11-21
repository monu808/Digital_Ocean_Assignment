# 🎯 Getting Started - Email Productivity Agent

Welcome! This guide will help you get the Email Productivity Agent up and running in minutes.

---

## ⚡ Quick Setup (5 minutes)

### Option 1: Automated Setup (Windows)

```powershell
# Run the setup script
.\setup_and_run.ps1
```

This script will:
1. Check Python installation
2. Create virtual environment
3. Install dependencies
4. Configure environment
5. Run tests
6. Launch the application

### Option 2: Manual Setup

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and add your API key

# 5. Run the app
streamlit run frontend/app.py
```

---

## 🔑 Getting an API Key

### Google Gemini (Recommended - FREE! 🎉)

1. Go to https://aistudio.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key (starts with `AIza`)
5. Add to `.env`: `GEMINI_API_KEY=AIza...`

**Cost**: FREE! (1,500 requests/day)
**No credit card required!**

👉 **See [GEMINI_SETUP.md](GEMINI_SETUP.md) for detailed instructions**

### OpenAI (Alternative - Paid)

1. Go to https://platform.openai.com/api-keys
2. Create account or sign in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. Add to `.env`: `OPENAI_API_KEY=sk-...`

**Cost**: ~$0.002 per email processed

### Anthropic Claude (Alternative - Paid)

1. Go to https://console.anthropic.com/
2. Sign up for an account
3. Generate API key
4. Set in `.env`:
   ```
   LLM_PROVIDER=anthropic
   ANTHROPIC_API_KEY=sk-ant-...
   ```

### Ollama (Free/Local)

1. Download from https://ollama.ai
2. Install and run: `ollama run llama3`
3. Set in `.env`:
   ```
   LLM_PROVIDER=ollama
   OLLAMA_MODEL=llama3
   ```

---

## 🎮 First Time Usage

### Step 1: Launch the Application

```bash
streamlit run frontend/app.py
```

Your browser will open to `http://localhost:8501`

### Step 2: Load Sample Emails

1. Click **"📥 Load Mock Inbox"** button
2. Wait for confirmation (18 emails loaded)
3. View emails in the inbox list

### Step 3: Process Emails with AI

1. Click **"🔄 Process All Emails"** button
2. Wait for AI to analyze (~30 seconds)
3. See categorization results and action items

### Step 4: Explore Features

**View Processed Emails:**
- Expand any email to see:
  - ✅ Category (Important/Newsletter/Spam/To-Do)
  - 📋 Extracted action items
  - 📝 Auto-generated draft replies

**Configure Prompts:**
- Navigate to **⚙️ Prompt Configuration**
- Edit any prompt template
- Test with sample data

**Chat with Agent:**
- Navigate to **💬 Email Agent Chat**
- Try: "What are my urgent tasks?"
- Try: "Summarize all meeting requests"

**Manage Drafts:**
- Navigate to **📝 Draft Manager**
- Edit, regenerate, or delete drafts

---

## 📋 Common Tasks

### Task 1: Customize Email Categories

```
1. Go to Prompt Configuration
2. Select "Categorization" tab
3. Edit the prompt to add/change categories
4. Click "Save Changes"
5. Go back to Home and click "Process All Emails"
```

### Task 2: Extract Specific Information

```
1. Go to Email Agent Chat
2. Ask: "Find all emails with deadlines"
3. Or: "Show me tasks due this week"
4. Or: "Which emails mention 'budget'?"
```

### Task 3: Generate a Reply

```
1. Find the email you want to reply to
2. Go to Email Agent Chat
3. Ask: "Draft a reply to [sender name]'s email about [topic]"
4. Go to Draft Manager to edit and refine
```

### Task 4: Export Data

```
1. Go to Draft Manager
2. Click "Export All Drafts"
3. Download JSON file with all drafts
```

---

## 🔧 Configuration Options

### LLM Provider Selection

Edit `.env` file:

```env
# Use Google Gemini (FREE! - Recommended for demo/personal use)
LLM_PROVIDER=gemini
GEMINI_API_KEY=AIza...
GEMINI_MODEL=gemini-1.5-flash

# OR use OpenAI (Paid)
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini

# OR use Anthropic (Paid)
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# OR use Ollama (Local/Free but requires setup)
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
```

### Database Location

```env
DATABASE_PATH=data/email_agent.db
```

### Application Settings

```env
MAX_EMAILS_DISPLAY=50
DEBUG_MODE=False
```

---

## 🐛 Troubleshooting

### Issue: "OpenAI API key not found"

**Solution:**
1. Make sure `.env` file exists
2. Check that `OPENAI_API_KEY=sk-...` is set
3. No spaces around the `=` sign
4. Restart the application

### Issue: "Module not found"

**Solution:**
```bash
# Activate virtual environment first
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Then install
pip install -r requirements.txt
```

### Issue: "Database is locked"

**Solution:**
1. Close all other instances of the app
2. Delete `data/email_agent.db`
3. Restart and reload inbox

### Issue: "Port 8501 already in use"

**Solution:**
```bash
# Use a different port
streamlit run frontend/app.py --server.port 8502
```

### Issue: "Cannot execute scripts" (Windows)

**Solution:**
```powershell
# Run this once
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📊 Understanding the Interface

### Home Page
- **Statistics Cards**: Total emails, processed count, pending tasks
- **Category Chart**: Visual breakdown of email types
- **Email List**: Expandable view of all emails
- **Action Buttons**: Load inbox, process emails, clear data

### Prompt Configuration
- **Tabs**: Different prompt types (5 total)
- **Template Editor**: Modify AI behavior
- **Test Interface**: Preview LLM responses
- **Variables**: Use {sender}, {subject}, {body}

### Email Agent Chat
- **Quick Actions**: Pre-defined queries
- **Chat Input**: Type any question
- **Context**: Agent knows your entire inbox
- **Draft Generator**: Create new emails

### Draft Manager
- **Draft List**: All generated drafts
- **Edit Mode**: Modify draft content
- **Actions**: Copy, regenerate, delete
- **Statistics**: Analyze draft patterns

---

## 💡 Pro Tips

### Tip 1: Better Prompts = Better Results
```
❌ Bad: "Categorize this email"
✅ Good: "Categorize into Important/Newsletter/Spam/To-Do based on urgency and content type"
```

### Tip 2: Use Specific Queries
```
❌ Bad: "Show emails"
✅ Good: "Show all Important emails from this week with pending actions"
```

### Tip 3: Iterate on Prompts
1. Edit a prompt
2. Test with sample data
3. Process one email
4. Adjust and repeat

### Tip 4: Save Often
- Changes to prompts are saved immediately
- Drafts are auto-saved
- But export important drafts as backup

### Tip 5: Use Categories Wisely
```
Important: Urgent business matters
To-Do: Actionable requests
Newsletter: Informational content
Spam: Unwanted/suspicious emails
```

---

## 🎓 Learning Resources

### Understanding the Code

**Start Here:**
1. `backend/models/database.py` - Database schema
2. `backend/services/llm_service.py` - LLM integration
3. `frontend/app.py` - Main UI
4. `data/prompt_templates.json` - Example prompts

**Key Concepts:**
- **Services**: Modular business logic
- **Models**: Database structure
- **Prompts**: Control AI behavior
- **Context**: Information passed to LLM

### Extending the Project

**Add a New Prompt Type:**
1. Add to `data/prompt_templates.json`
2. Create method in `llm_service.py`
3. Add UI tab in `prompt_config.py`

**Add a New Category:**
1. Edit categorization prompt
2. Update UI category filters
3. Add new emoji mapping in `helpers.py`

**Integrate Real Email:**
1. Add Gmail API credentials
2. Create `gmail_service.py`
3. Replace mock inbox loading
4. Add send functionality

---

## 📚 Documentation Index

- **README.md**: Complete project documentation
- **QUICKSTART.md**: This file - getting started guide
- **DEMO_GUIDE.md**: Step-by-step demo walkthrough
- **PROJECT_SUMMARY.md**: Technical overview and completion status
- **.env.example**: Configuration template with all options

---

## 🎬 Next Steps

### Beginner Path
1. ✅ Complete setup and load inbox
2. ✅ Process emails and explore results
3. ✅ Try different chat queries
4. ✅ Edit a draft

### Intermediate Path
1. ✅ Customize a prompt template
2. ✅ Test your custom prompt
3. ✅ Process emails with new prompt
4. ✅ Compare results

### Advanced Path
1. ✅ Switch LLM providers
2. ✅ Create custom prompts for your use case
3. ✅ Add new email categories
4. ✅ Integrate with real email (Gmail API)
5. ✅ Deploy to production

---

## 🤝 Getting Help

### Check Documentation
1. Read README.md for detailed info
2. Check DEMO_GUIDE.md for examples
3. Review code comments

### Common Questions

**Q: How much does it cost?**
A: OpenAI: ~$0.002/email. Process 500 emails for $1.

**Q: Is my data secure?**
A: All data stored locally in SQLite. Only email text sent to LLM API.

**Q: Can I use with real email?**
A: Architecture supports it! Add Gmail API integration.

**Q: What if LLM fails?**
A: Graceful fallbacks included. App won't crash.

**Q: Can I customize categories?**
A: Yes! Edit the categorization prompt.

---

## 🎉 You're Ready!

You now have everything you need to use the Email Productivity Agent effectively.

### Quick Command Reference

```bash
# Start the app
streamlit run frontend/app.py

# Run tests
python tests/test_basic.py

# Check structure
tree /F /A

# Install new package
pip install package_name
pip freeze > requirements.txt
```

### Important Files

```
.env                    # Your API keys (don't commit!)
data/email_agent.db    # Your database (auto-created)
data/mock_inbox.json   # Sample emails
```

---

**Need more help?** Check the other documentation files or review the inline code comments.

**Ready to demo?** See DEMO_GUIDE.md for a complete walkthrough.

**Want technical details?** Read PROJECT_SUMMARY.md for architecture info.

---

*Happy email managing! 📧✨*

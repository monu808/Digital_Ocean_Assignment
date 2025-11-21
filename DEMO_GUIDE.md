# Demo Guide for Email Productivity Agent

## Quick Start Demo Script (5-10 minutes)

This guide walks you through demonstrating all key features of the Email Productivity Agent.

---

## Prerequisites Check

Before starting the demo:
- [ ] Python 3.9+ installed
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file configured with API key
- [ ] Application running (`streamlit run frontend/app.py`)

---

## Demo Flow

### Part 1: Introduction (30 seconds)

**What to Say:**
> "This is an intelligent Email Productivity Agent that uses LLMs to automate email management. It can categorize emails, extract action items, generate reply drafts, and provide a chat interface for inbox queries."

**Show:**
- Main landing page
- Highlight the 4 main navigation sections in sidebar

---

### Part 2: Loading & Processing Inbox (2 minutes)

**Steps:**

1. **Click "Load Mock Inbox"**
   - Shows 18 sample emails being loaded
   - Point out the variety: meetings, tasks, newsletters, spam

2. **Show Inbox Overview**
   - Statistics cards update automatically
   - Category breakdown chart appears
   - Scroll through email list

3. **Click "Process All Emails"**
   - Watch AI categorization happen
   - Point out: "The agent is using our custom prompts to analyze each email"
   - Show success message with count

4. **Browse Processed Emails**
   - Expand a few emails to show:
     - ✅ Automatic categorization (Important/To-Do/Newsletter/Spam)
     - 📋 Extracted action items with deadlines
     - 📝 Auto-generated draft replies
   
**What to Highlight:**
- "Each email was analyzed by the LLM using our prompt templates"
- "Action items were automatically extracted with priorities"
- "Draft replies were generated for Important and To-Do emails"

---

### Part 3: Prompt Configuration (2 minutes)

**Steps:**

1. **Navigate to "Prompt Configuration"**
   - Show the 5 different prompt types
   
2. **Select "Categorization" tab**
   - Point out the current prompt template
   - Highlight placeholder variables: `{sender}`, `{subject}`, `{body}`
   
3. **Show Edit Functionality**
   - Scroll through the template
   - Point out the categorization rules
   
4. **Test a Prompt (Optional)**
   - Click "Test This Prompt"
   - Enter sample data:
     - Sender: `boss@company.com`
     - Subject: `URGENT: Project Deadline Moved`
     - Body: `We need to finish by tomorrow!`
   - Click "Test Prompt"
   - Show LLM response: "Important"

5. **Switch to "Action Extraction" tab**
   - Show JSON format prompt
   - Explain: "This extracts tasks, deadlines, and priorities"

**What to Highlight:**
- "All agent behavior is controlled by these editable prompts"
- "Users can customize how emails are categorized"
- "Different prompts for different purposes"
- "Test feature lets you validate changes before applying"

---

### Part 4: Email Agent Chat (2-3 minutes)

**Steps:**

1. **Navigate to "Email Agent Chat"**

2. **Try Quick Actions:**
   - Click "Summarize urgent" button
   - Show AI response listing important emails
   
3. **Ask Custom Questions:**

   **Query 1:** "What tasks do I need to complete this week?"
   - Agent lists action items from To-Do emails
   - Shows deadlines and priorities
   
   **Query 2:** "Show me all meeting requests"
   - Agent searches and summarizes meeting emails
   
   **Query 3:** "Draft a reply to the latest security email"
   - Agent generates a professional response
   - Show how it considers context

4. **Generate New Email Draft**
   - Expand "Generate New Email Draft" section
   - Subject: `Team Update - Project Status`
   - Context: `Write an email updating the team that we completed Phase 1 and are moving to Phase 2`
   - Tone: Professional
   - Click "Generate Draft"
   - Show generated email

**What to Highlight:**
- "Natural language interface - ask anything about your inbox"
- "Agent has access to all email data and categories"
- "Can generate both replies and new emails"
- "Understands context and maintains conversation history"

---

### Part 5: Draft Manager (1-2 minutes)

**Steps:**

1. **Navigate to "Draft Manager"**
   - Show list of all generated drafts

2. **Expand a Draft**
   - Show "In Reply To" section with original email
   - Display draft subject and body

3. **Edit a Draft**
   - Click "Edit" button
   - Make a small change to the text
   - Click "Save Changes"
   - Show update confirmation

4. **Show Additional Features:**
   - Click "Copy" to copy draft
   - Point out "Regenerate" option
   - Show "Delete" functionality

5. **Bulk Actions**
   - Click "Draft Statistics"
   - Show metrics: total drafts, types, tone distribution

**What to Highlight:**
- "All drafts are saved and can be edited"
- "Never sends automatically - always review first"
- "Can regenerate drafts with different AI outputs"
- "Export feature for backing up drafts"

---

## Key Talking Points Throughout Demo

### Architecture Highlights
- "Prompt-driven: All AI behavior is customizable via prompts"
- "Modular backend: Storage, LLM, Email, and Agent services"
- "Flexible LLM support: Works with OpenAI, Anthropic, or local Ollama"

### Safety Features
- "Draft-only mode: Never sends emails automatically"
- "User review required before any email goes out"
- "Graceful error handling for API failures"

### Extensibility
- "Easy to add new prompt types"
- "Can integrate with real email (Gmail API, SMTP)"
- "Database schema supports additional metadata"

---

## Demo Variations

### Quick Demo (3 minutes)
1. Load inbox (30 sec)
2. Process emails, show results (1 min)
3. Chat query example (1 min)
4. Show one draft (30 sec)

### Technical Demo (10 minutes)
- Include prompt editing
- Show test functionality
- Explain LLM integration
- Demonstrate error handling
- Show database structure

### Executive Demo (5 minutes)
- Focus on business value
- Highlight time savings
- Show intelligent categorization
- Demonstrate chat interface
- Emphasize customization

---

## Common Questions & Answers

**Q: What LLM providers are supported?**
A: OpenAI (GPT-4), Anthropic (Claude), and Ollama (local/free). Configured via .env file.

**Q: Can this work with real email?**
A: Yes! The architecture supports Gmail API or SMTP integration. Currently uses mock data for demo.

**Q: How accurate is the categorization?**
A: Very accurate with proper prompts. Users can customize prompts to match their needs.

**Q: Is my data secure?**
A: All data stored locally in SQLite. API calls to LLM providers follow their security standards.

**Q: Can I customize categories?**
A: Yes! Edit the categorization prompt to add/change categories.

**Q: What about attachments?**
A: Current version tracks attachment presence. Full parsing can be added.

---

## Troubleshooting During Demo

### If inbox won't load:
- Check `data/mock_inbox.json` exists
- Verify database permissions

### If processing fails:
- Check API key in `.env`
- Verify internet connection
- Show error handling gracefully

### If chat doesn't respond:
- Check LLM service connection
- Test with simple query first
- Show fallback behavior

---

## Post-Demo Follow-Up

**Show These Files:**
- `README.md` - Complete documentation
- `data/mock_inbox.json` - Sample data structure
- `data/prompt_templates.json` - Prompt examples
- `.env.example` - Configuration template

**Mention These Features:**
- Comprehensive test suite in `tests/`
- Modular architecture for easy extension
- Clear separation of concerns
- Production-ready error handling

---

## Recording Tips

For video demo recording:

1. **Use Screen Recording Software**: OBS Studio, Loom, or built-in tools
2. **Set Resolution**: 1920x1080 recommended
3. **Clean Browser**: Close unnecessary tabs
4. **Prepare Script**: Follow this guide
5. **Test Audio**: Check microphone levels
6. **Rehearse**: Do a practice run
7. **Keep it Concise**: 5-10 minutes is ideal
8. **Show Enthusiasm**: Demo with energy!

---

## Demo Completion Checklist

After demo, ensure you've shown:
- ✅ Loading mock inbox
- ✅ Email processing with AI
- ✅ Categorization results
- ✅ Action item extraction
- ✅ Prompt configuration
- ✅ Prompt testing
- ✅ Chat agent queries
- ✅ Draft generation
- ✅ Draft editing
- ✅ Statistics and metrics

---

**🎉 You're ready to give an impressive demo!**

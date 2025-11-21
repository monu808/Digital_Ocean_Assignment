# Email Productivity Agent 📧🤖

An intelligent, prompt-driven Email Productivity Agent that processes your inbox using LLMs to automate email categorization, action-item extraction, and draft generation.

## Features

- **🏷️ Smart Email Categorization**: Automatically categorize emails (Important, Newsletter, Spam, To-Do)
- **✅ Action Item Extraction**: Extract tasks and deadlines from emails
- **✉️ Auto-Draft Replies**: Generate intelligent reply drafts based on context
- **💬 Chat-Based Inbox Interaction**: Ask questions about your emails naturally
- **🎯 Prompt-Driven Architecture**: Fully customizable behavior via user-defined prompts
- **🔒 Safe Draft Mode**: Never sends emails automatically - all drafts are saved for review

## Architecture

```
Ocean-Digital/
├── backend/                # Backend services
│   ├── models/            # Database models
│   ├── services/          # Business logic
│   └── utils/             # Helper functions
├── frontend/              # Streamlit UI
│   └── pages/            # UI pages
├── data/                 # Data storage
│   ├── mock_inbox.json   # Sample emails
│   └── prompt_templates.json  # Default prompts
├── tests/                # Unit tests
└── README.md            # This file
```

## Setup Instructions

### Prerequisites

- Python 3.9 or higher
- OpenAI API key (or Anthropic/Ollama for alternatives)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Ocean-Digital
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your API key
   # OPENAI_API_KEY=sk-...
   ```

### Running the Application

1. **Start the Streamlit UI**
   ```bash
   streamlit run frontend/app.py
   ```

2. **Access the application**
   - Open your browser to `http://localhost:8501`

## Usage Guide

### 1. Loading the Mock Inbox

- Navigate to the **Home** page
- Click "Load Mock Inbox" to import sample emails
- The system will automatically:
  - Load 15+ sample emails
  - Initialize the database
  - Display emails in the inbox viewer

### 2. Configuring Prompts

Navigate to **Prompt Configuration** page to customize agent behavior:

#### Categorization Prompt
Controls how emails are classified into categories (Important, Newsletter, Spam, To-Do).

**Default Example:**
```
Categorize this email into one of: Important, Newsletter, Spam, To-Do.
To-Do emails must include a direct request requiring user action.
Respond with just the category name.
```

#### Action Item Extraction Prompt
Defines how tasks and deadlines are extracted from emails.

**Default Example:**
```
Extract action items from this email. Respond in JSON format:
{
  "tasks": [
    {"task": "description", "deadline": "date or null", "priority": "high/medium/low"}
  ]
}
```

#### Auto-Reply Draft Prompt
Guides the generation of reply drafts.

**Default Example:**
```
Draft a professional reply to this email. Consider the context and tone.
If it's a meeting request, ask for an agenda.
If it's a task request, acknowledge and provide estimated timeline.
```

### 3. Email Processing

After loading emails:
- View categorized emails in the inbox
- Click on any email to see details
- View extracted action items
- Check auto-generated draft suggestions

### 4. Using the Email Agent Chat

Navigate to **Email Agent** page:

**Example Queries:**
- "Summarize all urgent emails"
- "What tasks do I need to complete this week?"
- "Show me all meeting requests"
- "Draft a reply to the project update email"
- "Which emails require immediate attention?"

### 5. Managing Drafts

Navigate to **Draft Manager** page:
- View all generated drafts
- Edit draft content
- Save updated drafts
- Copy to clipboard for sending via your email client

## Mock Inbox Content

The mock inbox includes 15+ diverse emails:

- **Meeting Requests**: Team sync, client calls
- **Newsletters**: Industry updates, marketing emails
- **Spam**: Promotional offers, suspicious emails
- **Task Requests**: Code reviews, report submissions
- **Project Updates**: Status reports, milestone notifications

## Configuration Options

### LLM Provider Selection

Edit `.env` to choose your LLM provider:

**OpenAI (Recommended)**
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
```

**Anthropic Claude**
```env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

**Google Gemini (FREE with generous limits!)**
```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_api_key
GEMINI_MODEL=gemini-1.5-flash
```

**Ollama (Local/Free)**
```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
```

## Project Structure Details

### Backend Services

- **`storage_service.py`**: SQLite database operations
- **`llm_service.py`**: LLM API integration (OpenAI/Anthropic/Ollama)
- **`prompt_service.py`**: Prompt CRUD operations
- **`email_service.py`**: Email loading and parsing
- **`agent_service.py`**: Email processing pipeline orchestration

### Database Schema

- **emails**: Stores email content and metadata
- **prompts**: Stores user-defined prompt templates
- **categories**: Stores categorization results
- **action_items**: Stores extracted tasks
- **drafts**: Stores generated email drafts

## API Examples

### Programmatic Usage

```python
from backend.services.agent_service import AgentService
from backend.services.storage_service import StorageService

# Initialize services
storage = StorageService()
agent = AgentService(storage)

# Load inbox
agent.load_mock_inbox()

# Process emails
agent.process_all_emails()

# Query agent
response = agent.chat_query("What are my urgent tasks?")
print(response)
```

## Troubleshooting

### Common Issues

1. **API Key Error**
   - Ensure `.env` file exists and contains valid API key
   - Check API key has sufficient credits

2. **Database Lock Error**
   - Close all other instances of the app
   - Delete `data/email_agent.db` and restart

3. **Module Import Error**
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt` again

4. **Streamlit Port Already in Use**
   - Use: `streamlit run frontend/app.py --server.port 8502`

## Testing

Run the test suite:

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=backend tests/
```

## Safety Features

- **No Automatic Sending**: All emails are saved as drafts only
- **User Review Required**: Drafts must be manually sent
- **Error Handling**: Graceful LLM failure handling
- **Rate Limiting**: Prevents API overuse

## Demo Video

[Link to demo video will be provided]

**Demo covers:**
- Loading mock inbox
- Creating custom prompts
- Email ingestion and categorization
- Action item extraction
- Chat-based queries
- Draft generation

## Future Enhancements

- [ ] Real Gmail/Outlook integration
- [ ] Multi-language support
- [ ] Email threading/conversation view
- [ ] Advanced filters and search
- [ ] Calendar integration
- [ ] Attachment handling
- [ ] Email templates library

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ using Streamlit, OpenAI, and Python**

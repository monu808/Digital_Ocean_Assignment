# 🆓 Using Google Gemini API (FREE!)

## Why Gemini?

- **FREE**: Generous free tier (15 requests/minute, 1500 requests/day for Gemini 1.5 Flash)
- **Fast**: Gemini 1.5 Flash is optimized for speed
- **Capable**: Excellent performance for email processing
- **No Credit Card Required**: Start immediately

---

## Quick Setup (3 steps)

### Step 1: Get Your Free API Key

1. Go to **[Google AI Studio](https://aistudio.google.com/app/apikey)**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the API key (starts with `AIza...`)

**That's it! No credit card, no payment setup required.**

---

### Step 2: Configure Your Project

Edit your `.env` file:

```env
# Use Google Gemini (FREE!)
LLM_PROVIDER=gemini
GEMINI_API_KEY=AIzaSyD...your_actual_key_here
GEMINI_MODEL=gemini-1.5-flash
```

---

### Step 3: Install & Run

```bash
# Install dependencies (includes google-generativeai)
pip install -r requirements.txt

# Run the app
streamlit run frontend/app.py
```

---

## Available Gemini Models

### Gemini 1.5 Flash (Recommended - FREE)
- **Model**: `gemini-1.5-flash`
- **Speed**: Very fast
- **Use case**: Perfect for email processing
- **Free tier**: 15 RPM, 1500 RPD
- **Best for**: This project! ✅

### Gemini 1.5 Pro
- **Model**: `gemini-1.5-pro`
- **Speed**: Slower but more capable
- **Free tier**: 2 RPM, 50 RPD
- **Best for**: Complex analysis

### Gemini 1.0 Pro
- **Model**: `gemini-pro`
- **Speed**: Fast
- **Free tier**: 60 RPM
- **Best for**: Simple tasks

**For this email agent, use `gemini-1.5-flash` - it's fast and free!**

---

## Free Tier Limits

### Gemini 1.5 Flash
- 15 requests per minute
- 1,500 requests per day
- 1 million tokens per minute

**This is enough for:**
- Processing 100+ emails per day
- Hundreds of chat queries
- Testing and development
- Personal use

---

## Comparison: Gemini vs Others

| Feature | Gemini 1.5 Flash | OpenAI GPT-4o-mini | Anthropic Claude |
|---------|------------------|-------------------|------------------|
| **Cost** | 🟢 FREE | 🟡 $0.15/1M tokens | 🟡 $3/1M tokens |
| **Speed** | 🟢 Very Fast | 🟢 Fast | 🟡 Medium |
| **Setup** | 🟢 No card needed | 🔴 Card required | 🔴 Card required |
| **Free tier** | 🟢 1500 req/day | 🟡 $5 credit | 🟡 Limited |
| **Quality** | 🟢 Excellent | 🟢 Excellent | 🟢 Excellent |

**Winner for this project: Gemini! 🏆**

---

## Example .env Configuration

```env
# Google Gemini Configuration (FREE!)
LLM_PROVIDER=gemini
GEMINI_API_KEY=AIzaSyD...your_actual_key_here
GEMINI_MODEL=gemini-1.5-flash

# Database Configuration
DATABASE_PATH=data/email_agent.db

# Application Settings
MAX_EMAILS_DISPLAY=50
DEBUG_MODE=False
```

---

## Testing Your Setup

Run this quick test:

```python
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Configure
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Test
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content('Say hello!')
print(response.text)
```

If you see "Hello!" or similar, you're good to go! ✅

---

## Troubleshooting

### Error: "API key not found"
**Solution**: Make sure `.env` file has `GEMINI_API_KEY=AIza...`

### Error: "Module not found: google.generativeai"
**Solution**: 
```bash
pip install google-generativeai
# or
pip install -r requirements.txt
```

### Error: "Quota exceeded"
**Solution**: You've hit the free tier limit. Wait a bit or upgrade to paid tier.

### Error: "Invalid API key"
**Solution**: 
1. Check the key is correct (no spaces)
2. Regenerate key at [Google AI Studio](https://aistudio.google.com/app/apikey)

---

## Rate Limiting

The free tier has limits:
- **15 requests per minute**
- **1,500 requests per day**

**If you hit the limit:**
1. Wait a minute (for RPM limit)
2. Try again tomorrow (for daily limit)
3. Or upgrade to paid tier (still very cheap!)

**For normal use, you won't hit these limits.**

---

## Performance Tips

### 1. Use gemini-1.5-flash
It's optimized for speed and works great for email processing.

### 2. Batch Operations
Process multiple emails in one go rather than one-by-one.

### 3. Cache Results
The app already caches in database, so re-processing is fast.

### 4. Optimize Prompts
Shorter prompts = faster responses = lower quota usage.

---

## Cost Comparison

### Processing 100 emails:

**With Gemini 1.5 Flash:**
- Cost: $0.00 (FREE!) 🎉
- Requests: ~100-200 (well within free tier)

**With OpenAI GPT-4o-mini:**
- Cost: ~$0.02-0.05
- Requires credit card

**With Anthropic Claude:**
- Cost: ~$0.30-0.50
- Requires credit card

**Gemini wins for personal/demo use!**

---

## Upgrading to Paid (Optional)

If you need more than 1,500 requests/day:

1. Enable billing in Google Cloud Console
2. Pay-as-you-go pricing:
   - Gemini 1.5 Flash: $0.075 per 1M input tokens
   - Still cheaper than OpenAI/Anthropic!

But for this project, **free tier is more than enough!**

---

## Why This Works So Well

### Perfect Match
- Email processing doesn't need the most powerful model
- Gemini 1.5 Flash is fast and accurate
- Free tier is generous
- No payment setup needed

### Demo Ready
- Show the project without spending money
- Process hundreds of emails for free
- Test and iterate unlimited times (within rate limits)

### Production Ready
- If you go over free tier, costs are low
- Easy to upgrade when needed
- Reliable Google infrastructure

---

## Getting Your API Key (Detailed Steps)

1. **Visit Google AI Studio**
   - URL: https://aistudio.google.com/app/apikey
   - Or Google "Google AI Studio API key"

2. **Sign In**
   - Use any Google account
   - No payment info needed

3. **Create API Key**
   - Click "Create API Key" button
   - Choose "Create API key in new project" (easiest)
   - Or select existing Google Cloud project

4. **Copy Key**
   - Key format: `AIzaSyD...` (37 characters)
   - Click copy button
   - Save it securely

5. **Add to .env**
   ```env
   GEMINI_API_KEY=AIzaSyD...your_key_here
   ```

6. **Done!**
   - No verification needed
   - Start using immediately

---

## Quick Start Commands

```bash
# 1. Configure
echo "LLM_PROVIDER=gemini" >> .env
echo "GEMINI_API_KEY=your_key_here" >> .env
echo "GEMINI_MODEL=gemini-1.5-flash" >> .env

# 2. Install
pip install google-generativeai

# 3. Run
streamlit run frontend/app.py
```

---

## FAQs

**Q: Is Gemini really free?**
A: Yes! 1,500 requests/day free forever.

**Q: Do I need a credit card?**
A: No! Just a Google account.

**Q: How does it compare to ChatGPT?**
A: Very similar quality for this use case.

**Q: Will I hit the rate limits?**
A: Unlikely for personal use. 1,500/day is generous.

**Q: Can I use it commercially?**
A: Free tier is for testing. Paid tier for production.

**Q: What about privacy?**
A: Same as OpenAI/Anthropic - read Google's terms.

---

## Recommended Setup for Demo

```env
# Best setup for assignment demo
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-1.5-flash
```

**Why?**
- ✅ Free - no costs!
- ✅ Fast - quick demos
- ✅ Reliable - Google infrastructure
- ✅ Easy - no payment setup
- ✅ Generous - 1,500 requests/day

---

## Next Steps

1. ✅ Get your free API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. ✅ Add to `.env` file
3. ✅ Run `pip install -r requirements.txt`
4. ✅ Start the app: `streamlit run frontend/app.py`
5. ✅ Process your emails for free!

---

**🎉 Congratulations! You now have a completely free LLM-powered email agent!**

No credit card, no payment, no worries. Just pure AI magic! ✨

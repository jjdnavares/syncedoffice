# SO Writer - Quick Start Guide

## 🚀 Installation (5 minutes)

```bash
# 1. Install Python dependencies (optional)
pip install openai anthropic google-generativeai

# 2. Build frontend
cd /home/jumes/bench/apps/syncedoffice/syncedoffice/so_writer/frontend
yarn install && yarn build

# 3. Run migrations
cd /home/jumes/bench
bench --site [site-name] migrate

# 4. Clear cache and restart
bench --site [site-name] clear-cache
bench restart
```

## 🌐 Access

Navigate to: **`http://[your-site]/so_writer`**

## ⚙️ Configuration

### Option 1: System-Wide (Recommended)
1. Go to: **SO Writer → LLM System Settings**
2. Add provider (e.g., "openai")
3. Enter API key
4. Save

### Option 2: User-Specific
1. Go to: **SO Writer → LLM Settings**
2. Create new record for your user
3. Add provider settings
4. Save

## 📝 Generate Content (Web UI)

1. Select **LLM Provider** (e.g., OpenAI)
2. Select **Model** (e.g., gpt-4)
3. Enter **API Key** (if not configured)
4. Fill in:
   - **Keyword**: "AI automation"
   - **Content Type**: Blog Post
   - **Tone**: Professional
5. Click **Generate Content**
6. Wait ~30-60 seconds
7. View, copy, or save your content

## 🔧 Workflow Integration

```python
from syncedoffice.so_writer.workflow_hook import generate_content_for_workflow

# Generate content in your workflow
result = generate_content_for_workflow(
    keyword="digital marketing",
    content_type="Blog Post",
    tone="professional",
    provider="openai",
    model="gpt-4",
    save_to_db=True
)

# Access the result
content = result["generated_text"]
doc_name = result["name"]  # If saved to DB
```

## 🎯 Quick Generate (Custom Prompt)

```python
from syncedoffice.so_writer.workflow_hook import quick_generate

result = quick_generate(
    prompt="Write a 500-word article about renewable energy",
    provider="openai",
    model="gpt-4"
)

content = result["generated_text"]
```

## 📊 Supported Providers

| Provider | Model Examples |
|----------|---------------|
| OpenAI | gpt-4, gpt-4-turbo, gpt-3.5-turbo |
| Anthropic | claude-3-opus, claude-3-sonnet |
| Google | gemini-pro, gemini-1.5-pro |
| Groq | llama3-70b-8192, mixtral-8x7b |
| Mistral | mistral-large, mistral-medium |
| Ollama | Any local model |
| Others | Cohere, Perplexity, Together, Bedrock, OpenRouter |

## 📋 Content Types

- **Blog Post** (1,500 words)
- **Article** (2,000 words)
- **Product Description** (500 words)
- **Landing Page** (1,000 words)
- **SEO Meta Description** (150 chars)
- **Social Media Post** (800 words)
- **Blog Outline** (600 words)

## 🎨 Available Tones

- Professional
- Casual
- Friendly
- Authoritative
- Witty

## 🔍 Troubleshooting

### Frontend not loading?
```bash
cd syncedoffice/so_writer/frontend
yarn build
bench --site [site] clear-cache
```

### API key error?
- Check LLM Settings or LLM System Settings
- Verify provider name is lowercase
- Ensure API key is valid

### Generation fails?
- Check Error Log in Frappe
- Verify internet connection
- Confirm API key has credits
- Check model name is correct

## 📚 Documentation

- **README.md** - Full API reference
- **SETUP.md** - Detailed setup guide
- **IMPLEMENTATION_SUMMARY.md** - Technical details
- **workflow_node_example.py** - Integration examples

## 💡 Pro Tips

1. **System API Keys**: Set once, use for all users
2. **Humanization**: Content goes through 2-pass generation for natural output
3. **History**: All content saved automatically, access via History tab
4. **Workflow**: Use hooks for automated content generation
5. **Custom Prompts**: Use `quick_generate()` for flexibility

## 🆘 Need Help?

1. Check Error Log: **Tools → Error Log**
2. Review documentation in module folder
3. Test with OpenAI first (most reliable)
4. Verify API key and credits

## ✅ Quick Test

```python
# Test in Frappe console
import frappe
from syncedoffice.so_writer.api import generate_content

doc = generate_content(
    keyword="test",
    content_type="blog-post",
    tone="casual",
    provider="openai",
    model="gpt-3.5-turbo"
)

print(doc.generated_text[:100])  # First 100 chars
```

---

**Ready to generate amazing content! 🎉**

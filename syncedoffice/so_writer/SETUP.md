# SO Writer Setup Guide

## Installation Steps

### 1. Install Python Dependencies (Optional)

Install the LLM provider libraries you plan to use:

```bash
# For OpenAI
pip install openai

# For Anthropic
pip install anthropic

# For Google Generative AI
pip install google-generativeai

# For Amazon Bedrock
pip install boto3
```

### 2. Run Database Migrations

```bash
cd /home/jumes/bench
bench --site [your-site-name] migrate
```

This will create the following DocTypes:
- Generated Content
- LLM Settings
- LLM System Settings
- LLM Provider Setting

### 3. Build Frontend

```bash
cd /home/jumes/bench/apps/syncedoffice/syncedoffice/so_writer/frontend
yarn install
yarn build
```

The build process will:
- Install all npm dependencies
- Build the Vue application
- Copy files to `/home/jumes/bench/apps/syncedoffice/syncedoffice/public/writer/`
- Create the HTML entry point at `/home/jumes/bench/apps/syncedoffice/syncedoffice/www/writer.html`

### 4. Clear Cache and Restart

```bash
cd /home/jumes/bench
bench --site [your-site-name] clear-cache
bench restart
```

### 5. Access the Application

Navigate to: `http://[your-site-url]/writer`

## Configuration

### System-Level API Keys (Recommended for shared environments)

1. Go to: **SO Writer > LLM System Settings**
2. Add provider settings with API keys
3. These keys will be available to all users

### User-Level API Keys (For individual users)

1. Go to: **SO Writer > LLM Settings**
2. Create a new record for your user
3. Add provider settings with your personal API keys

## Usage

### Via Web Interface

1. Access `/writer` in your browser
2. Select your LLM provider and model
3. Enter your API key (if not configured system-wide)
4. Fill in the content generation form:
   - Target keyword or phrase
   - Content type (Blog Post, Article, etc.)
   - Tone of voice
5. Click "Generate Content"
6. View, copy, or delete generated content
7. Access history from the History tab

### Via Workflow Nodes

Use the workflow hooks in your custom nodes:

```python
from syncedoffice.so_writer.workflow_hook import generate_content_for_workflow

# Generate content
result = generate_content_for_workflow(
    keyword="AI automation",
    content_type="Blog Post",
    tone="professional",
    provider="openai",
    model="gpt-4",
    save_to_db=True  # Optional: save to database
)

# Access the generated content
content = result["generated_text"]
doc_name = result.get("name")  # If saved to DB
```

### Via Python API

```python
import frappe
from syncedoffice.so_writer.api import generate_content

# Generate content
doc = generate_content(
    keyword="Digital Marketing",
    content_type="blog-post",
    tone="professional",
    provider="openai",
    model="gpt-4"
)

# Access the generated content
print(doc.generated_text)
```

## Troubleshooting

### Frontend not loading

1. Check if files exist in `/home/jumes/bench/apps/syncedoffice/syncedoffice/public/so_writer/`
2. Rebuild frontend: `cd frontend && yarn build`
3. Clear cache: `bench --site [site] clear-cache`

### API Key errors

1. Verify API key is set in LLM Settings or LLM System Settings
2. Check provider name matches exactly (lowercase)
3. Ensure the provider's Python library is installed

### Content generation fails

1. Check Error Log in Frappe
2. Verify API key is valid and has credits
3. Ensure the model name is correct for the provider
4. Check internet connectivity for API calls

### Workflow integration issues

1. Verify the workflow node is registered
2. Check that the handler path is correct
3. Review workflow execution logs

## Development

### Frontend Development

```bash
cd /home/jumes/bench/apps/syncedoffice/syncedoffice/so_writer/frontend
yarn dev
```

This starts a development server with hot reload.

### Adding New LLM Providers

1. Add provider handler in `api.py`:
   ```python
   def _call_newprovider_llm(prompt: str, model: str, api_key: str) -> str:
       # Implementation
       pass
   ```

2. Add provider to `LLM_PROVIDERS` in `frontend/src/lib/api.js`

3. Add models to `LLM_MODELS` in `frontend/src/lib/api.js`

### Adding New Content Types

1. Add prompt template to `prompts.py` in `CONTENT_PROMPTS` dict
2. Update frontend select options in `WriterSettings.vue`

## File Structure

```
syncedoffice/so_writer/
├── __init__.py
├── api.py                      # Backend API functions
├── prompts.py                  # Content generation prompts
├── workflow_hook.py            # Workflow integration hooks
├── workflow_node_example.py    # Example workflow nodes
├── README.md                   # Module documentation
├── SETUP.md                    # This file
├── doctype/                    # Frappe DocTypes
│   ├── generated_content/
│   ├── llm_settings/
│   ├── llm_system_settings/
│   └── llm_provider_setting/
└── frontend/                   # Vue 3 application
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   ├── lib/
    │   └── App.vue
    ├── package.json
    └── vite.config.js
```

## Support

For issues or questions:
1. Check the Error Log in Frappe
2. Review the README.md for API documentation
3. Check workflow_node_example.py for integration examples

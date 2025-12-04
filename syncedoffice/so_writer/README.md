# SO Writer Module

Content generation module for SyncedOffice using LLM providers.

## Features

- **Multiple LLM Providers**: Support for OpenAI, Anthropic, Google, Groq, Mistral, and more
- **Content Types**: Blog posts, articles, product descriptions, landing pages, SEO meta descriptions, social media posts, and blog outlines
- **Tone Customization**: Professional, casual, friendly, authoritative, and witty tones
- **Content Humanization**: Two-pass generation with humanization for natural-sounding content
- **History Management**: Track and manage all generated content
- **Workflow Integration**: Hooks for custom workflow nodes

## DocTypes

1. **Generated Content**: Stores all generated content with metadata
2. **LLM Settings**: User-specific LLM provider API keys
3. **LLM System Settings**: System-wide LLM provider API keys
4. **LLM Provider Setting**: Child table for storing provider settings

## API Functions

### Content Generation
- `generate_content(keyword, content_type, tone, provider, model)`: Generate content
- `get_generated_contents()`: Retrieve content history
- `delete_content(name)`: Delete generated content

### LLM Management
- `set_llm_api_key(provider, api_key)`: Save API key for provider
- `get_llm_api_key(provider)`: Retrieve API key for provider

### Workflow Hooks
- `generate_content_for_workflow()`: Generate content for workflow nodes
- `quick_generate()`: Quick generation with custom prompt
- `get_available_providers()`: List available providers
- `get_content_types()`: List available content types

## Frontend

Vue 3 application with:
- Writer page for content generation
- History page for managing generated content
- LLM provider and model selection
- API key management

## Installation

1. Install the app in your Frappe bench
2. Run migrations: `bench --site [site-name] migrate`
3. Build frontend: `cd syncedoffice/so_writer/frontend && yarn install && yarn build`
4. Access at: `http://[site-url]/writer`

## Workflow Integration

Use the workflow hooks to integrate content generation into your custom workflow nodes:

```python
from syncedoffice.so_writer.workflow_hook import generate_content_for_workflow

result = generate_content_for_workflow(
    keyword="AI automation",
    content_type="blog-post",
    tone="professional",
    provider="openai",
    model="gpt-4",
    save_to_db=True
)
```

## Dependencies

Python packages:
- openai (optional, for OpenAI)
- anthropic (optional, for Anthropic)
- google-generativeai (optional, for Google)
- boto3 (optional, for Amazon Bedrock)

Frontend packages:
- vue 3
- frappe-ui
- marked (for markdown rendering)
- pinia (state management)

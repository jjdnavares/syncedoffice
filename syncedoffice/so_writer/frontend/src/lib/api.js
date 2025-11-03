import { call } from 'frappe-ui'

export async function generateContent({ content_type, keyword, tone, provider, model }) {
  try {
    const result = await call('syncedoffice.so_writer.api.generate_content', {
      keyword,
      content_type,
      tone,
      provider,
      model,
    })
    return { message: result, error: null }
  } catch (error) {
    console.error('Error generating content:', error)
    return { message: null, error: error.message || 'Failed to generate content' }
  }
}

export async function getGeneratedContents() {
  try {
    const result = await call('syncedoffice.so_writer.api.get_generated_contents')
    return { message: result, error: null }
  } catch (error) {
    console.error('Error fetching contents:', error)
    return { message: [], error: error.message }
  }
}

export async function deleteContent(name) {
  try {
    const result = await call('syncedoffice.so_writer.api.delete_content', { name })
    return { message: result, error: null }
  } catch (error) {
    console.error('Error deleting content:', error)
    return { message: null, error: error.message }
  }
}

export async function setLLMApiKey(provider, apiKey) {
  try {
    const result = await call('syncedoffice.so_writer.api.set_llm_api_key', {
      provider,
      api_key: apiKey,
    })
    return { message: result, error: null }
  } catch (error) {
    console.error('Error setting API key:', error)
    return { message: null, error: error.message }
  }
}

export async function getLLMApiKey(provider) {
  try {
    const result = await call('syncedoffice.so_writer.api.get_llm_api_key', { provider })
    return { message: result, error: null }
  } catch (error) {
    console.error('Error getting API key:', error)
    return { message: {}, error: error.message }
  }
}

export const LLM_PROVIDERS = [
  { name: 'openai', label: 'OpenAI', requiresApiKey: true },
  { name: 'anthropic', label: 'Anthropic', requiresApiKey: true },
  { name: 'google', label: 'Google', requiresApiKey: true },
  { name: 'cohere', label: 'Cohere', requiresApiKey: true },
  { name: 'groq', label: 'Groq', requiresApiKey: true },
  { name: 'mistral', label: 'Mistral', requiresApiKey: true },
  { name: 'ollama', label: 'Ollama', requiresApiKey: true },
  { name: 'perplexity', label: 'Perplexity', requiresApiKey: true },
  { name: 'together', label: 'Together AI', requiresApiKey: true },
  { name: 'amazon-bedrock', label: 'Amazon Bedrock', requiresApiKey: true },
  { name: 'open-router', label: 'OpenRouter', requiresApiKey: true },
]

export const LLM_MODELS = {
  openai: [
    { name: 'gpt-4', label: 'GPT-4' },
    { name: 'gpt-4-turbo', label: 'GPT-4 Turbo' },
    { name: 'gpt-3.5-turbo', label: 'GPT-3.5 Turbo' },
  ],
  anthropic: [
    { name: 'claude-3-opus-20240229', label: 'Claude 3 Opus' },
    { name: 'claude-3-sonnet-20240229', label: 'Claude 3 Sonnet' },
    { name: 'claude-3-haiku-20240307', label: 'Claude 3 Haiku' },
  ],
  google: [
    { name: 'gemini-pro', label: 'Gemini Pro' },
    { name: 'gemini-1.5-pro', label: 'Gemini 1.5 Pro' },
  ],
  groq: [
    { name: 'llama3-70b-8192', label: 'Llama 3 70B' },
    { name: 'llama3-8b-8192', label: 'Llama 3 8B' },
    { name: 'mixtral-8x7b-32768', label: 'Mixtral 8x7B' },
  ],
  mistral: [
    { name: 'mistral-small', label: 'Mistral Small' },
    { name: 'mistral-medium', label: 'Mistral Medium' },
    { name: 'mistral-large-latest', label: 'Mistral Large' },
  ],
}

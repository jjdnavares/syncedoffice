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

export async function deleteLLMApiKey(provider) {
  try {
    const result = await call('syncedoffice.so_writer.api.delete_llm_api_key', { provider })
    return { message: result, error: null }
  } catch (error) {
    console.error('Error deleting API key:', error)
    return { message: null, error: error.message }
  }
}

export async function getLLMModels(provider) {
  try {
    const result = await call('syncedoffice.so_writer.api.get_llm_models', { provider })
    return { message: result, error: null }
  } catch (error) {
    console.error('Error getting LLM models:', error)
    return { message: [], error: error.message }
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

<template>
  <main class="grid grid-cols-1 lg:grid-cols-3 gap-8">
    <div class="lg:col-span-1 space-y-8">
      <LLMSettings
        :selected-provider="provider"
        :selected-model="model"
        :api-key="apiKeys[provider] || ''"
        :api-key-error="apiKeyError"
        :model-error="modelError"
        :is-loading-models="isLoadingModels"
        @provider-change="handleProviderChange"
        @model-change="setModel"
        @api-key-change="handleApiKeyChange"
      />
      <WriterSettings
        :provider="provider"
        :model="model"
        @generate="onContentGenerated"
        @generate-start="handleGenerateStart"
        @error="handleGenerateError"
      />
    </div>
    <div class="lg:col-span-2">
      <GeneratedContent
        :active-content="activeContent"
        :is-loading="isGenerating"
        :error="generationError"
        @delete="handleDelete"
      />
    </div>
  </main>
</template>

<script>
import { ref, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import LLMSettings from '../components/LLMSettings.vue'
import WriterSettings from '../components/WriterSettings.vue'
import GeneratedContent from '../components/GeneratedContent.vue'
import { getGeneratedContents, deleteContent, getLLMApiKey, LLM_PROVIDERS, LLM_MODELS } from '../lib/api'

export default {
  name: 'WriterPage',
  components: {
    LLMSettings,
    WriterSettings,
    GeneratedContent,
  },
  setup() {
    const route = useRoute()
    const activeContent = ref(route.params.activeContent || null)
    const isGenerating = ref(false)
    const generationError = ref(null)

    // LLM state
    const provider = ref('')
    const model = ref('')
    const apiKeys = ref({})
    const apiKeyError = ref('')
    const modelError = ref('')
    const isLoadingModels = ref(false)

    // Initialize provider
    onMounted(async () => {
      if (LLM_PROVIDERS.length > 0 && !provider.value) {
        provider.value = LLM_PROVIDERS[0].name
        await fetchApiKey(provider.value)
      }
    })

    // Watch for provider changes to load models
    watch(provider, (newProvider) => {
      if (newProvider) {
        const models = LLM_MODELS[newProvider]
        if (models && models.length > 0) {
          model.value = models[0].name
        } else {
          model.value = ''
        }
      }
    })

    const fetchApiKey = async (providerName) => {
      const response = await getLLMApiKey(providerName)
      if (response.message?.api_key) {
        apiKeys.value[providerName] = response.message.api_key
        apiKeyError.value = ''
      } else {
        apiKeyError.value = 'API key not found. Please enter your API key.'
      }
    }

    const handleProviderChange = async (newProvider) => {
      provider.value = newProvider
      model.value = ''
      await fetchApiKey(newProvider)
    }

    const setModel = (newModel) => {
      model.value = newModel
    }

    const handleApiKeyChange = (key) => {
      apiKeys.value[provider.value] = key
      apiKeyError.value = ''
    }

    const onContentGenerated = async (generatedContent = null) => {
      isGenerating.value = false
      generationError.value = null
      if (generatedContent) {
        activeContent.value = generatedContent
      } else {
        const response = await getGeneratedContents()
        if (response.message && response.message.length > 0) {
          activeContent.value = response.message[0]
        }
      }
    }

    const handleGenerateStart = () => {
      isGenerating.value = true
      generationError.value = null
    }

    const handleGenerateError = (error) => {
      isGenerating.value = false
      generationError.value = error
    }

    const handleDelete = async (name) => {
      await deleteContent(name)
      if (activeContent.value && activeContent.value.name === name) {
        activeContent.value = null
      }
    }

    return {
      activeContent,
      isGenerating,
      generationError,
      provider,
      model,
      apiKeys,
      apiKeyError,
      modelError,
      isLoadingModels,
      handleProviderChange,
      setModel,
      handleApiKeyChange,
      onContentGenerated,
      handleGenerateStart,
      handleGenerateError,
      handleDelete,
    }
  },
}
</script>

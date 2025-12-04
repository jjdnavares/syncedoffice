<template>
  <main class="grid grid-cols-1 lg:grid-cols-3 gap-8">
    <div class="lg:col-span-1 space-y-8">
      <LLMSettings
        :selected-provider="provider"
        :selected-model="model"
        :models="models"
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
import LLMSettings from '@/components/writer/LLMSettings.vue'
import WriterSettings from '@/components/writer/WriterSettings.vue'
import GeneratedContent from '@/components/writer/GeneratedContent.vue'
import { getGeneratedContents, deleteContent, getLLMApiKey, getLLMModels, LLM_PROVIDERS } from '@/lib/writer-api'

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
    const models = ref([])
    const apiKeys = ref({})
    const apiKeyError = ref('')
    const modelError = ref('')
    const isLoadingModels = ref(false)

    // Initialize provider
    onMounted(async () => {
      // Don't auto-select provider - let user choose
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

    const loadModels = async (providerName) => {
      if (!providerName) {
        models.value = []
        model.value = ''
        return
      }

      isLoadingModels.value = true
      modelError.value = ''

      const response = await getLLMModels(providerName)
      if (response.error) {
        modelError.value = response.error
        models.value = []
        model.value = ''
      } else {
        const fetchedModels = response.message || []
        models.value = fetchedModels
        // Don't auto-select first model - let user choose
        model.value = ''
      }

      isLoadingModels.value = false
    }

    const handleProviderChange = async (newProvider) => {
      provider.value = newProvider
      model.value = ''
      await fetchApiKey(newProvider)
      await loadModels(newProvider)
    }

    const setModel = (newModel) => {
      model.value = newModel
    }

    const handleApiKeyChange = (key) => {
      apiKeys.value[provider.value] = key
      apiKeyError.value = ''
      if (provider.value) {
        loadModels(provider.value)
      }
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
      models,
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

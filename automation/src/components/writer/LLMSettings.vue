<template>
  <div class="bg-white rounded-lg shadow">
    <div class="p-4 border-b flex items-center justify-between">
      <h3 class="text-md font-semibold">LLM Provider Settings</h3>
      <button
        @click="toggleSettings"
        class="text-sm text-gray-600 hover:text-gray-900 flex items-center gap-2"
      >
        <svg class="h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
        {{ isExpanded ? 'Hide Settings' : 'Show Settings' }}
      </button>
    </div>

    <div v-if="isExpanded" class="p-4 space-y-4">
      <div class="space-y-2">
        <label for="provider" class="block text-sm font-medium text-gray-700">
          Provider
        </label>
        <select
          id="provider"
          :value="selectedProvider"
          @change="$emit('provider-change', $event.target.value)"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">Select provider...</option>
          <option v-for="provider in providers" :key="provider.name" :value="provider.name">
            {{ provider.label }}
          </option>
        </select>
      </div>

      <div class="space-y-2">
        <label for="model" class="block text-sm font-medium text-gray-700">
          Model
          <span v-if="isLoadingModels" class="ml-2 text-blue-600 text-xs">
            <svg class="animate-spin -mt-1 inline-block h-3 w-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Loading models...
          </span>
        </label>
        <select
          id="model"
          :value="selectedModel"
          @change="$emit('model-change', $event.target.value)"
          :disabled="!selectedProvider || isLoadingModels"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
        >
          <option value="">
            {{ !selectedProvider ? 'Select provider first' : (isLoadingModels ? 'Loading models...' : 'Select model...') }}
          </option>
          <option v-for="model in models" :key="model.name" :value="model.name">
            {{ model.label }}
          </option>
        </select>
        <p v-if="modelError" class="text-sm text-red-600">{{ modelError }}</p>
      </div>

      <div v-if="isApiKeyRequired" class="space-y-2">
        <div class="flex items-center justify-between">
          <label for="api-key" class="block text-sm font-medium text-gray-700">
            API Key
          </label>
          <button
            v-if="apiKey"
            @click="handleDeleteApiKey"
            class="text-xs text-red-600 hover:text-red-800 flex items-center gap-1"
          >
            <svg class="h-3 w-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            Delete Key
          </button>
        </div>
        <input
          id="api-key"
          type="password"
          :value="apiKey"
          @input="handleApiKeyChange($event.target.value)"
          placeholder="Enter your API key"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <p v-if="apiKeyError" class="text-sm text-red-600">{{ apiKeyError }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch } from 'vue'
import { LLM_PROVIDERS, setLLMApiKey, deleteLLMApiKey } from '@/lib/writer-api'

export default {
  name: 'LLMSettings',
  props: {
    selectedProvider: {
      type: String,
      required: true,
    },
    selectedModel: {
      type: String,
      required: true,
    },
    models: {
      type: Array,
      required: true,
    },
    apiKey: {
      type: String,
      default: '',
    },
    apiKeyError: {
      type: String,
      default: '',
    },
    modelError: {
      type: String,
      default: '',
    },
    isLoadingModels: {
      type: Boolean,
      default: false,
    },
  },
  emits: ['provider-change', 'model-change', 'api-key-change'],
  setup(props, { emit }) {
    const isExpanded = ref(true)
    const providers = ref(LLM_PROVIDERS)
    const internalApiKey = ref(props.apiKey)
    let debounceTimeout = null

    const models = computed(() => props.models || [])

    const isApiKeyRequired = computed(() => {
      const provider = providers.value.find(p => p.name === props.selectedProvider)
      return provider?.requiresApiKey || false
    })

    const toggleSettings = () => {
      isExpanded.value = !isExpanded.value
    }

    const handleApiKeyChange = (newApiKey) => {
      internalApiKey.value = newApiKey
      emit('api-key-change', newApiKey)

      // Debounce API key save
      if (debounceTimeout) {
        clearTimeout(debounceTimeout)
      }
      debounceTimeout = setTimeout(async () => {
        if (props.selectedProvider) {
          const response = await setLLMApiKey(props.selectedProvider, newApiKey)
          if (response.error) {
            console.error('Failed to save API key:', response.error)
          }
        }
      }, 500)
    }

    const handleDeleteApiKey = async () => {
      if (confirm('Are you sure you want to delete this API key?')) {
        // Delete the API key from backend first
        if (props.selectedProvider) {
          const response = await deleteLLMApiKey(props.selectedProvider)
          if (response.error) {
            console.error('Failed to delete API key:', response.error)
            return
          }
        }
        
        // Clear the API key in UI after successful backend deletion
        internalApiKey.value = ''
        emit('api-key-change', '')
      }
    }

    watch(() => props.apiKey, (newValue) => {
      internalApiKey.value = newValue
    })

    return {
      isExpanded,
      providers,
      models,
      isApiKeyRequired,
      internalApiKey,
      toggleSettings,
      handleApiKeyChange,
      handleDeleteApiKey,
    }
  },
}
</script>

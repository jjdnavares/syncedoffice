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
          <option value="">Select your AI provider</option>
          <option v-for="provider in providers" :key="provider.name" :value="provider.name">
            {{ provider.label }}
          </option>
        </select>
      </div>

      <div class="space-y-2">
        <label for="model" class="block text-sm font-medium text-gray-700">
          Model
        </label>
        <select
          id="model"
          :value="selectedModel"
          @change="$emit('model-change', $event.target.value)"
          :disabled="!selectedProvider || isLoadingModels"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
        >
          <option value="">Select your AI model</option>
          <option v-for="model in models" :key="model.name" :value="model.name">
            {{ model.label }}
          </option>
        </select>
        <p v-if="modelError" class="text-sm text-red-600">{{ modelError }}</p>
      </div>

      <div v-if="isApiKeyRequired" class="space-y-2">
        <label for="api-key" class="block text-sm font-medium text-gray-700">
          API Key
        </label>
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
import { LLM_PROVIDERS, LLM_MODELS, setLLMApiKey } from '../lib/api'

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

    const models = computed(() => {
      return LLM_MODELS[props.selectedProvider] || []
    })

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
    }
  },
}
</script>

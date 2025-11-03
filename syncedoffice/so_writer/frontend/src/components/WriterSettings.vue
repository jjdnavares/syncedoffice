<template>
  <div class="flex flex-col gap-8">
    <div class="bg-white rounded-lg shadow p-6 space-y-4">
      <div class="space-y-2">
        <label for="keyword" class="block text-sm font-medium text-gray-700">
          Target Keyword or Phrase
        </label>
        <textarea
          id="keyword"
          v-model="keyword"
          placeholder="Enter a keyword or phrase"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          rows="3"
        />
      </div>

      <div class="space-y-2">
        <label for="content-type" class="block text-sm font-medium text-gray-700">
          Content Type
        </label>
        <select
          id="content-type"
          v-model="contentType"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="blog-post">Blog Post</option>
          <option value="article">Article</option>
          <option value="product-description">Product Description</option>
          <option value="landing-page">Landing Page</option>
          <option value="seo-meta-description">SEO Meta Description</option>
          <option value="social-media-post">Social Media Post</option>
          <option value="blog-outline">Blog Outline</option>
        </select>
      </div>

      <div class="space-y-2">
        <label for="tone" class="block text-sm font-medium text-gray-700">
          Tone of Voice
        </label>
        <select
          id="tone"
          v-model="tone"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="professional">Professional</option>
          <option value="casual">Casual</option>
          <option value="friendly">Friendly</option>
          <option value="authoritative">Authoritative</option>
          <option value="witty">Witty</option>
        </select>
      </div>
    </div>

    <button
      @click="handleGenerate"
      :disabled="isLoading"
      class="w-full py-3 px-4 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2 text-lg font-medium"
    >
      <svg
        v-if="isLoading"
        class="animate-spin h-5 w-5"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
      >
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      <svg v-else class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
      </svg>
      {{ isLoading ? 'Generating...' : 'Generate Content' }}
    </button>
  </div>
</template>

<script>
import { ref } from 'vue'
import { generateContent } from '../lib/api'

export default {
  name: 'WriterSettings',
  props: {
    provider: {
      type: String,
      required: true,
    },
    model: {
      type: String,
      required: true,
    },
  },
  emits: ['generate', 'generate-start', 'error'],
  setup(props, { emit }) {
    const contentType = ref('blog-post')
    const keyword = ref('')
    const tone = ref('casual')
    const isLoading = ref(false)

    const handleGenerate = async () => {
      if (!keyword.value) {
        alert('Please enter a target keyword or phrase')
        return
      }

      isLoading.value = true
      emit('generate-start')

      const response = await generateContent({
        content_type: contentType.value,
        keyword: keyword.value,
        tone: tone.value,
        provider: props.provider,
        model: props.model,
      })

      if (response.error) {
        console.error('Failed to generate content:', response.error)
        emit('error', response.error || 'Failed to generate content')
      } else if (response.message) {
        emit('generate', response.message)
      }

      isLoading.value = false
    }

    return {
      contentType,
      keyword,
      tone,
      isLoading,
      handleGenerate,
    }
  },
}
</script>

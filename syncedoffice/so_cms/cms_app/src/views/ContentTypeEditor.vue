<template>
  <div>
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center">
        <button @click="goBack" class="mr-4 text-gray-500 hover:text-gray-700">
          <ArrowLeft :size="20" />
        </button>
        <div>
          <h1 class="text-2xl font-bold text-gray-900">
            {{ isNew ? 'Create Content Type' : 'Edit Content Type' }}
          </h1>
          <p class="mt-1 text-sm text-gray-500">
            {{ isNew ? 'Define your content structure' : contentType?.display_name }}
          </p>
        </div>
      </div>
      <div class="flex space-x-3">
        <BaseButton variant="secondary" @click="goBack">
          Cancel
        </BaseButton>
        <BaseButton @click="handleSave" :loading="saving">
          <Save :size="16" class="mr-2" />
          {{ isNew ? 'Create' : 'Save' }}
        </BaseButton>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin text-4xl">⟳</div>
      <p class="mt-2 text-gray-500">Loading...</p>
    </div>

    <!-- Editor -->
    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Left Column - Basic Info -->
      <div class="lg:col-span-1">
        <div class="card p-6 sticky top-24">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">Basic Information</h2>

          <BaseInput
            v-model="formData.content_type_name"
            label="Name"
            placeholder="e.g., Blog Post"
            required
            :error="errors.content_type_name"
            help-text="Internal name for this content type"
            class="mb-4"
          />

          <BaseInput
            v-model="formData.display_name"
            label="Display Name"
            placeholder="e.g., Blog Post"
            required
            :error="errors.display_name"
            class="mb-4"
          />

          <BaseSelect
            v-model="formData.kind"
            label="Type"
            :options="['Collection Type', 'Single Type']"
            required
            help-text="Collection for multiple entries, Single for one entry"
            class="mb-4"
          />

          <BaseInput
            v-model="formData.icon"
            label="Icon"
            placeholder="e.g., file-text"
            help-text="Lucide icon name"
            class="mb-4"
          />

          <div class="mb-4">
            <label class="label">Description</label>
            <textarea
              v-model="formData.description"
              rows="3"
              class="input"
              placeholder="Describe this content type..."
            ></textarea>
          </div>

          <div class="flex items-center">
            <input
              v-model="formData.is_published"
              type="checkbox"
              id="is_published"
              class="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
            />
            <label for="is_published" class="ml-2 text-sm text-gray-700">
              Published
            </label>
          </div>
        </div>
      </div>

      <!-- Right Column - Field Builder -->
      <div class="lg:col-span-2">
        <FieldBuilder
          v-model="formData.fields"
          @update:modelValue="handleFieldsUpdate"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useContentTypeStore } from '../stores/contentTypeStore'
import { ArrowLeft, Save } from 'lucide-vue-next'
import BaseButton from '../components/BaseButton.vue'
import BaseInput from '../components/BaseInput.vue'
import BaseSelect from '../components/BaseSelect.vue'
import FieldBuilder from '../components/FieldBuilder.vue'

const router = useRouter()
const route = useRoute()
const store = useContentTypeStore()

const loading = ref(false)
const saving = ref(false)
const errors = ref({})

const isNew = computed(() => route.params.name === undefined || route.params.name === 'new')
const contentType = computed(() => store.currentContentType)

const formData = ref({
  content_type_name: '',
  display_name: '',
  description: '',
  kind: 'Collection Type',
  icon: 'file-text',
  is_published: false,
  fields: [],
})

onMounted(async () => {
  if (!isNew.value) {
    loading.value = true
    try {
      await store.fetchContentType(route.params.name)
      if (contentType.value) {
        formData.value = {
          content_type_name: contentType.value.content_type_name || '',
          display_name: contentType.value.display_name || '',
          description: contentType.value.description || '',
          kind: contentType.value.kind || 'Collection Type',
          icon: contentType.value.icon || 'file-text',
          is_published: contentType.value.is_published || false,
          fields: contentType.value.fields || [],
        }
      }
    } catch (error) {
      alert('Error loading content type: ' + error.message)
      router.push('/cms/content-types')
    } finally {
      loading.value = false
    }
  }
})

// Auto-generate display name from content type name
watch(() => formData.value.content_type_name, (newVal) => {
  if (isNew.value && newVal && !formData.value.display_name) {
    formData.value.display_name = newVal
  }
})

function handleFieldsUpdate(fields) {
  formData.value.fields = fields
}

function validateForm() {
  errors.value = {}
  
  if (!formData.value.content_type_name) {
    errors.value.content_type_name = 'Name is required'
  }
  
  if (!formData.value.display_name) {
    errors.value.display_name = 'Display name is required'
  }
  
  return Object.keys(errors.value).length === 0
}

async function handleSave() {
  if (!validateForm()) {
    return
  }

  saving.value = true
  try {
    if (isNew.value) {
      await store.createContentType(formData.value)
      alert('Content type created successfully!')
      router.push('/cms/content-types')
    } else {
      await store.updateContentType(route.params.name, formData.value)
      alert('Content type updated successfully!')
    }
  } catch (error) {
    alert('Error saving content type: ' + error.message)
  } finally {
    saving.value = false
  }
}

function goBack() {
  router.push('/cms/content-types')
}
</script>

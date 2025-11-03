import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '../utils/api'

export const useContentTypeStore = defineStore('contentType', () => {
  const contentTypes = ref([])
  const currentContentType = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const collectionTypes = computed(() => 
    contentTypes.value.filter(ct => ct.kind === 'Collection Type')
  )

  const singleTypes = computed(() => 
    contentTypes.value.filter(ct => ct.kind === 'Single Type')
  )

  async function fetchContentTypes() {
    loading.value = true
    error.value = null
    try {
      const response = await api.call('syncedoffice.so_cms.api.content_type.get_content_types')
      contentTypes.value = response.message || response
    } catch (e) {
      error.value = e.message
      console.error('Error fetching content types:', e)
    } finally {
      loading.value = false
    }
  }

  async function fetchContentType(name) {
    loading.value = true
    error.value = null
    try {
      const response = await api.call('syncedoffice.so_cms.api.content_type.get_content_type', { name })
      currentContentType.value = response.message || response
      return currentContentType.value
    } catch (e) {
      error.value = e.message
      console.error('Error fetching content type:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function createContentType(data) {
    loading.value = true
    error.value = null
    try {
      const response = await api.call('syncedoffice.so_cms.api.content_type.create_content_type', { 
        data: JSON.stringify(data) 
      })
      const newContentType = response.message || response
      contentTypes.value.push(newContentType)
      return newContentType
    } catch (e) {
      error.value = e.message
      console.error('Error creating content type:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function updateContentType(name, data) {
    loading.value = true
    error.value = null
    try {
      const response = await api.call('syncedoffice.so_cms.api.content_type.update_content_type', { 
        name,
        data: JSON.stringify(data) 
      })
      const updated = response.message || response
      
      // Update in list
      const index = contentTypes.value.findIndex(ct => ct.name === name)
      if (index !== -1) {
        contentTypes.value[index] = updated
      }
      
      // Update current if it's the same
      if (currentContentType.value?.name === name) {
        currentContentType.value = updated
      }
      
      return updated
    } catch (e) {
      error.value = e.message
      console.error('Error updating content type:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function deleteContentType(name) {
    loading.value = true
    error.value = null
    try {
      await api.call('syncedoffice.so_cms.api.content_type.delete_content_type', { name })
      contentTypes.value = contentTypes.value.filter(ct => ct.name !== name)
      if (currentContentType.value?.name === name) {
        currentContentType.value = null
      }
    } catch (e) {
      error.value = e.message
      console.error('Error deleting content type:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function addField(contentTypeName, fieldData) {
    loading.value = true
    error.value = null
    try {
      const response = await api.call('syncedoffice.so_cms.api.content_type.add_field', {
        content_type: contentTypeName,
        field_data: JSON.stringify(fieldData)
      })
      const updated = response.message || response
      currentContentType.value = updated
      return updated
    } catch (e) {
      error.value = e.message
      console.error('Error adding field:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function updateField(contentTypeName, fieldName, data) {
    loading.value = true
    error.value = null
    try {
      const response = await api.call('syncedoffice.so_cms.api.content_type.update_field', {
        content_type: contentTypeName,
        field_name: fieldName,
        data: JSON.stringify(data)
      })
      const updated = response.message || response
      currentContentType.value = updated
      return updated
    } catch (e) {
      error.value = e.message
      console.error('Error updating field:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function deleteField(contentTypeName, fieldName) {
    loading.value = true
    error.value = null
    try {
      await api.call('syncedoffice.so_cms.api.content_type.delete_field', {
        content_type: contentTypeName,
        field_name: fieldName
      })
      // Refresh current content type
      await fetchContentType(contentTypeName)
    } catch (e) {
      error.value = e.message
      console.error('Error deleting field:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function reorderFields(contentTypeName, fieldOrder) {
    loading.value = true
    error.value = null
    try {
      const response = await api.call('syncedoffice.so_cms.api.content_type.reorder_fields', {
        content_type: contentTypeName,
        field_order: JSON.stringify(fieldOrder)
      })
      const updated = response.message || response
      currentContentType.value = updated
      return updated
    } catch (e) {
      error.value = e.message
      console.error('Error reordering fields:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    contentTypes,
    currentContentType,
    loading,
    error,
    collectionTypes,
    singleTypes,
    fetchContentTypes,
    fetchContentType,
    createContentType,
    updateContentType,
    deleteContentType,
    addField,
    updateField,
    deleteField,
    reorderFields,
  }
})

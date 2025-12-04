import { defineStore } from 'pinia'
import { ref } from 'vue'
import { call } from 'frappe-ui'

export const useNodeTypesStore = defineStore('nodeTypes', () => {
  const nodeTypes = ref({
    triggers: [],
    actions: [],
    core: [],
    transform: [],
    condition: [],
    integration: [],
    custom: []
  })
  
  const isLoading = ref(false)
  const error = ref(null)
  const isLoaded = ref(false)

  async function fetchNodeTypes() {
    if (isLoaded.value) return // Only fetch once
    
    isLoading.value = true
    error.value = null
    
    try {
      const result = await call('syncedoffice.so_workflow.doctype.workflow_node_type.workflow_node_type.get_node_types_for_editor')
      nodeTypes.value = result || {
        triggers: [],
        actions: [],
        core: [],
        transform: [],
        condition: [],
        integration: [],
        custom: []
      }
      isLoaded.value = true
    } catch (e) {
      error.value = e.message
      console.error('Error fetching node types:', e)
    } finally {
      isLoading.value = false
    }
  }

  function getNodeTypesByCategory(category) {
    return nodeTypes.value[category] || []
  }

  function getAllNodeTypes() {
    return Object.values(nodeTypes.value).flat()
  }

  function getNodeType(nodeTypeName) {
    const allTypes = getAllNodeTypes()
    return allTypes.find(nt => nt.type === nodeTypeName)
  }

  return {
    nodeTypes,
    isLoading,
    error,
    isLoaded,
    fetchNodeTypes,
    getNodeTypesByCategory,
    getAllNodeTypes,
    getNodeType
  }
})

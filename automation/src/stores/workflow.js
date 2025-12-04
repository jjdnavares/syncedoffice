import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { call } from 'frappe-ui'

export const useWorkflowStore = defineStore('workflow', () => {
  const workflows = ref([])
  const currentWorkflow = ref(null)
  const nodes = ref([])
  const edges = ref([])
  const selectedNode = ref(null)
  const isLoading = ref(false)
  const error = ref(null)
  
  // History management for undo/redo
  const history = ref([])
  const historyIndex = ref(-1)
  const maxHistorySize = 50

  // Computed
  const hasUnsavedChanges = computed(() => {
    if (!currentWorkflow.value) return false
    // Compare current nodes/edges with saved workflow
    return true // Simplified for MVP
  })
  
  const canUndo = computed(() => historyIndex.value > 0)
  const canRedo = computed(() => historyIndex.value < history.value.length - 1)

  // Actions
  async function fetchWorkflows() {
    isLoading.value = true
    error.value = null
    
    try {
      const result = await call('syncedoffice.so_workflow.doctype.so_workflow.so_workflow.get_workflow_list')
      workflows.value = result || []
    } catch (e) {
      error.value = e.message
      console.error('Error fetching workflows:', e)
    } finally {
      isLoading.value = false
    }
  }

  async function loadWorkflow(name) {
    isLoading.value = true
    error.value = null
    
    try {
      const result = await call('syncedoffice.so_workflow.doctype.so_workflow.so_workflow.get_workflow', {
        name
      })
      
      currentWorkflow.value = result
      
      // Parse nodes and connections
      const workflowNodes = typeof result.nodes === 'string' 
        ? JSON.parse(result.nodes) 
        : result.nodes || []
      
      const workflowConnections = typeof result.connections === 'string'
        ? JSON.parse(result.connections)
        : result.connections || {}
      
      // Convert to Vue Flow format
      nodes.value = workflowNodes.map(node => ({
        id: node.id,
        type: node.type || 'default',
        position: node.position || { x: 0, y: 0 },
        data: {
          label: node.name || node.id,
          ...node
        }
      }))
      
      // Convert connections to edges
      edges.value = convertConnectionsToEdges(workflowConnections)
      
    } catch (e) {
      error.value = e.message
      console.error('Error loading workflow:', e)
    } finally {
      isLoading.value = false
    }
  }

  async function saveWorkflow() {
    if (!currentWorkflow.value) return
    
    isLoading.value = true
    error.value = null
    
    try {
      // Convert Vue Flow format back to workflow format
      const workflowNodes = nodes.value.map(node => ({
        id: node.id,
        type: node.type,
        name: node.data.label,
        position: node.position,
        ...node.data
      }))
      
      const workflowConnections = convertEdgesToConnections(edges.value)
      
      const workflowData = {
        ...currentWorkflow.value,
        nodes: JSON.stringify(workflowNodes),
        connections: JSON.stringify(workflowConnections)
      }
      
      const result = await call('syncedoffice.so_workflow.doctype.so_workflow.so_workflow.save_workflow', {
        workflow_data: workflowData
      })
      
      currentWorkflow.value = result
      
      return result
    } catch (e) {
      error.value = e.message
      console.error('Error saving workflow:', e)
      throw e
    } finally {
      isLoading.value = false
    }
  }

  async function createWorkflow(workflowData) {
    isLoading.value = true
    error.value = null
    
    try {
      const result = await call('syncedoffice.so_workflow.doctype.so_workflow.so_workflow.save_workflow', {
        workflow_data: {
          workflow_name: workflowData.workflow_name,
          description: workflowData.description,
          active: workflowData.active ?? true,
          nodes: JSON.stringify([]),
          connections: JSON.stringify({})
        }
      })
      
      workflows.value.push(result)
      return result
    } catch (e) {
      error.value = e.message
      console.error('Error creating workflow:', e)
      throw e
    } finally {
      isLoading.value = false
    }
  }

  async function executeWorkflow(name, inputData = null) {
    isLoading.value = true
    error.value = null
    
    try {
      const result = await call('syncedoffice.so_workflow.doctype.so_workflow.so_workflow.execute_workflow_api', {
        name,
        input_data: inputData
      })
      
      return result
    } catch (e) {
      error.value = e.message
      console.error('Error executing workflow:', e)
      throw e
    } finally {
      isLoading.value = false
    }
  }

  async function deleteWorkflow(name) {
    isLoading.value = true
    error.value = null
    
    try {
      await call('syncedoffice.so_workflow.doctype.so_workflow.so_workflow.delete_workflow', {
        name
      })
      
      // Remove from local state
      workflows.value = workflows.value.filter(w => w.name !== name)
      
      return true
    } catch (e) {
      error.value = e.message
      console.error('Error deleting workflow:', e)
      throw e
    } finally {
      isLoading.value = false
    }
  }

  async function updateWorkflowStatus(name, active) {
    error.value = null
    
    try {
      const result = await call('syncedoffice.so_workflow.doctype.so_workflow.so_workflow.update_workflow_status', {
        name,
        active: active ? 1 : 0
      })
      
      // Update local state
      const workflow = workflows.value.find(w => w.name === name)
      if (workflow) {
        workflow.active = active
      }
      
      return result
    } catch (e) {
      error.value = e.message
      console.error('Error updating workflow status:', e)
      throw e
    }
  }

  // History management
  function saveToHistory() {
    const state = {
      nodes: JSON.parse(JSON.stringify(nodes.value)),
      edges: JSON.parse(JSON.stringify(edges.value))
    }
    
    // Remove any future history if we're not at the end
    if (historyIndex.value < history.value.length - 1) {
      history.value = history.value.slice(0, historyIndex.value + 1)
    }
    
    history.value.push(state)
    
    // Limit history size
    if (history.value.length > maxHistorySize) {
      history.value.shift()
    } else {
      historyIndex.value++
    }
  }
  
  function undo() {
    if (!canUndo.value) return
    
    historyIndex.value--
    const state = history.value[historyIndex.value]
    nodes.value = JSON.parse(JSON.stringify(state.nodes))
    edges.value = JSON.parse(JSON.stringify(state.edges))
  }
  
  function redo() {
    if (!canRedo.value) return
    
    historyIndex.value++
    const state = history.value[historyIndex.value]
    nodes.value = JSON.parse(JSON.stringify(state.nodes))
    edges.value = JSON.parse(JSON.stringify(state.edges))
  }

  function addNode(nodeData) {
    const nodeId = `node_${Date.now()}`
    const newNode = {
      id: nodeId,
      type: 'custom', // All nodes use 'custom' type for VueFlow rendering
      position: nodeData.position || { x: 100, y: 100 },
      data: {
        id: nodeId,
        label: nodeData.label || 'New Node',
        type: nodeData.type || 'default', // This is the actual node type (chat-trigger, etc.)
        parameters: nodeData.parameters || {},
        // Merge additional data from nodeData.data if provided
        ...(nodeData.data || {})
      }
    }
    
    nodes.value.push(newNode)
    saveToHistory()
    return newNode
  }

  function updateNode(nodeId, updates) {
    const index = nodes.value.findIndex(n => n.id === nodeId)
    if (index !== -1) {
      nodes.value[index] = {
        ...nodes.value[index],
        ...updates,
        data: {
          ...nodes.value[index].data,
          ...updates.data
        }
      }
      saveToHistory()
    }
  }

  function removeNode(nodeId) {
    nodes.value = nodes.value.filter(n => n.id !== nodeId)
    // Also remove connected edges
    edges.value = edges.value.filter(e => e.source !== nodeId && e.target !== nodeId)
    saveToHistory()
  }

  function addEdge(edgeData) {
    const newEdge = {
      id: `edge_${Date.now()}`,
      source: edgeData.source,
      target: edgeData.target,
      sourceHandle: edgeData.sourceHandle,
      targetHandle: edgeData.targetHandle,
      type: edgeData.type || 'default'
    }
    
    edges.value.push(newEdge)
    saveToHistory()
    return newEdge
  }

  function removeEdge(edgeId) {
    edges.value = edges.value.filter(e => e.id !== edgeId)
    saveToHistory()
  }

  function clearWorkflow() {
    currentWorkflow.value = null
    nodes.value = []
    edges.value = []
    selectedNode.value = null
  }

  // Helper functions
  function convertConnectionsToEdges(connections) {
    const edgesList = []
    
    for (const [sourceId, targets] of Object.entries(connections)) {
      if (typeof targets !== 'object') continue
      
      for (const [targetId, connectionsList] of Object.entries(targets)) {
        if (Array.isArray(connectionsList)) {
          connectionsList.forEach((conn, index) => {
            edgesList.push({
              id: `edge_${sourceId}_${targetId}_${index}`,
              source: sourceId,
              target: targetId,
              sourceHandle: conn.sourceHandle,
              targetHandle: conn.targetHandle,
              type: conn.type || 'default'
            })
          })
        }
      }
    }
    
    return edgesList
  }

  function convertEdgesToConnections(edgesList) {
    const connections = {}
    
    edgesList.forEach(edge => {
      if (!connections[edge.source]) {
        connections[edge.source] = {}
      }
      
      if (!connections[edge.source][edge.target]) {
        connections[edge.source][edge.target] = []
      }
      
      connections[edge.source][edge.target].push({
        sourceHandle: edge.sourceHandle,
        targetHandle: edge.targetHandle,
        type: edge.type
      })
    })
    
    return connections
  }

  return {
    // State
    workflows,
    currentWorkflow,
    nodes,
    edges,
    selectedNode,
    isLoading,
    error,
    
    // Computed
    hasUnsavedChanges,
    canUndo,
    canRedo,
    
    // Actions
    fetchWorkflows,
    loadWorkflow,
    saveWorkflow,
    createWorkflow,
    executeWorkflow,
    deleteWorkflow,
    updateWorkflowStatus,
    addNode,
    updateNode,
    removeNode,
    addEdge,
    removeEdge,
    clearWorkflow,
    undo,
    redo
  }
})

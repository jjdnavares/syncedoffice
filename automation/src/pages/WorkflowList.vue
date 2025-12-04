<template>
  <div class="workflow-list min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-6 py-6">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Workflows</h1>
            <p class="text-gray-600 mt-1">Automate your business processes</p>
          </div>
          
          <button
            @click="showCreateModal = true"
            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center gap-2"
          >
            <Plus :size="20" />
            New Workflow
          </button>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div class="max-w-7xl mx-auto px-6 py-8">
      <!-- Loading State -->
      <div v-if="workflowStore.isLoading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <p class="text-gray-600 mt-2">Loading workflows...</p>
      </div>

      <!-- Empty State -->
      <div v-else-if="!workflowStore.workflows.length" class="text-center py-12">
        <Workflow :size="64" class="mx-auto text-gray-400 mb-4" />
        <h3 class="text-lg font-medium text-gray-900 mb-2">No workflows yet</h3>
        <p class="text-gray-600 mb-6">Get started by creating your first workflow</p>
        <button
          @click="showCreateModal = true"
          class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          Create Workflow
        </button>
      </div>

      <!-- Workflow Grid -->
      <div v-else class="space-y-3">
        <div
          v-for="workflow in workflowStore.workflows"
          :key="workflow.name"
          class="bg-white rounded-lg border border-gray-200 hover:shadow-md transition-shadow"
        >
          <div class="p-4 flex items-center justify-between">
            <!-- Left: Workflow Info (clickable) -->
            <div 
              @click="openWorkflow(workflow.name)"
              class="flex-1 flex items-center gap-4 cursor-pointer min-w-0"
            >
              <div class="flex-shrink-0">
                <div class="p-2 bg-blue-100 rounded-lg">
                  <Workflow :size="20" class="text-blue-600" />
                </div>
              </div>
              
              <div class="flex-1 min-w-0">
                <h3 class="font-semibold text-gray-900 truncate">{{ workflow.workflow_name }}</h3>
                <div class="flex items-center gap-3 text-sm text-gray-500 mt-1">
                  <span>Last updated {{ formatDate(workflow.modified) }}</span>
                  <span>|</span>
                  <span>Created {{ formatDate(workflow.creation) }}</span>
                </div>
              </div>
            </div>
            
            <!-- Right: Status Badge, Toggle, and Menu -->
            <div class="flex items-center gap-3 flex-shrink-0">
              <!-- Status Badge -->
              <div
                :class="[
                  'px-2 py-1 rounded text-xs font-medium',
                  workflow.active 
                    ? 'bg-green-100 text-green-700' 
                    : 'bg-gray-100 text-gray-700'
                ]"
              >
                {{ workflow.active ? 'Active' : 'Inactive' }}
              </div>
              
              <!-- Toggle Switch -->
              <button
                @click.stop="toggleWorkflowStatus(workflow)"
                :class="[
                  'relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2',
                  workflow.active ? 'bg-blue-600' : 'bg-gray-300'
                ]"
                role="switch"
                :aria-checked="workflow.active"
              >
                <span
                  :class="[
                    'inline-block h-4 w-4 transform rounded-full bg-white transition-transform',
                    workflow.active ? 'translate-x-6' : 'translate-x-1'
                  ]"
                />
              </button>
              
              <!-- Dropdown Menu -->
              <div class="relative">
                <button
                  @click.stop="toggleDropdown(workflow.name)"
                  class="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                >
                  <MoreVertical :size="20" class="text-gray-600" />
                </button>
                
                <!-- Dropdown Content -->
                <div
                  v-if="openDropdown === workflow.name"
                  @click.stop
                  class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-1 z-10"
                >
                  <button
                    @click="confirmDelete(workflow)"
                    class="w-full px-4 py-2 text-left text-sm text-red-600 hover:bg-red-50 flex items-center gap-2"
                  >
                    <Trash2 :size="16" />
                    Delete
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Workflow Modal -->
    <div
      v-if="showCreateModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click="showCreateModal = false"
    >
      <div
        @click.stop
        class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4"
      >
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-semibold text-gray-900">Create New Workflow</h3>
        </div>
        
        <div class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Workflow Name *
            </label>
            <input
              v-model="newWorkflow.workflow_name"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="My Workflow"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              v-model="newWorkflow.description"
              rows="3"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Describe what this workflow does..."
            />
          </div>
          
          <div class="flex items-center gap-2">
            <input
              v-model="newWorkflow.active"
              type="checkbox"
              id="active"
              class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <label for="active" class="text-sm text-gray-700">
              Activate workflow immediately
            </label>
          </div>
        </div>
        
        <div class="px-6 py-4 border-t border-gray-200 flex justify-end gap-3">
          <button
            @click="showCreateModal = false"
            class="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg"
          >
            Cancel
          </button>
          <button
            @click="createWorkflow"
            :disabled="!newWorkflow.workflow_name"
            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Create Workflow
          </button>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div
      v-if="showDeleteModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click="showDeleteModal = false"
    >
      <div
        @click.stop
        class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4"
      >
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-semibold text-gray-900">Delete Workflow</h3>
        </div>
        
        <div class="p-6">
          <p class="text-gray-700">
            Are you sure you want to delete <strong>{{ workflowToDelete?.workflow_name }}</strong>?
            This action cannot be undone.
          </p>
        </div>
        
        <div class="px-6 py-4 border-t border-gray-200 flex justify-end gap-3">
          <button
            @click="showDeleteModal = false"
            class="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg"
          >
            Cancel
          </button>
          <button
            @click="deleteWorkflow"
            class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { Plus, Workflow, Play, Clock, MoreVertical, Trash2 } from 'lucide-vue-next'
import { useWorkflowStore } from '@/stores/workflow'

const router = useRouter()
const workflowStore = useWorkflowStore()

const showCreateModal = ref(false)
const showDeleteModal = ref(false)
const workflowToDelete = ref(null)
const openDropdown = ref(null)
const newWorkflow = ref({
  workflow_name: '',
  description: '',
  active: true
})


function openWorkflow(name) {
  router.push(`/workflow/${name}`)
}

async function createWorkflow() {
  try {
    const workflow = await workflowStore.createWorkflow(newWorkflow.value)
    showCreateModal.value = false
    newWorkflow.value = {
      workflow_name: '',
      description: '',
      active: true
    }
    router.push(`/workflow/${workflow.name}`)
  } catch (e) {
    alert('Error creating workflow: ' + e.message)
  }
}

function formatDate(dateStr) {
  if (!dateStr) return 'Never'
  const date = new Date(dateStr)
  const now = new Date()
  const diffMs = now - date
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)
  const diffWeeks = Math.floor(diffDays / 7)
  
  if (diffMins < 1) return 'just now'
  if (diffMins < 60) return `${diffMins} minutes ago`
  if (diffHours < 24) return `${diffHours} hours ago`
  if (diffDays < 7) return `${diffDays} days ago`
  if (diffWeeks < 4) return `${diffWeeks} weeks ago`
  
  return date.toLocaleDateString()
}

function toggleDropdown(workflowName) {
  openDropdown.value = openDropdown.value === workflowName ? null : workflowName
}

function confirmDelete(workflow) {
  workflowToDelete.value = workflow
  showDeleteModal.value = true
  openDropdown.value = null
}

async function deleteWorkflow() {
  if (!workflowToDelete.value) return
  
  try {
    await workflowStore.deleteWorkflow(workflowToDelete.value.name)
    showDeleteModal.value = false
    workflowToDelete.value = null
  } catch (e) {
    alert('Error deleting workflow: ' + e.message)
  }
}

async function toggleWorkflowStatus(workflow) {
  try {
    await workflowStore.updateWorkflowStatus(workflow.name, !workflow.active)
  } catch (e) {
    alert('Error updating workflow status: ' + e.message)
  }
}

// Close dropdown when clicking outside
function handleClickOutside(event) {
  if (openDropdown.value) {
    openDropdown.value = null
  }
}

onMounted(() => {
  workflowStore.fetchWorkflows()
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

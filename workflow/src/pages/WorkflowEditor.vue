<template>
  <div class="workflow-editor h-screen flex flex-col bg-gray-50">
    <!-- Header -->
    <div class="bg-white border-b border-gray-200 px-6 py-3 flex items-center justify-between">
      <div class="flex items-center gap-4">
        <button 
          @click="$router.push('/')"
          class="text-gray-600 hover:text-gray-900"
        >
          <ArrowLeft :size="20" />
        </button>
        <div>
          <h1 class="text-xl font-semibold text-gray-900">
            {{ workflowStore.currentWorkflow?.workflow_name || 'New Workflow' }}
          </h1>
          <p class="text-sm text-gray-500">
            {{ workflowStore.currentWorkflow?.description || 'Workflow automation' }}
          </p>
        </div>
      </div>
      
      <div class="flex items-center gap-3">
        <button
          @click="executeWorkflow"
          :disabled="!workflowStore.currentWorkflow || workflowStore.isLoading"
          class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
        >
          <Play :size="16" />
          Execute
        </button>
        
        <button
          @click="saveWorkflow"
          :disabled="workflowStore.isLoading"
          class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
        >
          <Save :size="16" />
          Save
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="flex-1 flex overflow-hidden">
      <!-- Sidebar - Trigger Selection for Empty Workflow -->
      <div v-if="workflowStore.nodes.length === 0 && showNodePane" class="w-80 bg-white border-r border-gray-200 overflow-y-auto">
        <div class="p-4">
          <!-- Back button for subcategory views -->
          <button 
            v-if="showAppTriggers || showAdvancedTriggers"
            @click="showAppTriggers = false; showAdvancedTriggers = false; triggerSearch = ''"
            class="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-3"
          >
            <ArrowLeft :size="18" />
            <span class="text-sm">Back</span>
          </button>

          <h2 class="text-lg font-semibold text-gray-900 mb-2">
            {{ showAppTriggers ? 'On app event' : showAdvancedTriggers ? 'Advanced triggers' : 'What triggers this workflow?' }}
          </h2>
          <p v-if="!showAppTriggers && !showAdvancedTriggers" class="text-sm text-gray-500 mb-4">A trigger is a step that starts your workflow</p>
          
          <!-- Search -->
          <div class="mb-4">
            <input
              v-model="triggerSearch"
              type="text"
              placeholder="Search nodes..."
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
            />
          </div>
          
          <!-- App Triggers List -->
          <div v-if="showAppTriggers" class="space-y-1">
            <div
              v-for="appNode in filteredAppTriggers"
              :key="appNode.type"
              @click="addNode(appNode)"
              class="p-3 rounded-lg cursor-pointer hover:bg-gray-100 transition-colors group flex items-center justify-between"
            >
              <div class="flex items-center gap-3">
                <component :is="appNode.icon" :size="20" :class="appNode.color" />
                <span class="text-sm font-medium text-gray-900">{{ appNode.label }}</span>
              </div>
              <svg class="w-4 h-4 text-gray-400 opacity-0 group-hover:opacity-100 transition-opacity" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </div>

          <!-- Advanced Triggers List -->
          <div v-else-if="showAdvancedTriggers" class="space-y-2">
            <div
              v-for="advNode in filteredAdvancedTriggers"
              :key="advNode.type"
              @click="addNode(advNode)"
              class="p-3 rounded-lg cursor-pointer hover:bg-gray-100 transition-colors group"
            >
              <div class="flex items-start gap-3">
                <div class="mt-0.5">
                  <component :is="advNode.icon" :size="20" :class="advNode.color" />
                </div>
                <div class="flex-1">
                  <div class="text-sm font-medium text-gray-900 mb-1">{{ advNode.label }}</div>
                  <div class="text-xs text-gray-500 leading-relaxed">{{ advNode.description }}</div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Main Triggers List -->
          <div v-else class="space-y-2">
            <div
              v-for="trigger in filteredTriggers"
              :key="trigger.type"
              @click="handleTriggerClick(trigger)"
              class="p-3 border border-gray-200 rounded-lg cursor-pointer hover:border-blue-500 hover:bg-blue-50 transition-colors group"
            >
              <div class="flex items-start gap-3">
                <div class="mt-0.5">
                  <component :is="trigger.icon" :size="20" :class="trigger.color" />
                </div>
                <div class="flex-1">
                  <div class="text-sm font-medium text-gray-900 mb-1">{{ trigger.label }}</div>
                  <div class="text-xs text-gray-500 leading-relaxed">{{ trigger.description }}</div>
                </div>
                <div class="opacity-0 group-hover:opacity-100 transition-opacity">
                  <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Sidebar - Node Palette for Non-Empty Workflow -->
      <div v-else-if="workflowStore.nodes.length > 0 && showNodePane" class="w-80 bg-white border-r border-gray-200 overflow-y-auto">
        <div class="p-4">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">Choose your next action</h2>
          
          <div class="space-y-2">
            <div
              v-for="nodeType in nodeTypes"
              :key="nodeType.type"
              draggable="true"
              @dragstart="onDragStart($event, nodeType)"
              @click="addNode(nodeType)"
              class="p-3 border border-gray-200 rounded-lg cursor-move hover:border-blue-500 hover:bg-blue-50 transition-colors"
            >
              <div class="flex items-center gap-2">
                <component :is="nodeType.icon" :size="18" :class="nodeType.color" />
                <div>
                  <div class="text-sm font-medium text-gray-900">{{ nodeType.label }}</div>
                  <div class="text-xs text-gray-500">{{ nodeType.description }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Canvas -->
      <div class="flex-1 relative">
        <!-- Floating Node Pane Toggle Button -->
        <button
          v-if="!showNodePane"
          @click="showNodePane = true"
          class="absolute top-4 left-4 z-20 w-12 h-12 bg-white rounded-lg shadow-lg hover:shadow-xl border border-gray-200 flex items-center justify-center group transition-all duration-300 hover:scale-105"
          title="Open node panel"
        >
          <svg class="w-6 h-6 text-gray-700 group-hover:text-blue-600 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>

        <!-- Close Node Pane Button (when pane is open) -->
        <button
          v-if="showNodePane"
          @click="showNodePane = false"
          class="absolute top-4 left-4 z-20 w-10 h-10 bg-white rounded-lg shadow-lg hover:shadow-xl border border-gray-200 flex items-center justify-center group transition-all duration-300 hover:scale-105"
          title="Close node panel"
        >
          <svg class="w-5 h-5 text-gray-700 group-hover:text-red-600 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        <!-- Canvas Toolbar -->
        <div class="absolute top-4 left-1/2 transform -translate-x-1/2 z-10 bg-white rounded-lg shadow-lg border border-gray-200 px-4 py-2 flex items-center gap-2">
          <button
            @click="fitView"
            class="p-2 hover:bg-gray-100 rounded transition-colors"
            title="Fit view"
          >
            <Maximize2 :size="18" />
          </button>
          <div class="w-px h-6 bg-gray-200"></div>
          <button
            @click="zoomIn"
            class="p-2 hover:bg-gray-100 rounded transition-colors"
            title="Zoom in"
          >
            <ZoomIn :size="18" />
          </button>
          <button
            @click="zoomOut"
            class="p-2 hover:bg-gray-100 rounded transition-colors"
            title="Zoom out"
          >
            <ZoomOut :size="18" />
          </button>
          <div class="w-px h-6 bg-gray-200"></div>
          <button
            @click="undo"
            :disabled="!canUndo"
            class="p-2 hover:bg-gray-100 rounded transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            title="Undo (Ctrl+Z)"
          >
            <Undo :size="18" />
          </button>
          <button
            @click="redo"
            :disabled="!canRedo"
            class="p-2 hover:bg-gray-100 rounded transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            title="Redo (Ctrl+Y)"
          >
            <Redo :size="18" />
          </button>
          <div class="w-px h-6 bg-gray-200"></div>
          <button
            @click="duplicateSelectedNode"
            :disabled="!workflowStore.selectedNode"
            class="p-2 hover:bg-gray-100 rounded transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            title="Duplicate (Ctrl+D)"
          >
            <Copy :size="18" />
          </button>
          <button
            @click="deleteSelectedNode"
            :disabled="!workflowStore.selectedNode"
            class="p-2 hover:bg-gray-100 rounded text-red-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            title="Delete (Delete)"
          >
            <Trash2 :size="18" />
          </button>
        </div>

        <!-- Empty State Placeholder - Modern & Actionable -->
        <div 
          v-if="workflowStore.nodes.length === 0"
          class="absolute inset-0 flex items-center justify-center z-10 pointer-events-none"
        >
          <div class="text-center pointer-events-auto">
            <!-- Animated Plus Button -->
            <div class="relative inline-block mb-6">
              <!-- Pulsing rings -->
              <div class="absolute inset-0 rounded-full bg-blue-500 opacity-20 animate-ping"></div>
              <div class="absolute inset-0 rounded-full bg-blue-400 opacity-30 animate-pulse"></div>
              
              <!-- Main button -->
              <button 
                class="relative w-24 h-24 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full shadow-lg hover:shadow-xl hover:scale-110 transition-all duration-300 flex items-center justify-center group"
                @click="showNodePane = true"
              >
                <div class="absolute inset-0 rounded-full bg-white opacity-0 group-hover:opacity-20 transition-opacity"></div>
                <svg class="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4" />
                </svg>
              </button>
            </div>

            <!-- Text with gradient -->
            <div class="mb-3">
              <h3 class="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-2">
                Add your first trigger
              </h3>
              <p class="text-gray-600 text-base">
                Choose a trigger from the sidebar to start building
              </p>
            </div>

            <!-- Arrow indicator pointing to sidebar -->
            <div class="flex items-center justify-center gap-2 text-blue-500 animate-bounce mt-6">
              <svg class="w-5 h-5 rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
              <span class="text-sm font-medium">Select from sidebar</span>
            </div>
          </div>
        </div>

        <VueFlow
          ref="vueFlowRef"
          v-model:nodes="workflowStore.nodes"
          v-model:edges="workflowStore.edges"
          @nodes-change="onNodesChange"
          @edges-change="onEdgesChange"
          @connect="onConnect"
          @node-click="onNodeClick"
          @edge-click="onEdgeClick"
          @pane-click="onPaneClick"
          @drop="onDrop"
          @dragover="onDragOver"
          :default-zoom="1"
          :min-zoom="0.2"
          :max-zoom="4"
          :snap-to-grid="true"
          :snap-grid="[15, 15]"
          class="workflow-canvas"
        >
          <Background pattern-color="#e5e7eb" :gap="16" />
          <Controls />
          <MiniMap />
          
          <template #node-custom="{ data, selected }">
            <CustomNode 
              :data="data" 
              :selected="selected" 
              @execute="handleNodeExecute"
              @chatAction="handleChatAction"
            />
          </template>
          
          <template #edge-default="props">
            <BaseEdge :id="props.id" :style="props.style" :path="props.path[0]" :marker-end="props.markerEnd" />
            <EdgeLabelRenderer>
              <button
                :style="{
                  position: 'absolute',
                  transform: `translate(-50%, -50%) translate(${props.labelX}px,${props.labelY}px)`,
                  pointerEvents: 'all',
                }"
                class="edge-delete-button"
                @click.stop="() => deleteEdgeById(props.id)"
              >
                <Trash2 :size="14" />
              </button>
            </EdgeLabelRenderer>
          </template>
        </VueFlow>
      </div>

      <!-- Properties Panel -->
      <div 
        v-if="workflowStore.selectedNode"
        class="w-80 bg-white border-l border-gray-200 overflow-y-auto"
      >
        <div class="p-4">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-sm font-semibold text-gray-700">Node Properties</h2>
            <button
              @click="deleteSelectedNode"
              class="text-red-600 hover:text-red-700"
            >
              <Trash2 :size="18" />
            </button>
          </div>
          
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Node Name
              </label>
              <input
                v-model="selectedNodeData.label"
                @input="updateSelectedNode"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Type
              </label>
              <input
                :value="selectedNodeData.type"
                type="text"
                disabled
                class="w-full px-3 py-2 border border-gray-300 rounded-lg bg-gray-50 text-gray-500"
              />
            </div>
            
            <div v-if="selectedNodeData.parameters">
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Parameters
              </label>
              <textarea
                v-model="selectedNodeParameters"
                @input="updateSelectedNodeParameters"
                rows="6"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Execution Result Modal -->
    <div
      v-if="showExecutionResult"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click="showExecutionResult = false"
    >
      <div
        @click.stop
        class="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[80vh] overflow-hidden flex flex-col"
      >
        <div class="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
          <h3 class="text-lg font-semibold text-gray-900">Execution Result</h3>
          <button @click="showExecutionResult = false" class="text-gray-400 hover:text-gray-600">
            <X :size="20" />
          </button>
        </div>
        
        <div class="p-6 overflow-y-auto">
          <pre class="bg-gray-50 p-4 rounded-lg text-sm overflow-x-auto">{{ JSON.stringify(executionResult, null, 2) }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { VueFlow, useVueFlow, BaseEdge, EdgeLabelRenderer } from '@vue-flow/core'
import { Background } from '@vue-flow/background'
import { Controls } from '@vue-flow/controls'
import { MiniMap } from '@vue-flow/minimap'
import { 
  ArrowLeft, Play, Save, Trash2, X,
  Zap, GitBranch, Code, Database, Mail, Webhook,
  Maximize2, ZoomIn, ZoomOut, Undo, Redo, Copy, MousePointer, MessageCircle
} from 'lucide-vue-next'
import { useWorkflowStore } from '@/stores/workflow'
import CustomNode from '@/components/workflow/CustomNode.vue'

const route = useRoute()
const router = useRouter()
const workflowStore = useWorkflowStore()
const vueFlowRef = ref(null)

const showExecutionResult = ref(false)
const executionResult = ref(null)
const selectedEdge = ref(null)
const selectedNodeData = ref({})
const selectedNodeParameters = ref('{}')
const draggedNodeType = ref(null)
const triggerSearch = ref('')
const showAppTriggers = ref(false)
const showAdvancedTriggers = ref(false)
const showNodePane = ref(false)

const canUndo = computed(() => workflowStore.canUndo)
const canRedo = computed(() => workflowStore.canRedo)

// App trigger nodes (for subcategory drill-down)
const appTriggerNodes = [
  { type: 'action-network', label: 'Action Network', icon: Webhook, color: 'text-blue-600' },
  { type: 'activecampaign', label: 'ActiveCampaign', icon: Mail, color: 'text-blue-700' },
  { type: 'acuity-scheduling', label: 'Acuity Scheduling', icon: Code, color: 'text-purple-600' },
  { type: 'adalo', label: 'Adalo', icon: Database, color: 'text-red-600' },
  { type: 'affinity', label: 'Affinity', icon: GitBranch, color: 'text-purple-700' },
  { type: 'agile-crm', label: 'Agile CRM', icon: Mail, color: 'text-blue-500' },
  { type: 'airtable', label: 'Airtable', icon: Database, color: 'text-yellow-600' },
  { type: 'airtop', label: 'Airtop', icon: Code, color: 'text-gray-700' },
  { type: 'amqp-trigger', label: 'AMQP Trigger', icon: Zap, color: 'text-orange-600' },
  { type: 'apitemplate', label: 'APITemplate.io', icon: Webhook, color: 'text-blue-600' },
  { type: 'asana', label: 'Asana', icon: Code, color: 'text-pink-600' },
  { type: 'autopilot', label: 'Autopilot', icon: Mail, color: 'text-teal-600' },
  { type: 'aws-certificate', label: 'AWS Certificate Manager', icon: Database, color: 'text-orange-700' },
  { type: 'aws-cognito', label: 'AWS Cognito', icon: Code, color: 'text-orange-600' },
  { type: 'aws-comprehend', label: 'AWS Comprehend', icon: Database, color: 'text-orange-500' }
]

// Trigger types for empty workflow
const triggerTypes = [
  {
    type: 'trigger-manual',
    label: 'When clicking \'Execute workflow\'',
    description: 'Runs the flow on clicking a button in n8n. Good for getting started quickly',
    icon: MousePointer,
    color: 'text-gray-400'
  },
  {
    type: 'trigger-app',
    label: 'On app event',
    description: 'Runs the flow when something happens in an app like Telegram, Notion or Airtable',
    icon: Webhook,
    color: 'text-blue-600',
    isSubcategory: true
  },
  {
    type: 'trigger-schedule',
    label: 'On a schedule',
    description: 'Runs the flow every day, hour, or custom interval',
    icon: Code,
    color: 'text-green-600'
  },
  {
    type: 'trigger-webhook',
    label: 'On webhook call',
    description: 'Runs the flow on receiving an HTTP request',
    icon: Webhook,
    color: 'text-indigo-600'
  },
  {
    type: 'trigger-form',
    label: 'On form submission',
    description: 'Generate webforms in n8n and pass their responses to the workflow',
    icon: Database,
    color: 'text-purple-600'
  },
  {
    type: 'trigger-workflow',
    label: 'When executed by another workflow',
    description: 'Runs the flow when called by the Execute Workflow node from a different workflow',
    icon: GitBranch,
    color: 'text-orange-600'
  },
  {
    type: 'chat-trigger',
    label: 'When chat message received',
    description: 'Runs the flow when a user sends a chat message. For use with AI nodes',
    icon: MessageCircle,
    color: 'text-pink-600'
  },
  {
    type: 'trigger-evaluation',
    label: 'When running evaluation',
    description: 'Run a dataset through your workflow to test performance',
    icon: Code,
    color: 'text-gray-600'
  },
  {
    type: 'trigger-advanced',
    label: 'Advanced triggers',
    description: 'Email triggers, file changes, system events, etc.',
    icon: Code,
    color: 'text-gray-600',
    isSubcategory: true
  }
]

// Advanced trigger nodes (for subcategory drill-down)
const advancedTriggerNodes = [
  { 
    type: 'email-imap', 
    label: 'Email Trigger (IMAP)', 
    description: 'Triggers the workflow when a new email is received',
    icon: Mail, 
    color: 'text-green-600' 
  },
  { 
    type: 'error-trigger', 
    label: 'Error Trigger', 
    description: 'Triggers the workflow when another workflow has an error',
    icon: Zap, 
    color: 'text-red-600' 
  },
  { 
    type: 'file-trigger', 
    label: 'File Trigger', 
    description: 'Triggers a workflow on file system changes',
    icon: Database, 
    color: 'text-blue-600' 
  },
  { 
    type: 'frappe-event', 
    label: 'Frappe Event Trigger', 
    description: 'Triggers on Frappe DocType events (save, submit, cancel)',
    icon: Code, 
    color: 'text-orange-600' 
  },
  { 
    type: 'cron-trigger', 
    label: 'Cron Trigger', 
    description: 'Advanced scheduling with cron expressions',
    icon: GitBranch, 
    color: 'text-purple-600' 
  },
  { 
    type: 'mqtt-trigger', 
    label: 'MQTT Trigger', 
    description: 'Triggers on MQTT message received',
    icon: Webhook, 
    color: 'text-teal-600' 
  },
  { 
    type: 'sse-trigger', 
    label: 'SSE Trigger', 
    description: 'Triggers the workflow when Server-Sent Events occur',
    icon: Zap, 
    color: 'text-indigo-600' 
  }
]

const filteredTriggers = computed(() => {
  if (!triggerSearch.value) return triggerTypes
  const search = triggerSearch.value.toLowerCase()
  return triggerTypes.filter(trigger => 
    trigger.label.toLowerCase().includes(search) || 
    trigger.description.toLowerCase().includes(search)
  )
})

const filteredAppTriggers = computed(() => {
  if (!triggerSearch.value) return appTriggerNodes
  const search = triggerSearch.value.toLowerCase()
  return appTriggerNodes.filter(node => 
    node.label.toLowerCase().includes(search)
  )
})

const filteredAdvancedTriggers = computed(() => {
  if (!triggerSearch.value) return advancedTriggerNodes
  const search = triggerSearch.value.toLowerCase()
  return advancedTriggerNodes.filter(node => 
    node.label.toLowerCase().includes(search) ||
    node.description.toLowerCase().includes(search)
  )
})

function handleTriggerClick(trigger) {
  if (trigger.isSubcategory) {
    if (trigger.type === 'trigger-app') {
      showAppTriggers.value = true
      showAdvancedTriggers.value = false
    } else if (trigger.type === 'trigger-advanced') {
      showAdvancedTriggers.value = true
      showAppTriggers.value = false
    }
    triggerSearch.value = ''
  } else {
    addNode(trigger)
  }
}

const nodeTypes = [
  {
    type: 'ai',
    label: 'AI',
    description: 'Build autonomous agents, summarize or search documents, etc.',
    icon: Code,
    color: 'text-purple-600'
  },
  {
    type: 'action',
    label: 'Action in an app',
    description: 'Do something in an app or service like Google Sheets, Telegram or Notion',
    icon: Webhook,
    color: 'text-blue-600'
  },
  {
    type: 'transform',
    label: 'Data transformation',
    description: 'Manipulate, filter or convert data',
    icon: Database,
    color: 'text-green-600'
  },
  {
    type: 'flow',
    label: 'Flow',
    description: 'Branch, merge or loop the flow, etc.',
    icon: GitBranch,
    color: 'text-orange-600'
  },
  {
    type: 'core',
    label: 'Core',
    description: 'Run code, make HTTP requests, set webhooks, etc.',
    icon: Code,
    color: 'text-gray-700'
  },
  {
    type: 'hitl',
    label: 'Human in the loop',
    description: 'Wait for approval or human input before continuing',
    icon: Mail,
    color: 'text-pink-600'
  },
  {
    type: 'trigger',
    label: 'Add another trigger',
    description: 'Workflows can have multiple triggers',
    icon: Zap,
    color: 'text-yellow-600'
  }
]

onMounted(async () => {
  const workflowName = route.params.name
  if (workflowName && workflowName !== 'new') {
    await workflowStore.loadWorkflow(workflowName)
  }
  
  // Add keyboard shortcuts
  window.addEventListener('keydown', handleKeyDown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown)
})

watch(() => workflowStore.selectedNode, (node) => {
  if (node) {
    selectedNodeData.value = { ...node.data }
    selectedNodeParameters.value = JSON.stringify(node.data.parameters || {}, null, 2)
  }
})

function handleKeyDown(event) {
  // Ctrl/Cmd + Z for undo
  if ((event.ctrlKey || event.metaKey) && event.key === 'z' && !event.shiftKey) {
    event.preventDefault()
    undo()
  }
  // Ctrl/Cmd + Y or Ctrl/Cmd + Shift + Z for redo
  else if ((event.ctrlKey || event.metaKey) && (event.key === 'y' || (event.key === 'z' && event.shiftKey))) {
    event.preventDefault()
    redo()
  }
  // Ctrl/Cmd + D for duplicate
  else if ((event.ctrlKey || event.metaKey) && event.key === 'd') {
    event.preventDefault()
    duplicateSelectedNode()
  }
  // Delete or Backspace
  if (event.key === 'Delete' || event.key === 'Backspace') {
    deleteSelectedItem()
  }
  
  // Escape to deselect
  if (event.key === 'Escape') {
    workflowStore.selectedNode = null
    selectedEdge.value = null
  }
  
  // Ctrl/Cmd + S to save
  if ((event.ctrlKey || event.metaKey) && event.key === 's') {
    event.preventDefault()
    saveWorkflow()
  }
}

function redo() {
  workflowStore.redo()
}

function duplicateSelectedNode() {
  if (!workflowStore.selectedNode) return
  
  const node = workflowStore.selectedNode
  const newPosition = {
    x: node.position.x + 50,
    y: node.position.y + 50
  }
  
  workflowStore.addNode({
    type: node.data.type,
    label: node.data.label + ' (Copy)',
    position: newPosition,
    parameters: { ...node.data.parameters }
  })
}

function onNodesChange(changes) {
  // Handle node changes
}

function onEdgesChange(changes) {
  // Handle edge changes
}

function onConnect(params) {
  // Validate connection - prevent self-loops
  if (params.source === params.target) {
    console.warn('Cannot connect a node to itself')
    return
  }
  
  // Check if connection already exists
  const existingEdge = workflowStore.edges.find(
    edge => edge.source === params.source && edge.target === params.target
  )
  
  if (existingEdge) {
    console.warn('Connection already exists')
    return
  }
  
  workflowStore.addEdge(params)
}

function onNodeClick(event) {
  workflowStore.selectedNode = event.node
}

function onPaneClick() {
  workflowStore.selectedNode = null
  selectedEdge.value = null
}

function onEdgeClick(event) {
  // Deselect any selected node
  workflowStore.selectedNode = null
  // Select the clicked edge
  selectedEdge.value = event.edge
  
  // Update edge selection state in the store
  workflowStore.edges = workflowStore.edges.map(edge => ({
    ...edge,
    selected: edge.id === event.edge.id
  }))
}

function deleteSelectedEdge() {
  if (selectedEdge.value) {
    workflowStore.removeEdge(selectedEdge.value.id)
    selectedEdge.value = null
  }
}

function deleteEdgeById(edgeId) {
  workflowStore.removeEdge(edgeId)
  if (selectedEdge.value?.id === edgeId) {
    selectedEdge.value = null
  }
}

function deleteSelectedItem() {
  if (selectedEdge.value) {
    deleteSelectedEdge()
  } else if (workflowStore.selectedNode) {
    deleteSelectedNode()
  }
}

function updateSelectedNode() {
  if (workflowStore.selectedNode) {
    workflowStore.updateNode(workflowStore.selectedNode.id, {
      data: selectedNodeData.value
    })
  }
}

function updateSelectedNodeParameters() {
  try {
    const params = JSON.parse(selectedNodeParameters.value)
    selectedNodeData.value.parameters = params
    updateSelectedNode()
  } catch (e) {
    console.error('Invalid JSON')
  }
}

function deleteSelectedNode() {
  if (workflowStore.selectedNode) {
    workflowStore.removeNode(workflowStore.selectedNode.id)
    workflowStore.selectedNode = null
  }
}

function addNode(nodeType) {
  const position = {
    x: Math.random() * 400 + 100,
    y: Math.random() * 300 + 100
  }
  
  workflowStore.addNode({
    type: nodeType.type,
    label: nodeType.label,
    position: position,
    data: {
      type: nodeType.type,
      label: nodeType.label,
      description: nodeType.description,
      icon: nodeType.icon,
      color: nodeType.color,
      parameters: {}
    }
  })
  
  // Close the node pane after adding
  showNodePane.value = false
  showAppTriggers.value = false
  showAdvancedTriggers.value = false
}

function handleNodeExecute(nodeId) {
  console.log('Execute node:', nodeId)
  // Find the node and trigger execution
  const node = workflowStore.nodes.find(n => n.id === nodeId)
  if (node) {
    executeWorkflow()
  }
}

function handleChatAction(nodeId) {
  console.log('Open chat for node:', nodeId)
  // TODO: Implement chat panel/modal
  alert('Chat interface would open here. This can be connected to a chat UI component.')
}

async function saveWorkflow() {
  try {
    await workflowStore.saveWorkflow()
    alert('Workflow saved successfully!')
  } catch (e) {
    alert('Error saving workflow: ' + e.message)
  }
}

async function executeWorkflow() {
  try {
    const result = await workflowStore.executeWorkflow(
      workflowStore.currentWorkflow.name
    )
    executionResult.value = result
    showExecutionResult.value = true
  } catch (e) {
    alert('Error executing workflow: ' + e.message)
  }
}
</script>

<style>
@import '@vue-flow/core/dist/style.css';
@import '@vue-flow/core/dist/theme-default.css';
@import '@vue-flow/controls/dist/style.css';
@import '@vue-flow/minimap/dist/style.css';

.workflow-canvas {
  background-color: #fafafa;
}

/* Override default node styles since we use custom nodes */
.vue-flow__node {
  padding: 0;
  border: none;
  background: transparent;
}

.vue-flow__node.selected {
  border: none;
  box-shadow: none;
}

/* Edge styling */
.vue-flow__edge {
  cursor: pointer;
}

.vue-flow__edge-path {
  stroke: #9ca3af;
  stroke-width: 2;
  transition: all 0.2s ease;
}

.vue-flow__edge:hover .vue-flow__edge-path {
  stroke: #6b7280;
  stroke-width: 3;
}

.vue-flow__edge.selected .vue-flow__edge-path {
  stroke: #3b82f6;
  stroke-width: 3;
  stroke-dasharray: 5, 5;
  animation: dash 0.5s linear infinite;
}

.vue-flow__edge.animated .vue-flow__edge-path {
  stroke: #3b82f6;
  stroke-width: 2.5;
}

@keyframes dash {
  to {
    stroke-dashoffset: -10;
  }
}

.vue-flow__edge-textwrapper {
  pointer-events: all;
}

.vue-flow__edge-text {
  fill: #374151;
  font-size: 12px;
}

/* Edge delete button */
.edge-delete-button {
  width: 24px;
  height: 24px;
  background: white;
  border: 2px solid #ef4444;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: all 0.2s ease;
  pointer-events: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.vue-flow__edge:hover .edge-delete-button,
.vue-flow__edge.selected .edge-delete-button {
  opacity: 1;
  pointer-events: all;
}

.edge-delete-button:hover {
  background: #ef4444;
  transform: scale(1.15);
  box-shadow: 0 4px 8px rgba(239, 68, 68, 0.3);
}

.edge-delete-button svg {
  stroke: #ef4444;
  transition: stroke 0.2s ease;
}

.edge-delete-button:hover svg {
  stroke: white;
}

/* Handle styling */
.vue-flow__handle {
  width: 12px;
  height: 12px;
  background: #3b82f6;
  border: 2px solid white;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.vue-flow__handle:hover {
  width: 16px;
  height: 16px;
  background: #2563eb;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.2);
}

.vue-flow__handle-connecting {
  background: #10b981;
}

.vue-flow__handle-valid {
  background: #10b981;
}

/* Controls styling */
.vue-flow__controls {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

.vue-flow__controls-button {
  border: none;
  border-bottom: 1px solid #e5e7eb;
  background: white;
  transition: background-color 0.2s ease;
}

.vue-flow__controls-button:hover {
  background: #f3f4f6;
}

.vue-flow__controls-button:last-child {
  border-bottom: none;
}

/* Minimap styling */
.vue-flow__minimap {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.vue-flow__minimap-mask {
  fill: rgba(59, 130, 246, 0.1);
  stroke: #3b82f6;
  stroke-width: 2;
}

.vue-flow__minimap-node {
  fill: #d1d5db;
  stroke: #9ca3af;
}

/* Background pattern */
.vue-flow__background {
  background-color: #fafafa;
}

/* Selection box */
.vue-flow__selection {
  background: rgba(59, 130, 246, 0.1);
  border: 1px solid #3b82f6;
}

/* Connection line while dragging */
.vue-flow__connectionline {
  stroke: #3b82f6;
  stroke-width: 2;
}

.vue-flow__connectionline-path {
  stroke: #3b82f6;
  stroke-width: 2;
}
</style>

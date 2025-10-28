<template>
  <!-- n8n-style trigger node -->
  <div 
    v-if="isTriggerManually" 
    class="n8n-trigger-node"
    :class="{
      'node-selected': selected,
      'node-executing': data.isExecuting,
      'node-error': data.hasError,
      'node-success': data.executionSuccess,
      'node-hovered': isHovered
    }"
    @mouseenter="isHovered = true"
    @mouseleave="isHovered = false"
  >
    <Handle 
      type="target" 
      :position="Position.Left" 
      class="n8n-handle n8n-handle-target"
    />
    
    <!-- Trigger button wrapper (left side) -->
    <div class="trigger-action-wrapper">
      <!-- Bolt icon (default state) -->
      <div class="bolt-icon">
        <Zap :size="20" class="text-blue-600" fill="currentColor" />
      </div>
      
      <!-- Execute button (hover state) -->
      <button 
        class="execute-button"
        :disabled="data.isExecuting"
        @click.stop="handleExecute"
      >
        <FlaskConical :size="16" />
        <span>Execute Workflow</span>
      </button>
    </div>
    
    <!-- Main node body -->
    <div class="n8n-trigger-body">
      <component 
        :is="nodeIcon" 
        :size="40" 
        :class="nodeColor"
      />
    </div>
    
    <!-- Status icons -->
    <div v-if="data.isExecuting || data.hasError || data.executionSuccess" class="status-icons">
      <div v-if="data.isExecuting" class="execution-spinner">
        <div class="spinner"></div>
      </div>
      <AlertCircle v-else-if="data.hasError" :size="16" class="text-red-500" />
      <CheckCircle v-else-if="data.executionSuccess" :size="16" class="text-green-500" />
    </div>
    
    <Handle 
      type="source" 
      :position="Position.Right" 
      class="n8n-handle n8n-handle-source"
    />
    
    <!-- Label below node -->
    <div class="node-description">
      <div class="node-label">{{ data.label }}</div>
      <div v-if="data.type" class="node-subtitle">{{ data.type }}</div>
    </div>
  </div>
  
  <!-- AI Agent node with multiple connection points -->
  <div v-else-if="isAIAgent" class="ai-agent-node"
    :class="{
      'node-selected': selected,
      'node-executing': data.isExecuting,
      'node-error': data.hasError,
      'node-success': data.executionSuccess
    }"
  >
    <Handle 
      type="target" 
      :position="Position.Left" 
      class="modern-handle modern-handle-target"
    />
    
    <!-- Main content -->
    <div class="ai-node-header">
      <div class="ai-icon-wrapper">
        <Bot :size="24" class="text-purple-600" />
      </div>
      <div class="ai-node-content">
        <div class="text-base font-semibold text-gray-900">{{ data.label }}</div>
        <div class="text-xs text-gray-500">{{ data.type }}</div>
      </div>
      
      <!-- Status indicator -->
      <div v-if="data.isExecuting" class="execution-spinner">
        <div class="spinner"></div>
      </div>
      <div v-else-if="data.hasError" class="status-icon">
        <AlertCircle :size="18" class="text-red-500" />
      </div>
      <div v-else-if="data.executionSuccess" class="status-icon">
        <CheckCircle :size="18" class="text-green-500" />
      </div>
    </div>
    
    <!-- Sub-connections (Chat Model, Memory, Tool) -->
    <div class="ai-sub-connections">
      <div class="ai-sub-port">
        <div class="ai-sub-label">Chat Model</div>
        <Handle 
          :id="`${data.id}-chat-model`"
          type="target" 
          :position="Position.Bottom"
          class="ai-sub-handle"
          :style="{ left: '25%' }"
        />
        <div class="ai-sub-plus">
          <Plus :size="10" class="text-gray-500" />
        </div>
      </div>
      
      <div class="ai-sub-port">
        <div class="ai-sub-label">Memory</div>
        <Handle 
          :id="`${data.id}-memory`"
          type="target" 
          :position="Position.Bottom"
          class="ai-sub-handle"
          :style="{ left: '50%' }"
        />
        <div class="ai-sub-plus">
          <Plus :size="10" class="text-gray-500" />
        </div>
      </div>
      
      <div class="ai-sub-port">
        <div class="ai-sub-label">Tool</div>
        <Handle 
          :id="`${data.id}-tool`"
          type="target" 
          :position="Position.Bottom"
          class="ai-sub-handle"
          :style="{ left: '75%' }"
        />
        <div class="ai-sub-plus">
          <Plus :size="10" class="text-gray-500" />
        </div>
      </div>
    </div>
    
    <Handle 
      type="source" 
      :position="Position.Right" 
      class="modern-handle modern-handle-source"
    />
  </div>
  
  <!-- Standard node design for other node types -->
  <div 
    v-else
    class="custom-node"
    :class="{
      'node-selected': selected,
      'node-executing': data.isExecuting,
      'node-error': data.hasError,
      'node-success': data.executionSuccess
    }"
  >
    <Handle 
      type="target" 
      :position="Position.Left" 
      class="node-handle node-handle-target"
    />
    
    <div class="node-header" :style="{ borderLeftColor: nodeBorderColor }">
      <div class="flex items-center gap-2 flex-1">
        <div class="node-icon-wrapper" :style="{ backgroundColor: nodeIconBg }">
          <component 
            :is="nodeIcon" 
            :size="16" 
            :class="nodeColor"
          />
        </div>
        <div class="flex-1 min-w-0">
          <div class="text-sm font-medium text-gray-900 truncate">{{ data.label }}</div>
          <div class="text-xs text-gray-500">{{ data.type }}</div>
        </div>
      </div>
      
      <!-- Execution status indicator -->
      <div v-if="data.isExecuting" class="execution-spinner">
        <div class="spinner"></div>
      </div>
      <div v-else-if="data.hasError" class="status-icon text-red-500">
        <AlertCircle :size="16" />
      </div>
      <div v-else-if="data.executionSuccess" class="status-icon text-green-500">
        <CheckCircle :size="16" />
      </div>
    </div>
    
    <!-- Parameters preview -->
    <div v-if="data.parameters && Object.keys(data.parameters).length > 0" class="node-params">
      <div class="text-xs text-gray-600">
        {{ Object.keys(data.parameters).length }} parameter(s)
      </div>
    </div>
    
    <Handle 
      type="source" 
      :position="Position.Right" 
      class="node-handle node-handle-source"
    />
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { Handle, Position } from '@vue-flow/core'
import { 
  Zap, Code, GitBranch, Database, Mail, Webhook, Box,
  AlertCircle, CheckCircle, MousePointer, Plus, Bot, FlaskConical
} from 'lucide-vue-next'

const props = defineProps({
  data: {
    type: Object,
    required: true
  },
  selected: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['execute'])

const isHovered = ref(false)

function handleExecute() {
  emit('execute', props.data.id)
}

const isTriggerManually = computed(() => {
  return props.data.type === 'trigger-manual' ||
         props.data.label?.toLowerCase().includes('trigger manually') ||
         props.data.label?.toLowerCase().includes('manual trigger') ||
         props.data.nodeType === 'trigger_manually'
})

const isAIAgent = computed(() => {
  return props.data.type === 'ai' ||
         props.data.label?.toLowerCase().includes('ai agent') ||
         props.data.label?.toLowerCase().includes('ai') ||
         props.data.nodeType === 'ai_agent'
})

const nodeIcon = computed(() => {
  const iconMap = {
    trigger: Zap,
    action: Webhook,
    condition: GitBranch,
    transform: Database,
    email: Mail,
    webhook: Webhook,
    ai: Bot,
    flow: GitBranch,
    core: Code,
    hitl: Mail
  }
  return iconMap[props.data.type] || Box
})

const nodeColor = computed(() => {
  const colorMap = {
    trigger: 'text-yellow-600',
    action: 'text-blue-600',
    condition: 'text-purple-600',
    transform: 'text-green-600',
    email: 'text-red-600',
    webhook: 'text-indigo-600',
    ai: 'text-purple-600',
    flow: 'text-orange-600',
    core: 'text-gray-700',
    hitl: 'text-pink-600'
  }
  return colorMap[props.data.type] || 'text-gray-600'
})

const nodeBorderColor = computed(() => {
  const colorMap = {
    trigger: '#ca8a04',
    action: '#2563eb',
    condition: '#9333ea',
    transform: '#16a34a',
    email: '#dc2626',
    webhook: '#4f46e5',
    ai: '#9333ea',
    flow: '#ea580c',
    core: '#374151',
    hitl: '#db2777'
  }
  return colorMap[props.data.type] || '#6b7280'
})

const nodeIconBg = computed(() => {
  const colorMap = {
    trigger: '#fef3c7',
    action: '#dbeafe',
    condition: '#f3e8ff',
    transform: '#dcfce7',
    email: '#fee2e2',
    webhook: '#e0e7ff',
    ai: '#f3e8ff',
    flow: '#ffedd5',
    core: '#f3f4f6',
    hitl: '#fce7f3'
  }
  return colorMap[props.data.type] || '#f3f4f6'
})
</script>

<style scoped>
.custom-node {
  border-radius: 8px;
  background: white;
  border: 2px solid #e5e7eb;
  min-width: 200px;
  max-width: 280px;
  position: relative;
  transition: all 0.2s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.custom-node:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-1px);
}

.custom-node.node-selected {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}

.custom-node.node-executing {
  border-color: #f59e0b;
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.custom-node.node-error {
  border-color: #ef4444;
  background: #fef2f2;
}

.custom-node.node-success {
  border-color: #10b981;
}

.node-header {
  padding: 12px;
  border-left: 4px solid;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.node-icon-wrapper {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.node-params {
  padding: 8px 12px;
  border-top: 1px solid #f3f4f6;
  background: #fafafa;
}

.node-handle {
  width: 12px;
  height: 12px;
  background: #3b82f6;
  border: 2px solid white;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.node-handle:hover {
  width: 16px;
  height: 16px;
  background: #2563eb;
}

.node-handle-target {
  left: -6px;
}

.node-handle-source {
  right: -6px;
}

.execution-spinner {
  display: flex;
  align-items: center;
  justify-content: center;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid #f3f4f6;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.status-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

/* n8n-style Trigger Node */
.n8n-trigger-node {
  --node-width: 100px;
  --node-height: 100px;
  --border-width: 2px;
  --trigger-radius: 36px;
  
  position: relative;
  width: var(--node-width);
  height: var(--node-height);
  display: flex;
  align-items: center;
  justify-content: center;
}

.n8n-trigger-body {
  width: 100%;
  height: 100%;
  background: white;
  border: var(--border-width) solid #e5e7eb;
  border-radius: var(--trigger-radius) 8px 8px var(--trigger-radius);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  transition: all 0.2s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.n8n-trigger-node:hover .n8n-trigger-body {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-1px);
}

/* Node States */
.n8n-trigger-node.node-selected .n8n-trigger-body {
  box-shadow: 0 0 0 8px rgba(59, 130, 246, 0.2);
  border-color: #3b82f6;
}

.n8n-trigger-node.node-executing .n8n-trigger-body {
  background-color: #fef3c7;
  border-color: #f59e0b;
}

.n8n-trigger-node.node-error .n8n-trigger-body {
  border-color: #ef4444;
  background: #fef2f2;
}

.n8n-trigger-node.node-success .n8n-trigger-body {
  border-color: #10b981;
}

/* Trigger Action Wrapper (Left Side) */
.trigger-action-wrapper {
  position: absolute;
  right: 100%;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  align-items: center;
  pointer-events: none;
  z-index: 1;
}

/* Bolt Icon (Default State) */
.bolt-icon {
  padding: 8px;
  opacity: 1;
  translate: 0 0;
  transition: translate 0.1s ease-in, opacity 0.1s ease-in;
  display: flex;
  align-items: center;
  justify-content: center;
}

.n8n-trigger-node.node-hovered .bolt-icon {
  translate: -12px 0;
  opacity: 0;
}

/* Execute Button (Hover State) */
.execute-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  margin-right: 12px;
  opacity: 0;
  translate: -12px 0;
  transition: all 0.1s ease-in;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  white-space: nowrap;
}

.n8n-trigger-node.node-hovered .execute-button {
  opacity: 1;
  translate: 0 0;
  pointer-events: all;
}

.execute-button:hover:not(:disabled) {
  background: #2563eb;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.execute-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Status Icons */
.status-icons {
  position: absolute;
  bottom: 4px;
  right: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Node Description (Below Node) */
.node-description {
  position: absolute;
  top: 100%;
  width: 100%;
  min-width: 200px;
  margin-top: 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  pointer-events: none;
}

.node-label {
  font-size: 14px;
  font-weight: 500;
  text-align: center;
  color: #1f2937;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  line-height: 1.4;
}

.node-subtitle {
  font-size: 12px;
  text-align: center;
  color: #6b7280;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* n8n Handle Styles */
.n8n-handle {
  width: 12px;
  height: 12px;
  background: white;
  border: 2px solid #9ca3af;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.n8n-handle:hover {
  width: 16px;
  height: 16px;
  border-color: #3b82f6;
  background: #dbeafe;
}

.n8n-handle-target {
  left: -6px;
}

.n8n-handle-source {
  right: -6px;
}

/* AI Agent Node - Horizontal with Sub-connections */
.ai-agent-node {
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  min-width: 280px;
  max-width: 320px;
  position: relative;
  transition: all 0.2s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  padding-bottom: 40px;
}

.ai-agent-node:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-1px);
}

.ai-agent-node.node-selected {
  border-color: #9333ea;
  box-shadow: 0 0 0 3px rgba(147, 51, 234, 0.2);
}

.ai-agent-node.node-executing {
  border-color: #f59e0b;
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.ai-agent-node.node-error {
  border-color: #ef4444;
  background: #fef2f2;
}

.ai-agent-node.node-success {
  border-color: #10b981;
}

.ai-node-header {
  padding: 14px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid #f3f4f6;
}

.ai-icon-wrapper {
  width: 40px;
  height: 40px;
  background: #f3e8ff;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.ai-node-content {
  flex: 1;
  min-width: 0;
}

.ai-sub-connections {
  display: flex;
  justify-content: space-around;
  padding: 12px 16px 0;
  position: relative;
}

.ai-sub-port {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  position: relative;
}

.ai-sub-label {
  font-size: 11px;
  font-weight: 500;
  color: #6b7280;
  text-align: center;
}

.ai-sub-handle {
  width: 12px;
  height: 12px;
  background: white;
  border: 2px solid #9ca3af;
  border-radius: 50%;
  transition: all 0.2s ease;
  bottom: -20px;
}

.ai-sub-handle:hover {
  width: 16px;
  height: 16px;
  border-color: #9333ea;
  background: #f3e8ff;
}

.ai-sub-plus {
  width: 16px;
  height: 16px;
  background: white;
  border: 1.5px solid #d1d5db;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.ai-sub-plus:hover {
  border-color: #9333ea;
  background: #f3e8ff;
}
</style>

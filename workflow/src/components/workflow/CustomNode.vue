<template>
  <!-- Modern trigger manually node -->
  <div v-if="isTriggerManually" class="trigger-manual-node">
    <Handle 
      type="target" 
      :position="Position.Left" 
      class="modern-handle modern-handle-hidden"
    />
    
    <!-- Lightning bolt badge -->
    <div class="trigger-badge">
      <Zap :size="16" class="text-white" fill="currentColor" />
    </div>
    
    <!-- Main node body -->
    <div class="trigger-node-body">
      <MousePointer :size="56" class="text-gray-300" strokeWidth="1.5" />
    </div>
    
    <!-- Connection handle with plus icon -->
    <div class="trigger-connection-wrapper">
      <Handle 
        type="source" 
        :position="Position.Right" 
        class="modern-handle modern-handle-source"
      />
      <div class="trigger-plus-icon">
        <Plus :size="14" class="text-gray-500" strokeWidth="2" />
      </div>
    </div>
    
    <!-- Label below node -->
    <div class="trigger-node-label">
      When clicking 'Execute workflow'
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
import { computed } from 'vue'
import { Handle, Position } from '@vue-flow/core'
import { 
  Zap, Code, GitBranch, Database, Mail, Webhook, Box,
  AlertCircle, CheckCircle, MousePointer, Plus, Bot
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

/* Modern Trigger Manually Node - Light Theme */
.trigger-manual-node {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 150px;
}

.trigger-node-body {
  width: 140px;
  height: 140px;
  background: #4b5563;
  border: 3px solid #6b7280;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.trigger-node-body:hover {
  border-color: #9ca3af;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  transform: translateY(-2px);
}

.trigger-badge {
  position: absolute;
  top: 10px;
  left: 10px;
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  box-shadow: 0 4px 6px -1px rgba(239, 68, 68, 0.3);
}

.trigger-connection-wrapper {
  position: absolute;
  right: -20px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  align-items: center;
  gap: 6px;
}

.trigger-plus-icon {
  width: 24px;
  height: 24px;
  background: white;
  border: 2px solid #d1d5db;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.trigger-plus-icon:hover {
  border-color: #3b82f6;
  background: #eff6ff;
  box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.2);
}

.trigger-node-label {
  margin-top: 16px;
  font-size: 14px;
  font-weight: 500;
  color: #1f2937;
  text-align: center;
  max-width: 180px;
  line-height: 1.5;
}

/* Modern Handle Styles */
.modern-handle {
  width: 14px;
  height: 14px;
  background: white;
  border: 2px solid #9ca3af;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.modern-handle:hover {
  width: 18px;
  height: 18px;
  border-color: #3b82f6;
  background: #dbeafe;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

.modern-handle-hidden {
  opacity: 0;
  pointer-events: none;
}

.modern-handle-target {
  left: -7px;
}

.modern-handle-source {
  position: relative;
  right: auto;
  left: auto;
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

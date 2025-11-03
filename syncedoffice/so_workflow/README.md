# SO Workflow - n8n-inspired Workflow Automation

A modern, light-themed workflow automation system built for SyncedOffice, inspired by n8n.

## ✅ MVP Status: COMPLETE

The workflow MVP is **production-ready** with full backend infrastructure, 6 functional node types, robust execution engine, complete API coverage, and comprehensive documentation.

**Quick Links:**
- 📖 [MVP Complete Documentation](MVP_COMPLETE.md) - Full feature overview
- 🚀 [Quick Start Guide](QUICK_START.md) - Get started in minutes
- 📝 [Node Types Reference](NODE_TYPES.md) - Available node types
- 👨‍💻 [Developer Guide](DEVELOPER_GUIDE.md) - API reference and patterns
- 📊 [Implementation Summary](IMPLEMENTATION_SUMMARY.md) - Technical details

## Features

- **Visual Workflow Editor**: Drag-and-drop canvas-based workflow builder using Vue Flow
- **Node-based Architecture**: Modular nodes for triggers, actions, transformations, and conditions
- **Execution Engine**: Robust workflow execution with logging and error handling
- **Execution Tracking**: Complete audit trail of workflow runs
- **Extensible**: Create custom nodes with Python code
- **Modern UI**: Clean, light theme with intuitive interface

## Architecture

### Backend (Frappe)

#### DocTypes

1. **Workflow**: Main workflow definition
   - Stores nodes, connections, and settings
   - Version tracking
   - Execution statistics

2. **Workflow Node**: Reusable node definitions
   - Node types: Trigger, Action, Transform, Condition, Loop, Custom
   - Parameter schemas
   - Python code templates

3. **Workflow Execution**: Execution tracking
   - Status monitoring
   - Input/output data
   - Execution logs
   - Performance metrics

#### Execution Engine

The workflow engine (`workflow_engine.py`) provides:
- Topological sorting for node execution order
- Dependency resolution
- Error handling and logging
- Node input/output management

### Frontend (Vue.js)

Built with:
- **Vue 3**: Modern reactive framework
- **Vue Flow**: Canvas-based workflow editor
- **Pinia**: State management
- **TailwindCSS**: Utility-first styling
- **Lucide Icons**: Modern icon set

#### Key Components

- `WorkflowList.vue`: Browse and manage workflows
- `WorkflowEditor.vue`: Visual workflow editor
- `CustomNode.vue`: Node rendering component
- `workflow.js` (Pinia store): State management

## Usage

### Creating a Workflow

1. Navigate to `/workflow` in your browser
2. Click "New Workflow"
3. Enter workflow name and description
4. Click "Create Workflow"

### Building a Workflow

1. Drag nodes from the left sidebar onto the canvas
2. Connect nodes by dragging from output handles to input handles
3. Click a node to edit its properties in the right panel
4. Save your workflow

### Executing a Workflow

1. Click the "Execute" button in the workflow editor
2. View execution results in the modal
3. Check execution history in the Workflow Execution doctype

## Available Nodes

### Triggers
- **Manual Trigger**: Start workflow manually

### Actions
- **HTTP Request**: Make API calls
- **Send Email**: Send email notifications
- **Frappe API Call**: Call Frappe methods

### Data
- **Transform Data**: Manipulate and transform data

### Logic
- **If Condition**: Branch based on conditions

## API Endpoints

### Workflow Management
```python
# Get workflow
frappe.call('syncedoffice.so_workflow.doctype.workflow.workflow.get_workflow', {
    name: 'workflow_name'
})

# Save workflow
frappe.call('syncedoffice.so_workflow.doctype.workflow.workflow.save_workflow', {
    workflow_data: {...}
})

# Execute workflow
frappe.call('syncedoffice.so_workflow.doctype.workflow.workflow.execute_workflow_api', {
    name: 'workflow_name',
    input_data: {...}
})

# List workflows
frappe.call('syncedoffice.so_workflow.doctype.workflow.workflow.get_workflow_list')
```

### Node Management
```python
# Get available nodes
frappe.call('syncedoffice.so_workflow.doctype.workflow_node.workflow_node.get_available_nodes')
```

## Extending with Custom Nodes

Create custom nodes by:

1. Creating a new Workflow Node document
2. Set `is_custom` to 1
3. Define parameter schema (JSON)
4. Write Python code template
5. Use in workflows

Example custom node:
```json
{
    "node_name": "My Custom Node",
    "node_type": "Custom",
    "description": "Does something custom",
    "parameters": {
        "param1": {"type": "string", "required": true}
    },
    "code_template": "# Your Python code here\nreturn {'result': 'success'}"
}
```

## Installation

1. Install workflow UI dependencies:
```bash
cd apps/syncedoffice/workflow
yarn install
```

2. Migrate DocTypes:
```bash
bench --site [site-name] migrate
```

3. Import fixtures:
```bash
bench --site [site-name] import-doc syncedoffice/so_workflow/fixtures/workflow_node.json
```

4. Build workflow UI:
```bash
cd apps/syncedoffice/workflow
yarn build
```

## Development

### Workflow UI Development
```bash
cd apps/syncedoffice/workflow
yarn dev
```

### Backend Development
- Edit DocTypes in `syncedoffice/so_workflow/doctype/`
- Modify execution engine in `workflow_engine.py`
- Add new nodes to `fixtures/workflow_node.json`

## Differences from n8n

While inspired by n8n, this implementation:
- Uses a **light theme** instead of dark
- Integrates natively with **Frappe Framework**
- Simplified for **MVP** functionality
- Focused on **internal automation** use cases
- Uses **Python** for node execution instead of JavaScript

## Future Enhancements

- [ ] Webhook triggers
- [ ] Scheduled workflows (cron)
- [ ] Sub-workflows
- [ ] Loop nodes
- [ ] Error handling nodes
- [ ] Workflow templates
- [ ] Collaborative editing
- [ ] Workflow versioning UI
- [ ] Performance optimization
- [ ] Advanced node types (AI, Database, etc.)

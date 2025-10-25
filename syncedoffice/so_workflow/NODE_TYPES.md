# n8n-Inspired Node Type System

## Overview

The workflow module now implements an n8n-inspired node type system that provides:

- **Reusable Node Types**: Define node types once, use them across multiple workflows
- **Dynamic Properties**: Configure node behavior through JSON-defined properties
- **Type Safety**: Validate node parameters against type definitions
- **Extensibility**: Easy to add custom node types via Python modules or built-in executors
- **Registry System**: Centralized node type management and loading

## Architecture

### Core Components

1. **Workflow Node Type DocType** (`workflow_node_type.json`)
   - Stores node type definitions in the database
   - Defines inputs, outputs, properties, and execution methods
   - Supports versioning and categorization

2. **Node Type Registry** (`node_type_registry.py`)
   - Loads and caches node type definitions
   - Provides lookup and validation services
   - Manages node executor resolution

3. **Node Executors** (`node_executors.py`)
   - Built-in execution methods for common node types
   - Execution context for accessing inputs and parameters
   - Support for Python, JavaScript, HTTP, and Frappe API calls

4. **Workflow Engine** (`workflow_engine.py`)
   - Updated to use node type registry
   - Validates nodes against type definitions
   - Routes execution to appropriate executors

## Node Type Structure

A node type definition includes:

```json
{
  "node_type_name": "n8n-nodes-base.httpRequest",
  "display_name": "HTTP Request",
  "description": "Makes an HTTP request and returns the response",
  "category": "Core",
  "icon": "fa-globe",
  "icon_color": "#2196F3",
  "version": 1,
  "inputs": ["main"],
  "outputs": ["main"],
  "execute_method": "HTTP Request",
  "properties": [
    {
      "displayName": "URL",
      "name": "url",
      "type": "string",
      "default": "",
      "required": true,
      "description": "The URL to make the request to"
    }
  ]
}
```

## Built-in Node Types

### Core Nodes

1. **HTTP Request** (`n8n-nodes-base.httpRequest`)
   - Make HTTP requests to external APIs
   - Supports GET, POST, PUT, DELETE, PATCH
   - Authentication: None, Basic Auth, Bearer Token
   - Custom headers and body

2. **Set** (`n8n-nodes-base.set`)
   - Set values on items
   - Option to keep only set values or merge with input
   - JSON-based value configuration

3. **Code** (`n8n-nodes-base.code`)
   - Execute custom Python code
   - Access input data and set output
   - Run once for all items or per item

4. **Frappe API** (`frappe.api`)
   - Execute Frappe API operations
   - Operations: get_doc, get_list, insert, update, delete
   - Direct integration with Frappe backend

### Control Flow Nodes

5. **IF** (`n8n-nodes-base.if`)
   - Conditional routing based on data
   - Multiple conditions support
   - Two outputs: true/false branches

6. **Merge** (`n8n-nodes-base.merge`)
   - Merge data from multiple inputs
   - Modes: append (list) or merge (dict)
   - Useful for combining parallel branches

## Execution Methods

Node types can use different execution methods:

1. **Python Function**: Execute Python code with access to Frappe
2. **JavaScript Code**: Execute JavaScript (placeholder for future implementation)
3. **HTTP Request**: Make HTTP calls to external services
4. **Frappe API**: Direct Frappe database operations
5. **Custom Module**: Load execution logic from a Python module

## Creating Custom Node Types

### Via Database

1. Create a new Workflow Node Type document
2. Define properties, inputs, and outputs
3. Select an execution method
4. Save and reload node types

### Via Fixture

Add to `fixtures/node_types.json`:

```json
{
  "doctype": "Workflow Node Type",
  "node_type_name": "custom.myNode",
  "display_name": "My Custom Node",
  "category": "Custom",
  "execute_method": "Python Function",
  "properties": [...]
}
```

### Via Python Module

1. Create a Python module with an `execute` function:

```python
# syncedoffice/so_workflow/nodes/my_custom_node.py
def execute(context):
    """Execute custom node logic"""
    input_data = context.get_input_data()
    param = context.get_parameter("my_param")
    
    # Your logic here
    result = process_data(input_data, param)
    
    context.log(f"Processed {len(result)} items")
    return result
```

2. Create node type with:
   - `execute_method`: "Custom Module"
   - `module_path`: "syncedoffice.so_workflow.nodes.my_custom_node"

## Node Execution Context

The `NodeExecutionContext` provides:

```python
# Get node parameters
value = context.get_parameter("param_name", default_value)

# Get input data
input_data = context.get_input_data(input_index=0)
all_inputs = context.get_all_input_data()

# Logging
context.log("Message", level="info")  # levels: info, warning, error

# Access workflow and node
context.workflow  # Workflow document
context.node      # Current node definition
context.parameters  # All node parameters
```

## Property Types

Supported property types in node definitions:

- `string`: Text input
- `number`: Numeric input
- `boolean`: Checkbox
- `options`: Dropdown selection
- `json`: JSON object/array
- `collection`: Nested properties
- `fixedCollection`: Fixed set of nested properties

## Usage Example

### Creating a Workflow with Typed Nodes

```python
import frappe

# Create workflow
workflow = frappe.get_doc({
    "doctype": "SO Workflow",
    "workflow_name": "API Data Processor",
    "nodes": [
        {
            "id": "node1",
            "name": "Fetch Data",
            "type": "n8n-nodes-base.httpRequest",
            "position": [100, 100],
            "parameters": {
                "method": "GET",
                "url": "https://api.example.com/data",
                "authentication": "bearer",
                "token": "your-token"
            }
        },
        {
            "id": "node2",
            "name": "Transform",
            "type": "n8n-nodes-base.set",
            "position": [300, 100],
            "parameters": {
                "keepOnlySet": False,
                "values": {
                    "processed": True,
                    "timestamp": "{{ $now }}"
                }
            }
        },
        {
            "id": "node3",
            "name": "Save to Frappe",
            "type": "frappe.api",
            "position": [500, 100],
            "parameters": {
                "operation": "insert",
                "doctype": "My DocType",
                "doc_data": {
                    "title": "{{ $json.title }}",
                    "data": "{{ $json }}"
                }
            }
        }
    ],
    "connections": {
        "node1": {
            "node2": [{"type": "main", "index": 0}]
        },
        "node2": {
            "node3": [{"type": "main", "index": 0}]
        }
    }
})
workflow.insert()

# Execute workflow
result = workflow.execute()
```

## API Methods

### Node Type Management

```python
# Get node type registry
from syncedoffice.so_workflow.node_type_registry import get_node_type_registry

registry = get_node_type_registry()

# Get node type definition
node_type = registry.get_node_type("n8n-nodes-base.httpRequest")

# Get all node types
all_types = registry.get_all_node_types()
filtered = registry.get_all_node_types(category="Core")

# Reload node types
registry.reload()
```

### Whitelisted API

```python
# Get node type (via API)
frappe.call("syncedoffice.so_workflow.doctype.workflow_node_type.workflow_node_type.get_node_type",
    {"name": "n8n-nodes-base.httpRequest"})

# Get node types list
frappe.call("syncedoffice.so_workflow.doctype.workflow_node_type.workflow_node_type.get_node_types_list",
    {"category": "Core"})

# Reload node types
frappe.call("syncedoffice.so_workflow.node_type_registry.reload_node_types")
```

## Migration from Legacy Nodes

Legacy node types (`trigger`, `transform`, `condition`, `action`) are still supported via the `_execute_legacy_node` method in the workflow engine. This ensures backward compatibility while allowing gradual migration to typed nodes.

## Best Practices

1. **Use Typed Nodes**: Always prefer typed nodes over legacy types
2. **Validate Parameters**: Define required parameters in node type definitions
3. **Error Handling**: Use try-catch in custom executors and log errors
4. **Logging**: Add informative log messages for debugging
5. **Versioning**: Increment version when making breaking changes to node types
6. **Documentation**: Document custom node types with clear descriptions
7. **Testing**: Test node types thoroughly before using in production workflows

## Future Enhancements

- [ ] JavaScript execution engine integration
- [ ] Visual node type editor
- [ ] Node type marketplace/sharing
- [ ] Advanced parameter validation (regex, ranges, etc.)
- [ ] Conditional property display
- [ ] Node type inheritance
- [ ] Webhook and trigger node support
- [ ] Credential management for node types
- [ ] Expression evaluation in parameters
- [ ] Batch processing support

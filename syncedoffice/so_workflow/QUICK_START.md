# Quick Start Guide - n8n-Inspired Node System

## Installation

The node types are already installed. To reinstall or update:

```bash
cd /home/jumes/bench
bench --site syncedoffice.localhost execute "syncedoffice.so_workflow.install_node_types.install_default_node_types"
```

## Available Node Types

| Node Type | Purpose | Category |
|-----------|---------|----------|
| `n8n-nodes-base.httpRequest` | Make HTTP requests | Core |
| `n8n-nodes-base.set` | Set/merge values | Core |
| `n8n-nodes-base.if` | Conditional routing | Condition |
| `n8n-nodes-base.merge` | Merge multiple inputs | Transform |
| `n8n-nodes-base.code` | Execute Python code | Core |
| `frappe.api` | Frappe database operations | Integration |

## Creating a Workflow

### Example 1: Simple Data Processing

```python
import frappe
import json

workflow = frappe.get_doc({
    "doctype": "SO Workflow",
    "workflow_name": "Data Processor",
    "nodes": json.dumps([
        {
            "id": "node1",
            "name": "Set Initial Data",
            "type": "n8n-nodes-base.set",
            "position": [100, 100],
            "parameters": {
                "keepOnlySet": False,
                "values": {
                    "name": "John Doe",
                    "email": "john@example.com",
                    "status": "active"
                }
            }
        }
    ]),
    "connections": json.dumps({}),
    "active": 1
})
workflow.insert()

# Execute
result = workflow.execute()
print(result)
```

### Example 2: API Integration

```python
workflow = frappe.get_doc({
    "doctype": "SO Workflow",
    "workflow_name": "API Integration",
    "nodes": json.dumps([
        {
            "id": "fetch",
            "name": "Fetch from API",
            "type": "n8n-nodes-base.httpRequest",
            "position": [100, 100],
            "parameters": {
                "method": "GET",
                "url": "https://jsonplaceholder.typicode.com/posts/1",
                "authentication": "none"
            }
        },
        {
            "id": "save",
            "name": "Save to Frappe",
            "type": "frappe.api",
            "position": [300, 100],
            "parameters": {
                "operation": "insert",
                "doctype": "Note",
                "doc_data": {
                    "title": "API Data",
                    "content": "Fetched from API"
                }
            }
        }
    ]),
    "connections": json.dumps({
        "fetch": {
            "save": [{"type": "main", "index": 0}]
        }
    })
})
workflow.insert()
result = workflow.execute()
```

### Example 3: Conditional Logic

```python
workflow = frappe.get_doc({
    "doctype": "SO Workflow",
    "workflow_name": "Conditional Workflow",
    "nodes": json.dumps([
        {
            "id": "check",
            "name": "Check Status",
            "type": "n8n-nodes-base.if",
            "position": [100, 100],
            "parameters": {
                "conditions": [
                    {
                        "field": "status",
                        "operation": "equals",
                        "value": "active"
                    }
                ]
            }
        }
    ]),
    "connections": json.dumps({})
})
workflow.insert()
result = workflow.execute(input_data={"status": "active"})
```

## Creating Custom Node Types

### Via Database

1. Go to: **Workflow Node Type** list
2. Click **New**
3. Fill in:
   - Node Type Name: `custom.myNode`
   - Display Name: `My Custom Node`
   - Category: `Custom`
   - Execute Method: `Python Function`
   - Properties: (JSON array of property definitions)
4. Save

### Via Python Module

```python
# syncedoffice/so_workflow/nodes/my_node.py
def execute(context):
    """Custom node executor"""
    input_data = context.get_input_data()
    param = context.get_parameter("my_param", "default")
    
    # Your logic
    result = {"processed": True, "data": input_data}
    
    context.log(f"Processed with param: {param}")
    return result
```

Then create node type with:
- Execute Method: `Custom Module`
- Module Path: `syncedoffice.so_workflow.nodes.my_node`

## Testing

Run the test suite:

```bash
bench --site syncedoffice.localhost execute "syncedoffice.so_workflow.test_node_types.run_all_tests"
```

## Common Operations

### Get Node Type Info

```python
from syncedoffice.so_workflow.node_type_registry import get_node_type_registry

registry = get_node_type_registry()
http_node = registry.get_node_type("n8n-nodes-base.httpRequest")
print(http_node)
```

### List All Node Types

```python
all_types = registry.get_all_node_types()
for nt in all_types:
    print(f"{nt['display_name']} - {nt['category']}")
```

### Reload Node Types

```python
registry.reload()
```

## Node Parameters

### HTTP Request Node

```python
"parameters": {
    "method": "GET|POST|PUT|DELETE|PATCH",
    "url": "https://api.example.com/endpoint",
    "authentication": "none|basic|bearer",
    "headers": {},
    "body": {}
}
```

### Set Node

```python
"parameters": {
    "keepOnlySet": False,  # True = replace all, False = merge
    "values": {
        "key1": "value1",
        "key2": "value2"
    }
}
```

### IF Node

```python
"parameters": {
    "conditions": [
        {
            "field": "status",
            "operation": "equals|notEquals|contains|exists",
            "value": "active"
        }
    ]
}
```

### Merge Node

```python
"parameters": {
    "mode": "append|merge"  # append = list, merge = dict
}
```

### Code Node

```python
"parameters": {
    "mode": "runOnceForAllItems|runOnceForEachItem",
    "code": """
# Access input_data
# Set output variable
output = {"result": "processed"}
"""
}
```

### Frappe API Node

```python
"parameters": {
    "operation": "get_doc|get_list|insert|update|delete",
    "doctype": "Customer",
    "doc_name": "CUST-001",  # for get_doc, update, delete
    "filters": {},  # for get_list
    "fields": ["name", "customer_name"],  # for get_list
    "doc_data": {},  # for insert, update
    "limit": 20  # for get_list
}
```

## Troubleshooting

### Node Type Not Found

```python
# Reload registry
from syncedoffice.so_workflow.node_type_registry import get_node_type_registry
registry = get_node_type_registry()
registry.reload()
```

### Execution Errors

Check the Workflow Execution document for detailed logs:

```python
execution = frappe.get_doc("Workflow Execution", "WE-XXX-00001")
print(execution.execution_log)
print(execution.error_message)
```

### Parameter Validation Errors

Ensure parameters match the node type definition:

```python
node_type = registry.get_node_type("n8n-nodes-base.httpRequest")
print(node_type['properties'])  # See required parameters
```

## Next Steps

1. **Build UI**: Create visual workflow editor
2. **Add Nodes**: Implement more node types (Email, Slack, etc.)
3. **Credentials**: Add credential management system
4. **Expressions**: Implement parameter expressions like `{{ $json.field }}`
5. **Webhooks**: Add webhook trigger support

## Resources

- Full Documentation: `NODE_TYPES.md`
- Implementation Details: `IMPLEMENTATION_SUMMARY.md`
- Test Suite: `test_node_types.py`
- Node Registry: `node_type_registry.py`
- Node Executors: `node_executors.py`

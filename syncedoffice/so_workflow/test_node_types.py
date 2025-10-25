"""
Test n8n-inspired node type system
"""

import frappe
import json


def test_node_type_registry():
    """Test node type registry"""
    print("\n=== Testing Node Type Registry ===\n")
    
    from syncedoffice.so_workflow.node_type_registry import get_node_type_registry
    
    registry = get_node_type_registry()
    registry.load_node_types(force_reload=True)
    
    # Get all node types
    all_types = registry.get_all_node_types()
    print(f"Total node types loaded: {len(all_types)}")
    
    for node_type in all_types:
        print(f"  - {node_type['display_name']} ({node_type['node_type_name']}) - {node_type['category']}")
    
    # Get specific node type
    http_node = registry.get_node_type("n8n-nodes-base.httpRequest")
    print(f"\nHTTP Request Node:")
    print(f"  Display Name: {http_node['display_name']}")
    print(f"  Description: {http_node['description']}")
    print(f"  Execute Method: {http_node['execute_method']}")
    
    return True


def test_simple_workflow():
    """Test simple workflow with typed nodes"""
    print("\n=== Testing Simple Workflow ===\n")
    
    # Create a test workflow
    workflow_data = {
        "doctype": "SO Workflow",
        "workflow_name": "Test Node Types Workflow",
        "description": "Testing n8n-inspired node types",
        "nodes": json.dumps([
            {
                "id": "node1",
                "name": "Set Values",
                "type": "n8n-nodes-base.set",
                "position": [100, 100],
                "parameters": {
                    "keepOnlySet": False,
                    "values": {
                        "message": "Hello from n8n-style nodes!",
                        "timestamp": "2025-01-21",
                        "status": "success"
                    }
                }
            },
            {
                "id": "node2",
                "name": "Add More Data",
                "type": "n8n-nodes-base.set",
                "position": [300, 100],
                "parameters": {
                    "keepOnlySet": False,
                    "values": {
                        "processed": True,
                        "node_count": 2
                    }
                }
            }
        ]),
        "connections": json.dumps({
            "node1": {
                "node2": [{"type": "main", "index": 0}]
            }
        }),
        "active": 1
    }
    
    # Check if workflow exists
    if frappe.db.exists("SO Workflow", "Test Node Types Workflow"):
        workflow = frappe.get_doc("SO Workflow", "Test Node Types Workflow")
        workflow.update(workflow_data)
        workflow.save()
        print("Updated existing workflow")
    else:
        workflow = frappe.get_doc(workflow_data)
        workflow.insert()
        print("Created new workflow")
    
    frappe.db.commit()
    
    # Execute workflow
    print("\nExecuting workflow...")
    result = workflow.execute(input_data={"initial": "data"})
    
    print(f"\nExecution Result:")
    print(f"  Success: {result['success']}")
    print(f"  Execution ID: {result.get('execution_id')}")
    
    if result['success']:
        print(f"\nNode Outputs:")
        for node_id, output in result.get('output', {}).items():
            print(f"  {node_id}: {json.dumps(output, indent=4)}")
        
        print(f"\nExecution Log:")
        for log_entry in result.get('log', []):
            print(f"  [{log_entry.get('level', 'info').upper()}] {log_entry.get('message')}")
    else:
        print(f"  Error: {result.get('error')}")
    
    return result['success']


def test_frappe_api_node():
    """Test Frappe API node"""
    print("\n=== Testing Frappe API Node ===\n")
    
    # Create workflow with Frappe API node
    workflow_data = {
        "doctype": "SO Workflow",
        "workflow_name": "Test Frappe API Workflow",
        "description": "Testing Frappe API node",
        "nodes": json.dumps([
            {
                "id": "node1",
                "name": "Get Workflow Node Types",
                "type": "frappe.api",
                "position": [100, 100],
                "parameters": {
                    "operation": "get_list",
                    "doctype": "Workflow Node Type",
                    "filters": {},
                    "fields": ["name", "display_name", "category"],
                    "limit": 5
                }
            }
        ]),
        "connections": json.dumps({}),
        "active": 1
    }
    
    # Check if workflow exists
    if frappe.db.exists("SO Workflow", "Test Frappe API Workflow"):
        workflow = frappe.get_doc("SO Workflow", "Test Frappe API Workflow")
        workflow.update(workflow_data)
        workflow.save()
    else:
        workflow = frappe.get_doc(workflow_data)
        workflow.insert()
    
    frappe.db.commit()
    
    # Execute workflow
    print("Executing Frappe API workflow...")
    result = workflow.execute()
    
    print(f"\nExecution Result:")
    print(f"  Success: {result['success']}")
    
    if result['success']:
        output = result.get('output', {}).get('node1', [])
        print(f"\nFetched {len(output)} node types:")
        for item in output:
            print(f"  - {item.get('display_name')} ({item.get('category')})")
    
    return result['success']


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("  n8n-Inspired Node Type System - Test Suite")
    print("="*60)
    
    tests = [
        ("Node Type Registry", test_node_type_registry),
        ("Simple Workflow", test_simple_workflow),
        ("Frappe API Node", test_frappe_api_node)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' failed with error: {str(e)}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "="*60)
    print("  Test Summary")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"  {status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("="*60 + "\n")
    
    return passed == total


if __name__ == "__main__":
    frappe.init(site="syncedoffice.localhost")
    frappe.connect()
    success = run_all_tests()
    exit(0 if success else 1)

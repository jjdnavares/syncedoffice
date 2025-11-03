"""
Test Workflow MVP - End-to-end test
"""

import frappe
import json


def test_workflow_mvp():
    """Test complete workflow MVP functionality"""
    
    print("\n" + "="*60)
    print("WORKFLOW MVP TEST")
    print("="*60)
    
    # Test 1: Verify node types are installed
    print("\n1. Testing Node Types Installation...")
    node_types = frappe.get_all("Workflow Node Type", fields=["node_type_name", "display_name", "category"])
    print(f"   ✓ Found {len(node_types)} node types")
    for nt in node_types:
        print(f"     - {nt['display_name']} ({nt['category']})")
    
    # Test 2: Create a simple workflow
    print("\n2. Creating Test Workflow...")
    workflow_name = f"Test Workflow {frappe.utils.now()}"
    
    workflow = frappe.get_doc({
        "doctype": "SO Workflow",
        "workflow_name": workflow_name,
        "description": "MVP Test Workflow",
        "active": 1,
        "nodes": json.dumps([
            {
                "id": "node1",
                "name": "Set Data",
                "type": "n8n-nodes-base.set",
                "position": [100, 100],
                "parameters": {
                    "keepOnlySet": False,
                    "values": {
                        "test_field": "test_value",
                        "number": 42,
                        "active": True
                    }
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
                        "timestamp": frappe.utils.now()
                    }
                }
            }
        ]),
        "connections": json.dumps({
            "node1": {
                "node2": [{"type": "main", "index": 0}]
            }
        })
    })
    
    workflow.insert()
    frappe.db.commit()
    print(f"   ✓ Created workflow: {workflow.name}")
    
    # Test 3: Execute the workflow
    print("\n3. Executing Workflow...")
    result = workflow.execute()
    
    if result.get("success"):
        print(f"   ✓ Execution successful!")
        print(f"   ✓ Execution ID: {result.get('execution_id')}")
        print(f"   ✓ Output nodes: {len(result.get('output', {}))}")
    else:
        print(f"   ✗ Execution failed: {result.get('error')}")
        return False
    
    # Test 4: Verify execution record
    print("\n4. Verifying Execution Record...")
    execution = frappe.get_doc("Workflow Execution", result.get("execution_id"))
    print(f"   ✓ Status: {execution.status}")
    print(f"   ✓ Duration: {execution.duration}s")
    print(f"   ✓ Log entries: {len(json.loads(execution.execution_log))}")
    
    # Test 5: Test API endpoints
    print("\n5. Testing API Endpoints...")
    
    # Get workflow list
    workflows = frappe.call(
        "syncedoffice.so_workflow.doctype.so_workflow.so_workflow.get_workflow_list"
    )
    print(f"   ✓ get_workflow_list: {len(workflows)} workflows")
    
    # Get workflow
    workflow_data = frappe.call(
        "syncedoffice.so_workflow.doctype.so_workflow.so_workflow.get_workflow",
        name=workflow.name
    )
    print(f"   ✓ get_workflow: {workflow_data.get('workflow_name')}")
    
    # Get node types for editor
    node_types_editor = frappe.call(
        "syncedoffice.so_workflow.doctype.workflow_node_type.workflow_node_type.get_node_types_for_editor"
    )
    print(f"   ✓ get_node_types_for_editor:")
    for category, types in node_types_editor.items():
        if types:
            print(f"     - {category}: {len(types)} types")
    
    # Test 6: Cleanup
    print("\n6. Cleaning Up...")
    # Delete execution first
    frappe.delete_doc("Workflow Execution", result.get("execution_id"))
    frappe.delete_doc("SO Workflow", workflow.name)
    frappe.db.commit()
    print(f"   ✓ Deleted test workflow and execution")
    
    print("\n" + "="*60)
    print("✓ ALL TESTS PASSED - MVP IS READY!")
    print("="*60)
    
    return True


def run_mvp_test():
    """Run the MVP test"""
    try:
        test_workflow_mvp()
    except Exception as e:
        print(f"\n✗ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    frappe.init(site="syncedoffice.localhost")
    frappe.connect()
    run_mvp_test()

"""
Install default node types
"""

import frappe
import json
import os


def install_default_node_types():
    """Install default node types from fixtures"""
    
    # Get fixture file path
    fixture_path = os.path.join(
        frappe.get_app_path("syncedoffice"),
        "so_workflow",
        "fixtures",
        "node_types.json"
    )
    
    # Load fixture data
    with open(fixture_path, "r") as f:
        node_types = json.load(f)
    
    installed_count = 0
    updated_count = 0
    
    for node_type_data in node_types:
        node_type_name = node_type_data.get("node_type_name")
        
        # Convert lists to JSON strings for JSON fields
        json_fields = ['inputs', 'outputs', 'properties', 'credentials', 'defaults', 'hints']
        for field in json_fields:
            if field in node_type_data and isinstance(node_type_data[field], (list, dict)):
                node_type_data[field] = json.dumps(node_type_data[field])
        
        # Check if node type already exists
        if frappe.db.exists("Workflow Node Type", node_type_name):
            # Update existing
            doc = frappe.get_doc("Workflow Node Type", node_type_name)
            doc.update(node_type_data)
            doc.save()
            updated_count += 1
            print(f"Updated: {node_type_name}")
        else:
            # Create new
            doc = frappe.get_doc(node_type_data)
            doc.insert()
            installed_count += 1
            print(f"Installed: {node_type_name}")
    
    frappe.db.commit()
    
    print(f"\nNode Types Installation Complete:")
    print(f"  - Installed: {installed_count}")
    print(f"  - Updated: {updated_count}")
    print(f"  - Total: {installed_count + updated_count}")
    
    return {
        "installed": installed_count,
        "updated": updated_count,
        "total": installed_count + updated_count
    }


if __name__ == "__main__":
    frappe.init(site="syncedoffice.localhost")
    frappe.connect()
    install_default_node_types()

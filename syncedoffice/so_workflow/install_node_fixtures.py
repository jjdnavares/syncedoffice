"""
Install node types from fixtures
"""

import frappe
import json
import os


def install_node_types():
    """Install node types from fixtures"""
    
    # Get fixture file paths
    fixtures_dir = os.path.join(
        frappe.get_app_path("syncedoffice"),
        "so_workflow",
        "fixtures"
    )
    
    fixture_files = [
        "style_nodes.json",
        "trigger_nodes.json"
    ]
    
    all_node_types = []
    
    # Load all fixture files
    for fixture_file in fixture_files:
        fixture_path = os.path.join(fixtures_dir, fixture_file)
        if os.path.exists(fixture_path):
            with open(fixture_path, "r") as f:
                node_types = json.load(f)
                all_node_types.extend(node_types)
                print(f"Loaded {len(node_types)} nodes from {fixture_file}")
    
    node_types = all_node_types
    
    installed_count = 0
    updated_count = 0
    
    for node_type_data in node_types:
        node_type_name = node_type_data.get("node_type_name")
        
        # Convert lists/dicts to JSON strings for JSON fields
        json_fields = ['version_array', 'codex', 'webhooks', 'inputs', 'outputs', 
                       'properties', 'credentials', 'defaults', 'hints', 
                       'display_options', 'type_options']
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


def migrate_old_node_types():
    """Migrate old node types to new format"""
    
    print("\nMigrating old node types...")
    
    # Get all existing node types
    old_nodes = frappe.get_all(
        "Workflow Node Type",
        filters={"codex": ["is", "not set"]},
        fields=["name", "node_type_name", "category"]
    )
    
    migrated_count = 0
    
    for old_node in old_nodes:
        doc = frappe.get_doc("Workflow Node Type", old_node.name)
        
        # Add default codex if missing
        if not doc.codex:
            doc.codex = json.dumps({
                "alias": [],
                "categories": [doc.category or "Custom"],
                "subcategories": {
                    doc.category or "Custom": ["General"]
                },
                "resources": {
                    "primaryDocumentation": []
                }
            })
        
        # Add default group if missing
        if not doc.group:
            doc.group = "transform"
        
        # Add defaults if missing
        if not doc.defaults:
            doc.defaults = json.dumps({
                "name": doc.display_name,
                "color": "#909298"
            })
        
        doc.save()
        migrated_count += 1
        print(f"Migrated: {doc.node_type_name}")
    
    frappe.db.commit()
    
    print(f"\nMigration Complete: {migrated_count} nodes updated")
    
    return {"migrated": migrated_count}


if __name__ == "__main__":
    frappe.init(site="syncedoffice.localhost")
    frappe.connect()
    install_node_types()
    migrate_old_node_types()

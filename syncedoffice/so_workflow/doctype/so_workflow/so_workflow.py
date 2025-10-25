import frappe
import json
import uuid
from frappe.model.document import Document
from frappe.utils import now, cint

class SOWorkflow(Document):
    def before_save(self):
        """Set audit fields and version before saving"""
        if self.is_new():
            self.created_by = frappe.session.user
            self.version = 1
            self.version_id = str(uuid.uuid4())
        else:
            # Increment version if workflow definition changed
            old_doc = self.get_doc_before_save()
            if old_doc and (
                old_doc.nodes != self.nodes or 
                old_doc.connections != self.connections
            ):
                self.version = cint(self.version) + 1
                self.version_id = str(uuid.uuid4())
        
        self.modified_by = frappe.session.user

    def validate(self):
        """Validate workflow definition"""
        # Ensure nodes is valid JSON
        try:
            if isinstance(self.nodes, str):
                nodes = json.loads(self.nodes)
            else:
                nodes = self.nodes or []
            
            # Ensure connections is valid JSON
            if isinstance(self.connections, str):
                connections = json.loads(self.connections)
            else:
                connections = self.connections or {}
            
            # Ensure settings is valid JSON
            if self.settings and isinstance(self.settings, str):
                json.loads(self.settings)
            
            # Ensure pinned_data is valid JSON
            if self.pinned_data and isinstance(self.pinned_data, str):
                json.loads(self.pinned_data)
                
        except (ValueError, json.JSONDecodeError) as e:
            frappe.throw(f"Invalid JSON data in workflow definition: {str(e)}")

    def execute(self, input_data=None, trigger_node=None):
        """Execute the workflow with the given input data"""
        from syncedoffice.so_workflow.workflow_engine import execute_workflow
        
        result = execute_workflow(self, input_data, trigger_node)
        
        # Update execution stats
        self.db_set('last_execution', now())
        self.db_set('execution_count', cint(self.execution_count) + 1)
        
        return result

@frappe.whitelist()
def get_workflow(name):
    """Get workflow by name"""
    if not frappe.has_permission("SO Workflow", "read"):
        frappe.throw("Not permitted", frappe.PermissionError)
    
    doc = frappe.get_doc("SO Workflow", name)
    return doc.as_dict()

@frappe.whitelist()
def save_workflow(workflow_data):
    """Save or update workflow"""
    try:
        if not frappe.has_permission("SO Workflow", "write"):
            frappe.throw("Not permitted", frappe.PermissionError)
        
        workflow_data = frappe.parse_json(workflow_data)
        
        # Ensure nodes and connections are initialized
        if "nodes" not in workflow_data:
            workflow_data["nodes"] = []
        if "connections" not in workflow_data:
            workflow_data["connections"] = {}
        
        # Convert to JSON strings if they're not already
        if isinstance(workflow_data.get("nodes"), (list, dict)):
            workflow_data["nodes"] = json.dumps(workflow_data["nodes"])
        if isinstance(workflow_data.get("connections"), (list, dict)):
            workflow_data["connections"] = json.dumps(workflow_data["connections"])
        if workflow_data.get("settings") and isinstance(workflow_data["settings"], dict):
            workflow_data["settings"] = json.dumps(workflow_data["settings"])
        if workflow_data.get("pinned_data") and isinstance(workflow_data["pinned_data"], dict):
            workflow_data["pinned_data"] = json.dumps(workflow_data["pinned_data"])
        
        if workflow_data.get("name"):
            doc = frappe.get_doc("SO Workflow", workflow_data["name"])
            doc.update(workflow_data)
        else:
            doc = frappe.get_doc({
                "doctype": "SO Workflow",
                **workflow_data
            })
        
        doc.save()
        frappe.db.commit()
        
        return doc.as_dict()
    except Exception as e:
        frappe.log_error(f"Error saving workflow: {str(e)}", "Workflow Save Error")
        raise

@frappe.whitelist()
def execute_workflow_api(name, input_data=None, trigger_node=None):
    """Execute workflow via API"""
    if not frappe.has_permission("SO Workflow", "read"):
        frappe.throw("Not permitted", frappe.PermissionError)
    
    doc = frappe.get_doc("SO Workflow", name)
    
    if not doc.active:
        frappe.throw("Workflow is not active")
    
    input_data = frappe.parse_json(input_data) if input_data else None
    
    return doc.execute(input_data, trigger_node)

@frappe.whitelist()
def get_workflow_list(filters=None):
    """Get list of workflows"""
    if not frappe.has_permission("SO Workflow", "read"):
        frappe.throw("Not permitted", frappe.PermissionError)
    
    filters = frappe.parse_json(filters) if filters else {}
    
    workflows = frappe.get_all(
        "SO Workflow",
        filters=filters,
        fields=["name", "workflow_name", "description", "active", "tags", 
                "modified", "creation", "execution_count", "last_execution"],
        order_by="modified desc"
    )
    
    return workflows

@frappe.whitelist()
def delete_workflow(name):
    """Delete a workflow"""
    if not frappe.has_permission("SO Workflow", "delete"):
        frappe.throw("Not permitted", frappe.PermissionError)
    
    try:
        frappe.delete_doc("SO Workflow", name)
        frappe.db.commit()
        return {"success": True, "message": "Workflow deleted successfully"}
    except Exception as e:
        frappe.log_error(f"Error deleting workflow: {str(e)}", "Workflow Delete Error")
        frappe.throw(f"Error deleting workflow: {str(e)}")

@frappe.whitelist()
def update_workflow_status(name, active):
    """Update workflow active status"""
    if not frappe.has_permission("SO Workflow", "write"):
        frappe.throw("Not permitted", frappe.PermissionError)
    
    try:
        doc = frappe.get_doc("SO Workflow", name)
        doc.active = cint(active)
        doc.save()
        frappe.db.commit()
        return doc.as_dict()
    except Exception as e:
        frappe.log_error(f"Error updating workflow status: {str(e)}", "Workflow Status Update Error")
        frappe.throw(f"Error updating workflow status: {str(e)}")

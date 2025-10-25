import frappe
from frappe.model.document import Document

class WorkflowNode(Document):
    pass

@frappe.whitelist()
def get_available_nodes():
    """Get all available workflow nodes"""
    if not frappe.has_permission("Workflow Node", "read"):
        frappe.throw("Not permitted", frappe.PermissionError)
    
    nodes = frappe.get_all(
        "Workflow Node",
        fields=["name", "node_name", "node_type", "description", "icon", 
                "color", "category", "parameters", "inputs", "outputs"],
        order_by="category, node_name"
    )
    
    return nodes

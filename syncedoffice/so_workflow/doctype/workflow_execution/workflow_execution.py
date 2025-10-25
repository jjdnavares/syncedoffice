import frappe
from frappe.model.document import Document

class WorkflowExecution(Document):
    pass

@frappe.whitelist()
def get_workflow_executions(workflow_name, limit=50):
    """Get execution history for a workflow"""
    if not frappe.has_permission("Workflow Execution", "read"):
        frappe.throw("Not permitted", frappe.PermissionError)
    
    executions = frappe.get_all(
        "Workflow Execution",
        filters={"workflow": workflow_name},
        fields=["name", "status", "started_at", "finished_at", "duration", "trigger_node"],
        order_by="started_at desc",
        limit=limit
    )
    
    return executions

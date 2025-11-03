import frappe
import json
from frappe.model.document import Document

class WorkflowNodeType(Document):
    def before_save(self):
        """Set audit fields before saving"""
        if self.is_new():
            self.created_by = frappe.session.user
        self.modified_by = frappe.session.user

    def validate(self):
        """Validate node type definition"""
        # Validate JSON fields
        json_fields = ['inputs', 'outputs', 'properties', 'credentials', 'defaults', 'hints']
        for field in json_fields:
            value = getattr(self, field, None)
            if value:
                try:
                    if isinstance(value, str):
                        json.loads(value)
                except (ValueError, json.JSONDecodeError) as e:
                    frappe.throw(f"Invalid JSON in {field}: {str(e)}")
        
        # Validate inputs configuration
        if self.inputs:
            inputs = self._parse_json(self.inputs)
            if inputs and not isinstance(inputs, list):
                frappe.throw("Inputs must be a list")
        
        # Validate outputs configuration
        if self.outputs:
            outputs = self._parse_json(self.outputs)
            if outputs and not isinstance(outputs, list):
                frappe.throw("Outputs must be a list")
        
        # Validate properties
        if self.properties:
            properties = self._parse_json(self.properties)
            if properties and not isinstance(properties, list):
                frappe.throw("Properties must be a list")

    def get_node_definition(self):
        """Get complete node definition for execution (n8n-compatible)"""
        return {
            "name": self.node_type_name,
            "displayName": self.display_name,
            "description": self.description,
            "category": self.category,
            "version": self.version,
            "versionArray": self._parse_json(self.version_array) or [self.version],
            "icon": self.icon,
            "iconColor": self.icon_color,
            "group": self.group,
            "subtitle": self.subtitle,
            "codex": self._parse_json(self.codex) or {},
            "webhooks": self._parse_json(self.webhooks) or [],
            "inputs": self._parse_json(self.inputs) or [],
            "outputs": self._parse_json(self.outputs) or [],
            "properties": self._parse_json(self.properties) or [],
            "credentials": self._parse_json(self.credentials) or [],
            "defaults": self._parse_json(self.defaults) or {},
            "hints": self._parse_json(self.hints) or [],
            "displayOptions": self._parse_json(self.display_options) or {},
            "typeOptions": self._parse_json(self.type_options) or {},
            "executeMethod": self.execute_method,
            "polling": self.polling,
            "trigger": self.trigger,
            "webhook": self.webhook,
            "maxNodes": self.max_nodes,
            "isCustom": self.is_custom,
            "modulePath": self.module_path
        }

    def _parse_json(self, data):
        """Parse JSON data"""
        if isinstance(data, str):
            try:
                return json.loads(data)
            except:
                return None
        return data


@frappe.whitelist()
def get_node_type(name):
    """Get node type by name"""
    if not frappe.has_permission("Workflow Node Type", "read"):
        frappe.throw("Not permitted", frappe.PermissionError)
    
    doc = frappe.get_doc("Workflow Node Type", name)
    return doc.get_node_definition()


@frappe.whitelist()
def get_node_types_list(category=None):
    """Get list of available node types"""
    if not frappe.has_permission("Workflow Node Type", "read"):
        frappe.throw("Not permitted", frappe.PermissionError)
    
    filters = {}
    if category:
        filters["category"] = category
    
    node_types = frappe.get_all(
        "Workflow Node Type",
        filters=filters,
        fields=["name", "node_type_name", "display_name", "description", 
                "category", "icon", "icon_color", "version", "group"],
        order_by="category, display_name"
    )
    
    return node_types


@frappe.whitelist()
def save_node_type(node_type_data):
    """Save or update node type"""
    if not frappe.has_permission("Workflow Node Type", "write"):
        frappe.throw("Not permitted", frappe.PermissionError)
    
    node_type_data = frappe.parse_json(node_type_data)
    
    # Convert lists/dicts to JSON strings
    json_fields = ['inputs', 'outputs', 'properties', 'credentials', 'defaults', 'hints']
    for field in json_fields:
        if field in node_type_data and isinstance(node_type_data[field], (list, dict)):
            node_type_data[field] = json.dumps(node_type_data[field])
    
    if node_type_data.get("name"):
        doc = frappe.get_doc("Workflow Node Type", node_type_data["name"])
        doc.update(node_type_data)
    else:
        doc = frappe.get_doc({
            "doctype": "Workflow Node Type",
            **node_type_data
        })
    
    doc.save()
    frappe.db.commit()
    
    return doc.get_node_definition()


@frappe.whitelist()
def get_node_types_for_editor():
    """Get node types formatted for the workflow editor frontend"""
    if not frappe.has_permission("Workflow Node Type", "read"):
        frappe.throw("Not permitted", frappe.PermissionError)
    
    node_types = frappe.get_all(
        "Workflow Node Type",
        fields=["name", "node_type_name", "display_name", "description", 
                "category", "icon", "icon_color", "version", "group", "trigger"],
        order_by="category, display_name"
    )
    
    # Organize by category
    organized = {
        "triggers": [],
        "actions": [],
        "core": [],
        "transform": [],
        "condition": [],
        "integration": [],
        "custom": []
    }
    
    for node_type in node_types:
        category = node_type.get("category", "Custom").lower()
        
        # Map to frontend structure
        frontend_node = {
            "type": node_type.get("node_type_name"),
            "label": node_type.get("display_name"),
            "description": node_type.get("description", ""),
            "icon": node_type.get("icon", "Code"),
            "color": node_type.get("icon_color", "text-gray-600"),
            "category": node_type.get("category"),
            "isTrigger": node_type.get("trigger", 0) == 1
        }
        
        # Add to appropriate category
        if node_type.get("trigger"):
            organized["triggers"].append(frontend_node)
        elif category in organized:
            organized[category].append(frontend_node)
        else:
            organized["custom"].append(frontend_node)
    
    return organized

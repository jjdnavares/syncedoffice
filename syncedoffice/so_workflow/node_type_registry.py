"""
Node Type Registry
Manages registration and loading of workflow node types
"""

import frappe
import json
from typing import Dict, List, Optional, Any
from importlib import import_module


class NodeTypeRegistry:
    """Registry for workflow node types"""
    
    def __init__(self):
        self._node_types: Dict[str, Dict] = {}
        self._loaded = False
    
    def load_node_types(self, force_reload=False):
        """Load all node types from database and modules"""
        if self._loaded and not force_reload:
            return
        
        self._node_types = {}
        
        # Load node types from database
        node_types = frappe.get_all(
            "Workflow Node Type",
            fields=["name", "node_type_name", "display_name", "category", 
                    "version", "version_array", "execute_method", "module_path", "is_custom",
                    "inputs", "outputs", "properties", "credentials", 
                    "defaults", "hints", "icon", "icon_color", "group",
                    "subtitle", "polling", "trigger", "webhook", "webhooks", "max_nodes",
                    "description", "codex", "display_options", "type_options"]
        )
        
        for node_type in node_types:
            self._register_node_type(node_type)
        
        self._loaded = True
    
    def _register_node_type(self, node_type_data: Dict):
        """Register a single node type"""
        node_type_name = node_type_data.get("node_type_name")
        
        # Parse JSON fields (including new n8n fields)
        json_fields = ['inputs', 'outputs', 'properties', 'credentials', 'defaults', 'hints',
                       'version_array', 'codex', 'webhooks', 'display_options', 'type_options']
        for field in json_fields:
            if node_type_data.get(field):
                try:
                    if isinstance(node_type_data[field], str):
                        node_type_data[field] = json.loads(node_type_data[field])
                except:
                    node_type_data[field] = None
        
        self._node_types[node_type_name] = node_type_data
    
    def get_node_type(self, node_type_name: str) -> Optional[Dict]:
        """Get node type definition by name"""
        if not self._loaded:
            self.load_node_types()
        
        return self._node_types.get(node_type_name)
    
    def get_all_node_types(self, category: Optional[str] = None) -> List[Dict]:
        """Get all node types, optionally filtered by category"""
        if not self._loaded:
            self.load_node_types()
        
        node_types = list(self._node_types.values())
        
        if category:
            node_types = [nt for nt in node_types if nt.get("category") == category]
        
        return node_types
    
    def get_node_executor(self, node_type_name: str):
        """Get executor function for a node type"""
        node_type = self.get_node_type(node_type_name)
        
        if not node_type:
            raise Exception(f"Node type not found: {node_type_name}")
        
        execute_method = node_type.get("execute_method")
        module_path = node_type.get("module_path")
        
        if execute_method == "Custom Module" and module_path:
            # Load custom module
            try:
                module = import_module(module_path)
                if hasattr(module, "execute"):
                    return module.execute
            except Exception as e:
                frappe.log_error(f"Failed to load custom module {module_path}: {str(e)}")
        
        # Return built-in executor
        return self._get_builtin_executor(execute_method)
    
    def _get_builtin_executor(self, execute_method: str):
        """Get built-in executor function"""
        from syncedoffice.so_workflow.node_executors import (
            execute_python_function,
            execute_javascript_code,
            execute_http_request,
            execute_frappe_api
        )
        
        executors = {
            "Python Function": execute_python_function,
            "JavaScript Code": execute_javascript_code,
            "HTTP Request": execute_http_request,
            "Frappe API": execute_frappe_api
        }
        
        return executors.get(execute_method)
    
    def validate_node_parameters(self, node_type_name: str, parameters: Dict) -> bool:
        """Validate node parameters against node type definition"""
        node_type = self.get_node_type(node_type_name)
        
        if not node_type:
            return False
        
        properties = node_type.get("properties", [])
        
        # Check required parameters
        for prop in properties:
            if prop.get("required") and prop.get("name") not in parameters:
                raise Exception(f"Required parameter missing: {prop.get('name')}")
        
        return True
    
    def get_node_inputs(self, node_type_name: str) -> List[Dict]:
        """Get input configuration for a node type"""
        node_type = self.get_node_type(node_type_name)
        return node_type.get("inputs", []) if node_type else []
    
    def get_node_outputs(self, node_type_name: str) -> List[Dict]:
        """Get output configuration for a node type"""
        node_type = self.get_node_type(node_type_name)
        return node_type.get("outputs", []) if node_type else []
    
    def reload(self):
        """Reload all node types"""
        self.load_node_types(force_reload=True)


# Global registry instance
_registry = None

def get_node_type_registry() -> NodeTypeRegistry:
    """Get global node type registry instance"""
    global _registry
    if _registry is None:
        _registry = NodeTypeRegistry()
    return _registry


@frappe.whitelist()
def reload_node_types():
    """Reload node types from database"""
    if not frappe.has_permission("Workflow Node Type", "read"):
        frappe.throw("Not permitted", frappe.PermissionError)
    
    registry = get_node_type_registry()
    registry.reload()
    
    return {"success": True, "message": "Node types reloaded"}

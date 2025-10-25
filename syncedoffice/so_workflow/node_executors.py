"""
Node Executors
Built-in execution methods for workflow nodes
"""

import frappe
import json
import requests
from typing import Dict, Any, List


class NodeExecutionContext:
    """Context for node execution"""
    
    def __init__(self, node, inputs, workflow, execution_log):
        self.node = node
        self.inputs = inputs
        self.workflow = workflow
        self.execution_log = execution_log
        self.parameters = node.get("parameters", {})
    
    def get_parameter(self, name: str, default=None):
        """Get node parameter value"""
        return self.parameters.get(name, default)
    
    def get_input_data(self, input_index: int = 0):
        """Get input data from connected nodes"""
        if not self.inputs:
            return []
        
        input_values = list(self.inputs.values())
        if input_index < len(input_values):
            return input_values[input_index]
        return []
    
    def get_all_input_data(self):
        """Get all input data"""
        return self.inputs
    
    def log(self, message: str, level: str = "info"):
        """Add log entry"""
        self.execution_log.append({
            "node": self.node.get("name"),
            "level": level,
            "message": message
        })


def execute_python_function(context: NodeExecutionContext) -> Any:
    """Execute Python function node"""
    code = context.get_parameter("code", "")
    
    if not code:
        return context.get_input_data()
    
    # Prepare execution context
    input_data = context.get_input_data()
    
    # Create safe execution environment
    exec_globals = {
        "frappe": frappe,
        "json": json,
        "input_data": input_data,
        "context": context
    }
    
    try:
        # Execute code
        exec(code, exec_globals)
        
        # Return result
        if "output" in exec_globals:
            return exec_globals["output"]
        else:
            return input_data
    except Exception as e:
        context.log(f"Python execution error: {str(e)}", "error")
        raise Exception(f"Python execution failed: {str(e)}")


def execute_javascript_code(context: NodeExecutionContext) -> Any:
    """Execute JavaScript code node"""
    code = context.get_parameter("code", "")
    
    if not code:
        return context.get_input_data()
    
    # For MVP, we'll just return input data
    # In production, you'd want to use a JS execution engine
    context.log("JavaScript execution not fully implemented, returning input data", "warning")
    return context.get_input_data()


def execute_http_request(context: NodeExecutionContext) -> Any:
    """Execute HTTP request node"""
    method = context.get_parameter("method", "GET")
    url = context.get_parameter("url", "")
    headers = context.get_parameter("headers", {})
    body = context.get_parameter("body", {})
    authentication = context.get_parameter("authentication", "none")
    
    if not url:
        raise Exception("URL is required for HTTP request")
    
    # Prepare request
    request_kwargs = {
        "method": method,
        "url": url,
        "headers": headers
    }
    
    # Add body for POST/PUT/PATCH
    if method in ["POST", "PUT", "PATCH"]:
        if isinstance(body, dict):
            request_kwargs["json"] = body
        else:
            request_kwargs["data"] = body
    
    # Add authentication
    if authentication == "basic":
        username = context.get_parameter("username", "")
        password = context.get_parameter("password", "")
        request_kwargs["auth"] = (username, password)
    elif authentication == "bearer":
        token = context.get_parameter("token", "")
        if token:
            request_kwargs["headers"]["Authorization"] = f"Bearer {token}"
    
    try:
        context.log(f"Making {method} request to {url}")
        response = requests.request(**request_kwargs)
        
        # Parse response
        result = {
            "statusCode": response.status_code,
            "headers": dict(response.headers),
            "body": None
        }
        
        # Try to parse JSON response
        try:
            result["body"] = response.json()
        except:
            result["body"] = response.text
        
        context.log(f"Request completed with status {response.status_code}")
        return result
    except Exception as e:
        context.log(f"HTTP request error: {str(e)}", "error")
        raise Exception(f"HTTP request failed: {str(e)}")


def execute_frappe_api(context: NodeExecutionContext) -> Any:
    """Execute Frappe API call node"""
    operation = context.get_parameter("operation", "get_doc")
    doctype = context.get_parameter("doctype", "")
    
    if not doctype:
        raise Exception("DocType is required for Frappe API call")
    
    try:
        if operation == "get_doc":
            doc_name = context.get_parameter("doc_name", "")
            if not doc_name:
                raise Exception("Document name is required for get_doc operation")
            
            doc = frappe.get_doc(doctype, doc_name)
            return doc.as_dict()
        
        elif operation == "get_list":
            filters = context.get_parameter("filters", {})
            fields = context.get_parameter("fields", [])
            limit = context.get_parameter("limit", 20)
            
            docs = frappe.get_all(
                doctype,
                filters=filters,
                fields=fields if fields else ["name"],
                limit=limit
            )
            return docs
        
        elif operation == "insert":
            doc_data = context.get_parameter("doc_data", {})
            if not doc_data:
                raise Exception("Document data is required for insert operation")
            
            doc = frappe.get_doc({
                "doctype": doctype,
                **doc_data
            })
            doc.insert()
            frappe.db.commit()
            return doc.as_dict()
        
        elif operation == "update":
            doc_name = context.get_parameter("doc_name", "")
            doc_data = context.get_parameter("doc_data", {})
            
            if not doc_name:
                raise Exception("Document name is required for update operation")
            
            doc = frappe.get_doc(doctype, doc_name)
            doc.update(doc_data)
            doc.save()
            frappe.db.commit()
            return doc.as_dict()
        
        elif operation == "delete":
            doc_name = context.get_parameter("doc_name", "")
            if not doc_name:
                raise Exception("Document name is required for delete operation")
            
            frappe.delete_doc(doctype, doc_name)
            frappe.db.commit()
            return {"success": True, "deleted": doc_name}
        
        else:
            raise Exception(f"Unknown operation: {operation}")
    
    except Exception as e:
        context.log(f"Frappe API error: {str(e)}", "error")
        raise Exception(f"Frappe API call failed: {str(e)}")


def execute_set_node(context: NodeExecutionContext) -> Any:
    """Execute Set node - sets values"""
    values = context.get_parameter("values", {})
    keep_only_set = context.get_parameter("keepOnlySet", False)
    
    input_data = context.get_input_data()
    
    if keep_only_set:
        return values
    else:
        # Merge with input data
        if isinstance(input_data, dict):
            result = {**input_data, **values}
        else:
            result = values
        return result


def execute_if_node(context: NodeExecutionContext) -> Any:
    """Execute IF node - conditional routing"""
    conditions = context.get_parameter("conditions", [])
    input_data = context.get_input_data()
    
    # Evaluate conditions
    for condition in conditions:
        field = condition.get("field", "")
        operation = condition.get("operation", "equals")
        value = condition.get("value", "")
        
        # Get field value from input data
        if isinstance(input_data, dict):
            field_value = input_data.get(field)
        else:
            field_value = None
        
        # Evaluate condition
        result = False
        if operation == "equals":
            result = field_value == value
        elif operation == "notEquals":
            result = field_value != value
        elif operation == "contains":
            result = value in str(field_value)
        elif operation == "exists":
            result = field_value is not None
        
        if not result:
            return {
                "condition_met": False,
                "data": input_data
            }
    
    return {
        "condition_met": True,
        "data": input_data
    }


def execute_merge_node(context: NodeExecutionContext) -> Any:
    """Execute Merge node - merges multiple inputs"""
    mode = context.get_parameter("mode", "append")
    all_inputs = context.get_all_input_data()
    
    if mode == "append":
        # Append all inputs into a list
        result = []
        for input_data in all_inputs.values():
            if isinstance(input_data, list):
                result.extend(input_data)
            else:
                result.append(input_data)
        return result
    
    elif mode == "merge":
        # Merge all inputs into a single dict
        result = {}
        for input_data in all_inputs.values():
            if isinstance(input_data, dict):
                result.update(input_data)
        return result
    
    else:
        return list(all_inputs.values())

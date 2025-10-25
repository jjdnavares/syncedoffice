"""
Workflow Execution Engine
Executes workflows defined with nodes and connections
"""

import frappe
import json
from datetime import datetime
from frappe.utils import now, get_datetime, time_diff_in_seconds
from syncedoffice.so_workflow.node_type_registry import get_node_type_registry
from syncedoffice.so_workflow.node_executors import (
    NodeExecutionContext,
    execute_set_node,
    execute_if_node,
    execute_merge_node
)

class WorkflowExecutionEngine:
    def __init__(self, workflow_doc, input_data=None, trigger_node=None):
        self.workflow = workflow_doc
        self.input_data = input_data or {}
        self.trigger_node = trigger_node
        self.execution_log = []
        self.node_outputs = {}
        
    def execute(self):
        """Execute the workflow"""
        execution_doc = self._create_execution_record()
        
        try:
            # Parse workflow definition
            nodes = self._parse_json(self.workflow.nodes) or []
            connections = self._parse_json(self.workflow.connections) or {}
            
            if not nodes:
                raise Exception("No nodes defined in workflow")
            
            # Build execution order
            execution_order = self._build_execution_order(nodes, connections)
            
            # Execute nodes in order
            for node_id in execution_order:
                node = next((n for n in nodes if n.get('id') == node_id), None)
                if not node:
                    continue
                    
                self._log(f"Executing node: {node.get('name', node_id)}")
                
                # Get node inputs from connected nodes
                node_inputs = self._get_node_inputs(node_id, connections)
                
                # Execute node
                output = self._execute_node(node, node_inputs)
                
                # Store output
                self.node_outputs[node_id] = output
                
                self._log(f"Node {node.get('name', node_id)} completed")
            
            # Mark execution as successful
            self._complete_execution(execution_doc, "Success")
            
            return {
                "success": True,
                "execution_id": execution_doc.name,
                "output": self.node_outputs,
                "log": self.execution_log
            }
            
        except Exception as e:
            self._log(f"Error: {str(e)}", level="error")
            self._complete_execution(execution_doc, "Failed", error=str(e))
            
            return {
                "success": False,
                "execution_id": execution_doc.name,
                "error": str(e),
                "log": self.execution_log
            }
    
    def _create_execution_record(self):
        """Create execution tracking record"""
        doc = frappe.get_doc({
            "doctype": "Workflow Execution",
            "workflow": self.workflow.name,
            "workflow_version": self.workflow.version,
            "status": "Running",
            "trigger_node": self.trigger_node,
            "started_at": now(),
            "input_data": json.dumps(self.input_data)
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        return doc
    
    def _complete_execution(self, execution_doc, status, error=None):
        """Complete execution record"""
        finished_at = now()
        duration = time_diff_in_seconds(get_datetime(finished_at), 
                                       get_datetime(execution_doc.started_at))
        
        execution_doc.db_set({
            "status": status,
            "finished_at": finished_at,
            "duration": duration,
            "output_data": json.dumps(self.node_outputs),
            "error_message": error,
            "execution_log": json.dumps(self.execution_log)
        })
        frappe.db.commit()
    
    def _build_execution_order(self, nodes, connections):
        """Build topological order for node execution"""
        # Simple approach: execute in order, respecting dependencies
        # For MVP, we'll use a basic topological sort
        
        node_ids = [n.get('id') for n in nodes]
        dependencies = {}
        
        # Build dependency graph
        for node_id in node_ids:
            dependencies[node_id] = []
            
        for source_id, targets in connections.items():
            if not isinstance(targets, dict):
                continue
            for target_id, connections_list in targets.items():
                if target_id in dependencies:
                    dependencies[target_id].append(source_id)
        
        # Topological sort
        visited = set()
        order = []
        
        def visit(node_id):
            if node_id in visited:
                return
            visited.add(node_id)
            for dep in dependencies.get(node_id, []):
                visit(dep)
            order.append(node_id)
        
        for node_id in node_ids:
            visit(node_id)
        
        return order
    
    def _get_node_inputs(self, node_id, connections):
        """Get inputs for a node from connected nodes"""
        inputs = {}
        
        # Find all connections to this node
        for source_id, targets in connections.items():
            if not isinstance(targets, dict):
                continue
            if node_id in targets:
                # Get output from source node
                if source_id in self.node_outputs:
                    inputs[source_id] = self.node_outputs[source_id]
        
        return inputs
    
    def _execute_node(self, node, inputs):
        """Execute a single node using node type registry"""
        node_type = node.get('type', 'custom')
        
        # Create execution context
        context = NodeExecutionContext(node, inputs, self.workflow, self.execution_log)
        
        # Check for built-in node types first
        if node_type == 'n8n-nodes-base.set':
            return execute_set_node(context)
        elif node_type == 'n8n-nodes-base.if':
            return execute_if_node(context)
        elif node_type == 'n8n-nodes-base.merge':
            return execute_merge_node(context)
        elif node_type == 'trigger':
            return self.input_data
        
        # Try to get node type from registry
        try:
            registry = get_node_type_registry()
            node_type_def = registry.get_node_type(node_type)
            
            if node_type_def:
                # Validate parameters
                parameters = node.get('parameters', {})
                registry.validate_node_parameters(node_type, parameters)
                
                # Get executor
                executor = registry.get_node_executor(node_type)
                
                if executor:
                    return executor(context)
                else:
                    self._log(f"No executor found for node type: {node_type}", "warning")
                    return inputs
            else:
                # Fallback to legacy execution
                return self._execute_legacy_node(node, inputs)
        except Exception as e:
            self._log(f"Error executing node: {str(e)}", "error")
            raise
    
    def _execute_legacy_node(self, node, inputs):
        """Execute legacy node types for backward compatibility"""
        node_type = node.get('type', 'custom')
        parameters = node.get('parameters', {})
        
        if node_type == 'transform':
            operation = parameters.get('operation', 'passthrough')
            if operation == 'passthrough':
                return inputs
            elif operation == 'merge':
                result = {}
                for input_data in inputs.values():
                    if isinstance(input_data, dict):
                        result.update(input_data)
                return result
            return inputs
        
        elif node_type == 'condition':
            return {
                "condition_met": True,
                "data": inputs
            }
        
        elif node_type == 'action':
            action_type = parameters.get('action_type', 'log')
            if action_type == 'log':
                message = parameters.get('message', 'Action executed')
                self._log(f"Action: {message}")
                return {"logged": True, "message": message}
            return inputs
        
        else:
            self._log(f"Unknown legacy node type: {node_type}", "warning")
            return inputs
    
    def _parse_json(self, data):
        """Parse JSON data"""
        if isinstance(data, str):
            try:
                return json.loads(data)
            except:
                return None
        return data
    
    def _log(self, message, level="info"):
        """Add log entry"""
        self.execution_log.append({
            "timestamp": now(),
            "level": level,
            "message": message
        })


def execute_workflow(workflow_doc, input_data=None, trigger_node=None):
    """Execute a workflow"""
    engine = WorkflowExecutionEngine(workflow_doc, input_data, trigger_node)
    return engine.execute()

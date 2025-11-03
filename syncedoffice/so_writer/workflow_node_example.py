# Copyright (c) 2024, jumes.dev and contributors
# For license information, please see license.txt

"""
Example workflow node implementation for content generation.

This file demonstrates how to create a custom workflow node that uses
the SO Writer module to generate content as part of a workflow.
"""

import frappe
from syncedoffice.so_writer.workflow_hook import (
    generate_content_for_workflow,
    quick_generate,
    get_available_providers,
    get_content_types
)


class ContentGeneratorNode:
    """
    Example workflow node for generating content.
    
    This node can be used in workflows to automatically generate content
    based on input parameters.
    """
    
    def __init__(self):
        self.node_type = "content_generator"
        self.label = "Content Generator"
        self.description = "Generate content using LLM providers"
        
    def get_config(self):
        """
        Return the configuration schema for this node.
        This defines what inputs the node accepts.
        """
        return {
            "inputs": [
                {
                    "name": "keyword",
                    "label": "Keyword",
                    "type": "text",
                    "required": True,
                    "description": "The main keyword or topic for content generation"
                },
                {
                    "name": "content_type",
                    "label": "Content Type",
                    "type": "select",
                    "options": get_content_types(),
                    "default": "Blog Post",
                    "required": True
                },
                {
                    "name": "tone",
                    "label": "Tone",
                    "type": "select",
                    "options": ["professional", "casual", "friendly", "authoritative", "witty"],
                    "default": "professional",
                    "required": True
                },
                {
                    "name": "provider",
                    "label": "LLM Provider",
                    "type": "select",
                    "options": get_available_providers(),
                    "default": "openai",
                    "required": True
                },
                {
                    "name": "model",
                    "label": "Model",
                    "type": "text",
                    "default": "gpt-4",
                    "required": True,
                    "description": "The specific model to use (e.g., gpt-4, claude-3-opus)"
                },
                {
                    "name": "save_to_db",
                    "label": "Save to Database",
                    "type": "checkbox",
                    "default": False,
                    "description": "Save the generated content to the database"
                }
            ],
            "outputs": [
                {
                    "name": "generated_text",
                    "label": "Generated Content",
                    "type": "text"
                },
                {
                    "name": "prompt",
                    "label": "Prompt Used",
                    "type": "text"
                },
                {
                    "name": "doc_name",
                    "label": "Document Name",
                    "type": "text",
                    "description": "Name of the saved document (if save_to_db is enabled)"
                }
            ]
        }
    
    def execute(self, inputs):
        """
        Execute the node with the given inputs.
        
        Args:
            inputs (dict): Dictionary containing the input values
            
        Returns:
            dict: Dictionary containing the output values
        """
        try:
            # Extract inputs
            keyword = inputs.get("keyword")
            content_type = inputs.get("content_type", "Blog Post")
            tone = inputs.get("tone", "professional")
            provider = inputs.get("provider", "openai")
            model = inputs.get("model", "gpt-4")
            save_to_db = inputs.get("save_to_db", False)
            
            # Validate required inputs
            if not keyword:
                frappe.throw("Keyword is required for content generation")
            
            # Generate content
            result = generate_content_for_workflow(
                keyword=keyword,
                content_type=content_type,
                tone=tone,
                provider=provider,
                model=model,
                save_to_db=save_to_db
            )
            
            # Prepare outputs
            outputs = {
                "generated_text": result.get("generated_text"),
                "prompt": result.get("prompt"),
                "doc_name": result.get("name", "")
            }
            
            return {
                "success": True,
                "outputs": outputs
            }
            
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "Content Generator Node Error")
            return {
                "success": False,
                "error": str(e)
            }


class QuickContentNode:
    """
    Simpler workflow node for quick content generation with custom prompts.
    """
    
    def __init__(self):
        self.node_type = "quick_content_generator"
        self.label = "Quick Content Generator"
        self.description = "Generate content with a custom prompt"
        
    def get_config(self):
        """Return the configuration schema for this node."""
        return {
            "inputs": [
                {
                    "name": "prompt",
                    "label": "Prompt",
                    "type": "textarea",
                    "required": True,
                    "description": "The prompt to send to the LLM"
                },
                {
                    "name": "provider",
                    "label": "LLM Provider",
                    "type": "select",
                    "options": get_available_providers(),
                    "default": "openai",
                    "required": True
                },
                {
                    "name": "model",
                    "label": "Model",
                    "type": "text",
                    "default": "gpt-4",
                    "required": True
                }
            ],
            "outputs": [
                {
                    "name": "generated_text",
                    "label": "Generated Content",
                    "type": "text"
                }
            ]
        }
    
    def execute(self, inputs):
        """Execute the node with the given inputs."""
        try:
            prompt = inputs.get("prompt")
            provider = inputs.get("provider", "openai")
            model = inputs.get("model", "gpt-4")
            
            if not prompt:
                frappe.throw("Prompt is required")
            
            result = quick_generate(
                prompt=prompt,
                provider=provider,
                model=model
            )
            
            return {
                "success": True,
                "outputs": {
                    "generated_text": result.get("generated_text")
                }
            }
            
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "Quick Content Node Error")
            return {
                "success": False,
                "error": str(e)
            }


# Register the nodes (this would typically be done in a fixtures file or setup script)
def register_writer_nodes():
    """
    Register the writer workflow nodes.
    This function should be called during app installation or setup.
    """
    nodes = [
        {
            "doctype": "Workflow Node Type",
            "name": "content_generator",
            "title": "Content Generator",
            "description": "Generate content using LLM providers",
            "category": "Content",
            "handler": "syncedoffice.so_writer.workflow_node_example.ContentGeneratorNode",
            "is_custom": 1
        },
        {
            "doctype": "Workflow Node Type",
            "name": "quick_content_generator",
            "title": "Quick Content Generator",
            "description": "Generate content with a custom prompt",
            "category": "Content",
            "handler": "syncedoffice.so_writer.workflow_node_example.QuickContentNode",
            "is_custom": 1
        }
    ]
    
    for node_data in nodes:
        if not frappe.db.exists("Workflow Node Type", node_data["name"]):
            doc = frappe.get_doc(node_data)
            doc.insert()
            frappe.db.commit()

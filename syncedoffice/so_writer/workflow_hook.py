# Copyright (c) 2024, jumes.dev and contributors
# For license information, please see license.txt

import frappe
from .api import _call_llm, get_llm_api_key
from .prompts import CONTENT_PROMPTS, HUMANIZE_PROMPT


def generate_content_for_workflow(keyword: str, content_type: str, tone: str, provider: str, model: str, save_to_db: bool = False):
    """
    Generate content for workflow custom node.
    
    This function is designed to be called from workflow nodes to generate content
    without necessarily saving it to the database.
    
    Args:
        keyword (str): The main keyword for content generation
        content_type (str): Type of content to generate (Blog Post, Article, etc.)
        tone (str): The tone for the content (professional, casual, etc.)
        provider (str): LLM provider to use (openai, anthropic, etc.)
        model (str): The specific model to use
        save_to_db (bool): Whether to save the generated content to database (default: False)
        
    Returns:
        dict: Dictionary containing:
            - generated_text: The final generated content
            - prompt: The initial prompt used
            - keyword: The keyword used
            - tone: The tone used
            - content_type: The content type
            - provider: The provider used
            - model: The model used
            - name: DocType name if saved to DB (only if save_to_db=True)
    """
    # Normalize content type
    content_type_map = {
        'blog-post': 'Blog Post',
        'article': 'Article',
        'product-description': 'Product Description',
        'landing-page': 'Landing Page',
        'seo-meta-description': 'SEO Meta Description',
        'social-media-post': 'Social Media Post',
        'blog-outline': 'Blog Outline',
    }
    
    normalized_content_type = content_type_map.get(content_type, content_type)
    
    # Get the prompt template
    prompt_info = CONTENT_PROMPTS.get(normalized_content_type)
    if not prompt_info:
        frappe.throw(f"Invalid content type: {content_type}")
    
    # Create the initial prompt
    initial_prompt = prompt_info['template'].format(keyword=keyword, tone=tone)
    
    # Generate raw content
    raw_content = _call_llm(initial_prompt, provider, model)
    
    # Create humanizing prompt
    humanize_prompt = f"{HUMANIZE_PROMPT}\n\nContent to humanize:\n{raw_content}"
    
    # Generate final humanized content
    final_content = _call_llm(humanize_prompt, provider, model)
    
    result = {
        "generated_text": final_content,
        "prompt": initial_prompt,
        "keyword": keyword,
        "tone": tone,
        "content_type": content_type,
        "provider": provider,
        "model": model
    }
    
    # Optionally save to database
    if save_to_db:
        doc = frappe.new_doc("Generated Content")
        doc.title = f"{content_type} for {keyword}"
        doc.generated_text = final_content
        doc.prompt = initial_prompt
        doc.keyword = keyword
        doc.tone = tone
        doc.content_type = content_type
        doc.provider = provider
        doc.model = model
        doc.user = frappe.session.user
        doc.insert()
        result["name"] = doc.name
    
    return result


def quick_generate(prompt: str, provider: str, model: str):
    """
    Quick content generation for workflow nodes with a custom prompt.
    
    This is a simpler function for workflow nodes that just need to generate
    content from a custom prompt without the full content generation pipeline.
    
    Args:
        prompt (str): The prompt to send to the LLM
        provider (str): LLM provider to use
        model (str): The specific model to use
        
    Returns:
        dict: Dictionary containing:
            - generated_text: The generated content
            - prompt: The prompt used
            - provider: The provider used
            - model: The model used
    """
    generated_text = _call_llm(prompt, provider, model)
    
    return {
        "generated_text": generated_text,
        "prompt": prompt,
        "provider": provider,
        "model": model
    }


def get_available_providers():
    """
    Get list of available LLM providers for workflow configuration.
    
    Returns:
        list: List of provider names
    """
    return [
        "openai",
        "anthropic",
        "google",
        "cohere",
        "groq",
        "mistral",
        "ollama",
        "perplexity",
        "together",
        "amazon-bedrock",
        "open-router"
    ]


def get_content_types():
    """
    Get list of available content types for workflow configuration.
    
    Returns:
        list: List of content type names
    """
    return list(CONTENT_PROMPTS.keys())

"""
Prompt service for managing prompt templates.
"""
import json
import os
from typing import Dict, Any, List
from backend.services.storage_service import StorageService


class PromptService:
    """Handles prompt template operations."""
    
    def __init__(self, storage_service: StorageService):
        """
        Initialize prompt service.
        
        Args:
            storage_service: Storage service instance for database operations
        """
        self.storage = storage_service
    
    def load_default_prompts(self, prompts_path: str = 'data/prompt_templates.json'):
        """
        Load default prompt templates from JSON file.
        
        Args:
            prompts_path: Path to the prompt templates JSON file
        """
        try:
            if not os.path.exists(prompts_path):
                raise FileNotFoundError(f"Prompt templates file not found: {prompts_path}")
            
            with open(prompts_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            prompts = data.get('prompts', {})
            
            for prompt_type, prompt_data in prompts.items():
                self.storage.add_prompt(
                    name=prompt_data['name'],
                    description=prompt_data['description'],
                    template=prompt_data['template'],
                    prompt_type=prompt_type,
                    version=prompt_data.get('version', '1.0'),
                    active=prompt_data.get('active', True)
                )
            
            print(f"Loaded {len(prompts)} default prompts")
        
        except Exception as e:
            print(f"Failed to load default prompts: {str(e)}")
    
    def get_prompt_template(self, prompt_type: str) -> str:
        """
        Get the template string for a specific prompt type.
        
        Args:
            prompt_type: Type of prompt (categorization, action_extraction, auto_reply, etc.)
            
        Returns:
            Prompt template string
        """
        prompt = self.storage.get_prompt_by_type(prompt_type)
        if prompt:
            return prompt.template
        raise ValueError(f"No active prompt found for type: {prompt_type}")
    
    def update_prompt(self, prompt_type: str, new_template: str):
        """
        Update a prompt template.
        
        Args:
            prompt_type: Type of prompt to update
            new_template: New template content
        """
        self.storage.update_prompt_template(prompt_type, new_template)
    
    def get_all_prompts_dict(self) -> Dict[str, Any]:
        """
        Get all prompts as a dictionary for UI display.
        
        Returns:
            Dictionary of prompts keyed by type
        """
        prompts = self.storage.get_all_prompts()
        result = {}
        
        for prompt in prompts:
            result[prompt.prompt_type] = {
                'id': prompt.id,
                'name': prompt.name,
                'description': prompt.description,
                'template': prompt.template,
                'version': prompt.version,
                'active': prompt.active,
                'updated_at': prompt.updated_at.isoformat() if prompt.updated_at else None
            }
        
        return result
    
    def ensure_default_prompts_loaded(self):
        """
        Check if prompts exist in database, if not load defaults.
        """
        prompts = self.storage.get_all_prompts()
        if len(prompts) == 0:
            print("No prompts found in database, loading defaults...")
            self.load_default_prompts()

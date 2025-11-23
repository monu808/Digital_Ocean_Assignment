"""
LLM Service for interacting with various LLM providers.
"""
import os
import json
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()


class LLMService:
    """Handles interactions with LLM providers (OpenAI, Anthropic, Ollama)."""
    
    def __init__(self, provider: str = None):
        """
        Initialize LLM service.
        
        Args:
            provider: LLM provider to use (openai, anthropic, ollama)
        """
        self.provider = provider or os.getenv('LLM_PROVIDER', 'openai')
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the appropriate LLM client based on provider."""
        try:
            if self.provider == 'openai':
                import openai
                self.api_key = os.getenv('OPENAI_API_KEY')
                if not self.api_key:
                    raise ValueError("OPENAI_API_KEY not found in environment variables")
                self.client = openai.OpenAI(api_key=self.api_key)
                self.model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
            
            elif self.provider == 'anthropic':
                import anthropic
                self.api_key = os.getenv('ANTHROPIC_API_KEY')
                if not self.api_key:
                    raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
                self.client = anthropic.Anthropic(api_key=self.api_key)
                self.model = os.getenv('ANTHROPIC_MODEL', 'claude-3-5-sonnet-20241022')
            
            elif self.provider == 'gemini':
                import google.generativeai as genai
                self.api_key = os.getenv('GEMINI_API_KEY')
                if not self.api_key:
                    raise ValueError("GEMINI_API_KEY not found in environment variables")
                genai.configure(api_key=self.api_key)
                self.model = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
                
                # Configure safety settings to be less restrictive for email processing
                from google.generativeai.types import HarmCategory, HarmBlockThreshold
                safety_settings = {
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                }
                
                self.client = genai.GenerativeModel(
                    self.model,
                    safety_settings=safety_settings
                )
            
            elif self.provider == 'ollama':
                import requests
                self.base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
                self.model = os.getenv('OLLAMA_MODEL', 'llama3')
                # Test connection
                try:
                    response = requests.get(f"{self.base_url}/api/tags")
                    if response.status_code != 200:
                        raise ValueError("Cannot connect to Ollama server")
                except Exception as e:
                    raise ValueError(f"Ollama connection failed: {str(e)}")
            
            else:
                raise ValueError(f"Unsupported LLM provider: {self.provider}")
        
        except ImportError as e:
            raise ImportError(f"Required library for {self.provider} not installed: {str(e)}")
    
    def generate_completion(self, prompt: str, temperature: float = 0.7, 
                          max_tokens: int = 1000) -> str:
        """
        Generate a completion from the LLM.
        
        Args:
            prompt: The prompt to send to the LLM
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
            
        Returns:
            The generated text response
        """
        try:
            if self.provider == 'openai':
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a helpful email assistant that processes emails and helps users manage their inbox efficiently."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                return response.choices[0].message.content.strip()
            
            elif self.provider == 'anthropic':
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                return response.content[0].text.strip()
            
            elif self.provider == 'gemini':
                # For JSON responses, add response_mime_type to force JSON
                generation_config = {
                    'temperature': temperature,
                    'max_output_tokens': max_tokens,
                }
                
                response = self.client.generate_content(
                    prompt,
                    generation_config=generation_config
                )
                
                # Check if response was blocked or has no text
                if not response.parts:
                    # Check finish reason
                    finish_reason = response.candidates[0].finish_reason if response.candidates else None
                    if finish_reason == 2:  # SAFETY
                        return "⚠️ Response blocked by safety filters. Try adjusting the prompt or use less sensitive test data."
                    elif finish_reason == 3:  # RECITATION
                        return "⚠️ Response blocked due to recitation concerns. Try rephrasing the prompt."
                    else:
                        return "⚠️ No response generated. The model may have encountered an issue."
                
                return response.text.strip()
            
            elif self.provider == 'ollama':
                import requests
                response = requests.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "temperature": temperature,
                        "stream": False
                    }
                )
                response.raise_for_status()
                return response.json()['response'].strip()
            
        except Exception as e:
            raise Exception(f"LLM generation failed: {str(e)}")
    
    def generate_json_completion(self, prompt: str, temperature: float = 0.3) -> Dict[str, Any]:
        """
        Generate a JSON response from the LLM.
        
        Args:
            prompt: The prompt to send to the LLM
            temperature: Sampling temperature (lower for more deterministic JSON)
            
        Returns:
            Parsed JSON response as dictionary
        """
        original_response = ""
        
        try:
            # For Gemini, use a special JSON-focused prompt with explicit single-line instruction
            if self.provider == 'gemini':
                json_prompt = f"{prompt}\n\nIMPORTANT: Output ONLY a single-line JSON object with no line breaks, no indentation, no extra spaces. Example format: {{\"key\":\"value\",\"key2\":\"value2\"}}"
            else:
                json_prompt = f"{prompt}\n\nCRITICAL: Your response must be ONLY valid JSON. Do not include any markdown formatting, code blocks, or explanatory text. Output raw JSON only."
            
            response = self.generate_completion(json_prompt, temperature=temperature, max_tokens=1500)
            original_response = response  # Save for error reporting
            
            # Check if response is a safety warning
            if response.startswith("⚠️"):
                raise Exception(response)
            
            # Store original response before any cleaning
            original_response = response.strip()
            
            # Remove markdown code blocks if present
            if original_response.startswith('```'):
                lines = original_response.split('\n')
                if len(lines) > 2:
                    original_response = '\n'.join(lines[1:-1])
                    if original_response.startswith('json') or original_response.startswith('JSON'):
                        original_response = original_response[4:].strip()
            
            # Try to parse original response first
            try:
                return json.loads(original_response)
            except json.JSONDecodeError:
                pass
            
            # Remove extra whitespace but preserve structure
            cleaned = ' '.join(original_response.split())
            try:
                return json.loads(cleaned)
            except json.JSONDecodeError:
                pass
            
            # Try to find JSON object in response
            start_idx = original_response.find('{')
            end_idx = original_response.rfind('}')
            if start_idx != -1 and end_idx != -1:
                json_str = original_response[start_idx:end_idx + 1]
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    pass
            
            # Try to find JSON array in response
            start_idx = original_response.find('[')
            end_idx = original_response.rfind(']')
            if start_idx != -1 and end_idx != -1:
                json_str = original_response[start_idx:end_idx + 1]
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    pass
            
            # If nothing worked, raise clear error with actual response
            raise json.JSONDecodeError(f"Could not parse JSON from: {original_response[:200]}", original_response, 0)
                    
        except json.JSONDecodeError:
            # Show the ACTUAL response that failed to parse
            clean_preview = original_response.replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
            # Limit to reasonable length
            if len(clean_preview) > 500:
                clean_preview = clean_preview[:500] + "..."
            
            raise Exception(f"JSON parsing failed. Gemini returned: {clean_preview}")
        except Exception as ex:
            raise Exception(f"Unexpected error in generate_json_completion: {str(ex)}")
    
    def categorize_email(self, sender: str, subject: str, body: str, 
                        categorization_prompt: str) -> str:
        """
        Categorize an email using the LLM.
        
        Args:
            sender: Email sender
            subject: Email subject
            body: Email body
            categorization_prompt: The prompt template for categorization
            
        Returns:
            Category name (Important, Newsletter, Spam, To-Do)
        """
        prompt = categorization_prompt.format(
            sender=sender,
            subject=subject,
            body=body
        )
        
        response = self.generate_completion(prompt, temperature=0.3, max_tokens=50)
        
        # Normalize response
        category = response.strip().title()
        valid_categories = ['Important', 'Newsletter', 'Spam', 'To-Do']
        
        if category not in valid_categories:
            # Try to find a valid category in the response
            for valid_cat in valid_categories:
                if valid_cat.lower() in response.lower():
                    return valid_cat
            # Default to Important if unclear
            return 'Important'
        
        return category
    
    def extract_action_items(self, sender: str, subject: str, body: str,
                            action_prompt: str) -> Dict[str, Any]:
        """
        Extract action items from an email.
        
        Args:
            sender: Email sender
            subject: Email subject
            body: Email body
            action_prompt: The prompt template for action extraction
            
        Returns:
            Dictionary with tasks list
        """
        prompt = action_prompt.format(
            sender=sender,
            subject=subject,
            body=body
        )
        
        result = self.generate_json_completion(prompt)
        
        # Ensure tasks key exists
        if 'tasks' not in result:
            result['tasks'] = []
        
        return result
    
    def generate_reply_draft(self, sender: str, subject: str, body: str,
                            reply_prompt: str) -> Dict[str, Any]:
        """
        Generate a reply draft for an email.
        
        Args:
            sender: Email sender
            subject: Email subject
            body: Email body
            reply_prompt: The prompt template for reply generation
            
        Returns:
            Dictionary with subject, body, and tone
        """
        prompt = reply_prompt.format(
            sender=sender,
            subject=subject,
            body=body
        )
        
        response = self.generate_json_completion(prompt, temperature=0.7)
        
        # Ensure all required fields are present
        if 'subject' not in response:
            response['subject'] = f"Re: {subject}"
        if 'body' not in response:
            response['body'] = "Thank you for your email. I will review and respond shortly."
        if 'tone' not in response:
            response['tone'] = "professional"
        
        return response
    
    def analyze_urgency(self, sender: str, subject: str, body: str,
                       urgency_prompt: str) -> Dict[str, Any]:
        """
        Analyze the urgency level of an email.
        
        Args:
            sender: Email sender
            subject: Email subject
            body: Email body
            urgency_prompt: The prompt template for urgency analysis
            
        Returns:
            Dictionary with urgency_score, reason, and suggested_response_time
        """
        prompt = urgency_prompt.format(
            sender=sender,
            subject=subject,
            body=body
        )
        
        result = self.generate_json_completion(prompt)
        
        # Ensure required fields exist with defaults
        if 'urgency_score' not in result:
            result['urgency_score'] = 3
        if 'reason' not in result:
            result['reason'] = 'Unable to determine urgency'
        if 'suggested_response_time' not in result:
            result['suggested_response_time'] = '1-2 days'
        
        return result
    
    def chat_query(self, query: str, context: str = "") -> str:
        """
        Handle a chat query about emails.
        
        Args:
            query: User's question or request
            context: Additional context (email content, summaries, etc.)
            
        Returns:
            Agent's response
        """
        prompt = f"""You are an intelligent email assistant. Help the user with their email-related query.

Context:
{context}

User Query: {query}

Provide a helpful, concise response. If the query involves summarizing emails, extracting information, or drafting responses, do so clearly and professionally."""

        return self.generate_completion(prompt, temperature=0.7, max_tokens=1500)
    
    def test_connection(self) -> bool:
        """
        Test if the LLM connection is working.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            response = self.generate_completion("Say 'hello'", temperature=0.5, max_tokens=10)
            return len(response) > 0
        except Exception:
            return False

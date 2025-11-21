"""
Agent service - orchestrates the email processing pipeline.
"""
from typing import List, Dict, Any
from backend.services.storage_service import StorageService
from backend.services.llm_service import LLMService
from backend.services.email_service import EmailService
from backend.services.prompt_service import PromptService


class AgentService:
    """Main agent that orchestrates email processing and chat interactions."""
    
    def __init__(self, storage_service: StorageService = None, llm_service: LLMService = None):
        """
        Initialize the agent service.
        
        Args:
            storage_service: Storage service instance
            llm_service: LLM service instance
        """
        self.storage = storage_service or StorageService()
        self.llm = llm_service or LLMService()
        self.email_service = EmailService(self.storage)
        self.prompt_service = PromptService(self.storage)
        
        # Ensure default prompts are loaded
        self.prompt_service.ensure_default_prompts_loaded()
    
    def load_mock_inbox(self) -> int:
        """
        Load the mock inbox.
        
        Returns:
            Number of emails loaded
        """
        return self.email_service.load_mock_inbox()
    
    def process_email(self, email_id: str) -> Dict[str, Any]:
        """
        Process a single email: categorize, extract actions, generate draft.
        
        Args:
            email_id: ID of the email to process
            
        Returns:
            Dictionary with processing results
        """
        # Get email
        email = self.storage.get_email_by_id(email_id)
        if not email:
            raise ValueError(f"Email not found: {email_id}")
        
        results = {
            'email_id': email_id,
            'category': None,
            'action_items': [],
            'draft': None,
            'errors': []
        }
        
        # 1. Categorize email
        try:
            cat_prompt = self.prompt_service.get_prompt_template('categorization')
            category = self.llm.categorize_email(
                email.sender,
                email.subject,
                email.body,
                cat_prompt
            )
            self.storage.add_category(email_id, category)
            results['category'] = category
        except Exception as e:
            results['errors'].append(f"Categorization failed: {str(e)}")
        
        # 2. Extract action items
        try:
            action_prompt = self.prompt_service.get_prompt_template('action_extraction')
            action_data = self.llm.extract_action_items(
                email.sender,
                email.subject,
                email.body,
                action_prompt
            )
            
            tasks = action_data.get('tasks', [])
            for task_item in tasks:
                action = self.storage.add_action_item(
                    email_id,
                    task_item.get('task', 'No task description'),
                    task_item.get('deadline'),
                    task_item.get('priority', 'medium')
                )
                results['action_items'].append({
                    'id': action.id,
                    'task': action.task,
                    'deadline': action.deadline,
                    'priority': action.priority
                })
        except Exception as e:
            results['errors'].append(f"Action extraction failed: {str(e)}")
        
        # 3. Generate reply draft (only for certain categories)
        try:
            category = results.get('category', '')
            if category in ['Important', 'To-Do']:
                reply_prompt = self.prompt_service.get_prompt_template('auto_reply')
                draft_data = self.llm.generate_reply_draft(
                    email.sender,
                    email.subject,
                    email.body,
                    reply_prompt
                )
                
                draft = self.storage.add_draft(
                    email_id,
                    draft_data.get('subject', f"Re: {email.subject}"),
                    draft_data.get('body', ''),
                    draft_data.get('tone', 'professional')
                )
                results['draft'] = {
                    'id': draft.id,
                    'subject': draft.subject,
                    'body': draft.body,
                    'tone': draft.tone
                }
        except Exception as e:
            results['errors'].append(f"Draft generation failed: {str(e)}")
        
        # Mark email as processed
        self.storage.update_email_processed(email_id, True)
        
        return results
    
    def process_all_emails(self, limit: int = None) -> Dict[str, Any]:
        """
        Process all unprocessed emails in the inbox.
        
        Args:
            limit: Maximum number of emails to process
            
        Returns:
            Dictionary with summary of processing results
        """
        unprocessed = self.email_service.get_unprocessed_emails()
        
        if limit:
            unprocessed = unprocessed[:limit]
        
        summary = {
            'total_processed': 0,
            'successful': 0,
            'failed': 0,
            'errors': []
        }
        
        for email in unprocessed:
            try:
                result = self.process_email(email.id)
                summary['total_processed'] += 1
                
                if result['errors']:
                    summary['errors'].extend(result['errors'])
                else:
                    summary['successful'] += 1
                    
            except Exception as e:
                summary['failed'] += 1
                summary['errors'].append(f"Failed to process {email.id}: {str(e)}")
        
        return summary
    
    def chat_query(self, user_query: str, email_id: str = None) -> str:
        """
        Handle a chat query from the user.
        
        Args:
            user_query: User's question or request
            email_id: Optional specific email ID for context
            
        Returns:
            Agent's response
        """
        context = ""
        
        # Build context based on query
        if email_id:
            # Specific email context
            email = self.storage.get_email_by_id(email_id)
            if email:
                formatted_email = self.email_service.format_email_for_display(email)
                context = f"""
Email Details:
From: {formatted_email['sender_name']} ({formatted_email['sender']})
Subject: {formatted_email['subject']}
Body: {formatted_email['body'][:500]}...
Category: {formatted_email['category']}
Action Items: {len(formatted_email['action_items'])}
"""
        else:
            # General inbox context
            query_lower = user_query.lower()
            
            if 'urgent' in query_lower or 'important' in query_lower:
                context = self.email_service.get_emails_summary(category='Important')
            elif 'task' in query_lower or 'to-do' in query_lower or 'action' in query_lower:
                context = self.email_service.get_emails_summary(category='To-Do')
                # Add action items
                actions = self.storage.get_all_action_items(completed=False)
                if actions:
                    context += "\n\nPending Action Items:\n"
                    for action in actions[:10]:
                        context += f"- {action.task}"
                        if action.deadline:
                            context += f" (Due: {action.deadline})"
                        context += f" [Priority: {action.priority}]\n"
            elif 'meeting' in query_lower:
                # Search for meeting-related emails
                meetings = self.email_service.search_emails('meeting', limit=10)
                context = "Meeting-related emails:\n"
                for email in meetings:
                    context += f"- {email.subject} (From: {email.sender_name})\n"
            else:
                # General inbox summary
                stats = self.email_service.get_email_statistics()
                context = f"""
Inbox Statistics:
- Total emails: {stats['total_emails']}
- Processed: {stats['processed_emails']}
- Categories: {stats['categories']}
- Pending action items: {stats['pending_action_items']}

Recent emails:
{self.email_service.get_emails_summary()[:1000]}
"""
        
        # Generate response
        response = self.llm.chat_query(user_query, context)
        
        # Store in chat history
        self.storage.add_chat_message(user_query, response, context[:500])
        
        return response
    
    def generate_email_draft(self, subject: str, context: str, tone: str = "professional") -> Dict[str, str]:
        """
        Generate a new email draft (not a reply).
        
        Args:
            subject: Subject for the email
            context: Context or instructions for the email
            tone: Desired tone (professional, friendly, formal)
            
        Returns:
            Dictionary with subject and body
        """
        prompt = f"""Generate a professional email with the following requirements:

Subject: {subject}
Context/Purpose: {context}
Tone: {tone}

Write a complete, well-structured email body. Be concise and professional."""

        body = self.llm.generate_completion(prompt, temperature=0.7, max_tokens=1000)
        
        # Store as draft (not linked to any email)
        draft = self.storage.add_draft(
            email_id=None,
            subject=subject,
            body=body,
            tone=tone,
            draft_type='new'
        )
        
        return {
            'id': draft.id,
            'subject': subject,
            'body': body,
            'tone': tone
        }
    
    def get_inbox_summary(self) -> Dict[str, Any]:
        """
        Get a comprehensive summary of the inbox.
        
        Returns:
            Dictionary with inbox statistics and highlights
        """
        stats = self.email_service.get_email_statistics()
        
        # Get urgent/important emails
        important_emails = self.email_service.get_emails_by_category('Important')
        todo_emails = self.email_service.get_emails_by_category('To-Do')
        
        # Get pending actions
        pending_actions = self.storage.get_all_action_items(completed=False)
        
        return {
            'statistics': stats,
            'important_count': len(important_emails),
            'todo_count': len(todo_emails),
            'pending_actions_count': len(pending_actions),
            'recent_important': [
                {
                    'subject': email.subject,
                    'sender': email.sender_name or email.sender,
                    'timestamp': email.timestamp.isoformat()
                }
                for email in important_emails[:5]
            ]
        }

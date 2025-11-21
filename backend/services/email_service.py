"""
Email service for loading and managing inbox emails.
"""
import json
import os
from typing import List, Dict, Any
from backend.services.storage_service import StorageService


class EmailService:
    """Handles email loading and parsing operations."""
    
    def __init__(self, storage_service: StorageService):
        """
        Initialize email service.
        
        Args:
            storage_service: Storage service instance for database operations
        """
        self.storage = storage_service
    
    def load_mock_inbox(self, mock_inbox_path: str = 'data/mock_inbox.json') -> int:
        """
        Load emails from the mock inbox JSON file.
        
        Args:
            mock_inbox_path: Path to the mock inbox JSON file
            
        Returns:
            Number of emails loaded
        """
        try:
            if not os.path.exists(mock_inbox_path):
                raise FileNotFoundError(f"Mock inbox file not found: {mock_inbox_path}")
            
            with open(mock_inbox_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            emails = data.get('emails', [])
            count = 0
            
            for email_data in emails:
                try:
                    self.storage.add_email(email_data)
                    count += 1
                except Exception as e:
                    print(f"Failed to load email {email_data.get('id')}: {str(e)}")
            
            return count
        
        except Exception as e:
            raise Exception(f"Failed to load mock inbox: {str(e)}")
    
    def get_emails_by_category(self, category: str) -> List[Any]:
        """
        Get emails filtered by category.
        
        Args:
            category: Category name (Important, Newsletter, Spam, To-Do)
            
        Returns:
            List of emails in the specified category
        """
        return self.storage.get_all_emails(category=category)
    
    def get_unprocessed_emails(self) -> List[Any]:
        """
        Get emails that haven't been processed yet.
        
        Returns:
            List of unprocessed emails
        """
        session = self.storage.get_session()
        try:
            from backend.models.database import Email
            return session.query(Email).filter(Email.processed == False).all()
        finally:
            session.close()
    
    def search_emails(self, query: str, limit: int = 20) -> List[Any]:
        """
        Search emails by subject or body content.
        
        Args:
            query: Search query string
            limit: Maximum number of results
            
        Returns:
            List of matching emails
        """
        session = self.storage.get_session()
        try:
            from backend.models.database import Email
            query_lower = query.lower()
            
            emails = session.query(Email).all()
            matches = []
            
            for email in emails:
                if (query_lower in email.subject.lower() or 
                    query_lower in email.body.lower() or
                    query_lower in email.sender.lower()):
                    matches.append(email)
                    if len(matches) >= limit:
                        break
            
            return matches
        finally:
            session.close()
    
    def get_email_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about emails in the inbox.
        
        Returns:
            Dictionary with email statistics
        """
        session = self.storage.get_session()
        try:
            from backend.models.database import Email, EmailCategory, ActionItem
            from sqlalchemy import func
            
            total_emails = session.query(Email).count()
            processed_emails = session.query(Email).filter(Email.processed == True).count()
            
            # Category counts
            category_counts = session.query(
                EmailCategory.category,
                func.count(EmailCategory.id)
            ).group_by(EmailCategory.category).all()
            
            categories = {cat: count for cat, count in category_counts}
            
            # Action items
            total_actions = session.query(ActionItem).count()
            pending_actions = session.query(ActionItem).filter(ActionItem.completed == False).count()
            
            return {
                'total_emails': total_emails,
                'processed_emails': processed_emails,
                'unprocessed_emails': total_emails - processed_emails,
                'categories': categories,
                'total_action_items': total_actions,
                'pending_action_items': pending_actions
            }
        finally:
            session.close()
    
    def format_email_for_display(self, email: Any) -> Dict[str, Any]:
        """
        Format an email object for display in UI.
        
        Args:
            email: Email model instance
            
        Returns:
            Dictionary with formatted email data
        """
        category = self.storage.get_category_by_email(email.id)
        action_items = self.storage.get_action_items_by_email(email.id)
        drafts = self.storage.get_drafts_by_email(email.id)
        
        return {
            'id': email.id,
            'sender': email.sender,
            'sender_name': email.sender_name,
            'subject': email.subject,
            'body': email.body,
            'timestamp': email.timestamp.isoformat(),
            'has_attachments': email.has_attachments,
            'labels': json.loads(email.labels) if email.labels else [],
            'processed': email.processed,
            'category': category.category if category else None,
            'action_items': [
                {
                    'id': item.id,
                    'task': item.task,
                    'deadline': item.deadline,
                    'priority': item.priority,
                    'completed': item.completed
                }
                for item in action_items
            ],
            'drafts': [
                {
                    'id': draft.id,
                    'subject': draft.subject,
                    'body': draft.body,
                    'tone': draft.tone
                }
                for draft in drafts
            ]
        }
    
    def get_emails_summary(self, category: str = None) -> str:
        """
        Get a text summary of emails for chat context.
        
        Args:
            category: Optional category filter
            
        Returns:
            Formatted text summary of emails
        """
        emails = self.storage.get_all_emails(limit=50, category=category)
        
        if not emails:
            return "No emails found."
        
        summary_lines = []
        for email in emails:
            category_obj = self.storage.get_category_by_email(email.id)
            category_name = category_obj.category if category_obj else "Uncategorized"
            
            summary_lines.append(
                f"[{category_name}] From: {email.sender_name or email.sender} | "
                f"Subject: {email.subject} | "
                f"Date: {email.timestamp.strftime('%Y-%m-%d %H:%M')}"
            )
        
        return "\n".join(summary_lines)

"""
Storage service for database operations.
"""
import os
import json
from datetime import datetime
from typing import List, Dict, Optional, Any
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker, Session
from backend.models.database import Base, Email, Prompt, EmailCategory, ActionItem, Draft, ChatHistory


class StorageService:
    """Handles all database operations."""
    
    def __init__(self, db_path: str = None):
        """Initialize the storage service with database connection."""
        if db_path is None:
            db_path = os.getenv('DATABASE_PATH', 'data/email_agent.db')
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)
    
    def get_session(self) -> Session:
        """Get a new database session."""
        return self.SessionLocal()
    
    # Email Operations
    def add_email(self, email_data: Dict[str, Any]) -> Email:
        """Add a new email to the database."""
        session = self.get_session()
        try:
            email = Email(
                id=email_data['id'],
                sender=email_data['sender'],
                sender_name=email_data.get('sender_name'),
                subject=email_data['subject'],
                body=email_data['body'],
                timestamp=datetime.fromisoformat(email_data['timestamp'].replace('Z', '+00:00')),
                has_attachments=email_data.get('has_attachments', False),
                labels=json.dumps(email_data.get('labels', []))
            )
            session.add(email)
            session.commit()
            session.refresh(email)
            return email
        finally:
            session.close()
    
    def get_all_emails(self, limit: int = None, category: str = None) -> List[Email]:
        """Get all emails, optionally filtered by category."""
        session = self.get_session()
        try:
            query = session.query(Email).order_by(desc(Email.timestamp))
            
            if category:
                query = query.join(EmailCategory).filter(EmailCategory.category == category)
            
            if limit:
                query = query.limit(limit)
            
            return query.all()
        finally:
            session.close()
    
    def get_email_by_id(self, email_id: str) -> Optional[Email]:
        """Get a specific email by ID."""
        session = self.get_session()
        try:
            return session.query(Email).filter(Email.id == email_id).first()
        finally:
            session.close()
    
    def update_email_processed(self, email_id: str, processed: bool = True):
        """Mark an email as processed."""
        session = self.get_session()
        try:
            email = session.query(Email).filter(Email.id == email_id).first()
            if email:
                email.processed = processed
                session.commit()
        finally:
            session.close()
    
    def clear_all_emails(self):
        """Clear all emails from the database."""
        session = self.get_session()
        try:
            session.query(Email).delete()
            session.commit()
        finally:
            session.close()
    
    # Prompt Operations
    def add_prompt(self, name: str, description: str, template: str, 
                   prompt_type: str, version: str = "1.0", active: bool = True) -> Prompt:
        """Add or update a prompt template."""
        session = self.get_session()
        try:
            # Check if prompt exists
            existing = session.query(Prompt).filter(Prompt.name == name).first()
            if existing:
                existing.description = description
                existing.template = template
                existing.prompt_type = prompt_type
                existing.version = version
                existing.active = active
                existing.updated_at = datetime.utcnow()
                session.commit()
                return existing
            else:
                prompt = Prompt(
                    name=name,
                    description=description,
                    template=template,
                    prompt_type=prompt_type,
                    version=version,
                    active=active
                )
                session.add(prompt)
                session.commit()
                session.refresh(prompt)
                return prompt
        finally:
            session.close()
    
    def get_prompt_by_type(self, prompt_type: str) -> Optional[Prompt]:
        """Get an active prompt by type."""
        session = self.get_session()
        try:
            return session.query(Prompt).filter(
                Prompt.prompt_type == prompt_type,
                Prompt.active == True
            ).first()
        finally:
            session.close()
    
    def get_all_prompts(self) -> List[Prompt]:
        """Get all prompts."""
        session = self.get_session()
        try:
            return session.query(Prompt).all()
        finally:
            session.close()
    
    def update_prompt_template(self, prompt_type: str, new_template: str):
        """Update a prompt template."""
        session = self.get_session()
        try:
            prompt = session.query(Prompt).filter(
                Prompt.prompt_type == prompt_type,
                Prompt.active == True
            ).first()
            if prompt:
                prompt.template = new_template
                prompt.updated_at = datetime.utcnow()
                session.commit()
        finally:
            session.close()
    
    # Category Operations
    def add_category(self, email_id: str, category: str, confidence: str = None) -> EmailCategory:
        """Add email categorization result."""
        session = self.get_session()
        try:
            # Check if category exists
            existing = session.query(EmailCategory).filter(EmailCategory.email_id == email_id).first()
            if existing:
                existing.category = category
                existing.confidence = confidence
                session.commit()
                return existing
            else:
                email_category = EmailCategory(
                    email_id=email_id,
                    category=category,
                    confidence=confidence
                )
                session.add(email_category)
                session.commit()
                session.refresh(email_category)
                return email_category
        finally:
            session.close()
    
    def get_category_by_email(self, email_id: str) -> Optional[EmailCategory]:
        """Get category for a specific email."""
        session = self.get_session()
        try:
            return session.query(EmailCategory).filter(EmailCategory.email_id == email_id).first()
        finally:
            session.close()
    
    # Action Item Operations
    def add_action_item(self, email_id: str, task: str, deadline: str = None, 
                        priority: str = "medium") -> ActionItem:
        """Add an action item extracted from an email."""
        session = self.get_session()
        try:
            action_item = ActionItem(
                email_id=email_id,
                task=task,
                deadline=deadline,
                priority=priority
            )
            session.add(action_item)
            session.commit()
            session.refresh(action_item)
            return action_item
        finally:
            session.close()
    
    def get_action_items_by_email(self, email_id: str) -> List[ActionItem]:
        """Get all action items for a specific email."""
        session = self.get_session()
        try:
            return session.query(ActionItem).filter(ActionItem.email_id == email_id).all()
        finally:
            session.close()
    
    def get_all_action_items(self, completed: bool = None) -> List[ActionItem]:
        """Get all action items, optionally filtered by completion status."""
        session = self.get_session()
        try:
            query = session.query(ActionItem).order_by(desc(ActionItem.created_at))
            if completed is not None:
                query = query.filter(ActionItem.completed == completed)
            return query.all()
        finally:
            session.close()
    
    def mark_action_completed(self, action_id: int, completed: bool = True):
        """Mark an action item as completed."""
        session = self.get_session()
        try:
            action = session.query(ActionItem).filter(ActionItem.id == action_id).first()
            if action:
                action.completed = completed
                session.commit()
        finally:
            session.close()
    
    # Draft Operations
    def add_draft(self, email_id: str, subject: str, body: str, 
                  tone: str = None, draft_type: str = "reply") -> Draft:
        """Add a draft email."""
        session = self.get_session()
        try:
            draft = Draft(
                email_id=email_id,
                subject=subject,
                body=body,
                tone=tone,
                draft_type=draft_type
            )
            session.add(draft)
            session.commit()
            session.refresh(draft)
            return draft
        finally:
            session.close()
    
    def get_drafts_by_email(self, email_id: str) -> List[Draft]:
        """Get all drafts for a specific email."""
        session = self.get_session()
        try:
            return session.query(Draft).filter(Draft.email_id == email_id).order_by(desc(Draft.created_at)).all()
        finally:
            session.close()
    
    def get_all_drafts(self) -> List[Draft]:
        """Get all drafts."""
        session = self.get_session()
        try:
            return session.query(Draft).order_by(desc(Draft.created_at)).all()
        finally:
            session.close()
    
    def update_draft(self, draft_id: int, subject: str = None, body: str = None):
        """Update a draft."""
        session = self.get_session()
        try:
            draft = session.query(Draft).filter(Draft.id == draft_id).first()
            if draft:
                if subject:
                    draft.subject = subject
                if body:
                    draft.body = body
                draft.updated_at = datetime.utcnow()
                session.commit()
        finally:
            session.close()
    
    def delete_draft(self, draft_id: int):
        """Delete a draft."""
        session = self.get_session()
        try:
            draft = session.query(Draft).filter(Draft.id == draft_id).first()
            if draft:
                session.delete(draft)
                session.commit()
        finally:
            session.close()
    
    # Chat History Operations
    def add_chat_message(self, user_message: str, agent_response: str, context: str = None) -> ChatHistory:
        """Add a chat message to history."""
        session = self.get_session()
        try:
            chat = ChatHistory(
                user_message=user_message,
                agent_response=agent_response,
                context=context
            )
            session.add(chat)
            session.commit()
            session.refresh(chat)
            return chat
        finally:
            session.close()
    
    def get_chat_history(self, limit: int = 50) -> List[ChatHistory]:
        """Get recent chat history."""
        session = self.get_session()
        try:
            return session.query(ChatHistory).order_by(desc(ChatHistory.timestamp)).limit(limit).all()
        finally:
            session.close()
    
    def clear_chat_history(self):
        """Clear all chat history."""
        session = self.get_session()
        try:
            session.query(ChatHistory).delete()
            session.commit()
        finally:
            session.close()

"""
Database models for the Email Productivity Agent.
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Email(Base):
    """Email model for storing inbox emails."""
    __tablename__ = 'emails'
    
    id = Column(String, primary_key=True)
    sender = Column(String, nullable=False)
    sender_name = Column(String)
    subject = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    has_attachments = Column(Boolean, default=False)
    labels = Column(String)  # JSON string of labels
    processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    category = relationship("EmailCategory", back_populates="email", uselist=False)
    action_items = relationship("ActionItem", back_populates="email")
    drafts = relationship("Draft", back_populates="email")


class Prompt(Base):
    """Prompt template model for storing user-defined prompts."""
    __tablename__ = 'prompts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text)
    template = Column(Text, nullable=False)
    prompt_type = Column(String, nullable=False)  # categorization, action_extraction, auto_reply, etc.
    version = Column(String, default="1.0")
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class EmailCategory(Base):
    """Email categorization results."""
    __tablename__ = 'email_categories'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email_id = Column(String, ForeignKey('emails.id'), unique=True, nullable=False)
    category = Column(String, nullable=False)  # Important, Newsletter, Spam, To-Do
    confidence = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    email = relationship("Email", back_populates="category")


class ActionItem(Base):
    """Action items extracted from emails."""
    __tablename__ = 'action_items'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email_id = Column(String, ForeignKey('emails.id'), nullable=False)
    task = Column(Text, nullable=False)
    deadline = Column(String)
    priority = Column(String)  # high, medium, low
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    email = relationship("Email", back_populates="action_items")


class Draft(Base):
    """Draft email responses."""
    __tablename__ = 'drafts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email_id = Column(String, ForeignKey('emails.id'))
    subject = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    tone = Column(String)
    draft_type = Column(String)  # reply, new, forward
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    email = relationship("Email", back_populates="drafts")


class ChatHistory(Base):
    """Chat history with the email agent."""
    __tablename__ = 'chat_history'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_message = Column(Text, nullable=False)
    agent_response = Column(Text, nullable=False)
    context = Column(Text)  # JSON string of context used
    timestamp = Column(DateTime, default=datetime.utcnow)

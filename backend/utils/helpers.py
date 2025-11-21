"""
Utility functions for the Email Productivity Agent
"""
from datetime import datetime
from typing import Dict, Any


def format_timestamp(timestamp: datetime) -> str:
    """
    Format a datetime object for display.
    
    Args:
        timestamp: datetime object
        
    Returns:
        Formatted string
    """
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to a maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def get_priority_emoji(priority: str) -> str:
    """
    Get emoji for priority level.
    
    Args:
        priority: Priority level (high, medium, low)
        
    Returns:
        Emoji string
    """
    emoji_map = {
        'high': '🔴',
        'medium': '🟡',
        'low': '🟢'
    }
    return emoji_map.get(priority.lower(), '⚪')


def get_category_emoji(category: str) -> str:
    """
    Get emoji for email category.
    
    Args:
        category: Category name
        
    Returns:
        Emoji string
    """
    emoji_map = {
        'important': '🔴',
        'to-do': '🟡',
        'newsletter': '🔵',
        'spam': '⚫'
    }
    return emoji_map.get(category.lower(), '⚪')


def validate_email_data(email_data: Dict[str, Any]) -> bool:
    """
    Validate email data structure.
    
    Args:
        email_data: Email data dictionary
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ['id', 'sender', 'subject', 'body', 'timestamp']
    return all(field in email_data for field in required_fields)


def sanitize_email_body(body: str) -> str:
    """
    Sanitize email body for safe display.
    
    Args:
        body: Raw email body
        
    Returns:
        Sanitized body
    """
    # Basic sanitization - in production, use proper HTML sanitization
    return body.replace('<script>', '').replace('</script>', '')

"""
Basic tests for the Email Productivity Agent
"""
import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))


def test_storage_service():
    """Test storage service initialization."""
    from backend.services.storage_service import StorageService
    
    storage = StorageService(db_path='test_email_agent.db')
    assert storage is not None
    
    # Cleanup
    if os.path.exists('test_email_agent.db'):
        os.remove('test_email_agent.db')
    
    print("✅ Storage service test passed")


def test_prompt_service():
    """Test prompt service."""
    from backend.services.storage_service import StorageService
    from backend.services.prompt_service import PromptService
    
    storage = StorageService(db_path='test_email_agent.db')
    prompt_service = PromptService(storage)
    
    # Load default prompts
    prompt_service.load_default_prompts()
    
    # Get a prompt
    cat_prompt = prompt_service.get_prompt_template('categorization')
    assert cat_prompt is not None
    assert '{sender}' in cat_prompt
    
    # Cleanup
    if os.path.exists('test_email_agent.db'):
        os.remove('test_email_agent.db')
    
    print("✅ Prompt service test passed")


def test_email_service():
    """Test email service."""
    from backend.services.storage_service import StorageService
    from backend.services.email_service import EmailService
    
    storage = StorageService(db_path='test_email_agent.db')
    email_service = EmailService(storage)
    
    # Load mock inbox
    count = email_service.load_mock_inbox()
    assert count > 0
    
    # Get emails
    emails = storage.get_all_emails()
    assert len(emails) > 0
    
    # Cleanup
    if os.path.exists('test_email_agent.db'):
        os.remove('test_email_agent.db')
    
    print(f"✅ Email service test passed - loaded {count} emails")


def test_mock_data():
    """Test mock inbox data structure."""
    import json
    
    with open('data/mock_inbox.json', 'r') as f:
        data = json.load(f)
    
    emails = data.get('emails', [])
    assert len(emails) > 0
    
    # Check first email structure
    email = emails[0]
    required_fields = ['id', 'sender', 'subject', 'body', 'timestamp']
    for field in required_fields:
        assert field in email, f"Missing field: {field}"
    
    print(f"✅ Mock data test passed - {len(emails)} emails validated")


def test_prompt_templates():
    """Test prompt template data structure."""
    import json
    
    with open('data/prompt_templates.json', 'r') as f:
        data = json.load(f)
    
    prompts = data.get('prompts', {})
    assert len(prompts) > 0
    
    # Check required prompt types
    required_types = ['categorization', 'action_extraction', 'auto_reply']
    for prompt_type in required_types:
        assert prompt_type in prompts, f"Missing prompt type: {prompt_type}"
        
        prompt_data = prompts[prompt_type]
        assert 'name' in prompt_data
        assert 'template' in prompt_data
        assert '{sender}' in prompt_data['template'] or '{subject}' in prompt_data['template']
    
    print(f"✅ Prompt templates test passed - {len(prompts)} prompts validated")


if __name__ == '__main__':
    print("Running Email Productivity Agent Tests...\n")
    
    try:
        test_mock_data()
        test_prompt_templates()
        test_storage_service()
        test_prompt_service()
        test_email_service()
        
        print("\n" + "="*50)
        print("🎉 All tests passed!")
        print("="*50)
    
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()

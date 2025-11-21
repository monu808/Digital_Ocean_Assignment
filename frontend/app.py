"""
Email Productivity Agent - Main Streamlit Application
"""
import streamlit as st
import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from backend.services.storage_service import StorageService
from backend.services.agent_service import AgentService

# Page configuration
st.set_page_config(
    page_title="Email Productivity Agent",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
    }
    .stat-label {
        font-size: 1rem;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'agent' not in st.session_state:
    try:
        st.session_state.agent = AgentService()
        st.session_state.storage = st.session_state.agent.storage
    except Exception as e:
        st.error(f"Failed to initialize agent: {str(e)}")
        st.info("Please ensure your .env file is configured correctly with API keys.")
        st.stop()

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/email.png", width=80)
    st.title("📧 Email Agent")
    st.markdown("---")
    
    # Navigation
    st.subheader("Navigation")
    page = st.radio(
        "Go to",
        ["🏠 Home", "⚙️ Prompt Configuration", "💬 Email Agent Chat", "📝 Draft Manager"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Quick stats
    st.subheader("Quick Stats")
    try:
        summary = st.session_state.agent.get_inbox_summary()
        stats = summary['statistics']
        
        st.metric("Total Emails", stats['total_emails'])
        st.metric("Pending Actions", summary['pending_actions_count'])
        st.metric("Important", summary['important_count'])
        st.metric("To-Do", summary['todo_count'])
    except Exception as e:
        st.info("Load inbox to see stats")
    
    st.markdown("---")
    st.caption("Built with ❤️ using Streamlit & LLMs")

# Main content area
if page == "🏠 Home":
    st.markdown('<div class="main-header">📧 Email Productivity Agent</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Intelligent email management powered by AI</div>', unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Load Mock Inbox", use_container_width=True, type="primary"):
            with st.spinner("Loading emails..."):
                try:
                    # Clear existing emails
                    st.session_state.storage.clear_all_emails()
                    
                    # Load mock inbox
                    count = st.session_state.agent.load_mock_inbox()
                    st.success(f"✅ Loaded {count} emails!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to load inbox: {str(e)}")
    
    with col2:
        if st.button("🔄 Process All Emails", use_container_width=True):
            with st.spinner("Processing emails with AI..."):
                try:
                    result = st.session_state.agent.process_all_emails()
                    st.success(f"✅ Processed {result['successful']} emails successfully!")
                    if result['errors']:
                        with st.expander("⚠️ View Errors"):
                            for error in result['errors']:
                                st.warning(error)
                    st.rerun()
                except Exception as e:
                    st.error(f"Processing failed: {str(e)}")
    
    with col3:
        if st.button("🗑️ Clear Inbox", use_container_width=True):
            if st.session_state.get('confirm_clear', False):
                st.session_state.storage.clear_all_emails()
                st.success("✅ Inbox cleared!")
                st.session_state.confirm_clear = False
                st.rerun()
            else:
                st.session_state.confirm_clear = True
                st.warning("Click again to confirm deletion")
    
    st.markdown("---")
    
    # Display inbox statistics
    try:
        summary = st.session_state.agent.get_inbox_summary()
        stats = summary['statistics']
        
        # Display statistics cards
        st.subheader("📊 Inbox Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{stats['total_emails']}</div>
                <div class="stat-label">Total Emails</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{stats['processed_emails']}</div>
                <div class="stat-label">Processed</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{stats['pending_action_items']}</div>
                <div class="stat-label">Pending Tasks</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{summary['important_count']}</div>
                <div class="stat-label">Important</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Category breakdown
        if stats['categories']:
            st.subheader("📂 Email Categories")
            col1, col2 = st.columns([2, 1])
            
            with col1:
                import pandas as pd
                df = pd.DataFrame(list(stats['categories'].items()), columns=['Category', 'Count'])
                st.bar_chart(df.set_index('Category'))
            
            with col2:
                for category, count in stats['categories'].items():
                    st.metric(category, count)
        
        st.markdown("---")
        
        # Email list
        st.subheader("📬 Inbox")
        
        # Filter options
        filter_col1, filter_col2 = st.columns([1, 3])
        with filter_col1:
            category_filter = st.selectbox(
                "Filter by Category",
                ["All"] + list(stats['categories'].keys())
            )
        
        # Get emails
        if category_filter == "All":
            emails = st.session_state.storage.get_all_emails(limit=50)
        else:
            emails = st.session_state.agent.email_service.get_emails_by_category(category_filter)
        
        # Display emails
        for email in emails:
            formatted = st.session_state.agent.email_service.format_email_for_display(email)
            
            with st.expander(f"{'📧' if not email.processed else '✅'} **{formatted['subject']}** - From: {formatted['sender_name']}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**From:** {formatted['sender_name']} ({formatted['sender']})")
                    st.markdown(f"**Subject:** {formatted['subject']}")
                    st.markdown(f"**Date:** {formatted['timestamp']}")
                    
                    if formatted['category']:
                        category_colors = {
                            'Important': '🔴',
                            'To-Do': '🟡',
                            'Newsletter': '🔵',
                            'Spam': '⚫'
                        }
                        st.markdown(f"**Category:** {category_colors.get(formatted['category'], '⚪')} {formatted['category']}")
                    
                    st.markdown("**Body:**")
                    st.text_area("", formatted['body'], height=200, key=f"body_{email.id}", label_visibility="collapsed")
                
                with col2:
                    if formatted['action_items']:
                        st.markdown("**📋 Action Items:**")
                        for item in formatted['action_items']:
                            st.markdown(f"- {item['task']}")
                            if item['deadline']:
                                st.caption(f"⏰ Due: {item['deadline']}")
                            st.caption(f"Priority: {item['priority']}")
                    
                    if formatted['drafts']:
                        st.markdown("**📝 Drafts:**")
                        st.info(f"{len(formatted['drafts'])} draft(s) available")
                    
                    if not email.processed:
                        if st.button("Process Email", key=f"process_{email.id}", use_container_width=True):
                            with st.spinner("Processing..."):
                                try:
                                    st.session_state.agent.process_email(email.id)
                                    st.success("✅ Processed!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Error: {str(e)}")
    
    except Exception as e:
        st.info("👆 Click 'Load Mock Inbox' to get started!")
        st.markdown("""
        ### 🚀 Getting Started
        
        1. **Load Mock Inbox** - Import 18 sample emails
        2. **Process All Emails** - Run AI categorization and action extraction
        3. **Explore** - Navigate to other pages to:
           - Configure custom prompts
           - Chat with the Email Agent
           - Manage email drafts
        """)

elif page == "⚙️ Prompt Configuration":
    from frontend.pages import prompt_config
    prompt_config.show()

elif page == "💬 Email Agent Chat":
    from frontend.pages import email_chat
    email_chat.show()

elif page == "📝 Draft Manager":
    from frontend.pages import draft_manager
    draft_manager.show()

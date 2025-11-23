"""
Email Agent Chat Page
"""
import streamlit as st


def show():
    """Display the email agent chat page."""
    st.title("💬 Email Agent Chat")
    st.markdown("Ask questions about your emails or get help managing your inbox.")
    st.markdown("---")
    
    agent = st.session_state.agent
    
    # Initialize chat history in session state
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    
    # Quick action buttons
    st.subheader("Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    quick_queries = {
        "📊 Summarize urgent emails": "Summarize all urgent and important emails in my inbox",
        "✅ List action items": "What are all my pending action items and tasks?",
        "📅 Meeting requests": "Show me all meeting requests",
        "🔍 Search emails": "Help me search my emails"
    }
    
    with col1:
        if st.button("📊 Summarize urgent", use_container_width=True):
            st.session_state.quick_query = quick_queries["📊 Summarize urgent emails"]
    
    with col2:
        if st.button("✅ List tasks", use_container_width=True):
            st.session_state.quick_query = quick_queries["✅ List action items"]
    
    with col3:
        if st.button("📅 Meetings", use_container_width=True):
            st.session_state.quick_query = quick_queries["📅 Meeting requests"]
    
    with col4:
        if st.button("🔍 Search", use_container_width=True):
            st.session_state.quick_query = quick_queries["🔍 Search emails"]
    
    st.markdown("---")
    
    # Chat interface
    st.subheader("Chat with Email Agent")
    
    # Display chat history
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.chat_messages:
            if message['role'] == 'user':
                st.chat_message("user").markdown(message['content'])
            else:
                st.chat_message("assistant").markdown(message['content'])
    
    # Chat input
    user_input = st.chat_input("Ask about your emails...")
    
    # Handle quick query button
    if 'quick_query' in st.session_state:
        user_input = st.session_state.quick_query
        del st.session_state.quick_query
    
    if user_input:
        # Add user message to chat
        st.session_state.chat_messages.append({
            'role': 'user',
            'content': user_input
        })
        
        # Display user message
        with chat_container:
            st.chat_message("user").markdown(user_input)
        
        # Generate response
        with st.spinner("🤔 Thinking..."):
            try:
                response = agent.chat_query(user_input)
                
                # Add assistant response to chat
                st.session_state.chat_messages.append({
                    'role': 'assistant',
                    'content': response
                })
                
                # Display assistant response
                with chat_container:
                    st.chat_message("assistant").markdown(response)
                
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.session_state.chat_messages.append({
                    'role': 'assistant',
                    'content': error_msg
                })
                with chat_container:
                    st.chat_message("assistant").markdown(error_msg)
        
        st.rerun()
    
    # Sidebar with context options
    with st.sidebar:
        st.markdown("---")
        st.subheader("Chat Options")
        
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.chat_messages = []
            agent.storage.clear_chat_history()
            st.rerun()
        
        st.markdown("---")
        st.subheader("💡 Example Queries")
        
        examples = [
            "Summarize all emails from today",
            "What tasks do I need to complete this week?",
            "Show me all unread important emails",
            "Which emails require immediate response?",
            "Draft a reply to the latest meeting request",
            "Search for emails about 'project deadline'",
            "What are my highest priority action items?",
            "Show me all emails from john.smith@company.com"
        ]
        
        for example in examples:
            st.caption(f"• {example}")
    
    # Draft generation section
    st.markdown("---")
    st.subheader("✉️ Generate New Email Draft")
    
    with st.expander("Create a new email"):
        draft_subject = st.text_input("Subject")
        draft_context = st.text_area(
            "Context/Instructions",
            placeholder="E.g., Write an email to the team about the project update..."
        )
        draft_tone = st.selectbox("Tone", ["professional", "friendly", "formal"])
        
        if st.button("Generate Draft", type="primary"):
            if draft_subject and draft_context:
                with st.spinner("Generating email draft..."):
                    try:
                        draft = agent.generate_email_draft(draft_subject, draft_context, draft_tone)
                        
                        st.success("✅ Draft generated!")
                        st.markdown("**Subject:**")
                        st.text(draft['subject'])
                        st.markdown("**Body:**")
                        st.text_area("Draft Body", draft['body'], height=300, label_visibility="collapsed")
                        
                        st.info("📝 Draft saved to Draft Manager")
                    except Exception as e:
                        st.error(f"Failed to generate draft: {str(e)}")
            else:
                st.warning("Please provide both subject and context")
    
    # Help section
    with st.expander("ℹ️ How to Use the Email Agent"):
        st.markdown("""
        ### What can the Email Agent do?
        
        - **Summarize Emails**: Get quick summaries of your inbox or specific categories
        - **Extract Information**: Find action items, tasks, deadlines
        - **Search**: Look for specific emails by sender, subject, or keywords
        - **Draft Replies**: Generate intelligent reply drafts for emails
        - **Analyze**: Get insights about email priority and urgency
        
        ### Tips for Better Results
        
        1. **Be Specific**: "Show me important emails from this week" works better than "show emails"
        2. **Use Context**: The agent has access to your entire inbox and understands categories
        3. **Ask Follow-ups**: You can ask clarifying questions or request more details
        4. **Iterate**: If the response isn't quite right, rephrase your question
        
        ### Example Conversations
        
        **User**: "What are my pending tasks?"  
        **Agent**: Lists all uncompleted action items with deadlines
        
        **User**: "Draft a reply to the meeting request from Sarah"  
        **Agent**: Generates a professional meeting response
        
        **User**: "Show me emails that need urgent attention"  
        **Agent**: Lists high-priority emails requiring action
        """)

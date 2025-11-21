"""
Prompt Configuration Page
"""
import streamlit as st


def show():
    """Display the prompt configuration page."""
    st.title("⚙️ Prompt Configuration")
    st.markdown("Customize the AI agent's behavior by editing prompt templates.")
    st.markdown("---")
    
    agent = st.session_state.agent
    
    # Get all prompts
    prompts = agent.prompt_service.get_all_prompts_dict()
    
    if not prompts:
        st.warning("No prompts found. Loading defaults...")
        agent.prompt_service.load_default_prompts()
        prompts = agent.prompt_service.get_all_prompts_dict()
    
    # Tabs for different prompt types
    tabs = st.tabs(["📂 Categorization", "✅ Action Extraction", "✉️ Auto-Reply", "📝 Summary", "⚡ Urgency Analysis"])
    
    prompt_types = ['categorization', 'action_extraction', 'auto_reply', 'summary', 'urgency_analysis']
    
    for tab, prompt_type in zip(tabs, prompt_types):
        with tab:
            if prompt_type in prompts:
                prompt_data = prompts[prompt_type]
                
                st.subheader(prompt_data['name'])
                st.caption(prompt_data['description'])
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**Version:** {prompt_data['version']}")
                    st.markdown(f"**Last Updated:** {prompt_data['updated_at'] or 'N/A'}")
                
                with col2:
                    active = st.checkbox("Active", value=prompt_data['active'], key=f"active_{prompt_type}")
                
                st.markdown("---")
                
                # Edit prompt template
                st.markdown("### Prompt Template")
                st.caption("Use {sender}, {subject}, {body} as placeholders for email content")
                
                new_template = st.text_area(
                    "Template Content",
                    value=prompt_data['template'],
                    height=400,
                    key=f"template_{prompt_type}"
                )
                
                # Save button
                col1, col2, col3 = st.columns([1, 1, 2])
                
                with col1:
                    if st.button("💾 Save Changes", key=f"save_{prompt_type}", type="primary"):
                        try:
                            agent.prompt_service.update_prompt(prompt_type, new_template)
                            st.success("✅ Prompt updated successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to save: {str(e)}")
                
                with col2:
                    if st.button("🔄 Reset to Default", key=f"reset_{prompt_type}"):
                        # Reload from default file
                        agent.prompt_service.load_default_prompts()
                        st.success("✅ Reset to default!")
                        st.rerun()
                
                # Test prompt
                with st.expander("🧪 Test This Prompt"):
                    st.markdown("Test the prompt with sample data")
                    
                    test_sender = st.text_input("Sender Email", "test@example.com", key=f"test_sender_{prompt_type}")
                    test_subject = st.text_input("Subject", "Test Email Subject", key=f"test_subject_{prompt_type}")
                    test_body = st.text_area("Body", "This is a test email body.", key=f"test_body_{prompt_type}")
                    
                    if st.button("🚀 Test Prompt", key=f"test_{prompt_type}"):
                        with st.spinner("Testing prompt with LLM..."):
                            try:
                                formatted_prompt = new_template.format(
                                    sender=test_sender,
                                    subject=test_subject,
                                    body=test_body
                                )
                                
                                st.markdown("**Formatted Prompt Sent to LLM:**")
                                st.code(formatted_prompt, language="text")
                                
                                # Call LLM
                                if prompt_type == 'categorization':
                                    result = agent.llm.categorize_email(test_sender, test_subject, test_body, new_template)
                                    st.markdown("**Result:**")
                                    st.success(f"Category: {result}")
                                
                                elif prompt_type == 'action_extraction':
                                    result = agent.llm.extract_action_items(test_sender, test_subject, test_body, new_template)
                                    st.markdown("**Result:**")
                                    st.json(result)
                                
                                elif prompt_type == 'auto_reply':
                                    result = agent.llm.generate_reply_draft(test_sender, test_subject, test_body, new_template)
                                    st.markdown("**Result:**")
                                    st.json(result)
                                
                                else:
                                    result = agent.llm.generate_completion(formatted_prompt)
                                    st.markdown("**Result:**")
                                    st.write(result)
                                
                            except Exception as e:
                                st.error(f"Test failed: {str(e)}")
            else:
                st.warning(f"Prompt type '{prompt_type}' not found in database")
    
    # Help section
    st.markdown("---")
    with st.expander("ℹ️ How to Use Prompts"):
        st.markdown("""
        ### Prompt Variables
        
        Use these placeholders in your prompt templates:
        - `{sender}` - Email sender address
        - `{subject}` - Email subject line
        - `{body}` - Email body content
        
        ### Best Practices
        
        1. **Be Specific**: Clearly define what you want the AI to do
        2. **Use Examples**: Show the AI the expected output format
        3. **Set Constraints**: Define boundaries and rules
        4. **Test Thoroughly**: Use the test feature before applying to all emails
        
        ### Prompt Types
        
        - **Categorization**: Classifies emails into categories
        - **Action Extraction**: Pulls out tasks and deadlines
        - **Auto-Reply**: Generates draft responses
        - **Summary**: Creates concise email summaries
        - **Urgency Analysis**: Determines email priority
        """)

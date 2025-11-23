"""
Draft Manager Page
"""
import streamlit as st


def show():
    """Display the draft manager page."""
    st.title("📝 Draft Manager")
    st.markdown("View, edit, and manage your email drafts.")
    st.markdown("---")
    
    agent = st.session_state.agent
    
    # Get all drafts
    drafts = agent.storage.get_all_drafts()
    
    if not drafts:
        st.info("No drafts yet. Process some emails or use the Email Agent to generate drafts!")
        st.markdown("""
        ### How to Create Drafts
        
        1. **Process Emails**: Go to Home and click "Process All Emails"
        2. **Use Chat Agent**: Ask the agent to draft replies
        3. **Generate New**: Use the draft generator in the Email Agent Chat
        """)
        return
    
    st.subheader(f"📬 {len(drafts)} Draft(s) Found")
    
    # Filter options
    col1, col2 = st.columns([1, 3])
    with col1:
        filter_type = st.selectbox(
            "Filter by Type",
            ["All", "Reply", "New", "Forward"]
        )
    
    # Display drafts
    for idx, draft in enumerate(drafts):
        # Get related email if it exists
        related_email = None
        if draft.email_id:
            related_email = agent.storage.get_email_by_id(draft.email_id)
        
        # Draft card
        with st.expander(f"📧 {draft.subject}", expanded=(idx == 0)):
            # Draft metadata
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.caption(f"**Type:** {draft.draft_type or 'reply'}")
            with col2:
                st.caption(f"**Tone:** {draft.tone or 'professional'}")
            with col3:
                st.caption(f"**Created:** {draft.created_at.strftime('%Y-%m-%d %H:%M')}")
            
            # Related email context
            if related_email:
                with st.container():
                    st.markdown("**📩 In Reply To:**")
                    st.caption(f"From: {related_email.sender_name or related_email.sender}")
                    st.caption(f"Subject: {related_email.subject}")
                    
                    with st.expander("View Original Email"):
                        st.text_area("Original Email", related_email.body, height=150, key=f"original_{draft.id}", label_visibility="collapsed")
            
            st.markdown("---")
            
            # Edit mode toggle
            edit_key = f"edit_mode_{draft.id}"
            if edit_key not in st.session_state:
                st.session_state[edit_key] = False
            
            col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
            
            with col1:
                if st.button("✏️ Edit" if not st.session_state[edit_key] else "👁️ View", 
                           key=f"toggle_edit_{draft.id}", use_container_width=True):
                    st.session_state[edit_key] = not st.session_state[edit_key]
                    st.rerun()
            
            with col2:
                if st.button("📋 Copy", key=f"copy_{draft.id}", use_container_width=True):
                    # In a real app, this would copy to clipboard
                    st.success("✅ Draft copied to clipboard!")
            
            with col3:
                if st.button("🔄 Regenerate", key=f"regen_{draft.id}", use_container_width=True):
                    if related_email:
                        with st.spinner("Regenerating draft..."):
                            try:
                                reply_prompt = agent.prompt_service.get_prompt_template('auto_reply')
                                new_draft = agent.llm.generate_reply_draft(
                                    related_email.sender,
                                    related_email.subject,
                                    related_email.body,
                                    reply_prompt
                                )
                                
                                agent.storage.update_draft(
                                    draft.id,
                                    new_draft.get('subject'),
                                    new_draft.get('body')
                                )
                                st.success("✅ Draft regenerated!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Regeneration failed: {str(e)}")
                    else:
                        st.warning("Cannot regenerate - no original email context")
            
            with col4:
                if st.button("🗑️ Delete", key=f"delete_{draft.id}", use_container_width=True):
                    agent.storage.delete_draft(draft.id)
                    st.success("✅ Draft deleted!")
                    st.rerun()
            
            st.markdown("---")
            
            # Display or edit draft
            if st.session_state[edit_key]:
                # Edit mode
                st.markdown("### Edit Draft")
                
                new_subject = st.text_input(
                    "Subject",
                    value=draft.subject,
                    key=f"subject_{draft.id}"
                )
                
                new_body = st.text_area(
                    "Body",
                    value=draft.body,
                    height=400,
                    key=f"body_{draft.id}"
                )
                
                col1, col2 = st.columns([1, 3])
                with col1:
                    if st.button("💾 Save Changes", key=f"save_{draft.id}", type="primary"):
                        try:
                            agent.storage.update_draft(draft.id, new_subject, new_body)
                            st.success("✅ Draft saved!")
                            st.session_state[edit_key] = False
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to save: {str(e)}")
            else:
                # View mode
                st.markdown("### Draft Preview")
                st.markdown(f"**Subject:** {draft.subject}")
                st.markdown("**Body:**")
                st.text_area("Draft Body", draft.body, height=400, key=f"view_{draft.id}", label_visibility="collapsed", disabled=True)
            
            st.markdown("---")
            
            # Quick actions
            st.markdown("### Quick Actions")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📤 Send Options**")
                st.caption("This is a demo - emails won't actually be sent")
                st.info("In a real implementation, integrate with your email client (Gmail API, SMTP, etc.)")
            
            with col2:
                st.markdown("**💡 Suggestions**")
                if draft.tone:
                    st.caption(f"Tone: {draft.tone.title()}")
                st.caption("Consider reviewing for:")
                st.caption("• Spelling and grammar")
                st.caption("• Appropriate tone")
                st.caption("• Clear call-to-action")
    
    # Bulk actions
    st.markdown("---")
    st.subheader("🔧 Bulk Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Export All Drafts", use_container_width=True):
            # Export drafts as JSON
            import json
            export_data = []
            for draft in drafts:
                export_data.append({
                    'subject': draft.subject,
                    'body': draft.body,
                    'tone': draft.tone,
                    'type': draft.draft_type,
                    'created_at': draft.created_at.isoformat()
                })
            
            st.download_button(
                label="💾 Download JSON",
                data=json.dumps(export_data, indent=2),
                file_name="email_drafts.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("🗑️ Delete All Drafts", use_container_width=True):
            if st.session_state.get('confirm_delete_all', False):
                for draft in drafts:
                    agent.storage.delete_draft(draft.id)
                st.success("✅ All drafts deleted!")
                st.session_state.confirm_delete_all = False
                st.rerun()
            else:
                st.session_state.confirm_delete_all = True
                st.warning("⚠️ Click again to confirm deletion of all drafts")
    
    with col3:
        if st.button("📊 Draft Statistics", use_container_width=True):
            # Show statistics
            st.session_state.show_stats = True
    
    # Statistics modal
    if st.session_state.get('show_stats', False):
        with st.container():
            st.markdown("### 📊 Draft Statistics")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Drafts", len(drafts))
            
            with col2:
                reply_count = sum(1 for d in drafts if d.draft_type == 'reply')
                st.metric("Reply Drafts", reply_count)
            
            with col3:
                new_count = sum(1 for d in drafts if d.draft_type == 'new')
                st.metric("New Drafts", new_count)
            
            # Tone distribution
            tones = {}
            for draft in drafts:
                tone = draft.tone or 'unknown'
                tones[tone] = tones.get(tone, 0) + 1
            
            st.markdown("**Tone Distribution:**")
            for tone, count in tones.items():
                st.caption(f"• {tone.title()}: {count}")
            
            if st.button("Close Statistics"):
                st.session_state.show_stats = False
                st.rerun()
    
    # Help section
    with st.expander("ℹ️ How to Use Draft Manager"):
        st.markdown("""
        ### Managing Drafts
        
        - **Edit**: Modify the subject and body of any draft
        - **Copy**: Copy draft content to your clipboard
        - **Regenerate**: Create a new version using AI (requires original email)
        - **Delete**: Remove drafts you don't need
        
        ### Best Practices
        
        1. **Review Carefully**: Always review AI-generated drafts before sending
        2. **Personalize**: Add personal touches to make drafts more authentic
        3. **Check Facts**: Verify any specific details or dates mentioned
        4. **Adjust Tone**: Modify the tone to match your relationship with the recipient
        
        ### Sending Emails
        
        This is a demonstration application. To send emails:
        
        1. Copy the draft content
        2. Open your email client (Gmail, Outlook, etc.)
        3. Paste and review
        4. Send when ready
        
        **Future Enhancement**: Direct integration with Gmail API or SMTP for one-click sending!
        """)

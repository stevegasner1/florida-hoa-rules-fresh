import streamlit as st
import json

# Simple HOA Rules Lookup - Web Version
st.set_page_config(
    page_title="HOA Rules Lookup",
    page_icon="🏘️",
    layout="wide"
)

# Web banner
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 1rem;">
    <h1>🏘️ HOA Rules Lookup System</h1>
    <p>Search HOA rules with natural language queries</p>
</div>
""", unsafe_allow_html=True)

# Sample rules database
sample_rules = {
    "Sample Community": {
        "architectural": {
            "paint_colors": "Exterior paint colors must be from the approved color palette",
            "fences": "Fences must be approved and cannot exceed 6 feet in height"
        },
        "pets": {
            "registration": "All pets must be registered with the management office within 30 days",
            "leash_policy": "Dogs must be on leash at all times when outside of owner's unit"
        },
        "parking": {
            "assigned_spaces": "Each unit is assigned two parking spaces",
            "guest_parking": "Guest parking is limited to 24 hours"
        },
        "noise": {
            "quiet_hours": "Quiet hours are from 10:00 PM to 7:00 AM daily"
        },
        "rentals": {
            "short_term": "Short-term rentals of less than 30 days are prohibited"
        }
    }
}

# Search interface
st.markdown("## 🔍 Search HOA Rules")
query = st.text_input(
    "Ask a question about HOA rules:",
    placeholder="e.g., Can I paint my house blue? What are the quiet hours?"
)

# Quick buttons
st.markdown("### 🎯 Quick Searches:")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🏠 Paint Rules"):
        query = "paint colors"
with col2:
    if st.button("🐕 Pet Policies"):
        query = "pet registration leash"
with col3:
    if st.button("🚗 Parking Rules"):
        query = "parking spaces guest"
with col4:
    if st.button("🔊 Noise Rules"):
        query = "quiet hours noise"

# Search results
if query:
    st.markdown("### 📋 Search Results:")
    
    results_found = False
    query_lower = query.lower()
    
    for community, categories in sample_rules.items():
        st.markdown(f"#### 🏘️ {community}")
        
        for category, rules in categories.items():
            for rule_name, rule_content in rules.items():
                # Simple keyword matching
                if any(word in rule_content.lower() or word in category.lower() 
                      for word in query_lower.split()):
                    
                    results_found = True
                    st.markdown(f"""
                    <div style="border: 1px solid #ddd; padding: 1rem; margin: 0.5rem 0; border-radius: 8px; background: #f8f9fa;">
                        <h4>📄 {rule_name.replace('_', ' ').title()}</h4>
                        <p><strong>Category:</strong> {category.replace('_', ' ').title()}</p>
                        <p><strong>Rule:</strong> {rule_content}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    if not results_found:
        st.warning("No rules found matching your query. Try different keywords or use the quick search buttons above.")

# Footer
st.markdown("---")
st.info("""
🌐 **This is a demo HOA Rules Lookup System**
- Add your own community rules to customize
- Natural language search capabilities
- Mobile-friendly interface
- No login required - share this link with anyone!
""")

st.success("✅ **System is live and accessible to anyone with this URL!**")
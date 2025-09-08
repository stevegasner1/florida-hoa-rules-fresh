import streamlit as st

st.set_page_config(page_title="HOA Rules Lookup", page_icon="🏘️")

st.markdown("# 🏘️ HOA Rules Lookup")
st.markdown("Search HOA rules with natural language queries")

rules = {
    "paint_colors": "Exterior paint colors must be from the approved color palette",
    "fences": "Fences must be approved and cannot exceed 6 feet in height",
    "pets": "All pets must be registered with the management office within 30 days",
    "parking": "Each unit is assigned two parking spaces",
    "quiet_hours": "Quiet hours are from 10:00 PM to 7:00 AM daily"
}

st.markdown("## 🔍 Search Rules")
query = st.text_input("Ask about HOA rules:", placeholder="e.g., paint colors")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏠 Paint Rules"):
        query = "paint"
with col2:
    if st.button("🐕 Pet Rules"):
        query = "pets"
with col3:
    if st.button("🔊 Noise Rules"):
        query = "quiet"

if query:
    st.markdown("### Results:")
    found = False
    for rule_name, rule_text in rules.items():
        if query.lower() in rule_name.lower() or query.lower() in rule_text.lower():
            found = True
            st.markdown(f"**{rule_name.replace('_', ' ').title()}:** {rule_text}")
    
    if not found:
        st.warning("No rules found. Try: paint, pets, parking, quiet, or fences")

st.success("✅ App is working! Click the buttons above to test.")
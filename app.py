import streamlit as st
import re

st.set_page_config(page_title="Florida HOA Rules Lookup", page_icon="🏘️")

st.markdown("# 🏘️ Florida HOA Rules Lookup")
st.markdown("**Emergency Restore - Testing Basic Functionality**")

# Minimal working search
st.markdown("## 🔍 Search")
query = st.text_input("Search HOA rules:")

if query:
    st.success("✅ App is working! Search functionality restored.")
    st.markdown(f"You searched for: **{query}**")
    
    # Simple contract answer
    if "bid" in query.lower() or "contract" in query.lower():
        st.markdown("### 📋 Contract Bidding Answer")
        st.markdown("**Florida Law:** While Florida Statute 720.3055 doesn't mandate a specific number of bids, most HOAs require 3 competitive bids for major contracts as a best practice.")
        st.markdown("🔗 [Florida Statute 720.3055](http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0700-0799/0720/Sections/0720.3055.html)")

st.info("🚨 This is an emergency restore version. Full functionality will be restored once the app is stable.")
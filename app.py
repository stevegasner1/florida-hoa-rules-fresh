import streamlit as st

# Absolute minimal version
st.title("Florida HOA Rules Lookup")
st.write("Emergency restore version - testing basic functionality")

query = st.text_input("Search:")

if query:
    st.write(f"You searched: {query}")
    
    if "bid" in query.lower():
        st.write("Answer: Florida HOAs typically require 3 competitive bids for major contracts as best practice.")

st.write("Status: Testing minimal deployment")
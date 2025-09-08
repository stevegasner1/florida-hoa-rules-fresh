import streamlit as st
import re

st.set_page_config(page_title="Florida HOA Rules Lookup", page_icon="🏘️")

st.markdown("# 🏘️ Florida HOA Rules Lookup")
st.markdown("**Comprehensive Florida HOA search based on Florida Statute 720 and state-specific requirements**")

# FLORIDA-SPECIFIC HOA rules database with statute references and links
florida_hoa_rules = {
    # Architectural Review - Florida Specific
    "architectural_review_process_fl": {
        "content": "Per Florida Statute 720.303, architectural review applications must be approved or denied within 45 days of submission. Failure to respond within 45 days constitutes approval unless governing documents specify otherwise.",
        "statute": "720.303",
        "links": [
            ("Florida Statute 720.303", "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0700-0799/0720/Sections/0720.303.html"),
            ("CAI Florida Chapter", "https://www.caionline.org/StateChapters/Florida/Pages/default.aspx"),
            ("Florida HOA Guide", "https://www.floridabar.org/the-florida-bar-journal/")
        ]
    },
    "architectural_review_requirements_fl": {
        "content": "Florida law requires architectural committees to follow written standards and provide written reasons for denials. All exterior modifications require approval before commencement of work.",
        "statute": "720.303",
        "links": [
            ("Florida Statute 720.303", "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0700-0799/0720/Sections/0720.303.html"),
            ("Architectural Review Best Practices", "https://www.caionline.org/"),
            ("FL Division of Real Estate", "https://www.myfloridalicense.com/dbpr/re/")
        ]
    },
    
    # Rental Policies - Florida Specific Laws
    "short_term_rentals_fl": {
        "content": "Florida Statute 720.3075 allows HOAs to restrict rentals of 30 days or less. Many Florida HOAs prohibit Airbnb, VRBO, and vacation rentals to maintain residential character.",
        "statute": "720.3075",
        "links": [
            ("Florida Statute 720.3075", "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0700-0799/0720/Sections/0720.3075.html"),
            ("Short-Term Rental Laws", "https://www.caionline.org/"),
            ("Florida Tourism Industry", "https://www.visitflorida.com/")
        ]
    },
    "long_term_rentals_fl": {
        "content": "Florida HOAs may restrict rentals but cannot completely prohibit them unless specified in original recorded documents. Rental caps are limited by Florida Statute 720.3075.",
        "statute": "720.3075",
        "links": [
            ("Florida Statute 720.3075", "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0700-0799/0720/Sections/0720.3075.html"),
            ("Rental Restriction Guidelines", "https://www.caionline.org/"),
            ("Florida Fair Housing", "https://www.myflorida.com/")
        ]
    },
    
    # Reserve Funds - Florida Requirements
    "reserve_fund_requirements_fl": {
        "content": "Florida Statute 720.303 requires HOAs to maintain reserve accounts for roof replacement, building painting, pavement resurfacing, and other major components with useful lives exceeding one year.",
        "statute": "720.303",
        "links": [
            ("Florida Statute 720.303", "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0700-0799/0720/Sections/0720.303.html"),
            ("Reserve Study Guidelines", "https://www.caionline.org/"),
            ("Florida CPA Requirements", "https://www.ficpa.org/")
        ]
    },
    "reserve_study_mandate_fl": {
        "content": "Florida law mandates reserve studies be updated at least every five years by licensed professionals, with annual adjustments for inflation and component condition changes.",
        "statute": "720.303",
        "links": [
            ("Florida Statute 720.303", "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0700-0799/0720/Sections/0720.303.html"),
            ("Reserve Study Professionals", "https://www.apra-usa.com/"),
            ("Florida Engineering Society", "https://www.fleng.org/")
        ]
    },
    
    # Board Governance - Florida Statute 720
    "board_meetings_fl": {
        "content": "Florida law requires 48-hour advance notice for board meetings, with emergency meetings allowed for urgent matters affecting health, safety, or significant financial issues.",
        "statute": "720.306",
        "links": [
            ("Florida Statute 720.306", "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0700-0799/0720/Sections/0720.306.html"),
            ("Government in Sunshine Law", "https://www.myflorida.com/myflorida/government/governmentinformation/sunshine_law.html"),
            ("Meeting Notice Requirements", "https://www.caionline.org/")
        ]
    },
    "board_quorum_fl": {
        "content": "Florida Statute 720.306 requires a majority of board members present to constitute quorum for conducting official business and making binding decisions.",
        "statute": "720.306",
        "links": [
            ("Florida Statute 720.306", "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0700-0799/0720/Sections/0720.306.html"),
            ("Board Governance Guide", "https://www.caionline.org/"),
            ("Roberts Rules of Order", "https://robertsrules.org/")
        ]
    },
    
    # Financial Reporting - Florida Requirements
    "annual_financial_reporting_fl": {
        "content": "Florida Statute 720.303 requires annual financial statements within 90 days of fiscal year end, with compilation, review, or audit requirements based on community budget size.",
        "statute": "720.303",
        "links": [
            ("Florida Statute 720.303", "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0700-0799/0720/Sections/0720.303.html"),
            ("Florida CPA Society", "https://www.ficpa.org/"),
            ("Financial Reporting Standards", "https://www.caionline.org/")
        ]
    },
    "cpa_requirements_fl": {
        "content": "Florida mandates CPA preparation of financial statements: compilation for budgets $150K-$300K, review for $300K-$500K, audit for budgets exceeding $500K annually.",
        "statute": "720.303",
        "links": [
            ("Florida Statute 720.303", "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0700-0799/0720/Sections/0720.303.html"),
            ("Find a CPA in Florida", "https://www.ficpa.org/"),
            ("Audit vs Review vs Compilation", "https://www.aicpa.org/")
        ]
    },
    
    # Insurance and Hurricane Requirements - Florida Specific  
    "hurricane_preparation_fl": {
        "content": "Florida HOAs must maintain hurricane preparedness plans including evacuation procedures, emergency contacts, and post-storm damage assessment protocols.",
        "statute": "General Florida Law",
        "links": [
            ("Florida Emergency Management", "https://www.floridadisaster.org/"),
            ("Hurricane Preparedness Guide", "https://www.nhc.noaa.gov/prepare/"),
            ("Insurance Institute for Business", "https://www.iiaba.net/")
        ]
    },
    "windstorm_insurance_fl": {
        "content": "Florida law requires HOAs to maintain windstorm insurance coverage adequate for full replacement cost, with specific requirements for hurricane-prone coastal areas.",
        "statute": "Florida Insurance Code",
        "links": [
            ("Florida Office of Insurance Regulation", "https://www.floir.com/"),
            ("Citizens Property Insurance", "https://www.citizensfla.com/"),
            ("Florida Insurance Requirements", "https://www.myflorida.com/")
        ]
    },
    
    # Water Management - Florida Specific
    "water_conservation_fl": {
        "content": "Florida water conservation follows local Water Management District regulations, with mandatory restrictions during drought conditions and year-round efficiency requirements.",
        "statute": "Water Management District Rules",
        "links": [
            ("South Florida Water Management", "https://www.sfwmd.gov/"),
            ("Southwest Florida Water Management", "https://www.swfwmd.state.fl.us/"),
            ("St. Johns River Water Management", "https://www.sjrwmd.com/")
        ]
    },
    "florida_friendly_landscaping": {
        "content": "Florida-Friendly Landscaping principles are encouraged statewide, emphasizing native plants, efficient irrigation, and reduced chemical fertilizer use.",
        "statute": "Environmental Guidelines",
        "links": [
            ("Florida-Friendly Landscaping", "https://ffl.ifas.ufl.edu/"),
            ("UF/IFAS Extension", "https://sfyl.ifas.ufl.edu/"),
            ("Native Plant Society of Florida", "https://www.fnps.org/")
        ]
    },
    
    # Violation and Enforcement - Florida Procedures
    "violation_notice_requirements_fl": {
        "content": "Florida Statute 720.305 requires specific violation notice procedures including 14-day cure period for most violations before fines can be imposed.",
        "statute": "720.305",
        "links": [
            ("Florida Statute 720.305", "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0700-0799/0720/Sections/0720.305.html"),
            ("Violation Enforcement Guide", "https://www.caionline.org/"),
            ("Due Process Requirements", "https://www.floridabar.org/")
        ]
    },
    "fine_hearing_process_fl": {
        "content": "Florida mandates impartial hearing panels for violations with fines, separate from boards that imposed violations, with specific notice and hearing rights.",
        "statute": "720.305",
        "links": [
            ("Florida Statute 720.305", "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0700-0799/0720/Sections/0720.305.html"),
            ("Hearing Committee Guidelines", "https://www.caionline.org/"),
            ("Florida Administrative Procedures", "https://www.myflorida.com/")
        ]
    },
    
    # Disclosure Requirements - Florida Specific
    "sales_disclosure_fl": {
        "content": "Florida Statute 720.401 requires specific HOA disclosures to prospective buyers including financial statements, budgets, meeting minutes, and governing documents.",
        "statute": "720.401",
        "links": [
            ("Florida Statute 720.401", "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0700-0799/0720/Sections/0720.401.html"),
            ("Real Estate Disclosure Guide", "https://www.myfloridalicense.com/"),
            ("Florida Realtors Association", "https://www.floridarealtors.org/")
        ]
    },
    "estoppel_certificate_fl": {
        "content": "Florida law requires HOAs to provide estoppel certificates within 15 days of request, detailing all amounts owed by unit owners for closing purposes.",
        "statute": "720.401",
        "links": [
            ("Florida Statute 720.401", "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0700-0799/0720/Sections/0720.401.html"),
            ("Estoppel Certificate Guide", "https://www.caionline.org/"),
            ("Title Insurance Requirements", "https://www.flta.org/")
        ]
    }
}

st.markdown("## 🔍 Search Florida HOA Laws and Rules")
query = st.text_input(
    "Ask any question about Florida HOA laws and regulations:",
    placeholder="e.g., Florida reserve requirements, architectural review timeline, rental restrictions"
)

# Florida-focused search function (same as before)
def search_florida_hoa_rules(search_query):
    if not search_query:
        return []
    
    results = []
    search_terms = search_query.lower().strip()
    query_words = re.findall(r'\b\w+\b', search_terms)
    
    for rule_id, rule_data in florida_hoa_rules.items():
        score = 0
        rule_content = rule_data["content"]
        rule_lower = rule_content.lower()
        rule_name_lower = rule_id.lower()
        
        # Boost for Florida statute references
        if 'florida statute' in rule_lower or 'florida law' in rule_lower:
            score += 20
        
        # Exact phrase matching (highest score)
        if search_terms in rule_lower or search_terms in rule_name_lower:
            score += 100
        
        # Multi-word phrase matching
        if len(query_words) > 1:
            for i in range(len(query_words) - 1):
                phrase = f"{query_words[i]} {query_words[i+1]}"
                if phrase in rule_lower or phrase in rule_name_lower:
                    score += 60
        
        # Individual word matching
        word_matches = 0
        for word in query_words:
            if len(word) > 2:
                if word in rule_lower:
                    word_matches += 1
                    score += 18
                if word in rule_name_lower:
                    word_matches += 1
                    score += 25
        
        # Bonus for multiple matches
        if word_matches > 1:
            score += word_matches * 12
        
        # Florida-specific synonym boosting (same as before)
        florida_synonyms = {
            'architectural': ['review', 'modification', 'approval', 'committee', '720.303'],
            'rental': ['lease', 'tenant', 'airbnb', 'vrbo', '720.3075'],
            'reserve': ['fund', 'study', 'component', 'replacement', '720.303'],
            'board': ['director', 'meeting', 'quorum', 'election', '720.306'],
            'financial': ['budget', 'assessment', 'audit', 'cpa', '720.303'],
            'violation': ['fine', 'hearing', 'enforcement', 'lien', '720.305'],
            'insurance': ['hurricane', 'windstorm', 'flood', 'deductible'],
            'disclosure': ['estoppel', 'sales', 'financial', '720.401']
        }
        
        for main_word, related_words in florida_synonyms.items():
            if main_word in query_words:
                for related in related_words:
                    if related in rule_lower or related in rule_name_lower:
                        score += 22
        
        # Add result if matches found
        if score > 0:
            results.append({
                'rule_id': rule_id,
                'rule_data': rule_data,
                'score': score,
                'title': rule_id.replace('_fl', '').replace('_', ' ').title(),
                'florida_specific': 'florida statute' in rule_lower or 'florida law' in rule_lower
            })
    
    # Sort by score (highest first)
    results.sort(key=lambda x: x['score'], reverse=True)
    return results

# Florida-specific topic buttons (same as before)
st.markdown("### 🎯 Florida HOA Law Topics:")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📜 FL Statute 720"):
        query = "florida statute 720 requirements"
with col2:
    if st.button("🏗️ Architectural FL"):
        query = "florida architectural review 45 days"
with col3:
    if st.button("🏠 FL Rental Laws"):
        query = "florida rental restrictions 720.3075"
with col4:
    if st.button("💰 FL Reserve Rules"):
        query = "florida reserve fund requirements 720.303"

col5, col6, col7, col8 = st.columns(4)

with col5:
    if st.button("🏛️ FL Board Rules"):
        query = "florida board meetings quorum 720.306"
with col6:
    if st.button("📊 FL Financial Laws"):
        query = "florida financial reporting audit requirements"
with col7:
    if st.button("⚖️ FL Violations"):
        query = "florida violation fines hearing 720.305"
with col8:
    if st.button("🌀 FL Hurricane/Insurance"):
        query = "florida hurricane windstorm insurance"

# Display search results with enhanced links
if query:
    results = search_florida_hoa_rules(query)
    
    if results:
        st.markdown(f"### 📋 Found {len(results)} Florida HOA Results for: '{query}'")
        
        for i, result in enumerate(results[:6], 1):
            rule_data = result['rule_data']
            
            # Enhanced relevance indicators
            if result['score'] >= 80:
                relevance = "🔥 High Relevance"
                color = "#d4edda"
            elif result['score'] >= 50:
                relevance = "⭐ Medium Relevance"  
                color = "#fff3cd"
            else:
                relevance = "💡 Related"
                color = "#f8f9fa"
            
            # Special indicator for statute references
            statute_indicator = " 📜" if result['florida_specific'] else ""
            
            # Create links section
            links_html = ""
            for link_text, link_url in rule_data['links']:
                links_html += f'<a href="{link_url}" target="_blank" style="margin-right: 15px; color: #007bff; text-decoration: none;">🔗 {link_text}</a>'
            
            st.markdown(f"""
            <div style="border: 1px solid #ddd; padding: 1.3rem; margin: 0.8rem 0; border-radius: 12px; background: {color}; box-shadow: 0 3px 6px rgba(0,0,0,0.1);">
                <h4 style="margin: 0 0 0.8rem 0; color: #2c3e50;">📄 {result['title']}{statute_indicator} <small style="color: #666; font-weight: normal;">({relevance})</small></h4>
                <p style="font-size: 1.05em; line-height: 1.7; margin: 0 0 1rem 0; color: #34495e;"><strong>Florida Law:</strong> {rule_data['content']}</p>
                <div style="border-top: 1px solid #ddd; padding-top: 0.8rem; margin-top: 0.8rem;">
                    <p style="margin: 0 0 0.5rem 0; font-weight: bold; color: #495057;">📚 Additional Resources:</p>
                    <div style="font-size: 0.9em; line-height: 1.5;">
                        {links_html}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        if len(results) > 6:
            st.info(f"Showing top 6 of {len(results)} Florida HOA results. Try more specific terms for better matches.")
    else:
        st.warning(f"No Florida HOA rules found for '{query}'. Try different keywords or use the Florida topic buttons above.")
        st.info("""
        **💡 Florida HOA Search Tips:**
        - **Statutes:** Try "Florida Statute 720.303", "720.306", "720.3075"
        - **Specific Laws:** "architectural review Florida", "reserve requirements FL"
        - **State Topics:** "Florida hurricane insurance", "water management district"
        - **Legal References:** "violation hearing Florida", "disclosure requirements FL"
        """)

# Florida-specific comprehensive footer (same as before)
st.markdown("---")
with st.expander("📜 Complete Florida HOA Law Coverage - Click to Expand"):
    st.markdown("""
    **🏗️ Architectural Review (FL Statute 720.303):** 45-day approval timeline, written standards, appeal rights
    
    **🏠 Rental Restrictions (FL Statute 720.3075):** Short-term prohibitions, rental caps, tenant rights
    
    **💰 Reserve Funds (FL Statute 720.303):** Mandatory components, 5-year studies, waiver procedures
    
    **🏛️ Board Governance (FL Statute 720.306):** Elections, meetings, quorum, Sunshine Law requirements
    
    **📊 Financial Reporting:** Annual statements, CPA requirements, budget adoption under Florida law
    
    **🌀 Insurance Requirements:** Hurricane, windstorm, flood coverage specific to Florida
    
    **💧 Water Management:** Conservation districts, irrigation restrictions, Florida-Friendly landscaping
    
    **⚖️ Violations (FL Statute 720.305):** Notice requirements, hearing rights, fine limitations
    
    **📄 Disclosure Laws (FL Statute 720.401):** Sales disclosures, estoppel certificates, document access
    
    **Plus:** All results include direct links to Florida statutes and additional resources
    """)

st.success("✅ **Florida-specific HOA search with direct links to statutes and resources!**")
st.info("🔗 **Each result includes clickable links to dig deeper into Florida laws and guidelines.**")
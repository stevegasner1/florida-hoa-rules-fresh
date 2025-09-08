import streamlit as st
import re

st.set_page_config(page_title="Florida HOA Rules Lookup", page_icon="🏘️")

st.markdown("# 🏘️ Florida HOA Rules Lookup")
st.markdown("**Comprehensive Florida HOA search based on Florida Statute 720 and state-specific requirements**")

# FLORIDA-SPECIFIC HOA rules database with statute references
florida_hoa_rules = {
    # Architectural Review - Florida Specific
    "architectural_review_process_fl": "Per Florida Statute 720.303, architectural review applications must be approved or denied within 45 days of submission. Failure to respond within 45 days constitutes approval unless governing documents specify otherwise.",
    "architectural_review_requirements_fl": "Florida law requires architectural committees to follow written standards and provide written reasons for denials. All exterior modifications require approval before commencement of work.",
    "architectural_appeal_process_fl": "Appeals of architectural decisions must be handled according to Florida Statute 720.303, with owners having the right to appear before the board and receive written explanations of denials.",
    "architectural_committee_authority_fl": "Architectural Review Committees in Florida must operate within the scope defined in governing documents and cannot impose standards not specified in recorded documents.",
    
    # Rental Policies - Florida Specific Laws
    "short_term_rentals_fl": "Florida Statute 720.3075 allows HOAs to restrict rentals of 30 days or less. Many Florida HOAs prohibit Airbnb, VRBO, and vacation rentals to maintain residential character.",
    "long_term_rentals_fl": "Florida HOAs may restrict rentals but cannot completely prohibit them unless specified in original recorded documents. Rental caps are limited by Florida Statute 720.3075.",
    "rental_approval_process_fl": "Per Florida law, HOAs may require rental approval but cannot charge application fees exceeding actual costs of background checks and processing.",
    "tenant_rights_fl": "Florida Statute 720.3075 grants tenants the same rights as owners regarding use of common areas and participation in meetings, except voting rights.",
    "rental_violations_fl": "Florida law holds both landlords and tenants responsible for HOA violations, with specific notice and hearing requirements before fines can be imposed.",
    
    # Property Rights and Easements - Florida Law
    "easements_florida_law": "Florida easements are governed by recorded plat maps and declarations. Utility easements typically include electric, water, sewer, cable, and telecommunications access rights.",
    "property_boundaries_fl": "Florida property boundaries are established by recorded surveys and cannot be altered without legal action. Survey disputes require licensed Florida surveyor resolution.",
    "common_area_definitions_fl": "Florida Statute 720.301 defines common areas as property owned by the association for use by all members, including recreational facilities, roads, and landscaped areas.",
    "limited_common_elements_fl": "Limited common elements in Florida are defined as common areas designated for exclusive use by specific units, such as assigned parking spaces or patios.",
    "easement_maintenance_fl": "Florida law requires HOAs to maintain utility easements and allows utility companies access for repairs and upgrades without additional owner consent.",
    
    # Reserve Funds - Florida Requirements
    "reserve_fund_requirements_fl": "Florida Statute 720.303 requires HOAs to maintain reserve accounts for roof replacement, building painting, pavement resurfacing, and other major components with useful lives exceeding one year.",
    "reserve_study_mandate_fl": "Florida law mandates reserve studies be updated at least every five years by licensed professionals, with annual adjustments for inflation and component condition changes.",
    "reserve_fund_waiver_fl": "Florida allows membership to waive or reduce reserve funding annually by majority vote, but waiver must be disclosed in budget and meeting minutes.",
    "reserve_fund_usage_restrictions_fl": "Per Florida Statute 720.303, reserve funds can only be used for their designated purposes unless membership approves alternative use by majority vote.",
    "reserve_fund_pooling_fl": "Florida HOAs may pool reserve funds for efficiency but must maintain separate accounting for each component category as required by state law.",
    
    # Board Governance - Florida Statute 720
    "board_composition_fl": "Florida Statute 720.306 requires boards of at least 3 members, with specific election procedures and term limits as defined in governing documents.",
    "board_meetings_fl": "Florida law requires 48-hour advance notice for board meetings, with emergency meetings allowed for urgent matters affecting health, safety, or significant financial issues.",
    "board_quorum_fl": "Florida Statute 720.306 requires a majority of board members present to constitute quorum for conducting official business and making binding decisions.",
    "open_meeting_requirements_fl": "Florida's Government in Sunshine Law applies to HOA board meetings, requiring most meetings be open to members with limited exceptions for personnel and legal matters.",
    "board_election_process_fl": "Florida Statute 720.306 mandates specific election procedures including candidate information sheets, secret ballots, and independent election supervisors for communities over 1,000 units.",
    
    # Financial Reporting - Florida Requirements
    "annual_financial_reporting_fl": "Florida Statute 720.303 requires annual financial statements within 90 days of fiscal year end, with compilation, review, or audit requirements based on community budget size.",
    "budget_adoption_process_fl": "Florida HOAs must adopt budgets at least 14 days before fiscal year begins, with membership notification and opportunity to object to proposed budgets.",
    "assessment_collection_fl": "Florida Statute 720.3085 provides HOAs with collection rights including liens, foreclosure, and attorney fees, with specific notice requirements before legal action.",
    "financial_records_access_fl": "Florida law grants members right to inspect financial records during business hours with 5-day written notice, including contracts, invoices, and bank statements.",
    "cpa_requirements_fl": "Florida mandates CPA preparation of financial statements: compilation for budgets $150K-$300K, review for $300K-$500K, audit for budgets exceeding $500K annually.",
    
    # Insurance and Hurricane Requirements - Florida Specific  
    "hurricane_preparation_fl": "Florida HOAs must maintain hurricane preparedness plans including evacuation procedures, emergency contacts, and post-storm damage assessment protocols.",
    "windstorm_insurance_fl": "Florida law requires HOAs to maintain windstorm insurance coverage adequate for full replacement cost, with specific requirements for hurricane-prone coastal areas.",
    "flood_insurance_requirements_fl": "Florida HOAs in flood zones must maintain appropriate flood insurance coverage and inform owners of individual unit flood insurance responsibilities.",
    "insurance_deductible_responsibility_fl": "Florida Statute 720.3085 allows HOAs to assess insurance deductibles to responsible unit owners, with specific notice and hearing requirements.",
    "property_insurance_coverage_fl": "Florida requires HOA master policies to cover all common areas, building exteriors, and infrastructure with coverage amounts meeting replacement cost standards.",
    
    # Water Management - Florida Specific
    "water_conservation_fl": "Florida water conservation follows local Water Management District regulations, with mandatory restrictions during drought conditions and year-round efficiency requirements.",
    "irrigation_restrictions_fl": "Florida irrigation is typically restricted to 2-3 days per week depending on local water management district rules, with seasonal adjustments for rainfall.",
    "florida_friendly_landscaping": "Florida-Friendly Landscaping principles are encouraged statewide, emphasizing native plants, efficient irrigation, and reduced chemical fertilizer use.",
    "stormwater_management_fl": "Florida HOAs must comply with stormwater management requirements including retention pond maintenance and water quality monitoring.",
    "well_water_regulations_fl": "Private wells in Florida HOAs require permits from local health departments and regular water quality testing for potability and safety.",
    
    # Bidding and Contracting - Florida Law
    "competitive_bidding_fl": "Florida Statute 720.3055 requires competitive bidding for contracts exceeding amounts specified in governing documents, typically $1,000-$5,000 depending on community size.",
    "contractor_licensing_fl": "All contractors working in Florida HOAs must hold appropriate state licensing, workers compensation insurance, and general liability coverage as required by state law.",
    "public_records_contracts_fl": "Florida HOA contracts are subject to public records laws, allowing member inspection of vendor agreements, specifications, and payment terms.",
    "emergency_contracting_fl": "Florida allows emergency contracts without bidding for health, safety, or security issues, but requires board ratification and documentation within 30 days.",
    "vendor_selection_criteria_fl": "Florida law permits HOAs to consider factors beyond lowest bid including contractor qualifications, references, and past performance in similar communities.",
    
    # Violation and Enforcement - Florida Procedures
    "violation_notice_requirements_fl": "Florida Statute 720.305 requires specific violation notice procedures including 14-day cure period for most violations before fines can be imposed.",
    "fine_hearing_process_fl": "Florida mandates impartial hearing panels for violations with fines, separate from boards that imposed violations, with specific notice and hearing rights.",
    "fine_limitations_fl": "Florida limits HOA fines to amounts specified in governing documents, typically $100 per violation with $1,000 aggregate limit unless documents specify higher amounts.",
    "lien_and_foreclosure_fl": "Florida Statute 720.3085 grants HOAs lien rights for unpaid assessments and fines, with specific foreclosure procedures and owner redemption rights.",
    "covenant_enforcement_fl": "Florida requires good faith enforcement of covenants with consistent application and cannot selectively enforce restrictions against specific owners.",
    
    # Disclosure Requirements - Florida Specific
    "sales_disclosure_fl": "Florida Statute 720.401 requires specific HOA disclosures to prospective buyers including financial statements, budgets, meeting minutes, and governing documents.",
    "estoppel_certificate_fl": "Florida law requires HOAs to provide estoppel certificates within 15 days of request, detailing all amounts owed by unit owners for closing purposes.",
    "financial_disclosure_fl": "Florida mandates disclosure of reserve funding status, special assessments, pending litigation, and major capital improvements planned within next two years.",
    "governing_documents_access_fl": "Florida requires HOAs to maintain current governing documents and make them available to members and prospective purchasers upon request.",
    
    # Meeting and Voting - Florida Requirements
    "annual_meeting_requirements_fl": "Florida Statute 720.306 requires annual membership meetings for director elections and community business, with specific notice and quorum requirements.",
    "proxy_voting_rules_fl": "Florida allows proxy voting for HOA matters with specific form requirements and limitations on proxy holder representation numbers.",
    "secret_ballot_voting_fl": "Florida requires secret ballot voting for board elections and certain community decisions, with independent vote counting and result certification.",
    "meeting_minutes_requirements_fl": "Florida law requires detailed meeting minutes including all motions, votes, and decisions, available for member inspection within specified timeframes.",
    
    # Additional Florida-Specific Rules
    "tree_protection_fl": "Florida communities may have local tree protection ordinances requiring permits for removal of trees exceeding specified size thresholds.",
    "noise_ordinances_fl": "Florida noise regulations vary by municipality but typically include quiet hours between 10 PM and 7 AM with specific decibel limitations.",
    "pool_safety_fl": "Florida pool safety requirements include specific fencing, gate, and safety equipment standards under state and local health department regulations.",
    "cable_satellite_fl": "Florida follows FCC rules allowing owners to install satellite dishes and antennas on exclusive-use areas with HOA architectural approval for common area installations.",
    "solar_panel_rights_fl": "Florida Statute 163.04 limits HOA authority to restrict solar installations, requiring reasonable restrictions that don't impair efficiency or increase costs significantly."
}

st.markdown("## 🔍 Search Florida HOA Laws and Rules")
query = st.text_input(
    "Ask any question about Florida HOA laws and regulations:",
    placeholder="e.g., Florida reserve requirements, architectural review timeline, rental restrictions"
)

# Florida-focused search function
def search_florida_hoa_rules(search_query):
    if not search_query:
        return []
    
    results = []
    search_terms = search_query.lower().strip()
    
    # Enhanced Florida-specific keyword processing
    query_words = re.findall(r'\b\w+\b', search_terms)
    
    for rule_id, rule_text in florida_hoa_rules.items():
        score = 0
        rule_lower = rule_text.lower()
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
        
        # Florida-specific synonym and keyword boosting
        florida_synonyms = {
            'architectural': ['review', 'modification', 'approval', 'committee', '720.303'],
            'rental': ['lease', 'tenant', 'airbnb', 'vrbo', '720.3075'],
            'reserve': ['fund', 'study', 'component', 'replacement', '720.303'],
            'board': ['director', 'meeting', 'quorum', 'election', '720.306'],
            'financial': ['budget', 'assessment', 'audit', 'cpa', '720.303'],
            'violation': ['fine', 'hearing', 'enforcement', 'lien', '720.305'],
            'insurance': ['hurricane', 'windstorm', 'flood', 'deductible'],
            'water': ['conservation', 'irrigation', 'management', 'district'],
            'bidding': ['contract', 'vendor', 'competitive', '720.3055'],
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
                'rule_text': rule_text,
                'score': score,
                'title': rule_id.replace('_fl', '').replace('_', ' ').title(),
                'florida_specific': 'florida statute' in rule_lower or 'florida law' in rule_lower
            })
    
    # Sort by score (highest first)
    results.sort(key=lambda x: x['score'], reverse=True)
    return results

# Florida-specific topic buttons
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

col9, col10, col11, col12 = st.columns(4)

with col9:
    if st.button("💧 FL Water Laws"):
        query = "florida water conservation management district"
with col10:
    if st.button("📋 FL Bidding Rules"):
        query = "florida competitive bidding 720.3055"
with col11:
    if st.button("📄 FL Disclosure Laws"):
        query = "florida sales disclosure estoppel 720.401"
with col12:
    if st.button("🗳️ FL Voting Rules"):
        query = "florida election proxy secret ballot"

# Display search results with Florida context
if query:
    results = search_florida_hoa_rules(query)
    
    if results:
        st.markdown(f"### 📋 Found {len(results)} Florida HOA Results for: '{query}'")
        
        for i, result in enumerate(results[:6], 1):
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
            
            st.markdown(f"""
            <div style="border: 1px solid #ddd; padding: 1.3rem; margin: 0.8rem 0; border-radius: 12px; background: {color}; box-shadow: 0 3px 6px rgba(0,0,0,0.1);">
                <h4 style="margin: 0 0 0.8rem 0; color: #2c3e50;">📄 {result['title']}{statute_indicator} <small style="color: #666; font-weight: normal;">({relevance})</small></h4>
                <p style="font-size: 1.05em; line-height: 1.7; margin: 0; color: #34495e;"><strong>Florida Law:</strong> {result['rule_text']}</p>
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

# Florida-specific comprehensive footer
st.markdown("---")
with st.expander("📜 Complete Florida HOA Law Coverage - Click to Expand"):
    st.markdown("""
    **🏗️ Architectural Review (FL Statute 720.303):** 45-day approval timeline, written standards, appeal rights
    
    **🏠 Rental Restrictions (FL Statute 720.3075):** Short-term prohibitions, rental caps, tenant rights
    
    **📍 Property Rights:** Easements, boundaries, common areas, limited common elements under Florida law
    
    **💰 Reserve Funds (FL Statute 720.303):** Mandatory components, 5-year studies, waiver procedures
    
    **🏛️ Board Governance (FL Statute 720.306):** Elections, meetings, quorum, Sunshine Law requirements
    
    **📊 Financial Reporting:** Annual statements, CPA requirements, budget adoption under Florida law
    
    **🌀 Insurance Requirements:** Hurricane, windstorm, flood coverage specific to Florida
    
    **💧 Water Management:** Conservation districts, irrigation restrictions, Florida-Friendly landscaping
    
    **📋 Bidding Laws (FL Statute 720.3055):** Competitive bidding thresholds, contractor licensing
    
    **⚖️ Violations (FL Statute 720.305):** Notice requirements, hearing rights, fine limitations
    
    **📄 Disclosure Laws (FL Statute 720.401):** Sales disclosures, estoppel certificates, document access
    
    **🗳️ Voting Requirements:** Elections, proxies, secret ballots, meeting procedures
    
    **Plus:** Tree protection, noise ordinances, pool safety, cable/satellite rights, solar panel protections
    """)

st.success("✅ **Florida-specific HOA search based on FL Statute 720 and state requirements!**")
st.info("🏛️ **All results include relevant Florida statute references and state-specific legal requirements.**")
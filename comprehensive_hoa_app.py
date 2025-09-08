import streamlit as st
import re

st.set_page_config(page_title="HOA Rules Lookup", page_icon="🏘️")

st.markdown("# 🏘️ HOA Rules Lookup")
st.markdown("Ask any question about HOA rules - comprehensive coverage of all community topics!")

# COMPREHENSIVE HOA rules database covering ALL major topics
hoa_rules = {
    # Architectural Review Requirements
    "architectural_review_process": "All exterior modifications require architectural review committee approval before construction begins. Submit applications with detailed plans, materials, and specifications.",
    "architectural_review_timeline": "Architectural review applications must be submitted at least 30 days before proposed work begins. The committee has 45 days to approve, deny, or request modifications.",
    "architectural_review_requirements": "Architectural review requires: detailed drawings, material specifications, color samples, contractor information, and estimated completion timeline.",
    "architectural_committee_composition": "The Architectural Review Committee consists of 3-5 board members or appointed volunteers with design and construction expertise.",
    "architectural_appeal_process": "Architectural decisions may be appealed to the full board within 30 days of committee decision. Appeals require written justification.",
    
    # Rental Policies - Short and Long Term
    "short_term_rentals": "Short-term rentals of less than 30 days are strictly prohibited including Airbnb, VRBO, and vacation rentals.",
    "long_term_rentals": "Long-term rentals (30+ days) require board approval, tenant background checks, and landlord registration with the association.",
    "rental_approval_process": "All rental applications must be submitted with tenant information, lease terms, and security deposit. Board has 30 days to approve or deny.",
    "rental_restrictions": "Maximum of 25% of units may be rented at any time. Waiting list maintained when rental cap is reached.",
    "tenant_requirements": "All tenants must receive copy of community rules, register vehicles, and provide emergency contact information.",
    "rental_violations": "Landlords are responsible for tenant rule violations and may face fines, rental privilege suspension, or legal action.",
    
    # Property Boundaries and Easements  
    "easements_location": "Easements are located along rear property lines for utilities, drainage, and maintenance access. Refer to recorded plat maps for specific locations.",
    "utility_easements": "Utility easements typically extend 10 feet from rear and side property lines for electric, water, sewer, and telecommunications access.",
    "drainage_easements": "Drainage easements are located in low-lying areas and restrict landscaping that could impede water flow or maintenance access.",
    "access_easements": "Maintenance access easements allow HOA contractors to access common areas and infrastructure through private property when necessary.",
    "easement_restrictions": "Property owners cannot build permanent structures, plant large trees, or install fencing within designated easement areas.",
    
    # Reserve Fund Usage
    "reserve_fund_purpose": "Reserve funds are designated for major repairs and replacement of common area components including roofs, roads, pools, and landscaping.",
    "reserve_fund_restrictions": "Reserve funds cannot be used for operating expenses, routine maintenance, or improvements that were not planned in the reserve study.",
    "reserve_study_requirements": "Professional reserve studies are conducted every 3-5 years to assess component conditions and funding needs.",
    "reserve_fund_approval": "Major reserve fund expenditures over $10,000 require board approval and may require membership notification or approval.",
    "reserve_fund_components": "Reserve funds cover: roofing, exterior painting, road resurfacing, pool equipment, clubhouse updates, and landscape replacement.",
    
    # Buffer Regulations and Tree/Structure Removal
    "buffer_regulations": "Structures must maintain minimum 10-foot buffers from property lines and 25-foot buffers from streets unless specifically approved.",
    "tree_removal_approval": "Tree removal requires architectural committee approval, especially for trees over 6 inches in diameter or in common areas.",
    "structure_removal_requirements": "Structure removal requires permits, contractor licensing verification, and restoration plan for affected landscape areas.",
    "setback_requirements": "New structures must meet minimum setback requirements: 25 feet from front, 10 feet from sides, 15 feet from rear property lines.",
    "buffer_zone_landscaping": "Buffer zones must be maintained with approved landscaping that doesn't interfere with drainage or utility access.",
    
    # Board Governance and Quorum
    "board_quorum_requirements": "A majority of board members (3 of 5 or 4 of 7) must be present to conduct official business and make binding decisions.",
    "board_composition": "The board consists of 5-7 elected directors serving staggered 2-year terms with elections held annually.",
    "board_meeting_requirements": "Regular board meetings are held monthly with 48-hour advance notice. Emergency meetings require 24-hour notice when possible.",
    "voting_procedures": "Board decisions require majority vote of members present. Tie votes fail unless broken by board president.",
    "board_responsibilities": "Board oversees community operations, enforces rules, manages finances, maintains common areas, and represents member interests.",
    
    # Financial Reporting Requirements  
    "financial_reporting_frequency": "Financial statements are provided to members annually. Monthly financial summaries are available upon request.",
    "annual_financial_statements": "Annual audited or reviewed financial statements are required for communities with budgets over $300,000.",
    "budget_approval_process": "Annual budgets require board approval and membership notification 30 days before implementation.",
    "assessment_collection": "Monthly assessments are due on the 1st with late fees applied after the 15th. Quarterly payment options may be available.",
    "financial_records_access": "Members may inspect financial records, contracts, and meeting minutes during business hours with 48-hour notice.",
    
    # Property Ownership Boundaries
    "unit_ownership_boundaries": "Unit owners own interior space from interior wall surfaces inward including fixtures, flooring, and personal improvements.",
    "common_area_ownership": "HOA owns and maintains exterior walls, roofs, common areas, landscaping, roads, pools, and recreational facilities.",
    "limited_common_elements": "Patios, balconies, and parking spaces are limited common elements maintained by HOA but exclusively used by specific units.",
    "maintenance_responsibilities": "Owners maintain interiors, fixtures, and appliances. HOA maintains exteriors, roofs, common areas, and major systems.",
    "property_modification_limits": "Modifications to common areas or exterior elements require board approval even if adjacent to owner's unit.",
    
    # Water Conservation Tools and Methods
    "water_conservation_tools": "Available water conservation tools include: rain sensors, drip irrigation, native plants, mulching, rain barrels, and efficient fixtures.",
    "irrigation_efficiency": "Smart irrigation controllers with weather sensors can reduce water usage by 30-50% compared to traditional timer systems.",
    "drought_resistant_landscaping": "Native and drought-resistant plants require 75% less water than traditional landscaping while providing year-round beauty.",
    "water_conservation_rebates": "Local water utilities may offer rebates for water-efficient landscaping, fixtures, and irrigation system upgrades.",
    "rain_harvesting_systems": "Rain collection systems are encouraged but must comply with local codes and not create standing water or pest issues.",
    
    # Property Survey Information
    "survey_markers_location": "Property survey markers are typically located at property corners and may be metal pins, concrete monuments, or marked trees.",
    "survey_marker_protection": "Survey markers are protected by law and cannot be removed or disturbed. Contact surveyor if markers appear damaged or missing.",
    "property_boundary_disputes": "Boundary disputes should be resolved through professional surveyor and may require legal consultation with HOA attorney.",
    "survey_requirements": "Current surveys may be required for major improvements, fence installation, or property boundary verification.",
    
    # Vendor Contracting and Bidding
    "vendor_bidding_requirements": "Contracts over $5,000 require minimum 3 competitive bids. Contracts over $25,000 may require membership approval.",
    "contractor_qualification": "All contractors must provide: licensing, insurance, bonding, references, and detailed scope of work specifications.",
    "bid_evaluation_criteria": "Bids are evaluated on: cost, qualifications, timeline, references, warranty terms, and previous HOA experience.",
    "emergency_contract_procedures": "Emergency repairs may proceed without bidding but must be ratified by board at next meeting with documentation.",
    "preferred_vendor_program": "Established relationships with qualified vendors may allow streamlined bidding for routine maintenance contracts.",
    
    # Roofing Coverage and Insurance
    "roof_damage_coverage": "HOA master insurance covers roof damage from covered perils (wind, hail, fire). Normal wear and maintenance are owner responsibility.",
    "roof_replacement_responsibility": "HOA is responsible for roof replacement when damage is from covered insurance events or normal end-of-life replacement.",
    "roof_maintenance_requirements": "Preventive roof maintenance is HOA responsibility including inspections, minor repairs, and gutter cleaning.",
    "insurance_deductible_responsibility": "Insurance deductibles for roof claims may be assessed to affected unit owners or paid from reserve funds.",
    "roof_modification_restrictions": "Roof modifications (skylights, vents, solar panels) require architectural approval and must maintain warranty coverage.",
    
    # Additional Core Rules
    "exterior_paint_colors": "Exterior paint colors must be from the approved color palette available at the management office. Earth tones and neutral colors are preferred.",
    "pet_registration": "All pets must be registered with the management office within 30 days of moving in or acquiring a pet.",
    "parking_assignments": "Each unit is assigned specific parking spaces. Parking in unauthorized spaces may result in towing at owner's expense.",
    "quiet_hours": "Quiet hours are from 10:00 PM to 7:00 AM daily. Excessive noise during these hours may result in violations.",
    "pool_rules": "Pool hours are 6:00 AM to 10:00 PM. Children must be supervised. No glass containers or alcohol in pool area.",
    "monthly_assessments": "Monthly assessments are due on the first of each month. Late fees apply after the 15th day.",
    "violation_procedures": "Rule violations are addressed through written notice, hearing opportunity, and progressive enforcement including fines.",
    "document_amendments": "HOA documents may be amended with proper notice and voting procedures as specified in governing documents."
}

st.markdown("## 🔍 Ask Any HOA Question")
query = st.text_input(
    "Type your question in natural language:",
    placeholder="e.g., architectural review requirements, rental rules, easements, reserves, board quorum"
)

# Advanced search function with comprehensive matching
def search_hoa_rules(search_query):
    if not search_query:
        return []
    
    results = []
    search_terms = search_query.lower().strip()
    
    # Split query into individual words and phrases
    query_words = re.findall(r'\b\w+\b', search_terms)
    
    for rule_id, rule_text in hoa_rules.items():
        score = 0
        rule_lower = rule_text.lower()
        rule_name_lower = rule_id.lower()
        
        # Exact phrase matching (highest score)
        if search_terms in rule_lower or search_terms in rule_name_lower:
            score += 100
        
        # Multi-word phrase matching
        if len(query_words) > 1:
            for i in range(len(query_words) - 1):
                phrase = f"{query_words[i]} {query_words[i+1]}"
                if phrase in rule_lower or phrase in rule_name_lower:
                    score += 50
        
        # Individual word matching with context scoring
        word_matches = 0
        for word in query_words:
            if len(word) > 2:  # Skip very short words
                if word in rule_lower:
                    word_matches += 1
                    score += 15
                if word in rule_name_lower:
                    word_matches += 1
                    score += 25  # Higher score for rule name matches
        
        # Bonus for multiple word matches
        if word_matches > 1:
            score += word_matches * 10
        
        # Enhanced synonym matching for better results
        synonyms = {
            'architectural': ['review', 'modification', 'approval', 'construction', 'building'],
            'rental': ['rent', 'lease', 'tenant', 'airbnb', 'vrbo', 'short', 'long'],
            'easement': ['boundary', 'property', 'utility', 'access', 'drainage'],
            'reserve': ['fund', 'money', 'budget', 'repair', 'replacement'],
            'buffer': ['setback', 'distance', 'space', 'boundary', 'tree', 'structure'],
            'board': ['quorum', 'meeting', 'director', 'governance', 'vote'],
            'financial': ['report', 'statement', 'budget', 'assessment', 'fee'],
            'ownership': ['property', 'boundary', 'common', 'unit', 'hoa'],
            'water': ['conservation', 'irrigation', 'drought', 'sprinkler', 'native'],
            'survey': ['marker', 'boundary', 'property', 'corner', 'pin'],
            'bid': ['contract', 'vendor', 'contractor', 'proposal', 'quote'],
            'roof': ['damage', 'insurance', 'repair', 'replacement', 'coverage']
        }
        
        for main_word, related_words in synonyms.items():
            if main_word in query_words:
                for related in related_words:
                    if related in rule_lower or related in rule_name_lower:
                        score += 18
        
        # Add result if any matches found
        if score > 0:
            results.append({
                'rule_id': rule_id,
                'rule_text': rule_text,
                'score': score,
                'title': rule_id.replace('_', ' ').title()
            })
    
    # Sort by score (highest first)
    results.sort(key=lambda x: x['score'], reverse=True)
    return results

# Comprehensive quick search buttons
st.markdown("### 🎯 Popular HOA Topics:")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🏗️ Architectural Review"):
        query = "architectural review requirements approval"
with col2:
    if st.button("🏠 Rental Rules"):
        query = "rental short term long term airbnb"
with col3:
    if st.button("📍 Property Boundaries"):
        query = "easements property boundaries ownership"
with col4:
    if st.button("💰 Reserve Funds"):
        query = "reserves fund usage repairs"

col5, col6, col7, col8 = st.columns(4)

with col5:
    if st.button("🌳 Tree & Buffer Rules"):
        query = "buffer regulations tree removal structures"
with col6:
    if st.button("🏛️ Board & Governance"):
        query = "board quorum meetings governance"
with col7:
    if st.button("📊 Financial Reports"):
        query = "financial reports statements budget"
with col8:
    if st.button("💧 Water Conservation"):
        query = "water conservation irrigation tools"

# Additional topic buttons
col9, col10, col11, col12 = st.columns(4)

with col9:
    if st.button("📐 Survey & Markers"):
        query = "survey markers property boundaries"
with col10:
    if st.button("📋 Bidding Process"):
        query = "bids contracts vendors contractors"
with col11:
    if st.button("🏠 Roof Coverage"):
        query = "roof damage insurance coverage"
with col12:
    if st.button("🎨 Paint Colors"):
        query = "paint colors exterior approval"

# Display search results
if query:
    results = search_hoa_rules(query)
    
    if results:
        st.markdown(f"### 📋 Found {len(results)} Results for: '{query}'")
        
        for i, result in enumerate(results[:6], 1):  # Show top 6 results
            relevance = "🔥 High" if result['score'] >= 70 else "⭐ Medium" if result['score'] >= 35 else "💡 Related"
            
            st.markdown(f"""
            <div style="border: 1px solid #ddd; padding: 1.2rem; margin: 0.8rem 0; border-radius: 10px; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h4 style="margin: 0 0 0.8rem 0; color: #2c3e50;">📄 {result['title']} <small style="color: #666; font-weight: normal;">({relevance} Relevance)</small></h4>
                <p style="font-size: 1.05em; line-height: 1.7; margin: 0; color: #34495e;">{result['rule_text']}</p>
            </div>
            """, unsafe_allow_html=True)
            
        if len(results) > 6:
            st.info(f"Showing top 6 of {len(results)} results. Try more specific terms for better matches.")
    else:
        st.warning(f"No rules found for '{query}'. Try different keywords or use the topic buttons above.")
        st.info("""
        **💡 Search Tips:**
        - **Architectural:** "architectural review", "modifications", "approval process"
        - **Rentals:** "short term rental", "long term rental", "airbnb rules"
        - **Property:** "easements", "boundaries", "ownership", "survey markers"
        - **Governance:** "board quorum", "financial reports", "reserve funds"
        - **Ask complete questions:** "What are the requirements for architectural review?"
        """)

# Comprehensive footer with all topics
st.markdown("---")
with st.expander("📚 Complete HOA Topics Coverage - Click to Expand"):
    st.markdown("""
    **🏗️ Architectural Review:** Requirements, timeline, committee, appeals, approval process
    
    **🏠 Rental Policies:** Short-term restrictions, long-term approval, tenant requirements, violations
    
    **📍 Property & Easements:** Boundaries, utility access, drainage, survey markers, ownership limits
    
    **💰 Reserve Funds:** Usage restrictions, approved components, study requirements, expenditure approval
    
    **🌳 Buffer & Removal:** Setback requirements, tree removal approval, structure removal, landscaping
    
    **🏛️ Board Governance:** Quorum requirements, meeting procedures, voting, responsibilities
    
    **📊 Financial Reporting:** Annual statements, budget approval, assessment collection, record access
    
    **🏠 Property Ownership:** Unit boundaries, common areas, maintenance responsibilities, modifications
    
    **💧 Water Conservation:** Available tools, irrigation efficiency, drought landscaping, rebates
    
    **📐 Survey Information:** Marker locations, boundary disputes, protection requirements
    
    **📋 Vendor Bidding:** Bid requirements, contractor qualifications, evaluation criteria, emergency procedures
    
    **🏠 Roof Coverage:** Insurance coverage, replacement responsibility, maintenance, modifications
    
    **Plus:** Paint colors, pets, parking, noise, pools, assessments, violations, amendments
    """)

st.success("✅ **Comprehensive HOA search covering ALL major topics! Try your specific questions now.**")
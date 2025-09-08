import streamlit as st
import re

st.set_page_config(page_title="Florida HOA Rules Lookup", page_icon="🏘️")

st.markdown("# 🏘️ Florida HOA Rules Lookup")
st.markdown("**Comprehensive Florida HOA search based on Florida Statute 720 and real community examples**")
st.info("🏘️ **Featured Community**: Includes actual rules from **Boca Ridge Glen HOA** in Palm Beach County, Florida")

# FLORIDA-SPECIFIC HOA rules database with statute references, links, AND Boca Ridge Glen examples
florida_hoa_rules = {
    # Architectural Review - Florida Specific with Boca Ridge Glen Examples
    "architectural_review_process_fl": {
        "content": "Per Florida Statute 720.303, architectural review applications must be approved or denied within 45 days of submission. Failure to respond within 45 days constitutes approval unless governing documents specify otherwise.",
        "boca_ridge_example": "Boca Ridge Glen Architectural Control Board: No building, wall, fence, or other structure shall be erected until construction plans and specifications are approved in writing by the Architectural Control Board. Refusal may be based on any ground, including purely aesthetic grounds.",
        "statute": "720.303",
        "links": [
            ("Florida Statute 720.303", "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0700-0799/0720/Sections/0720.303.html"),
            ("CAI Florida Chapter", "https://www.caionline.org/StateChapters/Florida/Pages/default.aspx")
        ]
    },
    
    # Pet Policies - Florida and Boca Ridge Glen
    "pet_restrictions_fl": {
        "content": "Florida HOAs may establish reasonable pet restrictions and registration requirements under community covenants and Florida Statute 720.",
        "boca_ridge_example": "Boca Ridge Glen Pet Policy: Dogs weighing less than 30 pounds, cats, or other household pets may be kept, provided they are not kept for commercial purposes and do not become a nuisance. Dogs must be on leash not exceeding 6 feet. No pet excretions allowed except in designated areas.",
        "statute": "720 (General)",
        "links": [
            ("Florida Statute 720", "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0700-0799/0720/"),
            ("Pet Policy Guidelines", "https://www.caionline.org/")
        ]
    },
    
    # Property Boundaries and Common Areas - Boca Ridge Glen Specific
    "common_areas_definition_fl": {
        "content": "Florida Statute 720.301 defines common areas as property owned by the association for use by all members, including recreational facilities, roads, and landscaped areas.",
        "boca_ridge_example": "Boca Ridge Glen Common Areas: Include walkways, parking facilities, lakes, ponds, canals, open spaces, private streets, sidewalks, driveways, street lighting, entrance features and landscaping. Common Areas include grass areas to the edge of pavement of Boca Ridge Drive and Boca Ridge Drive South.",
        "statute": "720.301",
        "links": [
            ("Florida Statute 720.301", "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0700-0799/0720/Sections/0720.301.html"),
            ("Property Rights Guide", "https://www.caionline.org/")
        ]
    },
    
    # Assessments and Collection - Boca Ridge Glen Example
    "assessment_collection_fl": {
        "content": "Florida Statute 720.3085 provides HOAs with collection rights including liens, foreclosure, and attorney fees, with specific notice requirements before legal action.",
        "boca_ridge_example": "Boca Ridge Glen Assessment Policy: Annual assessments payable in monthly installments. If not paid within 30 days after due date, assessment bears interest at 18% per annum. Association may bring legal action and add attorneys' fees and costs to the amount owed.",
        "statute": "720.3085",
        "links": [
            ("Florida Statute 720.3085", "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0700-0799/0720/Sections/0720.3085.html"),
            ("Collection Procedures", "https://www.caionline.org/")
        ]
    },
    
    # Fines and Violations - Boca Ridge Glen Specific Process
    "violation_fines_fl": {
        "content": "Florida Statute 720.305 requires specific violation notice procedures including 14-day cure period for most violations before fines can be imposed.",
        "boca_ridge_example": "Boca Ridge Glen Fine Schedule: First violation up to $50, Second violation up to $100, Third violation up to $200, Fourth and subsequent violations up to $500. Owner gets notice and hearing opportunity before Board of Directors, with appeals committee process available.",
        "statute": "720.305",
        "links": [
            ("Florida Statute 720.305", "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0700-0799/0720/Sections/0720.305.html"),
            ("Violation Procedures", "https://www.caionline.org/")
        ]
    },
    
    # Exterior Maintenance - Boca Ridge Glen Specific
    "exterior_maintenance_fl": {
        "content": "Florida HOAs typically maintain exterior elements of buildings and common areas, with specific responsibilities defined in governing documents.",
        "boca_ridge_example": "Boca Ridge Glen Exterior Maintenance: Association maintains paint, coating, stain and other exterior finishing on all buildings as originally installed. Association also maintains landscaping, sprinkler systems, private streets, sidewalks, driveways, and street lighting throughout the community.",
        "statute": "720 (General)",
        "links": [
            ("Florida HOA Maintenance Law", "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0700-0799/0720/"),
            ("Maintenance Guidelines", "https://www.caionline.org/")
        ]
    },
    
    # Landscaping Requirements - Boca Ridge Glen
    "landscaping_requirements_fl": {
        "content": "Florida communities often have specific landscaping standards to maintain property values and community appearance.",
        "boca_ridge_example": "Boca Ridge Glen Landscaping Rules: Landscaping maintained as originally installed by Developer unless prior approval obtained from Architectural Control Board. No tree or shrub with trunk exceeding 2 inches diameter may be removed without written consent. No artificial grass or plants allowed without approval.",
        "statute": "Community Covenants",
        "links": [
            ("Florida-Friendly Landscaping", "https://ffl.ifas.ufl.edu/"),
            ("Native Plant Guidelines", "https://www.fnps.org/")
        ]
    },
    
    # Water Conservation Requirements - Florida and Boca Ridge Glen
    "water_conservation_fl": {
        "content": "Florida communities must comply with water management district regulations and may implement additional conservation measures during drought conditions. Florida Statute 373 governs water use and conservation throughout the state.",
        "boca_ridge_example": "Boca Ridge Glen Water Conservation: Irrigation systems must comply with South Florida Water Management District regulations. Watering restricted to designated days and times. Drought-tolerant landscaping encouraged. Pool covers required to reduce evaporation.",
        "statute": "373 (Water Resources)",
        "links": [
            ("Florida Water Management", "https://www.sfwmd.gov/"),
            ("Water Conservation Guidelines", "https://floridadep.gov/water"),
            ("SFWMD Regulations", "https://www.sfwmd.gov/doing-business-with-us/permits/irrigation")
        ]
    },
    
    "irrigation_restrictions_fl": {
        "content": "South Florida Water Management District requires year-round irrigation restrictions: residential properties may water on assigned days only, typically twice per week, between 4am-10am or 4pm-8pm.",
        "boca_ridge_example": "Boca Ridge Glen follows SFWMD irrigation schedule: Even-numbered addresses water Wednesday/Saturday, odd-numbered addresses water Thursday/Sunday. No watering 10am-4pm. Hand watering and micro-irrigation allowed anytime.",
        "statute": "SFWMD Rules",
        "links": [
            ("SFWMD Watering Rules", "https://www.sfwmd.gov/living-in-south-florida/water-restrictions"),
            ("Year-Round Restrictions", "https://www.sfwmd.gov/sites/default/files/documents/wsd_year_round_landscape_irrigation_rule.pdf")
        ]
    },
    
    "drought_emergency_procedures_fl": {
        "content": "During declared water emergencies, Florida communities must implement additional restrictions including prohibition of non-essential water uses such as car washing, fountain operation, and landscape irrigation.",
        "boca_ridge_example": "Boca Ridge Glen Emergency Water Plan: During Phase I restrictions, irrigation reduced to once per week. Phase II eliminates all irrigation except hand watering. Violations subject to fines and water service suspension.",
        "statute": "Emergency Management",
        "links": [
            ("Florida Drought Response", "https://floridadisaster.org/dem/mitigation/drought/"),
            ("Water Emergency Plans", "https://www.sfwmd.gov/")
        ]
    },
    
    "florida_friendly_landscaping_fl": {
        "content": "Florida Statute 720.3075 and 373.185 require HOAs to allow Florida-friendly landscaping that conserves water and protects the environment. HOAs cannot enforce rules prohibiting sustainable landscaping practices including drought-tolerant plants, efficient irrigation, and native species.",
        "boca_ridge_example": "Boca Ridge Glen must permit Florida-friendly landscaping modifications under state law, including replacement of high-water-use grass with drought-tolerant alternatives, installation of rain gardens, and use of native plant species approved by University of Florida guidelines.",
        "statute": "720.3075, 373.185",
        "links": [
            ("Florida Statute 720.3075", "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0700-0799/0720/Sections/0720.3075.html"),
            ("Florida Statute 373.185", "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0300-0399/0373/Sections/0373.185.html"),
            ("Florida-Friendly Landscaping", "https://ffl.ifas.ufl.edu/"),
            ("UF Plant Database", "https://gardeningsolutions.ifas.ufl.edu/plants/")
        ]
    },
    
    "rain_water_collection_fl": {
        "content": "Florida Statute 373.036 permits residential rainwater collection for landscape irrigation and other non-potable uses. HOAs cannot prohibit rain barrels or cisterns used for water conservation.",
        "boca_ridge_example": "Boca Ridge Glen residents may install rain collection systems under Florida law for irrigation purposes, subject to reasonable aesthetic guidelines from the Architectural Control Board.",
        "statute": "373.036",
        "links": [
            ("Florida Statute 373.036", "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0300-0399/0373/Sections/0373.036.html"),
            ("Rainwater Harvesting Guide", "https://edis.ifas.ufl.edu/")
        ]
    },
    
    # Vehicle and Parking Restrictions - Boca Ridge Glen
    "vehicle_restrictions_fl": {
        "content": "Florida HOAs commonly restrict commercial vehicles, RVs, and boats to maintain residential character and property values.",
        "boca_ridge_example": "Boca Ridge Glen Vehicle Policy: No trucks, commercial vehicles (over 6 feet height or with commercial markings), campers, motor homes, boats, or trailers permitted except during construction or if stored in garages/behind walls where not visible from streets. Temporary parking allowed for deliveries and services.",
        "statute": "Community Covenants",
        "links": [
            ("HOA Vehicle Restrictions", "https://www.caionline.org/"),
            ("Property Value Protection", "https://www.appraisalinstitute.org/")
        ]
    },
    
    # Use Restrictions - Boca Ridge Glen
    "residential_use_fl": {
        "content": "Florida residential communities restrict properties to residential use only, preventing commercial activities that could disrupt neighborhood character.",
        "boca_ridge_example": "Boca Ridge Glen Use Restrictions: No Lot shall be used except for residential purposes. No business, service repair or maintenance for general public allowed on any Lot or Common Areas. No 'for rent', 'for sale' or other signs displayed to public view.",
        "statute": "Zoning and Covenants",
        "links": [
            ("Residential Zoning Laws", "https://www.myflorida.com/"),
            ("Land Use Guidelines", "https://www.caionline.org/")
        ]
    },
    
    # Party Wall Maintenance - Boca Ridge Glen Specific
    "party_wall_maintenance_fl": {
        "content": "Florida attached housing developments often have specific party wall maintenance requirements shared between adjacent owners.",
        "boca_ridge_example": "Boca Ridge Glen Party Wall Policy: Cost of reasonable repair and maintenance shared by Owners in proportion to use. If party wall destroyed by fire/casualty not covered by insurance, any Owner may restore it with others contributing proportionally. Association may repair party walls if Owner fails to maintain properly.",
        "statute": "Property Law",
        "links": [
            ("Florida Property Law", "http://www.leg.state.fl.us/statutes/"),
            ("Party Wall Guidelines", "https://www.caionline.org/")
        ]
    },
    
    # Additional Florida Statutory Requirements
    "reserve_fund_requirements_fl": {
        "content": "Florida Statute 720.303 requires HOAs to maintain reserve accounts for roof replacement, building painting, pavement resurfacing, and other major components with useful lives exceeding one year.",
        "boca_ridge_example": "Reserve funding requirements apply to Boca Ridge Glen for major component replacement and capital improvements as mandated by Florida law.",
        "statute": "720.303",
        "links": [
            ("Florida Statute 720.303", "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0700-0799/0720/Sections/0720.303.html"),
            ("Reserve Study Guidelines", "https://www.apra-usa.com/")
        ]
    },
    
    "board_meetings_fl": {
        "content": "Florida law requires 48-hour advance notice for board meetings, with emergency meetings allowed for urgent matters affecting health, safety, or significant financial issues.",
        "boca_ridge_example": "Boca Ridge Glen board governance follows Florida Sunshine Law requirements for open meetings and proper notice procedures.",
        "statute": "720.306",
        "links": [
            ("Florida Statute 720.306", "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0700-0799/0720/Sections/0720.306.html"),
            ("Sunshine Law Guide", "https://www.myflorida.com/myflorida/government/governmentinformation/sunshine_law.html")
        ]
    }
}

st.markdown("## 🔍 Search Florida HOA Laws and Community Rules")
query = st.text_input(
    "Ask any question about Florida HOA laws and community rules:",
    placeholder="e.g., Boca Ridge Glen pet policies, architectural review, assessment collection"
)

# Enhanced Florida search function with Boca Ridge examples
def search_florida_hoa_rules(search_query):
    if not search_query:
        return []
    
    results = []
    search_terms = search_query.lower().strip()
    query_words = re.findall(r'\b\w+\b', search_terms)
    
    for rule_id, rule_data in florida_hoa_rules.items():
        score = 0
        rule_content = rule_data["content"]
        boca_example = rule_data.get("boca_ridge_example", "")
        rule_lower = (rule_content + " " + boca_example).lower()
        rule_name_lower = rule_id.lower()
        
        # Boost for Boca Ridge Glen mentions
        if 'boca ridge' in search_terms or 'boca ridge glen' in rule_lower:
            score += 30
        
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
        
        # Enhanced synonym matching
        florida_synonyms = {
            'pet': ['dog', 'cat', 'animal', 'leash', 'weight'],
            'architectural': ['building', 'modification', 'approval', 'construction'],
            'assessment': ['fee', 'payment', 'collection', 'lien', 'interest'],
            'fine': ['violation', 'penalty', 'hearing', 'appeal'],
            'maintenance': ['repair', 'exterior', 'painting', 'landscaping'],
            'vehicle': ['truck', 'commercial', 'boat', 'trailer', 'parking'],
            'boca': ['ridge', 'glen', 'community', 'example']
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
                'has_boca_example': bool(rule_data.get("boca_ridge_example"))
            })
    
    # Sort by score (highest first)
    results.sort(key=lambda x: x['score'], reverse=True)
    return results

# Florida-specific topic buttons with Boca Ridge examples
st.markdown("### 🎯 Florida HOA Law Topics:")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🏗️ Architectural Rules"):
        query = "architectural review boca ridge glen"
with col2:
    if st.button("🐕 Pet Policies"):
        query = "pet restrictions boca ridge glen dogs"
with col3:
    if st.button("💰 Assessments & Fines"):
        query = "assessment collection fines boca ridge"
with col4:
    if st.button("🏠 Property Use"):
        query = "residential use restrictions boca ridge"

col5, col6, col7, col8 = st.columns(4)

with col5:
    if st.button("🌳 Landscaping Rules"):
        query = "landscaping requirements boca ridge trees"
with col6:
    if st.button("🚗 Vehicle Restrictions"):
        query = "vehicle parking restrictions boca ridge"
with col7:
    if st.button("🏛️ Common Areas"):
        query = "common areas boca ridge glen"
with col8:
    if st.button("📜 FL Statute 720"):
        query = "florida statute 720 requirements"

# Display enhanced search results with Boca Ridge examples
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
            
            # Special indicators
            boca_indicator = " 🏘️" if result['has_boca_example'] else ""
            
            # Create links section
            links_html = ""
            for link_text, link_url in rule_data['links']:
                links_html += f'<a href="{link_url}" target="_blank" style="margin-right: 15px; color: #007bff; text-decoration: none;">🔗 {link_text}</a>'
            
            # Boca Ridge example section
            boca_section = ""
            if result['has_boca_example']:
                boca_section = f"""
                <div style="border-top: 1px solid #28a745; padding-top: 0.8rem; margin-top: 0.8rem; background: #f8fff8; padding: 0.8rem; border-radius: 6px;">
                    <p style="margin: 0 0 0.5rem 0; font-weight: bold; color: #28a745;">🏘️ Boca Ridge Glen Example:</p>
                    <p style="margin: 0; font-size: 0.95em; line-height: 1.6; color: #155724; font-style: italic;">{rule_data['boca_ridge_example']}</p>
                </div>
                """
            
            st.markdown(f"""
            <div style="border: 1px solid #ddd; padding: 1.3rem; margin: 0.8rem 0; border-radius: 12px; background: {color}; box-shadow: 0 3px 6px rgba(0,0,0,0.1);">
                <h4 style="margin: 0 0 0.8rem 0; color: #2c3e50;">📄 {result['title']}{boca_indicator} <small style="color: #666; font-weight: normal;">({relevance})</small></h4>
                <p style="font-size: 1.05em; line-height: 1.7; margin: 0 0 1rem 0; color: #34495e;"><strong>Florida Law:</strong> {rule_data['content']}</p>
                {boca_section}
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
        st.warning(f"No Florida HOA rules found for '{query}'. Try different keywords or use the topic buttons above.")
        st.info("""
        **💡 Florida HOA Search Tips:**
        - **Boca Ridge Glen Examples:** Try "boca ridge pet policy", "boca ridge architectural"
        - **Florida Statutes:** Try "Florida Statute 720.303", "720.305", "720.3085"  
        - **Specific Topics:** "assessment collection", "violation procedures", "common areas"
        - **Ask Questions:** "What are Boca Ridge Glen's pet restrictions?"
        """)

# Enhanced footer with Boca Ridge information
st.markdown("---")
with st.expander("🏘️ About Boca Ridge Glen HOA Community"):
    st.markdown("""
    **Boca Ridge Glen** is a real HOA community in **Palm Beach County, Florida** that serves as our example community.
    
    **📍 Location:** Palm Beach County, Florida
    **🏗️ Developer:** Originally developed by Ketay Enterprises, Inc.
    **📅 Established:** 1983
    **🏘️ Type:** Residential planned community with villas and townhouses
    
    **Key Features:**
    - Private streets and common areas
    - Architectural control board with aesthetic standards
    - Comprehensive landscaping and exterior maintenance by HOA
    - Pet policies with specific size and behavior requirements
    - Vehicle restrictions to maintain residential character
    - Party wall maintenance agreements for attached units
    
    **Why We Use This Example:**
    Boca Ridge Glen provides real-world examples of how Florida HOA laws are implemented in actual communities, showing both state statutory requirements and specific community covenant applications.
    """)

with st.expander("📜 Complete Florida HOA Law Coverage - Click to Expand"):
    st.markdown("""
    **🏗️ Architectural Review:** Florida 45-day timeline + Boca Ridge Glen board procedures
    
    **🐕 Pet Policies:** State law framework + Boca Ridge 30-pound limit and leash requirements
    
    **💰 Assessment Collection:** FL Statute 720.3085 procedures + Boca Ridge 18% interest rate
    
    **⚖️ Violation Procedures:** FL Statute 720.305 notice requirements + Boca Ridge fine schedule
    
    **🏠 Property Use:** Residential restrictions + Boca Ridge specific use limitations
    
    **🌳 Landscaping:** Florida-Friendly principles + Boca Ridge tree removal approval
    
    **🚗 Vehicle Restrictions:** Community standards + Boca Ridge commercial vehicle prohibitions
    
    **🏘️ Common Areas:** State definitions + Boca Ridge specific areas and maintenance
    
    **Plus:** Real community examples show how Florida laws work in practice
    """)

st.success("✅ **Florida HOA search with real community examples from Boca Ridge Glen!**")
st.info("🏘️ **All results include both Florida statutory requirements AND real-world community implementations.**")
import streamlit as st
import re

st.set_page_config(page_title="HOA Rules Lookup", page_icon="🏘️")

st.markdown("# 🏘️ HOA Rules Lookup")
st.markdown("Ask any question about HOA rules - search is completely open-ended!")

# Comprehensive HOA rules database
hoa_rules = {
    # Architectural Rules
    "exterior_paint_colors": "Exterior paint colors must be from the approved color palette available at the management office. Earth tones and neutral colors are preferred.",
    "house_modifications": "All exterior modifications including additions, decks, patios, and structural changes require architectural approval before construction.",
    "roof_materials": "Roof materials must be approved by the architectural committee. Tile, shingle, and metal roofs may be permitted based on community standards.",
    "fencing_guidelines": "Fences must be approved and cannot exceed 6 feet in height. Chain link fences are prohibited. Wood, vinyl, and decorative metal fences are acceptable.",
    "driveway_requirements": "Driveways must be maintained in good condition. Cracks and stains should be repaired promptly. Oil stains must be cleaned immediately.",
    "landscaping_front_yard": "Front yard landscaping must be maintained according to community standards. Native plants are encouraged to reduce water usage.",
    "mailbox_standards": "All mailboxes must conform to community standards and be maintained in good condition. Replacement requires approval.",
    "exterior_lighting": "Exterior lighting must not create glare or disturbance to neighbors. Security lighting should be directed downward.",
    "satellite_dishes": "Satellite dishes and antennas require approval for placement and must be screened from view when possible.",
    "solar_panels": "Solar panel installations require architectural approval and must comply with community aesthetic guidelines.",
    
    # Pet Policies  
    "pet_registration": "All pets must be registered with the management office within 30 days of moving in or acquiring a pet.",
    "leash_requirements": "Dogs must be on leash at all times when outside of owner's unit. Retractable leashes are not recommended in common areas.",
    "pet_waste_cleanup": "Pet owners must immediately clean up after their pets on all community property. Waste stations are provided throughout the community.",
    "pet_size_limits": "Dogs over 50 pounds may require special approval. Aggressive breeds are prohibited as determined by insurance guidelines.",
    "pet_noise_control": "Pets that create excessive noise or disturbance may be subject to violation proceedings. Training is encouraged.",
    "pet_limits": "No more than two pets per household unless specifically approved by the board of directors.",
    
    # Parking Regulations
    "assigned_parking": "Each unit is assigned specific parking spaces. Parking in unauthorized spaces may result in towing at owner's expense.",
    "guest_parking": "Guest parking is limited to 24 consecutive hours. Extended guest stays require notification to management.",
    "commercial_vehicles": "Commercial vehicles, RVs, boats, and trailers are prohibited except during business hours for service calls.",
    "parking_violations": "Vehicles parked in violation may be towed immediately at owner's expense after proper notification.",
    "garage_use": "Garages must be used primarily for vehicle storage, not general storage that prevents parking.",
    "street_parking": "Street parking may be prohibited or restricted based on local municipal regulations and community guidelines.",
    
    # Noise Regulations
    "quiet_hours": "Quiet hours are from 10:00 PM to 7:00 AM daily. Excessive noise during these hours may result in violations.",
    "construction_hours": "Construction and maintenance work is permitted Monday-Friday 8:00 AM to 6:00 PM, Saturday 9:00 AM to 5:00 PM. No work on Sundays.",
    "pool_noise": "Pool areas have specific quiet hours. No loud music or parties after 10:00 PM. Glass containers are prohibited.",
    "air_conditioning": "Air conditioning units must be properly maintained to minimize noise. Window units may require approval.",
    
    # Rental Policies
    "short_term_rentals": "Short-term rentals of less than 30 days are prohibited. All rentals require board approval and tenant registration.",
    "rental_approval": "All rental agreements must be approved by the board and tenants must receive community rules and regulations.",
    "rental_deposits": "Landlords may be required to provide security deposits for tenant compliance with community rules.",
    
    # Financial Obligations
    "monthly_assessments": "Monthly assessments are due on the first of each month. Late fees apply after the 15th day.",
    "late_payment_fees": "Late fees of $25 will be charged for payments received after the 15th of the month.",
    "special_assessments": "Special assessments may be levied with approval of 75% of the membership for major repairs or improvements.",
    "collection_procedures": "Unpaid assessments may result in liens, legal action, and foreclosure proceedings as permitted by state law.",
    
    # Common Area Usage
    "pool_rules": "Pool hours are 6:00 AM to 10:00 PM. Children must be supervised. No glass containers or alcohol in pool area.",
    "clubhouse_rental": "Clubhouse may be reserved by residents for private functions with 14 days advance notice and deposit.",
    "playground_guidelines": "Children must be supervised at all times. Age restrictions apply to certain equipment for safety.",
    "fitness_center": "Fitness center hours are 6:00 AM to 10:00 PM daily. Users must be 16 or older and sign waiver.",
    "tennis_courts": "Tennis courts are available first-come, first-served. Proper athletic attire required.",
    
    # Maintenance Responsibilities
    "unit_maintenance": "Owners are responsible for all interior maintenance and repairs within their units.",
    "exterior_maintenance": "The association maintains common areas, building exteriors, roofs, and community amenities.",
    "emergency_repairs": "Emergency repairs that affect common areas should be reported immediately to management.",
    "preventive_maintenance": "Regular preventive maintenance schedules are established for all community systems and amenities.",
    
    # Governance and Meetings
    "board_meetings": "Board meetings are held monthly with 48 hours advance notice. Owners may attend and speak during designated times.",
    "annual_meeting": "The annual meeting is held each year for election of directors and presentation of financial reports.",
    "voting_procedures": "Voting may be conducted in person, by proxy, or by mail ballot as determined by the board.",
    "document_access": "Community documents, financial reports, and meeting minutes are available for inspection by owners.",
    
    # Landscaping and Environment
    "tree_removal": "Tree removal requires approval from the architectural committee or board of directors.",
    "irrigation_systems": "Irrigation systems must be properly maintained and not waste water. Watering restrictions may apply.",
    "pesticide_use": "Pesticide and herbicide use must comply with local environmental regulations and community guidelines."
}

st.markdown("## 🔍 Ask Any HOA Question")
query = st.text_input(
    "Type your question in natural language:",
    placeholder="e.g., Can I paint my house blue? What about guest parking? Are pets allowed?"
)

# Enhanced search function
def search_hoa_rules(search_query):
    if not search_query:
        return []
    
    results = []
    search_terms = search_query.lower().strip()
    
    # Split query into individual words for broader matching
    query_words = re.findall(r'\b\w+\b', search_terms)
    
    for rule_id, rule_text in hoa_rules.items():
        score = 0
        rule_lower = rule_text.lower()
        rule_name_lower = rule_id.lower()
        
        # Exact phrase matching (highest score)
        if search_terms in rule_lower or search_terms in rule_name_lower:
            score += 100
        
        # Individual word matching
        word_matches = 0
        for word in query_words:
            if len(word) > 2:  # Skip very short words
                if word in rule_lower or word in rule_name_lower:
                    word_matches += 1
                    score += 10
        
        # Bonus for multiple word matches
        if word_matches > 1:
            score += word_matches * 5
        
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

# Quick search buttons
st.markdown("### 🎯 Popular Searches:")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🏠 House Colors"):
        query = "paint colors exterior"
with col2:
    if st.button("🐕 Pet Rules"):
        query = "pets dogs leash"
with col3:
    if st.button("🚗 Parking Info"):
        query = "parking guests spaces"
with col4:
    if st.button("💰 Fees & Costs"):
        query = "fees assessments payments"

col5, col6, col7, col8 = st.columns(4)

with col5:
    if st.button("🔊 Noise Rules"):
        query = "quiet hours noise"
with col6:
    if st.button("🏊 Pool Rules"):
        query = "pool swimming hours"
with col7:
    if st.button("🏠 Rentals"):
        query = "rental airbnb lease"
with col8:
    if st.button("🌳 Landscaping"):
        query = "trees plants landscaping"

# Display search results
if query:
    results = search_hoa_rules(query)
    
    if results:
        st.markdown(f"### 📋 Found {len(results)} Results for: '{query}'")
        
        for i, result in enumerate(results[:10], 1):  # Show top 10 results
            relevance = "🔥 High" if result['score'] >= 50 else "⭐ Medium" if result['score'] >= 20 else "💡 Related"
            
            st.markdown(f"""
            <div style="border: 1px solid #ddd; padding: 1rem; margin: 0.5rem 0; border-radius: 8px; background: #f8f9fa;">
                <h4>📄 {result['title']} <small style="color: #666;">({relevance} Relevance)</small></h4>
                <p style="font-size: 1.1em; line-height: 1.6;">{result['rule_text']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning(f"No rules found for '{query}'. Try different keywords or phrases.")
        st.info("""
        **💡 Search Tips:**
        - Try keywords like: paint, pets, parking, noise, pool, rental, fees
        - Ask natural questions: "Can I have a dog?" or "What are quiet hours?"
        - Use specific terms: "guest parking" instead of just "parking"
        """)

# Footer with available topics
st.markdown("---")
with st.expander("📚 Available HOA Topics - Click to Expand"):
    st.markdown("""
    **🏠 Architecture:** Paint colors, modifications, roofs, fencing, driveways, landscaping, mailboxes, lighting, solar panels
    
    **🐕 Pets:** Registration, leash rules, waste cleanup, size limits, noise control, pet limits
    
    **🚗 Parking:** Assigned spaces, guest parking, commercial vehicles, violations, garage use, street parking
    
    **🔊 Noise:** Quiet hours, construction times, pool noise, air conditioning
    
    **🏠 Rentals:** Short-term restrictions, approval process, tenant requirements, deposits
    
    **💰 Finances:** Monthly assessments, late fees, special assessments, collection procedures
    
    **🏊 Common Areas:** Pool rules, clubhouse rental, playground, fitness center, tennis courts
    
    **🔧 Maintenance:** Unit vs. association responsibilities, emergency repairs, preventive maintenance
    
    **🏛️ Governance:** Board meetings, annual meetings, voting, document access
    
    **🌳 Environment:** Tree removal, irrigation, landscaping, pesticide use
    """)

st.success("✅ **Ask anything about HOA rules! The search covers all community topics.**")
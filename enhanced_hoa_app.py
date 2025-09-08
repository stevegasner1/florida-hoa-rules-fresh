import streamlit as st
import re

st.set_page_config(page_title="HOA Rules Lookup", page_icon="🏘️")

st.markdown("# 🏘️ HOA Rules Lookup")
st.markdown("Ask any question about HOA rules - comprehensive search covering all topics!")

# EXPANDED HOA rules database with water conservation and more
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
    
    # Water Conservation Requirements
    "water_conservation_general": "All residents must follow water conservation guidelines to preserve this valuable resource and comply with local water management districts.",
    "irrigation_restrictions": "Lawn and landscape irrigation is restricted to designated days and times. Watering is prohibited between 10:00 AM and 4:00 PM daily.",
    "drought_restrictions": "During drought conditions, additional water restrictions may be implemented including limits on car washing and pool filling.",
    "sprinkler_systems": "Automatic sprinkler systems must include rain sensors and be properly maintained to prevent waste. Broken sprinklers must be repaired immediately.",
    "water_waste_prohibition": "Water waste is prohibited including allowing water to run off property, irrigating during rain, or operating broken irrigation equipment.",
    "native_plant_requirements": "Native and drought-resistant plants are encouraged and may be required for new landscaping to reduce water consumption.",
    "rain_collection": "Rain barrels and collection systems are encouraged for landscape irrigation. Installation must comply with local codes.",
    "pool_water_conservation": "Pool owners must use covers to reduce evaporation and are encouraged to use water-efficient equipment and maintenance practices.",
    
    # Pet Policies  
    "pet_registration": "All pets must be registered with the management office within 30 days of moving in or acquiring a pet.",
    "leash_requirements": "Dogs must be on leash at all times when outside of owner's unit. Retractable leashes are not recommended in common areas.",
    "pet_waste_cleanup": "Pet owners must immediately clean up after their pets on all community property. Waste stations are provided throughout the community.",
    "pet_size_limits": "Dogs over 50 pounds may require special approval. Aggressive breeds are prohibited as determined by insurance guidelines.",
    "pet_noise_control": "Pets that create excessive noise or disturbance may be subject to violation proceedings. Training is encouraged.",
    "pet_limits": "No more than two pets per household unless specifically approved by the board of directors.",
    "service_animals": "Service animals and emotional support animals are accommodated according to federal and state fair housing laws.",
    
    # Parking Regulations
    "assigned_parking": "Each unit is assigned specific parking spaces. Parking in unauthorized spaces may result in towing at owner's expense.",
    "guest_parking": "Guest parking is limited to 24 consecutive hours. Extended guest stays require notification to management.",
    "commercial_vehicles": "Commercial vehicles, RVs, boats, and trailers are prohibited except during business hours for service calls.",
    "parking_violations": "Vehicles parked in violation may be towed immediately at owner's expense after proper notification.",
    "garage_use": "Garages must be used primarily for vehicle storage, not general storage that prevents parking.",
    "street_parking": "Street parking may be prohibited or restricted based on local municipal regulations and community guidelines.",
    "electric_vehicles": "Electric vehicle charging stations may be available. Personal charging equipment installation requires approval.",
    
    # Noise Regulations
    "quiet_hours": "Quiet hours are from 10:00 PM to 7:00 AM daily. Excessive noise during these hours may result in violations.",
    "construction_hours": "Construction and maintenance work is permitted Monday-Friday 8:00 AM to 6:00 PM, Saturday 9:00 AM to 5:00 PM. No work on Sundays.",
    "pool_noise": "Pool areas have specific quiet hours. No loud music or parties after 10:00 PM. Glass containers are prohibited.",
    "air_conditioning": "Air conditioning units must be properly maintained to minimize noise. Window units may require approval.",
    "music_and_parties": "Music and social gatherings must respect quiet hours and not disturb neighboring units at any time.",
    
    # Rental Policies
    "short_term_rentals": "Short-term rentals of less than 30 days are prohibited. All rentals require board approval and tenant registration.",
    "rental_approval": "All rental agreements must be approved by the board and tenants must receive community rules and regulations.",
    "rental_deposits": "Landlords may be required to provide security deposits for tenant compliance with community rules.",
    "airbnb_restrictions": "Airbnb, VRBO, and similar short-term rental platforms are prohibited within the community.",
    "rental_inspections": "Rental units may be subject to periodic inspections to ensure compliance with community standards.",
    
    # Financial Obligations
    "monthly_assessments": "Monthly assessments are due on the first of each month. Late fees apply after the 15th day.",
    "late_payment_fees": "Late fees of $25 will be charged for payments received after the 15th of the month.",
    "special_assessments": "Special assessments may be levied with approval of 75% of the membership for major repairs or improvements.",
    "collection_procedures": "Unpaid assessments may result in liens, legal action, and foreclosure proceedings as permitted by state law.",
    "fee_increases": "Assessment increases require proper notice and may be subject to membership approval depending on the amount.",
    "payment_methods": "Assessments may be paid by check, online portal, or automatic bank draft. Credit card payments may incur additional fees.",
    
    # Common Area Usage
    "pool_rules": "Pool hours are 6:00 AM to 10:00 PM. Children must be supervised. No glass containers or alcohol in pool area.",
    "clubhouse_rental": "Clubhouse may be reserved by residents for private functions with 14 days advance notice and deposit.",
    "playground_guidelines": "Children must be supervised at all times. Age restrictions apply to certain equipment for safety.",
    "fitness_center": "Fitness center hours are 6:00 AM to 10:00 PM daily. Users must be 16 or older and sign waiver.",
    "tennis_courts": "Tennis courts are available first-come, first-served. Proper athletic attire required.",
    "walking_trails": "Walking trails are for pedestrian use only. Bicycles and motorized vehicles are prohibited on designated walking paths.",
    
    # Maintenance Responsibilities
    "unit_maintenance": "Owners are responsible for all interior maintenance and repairs within their units.",
    "exterior_maintenance": "The association maintains common areas, building exteriors, roofs, and community amenities.",
    "emergency_repairs": "Emergency repairs that affect common areas should be reported immediately to management.",
    "preventive_maintenance": "Regular preventive maintenance schedules are established for all community systems and amenities.",
    "hvac_maintenance": "Unit owners are responsible for HVAC maintenance including filter changes and regular service.",
    
    # Governance and Meetings
    "board_meetings": "Board meetings are held monthly with 48 hours advance notice. Owners may attend and speak during designated times.",
    "annual_meeting": "The annual meeting is held each year for election of directors and presentation of financial reports.",
    "voting_procedures": "Voting may be conducted in person, by proxy, or by mail ballot as determined by the board.",
    "document_access": "Community documents, financial reports, and meeting minutes are available for inspection by owners.",
    "election_process": "Board elections are conducted annually with nominations accepted according to established procedures.",
    
    # Landscaping and Environment
    "tree_removal": "Tree removal requires approval from the architectural committee or board of directors.",
    "irrigation_systems": "Irrigation systems must be properly maintained and not waste water. Watering restrictions may apply.",
    "pesticide_use": "Pesticide and herbicide use must comply with local environmental regulations and community guidelines.",
    "composting": "Composting is encouraged but must be done in approved containers that do not create odors or attract pests.",
    "recycling_requirements": "Residents must participate in community recycling programs and follow proper sorting guidelines.",
    
    # Security and Safety
    "security_systems": "Personal security systems are permitted but must not interfere with common area safety systems.",
    "gate_access": "Access gates and key fobs remain property of the association. Lost devices incur replacement fees.",
    "visitor_policies": "All visitors must be registered and may be required to show identification at security checkpoints.",
    "emergency_procedures": "Residents should be familiar with emergency evacuation procedures and assembly points.",
    
    # Holiday and Seasonal Rules
    "holiday_decorations": "Holiday decorations are permitted during appropriate seasons and must be removed within 30 days after holidays.",
    "seasonal_items": "Seasonal items like holiday lights and decorations must comply with architectural guidelines.",
    "storage_restrictions": "Seasonal items must be stored inside units or designated storage areas, not on patios or balconies."
}

st.markdown("## 🔍 Ask Any HOA Question")
query = st.text_input(
    "Type your question in natural language:",
    placeholder="e.g., water conservation requirements, paint colors, pet policies, parking rules"
)

# Enhanced search function with better matching
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
        
        # Individual word matching with better scoring
        word_matches = 0
        for word in query_words:
            if len(word) > 2:  # Skip very short words
                if word in rule_lower:
                    word_matches += 1
                    score += 15  # Higher score for content matches
                if word in rule_name_lower:
                    word_matches += 1
                    score += 20  # Even higher for rule name matches
        
        # Bonus for multiple word matches
        if word_matches > 1:
            score += word_matches * 8
        
        # Special scoring for common synonyms
        synonyms = {
            'water': ['irrigation', 'watering', 'sprinkler', 'conservation'],
            'paint': ['color', 'exterior', 'house'],
            'dog': ['pet', 'animal', 'leash'],
            'parking': ['car', 'vehicle', 'garage'],
            'noise': ['quiet', 'sound', 'loud'],
            'rental': ['rent', 'lease', 'airbnb', 'vrbo'],
            'fee': ['assessment', 'cost', 'payment', 'dues']
        }
        
        for main_word, related_words in synonyms.items():
            if main_word in query_words:
                for related in related_words:
                    if related in rule_lower or related in rule_name_lower:
                        score += 12
        
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
    if st.button("🏠 Paint Colors"):
        query = "paint colors exterior"
with col2:
    if st.button("💧 Water Rules"):
        query = "water conservation irrigation"
with col3:
    if st.button("🐕 Pet Policies"):
        query = "pets dogs leash registration"
with col4:
    if st.button("🚗 Parking Rules"):
        query = "parking spaces guests"

col5, col6, col7, col8 = st.columns(4)

with col5:
    if st.button("💰 Fees & Costs"):
        query = "fees assessments payments"
with col6:
    if st.button("🏠 Rental Rules"):
        query = "rental airbnb short term"
with col7:
    if st.button("🔊 Noise Policy"):
        query = "quiet hours noise"
with col8:
    if st.button("🏊 Pool Rules"):
        query = "pool swimming hours"

# Display search results
if query:
    results = search_hoa_rules(query)
    
    if results:
        st.markdown(f"### 📋 Found {len(results)} Results for: '{query}'")
        
        for i, result in enumerate(results[:8], 1):  # Show top 8 results
            relevance = "🔥 High" if result['score'] >= 50 else "⭐ Medium" if result['score'] >= 25 else "💡 Related"
            
            st.markdown(f"""
            <div style="border: 1px solid #ddd; padding: 1rem; margin: 0.5rem 0; border-radius: 8px; background: #f8f9fa;">
                <h4>📄 {result['title']} <small style="color: #666;">({relevance} Relevance)</small></h4>
                <p style="font-size: 1.1em; line-height: 1.6; margin: 0.5rem 0;">{result['rule_text']}</p>
            </div>
            """, unsafe_allow_html=True)
            
        if len(results) > 8:
            st.info(f"Showing top 8 of {len(results)} results. Try more specific terms for better matches.")
    else:
        st.warning(f"No rules found for '{query}'. Try different keywords or phrases.")
        st.info("""
        **💡 Search Tips:**
        - **Water:** Try "water conservation", "irrigation", "sprinkler", "drought"
        - **Paint:** Try "paint colors", "exterior", "house colors"
        - **Pets:** Try "dogs", "pets", "leash", "registration"
        - **Money:** Try "fees", "assessments", "costs", "payments"
        - **Ask questions:** "Can I paint my house blue?", "Are dogs allowed?"
        """)

# Footer with available topics
st.markdown("---")
with st.expander("📚 All Available HOA Topics - Click to Expand"):
    st.markdown("""
    **🏠 Architecture:** Paint colors, modifications, roofs, fencing, driveways, landscaping, mailboxes, lighting, solar panels
    
    **💧 Water Conservation:** Irrigation restrictions, drought rules, sprinkler systems, water waste, native plants, rain collection
    
    **🐕 Pets:** Registration, leash rules, waste cleanup, size limits, noise control, service animals
    
    **🚗 Parking:** Assigned spaces, guest parking, commercial vehicles, violations, garage use, electric vehicles
    
    **🔊 Noise:** Quiet hours, construction times, pool noise, air conditioning, music and parties
    
    **🏠 Rentals:** Short-term restrictions, Airbnb prohibitions, approval process, tenant requirements, deposits
    
    **💰 Finances:** Monthly assessments, late fees, special assessments, collection procedures, payment methods
    
    **🏊 Common Areas:** Pool rules, clubhouse rental, playground, fitness center, tennis courts, walking trails
    
    **🔧 Maintenance:** Unit vs. association responsibilities, emergency repairs, preventive maintenance, HVAC
    
    **🏛️ Governance:** Board meetings, annual meetings, voting, document access, elections
    
    **🌳 Environment:** Tree removal, irrigation, landscaping, pesticide use, composting, recycling
    
    **🔒 Security:** Security systems, gate access, visitor policies, emergency procedures
    
    **🎄 Seasonal:** Holiday decorations, seasonal items, storage restrictions
    """)

st.success("✅ **Comprehensive HOA search covering 70+ rules! Try 'water conservation' now.**")
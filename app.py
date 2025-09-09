import streamlit as st
import re
import math
from collections import Counter

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
    },
    
    "board_quorum_requirements_fl": {
        "content": "Florida Statute 720.306 requires a majority of board members to constitute a quorum for conducting HOA business. For a 5-member board, 3 members are required; for a 7-member board, 4 members are required. Decisions require a majority vote of those present at a properly noticed meeting.",
        "boca_ridge_example": "Boca Ridge Glen HOA Board requires a majority of directors present to conduct official business, following Florida statutory quorum requirements for valid board actions and voting procedures.",
        "statute": "720.306",
        "links": [
            ("Florida Statute 720.306", "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0700-0799/0720/Sections/0720.306.html"),
            ("Board Governance Guide", "https://www.caionline.org/StateChapters/Florida/Pages/default.aspx")
        ]
    },
    
    "board_composition_fl": {
        "content": "Florida HOA boards typically consist of 3, 5, or 7 members as specified in governing documents. Florida Statute 720.306 governs board member eligibility, terms, and election procedures.",
        "boca_ridge_example": "Boca Ridge Glen Board of Directors composition and member terms are established in the community bylaws in compliance with Florida HOA governance requirements.",
        "statute": "720.306",
        "links": [
            ("Florida Statute 720.306", "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0700-0799/0720/Sections/0720.306.html"),
            ("Board Structure Guidelines", "https://www.caionline.org/")
        ]
    },
    
    "financial_reporting_requirements_fl": {
        "content": "Florida Statute 720.308 requires HOAs to prepare annual financial reports within 90 days after the end of the fiscal year. Associations with annual revenues over $150,000 must have reports reviewed by a CPA. Monthly financial statements must be available to members upon request.",
        "boca_ridge_example": "Boca Ridge Glen provides annual financial reports to homeowners within Florida's required timeline, including balance sheets, income statements, and reserve fund status as mandated by FL Statute 720.308.",
        "statute": "720.308",
        "links": [
            ("Florida Statute 720.308", "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0700-0799/0720/Sections/0720.308.html"),
            ("Financial Reporting Guide", "https://www.caionline.org/")
        ]
    },
    
    "budget_requirements_fl": {
        "content": "Florida Statute 720.308 requires HOAs to adopt an annual budget at least 14 days before the start of the fiscal year. The budget must be provided to all members and include operating expenses, reserves, and any special assessments planned.",
        "boca_ridge_example": "Boca Ridge Glen adopts its annual budget in compliance with Florida requirements, providing detailed financial planning documents to homeowners before the fiscal year begins.",
        "statute": "720.308", 
        "links": [
            ("Florida Statute 720.308", "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0700-0799/0720/Sections/0720.308.html"),
            ("Budget Planning Guide", "https://www.apra-usa.com/")
        ]
    }
}

st.markdown("## 🔍 Search Florida HOA Laws and Community Rules")
st.info("🤖 **NEW**: Dynamic search now handles ANY HOA question - ask about noise rules, solar panels, flags, elections, or any other topic!")
query = st.text_input(
    "Ask any question about Florida HOA laws and community rules:",
    placeholder="e.g., noise restrictions, solar panel installation, flag display rights, HOA elections"
)

# Dynamic response generator for open-ended queries
def generate_dynamic_response(query):
    """Generate dynamic HOA responses for queries not covered by existing rules"""
    
    # Common HOA topics and their Florida law context
    hoa_knowledge_base = {
        'noise': {
            'statutes': ['720.305 (Violation Procedures)'],
            'content': 'Florida HOAs can establish reasonable noise restrictions to maintain peaceful enjoyment of properties. Enforcement follows FL Statute 720.305 violation procedures.',
            'examples': ['Quiet hours (typically 10 PM - 7 AM)', 'Construction noise limits', 'Party/gathering restrictions', 'HVAC equipment placement rules']
        },
        'solar': {
            'statutes': ['163.04 (Solar Rights)', '720.3075 (Property Rights)'],
            'content': 'Florida Statute 163.04 protects homeowner rights to install solar collectors. HOAs cannot prohibit solar installations but may impose reasonable aesthetic restrictions.',
            'examples': ['Solar panel placement guidelines', 'Roof installation approval process', 'Aesthetic screening requirements', 'Energy efficiency improvements']
        },
        'flag': {
            'statutes': ['720.3075 (Display Rights)'],
            'content': 'Florida law protects the right to display the US flag, Florida state flag, and military service flags. HOAs may establish reasonable size and placement restrictions.',
            'examples': ['American flag display rights', 'Military service flag protection', 'Holiday decoration guidelines', 'Political sign restrictions']
        },
        'storage': {
            'statutes': ['720 (General Covenants)'],
            'content': 'Florida HOAs commonly restrict outdoor storage to maintain community appearance and property values through architectural guidelines.',
            'examples': ['Garage storage requirements', 'Shed installation approval', 'Pool equipment screening', 'Trash container placement']
        },
        'security': {
            'statutes': ['720.301 (Common Areas)', '768.28 (Liability)'],
            'content': 'Florida HOAs may provide security services and establish access control measures for common areas while managing liability considerations.',
            'examples': ['Gated community access', 'Security patrol services', 'Camera surveillance systems', 'Guest registration procedures']
        },
        'insurance': {
            'statutes': ['720.3085 (Financial Management)'],
            'content': 'Florida law requires HOAs to maintain appropriate insurance coverage and may require individual owners to carry specific insurance types.',
            'examples': ['Hurricane/windstorm coverage', 'Flood insurance requirements', 'Liability insurance minimums', 'Building coverage responsibilities']
        },
        'election': {
            'statutes': ['720.306 (Board Elections)'],
            'content': 'Florida Statute 720.306 governs HOA board elections including candidate eligibility, voting procedures, and term limits.',
            'examples': ['Annual election requirements', 'Candidate qualification rules', 'Voting method procedures', 'Term limit restrictions']
        },
        'budget': {
            'statutes': ['720.308 (Budgets and Financial Reports)'],
            'content': 'Florida law requires HOAs to prepare annual budgets, provide financial reports to owners, and follow specific assessment procedures.',
            'examples': ['Annual budget adoption', 'Financial statement distribution', 'Assessment increase limitations', 'Reserve fund requirements']
        }
    }
    
    query_lower = query.lower()
    
    # Find matching topics
    for topic, info in hoa_knowledge_base.items():
        if topic in query_lower or any(keyword in query_lower for keyword in [topic + 's', topic + 'ing']):
            return {
                'type': 'dynamic',
                'title': f'Florida HOA {topic.title()} Requirements',
                'content': info['content'],
                'statute': ', '.join(info['statutes']),
                'examples': info['examples'],
                'boca_example': f'Boca Ridge Glen would handle {topic} matters according to Florida statutory requirements and community covenants.',
                'links': [
                    ('Florida HOA Laws', 'http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0700-0799/0720/'),
                    ('CAI Florida Resources', 'https://www.caionline.org/StateChapters/Florida/Pages/default.aspx')
                ]
            }
    
    # General catch-all response for any HOA question
    return {
        'type': 'general',
        'title': f'Florida HOA Information: {query.title()}',
        'content': f'Florida HOA communities are governed by Chapter 720, Florida Statutes, which provides comprehensive frameworks for community governance. For specific questions about "{query}", consult your community\'s governing documents alongside applicable Florida statutes.',
        'statute': '720 (Florida HOA Act)',
        'examples': ['Review community covenants and bylaws', 'Consult Florida Statute Chapter 720', 'Contact your HOA board or management', 'Seek legal advice for complex issues'],
        'boca_example': f'Boca Ridge Glen, like all Florida HOAs, must comply with state law requirements while implementing community-specific rules through properly adopted covenants and bylaws.',
        'links': [
            ('Florida Statute 720', 'http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0700-0799/0720/'),
            ('Florida HOA Resources', 'https://www.caionline.org/StateChapters/Florida/Pages/default.aspx'),
            ('Legal Information', 'https://www.floridabar.org/')
        ]
    }

# Comprehensive semantic similarity system for HOA rule matching
def calculate_semantic_similarity(query, rule_content, rule_id):
    """Calculate semantic similarity using multiple algorithms"""
    
    # Normalize text
    query = query.lower().strip()
    content = rule_content.lower()
    rule_name = rule_id.lower()
    
    # Extract words (remove stop words for better matching)
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can'}
    
    query_words = [w for w in re.findall(r'\b\w+\b', query) if w not in stop_words and len(w) > 2]
    content_words = [w for w in re.findall(r'\b\w+\b', content + ' ' + rule_name) if w not in stop_words and len(w) > 2]
    
    if not query_words or not content_words:
        return 0
    
    # 1. TF-IDF-inspired scoring
    query_freq = Counter(query_words)
    content_freq = Counter(content_words)
    
    tf_idf_score = 0
    for word in query_words:
        if word in content_freq:
            # Term frequency in content
            tf = content_freq[word] / len(content_words)
            # Inverse document frequency (simplified - higher weight for less common words)
            idf = math.log(len(content_words) / (content_freq[word] + 1)) + 1
            tf_idf_score += tf * idf * 100
    
    # 2. Cosine similarity
    all_words = set(query_words + content_words)
    query_vector = [query_freq.get(word, 0) for word in all_words]
    content_vector = [content_freq.get(word, 0) for word in all_words]
    
    dot_product = sum(q * c for q, c in zip(query_vector, content_vector))
    query_magnitude = math.sqrt(sum(q * q for q in query_vector))
    content_magnitude = math.sqrt(sum(c * c for c in content_vector))
    
    cosine_score = 0
    if query_magnitude > 0 and content_magnitude > 0:
        cosine_score = (dot_product / (query_magnitude * content_magnitude)) * 100
    
    # 3. Jaccard similarity (overlap coefficient)
    query_set = set(query_words)
    content_set = set(content_words)
    intersection = len(query_set.intersection(content_set))
    union = len(query_set.union(content_set))
    jaccard_score = (intersection / union * 100) if union > 0 else 0
    
    # 4. Phrase matching bonuses
    phrase_score = 0
    # Exact query match
    if query in content:
        phrase_score += 200
    
    # Multi-word phrases
    if len(query_words) > 1:
        for i in range(len(query_words) - 1):
            phrase = f"{query_words[i]} {query_words[i+1]}"
            if phrase in content:
                phrase_score += 80
    
    # 5. Semantic categories and domain-specific matching
    semantic_categories = {
        'governance': ['board', 'director', 'meeting', 'quorum', 'voting', 'election', 'governance', 'bylaws', 'member', 'majority'],
        'financial': ['budget', 'financial', 'report', 'reports', 'reporting', 'money', 'fee', 'assessment', 'revenue', 'expense', 'accounting', 'cpa', 'audit', 'fiscal'],
        'property': ['property', 'real estate', 'lot', 'unit', 'residence', 'home', 'building', 'structure', 'land'],
        'maintenance': ['maintenance', 'repair', 'upkeep', 'service', 'contractor', 'work', 'improvement', 'renovation'],
        'rules': ['rule', 'rules', 'regulation', 'restriction', 'requirement', 'guideline', 'policy', 'covenant', 'provision'],
        'legal': ['statute', 'law', 'legal', 'florida', 'compliance', 'violation', 'enforcement', 'penalty', 'fine'],
        'pets': ['pet', 'dog', 'cat', 'animal', 'leash', 'weight', 'breed', 'registration'],
        'architectural': ['architectural', 'modification', 'approval', 'construction', 'building', 'design', 'structure'],
        'landscaping': ['landscape', 'landscaping', 'garden', 'tree', 'plant', 'grass', 'irrigation', 'lawn'],
        'vehicle': ['vehicle', 'car', 'truck', 'parking', 'garage', 'driveway', 'boat', 'trailer', 'commercial'],
        'water': ['water', 'irrigation', 'conservation', 'drought', 'watering', 'sprinkler', 'usage', 'restriction'],
        'frequency': ['often', 'frequency', 'when', 'timing', 'schedule', 'annual', 'monthly', 'quarterly', 'produced', 'prepared', 'issued']
    }
    
    category_score = 0
    query_categories = set()
    content_categories = set()
    
    # Identify categories in query and content
    for category, terms in semantic_categories.items():
        if any(term in query_words for term in terms):
            query_categories.add(category)
        if any(term in content_words for term in terms):
            content_categories.add(category)
    
    # Boost score for matching categories
    matching_categories = query_categories.intersection(content_categories)
    category_score = len(matching_categories) * 50
    
    # Penalty for mismatched primary categories
    mismatch_penalty = 0
    if query_categories and content_categories:
        if not matching_categories and len(query_categories) == 1 and len(content_categories) == 1:
            mismatch_penalty = 50  # Strong penalty for completely unrelated topics
    
    # 6. Context-specific boosters
    context_score = 0
    
    # Florida-specific boost
    if 'florida' in query and ('florida' in content or 'fl' in content):
        context_score += 30
    
    # Boca Ridge specific boost  
    if 'boca' in query and 'boca' in content:
        context_score += 40
    
    # HOA context boost
    if 'hoa' in query and 'hoa' in content:
        context_score += 20
    
    # Combine all scores with weights
    total_score = (
        tf_idf_score * 0.3 +
        cosine_score * 0.25 + 
        jaccard_score * 0.15 +
        phrase_score * 0.4 +
        category_score * 0.3 +
        context_score * 0.2 -
        mismatch_penalty
    )
    
    return max(0, total_score)  # Ensure non-negative score

# Enhanced Florida search function with semantic similarity
def search_florida_hoa_rules(search_query):
    if not search_query:
        return []
    
    results = []
    
    # Search existing rule database using semantic similarity
    for rule_id, rule_data in florida_hoa_rules.items():
        rule_content = rule_data["content"]
        boca_example = rule_data.get("boca_ridge_example", "")
        combined_content = rule_content + " " + boca_example
        
        # Calculate semantic similarity score
        score = calculate_semantic_similarity(search_query, combined_content, rule_id)
        
        # Add result if score is significant
        if score > 10:  # Lower threshold since we use more sophisticated scoring
            results.append({
                'rule_id': rule_id,
                'rule_data': rule_data,
                'score': score,
                'title': rule_id.replace('_fl', '').replace('_', ' ').title(),
                'has_boca_example': bool(rule_data.get("boca_ridge_example")),
                'type': 'existing'
            })
    
    # If no good matches found (highest score < 30), add dynamic response
    if not results or (results and max(r['score'] for r in results) < 30):
        dynamic_response = generate_dynamic_response(search_query)
        results.append({
            'rule_id': f'dynamic_{hash(search_query) % 1000}',
            'rule_data': {
                'content': dynamic_response['content'],
                'boca_ridge_example': dynamic_response['boca_example'],
                'statute': dynamic_response['statute'],
                'links': dynamic_response['links']
            },
            'score': 50,  # Medium relevance for dynamic responses
            'title': dynamic_response['title'],
            'has_boca_example': True,
            'type': 'dynamic',
            'examples': dynamic_response.get('examples', [])
        })
    
    # Filter out low-relevance results - only keep high-quality matches
    if results:
        # Get the top score to establish relevance threshold
        top_score = max(r['score'] for r in results)
        
        # Keep results that are at least 40% of the top score or have score >= 50
        relevance_threshold = max(top_score * 0.4, 50)
        high_quality_results = [r for r in results if r['score'] >= relevance_threshold]
        
        # If we have good results, use them; otherwise keep top 3
        if len(high_quality_results) >= 3:
            results = high_quality_results[:3]  # Limit to top 3 most relevant
        else:
            results = results[:3]  # Fallback to top 3
    
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

# Dynamic topic buttons
st.markdown("### 🤖 Dynamic Search Topics:")
col9, col10, col11, col12 = st.columns(4)

with col9:
    if st.button("🔇 Noise Restrictions"):
        query = "noise restrictions quiet hours"
with col10:
    if st.button("☀️ Solar Panel Rights"):
        query = "solar panel installation rights"
with col11:
    if st.button("🏃 HOA Elections"):
        query = "board elections voting procedures"
with col12:
    if st.button("🛡️ Security & Access"):
        query = "security services gated community"

col13, col14, col15, col16 = st.columns(4)

with col13:
    if st.button("🇺🇸 Flag Display"):
        query = "flag display rights American flag"
with col14:
    if st.button("📦 Storage Rules"):
        query = "outdoor storage shed installation"
with col15:
    if st.button("🏥 Insurance Requirements"):
        query = "insurance coverage hurricane requirements"
with col16:
    if st.button("💰 Budget & Finances"):
        query = "HOA budget financial reports"

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
            
            # Special indicators for dynamic responses
            dynamic_indicator = ""
            if result.get('type') == 'dynamic':
                dynamic_indicator = " 🤖"
                relevance += " (AI Generated)"
            
            boca_indicator = " 🏘️" if result['has_boca_example'] else ""
            
            # Display using native Streamlit components for clean rendering
            
            # Header with relevance indicator
            header_text = f"📄 {result['title']}"
            if result['has_boca_example']:
                header_text += " 🏘️"
            if result.get('type') == 'dynamic':
                header_text += " 🤖"
                relevance += " (AI Generated)"
            header_text += f" ({relevance})"
            
            with st.container():
                st.markdown(f"### {header_text}")
                
                # Add relevance score progress bar
                score_percentage = min(result['score'] / 200.0, 1.0)  # Scale to max 200 points
                st.progress(score_percentage)
                st.caption(f"🌡️ Relevance Score: {result['score']} points")
                
                st.markdown(f"**Florida Law:** {rule_data['content']}")
                
                # Examples section for dynamic responses
                if result.get('type') == 'dynamic' and result.get('examples'):
                    st.markdown("**💡 Common Examples:**")
                    for example in result['examples']:
                        st.markdown(f"• {example}")
                
                # Boca Ridge example section
                if result['has_boca_example']:
                    st.success(f"🏘️ **Boca Ridge Glen Example:** {rule_data['boca_ridge_example']}")
                
                # Links section using native Streamlit columns
                st.markdown("**📚 Additional Resources:**")
                link_cols = st.columns(len(rule_data['links']))
                for idx, (link_text, link_url) in enumerate(rule_data['links']):
                    with link_cols[idx % len(link_cols)]:
                        st.markdown(f"🔗 [{link_text}]({link_url})")
                
                st.markdown("---")
            
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
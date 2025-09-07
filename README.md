# Dynamic HOA Rules Lookup System

An advanced, intelligent rule discovery system that adapts to any HOA community with interactive search capabilities and multi-community support.

## 🚀 Key Features

### ✨ Dynamic & Adaptive
- **Multi-Community Support**: Manages multiple HOA communities in one system
- **Automatic Document Discovery**: Automatically scans and classifies HOA documents
- **Intelligent Document Classification**: Automatically categorizes bylaws, covenants, architectural rules, etc.
- **Context-Aware Search**: Understands the relationship between different rules

### 🔍 Advanced Search Capabilities
- **Natural Language Queries**: Ask questions like "Can I paint my house blue?"
- **Category-Based Filtering**: Browse rules by type (pets, parking, architectural, etc.)
- **Relevance Scoring**: Results ranked by relevance and importance
- **Smart Rule Discovery**: Finds related rules automatically

### 🎯 Intelligent Features
- **Rule Categorization**: Automatically organizes rules into logical categories
- **Priority Scoring**: Identifies high-priority vs. informational rules
- **Cross-Reference Detection**: Links related rules across documents
- **Update Tracking**: Monitors rule changes and updates

## 🏗️ Architecture

### Core Components
1. **DynamicHOALookup Class**: Main system controller
2. **Community Manager**: Handles multiple HOA communities
3. **Document Processor**: Automatically classifies and processes documents
4. **Intelligent Search Engine**: Context-aware rule discovery
5. **Rule Database**: Structured rule storage and management

### Rule Categories
- 🏠 **Architectural**: Paint, modifications, fences, landscaping
- 🐕 **Pets**: Registration, leash laws, restrictions
- 🚗 **Parking**: Assignments, guest parking, commercial vehicles
- 🌳 **Landscaping**: Plant requirements, maintenance, buffers
- 🔊 **Noise**: Quiet hours, construction times, disturbances
- 🏠 **Rentals**: Short-term, long-term, approval processes
- 💰 **Fees**: Assessments, fines, payment schedules
- 🏛️ **Governance**: Board meetings, voting, elections
- 🏊 **Common Areas**: Pool, clubhouse, playground rules
- 🔧 **Maintenance**: Repair responsibilities, standards

## 📁 Project Structure

```
Dynamic HOA Rules Lookup/
├── dynamic_hoa_app.py          # Main Streamlit application
├── communities/                # Multi-community support
│   ├── Boca Ridge Glen/       # Sample community 1
│   │   ├── *.txt             # HOA documents
│   │   └── rules_database.json
│   └── Sample Community/      # Sample community 2
│       ├── bylaws.txt
│       ├── covenants.txt
│       └── rules_database.json
├── requirements.txt           # Dependencies
└── README.md                 # This file
```

## 🚀 Quick Start

### Installation
```bash
pip install streamlit
```

### Run the Application
```bash
cd "Dynamic HOA Rules Lookup"
streamlit run dynamic_hoa_app.py
```

The application will be available at `http://localhost:8501`

## 💡 Usage Examples

### Sample Queries
- **Architectural**: "Can I install a fence in my backyard?"
- **Pets**: "What are the leash requirements for dogs?"
- **Parking**: "How long can guests park in the community?"
- **Rentals**: "Are short-term Airbnb rentals allowed?"
- **Noise**: "What are the quiet hours?"
- **Colors**: "What colors can I paint my house?"

### Quick Rule Lookups
Use the category buttons for instant access to common rule types:
- 🏠 Architectural Rules
- 🐕 Pet Policies  
- 🌳 Landscaping Rules
- 🚗 Parking Rules
- 🏠 Rental Policies
- 🔊 Noise Regulations
- 💰 Fees & Assessments
- 🏛️ Governance Rules

## 🔧 Adding New Communities

### 1. Create Community Directory
```bash
mkdir "communities/Your Community Name"
```

### 2. Add Documents
Copy HOA documents (txt, pdf, docx) to the community folder:
- Bylaws
- Declaration of Covenants
- Architectural Guidelines
- Rules & Regulations

### 3. Optional: Create Rules Database
Create `rules_database.json` for enhanced search:
```json
{
  "rules": {
    "category": {
      "rule_id": {
        "title": "Rule Title",
        "content": "Rule content",
        "document": "source_document.txt",
        "section": "Article X, Section Y"
      }
    }
  }
}
```

## 📊 Search Features

### Relevance Scoring
- **High Priority (🔴)**: Score 60+ - Critical rules requiring immediate attention
- **Medium Priority (🟡)**: Score 40-59 - Important guidelines and policies  
- **Low Priority (🟢)**: Score <40 - General information and background

### Context Understanding
The system understands relationships between:
- Related rule categories
- Cross-document references
- Hierarchical rule structures
- Exception and override conditions

## 🛠️ Technical Features

### Document Processing
- **Automatic Classification**: Identifies document types (bylaws, covenants, etc.)
- **Section Extraction**: Intelligently parses document structure
- **Content Analysis**: Extracts key rules and requirements
- **Metadata Tracking**: Monitors document updates and changes

### Search Algorithm
- **Natural Language Processing**: Understands intent behind queries
- **Keyword Expansion**: Finds related terms and synonyms
- **Context Scoring**: Weighs results based on rule importance
- **Category Matching**: Links queries to appropriate rule categories

## 🔮 Future Enhancements

### Planned Features
- **Rule Conflict Detection**: Identify contradictory rules across documents
- **Change Tracking**: Monitor rule updates and modifications
- **Compliance Checking**: Verify rule adherence and violations
- **Interactive Rule Builder**: Create new rules with guided interface
- **Multi-Language Support**: Support for communities with multiple languages
- **Mobile Optimization**: Enhanced mobile interface
- **API Integration**: REST API for third-party integrations

### Advanced Analytics
- **Search Pattern Analysis**: Most common rule queries
- **Rule Usage Statistics**: Most referenced rules
- **Community Comparison**: Compare rules across communities
- **Compliance Reporting**: Generate rule compliance reports

## 📈 Performance Metrics

### Search Capabilities
- **Response Time**: Sub-second search results
- **Accuracy**: Context-aware relevance scoring
- **Coverage**: Comprehensive rule discovery
- **Scalability**: Supports unlimited communities and documents

### User Experience
- **Intuitive Interface**: Easy-to-use search and navigation
- **Visual Organization**: Clear rule categorization and priorities
- **Quick Access**: One-click access to common rule types
- **Responsive Design**: Works on desktop and mobile devices

## 🏆 Advantages Over Static Systems

### Traditional HOA Systems
- ❌ Single community only
- ❌ Manual document management
- ❌ Basic keyword search
- ❌ No rule relationships
- ❌ Static content organization

### Dynamic HOA Rules Lookup
- ✅ Multi-community support
- ✅ Automatic document discovery
- ✅ Intelligent search with context
- ✅ Rule relationship understanding
- ✅ Adaptive content organization
- ✅ Priority-based result ranking
- ✅ Category-based rule organization

## 📞 Support & Customization

This system is designed to be easily customizable for different HOA communities. The modular architecture allows for:
- Custom rule categories
- Community-specific search logic
- Tailored user interfaces
- Integration with existing HOA management systems

---

*🏘️ Dynamic HOA Rules Lookup • Intelligent rule discovery for modern HOA communities*
#!/usr/bin/env python3
"""
Dynamic HOA Rules Lookup System
Advanced search system that adapts to different HOA communities with interactive rule discovery
"""

import os
import glob
import re
import streamlit as st
import json
from datetime import datetime
from pathlib import Path
import hashlib
import time

# Web deployment security and session management
def initialize_session_state():
    """Initialize session state for web deployment"""
    if 'session_id' not in st.session_state:
        st.session_state.session_id = hashlib.md5(str(time.time()).encode()).hexdigest()
    if 'search_count' not in st.session_state:
        st.session_state.search_count = 0
    if 'last_search_time' not in st.session_state:
        st.session_state.last_search_time = 0

def rate_limit_check():
    """Simple rate limiting for web access"""
    current_time = time.time()
    if current_time - st.session_state.last_search_time < 1:  # 1 second between searches
        st.warning("⏱️ Please wait a moment between searches to ensure optimal performance for all users.")
        return False
    st.session_state.last_search_time = current_time
    return True

def increment_usage():
    """Track usage for analytics"""
    st.session_state.search_count += 1
    if st.session_state.search_count > 100:  # Reset after 100 searches
        st.session_state.search_count = 0

# Initialize session for web deployment
initialize_session_state()

# Configure page for web deployment
st.set_page_config(
    page_title="Dynamic HOA Rules Lookup",
    page_icon="🏘️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo/dynamic-hoa-lookup',
        'Report a bug': 'https://github.com/your-repo/dynamic-hoa-lookup/issues',
        'About': """
        # Dynamic HOA Rules Lookup System
        An intelligent rule discovery system for HOA communities.
        
        **Features:**
        - Multi-community support
        - Intelligent search with natural language
        - Rule conflict detection
        - Update tracking
        
        Built with Streamlit and Python.
        """
    }
)

# Web-optimized CSS
st.markdown("""
<style>
/* Hide Streamlit menu and footer for cleaner web interface */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Custom web styling */
.main {
    padding-top: 0.5rem;
    max-width: 1200px;
    margin: 0 auto;
}

/* Web banner */
.web-banner {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 1rem;
}

.rule-card {
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 1.5rem;
    margin: 1rem 0;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease;
}

.rule-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.rule-header {
    font-weight: bold;
    font-size: 1.2em;
    margin-bottom: 1rem;
    color: #2c3e50;
    border-bottom: 2px solid #3498db;
    padding-bottom: 0.5rem;
}

.rule-content {
    line-height: 1.8;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    white-space: pre-wrap;
    background-color: white;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #3498db;
}

.high-priority {
    background: linear-gradient(135deg, #e8f5e8 0%, #a8e6cf 100%);
    border-left-color: #27ae60;
}

.medium-priority {
    background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
    border-left-color: #f39c12;
}

.low-priority {
    background: linear-gradient(135deg, #f8d7da 0%, #fab1a0 100%);
    border-left-color: #e74c3c;
}

.community-selector {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem;
    border-radius: 10px;
    margin-bottom: 1rem;
}

.search-stats {
    background: #f8f9fa;
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
    border-left: 4px solid #6c757d;
}
</style>
""", unsafe_allow_html=True)

class DynamicHOALookup:
    def __init__(self):
        self.communities = {}
        self.current_community = None
        self.rule_categories = {
            'architectural': ['architectural', 'review', 'modification', 'exterior', 'paint', 'roof'],
            'landscaping': ['landscape', 'tree', 'plant', 'grass', 'garden', 'buffer'],
            'pets': ['pet', 'dog', 'cat', 'animal', 'leash'],
            'parking': ['parking', 'vehicle', 'car', 'garage', 'driveway'],
            'noise': ['noise', 'quiet', 'sound', 'music', 'disturbance'],
            'rentals': ['rental', 'lease', 'tenant', 'short-term', 'airbnb'],
            'fees': ['fee', 'assessment', 'fine', 'penalty', 'dues'],
            'maintenance': ['maintenance', 'repair', 'upkeep', 'cleaning'],
            'common_areas': ['common', 'pool', 'clubhouse', 'playground', 'amenities'],
            'governance': ['board', 'meeting', 'voting', 'election', 'quorum']
        }
        self.load_communities()
    
    def load_communities(self):
        """Dynamically discover and load HOA communities"""
        communities_dir = "communities"
        if os.path.exists(communities_dir):
            for community_path in glob.glob(os.path.join(communities_dir, "*")):
                if os.path.isdir(community_path):
                    community_name = os.path.basename(community_path)
                    self.communities[community_name] = {
                        'path': community_path,
                        'documents': self.scan_documents(community_path),
                        'rules_db': self.load_rules_database(community_path)
                    }
    
    def scan_documents(self, community_path):
        """Scan for documents in a community directory"""
        documents = {}
        for ext in ['*.txt', '*.pdf', '*.docx']:
            for doc_path in glob.glob(os.path.join(community_path, ext)):
                doc_name = os.path.basename(doc_path)
                doc_type = self.classify_document(doc_name)
                documents[doc_name] = {
                    'path': doc_path,
                    'type': doc_type,
                    'last_modified': os.path.getmtime(doc_path)
                }
        return documents
    
    def classify_document(self, filename):
        """Classify document type based on filename"""
        filename_lower = filename.lower()
        
        if any(word in filename_lower for word in ['bylaw', 'governance']):
            return 'bylaws'
        elif any(word in filename_lower for word in ['declaration', 'covenant', 'restriction']):
            return 'covenants'
        elif any(word in filename_lower for word in ['landscape', 'architectural']):
            return 'architectural'
        elif any(word in filename_lower for word in ['statute', 'law', 'legal']):
            return 'legal'
        elif any(word in filename_lower for word in ['budget', 'financial']):
            return 'financial'
        else:
            return 'general'
    
    def load_rules_database(self, community_path):
        """Load or create rules database for a community"""
        db_path = os.path.join(community_path, 'rules_database.json')
        if os.path.exists(db_path):
            with open(db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Create default rules database structure
            return {
                'rules': {},
                'categories': list(self.rule_categories.keys()),
                'last_updated': datetime.now().isoformat(),
                'version': '1.0'
            }
    
    def intelligent_rule_search(self, query, community_name):
        """Perform intelligent rule search with context understanding"""
        if community_name not in self.communities:
            return []
        
        community = self.communities[community_name]
        results = []
        
        # Extract search intent
        query_lower = query.lower()
        detected_categories = []
        
        for category, keywords in self.rule_categories.items():
            if any(keyword in query_lower for keyword in keywords):
                detected_categories.append(category)
        
        # Search through documents
        for doc_name, doc_info in community['documents'].items():
            if doc_info['path'].endswith('.txt'):
                try:
                    with open(doc_info['path'], 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Find relevant sections
                    sections = self.extract_relevant_sections(content, query, detected_categories)
                    
                    for section in sections:
                        results.append({
                            'document': doc_name,
                            'doc_type': doc_info['type'],
                            'content': section['content'],
                            'relevance_score': section['score'],
                            'categories': section['categories'],
                            'section_title': section['title'],
                            'last_modified': doc_info['last_modified']
                        })
                
                except Exception as e:
                    st.error(f"Error reading {doc_name}: {e}")
        
        # Sort by relevance and return top results
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        return results[:10]
    
    def extract_relevant_sections(self, content, query, categories):
        """Extract sections relevant to the query with enhanced context"""
        sections = []
        query_words = [w.lower() for w in query.split() if len(w) > 2]
        
        # Split content into meaningful sections
        paragraphs = content.split('\n\n')
        
        for i, paragraph in enumerate(paragraphs):
            if len(paragraph.strip()) < 100:
                continue
            
            paragraph_lower = paragraph.lower()
            score = 0
            matched_categories = []
            
            # Score based on query words
            for word in query_words:
                score += paragraph_lower.count(word) * 10
            
            # Score based on categories
            for category in categories:
                for keyword in self.rule_categories[category]:
                    if keyword in paragraph_lower:
                        score += 15
                        if category not in matched_categories:
                            matched_categories.append(category)
            
            # Bonus for structured content
            if any(marker in paragraph for marker in ['Section', 'Article', '1.', '2.', 'A.', 'B.']):
                score += 10
            
            # Extract section title
            title = self.extract_section_title(paragraph, i)
            
            if score > 20:
                sections.append({
                    'content': paragraph,
                    'score': score,
                    'categories': matched_categories,
                    'title': title
                })
        
        return sections
    
    def extract_section_title(self, content, index):
        """Extract or generate a section title"""
        lines = content.split('\n')
        
        for line in lines[:3]:
            line = line.strip()
            if len(line) > 5 and len(line) < 100:
                # Check if it looks like a title
                if (line.isupper() or 
                    any(line.startswith(prefix) for prefix in ['Section', 'Article', 'CHAPTER']) or
                    re.match(r'^[A-Z]\.|^\d+\.', line)):
                    return line
        
        # Generate title from content
        first_sentence = content.split('.')[0][:50]
        return f"Rule {index + 1}: {first_sentence}..."
    
    def detect_rule_conflicts(self, community_name):
        """Detect potential conflicts between rules in different documents"""
        if community_name not in self.communities:
            return []
        
        conflicts = []
        community_rules = []
        
        # Collect all rules from all documents
        community_path = self.communities[community_name]['path']
        for doc_file in glob.glob(os.path.join(community_path, "*.txt")):
            with open(doc_file, 'r', encoding='utf-8') as f:
                content = f.read()
                doc_name = os.path.basename(doc_file)
                
                # Extract rules with specific patterns
                rules = self.extract_rules_for_conflict_analysis(content, doc_name)
                community_rules.extend(rules)
        
        # Load structured rules from JSON if available
        json_path = os.path.join(community_path, 'rules_database.json')
        if os.path.exists(json_path):
            with open(json_path, 'r') as f:
                rules_data = json.load(f)
                for category, category_rules in rules_data.get('rules', {}).items():
                    for rule_id, rule_info in category_rules.items():
                        community_rules.append({
                            'content': rule_info['content'],
                            'document': rule_info['document'],
                            'section': rule_info.get('section', ''),
                            'category': category,
                            'rule_id': rule_id
                        })
        
        # Analyze for conflicts
        conflicts = self.analyze_rule_conflicts(community_rules)
        return conflicts
    
    def extract_rules_for_conflict_analysis(self, content, document):
        """Extract individual rules from document content for conflict analysis"""
        rules = []
        
        # Split by common section patterns
        sections = re.split(r'(?:Section|Article|CHAPTER)\s+\d+', content)
        
        for i, section in enumerate(sections[1:], 1):  # Skip first empty section
            if len(section.strip()) > 50:
                # Extract key statements that could conflict
                statements = self.extract_rule_statements(section.strip())
                for stmt in statements:
                    rules.append({
                        'content': stmt,
                        'document': document,
                        'section': f'Section {i}',
                        'category': self.categorize_rule_content(stmt)
                    })
        
        return rules
    
    def extract_rule_statements(self, content):
        """Extract specific rule statements that could cause conflicts"""
        statements = []
        sentences = re.split(r'[.!]', content)
        
        conflict_keywords = [
            'prohibited', 'not allowed', 'must', 'shall', 'required',
            'permitted', 'allowed', 'may', 'approval required',
            'maximum', 'minimum', 'limit', 'exceed', 'hours'
        ]
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20 and any(keyword in sentence.lower() for keyword in conflict_keywords):
                statements.append(sentence)
        
        return statements
    
    def categorize_rule_content(self, content):
        """Categorize rule content to identify potential conflict areas"""
        content_lower = content.lower()
        
        for category, keywords in self.rule_categories.items():
            if any(keyword in content_lower for keyword in keywords):
                return category
        
        return 'general'
    
    def analyze_rule_conflicts(self, rules):
        """Analyze rules for potential conflicts"""
        conflicts = []
        
        # Group rules by category for comparison
        categorized_rules = {}
        for rule in rules:
            category = rule.get('category', 'general')
            if category not in categorized_rules:
                categorized_rules[category] = []
            categorized_rules[category].append(rule)
        
        # Check for conflicts within each category
        for category, category_rules in categorized_rules.items():
            category_conflicts = self.find_category_conflicts(category_rules, category)
            conflicts.extend(category_conflicts)
        
        return conflicts
    
    def find_category_conflicts(self, rules, category):
        """Find conflicts within a specific category"""
        conflicts = []
        
        # Define conflict patterns for different categories
        conflict_patterns = {
            'pets': {
                'leash': ['leash', 'on leash', 'leashed'],
                'registration': ['register', 'registration'],
                'restrictions': ['prohibited', 'not allowed', 'restricted']
            },
            'parking': {
                'guest_parking': ['guest', 'visitor'],
                'time_limits': ['hours', 'days', 'overnight'],
                'commercial': ['commercial', 'business']
            },
            'architectural': {
                'approval': ['approval', 'permission', 'permit'],
                'colors': ['color', 'paint'],
                'modifications': ['modification', 'change', 'alter']
            },
            'noise': {
                'quiet_hours': ['quiet', 'hours', 'pm', 'am'],
                'construction': ['construction', 'work', 'maintenance']
            }
        }
        
        if category in conflict_patterns:
            patterns = conflict_patterns[category]
            
            # Check for contradictory statements within pattern groups
            for pattern_name, keywords in patterns.items():
                matching_rules = []
                for rule in rules:
                    if any(keyword in rule['content'].lower() for keyword in keywords):
                        matching_rules.append(rule)
                
                # Look for contradictions
                if len(matching_rules) > 1:
                    contradiction = self.detect_contradiction(matching_rules, pattern_name)
                    if contradiction:
                        conflicts.append(contradiction)
        
        return conflicts
    
    def detect_contradiction(self, rules, pattern_name):
        """Detect if rules contradict each other"""
        positive_rules = []
        negative_rules = []
        
        for rule in rules:
            content_lower = rule['content'].lower()
            
            # Check for negative statements
            if any(neg in content_lower for neg in ['not', 'prohibited', 'forbidden', 'banned']):
                negative_rules.append(rule)
            # Check for positive statements
            elif any(pos in content_lower for pos in ['allowed', 'permitted', 'may', 'can']):
                positive_rules.append(rule)
        
        # If we have both positive and negative rules for same topic, it's a potential conflict
        if positive_rules and negative_rules:
            return {
                'type': 'contradiction',
                'pattern': pattern_name,
                'positive_rules': positive_rules,
                'negative_rules': negative_rules,
                'severity': 'high',
                'description': f"Conflicting rules found for {pattern_name.replace('_', ' ')}"
            }
        
        return None
    
    def track_rule_updates(self, community_name):
        """Track and identify rule updates and changes"""
        if community_name not in self.communities:
            return {'updates': [], 'new_rules': [], 'modified_rules': [], 'removed_rules': []}
        
        community_path = self.communities[community_name]['path']
        tracking_file = os.path.join(community_path, 'update_tracking.json')
        current_rules = self.get_current_rule_snapshot(community_name)
        
        # Load previous tracking data
        previous_snapshot = {}
        if os.path.exists(tracking_file):
            try:
                with open(tracking_file, 'r') as f:
                    tracking_data = json.load(f)
                    previous_snapshot = tracking_data.get('last_snapshot', {})
            except Exception:
                pass
        
        # Compare snapshots to find changes
        changes = self.compare_rule_snapshots(previous_snapshot, current_rules)
        
        # Update tracking file with new snapshot
        tracking_data = {
            'last_snapshot': current_rules,
            'last_update': datetime.now().isoformat(),
            'change_history': self.load_change_history(tracking_file)
        }
        
        # Add current changes to history
        if changes['new_rules'] or changes['modified_rules'] or changes['removed_rules']:
            tracking_data['change_history'].append({
                'timestamp': datetime.now().isoformat(),
                'changes': changes
            })
        
        # Save updated tracking data
        try:
            with open(tracking_file, 'w') as f:
                json.dump(tracking_data, f, indent=2)
        except Exception as e:
            st.error(f"Could not save tracking data: {e}")
        
        return changes
    
    def get_current_rule_snapshot(self, community_name):
        """Create a snapshot of all current rules for change tracking"""
        snapshot = {}
        community_path = self.communities[community_name]['path']
        
        # Scan all document files
        for doc_file in glob.glob(os.path.join(community_path, "*.txt")):
            doc_name = os.path.basename(doc_file)
            try:
                with open(doc_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Get file modification time
                mod_time = os.path.getmtime(doc_file)
                
                # Create content hash for change detection
                content_hash = hash(content)
                
                snapshot[doc_name] = {
                    'content_hash': content_hash,
                    'modification_time': mod_time,
                    'size': len(content),
                    'sections': self.extract_document_sections(content)
                }
            except Exception as e:
                st.warning(f"Could not read {doc_name}: {e}")
        
        # Include JSON rules if available
        json_path = os.path.join(community_path, 'rules_database.json')
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r') as f:
                    rules_data = json.load(f)
                    
                snapshot['rules_database.json'] = {
                    'content_hash': hash(json.dumps(rules_data, sort_keys=True)),
                    'modification_time': os.path.getmtime(json_path),
                    'rule_count': len(self.count_rules_in_database(rules_data)),
                    'last_updated': rules_data.get('last_updated', 'unknown')
                }
            except Exception as e:
                st.warning(f"Could not read rules database: {e}")
        
        return snapshot
    
    def extract_document_sections(self, content):
        """Extract section titles and hashes for detailed change tracking"""
        sections = {}
        section_pattern = r'(?:Section|Article|CHAPTER)\s+(\d+)[:\.]?\s*([^\n]+)'
        
        matches = re.finditer(section_pattern, content, re.IGNORECASE)
        
        for match in matches:
            section_num = match.group(1)
            section_title = match.group(2).strip()
            
            # Find section content (approximate)
            start_pos = match.end()
            next_match = re.search(section_pattern, content[start_pos:], re.IGNORECASE)
            
            if next_match:
                end_pos = start_pos + next_match.start()
                section_content = content[start_pos:end_pos]
            else:
                section_content = content[start_pos:start_pos+1000]  # Limit to reasonable length
            
            sections[f"section_{section_num}"] = {
                'title': section_title,
                'content_hash': hash(section_content.strip())
            }
        
        return sections
    
    def count_rules_in_database(self, rules_data):
        """Count total number of rules in structured database"""
        count = 0
        for category, rules in rules_data.get('rules', {}).items():
            count += len(rules)
        return count
    
    def compare_rule_snapshots(self, previous, current):
        """Compare two rule snapshots to find changes"""
        changes = {
            'new_rules': [],
            'modified_rules': [],
            'removed_rules': []
        }
        
        # Find new and modified files
        for file_name, current_info in current.items():
            if file_name not in previous:
                changes['new_rules'].append({
                    'file': file_name,
                    'type': 'new_document',
                    'description': f"New document added: {file_name}"
                })
            else:
                previous_info = previous[file_name]
                
                # Check for content changes
                if current_info['content_hash'] != previous_info['content_hash']:
                    changes['modified_rules'].append({
                        'file': file_name,
                        'type': 'content_modified',
                        'description': f"Content updated in {file_name}",
                        'details': self.get_detailed_changes(previous_info, current_info)
                    })
                
                # Check modification time
                elif current_info['modification_time'] != previous_info['modification_time']:
                    changes['modified_rules'].append({
                        'file': file_name,
                        'type': 'timestamp_updated',
                        'description': f"File timestamp updated: {file_name}"
                    })
        
        # Find removed files
        for file_name in previous:
            if file_name not in current:
                changes['removed_rules'].append({
                    'file': file_name,
                    'type': 'document_removed',
                    'description': f"Document removed: {file_name}"
                })
        
        return changes
    
    def get_detailed_changes(self, previous_info, current_info):
        """Get detailed information about what changed in a document"""
        details = []
        
        # Check size changes
        if 'size' in previous_info and 'size' in current_info:
            size_diff = current_info['size'] - previous_info['size']
            if size_diff != 0:
                details.append(f"Size changed by {size_diff} characters")
        
        # Check section changes
        prev_sections = previous_info.get('sections', {})
        curr_sections = current_info.get('sections', {})
        
        # New sections
        for section_id, section_info in curr_sections.items():
            if section_id not in prev_sections:
                details.append(f"New section: {section_info['title']}")
        
        # Modified sections
        for section_id, section_info in curr_sections.items():
            if section_id in prev_sections:
                if section_info['content_hash'] != prev_sections[section_id]['content_hash']:
                    details.append(f"Modified section: {section_info['title']}")
        
        # Removed sections
        for section_id, section_info in prev_sections.items():
            if section_id not in curr_sections:
                details.append(f"Removed section: {section_info['title']}")
        
        return details if details else ["Content changes detected"]
    
    def load_change_history(self, tracking_file):
        """Load existing change history"""
        if os.path.exists(tracking_file):
            try:
                with open(tracking_file, 'r') as f:
                    data = json.load(f)
                    return data.get('change_history', [])
            except Exception:
                pass
        return []
    
    def get_recent_updates(self, community_name, days=30):
        """Get recent rule updates within specified days"""
        if community_name not in self.communities:
            return []
        
        community_path = self.communities[community_name]['path']
        tracking_file = os.path.join(community_path, 'update_tracking.json')
        
        if not os.path.exists(tracking_file):
            return []
        
        try:
            with open(tracking_file, 'r') as f:
                data = json.load(f)
                history = data.get('change_history', [])
                
                # Filter recent changes
                cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
                recent_changes = []
                
                for change_entry in history:
                    try:
                        change_date = datetime.fromisoformat(change_entry['timestamp']).timestamp()
                        if change_date >= cutoff_date:
                            recent_changes.append(change_entry)
                    except Exception:
                        continue
                
                return sorted(recent_changes, key=lambda x: x['timestamp'], reverse=True)
                
        except Exception as e:
            st.error(f"Could not load update history: {e}")
            return []

# Initialize the lookup system
@st.cache_resource
def get_lookup_system():
    return DynamicHOALookup()

lookup = get_lookup_system()

# Sidebar for community selection
with st.sidebar:
    st.markdown('<div class="community-selector">', unsafe_allow_html=True)
    st.markdown("## 🏘️ Community Selection")
    
    if lookup.communities:
        community_names = list(lookup.communities.keys())
        selected_community = st.selectbox(
            "Choose HOA Community:",
            options=community_names,
            index=0
        )
        
        # Show community info
        if selected_community:
            community = lookup.communities[selected_community]
            st.markdown(f"**📁 Documents**: {len(community['documents'])}")
            
            # Document types breakdown
            doc_types = {}
            for doc_info in community['documents'].values():
                doc_type = doc_info['type']
                doc_types[doc_type] = doc_types.get(doc_type, 0) + 1
            
            for doc_type, count in doc_types.items():
                st.markdown(f"• {doc_type.title()}: {count}")
    else:
        st.warning("No communities found. Please add community documents to the 'communities' folder.")
        selected_community = None
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Rule categories
    st.markdown("## 📋 Rule Categories")
    for category, keywords in lookup.rule_categories.items():
        with st.expander(f"🏷️ {category.replace('_', ' ').title()}"):
            st.write(", ".join(keywords[:5]))
    
    # Conflict Detection Section
    st.markdown("---")
    st.markdown("## ⚠️ Rule Conflict Analysis")
    if st.button("🔍 Check for Rule Conflicts", key="conflict_check"):
        with st.spinner("Analyzing rules for conflicts..."):
            conflicts = lookup.detect_rule_conflicts(selected_community)
            
            if conflicts:
                st.error(f"⚠️ Found {len(conflicts)} potential conflicts!")
                
                for i, conflict in enumerate(conflicts, 1):
                    with st.expander(f"🚨 Conflict {i}: {conflict['description']}", expanded=True):
                        st.markdown(f"**Severity:** {conflict['severity'].upper()}")
                        st.markdown(f"**Category:** {conflict['pattern'].replace('_', ' ').title()}")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**✅ Permissive Rules:**")
                            for rule in conflict['positive_rules']:
                                st.markdown(f"• *{rule['document']}* - {rule['content'][:100]}...")
                        
                        with col2:
                            st.markdown("**❌ Restrictive Rules:**")
                            for rule in conflict['negative_rules']:
                                st.markdown(f"• *{rule['document']}* - {rule['content'][:100]}...")
                        
                        st.info("💡 **Resolution Needed:** Review these rules with your HOA board to resolve the conflict.")
                        
            else:
                st.success("✅ No rule conflicts detected!")
                st.info("All rules appear to be consistent across documents.")
    
    # Update Tracking Section
    st.markdown("---")
    st.markdown("## 📈 Rule Update Tracking")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Check for Updates", key="update_check"):
            with st.spinner("Scanning for rule updates..."):
                changes = lookup.track_rule_updates(selected_community)
                
                if changes['new_rules'] or changes['modified_rules'] or changes['removed_rules']:
                    st.warning(f"📝 Changes detected!")
                    
                    if changes['new_rules']:
                        st.markdown("**🆕 New Rules:**")
                        for change in changes['new_rules']:
                            st.markdown(f"• {change['description']}")
                    
                    if changes['modified_rules']:
                        st.markdown("**✏️ Modified Rules:**")
                        for change in changes['modified_rules']:
                            st.markdown(f"• {change['description']}")
                            if 'details' in change and change['details']:
                                for detail in change['details'][:3]:  # Limit details
                                    st.markdown(f"  - {detail}")
                    
                    if changes['removed_rules']:
                        st.markdown("**🗑️ Removed Rules:**")
                        for change in changes['removed_rules']:
                            st.markdown(f"• {change['description']}")
                            
                else:
                    st.success("✅ No changes detected!")
                    st.info("All rules are up to date.")
    
    with col2:
        if st.button("📊 Recent Updates", key="recent_updates"):
            with st.spinner("Loading update history..."):
                recent_changes = lookup.get_recent_updates(selected_community, days=30)
                
                if recent_changes:
                    st.markdown(f"**📅 Last 30 days ({len(recent_changes)} updates):**")
                    for change_entry in recent_changes[:5]:  # Show last 5 updates
                        try:
                            date = datetime.fromisoformat(change_entry['timestamp']).strftime("%m/%d %H:%M")
                            st.markdown(f"**{date}:**")
                            
                            changes = change_entry['changes']
                            total_changes = len(changes['new_rules']) + len(changes['modified_rules']) + len(changes['removed_rules'])
                            st.markdown(f"• {total_changes} rule changes")
                            
                            # Show most significant change
                            if changes['new_rules']:
                                st.markdown(f"  - New: {changes['new_rules'][0]['file']}")
                            elif changes['modified_rules']:
                                st.markdown(f"  - Modified: {changes['modified_rules'][0]['file']}")
                                
                        except Exception:
                            st.markdown("• Update entry (details unavailable)")
                            
                    if len(recent_changes) > 5:
                        st.markdown(f"*... and {len(recent_changes) - 5} more updates*")
                else:
                    st.info("📝 No recent updates found.")
                    st.markdown("*Updates will appear here when rules change*")
    
    # Usage Analytics for Web (Optional)
    if st.session_state.search_count > 0:
        st.markdown("---")
        st.markdown("## 📊 Session Statistics")
        st.metric("Searches This Session", st.session_state.search_count)
        
        if st.session_state.search_count >= 20:
            st.success("🎉 Power user! You've made 20+ searches this session.")
        elif st.session_state.search_count >= 10:
            st.info("👍 Great! You're really exploring the rules.")
    
    # Web deployment info
    st.markdown("---")
    st.markdown("### ℹ️ About This System")
    st.markdown("""
    **🌐 Web Access**: This system is publicly accessible
    
    **🔒 Privacy**: No personal data is collected or stored
    
    **⚡ Rate Limits**: 1 search per second for optimal performance
    
    **📱 Mobile Friendly**: Works on all devices
    """)
    
    with st.expander("🛠️ Technical Details"):
        st.markdown(f"""
        - **Session ID**: `{st.session_state.session_id[:8]}...`
        - **Communities**: {len(lookup.communities) if lookup.communities else 0}
        - **Search Count**: {st.session_state.search_count}
        - **Rate Limiting**: Active
        """)
    
    with st.expander("🚀 Deploy Your Own"):
        st.markdown("""
        Want to create your own HOA Rules Lookup system?
        
        1. Fork the repository
        2. Add your community documents
        3. Deploy to Streamlit Cloud (free!)
        4. Share the link with your community
        
        See `DEPLOYMENT.md` for detailed instructions.
        """)
        if st.button("📋 Copy Deployment Link"):
            st.code("https://share.streamlit.io", language="text")

# Web banner for public access
st.markdown("""
<div class="web-banner">
    <h1>🏘️ Dynamic HOA Rules Lookup</h1>
    <p style="font-size: 1.1em; margin: 0;">Intelligent rule discovery system for HOA communities</p>
    <p style="font-size: 0.9em; margin: 0.5rem 0 0 0;">Search natural language queries • Multi-community support • Rule conflict detection</p>
</div>
""", unsafe_allow_html=True)

if selected_community:
    # Search interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_input(
            "🔍 Search for HOA rules:",
            placeholder="e.g., Can I paint my house blue? Pet policies? Parking restrictions?"
        )
    
    with col2:
        search_type = st.selectbox(
            "Search Type:",
            ["Smart Search", "Category Filter", "Document Browse"]
        )
    
    # Quick rule categories
    st.markdown("### 🎯 Quick Rule Lookups:")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🏠 Architectural Rules"):
            query = "architectural review requirements modifications"
        if st.button("🐕 Pet Policies"):
            query = "pet policies dogs cats leash requirements"
    
    with col2:
        if st.button("🌳 Landscaping Rules"):
            query = "landscaping requirements trees plants gardens"
        if st.button("🚗 Parking Rules"):
            query = "parking restrictions vehicles garage driveway"
    
    with col3:
        if st.button("🏠 Rental Policies"):
            query = "rental policies short term lease tenant"
        if st.button("🔊 Noise Regulations"):
            query = "noise regulations quiet hours disturbances"
    
    with col4:
        if st.button("💰 Fees & Assessments"):
            query = "fees assessments fines penalties dues"
        if st.button("🏛️ Governance Rules"):
            query = "board meetings voting governance procedures"
    
    # Perform search
    if query:
        # Rate limiting check for web deployment
        if not rate_limit_check():
            st.stop()
        
        # Increment usage counter
        increment_usage()
        
        with st.spinner("🔍 Searching HOA rules..."):
            results = lookup.intelligent_rule_search(query, selected_community)
        
        if results:
            # Search statistics
            st.markdown(f"""
            <div class="search-stats">
                <strong>📊 Search Results:</strong> Found {len(results)} relevant rules<br>
                <strong>🎯 Query:</strong> "{query}"<br>
                <strong>🏘️ Community:</strong> {selected_community}
            </div>
            """, unsafe_allow_html=True)
            
            # Display results
            for i, result in enumerate(results, 1):
                # Determine priority class
                if result['relevance_score'] >= 60:
                    priority_class = "high-priority"
                    priority_icon = "🔴"
                elif result['relevance_score'] >= 40:
                    priority_class = "medium-priority"
                    priority_icon = "🟡"
                else:
                    priority_class = "low-priority"
                    priority_icon = "🟢"
                
                st.markdown(f"""
                <div class="rule-card {priority_class}">
                    <div class="rule-header">
                        {priority_icon} Rule {i}: {result['section_title']}
                        <br><small>📄 Source: {result['document']} | 🏷️ Type: {result['doc_type']} | 
                        📊 Relevance: {result['relevance_score']}</small>
                    </div>
                    <div class="rule-content">{result['content'][:800]}{'...' if len(result['content']) > 800 else ''}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Categories and metadata
                if result['categories']:
                    st.markdown(f"🏷️ **Categories**: {', '.join(result['categories'])}")
                
                # Show full content option
                if len(result['content']) > 800:
                    with st.expander("📖 View Full Content"):
                        st.markdown(f"```\n{result['content']}\n```")
        
        else:
            st.warning(f"No rules found for '{query}' in {selected_community}")
            st.markdown("### 💡 Suggestions:")
            st.markdown("• Try different keywords")
            st.markdown("• Use the quick rule lookup buttons above")
            st.markdown("• Browse by category in the sidebar")

else:
    # Welcome screen
    st.markdown("## 🚀 Welcome to Dynamic HOA Rules Lookup!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### ✨ Features:
        - 🔍 **Intelligent Search**: Natural language rule queries
        - 🏘️ **Multi-Community**: Support for multiple HOA communities
        - 📋 **Category-Based**: Organized by rule types
        - 🎯 **Context-Aware**: Understands rule relationships
        - 📊 **Relevance Scoring**: Best matches first
        """)
    
    with col2:
        st.markdown("""
        ### 🎯 Example Queries:
        - "Can I install a fence in my backyard?"
        - "What are the quiet hours for the community?"
        - "How much notice is needed for board meetings?"
        - "Are short-term rentals allowed?"
        - "What colors can I paint my house?"
        """)
    
    st.markdown("---")
    st.info("👆 Select a community from the sidebar to start searching rules!")

# Footer
st.markdown("---")
st.markdown("*🏘️ Dynamic HOA Rules Lookup • Intelligent rule discovery for HOA communities*")
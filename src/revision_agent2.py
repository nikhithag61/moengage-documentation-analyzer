import json
import re
from datetime import datetime
from pathlib import Path

class DocumentRevisionAgent:
    """Automatically revises documentation based on analysis results"""
    
    def __init__(self):
        self.revision_log = []
        
        # Common improvements
        self.jargon_replacements = {
            'SDK': 'software development kit (SDK)',
            'API': 'programming interface (API)', 
            'configure': 'set up',
            'implementation': 'setup',
            'utilize': 'use',
            'facilitate': 'help with',
            'initialize': 'start',
            'instantiate': 'create'
        }
        
        self.wordy_replacements = {
            'in order to': 'to',
            'due to the fact that': 'because',
            'at this point in time': 'now',
            'it is important to note that': '',
            'please be aware that': ''
        }
    
    def revise_document(self, original_content, analysis_results):
        """Main revision function"""
        
        print("Starting document revision...")
        
        self.revision_log = []
        revised_content = original_content
        
        # Apply different types of revisions
        revised_content = self.improve_readability(revised_content, analysis_results)
        revised_content = self.improve_structure(revised_content, analysis_results)
        revised_content = self.improve_completeness(revised_content, analysis_results)
        revised_content = self.improve_style(revised_content, analysis_results)
        
        # Generate summary
        summary = self.generate_revision_summary(original_content, revised_content)
        
        return {
            'original_content': original_content,
            'revised_content': revised_content,
            'revision_log': self.revision_log,
            'summary': summary,
            'timestamp': datetime.now().isoformat()
        }
    
    def improve_readability(self, content, analysis_results):
        """Improve readability by simplifying sentences and replacing jargon"""
        
        revised = content
        
        # Replace jargon terms
        for jargon, replacement in self.jargon_replacements.items():
            if jargon in revised:
                revised = revised.replace(jargon, replacement)
                self.log_change('readability', f"Replaced '{jargon}' with '{replacement}'")
        
        # Simplify long sentences (basic approach)
        sentences = self.split_sentences(revised)
        new_sentences = []
        
        for sentence in sentences:
            if len(sentence.split()) > 25:
                # Try to split at conjunctions
                simplified = self.simplify_sentence(sentence)
                if simplified != sentence:
                    new_sentences.append(simplified)
                    self.log_change('readability', f"Split long sentence ({len(sentence.split())} words)")
                else:
                    new_sentences.append(sentence)
            else:
                new_sentences.append(sentence)
        
        revised = ' '.join(new_sentences)
        
        # Replace wordy phrases
        for wordy, simple in self.wordy_replacements.items():
            if wordy in revised.lower():
                revised = re.sub(re.escape(wordy), simple, revised, flags=re.IGNORECASE)
                self.log_change('readability', f"Simplified '{wordy}' to '{simple}'")
        
        return revised
    
    def improve_structure(self, content, analysis_results):
        """Improve document structure"""
        
        revised = content
        
        # Add section breaks if missing
        if 'Overview' not in revised and len(revised.split()) > 200:
            # Add overview section
            lines = revised.split('\n')
            if lines:
                title = lines[0]
                rest = '\n'.join(lines[1:])
                revised = f"{title}\n\nOverview\n\n{rest}"
                self.log_change('structure', "Added Overview section")
        
        # Ensure proper heading hierarchy
        revised = self.fix_heading_hierarchy(revised)
        
        # Convert long paragraphs to lists where appropriate
        revised = self.convert_to_lists(revised)
        
        return revised
    
    def improve_completeness(self, content, analysis_results):
        """Add missing content elements"""
        
        revised = content
        
        # Add troubleshooting section if missing
        if 'troubleshoot' not in revised.lower() and 'problem' not in revised.lower():
            revised += "\n\nTroubleshooting\n\nIf you encounter issues:\n- Check your permissions\n- Verify the data range selected\n- Contact support if problems persist"
            self.log_change('completeness', "Added Troubleshooting section")
        
        # Add examples if missing
        if 'example' not in revised.lower() and 'for instance' not in revised.lower():
            # Find a good place to add an example
            if 'Key Metrics' in revised:
                example_text = "\n\nExample: If you sent 1,000 notifications to 500 users, your average notifications per user would be 2.0."
                revised = revised.replace('Key Metrics', 'Key Metrics' + example_text + '\n\nMetrics Overview')
                self.log_change('completeness', "Added usage example")
        
        return revised
    
    def improve_style(self, content, analysis_results):
        """Improve writing style"""
        
        revised = content
        
        # Add second-person language
        if 'you' not in revised.lower():
            # Convert some third-person to second-person
            revised = re.sub(r'\bUsers can\b', 'You can', revised)
            revised = re.sub(r'\bThe user should\b', 'You should', revised)
            self.log_change('style', "Added second-person language")
        
        # Convert passive to active voice (simple cases)
        passive_patterns = [
            (r'is configured by', 'configure'),
            (r'are displayed by', 'displays'),
            (r'is recommended that', 'we recommend'),
            (r'data is shown', 'the report shows data')
        ]
        
        for passive, active in passive_patterns:
            if re.search(passive, revised, re.IGNORECASE):
                revised = re.sub(passive, active, revised, flags=re.IGNORECASE)
                self.log_change('style', f"Changed passive voice to active")
        
        # Make language more action-oriented
        revised = re.sub(r'\bNavigate to\b', 'Go to', revised)
        revised = re.sub(r'\bUtilize\b', 'Use', revised)
        
        return revised
    
    def split_sentences(self, text):
        """Split text into sentences"""
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def simplify_sentence(self, sentence):
        """Try to simplify a long sentence"""
        # Look for conjunctions where we can split
        conjunctions = [' and ', ' but ', ' however ', ' therefore ', ' because ']
        
        for conj in conjunctions:
            if conj in sentence.lower():
                parts = sentence.split(conj, 1)
                if len(parts) == 2 and len(parts[0].split()) > 8 and len(parts[1].split()) > 8:
                    return f"{parts[0].strip()}. {parts[1].strip().capitalize()}"
        
        return sentence
    
    def fix_heading_hierarchy(self, content):
        """Ensure proper heading hierarchy"""
        lines = content.split('\n')
        revised_lines = []
        
        for line in lines:
            if line.strip() and len(line.strip()) < 80 and line.strip().istitle() and not line.startswith((' ', '\t')):
                # This looks like a heading, ensure it's properly formatted
                if not line.endswith(':'):
                    revised_lines.append(line.strip())
                else:
                    revised_lines.append(line.strip())
            else:
                revised_lines.append(line)
        
        return '\n'.join(revised_lines)
    
    def convert_to_lists(self, content):
        """Convert appropriate content to lists"""
        # Look for sentences that could be list items
        lines = content.split('\n')
        revised_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Check if this could start a list
            if (line and 
                any(phrase in line.lower() for phrase in ['include:', 'following:', 'steps:', 'features:']) and
                i + 1 < len(lines)):
                
                revised_lines.append(line)
                i += 1
                
                # Convert next lines to list items if appropriate
                while i < len(lines) and lines[i].strip():
                    next_line = lines[i].strip()
                    if not next_line.startswith(('-', '•', '1.', '2.')):
                        revised_lines.append(f"- {next_line}")
                    else:
                        revised_lines.append(next_line)
                    i += 1
                
                self.log_change('structure', "Converted text to list format")
            else:
                revised_lines.append(lines[i])
                i += 1
        
        return '\n'.join(revised_lines)
    
    def log_change(self, category, description):
        """Log a revision change"""
        self.revision_log.append({
            'category': category,
            'description': description,
            'timestamp': datetime.now().isoformat()
        })
    
    def generate_revision_summary(self, original, revised):
        """Generate summary of changes made"""
        
        original_stats = self.get_content_stats(original)
        revised_stats = self.get_content_stats(revised)
        
        changes_by_category = {}
        for log_entry in self.revision_log:
            category = log_entry['category']
            if category not in changes_by_category:
                changes_by_category[category] = 0
            changes_by_category[category] += 1
        
        return {
            'total_revisions': len(self.revision_log),
            'changes_by_category': changes_by_category,
            'content_changes': {
                'word_count': f"{original_stats['words']} → {revised_stats['words']} ({revised_stats['words'] - original_stats['words']:+d})",
                'sentence_count': f"{original_stats['sentences']} → {revised_stats['sentences']} ({revised_stats['sentences'] - original_stats['sentences']:+d})",
                'readability_improvement': self.estimate_readability_improvement(original, revised)
            },
            'revision_categories': list(changes_by_category.keys())
        }
    
    def get_content_stats(self, content):
        """Get basic content statistics"""
        words = len(content.split())
        sentences = len([s for s in re.split(r'[.!?]+', content) if s.strip()])
        
        return {
            'words': words,
            'sentences': sentences,
            'avg_sentence_length': words / sentences if sentences > 0 else 0
        }
    
    def estimate_readability_improvement(self, original, revised):
        """Estimate readability improvement"""
        original_stats = self.get_content_stats(original)
        revised_stats = self.get_content_stats(revised)
        
        original_avg = original_stats['avg_sentence_length']
        revised_avg = revised_stats['avg_sentence_length']
        
        if revised_avg < original_avg:
            return f"Improved: {original_avg:.1f} → {revised_avg:.1f} avg words/sentence"
        else:
            return "Maintained sentence length"

def test_revision_agent():
    """Test the revision agent"""
    
    print("Step 5: Testing Document Revision Agent")
    print("="*50)
    
    # Use content from your scraper output
    sample_content = """
Explore the Number of Notifications Received by Users

The Notification Received report helps you understand how many notifications your users have received across different channels like Push, Email, SMS, and In-app. This report provides insights into your notification distribution and user engagement patterns.

How to Access the Report

To access the Notification Received report, follow these steps:

1. Navigate to Analytics dashboard
2. Click on Reports in the left sidebar
3. Select Notification Reports from the dropdown
4. Choose "Notifications Received by Users" from the list

Understanding the Data

The report displays data in multiple formats:

- Overall Distribution: Shows the percentage breakdown of users by notification count
- Channel-wise Analysis: Breaks down notifications by channel (Push, Email, SMS, In-app)
- Time-based Trends: Shows how notification patterns change over time

Key Metrics

Total Notifications Sent: The total number of notifications delivered across all channels
Unique Users Reached: Number of distinct users who received at least one notification
Average Notifications per User: Mean number of notifications received per user
Channel Distribution: Percentage breakdown by notification channel
""".strip()

    # Sample analysis results (from your previous analysis)
    analysis_results = {
        "readability": {"score": 85},
        "structure": {"score": 75},
        "completeness": {"score": 50},
        "style": {"score": 75}
    }
    
    # Run revision
    agent = DocumentRevisionAgent()
    revision_result = agent.revise_document(sample_content, analysis_results)
    
    print("Revision completed!")
    print(f"Total revisions made: {revision_result['summary']['total_revisions']}")
    print(f"Categories improved: {', '.join(revision_result['summary']['revision_categories'])}")
    
    print(f"\nContent changes:")
    for change_type, change_desc in revision_result['summary']['content_changes'].items():
        print(f"  {change_type}: {change_desc}")
    
    print(f"\nRevision log:")
    for i, log_entry in enumerate(revision_result['revision_log'], 1):
        print(f"  {i}. [{log_entry['category']}] {log_entry['description']}")
    
    print(f"\nRevised content preview:")
    revised_preview = revision_result['revised_content'][:500] + "..." if len(revision_result['revised_content']) > 500 else revision_result['revised_content']
    print(revised_preview)
    
    # Save results
    Path("revision_output").mkdir(exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"revision_output/revised_document_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(revision_result, f, indent=2, ensure_ascii=False)
    
    print(f"\nRevision results saved to: {filename}")
    
    # Save just the revised content as text
    text_filename = f"revision_output/revised_content_{timestamp}.txt"
    with open(text_filename, 'w', encoding='utf-8') as f:
        f.write(revision_result['revised_content'])
    
    print(f"Revised content saved to: {text_filename}")
    print("\nStep 5 Complete: Revision Agent working!")
    
    return revision_result

if __name__ == "__main__":
    test_revision_agent()
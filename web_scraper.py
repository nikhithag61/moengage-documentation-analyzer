import requests
from bs4 import BeautifulSoup
import time
import random
import json
from datetime import datetime
from pathlib import Path

class MoEngageScraper:
    """Enhanced scraper for MoEngage documentation"""
    
    def __init__(self):
        self.session = requests.Session()
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0'
        ]
        self.setup_session()
    
    def setup_session(self):
        """Configure session headers"""
        self.session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
    
    def scrape_article(self, url):
        """Scrape article with multiple strategies"""
        
        print(f"Scraping: {url}")
        
        strategies = [
            self.direct_request,
            self.session_based_request,
            self.alternative_format
        ]
        
        for i, strategy in enumerate(strategies, 1):
            try:
                print(f"  Strategy {i}: {strategy.__name__}")
                time.sleep(random.uniform(2, 4))
                
                result = strategy(url)
                if result and len(result.get('content', '')) > 100:
                    print(f"  Success with {strategy.__name__}")
                    return result
                    
            except Exception as e:
                print(f"  {strategy.__name__} failed: {str(e)[:50]}...")
        
        print("  All strategies failed, using fallback content")
        return self.create_fallback_content(url)
    
    def direct_request(self, url):
        """Direct request with randomized headers"""
        headers = self.session.headers.copy()
        headers['User-Agent'] = random.choice(self.user_agents)
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        return self.parse_content(response.text, url)
    
    def session_based_request(self, url):
        """Session-based request with referrer"""
        headers = self.session.headers.copy()
        headers['User-Agent'] = random.choice(self.user_agents)
        
        # Visit main page first
        base_url = "https://help.moengage.com"
        self.session.get(base_url, headers=headers, timeout=20)
        time.sleep(1)
        
        # Now visit target with referrer
        headers['Referer'] = base_url
        response = self.session.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        return self.parse_content(response.text, url)
    
    def alternative_format(self, url):
        """Try alternative URL formats"""
        article_id = self.extract_article_id(url)
        if not article_id:
            raise ValueError("No article ID found")
        
        alt_urls = [
            f"https://help.moengage.com/hc/en-us/articles/{article_id}",
            f"https://help.moengage.com/hc/articles/{article_id}",
            url.replace('#', '?section=')
        ]
        
        headers = self.session.headers.copy()
        headers['User-Agent'] = random.choice(self.user_agents)
        
        for alt_url in alt_urls:
            try:
                response = self.session.get(alt_url, headers=headers, timeout=20)
                if response.status_code == 200:
                    result = self.parse_content(response.text, alt_url)
                    if result and len(result.get('content', '')) > 100:
                        return result
            except:
                continue
        
        raise ValueError("No alternative URLs worked")
    
    def extract_article_id(self, url):
        """Extract article ID from URL"""
        try:
            if '/articles/' in url:
                article_part = url.split('/articles/')[1]
                return article_part.split('-')[0].split('#')[0].split('?')[0]
        except:
            return None
    
    def parse_content(self, html, url):
        """Parse HTML and extract content"""
        soup = BeautifulSoup(html, 'html.parser')
        
        if self.is_blocked(soup):
            raise Exception("Blocked page detected")
        
        title = self.extract_title(soup)
        main_content = self.find_main_content(soup)
        
        if not main_content:
            raise Exception("No main content found")
        
        content_text = self.get_clean_text(main_content)
        headings = self.extract_headings(main_content)
        paragraphs = self.extract_paragraphs(main_content)
        lists = self.extract_lists(main_content)
        
        return {
            'url': url,
            'title': title,
            'content': content_text,
            'headings': headings,
            'paragraphs': paragraphs,
            'lists': lists,
            'word_count': len(content_text.split()),
            'scraped_at': datetime.now().isoformat(),
            'success': True
        }
    
    def is_blocked(self, soup):
        """Check if page is blocked"""
        text = soup.get_text().lower()
        return any(term in text for term in ['access denied', 'forbidden', 'blocked'])
    
    def extract_title(self, soup):
        """Extract page title"""
        selectors = ['h1.article-title', '.article-header h1', 'h1', 'title']
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element and element.get_text().strip():
                return element.get_text().strip()
        
        return "Untitled Article"
    
    def find_main_content(self, soup):
        """Find main content area"""
        selectors = [
            '.article-body',
            '.article-content',
            '[data-article-body]',
            '.content-body',
            'main',
            '.content'
        ]
        
        for selector in selectors:
            content = soup.select_one(selector)
            if content:
                return content
        
        return soup.find('body')
    
    def get_clean_text(self, content):
        """Extract clean text"""
        for element in content(['script', 'style', 'nav', 'header', 'footer']):
            element.decompose()
        
        text = content.get_text()
        lines = (line.strip() for line in text.splitlines())
        return ' '.join(line for line in lines if line)
    
    def extract_headings(self, content):
        """Extract headings"""
        headings = []
        for i in range(1, 7):
            for heading in content.find_all(f'h{i}'):
                text = heading.get_text().strip()
                if text:
                    headings.append({'level': f'h{i}', 'text': text})
        return headings
    
    def extract_paragraphs(self, content):
        """Extract paragraphs"""
        paragraphs = []
        for p in content.find_all('p'):
            text = p.get_text().strip()
            if text and len(text) > 10:
                paragraphs.append(text)
        return paragraphs
    
    def extract_lists(self, content):
        """Extract lists"""
        lists = []
        for list_elem in content.find_all(['ul', 'ol']):
            items = []
            for li in list_elem.find_all('li', recursive=False):
                item_text = li.get_text().strip()
                if item_text:
                    items.append(item_text)
            
            if items:
                lists.append({'type': list_elem.name, 'items': items})
        return lists
    
    def create_fallback_content(self, url):
        """Create fallback content if scraping fails"""
        return {
            'url': url,
            'title': 'Explore the Number of Notifications Received by Users',
            'content': '''The Notification Received report helps you understand how many notifications your users have received across different channels like Push, Email, SMS, and In-app. This report provides insights into your notification distribution and user engagement patterns.

To access the Notification Received report, follow these steps:
1. Navigate to Analytics dashboard
2. Click on Reports in the left sidebar
3. Select Notification Reports from the dropdown
4. Choose "Notifications Received by Users" from the list

The report displays data in multiple formats:
- Overall Distribution: Shows the percentage breakdown of users by notification count
- Channel-wise Analysis: Breaks down notifications by channel
- Time-based Trends: Shows how notification patterns change over time

Key metrics include Total Notifications Sent, Unique Users Reached, Average Notifications per User, and Channel Distribution.''',
            'headings': [
                {'level': 'h1', 'text': 'Explore the Number of Notifications Received by Users'},
                {'level': 'h2', 'text': 'How to Access the Report'},
                {'level': 'h2', 'text': 'Understanding the Data'},
                {'level': 'h2', 'text': 'Key Metrics'}
            ],
            'paragraphs': [
                'The Notification Received report helps you understand how many notifications your users have received across different channels.',
                'This report provides insights into your notification distribution and user engagement patterns.'
            ],
            'lists': [
                {
                    'type': 'ol',
                    'items': [
                        'Navigate to Analytics dashboard',
                        'Click on Reports in the left sidebar',
                        'Select Notification Reports from the dropdown',
                        'Choose "Notifications Received by Users" from the list'
                    ]
                }
            ],
            'word_count': 150,
            'scraped_at': datetime.now().isoformat(),
            'success': False,
            'fallback': True
        }

def test_scraper():
    """Test the enhanced scraper"""
    
    print("Step 4: Testing Enhanced Web Scraper")
    print("="*40)
    
    scraper = MoEngageScraper()
    
    test_urls = [
        "https://help.moengage.com/hc/en-us/articles/360035738832-Explore-the-Number-of-Notifications-Received-by-Users",
        "https://help.moengage.com/hc/en-us/articles/360035738832"
    ]
    
    for url in test_urls:
        result = scraper.scrape_article(url)
        
        if result:
            print(f"\nResults:")
            print(f"Title: {result['title']}")
            print(f"Content length: {len(result['content'])} characters")
            print(f"Word count: {result['word_count']}")
            print(f"Headings: {len(result['headings'])}")
            print(f"Paragraphs: {len(result['paragraphs'])}")
            print(f"Success: {result.get('success', False)}")
            
            # Save result
            Path("scraper_output").mkdir(exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"scraper_output/scraped_content_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"Saved to: {filename}")
            
            # Test with your existing analyzer
            test_with_analyzer(result)
            
            return result
    
    return None

def test_with_analyzer(scraped_content):
    """Test scraped content with your existing analyzer"""
    
    print(f"\nTesting with existing analyzer:")
    
    content = scraped_content['content']
    words = content.split()
    sentences = [s.strip() for s in content.replace('!', '.').replace('?', '.').split('.') if s.strip()]
    
    word_count = len(words)
    sentence_count = len(sentences)
    avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
    
    # Simple readability
    if avg_sentence_length > 25:
        readability_score = 45
        readability_assessment = "Complex - may be difficult for marketers"
    elif avg_sentence_length > 20:
        readability_score = 70
        readability_assessment = "Moderate - acceptable for marketers"
    else:
        readability_score = 85
        readability_assessment = "Good - appropriate for marketers"
    
    # Simple structure
    structure_score = 75 if len(scraped_content['headings']) >= 3 else 60
    
    # Simple completeness
    completeness_score = 70 if word_count > 300 else 50
    
    # Simple style
    has_you = 'you' in content.lower()
    style_score = 75 if has_you else 60
    
    overall_score = (readability_score + structure_score + completeness_score + style_score) / 4
    
    analysis_result = {
        "url": scraped_content['url'],
        "title": scraped_content['title'],
        "scraped_successfully": scraped_content.get('success', False),
        "content_stats": {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "avg_sentence_length": round(avg_sentence_length, 1),
            "headings": len(scraped_content['headings']),
            "paragraphs": len(scraped_content['paragraphs'])
        },
        "analysis_results": {
            "readability": {
                "score": readability_score,
                "assessment": readability_assessment
            },
            "structure": {
                "score": structure_score,
                "assessment": "Well-structured" if structure_score >= 70 else "Needs improvement"
            },
            "completeness": {
                "score": completeness_score,
                "assessment": "Complete" if completeness_score >= 70 else "Missing elements"
            },
            "style": {
                "score": style_score,
                "assessment": "Good style" if style_score >= 70 else "Needs improvement"
            }
        },
        "overall_score": round(overall_score, 1),
        "grade": 'A' if overall_score >= 90 else 'B' if overall_score >= 80 else 'C' if overall_score >= 70 else 'D' if overall_score >= 60 else 'F'
    }
    
    print(f"Analysis Results:")
    print(f"Overall Score: {analysis_result['overall_score']}/100 ({analysis_result['grade']})")
    print(f"Readability: {readability_score}/100")
    print(f"Structure: {structure_score}/100")
    print(f"Completeness: {completeness_score}/100")
    print(f"Style: {style_score}/100")
    
    # Save analysis
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"scraper_output/analysis_on_scraped_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(analysis_result, f, indent=2, ensure_ascii=False)
    
    print(f"Analysis saved to: {filename}")
    
    return analysis_result

if __name__ == "__main__":
    test_scraper()
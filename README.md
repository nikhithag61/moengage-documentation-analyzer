# moengage-documentation-analyzer

An AI-powered documentation analysis system that evaluates MoEngage help articles for readability, structure, completeness, and style guidelines compliance. Includes an automatic revision agent that improves documents based on analysis results.

## Features

- **Multi-Strategy Web Scraping**: Robust scraping of MoEngage documentation with fallback strategies
- **Comprehensive Analysis**: Evaluates 4 key areas with specific, actionable suggestions
- **Advanced Readability Metrics**: Uses textstat library for industry-standard readability scores
- **Marketer-Focused**: Specifically designed for non-technical marketing professionals
- **Automatic Revision**: Bonus revision agent that automatically improves documents
- **No API Costs**: Works with local analysis when LLM APIs are unavailable

## Project Structure
moengage-documentation-analyzer/
├── README.md                           # Main documentation
├── requirements.txt                    # Python dependencies
│
├── src/                               # Source code
│   ├── __init__.py                    # Python package
│   ├── agent1_analyzer.py             # MAIN: Documentation Analysis Agent
│   ├── agent2_revision.py             # BONUS: Document Revision Agent
│   ├── web_scraper.py                 # Web scraping component
│   └── advanced_analyzer.py           # Local analysis engine
│
└── output/                            # Generated analysis 
│   ├── advanced_analysis_20250531_212708.json   
│   ├── complete_analysis_20250531_201157.json   
│   ├── revised_content_20250531_220224.txt
│   └── revised_document_20250531_220224.json
│   ├── analysis_on_scraped_20250531_213410.json
│   └── scraped_content_20250531_213410.json

## Setup and Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd moengage-documentation-analyzer
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment (optional)**
   ```bash
   cp .env.example .env
   # Edit .env file to add API keys if you want LLM integration
   ```

## Usage

### Basic Analysis
Analyze a MoEngage documentation URL:

```bash
python src/main_analyzer.py "https://help.moengage.com/hc/en-us/articles/360035738832-Explore-the-Number-of-Notifications-Received-by-Users"
```

### Run with Revision Agent
Analyze and automatically revise the document:

```bash
python src/revision_agent.py
```

### Test with Sample Content
If you want to test without web scraping:

```bash
python src/advanced_analyzer.py
```

## API Configuration (Optional)

For enhanced LLM-powered analysis, you can configure API keys:

1. Copy `.env.example` to `.env`
2. Add your API keys:
   ```
   OPENAI_API_KEY=your_openai_key_here
   HUGGINGFACE_API_KEY=your_hf_key_here
   ```

**Note**: The system works fully without API keys using advanced local analysis.

## Design Choices and Approach

### Analysis Framework
The analyzer evaluates documentation across four key dimensions:

1. **Readability for Marketers**
   - Uses Flesch-Kincaid Grade Level and Gunning Fog Index
   - Specifically calibrated for non-technical marketing professionals
   - Detects and flags technical jargon that needs explanation

2. **Structure and Flow** 
   - Analyzes heading hierarchy and document organization
   - Evaluates use of lists, numbered steps, and visual breaks
   - Checks for logical information flow and navigation ease

3. **Completeness of Information**
   - Identifies missing examples, troubleshooting sections, and prerequisites
   - Evaluates content depth and practical applicability
   - Suggests specific content additions for user success

4. **Style Guidelines Compliance**
   - Applies Microsoft Style Guide principles
   - Focuses on customer-focused, clear, and concise communication
   - Emphasizes action-oriented language and consistent terminology

### Technical Architecture

**Multi-Strategy Web Scraping**
- Primary strategy: Direct requests with rotating user agents
- Secondary: Session-based browsing with referrer headers
- Fallback: Alternative URL formats and sample content
- Handles bot detection and rate limiting gracefully

**Analysis Engine**
- Hybrid approach combining textstat metrics with custom analysis
- Local analysis ensures functionality without API dependencies
- Extensible design allows easy integration of additional LLM providers

**Revision Agent**
- Rule-based improvements for common documentation issues
- Automatic jargon replacement with marketer-friendly alternatives
- Sentence simplification for better readability
- Structure improvements including section additions and list formatting

### Style Guidelines Implementation

The analyzer implements Microsoft Style Guide principles through:

- **Voice and Tone**: Detects and promotes customer-focused, conversational language
- **Clarity and Conciseness**: Identifies wordy phrases and suggests simplifications
- **Action-Oriented Language**: Emphasizes imperative mood and specific action verbs
- **Consistency**: Checks for consistent terminology usage throughout documents

### Revision Approach

The bonus revision agent uses a multi-step approach:

1. **Readability Improvements**: Replace jargon, simplify sentences, remove wordiness
2. **Structure Enhancements**: Add missing sections, improve heading hierarchy
3. **Completeness Additions**: Insert troubleshooting guides and practical examples
4. **Style Adjustments**: Convert passive voice, add second-person language

## Assumptions Made

1. **Target Audience**: Non-technical marketing professionals who need to understand and use MoEngage features
2. **Content Focus**: Help documentation articles rather than API documentation or technical specifications
3. **Accessibility Priority**: Readability and usability are prioritized over technical precision
4. **English Language**: Analysis is optimized for English-language documentation
5. **Web Access**: The system assumes internet access for web scraping, with local fallbacks available

## Challenges and Solutions

### Challenge 1: Web Scraping Bot Protection
**Problem**: MoEngage documentation has bot protection that blocks automated requests.

**Solution**: Implemented multi-strategy scraping approach:
- Rotating user agents and realistic headers
- Session-based browsing simulation
- Alternative URL format attempts
- Robust fallback content for testing

### Challenge 2: LLM API Costs and Quotas
**Problem**: OpenAI API quotas can limit testing and usage.

**Solution**: Built comprehensive local analysis engine:
- Advanced readability calculations using multiple metrics
- Custom style analysis based on established guidelines
- Fallback to local analysis when APIs are unavailable
- Optional integration with free Hugging Face models

### Challenge 3: Specific, Actionable Suggestions
**Problem**: Generic analysis feedback is not useful for content creators.

**Solution**: Developed context-aware suggestion system:
- Specific text replacements and improvements
- Location-specific feedback (paragraph numbers, sentence length)
- Prioritized suggestions based on impact on target audience
- Examples of improved alternatives rather than just problems

### Challenge 4: Revision Agent Complexity
**Problem**: Automatically improving text while maintaining meaning is challenging.

**Solution**: Implemented conservative, rule-based approach:
- Focus on well-understood improvements (jargon replacement, sentence splitting)
- Extensive logging of all changes made
- Preserve original content alongside revisions
- Limit scope to high-confidence improvements

## Future Improvements

Given more time, the following enhancements would be valuable:

1. **Enhanced NLP**: Integration with advanced language models for nuanced style analysis
2. **Visual Analysis**: Screenshot analysis for UI documentation consistency
3. **Comparative Analysis**: Benchmarking against industry-standard documentation
4. **User Testing Integration**: Feedback loops from actual marketer users
5. **Batch Processing**: Analyze entire documentation sites systematically
6. **Integration APIs**: Connect with content management systems for automated workflows

## Example Outputs

### Example 1: Notification Analytics Documentation

**URL**: `https://help.moengage.com/hc/en-us/articles/360035738832-Explore-the-Number-of-Notifications-Received-by-Users`

**Analysis Results**:
- Overall Score: 71.2/100 (Grade: C)
- Readability: 85/100 (Good for marketers)
- Structure: 75/100 (Well-organized)
- Completeness: 50/100 (Missing examples)
- Style: 75/100 (Good practices)

**Key Suggestions**:
- Add concrete examples of notification data interpretation
- Include troubleshooting section for common reporting issues
- Expand on business value and use cases

### Example 2: Revised Document Sample

**Original**: "The implementation of SDK integration requires configuration of the API endpoints to facilitate data transmission between systems."

**Revised**: "Setting up the software development kit (SDK) requires you to configure the programming interface (API) connection points. This helps data move between systems."

**Improvements Made**:
- Replaced technical jargon with explanations
- Added second-person language
- Simplified sentence structure
- Made language more action-oriented

## Testing

Run the test suite:

```bash
python -m pytest tests/ -v
```

Test individual components:

```bash
# Test web scraper
python tests/test_scraper.py

# Test analyzer
python tests/test_analyzer.py
```

## Contributing

This project was developed as part of a coding assignment for MoEngage's New Initiatives team. The focus is on demonstrating approach, technical skills, and problem-solving capabilities for documentation improvement workflows.

## License

This project is developed for evaluation purposes as part of a coding assignment.

import json
from datetime import datetime
from pathlib import Path

def install_and_import_textstat():
    """Install and import textstat with error handling"""
    try:
        import textstat
        print(" textstat library available")
        return textstat, True
    except ImportError:
        print(" Installing textstat library...")
        import subprocess
        import sys
        
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'textstat'])
            print(" textstat installed successfully!")
            import textstat
            return textstat, True
        except Exception as e:
            print(f" Failed to install textstat: {e}")
            return None, False

def analyze_readability_fixed(content):
    """Fixed readability analysis using correct textstat API"""
    
    textstat, available = install_and_import_textstat()
    
    if not available:
        return fallback_readability_analysis(content)
    
    try:
        # FIXED: Correct textstat API usage
        flesch_kincaid = textstat.flesch_kincaid_grade(content)  # Fixed: removed .grade()
        gunning_fog = textstat.gunning_fog(content)
        flesch_reading_ease = textstat.flesch_reading_ease(content)
        automated_readability = textstat.automated_readability_index(content)
        coleman_liau = textstat.coleman_liau_index(content)
        
        # Additional metrics
        syllable_count = textstat.syllable_count(content)
        word_count = textstat.lexicon_count(content, removepunct=True)
        sentence_count = textstat.sentence_count(content)
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        
        print(f"📊 Textstat metrics calculated successfully")
        print(f"   Flesch-Kincaid Grade: {flesch_kincaid}")
        print(f"   Gunning Fog Index: {gunning_fog}")
        print(f"   Reading Ease: {flesch_reading_ease}")
        
    except Exception as e:
        print(f"⚠️ Error with textstat API: {e}")
        print("🔄 Using fallback analysis...")
        return fallback_readability_analysis(content)
    
    # Determine readability level for marketers
    if flesch_reading_ease >= 80:
        ease_level = "Very Easy - Perfect for marketers"
        ease_score = 95
        marketer_friendly = True
    elif flesch_reading_ease >= 70:
        ease_level = "Easy - Good for marketers"
        ease_score = 85
        marketer_friendly = True
    elif flesch_reading_ease >= 60:
        ease_level = "Standard - Acceptable for marketers"
        ease_score = 75
        marketer_friendly = True
    elif flesch_reading_ease >= 50:
        ease_level = "Fairly Difficult - May challenge marketers"
        ease_score = 60
        marketer_friendly = False
    elif flesch_reading_ease >= 30:
        ease_level = "Difficult - Too complex for marketers"
        ease_score = 40
        marketer_friendly = False
    else:
        ease_level = "Very Difficult - Inappropriate for marketers"
        ease_score = 20
        marketer_friendly = False
    
    # Generate specific suggestions
    suggestions = []
    
    # Flesch-Kincaid Grade Level suggestions
    if flesch_kincaid > 12:
        suggestions.append(f"Flesch-Kincaid grade level is {flesch_kincaid:.1f} (college level) - aim for 8-10 for marketers")
    elif flesch_kincaid > 10:
        suggestions.append(f"Flesch-Kincaid grade level is {flesch_kincaid:.1f} - consider simplifying for broader accessibility")
    else:
        suggestions.append(f"Flesch-Kincaid grade level is {flesch_kincaid:.1f} - good level for marketers")
    
    # Gunning Fog Index suggestions
    if gunning_fog > 12:
        suggestions.append(f"Gunning Fog index is {gunning_fog:.1f} - reduce complex words and long sentences")
    elif gunning_fog > 10:
        suggestions.append(f"Gunning Fog index is {gunning_fog:.1f} - good but could be more accessible")
    else:
        suggestions.append(f"Gunning Fog index is {gunning_fog:.1f} - excellent accessibility")
    
    # Flesch Reading Ease suggestions
    if flesch_reading_ease < 60:
        suggestions.append(f"Reading ease score is {flesch_reading_ease:.1f} - aim for 60+ for marketing content")
    else:
        suggestions.append(f"Reading ease score is {flesch_reading_ease:.1f} - good accessibility")
    
    # Sentence length suggestions
    if avg_sentence_length > 25:
        suggestions.append(f"Average sentence length is {avg_sentence_length:.1f} words - break up long sentences")
    elif avg_sentence_length > 20:
        suggestions.append(f"Average sentence length is {avg_sentence_length:.1f} words - consider shorter sentences")
    else:
        suggestions.append(f"Average sentence length is {avg_sentence_length:.1f} words - good length")
    
    return {
        "assessment": ease_level,
        "score": ease_score,
        "marketer_friendly": marketer_friendly,
        "detailed_metrics": {
            "flesch_kincaid_grade": round(flesch_kincaid, 1),
            "gunning_fog_index": round(gunning_fog, 1),
            "flesch_reading_ease": round(flesch_reading_ease, 1),
            "automated_readability_index": round(automated_readability, 1),
            "coleman_liau_index": round(coleman_liau, 1),
            "word_count": word_count,
            "sentence_count": sentence_count,
            "syllable_count": syllable_count,
            "avg_sentence_length": round(avg_sentence_length, 1)
        },
        "grade_level_interpretation": {
            "flesch_kincaid": f"Grade {flesch_kincaid:.0f} level",
            "target_audience": "Non-technical marketers",
            "recommended_grade": "8-10 for optimal accessibility"
        },
        "suggestions": suggestions,
        "analysis_method": "textstat_library"
    }

def fallback_readability_analysis(content):
    """Fallback analysis if textstat fails"""
    words = content.split()
    sentences = [s.strip() for s in content.replace('!', '.').replace('?', '.').split('.') if s.strip()]
    
    word_count = len(words)
    sentence_count = len(sentences) if sentences else 1
    avg_words_per_sentence = word_count / sentence_count
    
    # Estimate Flesch-Kincaid (simplified formula)
    estimated_fk = avg_words_per_sentence * 0.39 + 11.8 - 15.59
    
    # Simple readability assessment
    if avg_words_per_sentence > 25:
        assessment = "Complex - may be difficult for marketers"
        score = 50
    elif avg_words_per_sentence > 20:
        assessment = "Moderate - acceptable for marketers"
        score = 70
    else:
        assessment = "Good - appropriate for marketers"
        score = 85
    
    return {
        "assessment": assessment,
        "score": score,
        "marketer_friendly": score >= 70,
        "detailed_metrics": {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "avg_sentence_length": round(avg_words_per_sentence, 1),
            "estimated_flesch_kincaid": round(estimated_fk, 1)
        },
        "suggestions": [
            f"Using basic analysis - average sentence length: {avg_words_per_sentence:.1f} words",
            "Install textstat for detailed metrics: pip install textstat",
            f"Estimated reading level: Grade {estimated_fk:.0f}"
        ],
        "analysis_method": "fallback_basic"
    }

def test_fixed_analyzer():
    """Test the fixed analyzer"""
    
    print("🔧 Testing Fixed Textstat Analyzer")
    print("=" * 40)
    
    # Your sample content
    sample_content = """
Explore the Number of Notifications Received by Users

The Notification Received report helps you understand how many notifications your users have received across different channels like Push, Email, SMS, and In-app. This report provides insights into your notification distribution and user engagement patterns.

Overview

This report shows the distribution of notifications sent to users over a selected time period. You can analyze the data by different dimensions and understand your notification patterns better.

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

The following metrics are available in this report:

Total Notifications Sent: The total number of notifications delivered across all channels
Unique Users Reached: Number of distinct users who received at least one notification
Average Notifications per User: Mean number of notifications received per user
Channel Distribution: Percentage breakdown by notification channel

Best Practices

When analyzing notification data, consider these best practices:

Monitor notification frequency to avoid user fatigue
Analyze channel performance to optimize your communication strategy
Use segmentation to understand different user behaviors
Track trends over time to identify patterns and opportunities
""".strip()
    
    print(" Analyzing sample content...")
    
    # Run fixed analysis
    analysis = analyze_readability_fixed(sample_content)
    
    print(f"\n FIXED ANALYSIS RESULTS")
    print("=" * 30)
    print(f" Score: {analysis['score']}/100")
    print(f" Assessment: {analysis['assessment']}")
    print(f" Marketer Friendly: {analysis['marketer_friendly']}")
    print(f" Method: {analysis['analysis_method']}")
    
    print(f"\n Detailed Metrics:")
    for metric, value in analysis['detailed_metrics'].items():
        print(f"   {metric.replace('_', ' ').title()}: {value}")
    
    print(f"\n Suggestions:")
    for i, suggestion in enumerate(analysis['suggestions'], 1):
        print(f"   {i}. {suggestion}")
    
    # Compare with your original result
    print(f"\n Comparison with Original Result:")
    print(f"   Original Score: 45/100 (Complex)")
    print(f"   Fixed Score: {analysis['score']}/100 ({analysis['assessment'].split(' - ')[0]})")
    print(f"   Improvement: {'Better' if analysis['score'] > 45 else ' Similar' if analysis['score'] == 45 else ' Lower'}")
    
    # Save results
    Path("fixed_output").mkdir(exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"fixed_output/fixed_readability_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    
    print(f"\n Results saved to: {filename}")
    print(f"\n Fixed analyzer is working!")
    
    return analysis

def create_complete_working_analyzer():
    """Create a complete analyzer that works with all your existing components"""
    
    print(f"\n Creating Complete Working Analyzer")
    print("=" * 45)
    
    # Test the fixed readability
    readability_result = analyze_readability_fixed("""
Explore the Number of Notifications Received by Users

The Notification Received report helps you understand how many notifications your users have received across different channels like Push, Email, SMS, and In-app. This report provides insights into your notification distribution and user engagement patterns.

Overview

This report shows the distribution of notifications sent to users over a selected time period. You can analyze the data by different dimensions and understand your notification patterns better.

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

The following metrics are available in this report:

Total Notifications Sent: The total number of notifications delivered across all channels
Unique Users Reached: Number of distinct users who received at least one notification
Average Notifications per User: Mean number of notifications received per user
Channel Distribution: Percentage breakdown by notification channel

Best Practices

When analyzing notification data, consider these best practices:

Monitor notification frequency to avoid user fatigue
Analyze channel performance to optimize your communication strategy
Use segmentation to understand different user behaviors
Track trends over time to identify patterns and opportunities
""".strip())
    
    # Create complete analysis report combining all your work
    complete_report = {
        "analysis_info": {
            "title": "Complete MoEngage Documentation Analysis",
            "url": "https://help.moengage.com/hc/en-us/articles/360035738832-Explore-the-Number-of-Notifications-Received-by-Users",
            "analysis_timestamp": datetime.now().isoformat(),
            "analyzer_version": "complete_v1.0"
        },
        "enhanced_readability": readability_result,
        "your_original_results": {
            "overall_score": 65.0,
            "grade": "D",
            "category_scores": {
                "readability": 45,
                "structure": 75,
                "completeness": 65,
                "style": 75
            }
        },
        "improvement_comparison": {
            "readability_improvement": readability_result['score'] - 45,
            "new_detailed_metrics": len(readability_result['detailed_metrics']),
            "enhanced_suggestions": len(readability_result['suggestions'])
        }
    }
    
    # Save complete report
    filename = f"fixed_output/complete_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(complete_report, f, indent=2, ensure_ascii=False)
    
    print(f"Complete report saved to: {filename}")
    
    return complete_report

def main():
    """Main function to test the fix"""
    
    # Test the fix
    result = test_fixed_analyzer()
    
    # Create complete working version
    complete_result = create_complete_working_analyzer()
    

if __name__ == "__main__":
    main()
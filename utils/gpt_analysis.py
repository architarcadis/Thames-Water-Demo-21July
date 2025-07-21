import os
from openai import OpenAI
import json

def analyze_market_data(category, market, scraped_content):
    """
    Analyze scraped market data using GPT-4 with specialized prompts for structured report
    """
    # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
    # do not change this unless explicitly requested by the user
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Combine all scraped content
    combined_content = "\n\n".join([item['content'] for item in scraped_content if item['content']])
    
    # Load prompts for structured report
    prompts = {}
    prompt_files = [
        'report_insights.txt', 'thematic_analysis.txt', 'timeline_events.txt', 
        'strategic_outlook.txt', 'risk_flags.txt'
    ]
    
    for prompt_file in prompt_files:
        with open(f"prompts/{prompt_file}", "r") as f:
            prompts[prompt_file.replace('.txt', '')] = f.read()
    
    analysis_results = {}
    
    # Top 3 Insights Analysis
    try:
        insights_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": prompts['report_insights']
                },
                {
                    "role": "user",
                    "content": f"Category: {category}\nMarket: {market}\n\nMarket Data:\n{combined_content[:8000]}"
                }
            ],
            response_format={"type": "json_object"}
        )
        
        insights_content = insights_response.choices[0].message.content
        if insights_content:
            insights_analysis = json.loads(insights_content)
            analysis_results['insights'] = insights_analysis.get('insights', [])
        else:
            analysis_results['insights'] = []
        
    except Exception as e:
        print(f"Error in insights analysis: {e}")
        analysis_results['insights'] = []
    
    # Thematic Analysis
    try:
        thematic_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": prompts['thematic_analysis']
                },
                {
                    "role": "user",
                    "content": f"Category: {category}\nMarket: {market}\n\nMarket Data:\n{combined_content[:8000]}"
                }
            ],
            response_format={"type": "json_object"}
        )
        
        thematic_content = thematic_response.choices[0].message.content
        if thematic_content:
            thematic_analysis = json.loads(thematic_content)
            analysis_results['themes'] = thematic_analysis.get('themes', {})
        else:
            analysis_results['themes'] = {}
        
    except Exception as e:
        print(f"Error in thematic analysis: {e}")
        analysis_results['themes'] = {}
    
    # Risk Flags Analysis
    try:
        risk_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": prompts['risk_flags']
                },
                {
                    "role": "user",
                    "content": f"Category: {category}\nMarket: {market}\n\nMarket Data:\n{combined_content[:8000]}"
                }
            ],
            response_format={"type": "json_object"}
        )
        
        risk_content = risk_response.choices[0].message.content
        if risk_content:
            risk_analysis = json.loads(risk_content)
            analysis_results['risk_flags'] = risk_analysis.get('risks', [])
        else:
            analysis_results['risk_flags'] = []
        
    except Exception as e:
        print(f"Error in risk analysis: {e}")
        analysis_results['risk_flags'] = []
    
    # Timeline Events Analysis
    try:
        timeline_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": prompts['timeline_events']
                },
                {
                    "role": "user",
                    "content": f"Category: {category}\nMarket: {market}\n\nMarket Data:\n{combined_content[:8000]}"
                }
            ],
            response_format={"type": "json_object"}
        )
        
        timeline_content = timeline_response.choices[0].message.content
        if timeline_content:
            timeline_analysis = json.loads(timeline_content)
            analysis_results['timeline'] = timeline_analysis.get('timeline', [])
        else:
            analysis_results['timeline'] = []
        
    except Exception as e:
        print(f"Error in timeline analysis: {e}")
        analysis_results['timeline'] = []
    
    # Strategic Outlook Analysis
    try:
        strategic_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": prompts['strategic_outlook']
                },
                {
                    "role": "user",
                    "content": f"Category: {category}\nMarket: {market}\n\nMarket Data:\n{combined_content[:8000]}"
                }
            ],
            response_format={"type": "json_object"}
        )
        
        strategic_content = strategic_response.choices[0].message.content
        if strategic_content:
            strategic_analysis = json.loads(strategic_content)
            analysis_results['strategic_outlook'] = strategic_analysis.get('strategic_outlook', {})
        else:
            analysis_results['strategic_outlook'] = {}
        
    except Exception as e:
        print(f"Error in strategic outlook analysis: {e}")
        analysis_results['strategic_outlook'] = {}
    
    return analysis_results

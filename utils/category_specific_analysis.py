import os
from openai import OpenAI
import json
import re

def analyze_category_specific_data(category, market, scraped_content):
    """
    Analyze scraped market data for a specific category with personalized insights
    """
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Combine all scraped content with source tracking
        source_content = []
        for content in scraped_content:
            if content['content']:
                source_content.append({
                    'url': content['url'],
                    'content': content['content'][:3000],
                    'domain': content['url'].split('/')[2] if '/' in content['url'] else content['url']
                })
        
        if not source_content:
            return {"error": "No content available for analysis"}
        
        combined_content = "\n\n".join([
            f"Source: {content['url']}\nDomain: {content['domain']}\nContent: {content['content']}" 
            for content in source_content
        ])
        
        category_prompt = f"""
        Analyze the following market intelligence specifically for {category} in {market} market:
        
        Sources: {combined_content}
        
        CRITICAL INSTRUCTIONS:
        1. Focus exclusively on {category} - all insights must be specific to this category
        2. Extract ONLY quantitative data (numbers, percentages, financial figures, dates, metrics)
        3. NO HTML tags in responses - use plain text only
        4. Provide category-specific analysis that would be different for other categories
        5. Look for: market size, growth rates, pricing data, tender values, company revenues, employment figures, cost changes, capacity numbers, production volumes, market share percentages
        
        Provide analysis in JSON format:
        {{
            "category_name": "{category}",
            "executive_summary": {{
                "key_recommendation": "Primary strategic recommendation specific to {category}",
                "urgency_level": "High/Medium/Low",
                "decision_window": "Immediate/3-6 months/6-12 months",
                "confidence_level": "High/Medium/Low"
            }},
            "insights": [
                {{
                    "headline": "Category-specific finding with numbers",
                    "explanation": "Detailed explanation with quantitative data for {category}",
                    "evidence": "Supporting evidence with specific metrics - NO HTML TAGS",
                    "confidence": "High/Medium/Low",
                    "sources_count": number_of_sources,
                    "emoji": "📊",
                    "key_metrics": [
                        {{
                            "metric": "Metric name",
                            "value": "Quantitative value",
                            "context": "Context or time period"
                        }}
                    ],
                    "source_urls": ["url1", "url2"],
                    "quantitative_data": "Specific numbers or percentages",
                    "impact_assessment": "Business impact assessment",
                    "market_implications": "Strategic market implications",
                    "urgency": "High/Medium/Low"
                }}
            ],
            "market_players": [
                {{
                    "company": "Company name",
                    "market_share": "Market share percentage or description",
                    "strengths": "Key competitive strengths",
                    "key_products": "Main products/services",
                    "recent_developments": "Recent company developments"
                }}
            ],
            "cost_analysis": {{
                "cost_trends": [
                    "Cost trend with specific data",
                    "Price movement with quantitative details"
                ],
                "price_drivers": [
                    "Key factor affecting pricing",
                    "Economic driver with impact description"
                ],
                "market_rates": "Current market rates or pricing ranges",
                "cost_projections": "Future cost projections if available"
            }},
            "supply_chain": {{
                "risks": [
                    "Supply chain risk with specific details",
                    "Operational risk with quantitative impact"
                ],
                "suppliers": [
                    "Key supplier with market presence",
                    "Important supplier with specialization"
                ],
                "capacity_constraints": "Capacity limitations if identified",
                "lead_times": "Typical lead times for {category}"
            }},
            "growth_trends": {{
                "indicators": [
                    "Growth indicator with specific metrics",
                    "Market expansion data with percentages"
                ],
                "outlook": "Future market outlook with quantitative projections",
                "growth_drivers": [
                    "Factor driving growth with impact measurement",
                    "Market catalyst with expected outcomes"
                ],
                "market_maturity": "Assessment of market maturity stage"
            }},
            "market_dynamics": {{
                "key_trends": [
                    {{
                        "trend": "Trend specific to {category}",
                        "quantitative_data": "Specific numbers or percentages",
                        "source_evidence": "Evidence without HTML tags",
                        "impact": "High/Medium/Low",
                        "source_urls": ["url1", "url2"]
                    }}
                ]
            }},
            "market_opportunities": [
                {{
                    "opportunity": "Opportunity specific to {category}",
                    "quantitative_potential": "Specific value or percentage",
                    "source_evidence": "Evidence without HTML tags",
                    "recommended_action": "Action specific to {category}",
                    "source_urls": ["url1", "url2"]
                }}
            ],
            "risk_flags": [
                {{
                    "risk_type": "Risk specific to {category}",
                    "description": "Risk description without HTML tags",
                    "likelihood": "High/Medium/Low",
                    "impact": "High/Medium/Low",
                    "mitigation": "Mitigation strategy for {category}",
                    "source_urls": ["url1", "url2"]
                }}
            ],
            "strategic_recommendations": [
                {{
                    "recommendation": "Recommendation specific to {category}",
                    "rationale": "Rationale without HTML tags",
                    "timeline": "Implementation timeframe",
                    "category_specific": true,
                    "source_urls": ["url1", "url2"]
                }}
            ]
        }}
        
        IMPORTANT: All content must be specific to {category} and contain NO HTML tags.
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"You are a procurement intelligence specialist focused on {category} market analysis. Never include HTML tags in your responses."},
                {"role": "user", "content": category_prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        
        # Clean any remaining HTML tags from the response
        result = clean_html_tags(result)
        
        # Add source URLs to each analysis section
        source_urls = [content['url'] for content in source_content]
        result = add_source_urls(result, source_urls)
        
        return result
        
    except Exception as e:
        return {"error": f"Category analysis failed: {str(e)}"}

def clean_html_tags(data):
    """
    Recursively clean HTML tags from data structure
    """
    if isinstance(data, dict):
        return {key: clean_html_tags(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [clean_html_tags(item) for item in data]
    elif isinstance(data, str):
        # Remove HTML tags using regex
        clean_text = re.sub(r'<[^>]+>', '', data)
        return clean_text
    else:
        return data

def add_source_urls(result, source_urls):
    """
    Add source URLs to analysis sections that don't already have them
    """
    # Add to market dynamics
    if 'market_dynamics' in result and 'key_trends' in result['market_dynamics']:
        for trend in result['market_dynamics']['key_trends']:
            if 'source_urls' not in trend or not trend['source_urls']:
                trend['source_urls'] = source_urls[:2]  # Add first 2 sources
    
    # Add to market opportunities
    if 'market_opportunities' in result:
        for opp in result['market_opportunities']:
            if 'source_urls' not in opp or not opp['source_urls']:
                opp['source_urls'] = source_urls[:2]  # Add first 2 sources
    
    # Add to risk flags
    if 'risk_flags' in result:
        for risk in result['risk_flags']:
            if 'source_urls' not in risk or not risk['source_urls']:
                risk['source_urls'] = source_urls[:2]  # Add first 2 sources
    
    # Add to strategic recommendations
    if 'strategic_recommendations' in result:
        for rec in result['strategic_recommendations']:
            if 'source_urls' not in rec or not rec['source_urls']:
                rec['source_urls'] = source_urls[:2]  # Add first 2 sources
    
    return result
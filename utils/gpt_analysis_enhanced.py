import os
from openai import OpenAI
import json

def analyze_market_data(category, market, scraped_content):
    """
    Analyze scraped market data using enhanced intelligence synthesis
    """
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Combine all scraped content with source tracking
        source_content = []
        for content in scraped_content:
            if content['content']:
                source_content.append({
                    'url': content['url'],
                    'content': content['content'][:3000],  # Increased content length
                    'domain': content['url'].split('/')[2] if '/' in content['url'] else content['url']
                })
        
        if not source_content:
            return {"error": "No content available for analysis"}
        
        # Cross-validation analysis
        cross_validation_result = perform_cross_validation(client, source_content, category, market)
        
        # Intelligence synthesis
        synthesis_result = perform_intelligence_synthesis(client, source_content, category, market)
        
        # Actionable intelligence generation
        actionable_result = generate_actionable_intelligence(client, source_content, category, market)
        
        # Combine all analysis results
        analysis_results = {
            **cross_validation_result,
            **synthesis_result,
            **actionable_result
        }
        
        return analysis_results
        
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}

def perform_cross_validation(client, source_content, category, market):
    """
    Cross-validate information across multiple sources
    """
    combined_content = "\n\n".join([
        f"Source: {content['url']}\nDomain: {content['domain']}\nContent: {content['content']}" 
        for content in source_content
    ])
    
    validation_prompt = f"""
    Analyze the following market intelligence from multiple sources and extract SPECIFIC QUANTITATIVE DATA:
    
    Category: {category}
    Market: {market}
    
    Sources: {combined_content}
    
    CRITICAL: Focus on extracting actual numbers, percentages, financial figures, dates, and specific metrics from the sources.
    Look for: market size, growth rates, pricing data, tender values, company revenues, employment figures, cost changes, capacity numbers, production volumes, market share percentages, etc.
    
    Provide analysis in JSON format:
    {{
        "insights": [
            {{
                "headline": "Key finding with specific numbers",
                "explanation": "Detailed explanation with quantitative data", 
                "evidence": "Supporting evidence with specific metrics, dates, and figures",
                "confidence": "High/Medium/Low",
                "sources_count": number_of_sources_confirming,
                "contradictions": "Any conflicting information found",
                "source_urls": ["url1", "url2"],
                "source_domains": ["domain1", "domain2"],
                "emoji": "relevant_emoji",
                "key_metrics": [
                    {{"metric": "metric name", "value": "specific number/percentage", "context": "explanation"}},
                    {{"metric": "metric name", "value": "specific number/percentage", "context": "explanation"}}
                ]
            }}
        ],
        "data_quality": {{
            "total_sources": number,
            "unique_domains": number,
            "information_gaps": ["gap1", "gap2"],
            "conflicting_data": ["conflict1", "conflict2"],
            "confidence_score": float_between_0_and_1
        }}
    }}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024. do not change this unless explicitly requested by the user
        messages=[
            {"role": "system", "content": "You are a market intelligence analyst specializing in cross-validation of information from multiple sources."},
            {"role": "user", "content": validation_prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    return json.loads(response.choices[0].message.content)

def perform_intelligence_synthesis(client, source_content, category, market):
    """
    Synthesize intelligence to identify patterns and connections
    """
    combined_content = "\n\n".join([
        f"Source: {content['url']}\nContent: {content['content']}" 
        for content in source_content
    ])
    
    synthesis_prompt = f"""
    Synthesize the following market intelligence and extract QUANTITATIVE DATA for strategic insights:
    
    Category: {category}
    Market: {market}
    
    Content: {combined_content}
    
    CRITICAL: Extract specific numbers, percentages, financial figures, growth rates, market sizes, capacity data, employment figures, cost changes, and quantitative metrics from the sources.
    
    Provide synthesis in JSON format:
    {{
        "market_dynamics": {{
            "key_trends": [
                {{"trend": "trend description", "quantitative_data": "specific numbers/percentages", "source_evidence": "direct quote or reference"}},
                {{"trend": "trend description", "quantitative_data": "specific numbers/percentages", "source_evidence": "direct quote or reference"}}
            ],
            "market_drivers": [
                {{"driver": "driver description", "quantitative_impact": "specific metrics", "source_evidence": "supporting data"}},
                {{"driver": "driver description", "quantitative_impact": "specific metrics", "source_evidence": "supporting data"}}
            ],
            "disruption_signals": [
                {{"signal": "signal description", "quantitative_indicator": "specific metrics", "source_evidence": "supporting data"}},
                {{"signal": "signal description", "quantitative_indicator": "specific metrics", "source_evidence": "supporting data"}}
            ]
        }},
        "competitive_intelligence": {{
            "market_concentration": "High/Medium/Low",
            "competitive_pressure": "Increasing/Stable/Decreasing",
            "innovation_activity": "High/Medium/Low",
            "entry_barriers": ["barrier1", "barrier2"],
            "market_size_data": {{"value": "specific figure", "currency": "currency", "timeframe": "year", "source": "source reference"}},
            "growth_metrics": {{"rate": "percentage", "timeframe": "period", "source": "source reference"}},
            "competitive_metrics": [
                {{"metric": "market share/revenue/capacity", "value": "specific number", "company": "company name", "source": "source reference"}},
                {{"metric": "market share/revenue/capacity", "value": "specific number", "company": "company name", "source": "source reference"}}
            ]
        }},
        "strategic_implications": {{
            "market_opportunities": [
                {{"opportunity": "description", "quantitative_potential": "specific value/savings/growth", "source_evidence": "supporting data"}},
                {{"opportunity": "description", "quantitative_potential": "specific value/savings/growth", "source_evidence": "supporting data"}}
            ],
            "threat_assessment": [
                {{"threat": "description", "quantitative_impact": "specific cost/risk amount", "source_evidence": "supporting data"}},
                {{"threat": "description", "quantitative_impact": "specific cost/risk amount", "source_evidence": "supporting data"}}
            ],
            "timing_considerations": "Immediate/Medium-term/Long-term focus"
        }}
    }}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a strategic intelligence analyst specializing in market synthesis and pattern recognition."},
            {"role": "user", "content": synthesis_prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    return json.loads(response.choices[0].message.content)

def generate_actionable_intelligence(client, source_content, category, market):
    """
    Generate actionable intelligence for procurement decision-making
    """
    combined_content = "\n\n".join([
        f"Source: {content['url']}\nContent: {content['content']}" 
        for content in source_content
    ])
    
    actionable_prompt = f"""
    Generate actionable intelligence for procurement decision-making with QUANTITATIVE DATA:
    
    Category: {category}
    Market: {market}
    
    Content: {combined_content}
    
    CRITICAL: Include specific numbers, percentages, financial figures, pricing data, cost savings, timeframes, and quantitative metrics from the sources.
    
    Provide actionable intelligence in JSON format:
    {{
        "executive_summary": {{
            "key_recommendation": "Primary strategic recommendation",
            "urgency_level": "High/Medium/Low",
            "decision_window": "timeframe for action",
            "confidence_level": "High/Medium/Low"
        }},
        "strategic_outlook": {{
            "supply_security": {{
                "assessment": "Current supply security status",
                "pressure_score": 1-5,
                "suggested_play": "Recommended action",
                "timeline": "Implementation timeframe"
            }},
            "supplier_ecosystem": {{
                "assessment": "Supplier landscape evaluation",
                "pressure_score": 1-5,
                "suggested_play": "Recommended action",
                "timeline": "Implementation timeframe"
            }},
            "innovation_levers": {{
                "assessment": "Innovation opportunities",
                "pressure_score": 1-5,
                "suggested_play": "Recommended action",
                "timeline": "Implementation timeframe"
            }}
        }},
        "risk_flags": [
            {{
                "risk_type": "Supply/Demand/Price/Regulatory",
                "description": "Risk description",
                "likelihood": "High/Medium/Low",
                "impact": "High/Medium/Low",
                "mitigation": "Recommended mitigation strategy"
            }}
        ],
        "market_opportunities": [
            {{
                "opportunity": "Market opportunity description",
                "value_potential": "High/Medium/Low",
                "implementation_complexity": "High/Medium/Low",
                "recommended_action": "Specific action to take"
            }}
        ]
    }}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a procurement intelligence specialist focused on generating actionable business intelligence."},
            {"role": "user", "content": actionable_prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    return json.loads(response.choices[0].message.content)
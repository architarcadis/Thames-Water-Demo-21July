"""
Search Options Generation - Convert user natural language input to selectable research options
"""

import os
import json
from openai import OpenAI

def generate_search_options(user_input, market="UK"):
    """
    Generate intelligent search options from user's natural language input
    """
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        prompt = f"""
        Convert this user research request into 3-5 specific, actionable procurement intelligence topics:
        
        User input: "{user_input}"
        Market: {market}
        
        Generate options that would be relevant for built-asset procurement intelligence.
        Focus on supply chain, market capacity, supplier landscape, pricing, and risk factors.
        
        Return JSON in this format:
        {{
            "options": [
                "Specific topic 1 - focus area",
                "Specific topic 2 - focus area", 
                "Specific topic 3 - focus area"
            ]
        }}
        
        Example:
        If user says "concrete supply chains", generate options like:
        - "Precast concrete supply capacity and constraints in {market}"
        - "Concrete material pricing trends and supplier landscape"
        - "Infrastructure concrete demand pipeline and market forecasts"
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024. do not change this unless explicitly requested by the user
            messages=[
                {"role": "system", "content": "You are a procurement intelligence specialist. Generate specific, actionable research topics from user input."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result.get("options", [])
        
    except Exception as e:
        print(f"Error generating search options: {e}")
        return [
            f"{user_input} - market capacity analysis",
            f"{user_input} - supplier landscape assessment", 
            f"{user_input} - pricing and risk evaluation"
        ]

def format_time_filter(timescale):
    """
    Convert timescale selection to enhanced search query modifier
    """
    from datetime import datetime, timedelta
    
    current_date = datetime.now()
    
    if "6 months" in timescale:
        six_months_ago = current_date - timedelta(days=180)
        return f"after:{six_months_ago.strftime('%Y-%m-%d')}"
    elif "12 months" in timescale:
        twelve_months_ago = current_date - timedelta(days=365)
        return f"after:{twelve_months_ago.strftime('%Y-%m-%d')}"
    else:
        # For older content, still apply some recency bias
        two_years_ago = current_date - timedelta(days=730)
        return f"after:{two_years_ago.strftime('%Y-%m-%d')}"

def get_research_depth_config(depth):
    """
    Get configuration based on research depth setting
    """
    configs = {
        "Quick": {"num_queries": 5, "num_results": 5, "max_workers": 3},
        "Medium": {"num_queries": 10, "num_results": 8, "max_workers": 5},
        "Deep": {"num_queries": 20, "num_results": 10, "max_workers": 8}
    }
    return configs.get(depth, configs["Medium"])
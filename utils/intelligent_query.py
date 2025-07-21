import os
from openai import OpenAI
import json

def generate_intelligent_queries(category, market, time_focus="6 months", research_depth="Medium"):
    """
    Generate intelligent, contextual procurement queries with fallback
    """
    # Use fallback queries for now to ensure system works reliably
    return generate_fallback_queries(category, market, time_focus, research_depth)

def generate_fallback_queries(category, market, time_focus="6 months", research_depth="Medium"):
    """
    Generate fallback queries when OpenAI is unavailable
    """
    # Enhanced queries with multiple research dimensions
    base_queries = [
        f"{category} suppliers {market} 2024 procurement framework",
        f"{category} market {market} latest news contracts",
        f"{category} tender opportunities {market} 2024",
        f"{category} innovation {market} 2024 sustainability",
        f"{category} supply chain {market} challenges disruption",
        f"{category} pricing trends {market} cost analysis",
        f"{category} technology {market} construction digital",
        f"{category} regulations {market} compliance 2024",
        f"{category} mergers acquisitions {market} consolidation",
        f"{category} ESG sustainability {market} green",
        f"{category} skills shortage {market} workforce",
        f"{category} investment funding {market} venture",
        f"{category} quality standards {market} certification",
        f"{category} trade disputes {market} tariffs",
        f"{category} export import {market} global"
    ]
    
    # Limit based on research depth
    num_queries_map = {
        "Quick (5 queries)": 5,
        "Medium (10 queries)": 8,
        "Deep (20 queries)": 15
    }
    
    num_queries = num_queries_map.get(research_depth, 8)
    selected_queries = base_queries[:num_queries]
    
    # Enhanced research dimensions
    research_dimensions = [
        "Market Dynamics", "Supplier Intelligence", "Innovation Trends", "Supply Chain Risk", 
        "Regulatory Compliance", "Pricing Intelligence", "Technology Adoption", "ESG Sustainability",
        "Market Consolidation", "Skills & Workforce", "Investment Flows", "Quality Standards",
        "Trade Policy", "Global Supply", "Competitive Intelligence"
    ]
    
    # Format as expected structure
    fallback_queries = []
    for i, query in enumerate(selected_queries):
        fallback_queries.append({
            "query": query,
            "dimension": research_dimensions[i % len(research_dimensions)],
            "rationale": f"Research {category} {research_dimensions[i % len(research_dimensions)].lower()} for strategic intelligence",
            "target_sources": ["Industry publications", "Government sources", "Company announcements"],
            "intelligence_value": f"{research_dimensions[i % len(research_dimensions)]} insights for {category}",
            "category": category,
            "optimized": True
        })
    
    return fallback_queries

def optimize_search_query(query_data, category, market, time_period):
    """
    Optimize individual search queries for better relevance and recency
    """
    base_query = query_data.get("query", "")
    
    # Add temporal keywords for recency
    temporal_keywords = ["2024", "2025", "current", "latest", "recent"]
    if not any(keyword in base_query.lower() for keyword in temporal_keywords):
        base_query = f"{base_query} 2024 latest"
    
    # Add market specificity if not present
    market_keywords = [market.lower(), "uk", "british"]
    if not any(keyword in base_query.lower() for keyword in market_keywords):
        base_query = f"{base_query} {market}"
    
    # Add procurement context if missing
    procurement_keywords = ["procurement", "supply", "tender", "framework", "sourcing"]
    if not any(keyword in base_query.lower() for keyword in procurement_keywords):
        base_query = f"{base_query} procurement supply chain"
    
    # Ensure category is prominently featured
    if category.lower() not in base_query.lower():
        base_query = f"{category} {base_query}"
    
    return {
        "dimension": query_data.get("dimension", "Market Intelligence"),
        "query": base_query,
        "rationale": query_data.get("rationale", "Contextual market research"),
        "target_sources": query_data.get("target_sources", ["Industry sources"]),
        "intelligence_value": query_data.get("intelligence_value", "Market insights"),
        "category": category,
        "optimized": True
    }

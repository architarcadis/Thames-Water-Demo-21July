import streamlit as st
import os
from dotenv import load_dotenv
import traceback
import random
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from streamlit_timeline import timeline
# Import utility functions with fallbacks for deployment
try:
    from utils.intelligent_query import generate_intelligent_queries
    from utils.search_google import search_google
    from utils.scrape_url import scrape_urls
    from utils.gpt_analysis_enhanced import analyze_market_data
    from utils.professional_pdf_report import generate_professional_pdf_report
    from utils.search_options import generate_search_options, format_time_filter, get_research_depth_config
    UTILS_AVAILABLE = True
except ImportError:
    UTILS_AVAILABLE = False
    # Define fallback functions for core functionality
    def generate_search_options(user_input, market):
        """Fallback search options generator"""
        categories = ["Steel & Metals", "Electrical", "Infrastructure", "Transport", "Water Utilities"]
        return categories
    
    def format_time_filter(timescale):
        """Fallback time filter"""
        return "last6months" if "6" in timescale else "last12months"
    
    def get_research_depth_config(depth):
        """Fallback research depth config"""
        return {"num_queries": 5}

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Smart Acquisition - Thames Water Demo",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'intelligence_data' not in st.session_state:
    st.session_state.intelligence_data = None
if 'current_categories' not in st.session_state:
    st.session_state.current_categories = []
if 'search_options' not in st.session_state:
    st.session_state.search_options = None
if 'queries_data' not in st.session_state:
    st.session_state.queries_data = None
if 'current_user_input' not in st.session_state:
    st.session_state.current_user_input = ""
if 'sidebar_uploaded_image' not in st.session_state:
    st.session_state.sidebar_uploaded_image = None
if 'current_market' not in st.session_state:
    st.session_state.current_market = "UK"
if 'current_timescale' not in st.session_state:
    st.session_state.current_timescale = "6 months"
if 'current_research_depth' not in st.session_state:
    st.session_state.current_research_depth = "Medium"
if 'current_selected_categories' not in st.session_state:
    st.session_state.current_selected_categories = []
if 'supply_chain_data_loaded' not in st.session_state:
    st.session_state.supply_chain_data_loaded = False

# Custom CSS for dark theme styling
st.markdown("""
<style>
    /* Dark theme for the entire app */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    /* Dark theme for sidebar */
    .css-1d391kg {
        background-color: #1e2130;
    }
    
    /* Dark theme for tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1e2130;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #262730;
        color: #fafafa;
    }
    
    /* Dark theme for metrics */
    [data-testid="metric-container"] {
        background-color: #262730;
        border: 1px solid #3d4450;
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Dark theme for dataframes */
    .stDataFrame {
        background-color: #262730;
    }
    
    /* Dark theme for dataframe tables */
    .stDataFrame > div {
        background-color: #262730;
        color: #fafafa;
    }
    
    /* Dark theme for dataframe headers */
    .stDataFrame th {
        background-color: #1e2130 !important;
        color: #fafafa !important;
        border: 1px solid #3d4450 !important;
    }
    
    /* Dark theme for dataframe cells */
    .stDataFrame td {
        background-color: #262730 !important;
        color: #fafafa !important;
        border: 1px solid #3d4450 !important;
    }
    
    /* Dark theme for text inputs */
    .stTextInput > div > div > input {
        background-color: #262730;
        color: #fafafa;
        border: 1px solid #3d4450;
    }
    
    /* Dark theme for selectboxes */
    .stSelectbox > div > div > div {
        background-color: #262730;
        color: #fafafa;
    }
    
    /* Dark theme for buttons */
    .stButton > button {
        background-color: #262730;
        color: #fafafa;
        border: 1px solid #3d4450;
    }
    
    .stButton > button:hover {
        background-color: #3d4450;
        border: 1px solid #4a5568;
    }
    
    /* Dark theme for expanders */
    .streamlit-expanderHeader {
        background-color: #262730;
        color: #fafafa;
    }
    
    .streamlit-expanderContent {
        background-color: #1e2130;
    }
    
    .main-header {
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
        color: #fafafa;
    }
    .metric-container {
        background-color: #262730;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border: 1px solid #3d4450;
    }
    .swot-quadrant {
        background-color: #262730;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem;
        height: 200px;
        border: 1px solid #3d4450;
    }
    .risk-indicator {
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.2rem 0;
        text-align: center;
    }
    .query-display {
        background-color: #1a1a2e;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #4A90E2;
    }
    .stProgress > div > div > div {
        background-color: #4A90E2;
    }
    
    /* Hide browser print headers and footers */
    @media print {
        @page {
            margin: 0.5in;
            size: A4;
        }
        
        /* Preserve dark theme colors for printing */
        body, .main {
            background-color: #0e1117 !important;
            color: white !important;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }
        
        /* Hide Streamlit UI elements when printing */
        .stSidebar,
        .stToolbar,
        .stDecoration,
        .stHeader,
        .stFooter,
        [data-testid="stHeader"],
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stSidebar"],
        .stApp > header,
        .stApp > footer {
            display: none !important;
        }
        
        /* Optimize content for printing */
        .main .block-container {
            max-width: none !important;
            padding: 0.5in !important;
            background-color: #0e1117 !important;
        }
        
        /* Preserve container styling */
        .metric-container,
        .swot-container,
        .query-display {
            background-color: #262730 !important;
            color: white !important;
            border-color: #4A90E2 !important;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }
        
        /* Ensure proper page breaks */
        .stTabs [data-baseweb="tab-panel"] {
            page-break-before: always;
            page-break-inside: avoid;
            display: block !important;
        }
        
        /* Hide tab navigation but show all content */
        .stTabs [data-baseweb="tab-list"] {
            display: none !important;
        }
        
        /* Preserve all colors and styling */
        * {
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }
        
        /* Ensure text remains visible */
        h1, h2, h3, h4, h5, h6, p, div, span {
            color: white !important;
        }
        
        /* Preserve header colors */
        div[data-testid="stMarkdownContainer"] h1 {
            color: #FF6B6B !important;
        }
        div[data-testid="stMarkdownContainer"] h2 {
            color: #4ECDC4 !important;
        }
        div[data-testid="stMarkdownContainer"] h3 {
            color: #FFD93D !important;
        }
        div[data-testid="stMarkdownContainer"] h4 {
            color: #6BCF7F !important;
        }
    }
    
    /* Force remove print headers and footers - additional approach */
    @page {
        @top-left { content: ""; }
        @top-center { content: ""; }
        @top-right { content: ""; }
        @bottom-left { content: ""; }
        @bottom-center { content: ""; }
        @bottom-right { content: ""; }
    }
</style>

<script>
// Print function for dark format without footer
function printDarkFormat() {
    // Store original styles
    const originalStyles = new Map();
    
    // Hide sidebar and other UI elements
    const elementsToHide = document.querySelectorAll('.stSidebar, .stToolbar, .stDecoration, .stHeader, .stFooter, [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stSidebar"]');
    elementsToHide.forEach(el => {
        originalStyles.set(el, el.style.display);
        el.style.display = 'none';
    });
    
    // Apply dark print styles to body
    document.body.style.webkitPrintColorAdjust = 'exact';
    document.body.style.printColorAdjust = 'exact';
    document.body.style.backgroundColor = '#0e1117';
    document.body.style.color = 'white';
    
    // Show all tab content and make them visible for printing
    const tabPanels = document.querySelectorAll('[data-baseweb="tab-panel"]');
    tabPanels.forEach((panel, index) => {
        originalStyles.set(panel, {
            display: panel.style.display,
            pageBreakBefore: panel.style.pageBreakBefore
        });
        panel.style.display = 'block';
        panel.style.visibility = 'visible';
        if (index > 0) {
            panel.style.pageBreakBefore = 'always';
        }
    });
    
    // Hide tab navigation
    const tabLists = document.querySelectorAll('[data-baseweb="tab-list"]');
    tabLists.forEach(tabList => {
        originalStyles.set(tabList, tabList.style.display);
        tabList.style.display = 'none';
    });
    
    // Print with a small delay to ensure styles are applied
    setTimeout(() => {
        window.print();
        
        // Restore original styles after printing
        setTimeout(() => {
            elementsToHide.forEach(el => {
                el.style.display = originalStyles.get(el) || '';
            });
            
            tabPanels.forEach(panel => {
                const original = originalStyles.get(panel);
                panel.style.display = original.display || '';
                panel.style.pageBreakBefore = original.pageBreakBefore || '';
            });
            
            tabLists.forEach(tabList => {
                tabList.style.display = originalStyles.get(tabList) || '';
            });
            
            // Reset body styles
            document.body.style.backgroundColor = '';
            document.body.style.color = '';
        }, 1000);
    }, 100);
}

// Additional JavaScript to handle print events and hide headers/footers
window.addEventListener('beforeprint', function() {
    // Remove any potential header/footer elements
    document.querySelectorAll('header, footer, .stHeader, .stFooter, [data-testid="stHeader"], [data-testid="stFooter"]').forEach(el => {
        el.style.display = 'none';
    });
    
    // Apply print-specific styles
    document.body.style.webkitPrintColorAdjust = 'exact';
    document.body.style.printColorAdjust = 'exact';
});

window.addEventListener('afterprint', function() {
    // Restore normal display after printing
    document.querySelectorAll('header, footer').forEach(el => {
        el.style.display = '';
    });
});
</script>
""", unsafe_allow_html=True)

def format_clickable_sources(source_urls):
    """Format source URLs as clickable links"""
    if not source_urls:
        return "No sources available"
    
    formatted_sources = []
    for url in source_urls[:3]:  # Limit to 3 sources for display
        domain = url.split('/')[2] if '/' in url else url
        formatted_sources.append(f'<a href="{url}" target="_blank" style="color: #4A90E2; text-decoration: underline;">{domain}</a>')
    
    return " | ".join(formatted_sources)

def display_category_analysis(category, intelligence_data):
    """Display analysis for a specific category"""
    st.markdown(f"### 📊 {category} Market Intelligence")
    
    # Get category-specific analysis
    category_analyses = intelligence_data.get('category_analyses', {})
    analysis = category_analyses.get(category, intelligence_data.get('analysis', {}))
    
    # Debug: Show category-specific data
    with st.expander(f"🔧 {category} Analysis Debug", expanded=False):
        st.write(f"Category: {category}")
        st.write(f"Category-specific analysis keys: {list(analysis.keys()) if analysis else 'No analysis data'}")
        st.write(f"Total categories available: {list(category_analyses.keys()) if category_analyses else 'No category analyses'}")
    
    # Executive Summary for this category
    if 'executive_summary' in analysis:
        exec_summary = analysis['executive_summary']
        st.markdown(f"""
        <div style="background-color: #1a1a2e; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #4A90E2; margin-bottom: 1.5rem;">
            <h4 style="color: #4A90E2; margin-top: 0;">Executive Summary - {category}</h4>
            <p style="color: #CCCCCC; margin-bottom: 1rem;">{exec_summary.get('key_recommendation', 'Analysis pending')}</p>
            <div style="display: flex; gap: 1rem; font-size: 0.9rem;">
                <span style="color: #FFA500;">Urgency: {exec_summary.get('urgency_level', 'Medium')}</span>
                <span style="color: #00DD88;">Confidence: {exec_summary.get('confidence_level', 'Medium')}</span>
                <span style="color: #4A90E2;">Timeline: {exec_summary.get('decision_window', 'Medium-term')}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Quantitative metrics section
    display_quantitative_metrics(analysis)
    
    # Enhanced key insights for this category
    insights = analysis.get('insights', [])
    if insights:
        st.markdown("#### Key Market Insights")
        
        # Display more comprehensive insights
        for i, insight in enumerate(insights):
            with st.expander(f"💡 {insight.get('headline', 'Market Insight')}", expanded=i < 2):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**{insight.get('explanation', 'Analysis pending')}**")
                    
                    # Show quantitative data if available
                    if insight.get('quantitative_data'):
                        st.markdown(f"📊 **Data:** {insight.get('quantitative_data')}")
                    
                    # Show evidence
                    st.markdown(f"🔍 **Evidence:** {insight.get('evidence', 'Data source pending')}")
                    
                    # Show impact assessment
                    if insight.get('impact_assessment'):
                        st.markdown(f"⚡ **Impact:** {insight.get('impact_assessment')}")
                    
                    # Show market implications
                    if insight.get('market_implications'):
                        st.markdown(f"🎯 **Market Implications:** {insight.get('market_implications')}")
                
                with col2:
                    # Show insight metrics
                    st.metric("Confidence", insight.get('confidence', 'Medium'))
                    st.metric("Urgency", insight.get('urgency', 'Medium'))
                    
                    # Show sources
                    if insight.get('source_urls'):
                        st.markdown("**Sources:**")
                        st.markdown(format_clickable_sources(insight.get('source_urls', [])), unsafe_allow_html=True)
    
    # Category-specific analysis sections - simplified and unique
    st.markdown("#### Category Analysis")
    
    # Two-column layout for analysis
    left_col, right_col = st.columns(2)
    
    with left_col:
        # Market Dynamics specific to this category
        st.markdown("**Market Dynamics**")
        market_dynamics = analysis.get('market_dynamics', {})
        key_trends = market_dynamics.get('key_trends', [])
        
        if key_trends:
            for i, trend in enumerate(key_trends[:4], 1):
                if isinstance(trend, dict):
                    st.markdown(f"**{i}. {trend.get('trend', 'Market Trend')}**")
                    if trend.get('quantitative_data'):
                        st.markdown(f"📊 {trend.get('quantitative_data')}")
                    if trend.get('source_evidence'):
                        st.markdown(f"🔍 {trend.get('source_evidence')}")
                    st.markdown("---")
        else:
            st.info("Market dynamics analysis in progress...")
        
        # Market Opportunities specific to this category
        st.markdown("**Market Opportunities**")  
        market_opportunities = analysis.get('market_opportunities', [])
        
        if market_opportunities:
            for i, opp in enumerate(market_opportunities[:4], 1):
                if isinstance(opp, dict):
                    st.markdown(f"**{i}. {opp.get('opportunity', 'Market Opportunity')}**")
                    if opp.get('quantitative_potential'):
                        st.markdown(f"💰 {opp.get('quantitative_potential')}")
                    if opp.get('source_evidence'):
                        st.markdown(f"📋 {opp.get('source_evidence')}")
                    st.markdown("---")
        else:
            st.info("Market opportunities analysis in progress...")
    
    with right_col:
        # Risk Assessment specific to this category
        st.markdown("**Risk Assessment**")
        risk_flags = analysis.get('risk_flags', [])
        
        if risk_flags:
            for i, risk in enumerate(risk_flags[:4], 1):
                if isinstance(risk, dict):
                    st.markdown(f"**{i}. {risk.get('risk_type', 'Risk Factor')}**")
                    st.markdown(f"⚠️ Likelihood: {risk.get('likelihood', 'Medium')} | Impact: {risk.get('impact', 'Medium')}")
                    if risk.get('description'):
                        st.markdown(f"📝 {risk.get('description')}")
                    if risk.get('mitigation'):
                        st.markdown(f"🛡️ Mitigation: {risk.get('mitigation')}")
                    st.markdown("---")
        else:
            st.info("Risk assessment analysis in progress...")
        
        # Strategic Recommendations specific to this category
        st.markdown("**Strategic Recommendations**")
        strategic_recommendations = analysis.get('strategic_recommendations', [])
        
        if strategic_recommendations:
            for i, rec in enumerate(strategic_recommendations[:4], 1):
                if isinstance(rec, dict):
                    st.markdown(f"**{i}. {rec.get('recommendation', 'Recommendation')}**")
                    if rec.get('rationale'):
                        st.markdown(f"🎯 {rec.get('rationale')}")
                    if rec.get('timeline'):
                        st.markdown(f"⏰ Timeline: {rec.get('timeline')}")
                    st.markdown("---")
        else:
            st.info("Strategic recommendations analysis in progress...")
    
    # Two-column layout for detailed analysis
    left_col, right_col = st.columns(2)
    
    with left_col:
        st.markdown("#### Market Dynamics")
        display_market_dynamics(analysis)
        
        st.markdown("#### Market Opportunities")
        display_market_opportunities(analysis)
    
    with right_col:
        st.markdown("#### Risk Assessment")
        display_risk_assessment(analysis)
        
        st.markdown("#### Strategic Recommendations")
        display_strategic_recommendations(analysis)

def display_quantitative_metrics(analysis):
    """Display quantitative metrics section"""
    st.markdown("#### Quantitative Market Metrics")
    
    # Extract quantitative metrics from analysis
    metrics_data = []
    
    # From competitive intelligence
    comp_intel = analysis.get('competitive_intelligence', {})
    if 'market_size_data' in comp_intel:
        market_size = comp_intel['market_size_data']
        if market_size.get('value'):
            metrics_data.append({
                'metric': 'Market Size',
                'value': market_size.get('value', 'N/A'),
                'context': f"{market_size.get('currency', '')} {market_size.get('timeframe', '')}"
            })
    
    if 'growth_metrics' in comp_intel:
        growth = comp_intel['growth_metrics']
        if growth.get('rate'):
            metrics_data.append({
                'metric': 'Growth Rate',
                'value': growth.get('rate', 'N/A'),
                'context': growth.get('timeframe', '')
            })
    
    # From insights key_metrics
    insights = analysis.get('insights', [])
    for insight in insights:
        if 'key_metrics' in insight:
            for metric in insight['key_metrics'][:2]:
                if metric.get('value'):
                    metrics_data.append({
                        'metric': metric.get('metric', 'Metric'),
                        'value': metric.get('value', 'N/A'),
                        'context': metric.get('context', '')
                    })
    
    # Display metrics
    if metrics_data:
        metrics_cols = st.columns(min(4, len(metrics_data)))
        for i, metric in enumerate(metrics_data[:4]):
            with metrics_cols[i]:
                st.markdown(f"""
                <div class="metric-container">
                    <div style="font-size: 1.8rem; font-weight: bold; color: #4A90E2; text-align: center; margin-bottom: 0.5rem;">{metric['value']}</div>
                    <div style="font-weight: bold; color: white; margin-bottom: 0.3rem; text-align: center; font-size: 0.9rem;">{metric['metric']}</div>
                    <div style="font-size: 0.8rem; color: #CCCCCC; text-align: center;">{metric['context']}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Quantitative metrics will appear here when available in source data")

def display_market_dynamics(analysis):
    """Display market dynamics section"""
    if 'market_dynamics' in analysis:
        dynamics = analysis['market_dynamics']
        trends = dynamics.get('key_trends', [])
        for trend in trends[:3]:
            if isinstance(trend, dict):
                trend_text = trend.get('trend', 'Market Trend')
                quantitative_data = trend.get('quantitative_data', '')
                source_evidence = trend.get('source_evidence', '')
                source_urls = trend.get('source_urls', [])
                
                quantitative_html = f'<div style="font-size: 1.2rem; color: #4A90E2; font-weight: bold; margin-bottom: 0.5rem;">{quantitative_data}</div>' if quantitative_data else ''
                
                st.markdown(f"""
                <div class="metric-container">
                    <div style="font-weight: bold; color: white; margin-bottom: 0.5rem;">{trend_text}</div>
                    <div style="font-size: 0.9rem; color: #CCCCCC; margin-bottom: 0.5rem;">{source_evidence}</div>
                    {quantitative_html}
                    <div style="font-size: 0.7rem; color: #666666; margin-top: 0.5rem;">
                        <strong>Sources:</strong> {format_clickable_sources(source_urls)}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="metric-container">
                    <div style="font-weight: bold; color: white; margin-bottom: 0.5rem;">Market Trend</div>
                    <div style="font-size: 0.9rem; color: #CCCCCC;">{trend}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Market dynamics analysis pending")

def display_market_opportunities(analysis):
    """Display market opportunities section"""
    if 'market_opportunities' in analysis:
        opportunities = analysis['market_opportunities']
        for opp in opportunities[:3]:
            if isinstance(opp, dict):
                opportunity_text = opp.get('opportunity', 'Market Opportunity')
                quantitative_potential = opp.get('quantitative_potential', '')
                source_evidence = opp.get('source_evidence', '')
                source_urls = opp.get('source_urls', [])
                
                quantitative_html = f'<div style="font-size: 1.2rem; color: #00DD88; font-weight: bold; margin-bottom: 0.5rem;">{quantitative_potential}</div>' if quantitative_potential else ''
                
                st.markdown(f"""
                <div class="metric-container">
                    <div style="font-weight: bold; color: white; margin-bottom: 0.5rem;">{opportunity_text}</div>
                    {quantitative_html}
                    <div style="font-size: 0.9rem; color: #CCCCCC; margin-bottom: 0.5rem;">{source_evidence}</div>
                    <div style="font-size: 0.7rem; color: #666666; margin-top: 0.5rem;">
                        <strong>Sources:</strong> {format_clickable_sources(source_urls)}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="metric-container">
                    <div style="font-weight: bold; color: white; margin-bottom: 0.5rem;">Market Opportunity</div>
                    <div style="font-size: 0.9rem; color: #CCCCCC;">{opp}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Market opportunities analysis pending")

def display_risk_assessment(analysis):
    """Display risk assessment section"""
    if 'risk_flags' in analysis:
        risks = analysis['risk_flags']
        for risk in risks[:3]:
            risk_level = risk.get('likelihood', 'Medium')
            risk_color = "#FF4444" if risk_level == 'High' else "#FFA500" if risk_level == 'Medium' else "#00DD88"
            source_urls = risk.get('source_urls', [])
            
            st.markdown(f"""
            <div class="metric-container">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <div style="font-weight: bold; color: white;">{risk.get('risk_type', 'Risk Factor')}</div>
                    <div style="background-color: {risk_color}; padding: 0.2rem 0.5rem; border-radius: 3px; font-size: 0.8rem;">{risk_level}</div>
                </div>
                <div style="font-size: 0.9rem; color: #CCCCCC; margin-bottom: 0.5rem;">{risk.get('description', 'Risk analysis pending')}</div>
                <div style="font-size: 0.8rem; color: #888888; margin-bottom: 0.5rem;"><strong>Impact:</strong> {risk.get('impact', 'Assessment pending')}</div>
                <div style="font-size: 0.7rem; color: #666666; margin-top: 0.5rem;">
                    <strong>Sources:</strong> {format_clickable_sources(source_urls)}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Risk assessment analysis pending")

def display_strategic_recommendations(analysis):
    """Display strategic recommendations section"""
    if 'strategic_recommendations' in analysis:
        recommendations = analysis['strategic_recommendations']
        for rec in recommendations[:3]:
            source_urls = rec.get('source_urls', [])
            
            st.markdown(f"""
            <div class="metric-container">
                <div style="font-weight: bold; color: white; margin-bottom: 0.5rem;">{rec.get('recommendation', 'Strategic Recommendation')}</div>
                <div style="font-size: 0.9rem; color: #CCCCCC; margin-bottom: 0.5rem;">{rec.get('rationale', 'Analysis pending')}</div>
                <div style="font-size: 0.8rem; color: #888888; margin-bottom: 0.5rem;"><strong>Timeline:</strong> {rec.get('timeline', 'Medium-term')}</div>
                <div style="font-size: 0.7rem; color: #666666; margin-top: 0.5rem;">
                    <strong>Sources:</strong> {format_clickable_sources(source_urls)}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Strategic recommendations analysis pending")

def main():
    st.markdown('<div class="main-header"><h1>🎯 Smart Acquisition</h1><p>AI Market Scanning</p></div>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'intelligence_data' not in st.session_state:
        st.session_state.intelligence_data = {}
    
    # Sidebar controls
    with st.sidebar:
        st.header("🎯 Market Scanning Parameters")
        
        # User input for search
        user_input = st.text_area(
            "Describe your market intelligence needs:",
            placeholder="e.g., 'I need intelligence on precast concrete suppliers for infrastructure projects in the UK'",
            height=100
        )
        
        # Market selection
        market = st.selectbox(
            "Market Region:",
            ["UK", "EU", "US", "Global"],
            index=0
        )
        
        # Time relevance
        timescale = st.selectbox(
            "Time Relevance:",
            ["Last 6 months", "Last 12 months", "Older than 12 months"],
            index=0
        )
        
        # Research depth
        research_depth = st.selectbox(
            "Research Depth:",
            ["Quick (5 queries)", "Medium (10 queries)", "Deep (20 queries)"],
            index=1
        )
        
        # Image upload for personalized scanning
        st.markdown("---")
        st.markdown("#### 📷 Template Upload (Optional)")
        st.markdown("Upload an image/template to enable personalized format filling")
        
        uploaded_file = st.file_uploader(
            "Upload image for personalized analysis",
            type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],
            help="Upload an image, template, or document to enable personalized market scanning with format filling",
            key="sidebar_image_upload"
        )
        
        if uploaded_file is not None:
            st.success("✅ Image uploaded - Personalized scanning enabled")
            st.session_state['sidebar_uploaded_image'] = uploaded_file
            # Show small preview
            st.image(uploaded_file, caption="Uploaded Template", width=200)
        else:
            st.session_state['sidebar_uploaded_image'] = None
        
        if st.button("🔍 Generate Market Intelligence", type="primary"):
            if user_input:
                # Step 1: Show search options first
                st.session_state.show_options = True
                st.session_state.current_user_input = user_input
                st.session_state.current_market = market
                st.session_state.current_timescale = timescale
                st.session_state.current_research_depth = research_depth
                st.rerun()
            else:
                st.warning("Please describe your procurement intelligence needs")
    
    # Show search options if flag is set
    if getattr(st.session_state, 'show_options', False):
        show_search_options_ui()
    
    # Execute research if flag is set
    if getattr(st.session_state, 'execute_research', False):
        st.session_state.execute_research = False
        categories = st.session_state.intelligence_data['categories']
        market = st.session_state.intelligence_data['market']
        user_input = st.session_state.intelligence_data['user_input']
        timescale = st.session_state.current_timescale
        research_depth = st.session_state.current_research_depth
        
        execute_research_workflow(categories, market, timescale, research_depth)
    
    # Display results if available
    if 'intelligence_data' in st.session_state and st.session_state.intelligence_data:
        display_unified_dashboard()

def show_search_options_ui():
    """Show search options UI with proper session state handling"""
    
    user_input = st.session_state.current_user_input
    market = st.session_state.current_market
    timescale = st.session_state.current_timescale
    research_depth = st.session_state.current_research_depth
    
    # Convert user input to search options (cache in session state)
    if 'current_search_options' not in st.session_state:
        with st.spinner("🤖 Converting your request to search options..."):
            search_options = generate_search_options(user_input, market)
            
            if not search_options or len(search_options) == 0:
                st.error("Could not generate search options. Please try rephrasing your request.")
                st.session_state.show_options = False
                return
            
            st.session_state.current_search_options = search_options
    else:
        search_options = st.session_state.current_search_options
    
    # Display search options for user selection
    st.success("✅ Search options generated successfully!")
    
    st.markdown("### 🎯 Select Market Scanning Focus")
    st.markdown("Choose the category that best matches your market intelligence needs:")
    
    # Remove the unused all_options variable
    
    st.markdown("**Category Selection:**")
    st.markdown("- Select one or more categories for targeted research")
    st.markdown("- Choose multiple categories for comprehensive analysis")
    
    selected_categories = st.multiselect(
        "Select research categories (you can choose multiple):",
        search_options,
        default=[],
        key="category_multiselect"
    )
    
    # Process selection
    if not selected_categories:
        final_categories = []
        display_categories = "No categories selected"
    else:
        final_categories = selected_categories
        display_categories = ", ".join(selected_categories)
    
    # Only show configuration and start button if categories are selected
    if final_categories:
        # Show preview of what will be researched
        st.markdown("**Research Configuration:**")
        st.markdown(f"- **Categories:** {display_categories}")
        st.markdown(f"- **Market:** {market}")
        st.markdown(f"- **Time Scope:** {timescale}")
        st.markdown(f"- **Research Depth:** {research_depth}")
        
        # Create two columns for buttons
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("🚀 Start Research", type="primary", key="start_research_btn"):
                # Store selections and set research flag
                st.session_state.intelligence_data['categories'] = final_categories
                st.session_state.intelligence_data['market'] = market
                st.session_state.intelligence_data['user_input'] = user_input
                st.session_state.show_options = False
                st.session_state.execute_research = True
                
                # Clear previous results
                st.session_state.intelligence_data['analysis'] = {}
                st.session_state.intelligence_data['queries'] = []
                st.session_state.intelligence_data['search_results'] = []
                
                st.rerun()
        
        with col2:
            if st.button("← Back to Options", key="back_to_options_btn"):
                st.session_state.show_options = False
                st.session_state.execute_research = False
                # Clear cached search options to allow regeneration
                if 'current_search_options' in st.session_state:
                    del st.session_state.current_search_options
                st.rerun()
    else:
        st.info("👆 Please select at least one category above to configure your research options.")
        
        # Still show back button even when no categories selected
        if st.button("← Back to Options", key="back_to_options_btn"):
            st.session_state.show_options = False
            st.session_state.execute_research = False
            # Clear cached search options to allow regeneration
            if 'current_search_options' in st.session_state:
                del st.session_state.current_search_options
            st.rerun()
            st.rerun()

def execute_research_workflow(categories, market, timescale, research_depth):
    """Execute research workflow for selected categories"""
    
    try:
        # Check if utilities are available
        if not UTILS_AVAILABLE:
            st.error("Market intelligence functionality requires additional utility modules. This demo shows the dashboard interface only.")
            
            # Create minimal fallback data structure
            st.session_state.intelligence_data = {
                'queries': [],
                'search_results': [],
                'analysis': {},
                'categories': categories,
                'market': market,
                'user_input': st.session_state.current_user_input
            }
            st.session_state.current_categories = categories
            return
        
        # Initialize intelligence_data if it's None
        if st.session_state.intelligence_data is None:
            st.session_state.intelligence_data = {
                'queries': [],
                'search_results': [],
                'analysis': {},
                'categories': categories,
                'market': market,
                'user_input': st.session_state.current_user_input
            }
        
        # Update current categories
        st.session_state.current_categories = categories
        
        # Step 1: Generate intelligent queries for all categories
        status_text = st.empty()
        progress_bar = st.progress(0)
        query_display = st.empty()
        
        status_text.text("🧠 Generating intelligent queries...")
        progress_bar.progress(0.1)
        
        # Get research configuration
        config = get_research_depth_config(research_depth)
        time_filter = format_time_filter(timescale)
        
        all_queries = []
        
        # Generate enhanced queries for each category
        for category in categories:
            category_queries = generate_intelligent_queries(
                category=category, 
                market=market, 
                time_focus=timescale, 
                research_depth=research_depth
            )
            # Add category context to each query
            for query in category_queries:
                query['category'] = category
            all_queries.extend(category_queries)
        
        # Limit total queries based on research depth
        all_queries = all_queries[:config['num_queries']]
        
        # Store queries in session state
        st.session_state.intelligence_data['queries'] = all_queries
        
        # Step 2: Execute searches
        search_results = []
        for i, query in enumerate(all_queries):
            status_text.text(f"🔍 Executing search {i+1}/{len(all_queries)}...")
            
            query_display.markdown(f"""
            <div class="query-display">
                <strong>🔍 Current Query:</strong> {query['query']}
                <br><small>Query {i+1} of {len(all_queries)} | Category: {query.get('category', 'General')} | Dimension: {query.get('dimension', 'Market Intelligence')}</small>
                <br><small><em>Intelligence Value:</em> {query.get('intelligence_value', 'Market insights')}</small>
            </div>
            """, unsafe_allow_html=True)
            
            # Use enhanced search with time filtering
            search_query = query['query']
            
            results = search_google(
                query=search_query, 
                num_results=config['num_results'], 
                time_filter=time_filter, 
                enhanced_filtering=True
            )
            search_results.extend(results)
            
            # Update progress
            progress_value = 0.3 + (i + 1) * 0.2 / len(all_queries)
            progress_bar.progress(progress_value)
        
        # Step 3: Scrape content
        status_text.text("📰 Extracting content from sources...")
        query_display.markdown(f"""
        <div class="query-display">
            <strong>📊 Processing Results:</strong> Extracting content from {len(search_results)} sources
            <br><small>Using {config['max_workers']} parallel workers | {timescale} filter applied</small>
        </div>
        """, unsafe_allow_html=True)
        
        progress_bar.progress(0.5)
        
        # Use enhanced configuration for scraping
        urls_to_scrape = [result['link'] for result in search_results[:config['num_results']*2]]
        
        scraped_content = scrape_urls(urls_to_scrape, max_workers=config['max_workers'])
        
        st.session_state.intelligence_data['scraped_content'] = scraped_content
        st.session_state.intelligence_data['search_results'] = search_results
        st.session_state.intelligence_data['config'] = config
        
        # Step 4: Analyze with GPT for multiple categories
        status_text.text("🤖 Analyzing market intelligence...")
        progress_bar.progress(0.7)
        
        if scraped_content:
            # Generate category-specific analyses
            from utils.category_specific_analysis import analyze_category_specific_data
            category_analyses = {}
            
            for category in categories:
                category_analysis = analyze_category_specific_data(category, market, scraped_content)
                category_analyses[category] = category_analysis
            
            st.session_state.intelligence_data['category_analyses'] = category_analyses
            
            # For backward compatibility, also store the first category as main analysis
            if categories:
                st.session_state.intelligence_data['analysis'] = category_analyses[categories[0]]
        else:
            st.warning("No content available for analysis - check scraping results")
            st.session_state.intelligence_data['category_analyses'] = {}
            st.session_state.intelligence_data['analysis'] = {}
        
        # Step 5: Complete
        status_text.text("✅ Intelligence generation complete!")
        progress_bar.progress(1.0)
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        query_display.empty()
        
    except Exception as e:
        st.error(f"Error generating intelligence: {str(e)}")
        st.error(traceback.format_exc())

def display_unified_dashboard():
    """Display the unified symmetric market intelligence dashboard"""
    
    if 'analysis' not in st.session_state.intelligence_data:
        st.warning("No analysis data available")
        return
    
    analysis = st.session_state.intelligence_data['analysis']
    intelligence_data = st.session_state.intelligence_data
    categories = intelligence_data.get('categories', [])
    
    # Debug: Show available analysis keys in expander for troubleshooting
    with st.expander("🔧 Analysis Data Debug", expanded=False):
        st.write("Available analysis keys:", list(analysis.keys()) if analysis else "No analysis data")
        st.write("Categories:", categories)
        if analysis:
            for key, value in analysis.items():
                if isinstance(value, (list, dict)):
                    st.write(f"- {key}: {len(value) if isinstance(value, (list, dict)) else 'N/A'} items")
                else:
                    st.write(f"- {key}: {type(value).__name__}")
    
    # Create category-specific tabs for analysis
    
    # Create tabs based on available categories with shorter names
    if categories:
        # Create shorter tab names for better readability
        short_names = {
            "Steel, Iron & Non-Ferrous Metal Construction": "Steel & Metals",
            "Electrical Installation & Maintenance": "Electrical",
            "Mechanical Installation & Maintenance": "Mechanical", 
            "Built-Asset Infrastructure & Civil Engineering": "Infrastructure",
            "Facilities Management & Maintenance": "Facilities",
            "Construction & Building Materials": "Construction",
            "Energy & Power Generation": "Energy",
            "Transportation & Logistics": "Transport",
            "Water & Wastewater Management": "Water",
            "Telecommunications & IT Infrastructure": "IT & Telecom",
            "Security & Safety Systems": "Security",
            "Environmental & Waste Management": "Environment"
        }
        
        # Create tabs for each category with shorter names
        short_category_names = [short_names.get(cat, cat[:15]) for cat in categories]
        tab_names = [f"📊 {name}" for name in short_category_names] + ["🔎 Queries", "📰 News", "📋 Sources", "📥 Export"]
        tabs = st.tabs(tab_names)
        
        # Category-specific analysis tabs
        for i, category in enumerate(categories):
            with tabs[i]:
                display_category_analysis(category, intelligence_data)
        
        # Common tabs
        queries_tab = tabs[len(categories)]
        news_tab = tabs[len(categories) + 1]
        source_tab = tabs[len(categories) + 2]
        export_tab = tabs[len(categories) + 3]
    else:
        # Fallback to single unified tab
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "🔎 Queries", "📰 News", "📋 Sources", "📥 Export"])
        queries_tab = tab2
        news_tab = tab3
        source_tab = tab4
        export_tab = tab5
        
        with tab1:
            display_single_category_dashboard()
    
    with queries_tab:
        # Display queries
        st.markdown("### 🔎 Generated Queries")
        
        queries = intelligence_data.get('queries', [])
        if queries:
            for i, query in enumerate(queries):
                st.markdown(f"""
                <div class="query-display">
                    <strong>Query {i+1}:</strong> {query.get('query', 'Query')}
                    <br><small>Focus: {query.get('dimension', 'General')}</small>
                    <br><small>Intelligence Value: {query.get('intelligence_value', 'Market insights')}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No queries available. Generate intelligence first.")
    
    with news_tab:
        # News insights
        st.markdown("### 📰 News Insights")
        
        search_results = intelligence_data.get('search_results', [])
        if search_results:
            for i, result in enumerate(search_results[:10]):
                st.markdown(f"""
                <div class="metric-container">
                    <div style="font-weight: bold; color: white; margin-bottom: 0.5rem;">
                        <a href="{result.get('link', '#')}" target="_blank" style="color: #4A90E2; text-decoration: none;">
                            {result.get('title', 'Article Title')}
                        </a>
                    </div>
                    <div style="font-size: 0.9rem; color: #CCCCCC; margin-bottom: 0.5rem;">
                        {result.get('snippet', 'Article snippet')}
                    </div>
                    <div style="font-size: 0.8rem; color: #888888;">
                        Source: {result.get('displayLink', 'Source')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No news insights available. Generate intelligence first.")
    
    with source_tab:
        # Source Analysis tab
        st.markdown("### 📋 Source Analysis")
        
        scraped_content = intelligence_data.get('scraped_content', [])
        search_results = intelligence_data.get('search_results', [])
        
        if scraped_content or search_results:
            # Source Overview
            st.markdown("#### Source Overview")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Sources Found", len(search_results))
            
            with col2:
                st.metric("Successfully Scraped", len(scraped_content))
            
            with col3:
                success_rate = (len(scraped_content) / len(search_results) * 100) if search_results else 0
                st.metric("Success Rate", f"{success_rate:.1f}%")
            
            st.divider()
            
            # Detailed Source Analysis
            st.markdown("#### Detailed Source Analysis")
            
            # Create a map of scraped content by URL
            scraped_by_url = {item['url']: item for item in scraped_content}
            
            for i, result in enumerate(search_results):
                url = result.get('link', '')
                domain = url.split('/')[2] if '/' in url else url
                
                # Check if this URL was successfully scraped
                scraped_item = scraped_by_url.get(url)
                
                with st.expander(f"Source {i+1}: {domain}", expanded=False):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**Title:** {result.get('title', 'N/A')}")
                        st.markdown(f"**URL:** [{url}]({url})")
                        st.markdown(f"**Snippet:** {result.get('snippet', 'N/A')}")
                        
                        if scraped_item:
                            content_length = len(scraped_item.get('content', ''))
                            st.markdown(f"**Content Length:** {content_length:,} characters")
                            
                            # Show content preview
                            if content_length > 0:
                                st.markdown("**Content Preview:**")
                                preview = scraped_item['content'][:300] + "..." if len(scraped_item['content']) > 300 else scraped_item['content']
                                st.markdown(f"```{preview}```")
                    
                    with col2:
                        if scraped_item:
                            st.success("✅ Successfully Scraped")
                            st.markdown(f"**Domain:** {domain}")
                            st.markdown(f"**Status:** Active Source")
                        else:
                            st.error("❌ Scraping Failed")
                            st.markdown(f"**Domain:** {domain}")
                            st.markdown(f"**Status:** Inactive Source")
        else:
            st.info("No source data available. Generate intelligence first.")
    
    with export_tab:
        # Enhanced PDF Export
        st.markdown("### 📥 Consolidated Report Export")
        
        st.markdown("#### Export Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Report Contents:**")
            st.markdown("• Executive Summary")
            st.markdown("• Quantitative Metrics")
            st.markdown("• Market Intelligence Analysis")
            st.markdown("• Risk Assessment")
            st.markdown("• Strategic Recommendations")
            st.markdown("• Complete Source References")
        
        with col2:
            st.markdown("**Professional Format:**")
            st.markdown("• Executive-level layout")
            st.markdown("• Clean print-friendly design")
            st.markdown("• Data visualizations")
            st.markdown("• Source attribution")
            st.markdown("• Quality indicators")
            st.markdown("• Clickable references")
        
        # Add print button for dark format
        st.markdown("### 🖨️ Print Dashboard")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Print button using JavaScript
            print_button = st.button("🖨️ Print All Tabs", key="print_dark_button")
            
            if print_button:
                st.markdown("""
                <script>
                printDarkFormat();
                </script>
                """, unsafe_allow_html=True)
        
        with col2:
            st.info("""
            **Print Features:**
            • Prints all tabs in current dark format
            • Removes browser headers/footers automatically
            • Maintains colors and styling
            • Includes all analysis sections
            """)
        
        # Add manual print instructions
        st.markdown("### 📋 Manual Print Instructions")
        st.info("""
        **For manual printing without browser headers/footers:**
        1. Use Ctrl+P (Windows/Linux) or Cmd+P (Mac) to open print dialog
        2. Click "More settings" 
        3. Uncheck "Headers and footers"
        4. Set margins to "Minimum" or "None"
        5. Select "More" > "Options" and uncheck "Print headers and footers"
        
        This will remove the "replit.com/@archit89us/TaskMaster" footer from your printouts.
        """)
        
        st.divider()
        
        # Export button
        if st.button("📄 Generate Complete PDF Report", type="primary", use_container_width=True):
            try:
                if UTILS_AVAILABLE:
                    with st.spinner("Generating comprehensive PDF report..."):
                        pdf_buffer = generate_professional_pdf_report(intelligence_data)
                        
                        st.download_button(
                            label="⬇️ Download Complete Intelligence Report",
                            data=pdf_buffer,
                            file_name=f"market_intelligence_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                        
                        st.success("Complete PDF report generated successfully!")
                else:
                    st.error("PDF generation requires additional utility modules not available in this deployment.")
                    
            except Exception as e:
                st.error(f"Error generating PDF: {str(e)}")
                st.info("Please ensure all analysis data is available before exporting.")

def display_single_category_dashboard():
    """Display the unified dashboard when no categories are available"""
    st.markdown("### 📊 Market Intelligence Dashboard")
    
    analysis = st.session_state.intelligence_data.get('analysis', {})
    
    # Executive Summary
    if 'executive_summary' in analysis:
        exec_summary = analysis['executive_summary']
        st.markdown(f"""
        <div style="background-color: #1a1a2e; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #FF6B6B; margin-bottom: 1rem;">
            <h3 style="color: #FF6B6B; margin-bottom: 1rem;">🎯 Executive Summary</h3>
            <div style="font-size: 1.1em; font-weight: bold; color: white; margin-bottom: 0.5rem;">
                {exec_summary.get('key_recommendation', 'Strategic analysis complete')}
            </div>
            <div style="display: flex; gap: 2rem; margin-top: 1rem;">
                <div><strong>Urgency:</strong> <span style="color: {'#FF4444' if exec_summary.get('urgency_level') == 'High' else '#FFA500' if exec_summary.get('urgency_level') == 'Medium' else '#00DD88'}">{exec_summary.get('urgency_level', 'Medium')}</span></div>
                <div><strong>Decision Window:</strong> {exec_summary.get('decision_window', 'Not specified')}</div>
                <div><strong>Confidence:</strong> <span style="color: {'#00DD88' if exec_summary.get('confidence_level') == 'High' else '#FFA500' if exec_summary.get('confidence_level') == 'Medium' else '#FF4444'}">{exec_summary.get('confidence_level', 'Medium')}</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Display quantitative metrics
    display_quantitative_metrics(analysis)
    
    # Display key insights
    insights = analysis.get('insights', [])
    if insights:
        st.markdown("### 🔍 Key Market Insights")
        cols = st.columns(3)
        for i, insight in enumerate(insights[:3]):
            with cols[i]:
                st.markdown(f"""
                <div class="metric-container">
                    <div style="text-align: center; margin-bottom: 1rem;">
                        <div style="font-size: 2rem;">{insight.get('emoji', '📊')}</div>
                        <div style="font-size: 1.2rem; font-weight: bold; color: white;">
                            {insight.get('headline', 'Market Insight')}
                        </div>
                    </div>
                    <div style="font-size: 0.9rem; color: #CCCCCC; margin-bottom: 0.5rem;">
                        {insight.get('explanation', 'Analysis pending')}
                    </div>
                    <div style="font-size: 0.8rem; color: #888888;">
                        <strong>Evidence:</strong> {insight.get('evidence', 'Data source pending')}
                    </div>
                    <div style="font-size: 0.7rem; color: #666666; margin-top: 0.5rem;">
                        <strong>Sources:</strong> {format_clickable_sources(insight.get('source_urls', []))}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Single dashboard doesn't need the detailed analysis sections
    # This is already covered in the category-specific tabs
    st.info("Select categories and generate intelligence to see detailed analysis in separate tabs.")

def display_personalized_scanning_tab():
    """Display the personalized market scanning tab"""
    st.markdown("### 🎨 Personalised Market Scanning")
    
    # Get the image from sidebar
    uploaded_file = st.session_state.get('sidebar_uploaded_image')
    
    if uploaded_file is None:
        st.warning("Please upload an image in the sidebar to enable personalized scanning.")
        return
    
    # Display the uploaded image
    st.image(uploaded_file, caption="Uploaded Template/Image", use_container_width=True)
    
    st.markdown("""
    **Using your uploaded template/image to generate personalized market intelligence.**
    
    This feature will:
    - Analyze your uploaded template/image content
    - Combine it with your market scanning parameters from the sidebar
    - Generate personalized search queries based on visual context
    - Create a filled template/report matching your specific format requirements
    """)
    
    # Get market scanning parameters from sidebar/session state
    user_query = st.session_state.get('current_user_input', '')
    market = st.session_state.get('current_market', 'UK')
    categories = st.session_state.intelligence_data.get('categories', [])
    
    # Display current parameters
    st.markdown("### 📋 Current Market Scanning Parameters")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"**User Query:** {user_query}")
        st.markdown(f"**Market:** {market}")
    
    with col2:
        st.markdown(f"**Categories:** {', '.join(categories) if categories else 'None selected'}")
        
    # Output format selection
    output_format = st.selectbox(
        "Preferred Output Format:",
        ["Template Fill", "Professional Report", "Executive Summary", "Visual Dashboard", "Comparative Analysis"],
        index=0,
        help="Choose how you want the personalized intelligence to be formatted",
        key="output_format"
    )
    
    # Process button
    if st.button("🚀 Generate Personalized Intelligence", type="primary", key="personalized_scan"):
        if user_query and categories:
            with st.spinner("🤖 Analyzing template and generating personalized intelligence..."):
                try:
                    # Step 1: Analyze image and combine with market parameters
                    from utils.personalized_scanning import analyze_image_and_query
                    
                    # Create combined query from user input and categories
                    combined_query = f"{user_query} - Focus on: {', '.join(categories)}"
                    
                    analysis_result = analyze_image_and_query(uploaded_file, combined_query, market)
                    
                    if 'error' in analysis_result:
                        st.error(f"Analysis failed: {analysis_result['error']}")
                        return
                    
                    # Store results in session state
                    st.session_state['personalized_analysis'] = analysis_result
                    
                    # Display analysis results
                    st.success("✅ Template analysis complete!")
                    
                    # Display image analysis
                    st.markdown("### 📊 Template Analysis Results")
                    
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        st.markdown("#### 🔍 Template Content")
                        image_analysis = analysis_result.get('image_analysis', {})
                        st.markdown(f"**Description:** {image_analysis.get('description', 'No description available')}")
                        
                        if 'key_elements' in image_analysis:
                            st.markdown("**Key Elements:**")
                            for element in image_analysis['key_elements']:
                                st.markdown(f"• {element}")
                    
                    with col2:
                        st.markdown("#### 💼 Business Context")
                        st.markdown(f"**Context:** {image_analysis.get('business_context', 'No context available')}")
                        
                        template_suggestions = analysis_result.get('template_suggestions', {})
                        if 'key_metrics' in template_suggestions:
                            st.markdown("**Suggested Metrics:**")
                            for metric in template_suggestions['key_metrics']:
                                st.markdown(f"• {metric}")
                    
                    # Display personalized queries
                    st.markdown("### 🎯 Generated Personalized Queries")
                    queries = analysis_result.get('personalized_queries', [])
                    
                    for i, query in enumerate(queries):
                        st.markdown(f"""
                        <div class="metric-container">
                            <div style="font-weight: bold; color: white; margin-bottom: 0.5rem;">
                                Query {i+1}: {query.get('query', 'Query')}
                            </div>
                            <div style="font-size: 0.9rem; color: #CCCCCC; margin-bottom: 0.5rem;">
                                <strong>Focus:</strong> {query.get('focus_area', 'General')}
                            </div>
                            <div style="font-size: 0.8rem; color: #888888;">
                                <strong>Rationale:</strong> {query.get('rationale', 'Analysis pending')}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Option to execute searches and generate filled template
                    if st.button("🔍 Execute Personalized Search & Fill Template", type="primary", key="execute_personalized"):
                        with st.spinner("🔍 Executing personalized search and filling template..."):
                            try:
                                execute_personalized_search(queries, market, output_format)
                            except Exception as e:
                                st.error(f"Execution failed: {str(e)}")
                                st.error("Please try again or check your internet connection.")
                        
                except Exception as e:
                    st.error(f"Error during personalized analysis: {str(e)}")
                    st.error("Please ensure you have uploaded a valid image and completed market scanning.")
        else:
            if not user_query:
                st.warning("Please enter a search query in the sidebar first.")
            if not categories:
                st.warning("Please select categories through the main market scanning flow first.")
    
    # Display previous results if available
    if 'personalized_analysis' in st.session_state:
        st.markdown("---")
        st.markdown("### 📋 Previous Analysis Results")
        
        with st.expander("View Previous Analysis Results", expanded=False):
            st.json(st.session_state['personalized_analysis'])

def execute_personalized_search(queries, market, output_format):
    """Execute personalized search and generate template"""
    try:
        from utils.search_google import search_google
        from utils.scrape_url import scrape_urls
        from utils.personalized_scanning import generate_personalized_template
        
        # Progress indicator
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Execute searches for personalized queries
        status_text.text("🔍 Executing personalized search queries...")
        all_results = []
        for i, query in enumerate(queries):
            try:
                search_results = search_google(query.get('query', ''), num_results=5)
                all_results.extend(search_results)
                progress_bar.progress((i + 1) / len(queries) * 0.5)
            except Exception as e:
                st.warning(f"Search failed for query: {query.get('query', 'Unknown')}")
                continue
        
        if not all_results:
            st.error("No search results found. Please try with different queries.")
            return
        
        # Scrape content
        status_text.text("📰 Scraping content from sources...")
        urls_to_scrape = [result['link'] for result in all_results[:15]]
        scraped_content = scrape_urls(urls_to_scrape, max_workers=3)
        progress_bar.progress(0.8)
        
        # Generate personalized template
        status_text.text("🤖 Generating personalized template...")
        template_data = st.session_state.get('personalized_analysis', {})
        
        # Combine scraped content for analysis
        combined_analysis = {
            'search_results': all_results,
            'scraped_content': scraped_content,
            'source_urls': urls_to_scrape
        }
        
        # Get user query from session state
        user_query = st.session_state.get('current_user_input', '')
        if not user_query:
            user_query = "Energy transmission projects UK risk assessment"
        
        try:
            personalized_report = generate_personalized_template(template_data, combined_analysis, user_query)
            progress_bar.progress(1.0)
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"Template generation failed: {str(e)}")
            return
        
        # Display results
        st.markdown("### 📊 Personalized Intelligence Report")
        
        if 'error' not in personalized_report:
            # Show format type
            format_type = st.session_state.get('output_format', 'Template Fill')
            st.markdown(f"**Format:** {format_type}")
            
            # Display report title
            st.markdown(f"## {personalized_report.get('report_title', 'Personalized Market Intelligence Report')}")
            
            # Executive Summary
            st.markdown("### 🎯 Executive Summary")
            st.markdown(personalized_report.get('executive_summary', 'Summary not available'))
            
            # Display filled structure if available
            filled_structure = personalized_report.get('filled_structure', {})
            if filled_structure and 'data_mapping' in filled_structure:
                st.markdown("### 📋 Filled Template/Structure")
                st.markdown(f"**Structure Type:** {filled_structure.get('structure_type', 'Unknown')}")
                
                # Display data mapping in a table format
                data_mapping = filled_structure.get('data_mapping', [])
                if data_mapping:
                    st.markdown("**Data Population Results:**")
                    for item in data_mapping:
                        confidence_color = "#00DD88" if item.get('confidence') == 'High' else "#FFA500" if item.get('confidence') == 'Medium' else "#FF6B6B"
                        
                        st.markdown(f"""
                        <div class="metric-container">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                                <div style="font-weight: bold; color: white;">{item.get('field_name', 'Field')}</div>
                                <div style="background-color: {confidence_color}; padding: 0.2rem 0.5rem; border-radius: 3px; font-size: 0.8rem;">
                                    {item.get('confidence', 'Medium')} Confidence
                                </div>
                            </div>
                            <div style="font-size: 1.1rem; color: #4A90E2; font-weight: bold; margin-bottom: 0.5rem;">
                                {item.get('value', 'No data available')}
                            </div>
                            <div style="font-size: 0.8rem; color: #888888;">
                                <strong>Source:</strong> {item.get('source_reference', 'Market intelligence analysis')}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            # Key Sections - formatted based on output format
            sections = personalized_report.get('key_sections', [])
            for section in sections:
                st.markdown(f"### {section.get('section_title', 'Section')}")
                st.markdown(section.get('content', 'Content not available'))
                
                # Display metrics if available
                metrics = section.get('metrics', [])
                if metrics:
                    if format_type == "Template Fill":
                        st.markdown("**Additional Template Fields:**")
                        for i, metric in enumerate(metrics):
                            st.markdown(f"• **Field {i+1}:** {metric}")
                    else:
                        st.markdown("**Key Metrics:**")
                        cols = st.columns(min(len(metrics), 3))
                        for i, metric in enumerate(metrics):
                            with cols[i % 3]:
                                st.metric(f"Metric {i+1}", metric)
            
            # Recommendations
            recommendations = personalized_report.get('recommendations', [])
            if recommendations:
                st.markdown("### 🎯 Strategic Recommendations")
                for rec in recommendations:
                    priority_color = "#FF6B6B" if rec.get('priority') == 'High' else "#FFA500" if rec.get('priority') == 'Medium' else "#4A90E2"
                    
                    st.markdown(f"""
                    <div class="metric-container" style="border-left: 4px solid {priority_color};">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                            <div style="font-weight: bold; color: white;">{rec.get('recommendation', 'Recommendation')}</div>
                            <div style="background-color: {priority_color}; padding: 0.2rem 0.5rem; border-radius: 3px; font-size: 0.8rem;">
                                {rec.get('priority', 'Medium')} Priority
                            </div>
                        </div>
                        <div style="font-size: 0.9rem; color: #CCCCCC;">
                            {rec.get('rationale', 'Rationale not available')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Data Sources
            sources = personalized_report.get('data_sources', [])
            if sources:
                st.markdown("### 📚 Data Sources")
                for source in sources:
                    st.markdown(f"• {source}")
            
            # Template Fill specific message
            if format_type == "Template Fill":
                st.success("✅ Template successfully filled with market intelligence data!")
                st.info("This report is customized to match your uploaded template format with real market data.")
        
        else:
            st.error(f"Report generation failed: {personalized_report['error']}")
            
    except Exception as e:
        st.error(f"Error executing personalized search: {str(e)}")



def render_supply_chain_dashboard():
    """Render the supply chain dashboard with visual analytics"""
    
    # Check if data is loaded
    if not st.session_state.supply_chain_data_loaded:
        st.info("🔄 Click 'Load Supply Chain Data' in the sidebar to view dashboard analytics")
        return
    
    st.markdown("### 📊 Thames Water Supply Chain Intelligence")
    
    # Create sample data for visualization (internal data, not market data)
    import numpy as np
    import pandas as pd
    
    # Key metrics row
    st.markdown("### 📈 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Tier 2 Visibility", "68%", "↑23%")
    
    with col2:
        st.metric("Tier 3 Visibility", "34%", "↑12%")
    
    with col3:
        st.metric("Risk Score", "7.2/10", "↓1.3")
    
    with col4:
        st.metric("Capacity Utilization", "82%", "↑5%")
    
    # Main dashboard layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Supply chain network visualization
        st.markdown("#### 🌐 Supply Chain Network Map")
        
        # Create network-style visualization
        fig = go.Figure()
        
        # Tier 1 suppliers (close to center)
        tier1_x = np.random.normal(0, 0.3, 8)
        tier1_y = np.random.normal(0, 0.3, 8)
        
        # Tier 2 suppliers (medium distance)
        tier2_x = np.random.normal(0, 0.8, 15)
        tier2_y = np.random.normal(0, 0.8, 15)
        
        # Tier 3 suppliers (far from center)
        tier3_x = np.random.normal(0, 1.5, 25)
        tier3_y = np.random.normal(0, 1.5, 25)
        
        # Add main company at center
        fig.add_trace(go.Scatter(
            x=[0], y=[0],
            mode='markers',
            marker=dict(size=30, color='#FF6B6B', symbol='diamond'),
            name='Your Company',
            text=['Main Company'],
            hovertemplate='<b>%{text}</b><extra></extra>'
        ))
        
        # Add Tier 1 suppliers
        fig.add_trace(go.Scatter(
            x=tier1_x, y=tier1_y,
            mode='markers',
            marker=dict(size=20, color='#4ECDC4'),
            name='Tier 1 Suppliers',
            text=[f'Tier 1 Supplier {i+1}' for i in range(8)],
            hovertemplate='<b>%{text}</b><br>Risk: Low<br>Capacity: 85%<extra></extra>'
        ))
        
        # Add Tier 2 suppliers
        fig.add_trace(go.Scatter(
            x=tier2_x, y=tier2_y,
            mode='markers',
            marker=dict(size=15, color='#FFD93D'),
            name='Tier 2 Suppliers',
            text=[f'Tier 2 Supplier {i+1}' for i in range(15)],
            hovertemplate='<b>%{text}</b><br>Risk: Medium<br>Visibility: 68%<extra></extra>'
        ))
        
        # Add Tier 3 suppliers
        fig.add_trace(go.Scatter(
            x=tier3_x, y=tier3_y,
            mode='markers',
            marker=dict(size=10, color='#95A5A6'),
            name='Tier 3 Suppliers',
            text=[f'Tier 3 Supplier {i+1}' for i in range(25)],
            hovertemplate='<b>%{text}</b><br>Risk: High<br>Visibility: 34%<extra></extra>'
        ))
        
        fig.update_layout(
            showlegend=True,
            height=500,
            paper_bgcolor='#0e1117',
            plot_bgcolor='#0e1117',
            font_color='#fafafa',
            title_font_color='#fafafa',
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            title="Interactive Supply Chain Network",
            legend=dict(font_color='#fafafa')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Risk assessment panel
        st.markdown("#### ⚠️ Risk Assessment")
        
        # Risk categories with levels
        risk_data = [
            {"category": "Supply Disruption", "level": 7.2, "color": "#FF6B6B"},
            {"category": "Capacity Constraints", "level": 5.8, "color": "#FFD93D"},
            {"category": "Quality Issues", "level": 4.1, "color": "#4ECDC4"},
            {"category": "Geopolitical Risk", "level": 6.9, "color": "#FF6B6B"},
            {"category": "Financial Stability", "level": 3.2, "color": "#4ECDC4"}
        ]
        
        for risk in risk_data:
            level = risk["level"]
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{risk['category']}**")
            with col2:
                st.write(f"{level}/10")
            st.progress(level/10)
        
        # Capacity indicators
        st.markdown("#### 📊 Capacity Analysis")
        
        capacity_data = pd.DataFrame({
            'Supplier Type': ['Tier 1', 'Tier 2', 'Tier 3'],
            'Current Capacity': [85, 72, 45],
            'Available Capacity': [15, 28, 55],
            'Risk Level': ['Low', 'Medium', 'High']
        })
        
        fig_capacity = px.bar(
            capacity_data, 
            x='Supplier Type', 
            y=['Current Capacity', 'Available Capacity'],
            title="Capacity Utilization by Tier",
            color_discrete_map={
                'Current Capacity': '#4ECDC4',
                'Available Capacity': '#95A5A6'
            }
        )
        
        fig_capacity.update_layout(
            height=300,
            paper_bgcolor='#0e1117',
            plot_bgcolor='#0e1117',
            font_color='#fafafa',
            title_font_color='#fafafa',
            xaxis=dict(color='#fafafa'),
            yaxis=dict(color='#fafafa')
        )
        
        st.plotly_chart(fig_capacity, use_container_width=True)
    
    # Second row - detailed analytics
    st.markdown("### 📋 Detailed Analytics")
    
    tab1, tab2, tab3 = st.tabs(["📋 Project Delivery Tracker", "📊 Performance Reporting", "🎯 Action Items"])
    
    with tab1:
        # Project Delivery Tracker header
        st.markdown("### 📋 Project Delivery Tracker")
        st.markdown("Real-time visibility of Your Water Utility Capital Programme contract delivery against regulatory deadlines")
        st.markdown("💡 Click on any chart element to filter all related charts")
        
        # Key metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("**Total Capital Programme Value**")
            st.markdown("# £8820.0M")
        
        with col2:
            st.markdown("**Contracts Delivered**") 
            st.markdown("# 4/12")
        
        with col3:
            st.markdown("**Regulatory Penalty Exposure**")
            st.markdown("# £5.0M")
        
        with col4:
            st.markdown("**Critical Path Dependencies**")
            st.markdown("# 1 blocked")
        
        st.divider()
        
        # Contract Delivery Status (RAG) - Pie Chart
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### Contract Delivery Status (RAG)")
            
            rag_data = pd.DataFrame({
                'Status': ['Green', 'Amber', 'Red'],
                'Value': [50, 33.3, 16.7],
                'Count': [6, 4, 2]
            })
            
            fig_rag = px.pie(
                rag_data,
                values='Value',
                names='Status',
                color='Status',
                color_discrete_map={
                    'Green': '#28a745',
                    'Amber': '#ffc107', 
                    'Red': '#dc3545'
                },
                hole=0.3
            )
            
            fig_rag.update_traces(
                textposition='inside',
                textinfo='percent+label',
                textfont_size=12
            )
            
            fig_rag.update_layout(
                height=400,
                paper_bgcolor='#0e1117',
                plot_bgcolor='#0e1117',
                font_color='#fafafa',
                title_font_color='#fafafa',
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.02,
                    font_color='#fafafa'
                )
            )
            
            st.plotly_chart(fig_rag, use_container_width=True)
        
        with col2:
            st.markdown("#### Procurement Pipeline Flow")
            
            # Horizontal bar chart for procurement pipeline
            pipeline_data = pd.DataFrame({
                'Stage': ['Market Analysis', 'RFQ Preparation', 'Tender Process', 'Evaluation', 'Award', 'Contract'],
                'Contracts': [2, 2, 2, 2, 2, 2],
                'Percentage': [100, 100, 100, 100, 100, 100],
                'Color': ['#dc3545', '#fd7e14', '#ffc107', '#28a745', '#17a2b8', '#28a745']
            })
            
            fig_pipeline = go.Figure()
            
            for i, row in pipeline_data.iterrows():
                fig_pipeline.add_trace(go.Bar(
                    y=[row['Stage']],
                    x=[row['Percentage']],
                    orientation='h',
                    marker_color=row['Color'],
                    text=f"{row['Contracts']} contracts<br>({row['Percentage']:.0f}%)",
                    textposition='inside',
                    textfont=dict(color='white', size=10),
                    showlegend=False
                ))
            
            fig_pipeline.update_layout(
                height=400,
                paper_bgcolor='#0e1117',
                plot_bgcolor='#0e1117',
                font_color='#fafafa',
                title_font_color='#fafafa',
                xaxis=dict(showgrid=False, showticklabels=False, range=[0, 100], color='#fafafa'),
                yaxis=dict(showgrid=False, color='#fafafa'),
                margin=dict(l=0, r=0, t=0, b=0)
            )
            
            st.plotly_chart(fig_pipeline, use_container_width=True)
        
        # Site SG1 Baseline vs Forecast Dates (Gantt Chart)
        st.markdown("#### Site SG1 Baseline vs Forecast Dates (Color = Status)")
        
        # Create Gantt chart data
        import datetime
        from datetime import timedelta
        
        # Generate sample data for 30 sites with realistic project timelines
        sites_data = []
        base_date = datetime.date(2025, 9, 1)
        
        for i in range(1, 31):
            site_name = f"Site-{i:02d}"
            
            # Random project duration and start offset
            duration_days = np.random.randint(30, 120)
            start_offset = np.random.randint(0, 300)
            
            start_date = base_date + timedelta(days=start_offset)
            end_date = start_date + timedelta(days=duration_days)
            
            # Determine if forecast on time or delayed
            is_delayed = np.random.choice([True, False], p=[0.3, 0.7])  # 30% delayed
            status = "Forecast Delayed" if is_delayed else "Forecast On Time"
            color = "#FF6B6B" if is_delayed else "#4ECDC4"
            
            sites_data.append({
                'Site': site_name,
                'Start': start_date,
                'End': end_date,
                'Status': status,
                'Color': color
            })
        
        # Create Gantt chart
        fig_gantt = go.Figure()
        
        for i, site in enumerate(sites_data):
            fig_gantt.add_trace(go.Scatter(
                x=[site['Start'], site['End']],
                y=[site['Site'], site['Site']],
                mode='lines',
                line=dict(color=site['Color'], width=8),
                name=site['Status'],
                showlegend=(i == 0 and site['Status'] == 'Forecast On Time') or (i == 0 and site['Status'] == 'Forecast Delayed'),
                legendgroup=site['Status'],
                hovertemplate=f"<b>{site['Site']}</b><br>Start: {site['Start']}<br>End: {site['End']}<br>Status: {site['Status']}<extra></extra>"
            ))
        
        # Update layout for Gantt chart
        fig_gantt.update_layout(
            height=800,
            paper_bgcolor='#0e1117',
            plot_bgcolor='#0e1117',
            font_color='#fafafa',
            title_font_color='#fafafa',
            xaxis=dict(
                title="Date",
                showgrid=True,
                gridcolor='rgba(255,255,255,0.1)',
                type='date',
                color='#fafafa'
            ),
            yaxis=dict(
                title="Site",
                showgrid=True,
                gridcolor='rgba(255,255,255,0.1)',
                autorange='reversed',  # Show Site-01 at top
                color='#fafafa'
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font_color='#fafafa'
            ),
            margin=dict(l=80, r=20, t=60, b=20)
        )
        
        st.plotly_chart(fig_gantt, use_container_width=True)
    
    with tab2:
        # Performance Reporting with tiles
        st.markdown("### 📊 Performance Reporting Dashboard")
        
        # Create performance tiles in a 3x4 grid
        col1, col2, col3 = st.columns(3)
        
        # Define tile styling for dark theme
        def create_performance_tile(title, value, mode, mode_color):
            tile_html = f"""
            <div style="
                border-left: 4px solid #17a2b8;
                background: #262730;
                padding: 20px;
                margin: 10px 0;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.3);
                text-align: center;
                border: 1px solid #3d4450;
            ">
                <h3 style="color: #fafafa; margin-bottom: 10px; font-size: 1.1rem;">{title}</h3>
                <h1 style="color: #fafafa; margin: 15px 0; font-size: 2.5rem; font-weight: bold;">{value}</h1>
                <div style="
                    background: {mode_color};
                    color: white;
                    padding: 8px 16px;
                    border-radius: 20px;
                    font-weight: bold;
                    display: inline-block;
                    font-size: 0.9rem;
                ">
                    Mode: {mode}
                </div>
            </div>
            """
            return tile_html
        
        # Row 1
        with col1:
            st.markdown(create_performance_tile("Schedule Adherence", "79.0%", "Red", "#dc3545"), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_performance_tile("Budget Compliance", "82.4%", "Red", "#dc3545"), unsafe_allow_html=True)
        
        with col3:
            st.markdown(create_performance_tile("Quality Standards", "87.6%", "Amber", "#ffc107"), unsafe_allow_html=True)
        
        # Row 2 - Document Completion
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(create_performance_tile("Avg. Doc Completion", "91.3%", "Red", "#dc3545"), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_performance_tile("Avg. Doc Completion", "93.8%", "Red", "#dc3545"), unsafe_allow_html=True)
        
        with col3:
            st.markdown(create_performance_tile("Avg. Doc Completion", "92.7%", "Red", "#dc3545"), unsafe_allow_html=True)
        
        # Row 3 - Resource Allocation
        col1, col2, col3 = st.columns(3)
        
        def create_resource_tile(title, value, mode, mode_color):
            tile_html = f"""
            <div style="
                border-left: 4px solid #17a2b8;
                background: #262730;
                padding: 20px;
                margin: 10px 0;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.3);
                text-align: center;
                border: 1px solid #3d4450;
            ">
                <h3 style="color: #17a2b8; margin-bottom: 10px; font-size: 1.1rem;">{title}</h3>
                <h1 style="color: #fafafa; margin: 15px 0; font-size: 2.5rem; font-weight: bold;">{value}</h1>
                <div style="
                    background: {mode_color};
                    color: white;
                    padding: 8px 16px;
                    border-radius: 20px;
                    font-weight: bold;
                    display: inline-block;
                    font-size: 0.9rem;
                ">
                    {mode}
                </div>
            </div>
            """
            return tile_html
        
        with col1:
            st.markdown(create_resource_tile("Resourcing Allocation", "8.5 Months", "Amber", "#ffc107"), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_resource_tile("Resourcing Allocation", "5.7 Months", "Amber", "#ffc107"), unsafe_allow_html=True)
        
        with col3:
            st.markdown(create_resource_tile("Resourcing Allocation", "1.4 Months", "Red", "#dc3545"), unsafe_allow_html=True)
        
        # Row 4 - H&S File Signed
        col1, col2, col3 = st.columns(3)
        
        def create_hs_tile(title, value, status_color):
            checkmark = "✓" if status_color == "#28a745" else "✗"
            tile_html = f"""
            <div style="
                border-left: 4px solid #17a2b8;
                background: #262730;
                padding: 20px;
                margin: 10px 0;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.3);
                text-align: center;
                border: 1px solid #3d4450;
            ">
                <h3 style="color: #17a2b8; margin-bottom: 15px; font-size: 1.1rem;">{title}</h3>
                <div style="
                    background: {status_color};
                    color: white;
                    padding: 15px;
                    border-radius: 50%;
                    font-weight: bold;
                    display: inline-block;
                    font-size: 1.5rem;
                    width: 60px;
                    height: 60px;
                    line-height: 30px;
                ">
                    {checkmark}
                </div>
            </div>
            """
            return tile_html
        
        with col1:
            st.markdown(create_hs_tile("H&S File Signed", "✓", "#28a745"), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_hs_tile("H&S File Signed", "✗", "#dc3545"), unsafe_allow_html=True)
        
        with col3:
            st.markdown(create_hs_tile("H&S File Signed", "✓", "#28a745"), unsafe_allow_html=True)
    
    with tab3:
        # Action Items with table format similar to the images
        st.markdown("### 🎯 Action Items")
        
        # Sites >30 Days Behind Schedule
        st.markdown("#### Sites >30 Days Behind Schedule:")
        
        behind_schedule_data = {
            'Site': ['Site-13', 'Site-24', 'Site-29', 'Site-05', 'Site-04', 'Site-16', 'Site-22'],
            'Programme Name': ['Programme Gamma', 'Programme Gamma', 'Programme Beta', 'Programme Gamma', 'Programme Gamma', 'Programme Alpha', 'Programme Beta'],
            'Schedule Delay': ['45 days', '52 days', '38 days', '41 days', '33 days', '47 days', '35 days'],
            'Impact': ['High', 'High', 'Medium', 'High', 'Medium', 'High', 'Medium']
        }
        
        behind_df = pd.DataFrame(behind_schedule_data)
        
        # Create styled table for behind schedule sites with dark theme
        def style_behind_schedule(row):
            if row['Impact'] == 'High':
                return ['background-color: #3d1a1a; color: #fafafa'] * len(row)
            else:
                return ['background-color: #2d2617; color: #fafafa'] * len(row)
        
        styled_behind = behind_df.style.apply(style_behind_schedule, axis=1)
        st.dataframe(styled_behind, use_container_width=True, hide_index=True)
        
        st.markdown("")
        
        # Sites Failing H&S Checks (KPI 7)
        st.markdown("#### Sites Failing H&S Checks (KPI 7):")
        
        hs_failure_data = {
            'Site': ['Site-03', 'Site-05', 'Site-07', 'Site-13', 'Site-18', 'Site-21'],
            'Programme Name': ['Programme Gamma', 'Programme Gamma', 'Programme Beta', 'Programme Gamma', 'Programme Gamma', 'Programme Alpha'],
            'H&S File Signed': ['❌ Missing', '✅ Completed', '✅ Completed', '✅ Completed', '❌ Missing', '❌ Missing'],
            'Compliance Status': ['Non-Compliant', 'Review Required', 'Review Required', 'Review Required', 'Non-Compliant', 'Non-Compliant'],
            'Action Required': ['Immediate', 'Standard', 'Standard', 'Standard', 'Immediate', 'Immediate']
        }
        
        hs_df = pd.DataFrame(hs_failure_data)
        
        # Create styled table for H&S failures with dark theme
        def style_hs_failures(row):
            if row['Action Required'] == 'Immediate':
                return ['background-color: #3d1a1a; color: #fafafa'] * len(row)
            else:
                return ['background-color: #2e1a2e; color: #fafafa'] * len(row)
        
        styled_hs = hs_df.style.apply(style_hs_failures, axis=1)
        st.dataframe(styled_hs, use_container_width=True, hide_index=True)
        
        st.markdown("")
        
        # Priority Action Summary
        st.markdown("#### 🚨 Priority Actions Required:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🔴 Immediate Actions (Next 7 Days):**")
            st.markdown("• **Site-13, Site-24, Site-05** - Schedule recovery plans required")
            st.markdown("• **Site-03, Site-18, Site-21** - H&S file completion urgent")
            st.markdown("• **Resource reallocation** - Address 1.4 month allocation delay")
            st.markdown("• **Regulatory compliance** - £5.0M penalty exposure mitigation")
        
        with col2:
            st.markdown("**🟡 Medium Priority (Next 30 Days):**")
            st.markdown("• **Programme Beta sites** - Review schedule adherence")
            st.markdown("• **Document completion** - Improve from 91.3% to target 95%")
            st.markdown("• **H&S process review** - Prevent future compliance failures")
            st.markdown("• **Budget compliance** - Address 82.4% performance gap")

def render_market_intelligence_tab():
    """Render the market intelligence tab with existing functionality"""
    st.markdown("# 🎯 Market Intelligence")
    
    # Main search interface
    st.markdown("### 🔍 Market Research Configuration")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # User input for search query
        user_input = st.text_area(
            "Describe your market intelligence needs:",
            placeholder="e.g., 'I need intelligence on precast concrete suppliers for infrastructure projects in the UK'",
            height=100,
            key="market_search_input"
        )
        
        # Market selection
        market = st.selectbox(
            "Market Region:",
            ["UK", "EU", "US", "Global"],
            index=0,
            key="market_region_select"
        )
        
        # Time relevance
        timescale = st.selectbox(
            "Time Relevance:",
            ["Last 6 months", "Last 12 months", "Older than 12 months"],
            index=0,
            key="time_relevance_select"
        )
        
        # Research depth
        research_depth = st.selectbox(
            "Research Depth:",
            ["Quick (5 queries)", "Medium (10 queries)", "Deep (20 queries)"],
            index=1,
            key="research_depth_select"
        )
        
        if st.button("🔍 Generate Market Intelligence", type="primary", key="generate_intelligence_btn"):
            if user_input:
                # Store the user input and generate search options
                st.session_state.current_user_input = user_input
                st.session_state.current_market = market
                st.session_state.current_timescale = timescale
                st.session_state.current_research_depth = research_depth
                
                # Generate search options
                with st.spinner("Converting your request to search options..."):
                    search_options = generate_search_options(user_input, market)
                    
                    if search_options and len(search_options) > 0:
                        st.session_state.current_search_options = search_options
                        st.session_state.show_category_selection = True
                        st.rerun()
                    else:
                        st.error("Could not generate search options. Please try rephrasing your request.")
            else:
                st.warning("Please describe your procurement intelligence needs")
    
    with col2:
        st.markdown("#### 💡 Quick Tips")
        st.markdown("""
        **Be specific about:**
        - Industry/category
        - Geographic region  
        - Specific products/services
        - Time period of interest
        
        **Example queries:**
        - "Steel suppliers in Northern England"
        - "Electrical contractors for data centers"
        - "Infrastructure projects in Scotland"
        """)
    
    # Show category selection if search options are generated
    if getattr(st.session_state, 'show_category_selection', False) and 'current_search_options' in st.session_state:
        st.divider()
        st.markdown("### 🎯 Select Research Categories")
        
        search_options = st.session_state.current_search_options
        
        selected_categories = st.multiselect(
            "Select research categories (you can choose multiple):",
            search_options,
            default=[],
            key="category_selection_multiselect"
        )
        
        if selected_categories:
            st.markdown("**Research Configuration:**")
            st.markdown(f"- **Categories:** {', '.join(selected_categories)}")
            st.markdown(f"- **Market:** {st.session_state.current_market}")
            st.markdown(f"- **Time Scope:** {st.session_state.current_timescale}")
            st.markdown(f"- **Research Depth:** {st.session_state.current_research_depth}")
            
            if st.button("🚀 Start Research", type="primary", key="start_market_research"):
                execute_research_workflow(
                    selected_categories, 
                    st.session_state.current_market, 
                    st.session_state.current_timescale, 
                    st.session_state.current_research_depth
                )
                st.session_state.show_category_selection = False
    
    st.divider()
    
    # Display results section
    if st.session_state.intelligence_data and st.session_state.current_categories:
        st.divider()
        st.markdown("## 📊 Market Intelligence Analysis")
        
        # Show available analysis
        try:
            display_unified_dashboard()
        except Exception as e:
            st.error(f"Analysis unavailable: {str(e)}")
            
            # Show basic fallback content
            st.markdown("### 📊 Basic Market Intelligence")
            st.info("Market intelligence generation requires valid API keys and successful data scraping. Please ensure your API configuration is correct.")
            
            # Show sample format
            with st.expander("Sample Intelligence Format", expanded=True):
                st.markdown("""
                **Executive Summary:** Market analysis pending
                
                **Key Insights:**
                - Market trend analysis
                - Competitive landscape overview  
                - Risk assessment
                - Strategic recommendations
                
                **Data Sources:** Real-time market data collection
                """)
    else:
        # Show informational content when no data is available
        st.markdown("## 📊 Market Intelligence Analysis")
        st.info("Configure research parameters above and click 'Generate Market Intelligence' to start analysis.")
        
        # Show what the analysis would include
        with st.expander("What You'll Get", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                **Market Intelligence Includes:**
                - Real-time market trends
                - Supplier landscape analysis
                - Competitive insights
                - Risk assessment
                - Strategic recommendations
                """)
            
            with col2:
                st.markdown("""
                **Analysis Categories:**
                - Steel & Metals
                - Electrical Systems
                - Infrastructure
                - Transport & Logistics
                - Water Utilities
                """)

def display_queries_insights_export_tabs(queries_tab, insights_tab, export_tab):
    """Display the queries, insights, and export tabs"""
    
    with queries_tab:
        if st.session_state.intelligence_data and 'queries' in st.session_state.intelligence_data:
            st.markdown("### 🔍 Research Queries")
            queries = st.session_state.intelligence_data['queries']
            
            for i, query in enumerate(queries):
                st.markdown(f"**Query {i+1}:** {query.get('query', 'No query available')}")
                st.markdown(f"- **Category:** {query.get('category', 'General')}")
                st.markdown(f"- **Dimension:** {query.get('dimension', 'Market Intelligence')}")
                st.markdown(f"- **Intelligence Value:** {query.get('intelligence_value', 'Market insights')}")
                st.markdown("")
        else:
            st.info("No queries available. Run a research session first.")
    
    with insights_tab:
        if st.session_state.intelligence_data and 'search_results' in st.session_state.intelligence_data:
            st.markdown("### 📰 Source Insights")
            search_results = st.session_state.intelligence_data['search_results']
            
            if search_results:
                for i, result in enumerate(search_results[:10]):  # Show first 10 results
                    with st.expander(f"Source {i+1}: {result.get('title', 'No title')}"):
                        st.markdown(f"**URL:** {result.get('url', 'No URL')}")
                        st.markdown(f"**Snippet:** {result.get('snippet', 'No snippet available')}")
            else:
                st.info("No source insights available.")
        else:
            st.info("No source insights available. Run a research session first.")
    
    with export_tab:
        st.markdown("### 📄 Export Report")
        
        if st.session_state.intelligence_data and st.session_state.current_categories:
            # Export options
            export_format = st.selectbox(
                "Choose export format:",
                ["PDF Report", "CSV Data", "JSON Raw Data"]
            )
            
            if st.button("📥 Generate Export"):
                if export_format == "PDF Report":
                    # Generate PDF report
                    try:
                        if UTILS_AVAILABLE:
                            from utils.professional_pdf_report import generate_professional_pdf_report
                            
                            pdf_buffer = generate_professional_pdf_report(
                                st.session_state.intelligence_data,
                                st.session_state.current_categories
                            )
                            
                            st.download_button(
                                label="📄 Download PDF Report",
                                data=pdf_buffer.getvalue(),
                                file_name=f"market_intelligence_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                mime="application/pdf"
                            )
                        else:
                            st.error("PDF generation requires additional utility modules not available in this deployment.")
                    except Exception as e:
                        st.error(f"Error generating PDF: {str(e)}")
                
                elif export_format == "CSV Data":
                    # Export CSV data
                    st.info("CSV export functionality coming soon")
                
                elif export_format == "JSON Raw Data":
                    # Export JSON data
                    import json
                    json_data = json.dumps(st.session_state.intelligence_data, indent=2)
                    st.download_button(
                        label="📊 Download JSON Data",
                        data=json_data,
                        file_name=f"market_intelligence_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
        else:
            st.info("No data available for export. Run a research session first.")

def main():
    """Main application - Thames Water Demo"""
    
    # Sidebar with load data button
    with st.sidebar:
        st.markdown("# 🎯 Smart Acquisition")
        st.markdown("### Thames Water Demo")
        st.divider()
        
        # Load Supply Chain Data button
        if st.button("📊 Load Supply Chain Data", use_container_width=True):
            st.session_state.supply_chain_data_loaded = True
            st.success("Supply chain data loaded successfully!")
            st.rerun()
        
        if st.session_state.supply_chain_data_loaded:
            st.success("✅ Data loaded")
        else:
            st.info("💡 Click to load demo data")
    
    # Main title
    st.markdown("# 🎯 Smart Acquisition - Thames Water Demo")
    
    # Main navigation tabs (removed home tab)
    supply_chain_tab, market_intel_tab = st.tabs([
        "📊 Supply Chain Intelligence", 
        "🎯 Market Intelligence"
    ])
    
    with supply_chain_tab:
        render_supply_chain_dashboard()
    
    with market_intel_tab:
        render_market_intelligence_tab()

if __name__ == "__main__":
    main()

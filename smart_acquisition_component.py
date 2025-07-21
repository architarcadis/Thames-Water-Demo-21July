"""
Smart Acquisition Component - Modular version for embedding in other Streamlit apps
This module provides the complete Smart Acquisition functionality as a component
that can be easily integrated as a tab or section in another Streamlit application.
"""

import streamlit as st
import os
from dotenv import load_dotenv
import traceback
import random
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from streamlit_timeline import timeline
from utils.intelligent_query import generate_intelligent_queries
from utils.search_google import search_google
from utils.scrape_url import scrape_urls
from utils.gpt_analysis_enhanced import analyze_market_data
from utils.professional_pdf_report import generate_professional_pdf_report
from utils.search_options import generate_search_options, format_time_filter, get_research_depth_config

# Load environment variables
load_dotenv()

class SmartAcquisitionComponent:
    """Smart Acquisition component for embedding in other Streamlit apps"""
    
    def __init__(self):
        self.initialize_session_state()
        self.apply_component_styles()
    
    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'sa_intelligence_data' not in st.session_state:
            st.session_state.sa_intelligence_data = None
        if 'sa_queries_data' not in st.session_state:
            st.session_state.sa_queries_data = None
        if 'sa_current_categories' not in st.session_state:
            st.session_state.sa_current_categories = []
    
    def apply_component_styles(self):
        """Apply component-specific styling"""
        st.markdown("""
        <style>
        /* Smart Acquisition Component Styles */
        .sa-component {
            background-color: #0e1117;
            color: white;
            padding: 1rem;
            border-radius: 8px;
        }
        .sa-metric-container {
            background-color: #262730;
            padding: 1rem;
            border-radius: 10px;
            margin: 0.5rem 0;
        }
        .sa-swot-quadrant {
            background-color: #262730;
            padding: 1rem;
            border-radius: 10px;
            margin: 0.5rem;
            height: 200px;
        }
        .sa-query-display {
            background-color: #1a1a2e;
            padding: 1rem;
            border-radius: 8px;
            margin: 0.5rem 0;
            border-left: 4px solid #4A90E2;
        }
        
        /* Print styles for component */
        @media print {
            .sa-component * {
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }
        }
        </style>
        """, unsafe_allow_html=True)
    
    def render_search_interface(self):
        """Render the search options interface"""
        st.markdown("### 🔍 Market Intelligence Search")
        
        # Market selection
        market = st.selectbox(
            "Select Market",
            ["UK", "EU", "US", "Global"],
            key="sa_market_select"
        )
        
        # Category selection
        categories = [
            "Steel & Metals", "Electrical", "Infrastructure", 
            "Transport", "Technology", "Energy", "Construction Materials"
        ]
        
        selected_categories = st.multiselect(
            "Select Categories",
            categories,
            default=["Steel & Metals"],
            key="sa_categories_select"
        )
        
        # Research parameters
        col1, col2 = st.columns(2)
        with col1:
            timescale = st.selectbox(
                "Time Focus",
                ["6 months", "12 months", "2+ years"],
                key="sa_timescale"
            )
        
        with col2:
            research_depth = st.selectbox(
                "Research Depth", 
                ["Quick", "Medium", "Deep"],
                index=1,
                key="sa_research_depth"
            )
        
        # Start research button
        if st.button("🔍 Start Market Research", key="sa_start_research"):
            if selected_categories:
                with st.spinner("Conducting market intelligence research..."):
                    self.execute_research_workflow(selected_categories, market, timescale, research_depth)
            else:
                st.error("Please select at least one category")
        
        return selected_categories, market, timescale, research_depth
    
    def execute_research_workflow(self, categories, market, timescale, research_depth):
        """Execute the complete research workflow"""
        try:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            all_intelligence_data = {}
            all_queries_data = {}
            
            total_categories = len(categories)
            
            for i, category in enumerate(categories):
                status_text.text(f"Processing {category}...")
                progress_bar.progress((i + 0.2) / total_categories)
                
                # Generate queries
                queries_data = generate_intelligent_queries(
                    category, market, timescale, research_depth
                )
                all_queries_data[category] = queries_data
                
                progress_bar.progress((i + 0.4) / total_categories)
                
                # Execute searches
                all_urls = []
                for query_data in queries_data:
                    search_results = search_google(
                        query_data['optimized_query'], 
                        num_results=5,
                        time_filter=format_time_filter(timescale)
                    )
                    all_urls.extend([result['link'] for result in search_results])
                
                progress_bar.progress((i + 0.6) / total_categories)
                
                # Scrape content
                scraped_content = scrape_urls(all_urls[:10])
                
                progress_bar.progress((i + 0.8) / total_categories)
                
                # Analyze data
                intelligence_data = analyze_market_data(category, market, scraped_content)
                all_intelligence_data[category] = intelligence_data
                
                progress_bar.progress((i + 1) / total_categories)
            
            # Store results
            st.session_state.sa_intelligence_data = all_intelligence_data
            st.session_state.sa_queries_data = all_queries_data
            st.session_state.sa_current_categories = categories
            
            progress_bar.progress(1.0)
            status_text.text("Research complete!")
            
            st.success(f"Market intelligence research completed for {len(categories)} categories!")
            
        except Exception as e:
            st.error(f"Error during research: {str(e)}")
            st.error(traceback.format_exc())
    
    def render_intelligence_dashboard(self):
        """Render the main intelligence dashboard"""
        if not st.session_state.sa_intelligence_data:
            st.info("Start a research query to view market intelligence")
            return
        
        intelligence_data = st.session_state.sa_intelligence_data
        categories = st.session_state.sa_current_categories
        
        st.markdown("### 📊 Market Intelligence Dashboard")
        
        # Create tabs for each category
        if len(categories) > 1:
            tabs = st.tabs(categories)
            for i, category in enumerate(categories):
                with tabs[i]:
                    self.display_category_analysis(category, intelligence_data.get(category, {}))
        else:
            # Single category
            category = categories[0]
            self.display_category_analysis(category, intelligence_data.get(category, {}))
    
    def display_category_analysis(self, category, analysis):
        """Display analysis for a specific category"""
        if not analysis:
            st.warning(f"No analysis data available for {category}")
            return
        
        # Executive Summary
        if 'executive_summary' in analysis:
            exec_summary = analysis['executive_summary']
            st.markdown(f"""
            <div class="sa-metric-container">
                <h4 style="color: #4A90E2;">Executive Summary - {category}</h4>
                <p>{exec_summary.get('key_recommendation', 'Analysis pending')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Key metrics in columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            confidence = analysis.get('data_quality', {}).get('confidence_score', 0.8)
            st.metric("Confidence Score", f"{confidence:.1%}")
        
        with col2:
            urgency = analysis.get('executive_summary', {}).get('urgency_level', 'Medium')
            st.metric("Urgency Level", urgency)
        
        with col3:
            sources = len(analysis.get('source_urls', []))
            st.metric("Data Sources", sources)
        
        # Market insights
        if 'market_insights' in analysis:
            st.markdown("#### 💡 Key Market Insights")
            insights = analysis['market_insights']
            for i, insight in enumerate(insights[:3]):
                st.markdown(f"""
                <div class="sa-query-display">
                    <strong>{insight.get('title', f'Insight {i+1}')}</strong><br>
                    {insight.get('description', 'No description available')}
                </div>
                """, unsafe_allow_html=True)
        
        # Risk assessment
        if 'risk_assessment' in analysis:
            st.markdown("#### ⚠️ Risk Assessment")
            risks = analysis['risk_assessment']
            for risk in risks[:2]:
                risk_level = risk.get('level', 'Medium')
                color = {'High': '#FF6B6B', 'Medium': '#FFD93D', 'Low': '#6BCF7F'}.get(risk_level, '#FFD93D')
                st.markdown(f"""
                <div class="sa-metric-container" style="border-left: 4px solid {color};">
                    <strong>{risk.get('title', 'Risk Factor')}</strong> - {risk_level}<br>
                    {risk.get('description', 'No description available')}
                </div>
                """, unsafe_allow_html=True)
    
    def render_export_options(self):
        """Render export options"""
        if not st.session_state.sa_intelligence_data:
            st.info("Complete a research query to enable export options")
            return
        
        st.markdown("### 📄 Export Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Download PDF Report", key="sa_download_pdf"):
                try:
                    with st.spinner("Generating professional report..."):
                        pdf_buffer = generate_professional_pdf_report(st.session_state.sa_intelligence_data)
                        
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"market_intelligence_report_{timestamp}.pdf"
                        
                        st.download_button(
                            label="📥 Download Report",
                            data=pdf_buffer,
                            file_name=filename,
                            mime="application/pdf",
                            key="sa_pdf_download_btn"
                        )
                        
                except Exception as e:
                    st.error(f"Error generating PDF: {str(e)}")
        
        with col2:
            st.info("**PDF Report includes:**\n• Executive Summary\n• Market Analysis\n• Risk Assessment\n• Strategic Recommendations")
    
    def render_complete_component(self):
        """Render the complete Smart Acquisition component"""
        st.markdown('<div class="sa-component">', unsafe_allow_html=True)
        
        # Component header
        st.markdown("## 🎯 Smart Acquisition - Market Intelligence")
        
        # Create sub-tabs within the component
        tab1, tab2, tab3 = st.tabs(["🔍 Research", "📊 Intelligence", "📄 Export"])
        
        with tab1:
            self.render_search_interface()
        
        with tab2:
            self.render_intelligence_dashboard()
        
        with tab3:
            self.render_export_options()
        
        st.markdown('</div>', unsafe_allow_html=True)


# Main function to use in other apps
def render_smart_acquisition_tab():
    """
    Main function to render Smart Acquisition as a tab in another Streamlit app.
    
    Usage in your main app:
    ```python
    from smart_acquisition_component import render_smart_acquisition_tab
    
    # In your main app
    tab1, tab2, tab3 = st.tabs(["Your App", "Smart Acquisition", "Other Tab"])
    
    with tab2:
        render_smart_acquisition_tab()
    ```
    """
    component = SmartAcquisitionComponent()
    component.render_complete_component()


# Example of how to integrate with another app
if __name__ == "__main__":
    st.set_page_config(
        page_title="Example Integration",
        page_icon="🎯",
        layout="wide"
    )
    
    st.title("Example: Smart Acquisition Integration")
    
    # Example tabs showing integration
    tab1, tab2, tab3 = st.tabs(["Your Main App", "Smart Acquisition", "Other Features"])
    
    with tab1:
        st.markdown("## Your Main Application")
        st.write("This is where your main application content would go.")
        st.info("This is just an example of how to integrate Smart Acquisition as a tab.")
    
    with tab2:
        render_smart_acquisition_tab()
    
    with tab3:
        st.markdown("## Other Features") 
        st.write("Additional features or tabs for your application.")
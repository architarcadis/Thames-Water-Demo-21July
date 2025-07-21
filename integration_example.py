"""
Example: How to integrate Smart Acquisition as a tab in your existing Streamlit app

This shows the exact steps to add Smart Acquisition to any existing Streamlit application.
"""

import streamlit as st
from smart_acquisition_component import render_smart_acquisition_tab

# Your existing app configuration
st.set_page_config(
    page_title="Your App with Smart Acquisition",
    page_icon="🚀", 
    layout="wide"
)

def main():
    """Your main application"""
    
    st.title("🚀 Your Main Application")
    
    # This is where you integrate Smart Acquisition as a tab
    # Simply add it to your existing tabs
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Dashboard",           # Your existing tab 1
        "📈 Analytics",           # Your existing tab 2  
        "🎯 Market Intelligence", # Smart Acquisition tab
        "⚙️ Settings"            # Your existing tab 3
    ])
    
    # Your existing tab content
    with tab1:
        st.markdown("## Your Dashboard")
        st.write("This is your existing dashboard content")
        
        # Example of your existing functionality
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Revenue", "$1.2M", "12%")
        with col2: 
            st.metric("Users", "1,234", "5%")
        with col3:
            st.metric("Growth", "23%", "2%")
    
    with tab2:
        st.markdown("## Your Analytics")
        st.write("This is your existing analytics content")
        
        # Example chart
        import pandas as pd
        import numpy as np
        
        chart_data = pd.DataFrame(
            np.random.randn(20, 3),
            columns=['a', 'b', 'c']
        )
        st.line_chart(chart_data)
    
    # Smart Acquisition integration - just one line!
    with tab3:
        render_smart_acquisition_tab()
    
    # Your other existing content  
    with tab4:
        st.markdown("## Settings")
        st.write("Your application settings")
        
        st.checkbox("Enable notifications")
        st.selectbox("Theme", ["Light", "Dark"])
        st.slider("Refresh rate", 1, 60, 10)

if __name__ == "__main__":
    main()
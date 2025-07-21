# Smart Acquisition Integration Guide

## Quick Integration (3 Steps)

### Step 1: Copy the Component File
Copy `smart_acquisition_component.py` to your project directory.

### Step 2: Import and Add Tab
In your main app file:

```python
from smart_acquisition_component import render_smart_acquisition_tab

# Add to your existing tabs
tab1, tab2, tab3 = st.tabs(["Your App", "Market Intelligence", "Settings"])

with tab2:
    render_smart_acquisition_tab()  # That's it!
```

### Step 3: Copy Dependencies
Copy these folders/files to your project:
- `utils/` folder (entire directory)
- `prompts/` folder (entire directory) 
- `.env` file (with your API keys)

## Environment Variables Required

Add these to your `.env` file:
```bash
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here  
SEARCH_CX=your_search_engine_id_here
```

## Package Dependencies

Add these to your requirements.txt or install via pip:

```bash
streamlit
openai
google-api-python-client
trafilatura
plotly
streamlit-timeline
python-dotenv
reportlab
requests
beautifulsoup4
```

## Full Integration Examples

### Example 1: Simple Tab Integration

```python
import streamlit as st
from smart_acquisition_component import render_smart_acquisition_tab

st.set_page_config(page_title="My App", layout="wide")

tab1, tab2 = st.tabs(["Main App", "Market Intelligence"])

with tab1:
    st.write("Your existing app content")

with tab2:
    render_smart_acquisition_tab()
```

### Example 2: Sidebar Integration

```python
import streamlit as st
from smart_acquisition_component import SmartAcquisitionComponent

# Sidebar navigation
page = st.sidebar.selectbox("Choose Page", ["Dashboard", "Market Intelligence"])

if page == "Market Intelligence":
    component = SmartAcquisitionComponent()
    component.render_complete_component()
```

### Example 3: Custom Integration

```python
import streamlit as st
from smart_acquisition_component import SmartAcquisitionComponent

# Create component instance
sa_component = SmartAcquisitionComponent()

# Use individual methods
col1, col2 = st.columns(2)

with col1:
    sa_component.render_search_interface()

with col2:
    sa_component.render_intelligence_dashboard()
```

## Configuration Options

### Custom Styling
The component includes its own styling with the `sa-` prefix to avoid conflicts:

```css
.sa-component { /* Main container */ }
.sa-metric-container { /* Metric boxes */ }
.sa-query-display { /* Query displays */ }
```

### Session State Variables
The component uses prefixed session state to avoid conflicts:
- `sa_intelligence_data` - Analysis results
- `sa_queries_data` - Generated queries  
- `sa_current_categories` - Selected categories

## API Integration

### Access Analysis Data
```python
# Get current analysis data
if 'sa_intelligence_data' in st.session_state:
    data = st.session_state.sa_intelligence_data
    # Use data in your app
```

### Trigger Research Programmatically
```python
component = SmartAcquisitionComponent()
component.execute_research_workflow(
    categories=["Steel & Metals"], 
    market="UK",
    timescale="6 months",
    research_depth="Medium"
)
```

## File Structure for Integration

```
your_project/
├── main_app.py                    # Your main app
├── smart_acquisition_component.py # The component
├── utils/                         # Analysis utilities
│   ├── intelligent_query.py
│   ├── search_google.py
│   ├── scrape_url.py
│   ├── gpt_analysis_enhanced.py
│   └── professional_pdf_report.py
├── prompts/                       # AI prompts
│   ├── intelligent_query_generation.txt
│   └── market_summary.txt
├── .env                          # Environment variables
└── requirements.txt              # Dependencies
```

## Troubleshooting

### Common Issues

1. **Import Error**: Ensure `utils` folder is in your project
2. **API Errors**: Check your `.env` file has valid API keys
3. **Styling Conflicts**: Component uses `sa-` prefixed CSS classes
4. **Session State**: Component uses prefixed variables (`sa_*`)

### Testing Integration

Run the example file to test:
```bash
streamlit run integration_example.py
```

## Advanced Customization

### Custom Categories
```python
# Modify categories in render_search_interface()
categories = ["Your Category 1", "Your Category 2"]
```

### Custom Markets
```python
# Modify markets in render_search_interface()  
markets = ["Your Market 1", "Your Market 2"]
```

### Custom Styling
```python
# Override component styles
st.markdown("""
<style>
.sa-metric-container {
    background-color: your_color !important;
}
</style>
""", unsafe_allow_html=True)
```

## Support

The component is self-contained and includes:
- Full market intelligence functionality
- PDF export capabilities
- Real-time data analysis
- Professional reporting
- Print-friendly output

Simply add it as a tab and it works independently within your app.
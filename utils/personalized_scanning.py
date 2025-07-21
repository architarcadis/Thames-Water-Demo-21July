import os
import base64
from openai import OpenAI
import json
from PIL import Image
import io

def analyze_image_and_query(image_file, user_query, market="UK"):
    """
    Analyze uploaded image and combine with user query to generate personalized search queries
    """
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Convert image to base64
        image_base64 = encode_image_to_base64(image_file)
        
        # Generate personalized search queries using multimodal GPT-4
        prompt = f"""
        Analyze the provided image and user query to generate personalized market intelligence search queries.
        
        User Query: {user_query}
        Market: {market}
        
        IMPORTANT: If the image shows a table, matrix, or structured format that needs to be filled with data, focus on generating search queries that will gather the specific information needed to populate that structure.
        
        Based on the image content and user query, generate 5-8 highly specific search queries that would gather the most relevant market intelligence. Consider:
        - Visual elements in the image (tables, matrices, charts, forms, etc.)
        - Specific data fields that need to be filled
        - User's specific needs expressed in the query
        - Market context and region
        - Procurement and business intelligence focus
        
        For table/matrix filling: Generate queries that target each dimension of the table (rows, columns, intersections).
        
        Provide response in JSON format:
        {{
            "image_analysis": {{
                "description": "What you see in the image",
                "key_elements": ["element1", "element2", "element3"],
                "business_context": "How this relates to market intelligence",
                "structure_type": "table/matrix/form/document/other",
                "data_requirements": "What specific data needs to be filled"
            }},
            "personalized_queries": [
                {{
                    "query": "Specific search query targeting table data",
                    "rationale": "Why this query is relevant for filling the structure",
                    "focus_area": "Market area this targets",
                    "intelligence_value": "What insights this will provide",
                    "table_relevance": "How this helps fill the table/matrix"
                }}
            ],
            "template_suggestions": {{
                "report_structure": "Suggested structure for final output",
                "key_metrics": ["metric1", "metric2", "metric3"],
                "visualization_ideas": ["chart1", "chart2", "chart3"],
                "filling_strategy": "How to approach filling the identified structure"
            }}
        }}
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
        
    except Exception as e:
        print(f"Image analysis error: {str(e)}")  # Debug print
        return {"error": f"Image analysis failed: {str(e)}"}

def generate_personalized_template(template_data, analysis_results, user_query):
    """
    Generate a personalized template/report based on user requirements and analysis results
    """
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        prompt = f"""
        Create a personalized market intelligence report that fills the structure identified in the uploaded image.
        
        User Query: {user_query}
        Image Analysis: {template_data.get('image_analysis', {})}
        Analysis Results: {analysis_results}
        Template Suggestions: {template_data.get('template_suggestions', {})}
        
        CRITICAL: If the image shows a table/matrix/form that needs to be filled with data, focus on providing the specific data points needed for each cell/field. Use the scraped market intelligence data to populate the structure.
        
        Based on the structure type identified:
        - For tables/matrices: Provide specific values for each row-column intersection
        - For forms: Fill in the requested fields with relevant data
        - For reports: Follow the template structure shown in the image
        
        Use ONLY the real market data from the analysis results. Do not use placeholder or mock data.
        
        Generate a comprehensive response that includes:
        - Executive summary tailored to their needs
        - Filled structure with real market data
        - Key findings with quantitative data from sources
        - Strategic recommendations based on real intelligence
        - Source attribution for all data points
        
        Provide response in JSON format:
        {{
            "report_title": "Professional report title matching user needs",
            "executive_summary": "Tailored executive summary",
            "filled_structure": {{
                "structure_type": "table/matrix/form/document",
                "data_mapping": [
                    {{
                        "field_name": "Field or cell identifier",
                        "value": "Real data value from market intelligence",
                        "confidence": "High/Medium/Low based on data quality",
                        "source_reference": "Source of this data point"
                    }}
                ]
            }},
            "key_sections": [
                {{
                    "section_title": "Section name",
                    "content": "Detailed content with real data",
                    "metrics": ["real metric1", "real metric2"],
                    "visualizations": ["data visualization description"]
                }}
            ],
            "recommendations": [
                {{
                    "recommendation": "Strategic recommendation based on real data",
                    "rationale": "Supporting reasoning with market evidence",
                    "priority": "High/Medium/Low"
                }}
            ],
            "data_sources": ["source1", "source2", "source3"]
        }}
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a market intelligence specialist creating personalized reports."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
        
    except Exception as e:
        print(f"Template generation error: {str(e)}")  # Debug print
        return {"error": f"Template generation failed: {str(e)}"}

def encode_image_to_base64(image_file):
    """
    Convert uploaded image file to base64 string
    """
    try:
        # Read the image file
        image = Image.open(image_file)
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Save to bytes
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG')
        image_bytes = buffer.getvalue()
        
        # Convert to base64
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        return image_base64
        
    except Exception as e:
        raise Exception(f"Image encoding failed: {str(e)}")

def create_visual_report(report_data, format_type="professional"):
    """
    Create a visual report based on the generated template
    """
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Generate visual elements description
        prompt = f"""
        Based on the following report data, create detailed descriptions for visual elements:
        
        Report Data: {report_data}
        Format Type: {format_type}
        
        Generate descriptions for:
        - Charts and graphs that would enhance the report
        - Visual layout suggestions
        - Color scheme and styling
        - Infographic elements
        
        Provide response in JSON format:
        {{
            "visual_elements": [
                {{
                    "type": "chart/graph/infographic",
                    "description": "Detailed description",
                    "data_source": "What data to display",
                    "placement": "Where in report"
                }}
            ],
            "design_suggestions": {{
                "color_scheme": "Professional color palette",
                "layout": "Report layout structure",
                "typography": "Font and text suggestions"
            }}
        }}
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a design specialist for business intelligence reports."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
        
    except Exception as e:
        return {"error": f"Visual report creation failed: {str(e)}"}
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from io import BytesIO
from datetime import datetime

def generate_pdf_report(intelligence_data):
    """
    Generate a professional PDF report from intelligence data
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=HexColor('#2E4057')
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=20,
        textColor=HexColor('#2E4057')
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubheading',
        parent=styles['Heading3'],
        fontSize=14,
        spaceAfter=6,
        spaceBefore=12,
        textColor=HexColor('#4A5568')
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        alignment=TA_JUSTIFY
    )
    
    # Build the story
    story = []
    
    # Cover Page
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph("SMART Acquisition", title_style))
    story.append(Paragraph("Built-Asset Procurement Intelligence Report", heading_style))
    story.append(Spacer(1, 0.5*inch))
    
    # Add category and date
    category = intelligence_data.get('category', 'General Procurement')
    report_date = datetime.now().strftime("%B %d, %Y")
    
    story.append(Paragraph(f"<b>Category:</b> {category}", body_style))
    story.append(Paragraph(f"<b>Report Date:</b> {report_date}", body_style))
    story.append(PageBreak())
    
    # Executive Summary
    story.append(Paragraph("Executive Summary", heading_style))
    
    # Get the actual analysis data from category analyses
    category_analyses = intelligence_data.get('category_analyses', {})
    analysis = intelligence_data.get('analysis', {})
    
    if category_analyses:
        # Use data from the first category analysis
        first_category = next(iter(category_analyses.keys()))
        analysis = category_analyses[first_category]
        story.append(Paragraph(f"<b>Primary Category:</b> {first_category}", body_style))
        story.append(Spacer(1, 0.1*inch))
    
    if 'market_summary' in analysis:
        for point in analysis['market_summary']:
            story.append(Paragraph(f"• {point}", body_style))
    
    story.append(PageBreak())
    
    # Market Intelligence Snapshot
    story.append(Paragraph("Market Intelligence Snapshot", heading_style))
    story.append(Paragraph("This section provides a comprehensive overview of the current market conditions, key players, and emerging trends in the procurement category.", body_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Market Dynamics
    story.append(Paragraph("Market Dynamics", heading_style))
    market_dynamics = analysis.get('market_dynamics', {})
    key_trends = market_dynamics.get('key_trends', [])
    
    for trend in key_trends:
        if isinstance(trend, dict):
            trend_text = trend.get('trend', 'Market Trend')
            quantitative_data = trend.get('quantitative_data', '')
            source_evidence = trend.get('source_evidence', '')
            
            story.append(Paragraph(f"<b>{trend_text}</b>", subheading_style))
            if quantitative_data:
                story.append(Paragraph(f"Data: {quantitative_data}", body_style))
            if source_evidence:
                story.append(Paragraph(f"Evidence: {source_evidence}", body_style))
            story.append(Spacer(1, 0.1*inch))
        else:
            story.append(Paragraph(f"• {trend}", body_style))
    
    # Market Opportunities
    story.append(Paragraph("Market Opportunities", heading_style))
    market_opportunities = analysis.get('market_opportunities', [])
    
    for opp in market_opportunities:
        if isinstance(opp, dict):
            opp_text = opp.get('opportunity', 'Market Opportunity')
            quantitative_potential = opp.get('quantitative_potential', '')
            source_evidence = opp.get('source_evidence', '')
            
            story.append(Paragraph(f"<b>{opp_text}</b>", subheading_style))
            if quantitative_potential:
                story.append(Paragraph(f"Potential: {quantitative_potential}", body_style))
            if source_evidence:
                story.append(Paragraph(f"Evidence: {source_evidence}", body_style))
            story.append(Spacer(1, 0.1*inch))
        else:
            story.append(Paragraph(f"• {opp}", body_style))
    
    story.append(PageBreak())
    
    # Risk Radar
    story.append(Paragraph("Risk Radar", heading_style))
    story.append(Paragraph("The following risk assessment provides a comprehensive view of potential challenges and mitigation strategies.", body_style))
    story.append(Spacer(1, 0.2*inch))
    
    risk_flags = analysis.get('risk_flags', [])
    for risk in risk_flags:
        if isinstance(risk, dict):
            risk_type = risk.get('risk_type', 'Risk Factor')
            risk_desc = risk.get('description', '')
            likelihood = risk.get('likelihood', 'Medium')
            impact = risk.get('impact', 'Medium')
            mitigation = risk.get('mitigation', '')
            
            story.append(Paragraph(f"<b>{risk_type}</b> (Likelihood: {likelihood}, Impact: {impact})", subheading_style))
            if risk_desc:
                story.append(Paragraph(f"Description: {risk_desc}", body_style))
            if mitigation:
                story.append(Paragraph(f"Mitigation: {mitigation}", body_style))
            story.append(Spacer(1, 0.1*inch))
        else:
            story.append(Paragraph(f"• {risk}", body_style))
    
    story.append(PageBreak())
    
    # Strategic Recommendations
    story.append(Paragraph("Strategic Recommendations", heading_style))
    
    strategic_recommendations = analysis.get('strategic_recommendations', [])
    
    for rec in strategic_recommendations:
        if isinstance(rec, dict):
            recommendation = rec.get('recommendation', 'Recommendation')
            rationale = rec.get('rationale', '')
            timeline = rec.get('timeline', '')
            
            story.append(Paragraph(f"<b>{recommendation}</b>", subheading_style))
            if rationale:
                story.append(Paragraph(f"Rationale: {rationale}", body_style))
            if timeline:
                story.append(Paragraph(f"Timeline: {timeline}", body_style))
            story.append(Spacer(1, 0.1*inch))
        else:
            story.append(Paragraph(f"• {rec}", body_style))
    
    # Add quantitative metrics if available
    if 'quantitative_metrics' in analysis:
        story.append(Paragraph("Key Quantitative Metrics", heading_style))
        metrics = analysis.get('quantitative_metrics', {})
        key_metrics = metrics.get('key_metrics', [])
        
        for metric in key_metrics:
            if isinstance(metric, dict):
                metric_name = metric.get('metric', 'Metric')
                value = metric.get('value', 'N/A')
                context = metric.get('context', '')
                
                story.append(Paragraph(f"<b>{metric_name}:</b> {value}", body_style))
                if context:
                    story.append(Paragraph(f"Context: {context}", body_style))
                story.append(Spacer(1, 0.1*inch))
            else:
                story.append(Paragraph(f"• {metric}", body_style))
    
    story.append(PageBreak())
    
    # Appendix
    story.append(Paragraph("Appendix", heading_style))
    
    # Queries used
    story.append(Paragraph("Intelligence Queries", subheading_style))
    queries = intelligence_data.get('queries', [])
    for i, query in enumerate(queries, 1):
        story.append(Paragraph(f"{i}. {query.get('query', '')}", body_style))
    
    # Sources
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Data Sources", subheading_style))
    search_results = intelligence_data.get('search_results', [])
    for i, result in enumerate(search_results[:10], 1):
        story.append(Paragraph(f"{i}. {result.get('title', '')} - {result.get('displayLink', '')}", body_style))
    
    # Build PDF
    doc.build(story)
    
    # Return the buffer
    buffer.seek(0)
    return buffer.getvalue()

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.colors import HexColor, black, white, red, green, orange
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from io import BytesIO
from datetime import datetime
import os

def generate_enhanced_pdf_report(intelligence_data):
    """
    Generate a professional PDF report in McKinsey/Gartner style
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    
    # Define enhanced styles
    styles = getSampleStyleSheet()
    
    # McKinsey-style title
    title_style = ParagraphStyle(
        'McKinseyTitle',
        parent=styles['Heading1'],
        fontSize=32,
        spaceAfter=16,
        alignment=TA_LEFT,
        textColor=HexColor('#000000'),
        fontName='Helvetica-Bold'
    )
    
    # McKinsey-style subtitle
    subtitle_style = ParagraphStyle(
        'McKinseySubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=24,
        alignment=TA_LEFT,
        textColor=HexColor('#666666'),
        fontName='Helvetica'
    )
    
    # Executive summary style
    exec_summary_style = ParagraphStyle(
        'ExecutiveSummary',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        textColor=HexColor('#333333'),
        fontName='Helvetica',
        backColor=HexColor('#F8F9FA'),
        borderColor=HexColor('#E5E7EB'),
        borderWidth=1,
        borderPadding=12
    )
    
    # Section heading style
    section_heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=20,
        textColor=HexColor('#1E40AF'),
        fontName='Helvetica-Bold'
    )
    
    # Subsection heading style
    subsection_heading_style = ParagraphStyle(
        'SubsectionHeading',
        parent=styles['Heading3'],
        fontSize=14,
        spaceAfter=8,
        spaceBefore=12,
        textColor=HexColor('#374151'),
        fontName='Helvetica-Bold'
    )
    
    # Body text style
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=8,
        alignment=TA_JUSTIFY,
        textColor=HexColor('#374151')
    )
    
    # Highlight style
    highlight_style = ParagraphStyle(
        'Highlight',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=8,
        alignment=TA_LEFT,
        textColor=HexColor('#1E40AF'),
        fontName='Helvetica-Bold'
    )
    
    # Bullet point style
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        leftIndent=20,
        bulletIndent=10,
        alignment=TA_LEFT,
        textColor=HexColor('#374151')
    )
    
    # Build the story
    story = []
    
    # COVER PAGE - McKinsey style
    story.append(Spacer(1, 1*inch))
    story.append(Paragraph("Market Intelligence Report", title_style))
    story.append(Paragraph("Strategic Market Analysis for Built-Asset Procurement", subtitle_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Add a subtle horizontal line
    from reportlab.platypus import HRFlowable
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#E5E7EB')))
    story.append(Spacer(1, 0.4*inch))
    
    # Report metadata
    categories = intelligence_data.get('categories', ['General Procurement'])
    market = intelligence_data.get('market', 'UK')
    report_date = datetime.now().strftime("%B %d, %Y")
    report_id = f"SI-{datetime.now().strftime('%Y%m%d')}-{hash(str(categories)) % 10000:04d}"
    
    # Create info box
    info_data = [
        ['Report ID:', report_id],
        ['Market Focus:', market],
        ['Categories:', ', '.join(categories)],
        ['Generated:', report_date],
        ['Classification:', 'Internal Use']
    ]
    
    info_table = Table(info_data, colWidths=[2*inch, 3*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HexColor('#F8FAFC')),
        ('TEXTCOLOR', (0, 0), (0, -1), HexColor('#64748B')),
        ('TEXTCOLOR', (1, 0), (1, -1), HexColor('#1E40AF')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#E2E8F0')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    story.append(info_table)
    story.append(PageBreak())
    
    # EXECUTIVE SUMMARY - McKinsey style
    story.append(Paragraph("Executive Summary", section_heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Get analysis data
    category_analyses = intelligence_data.get('category_analyses', {})
    main_analysis = intelligence_data.get('analysis', {})
    
    if category_analyses:
        first_category = next(iter(category_analyses.keys()))
        analysis = category_analyses[first_category]
        
        # Create executive summary box
        exec_summary = analysis.get('executive_summary', {})
        if exec_summary:
            exec_text = f"""
            <b>Key Strategic Recommendation:</b> {exec_summary.get('key_recommendation', 'Analysis pending')}
            <br/><br/>
            <b>Market Assessment:</b> Based on our analysis of {first_category} market dynamics, we identify significant opportunities and strategic imperatives for procurement optimization.
            <br/><br/>
            <b>Decision Framework:</b> Urgency Level: {exec_summary.get('urgency_level', 'Medium')} | Confidence: {exec_summary.get('confidence_level', 'Medium')} | Timeline: {exec_summary.get('decision_window', 'Medium-term')}
            """
            story.append(Paragraph(exec_text, exec_summary_style))
    else:
        analysis = main_analysis
        story.append(Paragraph("Comprehensive market intelligence analysis covering strategic procurement opportunities and risk assessment.", exec_summary_style))
    
    story.append(Spacer(1, 0.3*inch))
    
    # Key insights summary
    insights = analysis.get('insights', [])
    if insights:
        story.append(Paragraph("Key Market Insights", subsection_heading_style))
        
        # Create insights table
        insights_data = [['#', 'Insight', 'Impact']]
        for i, insight in enumerate(insights[:4], 1):
            insights_data.append([
                str(i), 
                insight.get('headline', 'Market Insight')[:60] + '...' if len(insight.get('headline', '')) > 60 else insight.get('headline', 'Market Insight'),
                insight.get('confidence', 'Medium')
            ])
        
        insights_table = Table(insights_data, colWidths=[0.5*inch, 4*inch, 1*inch])
        insights_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1E40AF')),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#FFFFFF')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#FFFFFF')),
            ('TEXTCOLOR', (0, 1), (-1, -1), HexColor('#374151')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#E5E7EB')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(insights_table)
    
    story.append(PageBreak())
    
    # KEY INSIGHTS
    story.append(Paragraph("Key Market Insights", section_heading_style))
    
    insights = analysis.get('insights', [])
    if insights:
        for i, insight in enumerate(insights[:5], 1):
            story.append(Paragraph(f"Insight {i}: {insight.get('headline', 'Market Insight')}", subsection_heading_style))
            story.append(Paragraph(insight.get('explanation', 'Analysis pending'), body_style))
            if insight.get('evidence'):
                story.append(Paragraph(f"Evidence: {insight.get('evidence', 'Data pending')}", bullet_style))
            story.append(Spacer(1, 0.1*inch))
    
    story.append(PageBreak())
    
    # QUANTITATIVE ANALYSIS
    story.append(Paragraph("Quantitative Market Analysis", section_heading_style))
    
    quantitative_metrics = analysis.get('quantitative_metrics', {})
    if quantitative_metrics:
        key_metrics = quantitative_metrics.get('key_metrics', [])
        
        if key_metrics:
            for metric in key_metrics:
                if isinstance(metric, dict):
                    story.append(Paragraph(f"{metric.get('metric', 'Metric')}: {metric.get('value', 'N/A')}", highlight_style))
                    if metric.get('context'):
                        story.append(Paragraph(metric.get('context', ''), body_style))
                    story.append(Spacer(1, 0.1*inch))
    
    story.append(PageBreak())
    
    # MARKET DYNAMICS
    story.append(Paragraph("Market Dynamics", section_heading_style))
    
    market_dynamics = analysis.get('market_dynamics', {})
    key_trends = market_dynamics.get('key_trends', [])
    
    if key_trends:
        for i, trend in enumerate(key_trends[:5], 1):
            if isinstance(trend, dict):
                story.append(Paragraph(f"Trend {i}: {trend.get('trend', 'Market Trend')}", subsection_heading_style))
                if trend.get('quantitative_data'):
                    story.append(Paragraph(f"Data: {trend.get('quantitative_data', '')}", body_style))
                if trend.get('source_evidence'):
                    story.append(Paragraph(f"Evidence: {trend.get('source_evidence', '')}", bullet_style))
                story.append(Spacer(1, 0.1*inch))
    
    story.append(PageBreak())
    
    # RISK ASSESSMENT
    story.append(Paragraph("Risk Assessment", section_heading_style))
    
    risk_flags = analysis.get('risk_flags', [])
    if risk_flags:
        for i, risk in enumerate(risk_flags[:5], 1):
            if isinstance(risk, dict):
                risk_type = risk.get('risk_type', 'Risk Factor')
                likelihood = risk.get('likelihood', 'Medium')
                impact = risk.get('impact', 'Medium')
                
                story.append(Paragraph(f"Risk {i}: {risk_type}", subsection_heading_style))
                story.append(Paragraph(f"Likelihood: {likelihood} | Impact: {impact}", highlight_style))
                
                if risk.get('description'):
                    story.append(Paragraph(risk.get('description', ''), body_style))
                if risk.get('mitigation'):
                    story.append(Paragraph(f"Mitigation: {risk.get('mitigation', '')}", bullet_style))
                story.append(Spacer(1, 0.1*inch))
    
    story.append(PageBreak())
    
    # STRATEGIC RECOMMENDATIONS
    story.append(Paragraph("Strategic Recommendations", section_heading_style))
    
    strategic_recommendations = analysis.get('strategic_recommendations', [])
    if strategic_recommendations:
        for i, rec in enumerate(strategic_recommendations[:5], 1):
            if isinstance(rec, dict):
                story.append(Paragraph(f"Recommendation {i}: {rec.get('recommendation', 'Recommendation')}", subsection_heading_style))
                if rec.get('rationale'):
                    story.append(Paragraph(f"Rationale: {rec.get('rationale', '')}", body_style))
                if rec.get('timeline'):
                    story.append(Paragraph(f"Timeline: {rec.get('timeline', '')}", bullet_style))
                story.append(Spacer(1, 0.1*inch))
    
    story.append(PageBreak())
    
    # APPENDIX
    story.append(Paragraph("Appendix", section_heading_style))
    
    # Data Sources
    story.append(Paragraph("Data Sources", subsection_heading_style))
    search_results = intelligence_data.get('search_results', [])
    
    if search_results:
        for i, result in enumerate(search_results[:10], 1):
            story.append(Paragraph(f"{i}. {result.get('title', 'Source Title')}", body_style))
            story.append(Paragraph(f"   URL: {result.get('link', 'No URL')}", bullet_style))
            story.append(Paragraph(f"   Domain: {result.get('displayLink', 'Unknown')}", bullet_style))
            story.append(Spacer(1, 0.1*inch))
    
    # Query methodology
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Query Methodology", subsection_heading_style))
    queries = intelligence_data.get('queries', [])
    
    if queries:
        for i, query in enumerate(queries, 1):
            story.append(Paragraph(f"{i}. {query.get('query', 'Query')}", body_style))
            story.append(Paragraph(f"   Focus: {query.get('dimension', 'General')}", bullet_style))
            story.append(Paragraph(f"   Intelligence Value: {query.get('intelligence_value', 'Market insights')}", bullet_style))
            story.append(Spacer(1, 0.1*inch))
    
    # Build PDF
    doc.build(story)
    
    # Return the buffer
    buffer.seek(0)
    return buffer.getvalue()
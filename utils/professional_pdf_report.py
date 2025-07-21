from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.colors import HexColor, black, white, red, green, orange
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus.flowables import HRFlowable
from io import BytesIO
from datetime import datetime
import os

def generate_professional_pdf_report(intelligence_data):
    """
    Generate a professional PDF report matching high-quality consulting standards
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    
    # Define professional styles
    styles = getSampleStyleSheet()
    
    # Professional title style
    title_style = ParagraphStyle(
        'ProfessionalTitle',
        parent=styles['Heading1'],
        fontSize=32,
        spaceAfter=12,
        alignment=TA_LEFT,
        textColor=HexColor('#1a1a1a'),
        fontName='Helvetica-Bold',
        leading=36
    )
    
    # Professional subtitle style
    subtitle_style = ParagraphStyle(
        'ProfessionalSubtitle',
        parent=styles['Heading2'],
        fontSize=18,
        spaceAfter=16,
        alignment=TA_LEFT,
        textColor=HexColor('#2c3e50'),
        fontName='Helvetica',
        leading=22
    )
    
    # Section heading style
    section_heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=10,
        spaceBefore=16,
        alignment=TA_LEFT,
        textColor=HexColor('#1a1a1a'),
        fontName='Helvetica-Bold'
    )
    
    # Subsection heading style
    subsection_heading_style = ParagraphStyle(
        'SubsectionHeading',
        parent=styles['Heading3'],
        fontSize=13,
        spaceAfter=8,
        spaceBefore=12,
        alignment=TA_LEFT,
        textColor=HexColor('#2c3e50'),
        fontName='Helvetica-Bold'
    )
    
    # Executive summary box style
    exec_summary_style = ParagraphStyle(
        'ExecutiveSummary',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        textColor=HexColor('#2c3e50'),
        fontName='Helvetica',
        backColor=HexColor('#f8f9fa'),
        borderColor=HexColor('#3498db'),
        borderWidth=2,
        borderPadding=16,
        leftIndent=12,
        rightIndent=12
    )
    
    # Body text style
    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=10,
        alignment=TA_JUSTIFY,
        textColor=HexColor('#2c3e50'),
        fontName='Helvetica',
        leading=14
    )
    
    # Highlight style
    highlight_style = ParagraphStyle(
        'Highlight',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
        alignment=TA_LEFT,
        textColor=HexColor('#e74c3c'),
        fontName='Helvetica-Bold'
    )
    
    # Build the story
    story = []
    
    # COVER PAGE
    story.append(Spacer(1, 1.5*inch))
    story.append(Paragraph("Market Intelligence Report", title_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Strategic Analysis for Built-Asset Procurement", subtitle_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Professional blue line
    story.append(HRFlowable(width="100%", thickness=3, color=HexColor('#3498db')))
    story.append(Spacer(1, 0.3*inch))
    
    # Report metadata
    categories = intelligence_data.get('categories', ['General Procurement'])
    market = intelligence_data.get('market', 'UK')
    report_date = datetime.now().strftime('%B %d, %Y')
    
    # Cover page info table
    cover_data = [
        ['Report Focus:', ', '.join(categories)],
        ['Market:', market],
        ['Date:', report_date],
        ['Report Type:', 'Strategic Market Intelligence']
    ]
    
    cover_table = Table(cover_data, colWidths=[2*inch, 3*inch])
    cover_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('TEXTCOLOR', (0, 0), (0, -1), HexColor('#2c3e50')),
        ('TEXTCOLOR', (1, 0), (1, -1), HexColor('#34495e')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    
    story.append(cover_table)
    story.append(PageBreak())
    
    # TABLE OF CONTENTS
    story.append(Paragraph("Table of Contents", section_heading_style))
    story.append(Spacer(1, 0.15*inch))
    
    toc_data = [
        ['Executive Summary', '3'],
        ['Market Overview', '4'],
        ['Category Analysis', '5'],
        ['Strategic Recommendations', '6'],
        ['Risk Assessment', '7'],
        ['Market Opportunities', '8'],
        ['Appendix: Sources', '9']
    ]
    
    toc_table = Table(toc_data, colWidths=[4.5*inch, 1*inch])
    toc_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('TEXTCOLOR', (0, 0), (-1, -1), HexColor('#2c3e50')),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('LINEAFTER', (0, 0), (0, -1), 1, HexColor('#bdc3c7')),
    ]))
    
    story.append(toc_table)
    story.append(PageBreak())
    
    # EXECUTIVE SUMMARY
    story.append(Paragraph("Executive Summary", section_heading_style))
    story.append(Spacer(1, 0.15*inch))
    
    # Get analysis data
    category_analyses = intelligence_data.get('category_analyses', {})
    main_analysis = intelligence_data.get('analysis', {})
    
    if category_analyses:
        first_category = next(iter(category_analyses.keys()))
        analysis = category_analyses[first_category]
        
        # Executive summary content
        exec_summary = analysis.get('executive_summary', {})
        if exec_summary:
            exec_text = f"""
            <b>Strategic Recommendation:</b> {exec_summary.get('key_recommendation', 'Comprehensive market analysis reveals strategic opportunities for procurement optimization.')}<br/><br/>
            <b>Market Context:</b> Our analysis of {first_category} market dynamics indicates significant opportunities for strategic procurement enhancement. Current market conditions present both challenges and opportunities that require immediate attention.<br/><br/>
            <b>Decision Framework:</b> Priority Level: {exec_summary.get('urgency_level', 'Medium')} | Confidence Score: {exec_summary.get('confidence_level', 'Medium')} | Implementation Timeline: {exec_summary.get('decision_window', 'Medium-term')}
            """
            story.append(Paragraph(exec_text, exec_summary_style))
    else:
        analysis = main_analysis
        story.append(Paragraph("This comprehensive market intelligence report provides strategic analysis and actionable recommendations for procurement optimization. Our analysis covers market dynamics, competitive landscape, risk assessment, and strategic opportunities.", exec_summary_style))
    
    story.append(Spacer(1, 0.2*inch))
    
    # Key findings summary
    story.append(Paragraph("Key Findings", subsection_heading_style))
    
    insights = analysis.get('insights', [])
    if insights and len(insights) > 0:
        findings_data = [['Finding', 'Impact', 'Confidence']]
        for i, insight in enumerate(insights[:5]):
            finding = insight.get('headline', f'Market Insight {i+1}')
            impact = insight.get('impact', 'Medium')
            confidence = insight.get('confidence', 'Medium')
            findings_data.append([finding[:50] + '...' if len(finding) > 50 else finding, impact, confidence])
        
        findings_table = Table(findings_data, colWidths=[3*inch, 1*inch, 1*inch])
        findings_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#ffffff')),
            ('TEXTCOLOR', (0, 1), (-1, -1), HexColor('#2c3e50')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#bdc3c7')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(findings_table)
    
    story.append(PageBreak())
    
    # MARKET OVERVIEW
    story.append(Paragraph("Market Overview", section_heading_style))
    story.append(Spacer(1, 0.1*inch))
    
    # Quantitative metrics
    story.append(Paragraph("Market Metrics", subsection_heading_style))
    
    quantitative_metrics = analysis.get('quantitative_metrics', {})
    if quantitative_metrics:
        metrics_data = [['Metric', 'Value', 'Source']]
        
        market_size = quantitative_metrics.get('market_size')
        if market_size:
            metrics_data.append(['Market Size', market_size.get('value', 'N/A'), market_size.get('source', 'Market Research')[:30]])
        
        growth_rate = quantitative_metrics.get('growth_rate')
        if growth_rate:
            metrics_data.append(['Growth Rate', growth_rate.get('value', 'N/A'), growth_rate.get('source', 'Industry Analysis')[:30]])
        
        key_metrics = quantitative_metrics.get('key_metrics', [])
        for metric in key_metrics[:3]:
            if isinstance(metric, dict):
                metrics_data.append([
                    metric.get('metric', 'Key Metric'),
                    metric.get('value', 'N/A'),
                    metric.get('source', 'Market Data')[:30]
                ])
        
        if len(metrics_data) > 1:
            metrics_table = Table(metrics_data, colWidths=[2*inch, 2*inch, 1.5*inch])
            metrics_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#34495e')),
                ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BACKGROUND', (0, 1), (-1, -1), HexColor('#ffffff')),
                ('TEXTCOLOR', (0, 1), (-1, -1), HexColor('#2c3e50')),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, HexColor('#bdc3c7')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ]))
            
            story.append(metrics_table)
            story.append(Spacer(1, 0.15*inch))
    
    # Market trends summary
    story.append(Paragraph("Market Trends", subsection_heading_style))
    
    # Add market trends content if available
    if analysis.get('market_dynamics', {}).get('key_trends'):
        trends = analysis['market_dynamics']['key_trends'][:3]
        for i, trend in enumerate(trends, 1):
            if isinstance(trend, dict):
                trend_text = f"<b>{i}. {trend.get('trend', 'Market Trend')}</b>"
                if trend.get('quantitative_data'):
                    trend_text += f" - {trend.get('quantitative_data')}"
                story.append(Paragraph(trend_text, body_style))
                story.append(Spacer(1, 0.05*inch))
    
    story.append(PageBreak())
    
    # COMPREHENSIVE CATEGORY ANALYSIS
    if category_analyses:
        story.append(Paragraph("Comprehensive Category Analysis", section_heading_style))
        story.append(Spacer(1, 0.1*inch))
        
        for category, category_analysis in category_analyses.items():
            story.append(Paragraph(f"{category} - Complete Analysis", subsection_heading_style))
            
            # Quantitative Metrics for this category
            quantitative_metrics = category_analysis.get('quantitative_metrics', {})
            if quantitative_metrics:
                story.append(Paragraph("Quantitative Data", ParagraphStyle('BoldSubheading', parent=body_style, fontName='Helvetica-Bold', fontSize=12, spaceAfter=8)))
                
                if quantitative_metrics.get('market_size'):
                    size_data = quantitative_metrics['market_size']
                    story.append(Paragraph(f"<b>Market Size:</b> {size_data.get('value', 'N/A')} - {size_data.get('source', 'Market Research')}", body_style))
                
                if quantitative_metrics.get('growth_rate'):
                    growth_data = quantitative_metrics['growth_rate']
                    story.append(Paragraph(f"<b>Growth Rate:</b> {growth_data.get('value', 'N/A')} - {growth_data.get('source', 'Industry Analysis')}", body_style))
                
                key_metrics = quantitative_metrics.get('key_metrics', [])
                for metric in key_metrics:
                    if isinstance(metric, dict):
                        story.append(Paragraph(f"<b>{metric.get('metric', 'Key Metric')}:</b> {metric.get('value', 'N/A')} - {metric.get('source', 'Market Data')}", body_style))
                
                story.append(Spacer(1, 0.1*inch))
            
            # Key Insights
            insights = category_analysis.get('insights', [])
            if insights:
                story.append(Paragraph("Key Market Insights", ParagraphStyle('BoldSubheading', parent=body_style, fontName='Helvetica-Bold', fontSize=12, spaceAfter=8)))
                
                for i, insight in enumerate(insights, 1):
                    if isinstance(insight, dict):
                        insight_text = f"<b>{i}. {insight.get('headline', 'Market Insight')}</b>"
                        if insight.get('explanation'):
                            insight_text += f"<br/>• {insight.get('explanation')}"
                        if insight.get('evidence'):
                            insight_text += f"<br/>• Evidence: {insight.get('evidence')}"
                        if insight.get('confidence'):
                            insight_text += f"<br/>• Confidence: {insight.get('confidence')}"
                        story.append(Paragraph(insight_text, body_style))
                        story.append(Spacer(1, 0.05*inch))
                
                story.append(Spacer(1, 0.1*inch))
            
            # Market dynamics
            market_dynamics = category_analysis.get('market_dynamics', {})
            key_trends = market_dynamics.get('key_trends', [])
            
            if key_trends:
                story.append(Paragraph("Market Dynamics", ParagraphStyle('BoldSubheading', parent=body_style, fontName='Helvetica-Bold', fontSize=12, spaceAfter=8)))
                
                for i, trend in enumerate(key_trends, 1):
                    if isinstance(trend, dict):
                        trend_text = f"<b>{i}. {trend.get('trend', 'Market Trend')}</b>"
                        if trend.get('quantitative_data'):
                            trend_text += f"<br/>• Data: {trend.get('quantitative_data')}"
                        if trend.get('source_evidence'):
                            trend_text += f"<br/>• Evidence: {trend.get('source_evidence')}"
                        story.append(Paragraph(trend_text, body_style))
                        story.append(Spacer(1, 0.05*inch))
                
                story.append(Spacer(1, 0.1*inch))
            
            # Risk assessment
            risk_flags = category_analysis.get('risk_flags', [])
            if risk_flags:
                story.append(Paragraph("Risk Assessment", ParagraphStyle('BoldSubheading', parent=body_style, fontName='Helvetica-Bold', fontSize=12, spaceAfter=8)))
                
                risk_data = [['Risk Factor', 'Likelihood', 'Impact', 'Mitigation']]
                for risk in risk_flags[:4]:
                    if isinstance(risk, dict):
                        risk_data.append([
                            risk.get('risk_type', 'Risk Factor')[:25],
                            risk.get('likelihood', 'Medium'),
                            risk.get('impact', 'Medium'),
                            risk.get('mitigation', 'Monitor')[:25]
                        ])
                
                if len(risk_data) > 1:
                    risk_table = Table(risk_data, colWidths=[1.5*inch, 1*inch, 1*inch, 1.5*inch])
                    risk_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#e74c3c')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#ffffff')),
                        ('TEXTCOLOR', (0, 1), (-1, -1), HexColor('#2c3e50')),
                        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                        ('FONTSIZE', (0, 1), (-1, -1), 9),
                        ('GRID', (0, 0), (-1, -1), 1, HexColor('#bdc3c7')),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('TOPPADDING', (0, 0), (-1, -1), 8),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                        ('LEFTPADDING', (0, 0), (-1, -1), 6),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                    ]))
                    
                    story.append(risk_table)
            
            # Market Opportunities
            market_opportunities = category_analysis.get('market_opportunities', [])
            if market_opportunities:
                story.append(Paragraph("Market Opportunities", ParagraphStyle('BoldSubheading', parent=body_style, fontName='Helvetica-Bold', fontSize=12, spaceAfter=8)))
                
                for i, opp in enumerate(market_opportunities, 1):
                    if isinstance(opp, dict):
                        opp_text = f"<b>{i}. {opp.get('opportunity', 'Market Opportunity')}</b>"
                        if opp.get('quantitative_potential'):
                            opp_text += f"<br/>• Potential: {opp.get('quantitative_potential')}"
                        if opp.get('source_evidence'):
                            opp_text += f"<br/>• Evidence: {opp.get('source_evidence')}"
                        story.append(Paragraph(opp_text, body_style))
                        story.append(Spacer(1, 0.05*inch))
                
                story.append(Spacer(1, 0.1*inch))
            
            # Strategic Recommendations for this category
            strategic_recommendations = category_analysis.get('strategic_recommendations', [])
            if strategic_recommendations:
                story.append(Paragraph("Strategic Recommendations", ParagraphStyle('BoldSubheading', parent=body_style, fontName='Helvetica-Bold', fontSize=12, spaceAfter=8)))
                
                for i, rec in enumerate(strategic_recommendations, 1):
                    if isinstance(rec, dict):
                        rec_text = f"<b>{i}. {rec.get('recommendation', 'Strategic Recommendation')}</b>"
                        if rec.get('rationale'):
                            rec_text += f"<br/>• Rationale: {rec.get('rationale')}"
                        if rec.get('timeline'):
                            rec_text += f"<br/>• Timeline: {rec.get('timeline')}"
                        story.append(Paragraph(rec_text, body_style))
                        story.append(Spacer(1, 0.05*inch))
                
                story.append(Spacer(1, 0.1*inch))
            
            # Executive Summary for this category
            exec_summary = category_analysis.get('executive_summary', {})
            if exec_summary:
                story.append(Paragraph("Executive Assessment", ParagraphStyle('BoldSubheading', parent=body_style, fontName='Helvetica-Bold', fontSize=12, spaceAfter=8)))
                
                if exec_summary.get('key_recommendation'):
                    story.append(Paragraph(f"<b>Key Recommendation:</b> {exec_summary.get('key_recommendation')}", body_style))
                
                summary_items = [
                    ('Urgency Level', exec_summary.get('urgency_level', 'Medium')),
                    ('Confidence Level', exec_summary.get('confidence_level', 'Medium')),
                    ('Decision Window', exec_summary.get('decision_window', 'Medium-term')),
                    ('Market Pressure', exec_summary.get('market_pressure', 'Medium'))
                ]
                
                for label, value in summary_items:
                    story.append(Paragraph(f"<b>{label}:</b> {value}", body_style))
                
                story.append(Spacer(1, 0.1*inch))
            
            story.append(Spacer(1, 0.15*inch))
    
    story.append(PageBreak())
    
    # SEARCH QUERIES AND SOURCES
    story.append(Paragraph("Research Methodology & Sources", section_heading_style))
    story.append(Spacer(1, 0.1*inch))
    
    # Add search queries if available
    search_queries = intelligence_data.get('search_queries', [])
    if search_queries:
        story.append(Paragraph("Search Queries Used", subsection_heading_style))
        story.append(Paragraph("The following intelligent search queries were used to gather market intelligence:", body_style))
        story.append(Spacer(1, 0.05*inch))
        
        for i, query in enumerate(search_queries[:10], 1):
            story.append(Paragraph(f"{i}. {query}", body_style))
            story.append(Spacer(1, 0.03*inch))
        
        story.append(Spacer(1, 0.1*inch))
    
    # Add source URLs if available
    all_sources = set()
    if category_analyses:
        for category_analysis in category_analyses.values():
            insights = category_analysis.get('insights', [])
            for insight in insights:
                if insight.get('source_urls'):
                    all_sources.update(insight['source_urls'])
    
    if all_sources:
        story.append(Paragraph("Key Data Sources", subsection_heading_style))
        story.append(Paragraph("This analysis is based on real-time market intelligence from the following verified sources:", body_style))
        story.append(Spacer(1, 0.05*inch))
        
        for i, source in enumerate(list(all_sources)[:15], 1):
            story.append(Paragraph(f"{i}. {source}", ParagraphStyle('SourceText', parent=body_style, fontSize=9, spaceAfter=3)))
    
    story.append(Spacer(1, 0.1*inch))
    
    # Add methodology note
    story.append(Paragraph("Methodology", subsection_heading_style))
    story.append(Paragraph("This report employs advanced AI-powered market intelligence analysis combining:", body_style))
    story.append(Paragraph("• Real-time web scraping from authoritative industry sources", body_style))
    story.append(Paragraph("• Quantitative data extraction and validation", body_style))
    story.append(Paragraph("• Cross-source intelligence synthesis", body_style))
    story.append(Paragraph("• Strategic risk assessment and opportunity identification", body_style))
    story.append(Paragraph("• Market trend analysis and forecasting", body_style))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("Report generated on " + datetime.now().strftime('%B %d, %Y at %H:%M'), ParagraphStyle('FooterText', parent=body_style, fontSize=9, textColor=HexColor('#7f8c8d'), alignment=TA_CENTER)))
    
    # Build and return the PDF
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
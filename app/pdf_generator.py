"""
PDF Generator - NEW FOR HACKATHON with Llama Image heatmap
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import os

def generate_pdf(scoring_result, verdict, lat, lon):
    os.makedirs("reports", exist_ok=True)
    filename = f"reports/BeeSense_{lat:.3f}_{lon:.3f}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Header
    story.append(Paragraph(f"<b>BeeSense Location Intelligence Report</b>", styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | {lat:.4f}, {lon:.4f}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Verdict - Llama Spark generated
    story.append(Paragraph(f"<b>🟢 BeeSense Verdict:</b>", styles['Heading2']))
    story.append(Paragraph(verdict['verdict_tr'], styles['Normal']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"<b>Decision:</b> {verdict['decision']} | <b>Score:</b> {scoring_result['ecological_score']}/100", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # 6-layer breakdown - NEW: SAM 3.1 + 5 engines
    story.append(Paragraph(f"<b>Ecological Score - 6 Layer Breakdown (NEW: SAM 3.1)</b>", styles['Heading2']))
    data = [
        ["Layer", "Score", "Details"],
        ["🌿 Forage Quality", f"{scoring_result['scores']['forage_quality']}", f"{scoring_result['flora']} - {scoring_result['forage_area_ha']}ha"],
        ["🔢 Diversity", f"{scoring_result['scores']['diversity']}", "Flora diversity index"],
        ["🌸 Bloom Timing", f"{scoring_result['scores']['bloom_timing']}", f"Bloom: {scoring_result['bloom_window']}"],
        ["🐝 Carrying Cap.", f"{scoring_result['scores']['carrying_capacity']}", f"Max {scoring_result['capacity']} hives"],
        ["👥 Competition", f"{scoring_result['scores']['competition']}", f"{scoring_result['competition']} hives in 2km"],
        ["⚠️ Risk Score", f"{scoring_result['scores']['risk']}", scoring_result['risk_details']],
    ]
    t = Table(data, colWidths=[120, 60, 280])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#FFC72C")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTSIZE', (0,0), (-1,-1), 9),
    ]))
    story.append(t)
    story.append(Spacer(1, 20))
    
    # SAM 3.1 confidence
    story.append(Paragraph(f"<b>SAM 3.1 Segmentation Confidence:</b> {scoring_result['sam_mask_confidence']*100:.1f}% | Forage area: {scoring_result['forage_area_ha']}ha", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Alternatives
    story.append(Paragraph(f"<b>5 Best Nearby Alternatives (Hexagon Grid)</b>", styles['Heading2']))
    alt_data = [["#", "Distance", "Score", "Lat/Lon"]]
    for i, alt in enumerate(scoring_result['alternatives'][:5], 1):
        alt_data.append([str(i), f"{alt['distance_km']}km", f"{alt['score']}/100", f"{alt['lat']:.3f}, {alt['lon']:.3f}"])
    t2 = Table(alt_data, colWidths=[30, 70, 70, 290])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E0E0E0")),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTSIZE', (0,0), (-1,-1), 8),
    ]))
    story.append(t2)
    story.append(Spacer(1, 30))
    
    story.append(Paragraph(f"<i>Built during Meta Global AI Developer Hackathon Oct 27-Nov 4 2026 | Models: SAM 3.1, Llama Spark, Llama Wonder, Llama Image, Voice Transcribe | Open-weights: Llama Spark Open via Baseten (meta-models/llama-spark-open-1026)</i>", styles['Italic']))
    
    doc.build(story)
    print(f"PDF generated: {filename}")
    return filename

# -*- coding: utf-8 -*-
"""
Cover Letter Generator — Marcos Gonzalez Fernandez
Role: Business Analyst (m/f/d) - Cyber Advisory / Compliance
Company: EWERK Consulting GmbH, Leipzig
Design: A4, centered serif header, horizontal rule, justified body, black and white
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT

OUTPUT = r"c:\Users\mg929\OneDrive\Documentos\MarkzProjects\cmd-agent-helper\outputs\cover_letter.pdf"

PAGE_W, PAGE_H = A4
L_MARGIN = 25 * mm
R_MARGIN = 25 * mm
T_MARGIN = 28 * mm
CONTENT_W = PAGE_W - L_MARGIN - R_MARGIN
BLACK = colors.black
LINK_BLUE = colors.HexColor("#1155CC")

# ── Candidate details ────────────────────────────────────────────────────────
NAME = "Marcos Gonzalez Fernandez"
LOCATION = "Leipzig, Germany"
PHONE = "+34 603 786 521"
EMAIL = "marcos.gonzalezfdez5@gmail.com"
LINKEDIN = "linkedin.com/in/marcos-gonzalez-fdez5"

# ── Letter details ───────────────────────────────────────────────────────────
COMPANY_NAME = "EWERK Consulting GmbH"
COMPANY_ADDRESS = "Leipzig, Germany"
DATE_STR = "16 April 2026"
ROLE = "Business Analyst (m/f/d) - Cyber Advisory / Compliance"
START_DATE = "as soon as possible"
SALUTATION = "Hiring Team"

# ── Letter body paragraphs ───────────────────────────────────────────────────
body_paragraphs = [
    (
        "My background in Software Engineering, combined with hands-on experience "
        "in structured analytical evaluation, IT process documentation, and enterprise "
        "system governance, makes EWERK Consulting's advisory work in KRITIS-critical "
        "sectors a natural next step. I am applying for the Business Analyst role in "
        "Cyber Advisory and Compliance, eager to contribute a rigorous analytical "
        "foundation to your team's work on IT security strategies and compliance frameworks."
    ),
    (
        "During my time at Carl Zeiss AG, I led the development of a centralised "
        "Power BI governance dashboard consolidating SAP Analytics and Excel data across "
        "global budget lines, improving reporting efficiency by 50%. Critically, I also "
        "supported the compliance and access governance requirements of a live SAP-to-Salesforce "
        "digital transformation migration, building KPI monitoring dashboards to ensure "
        "data governance continuity throughout the transition. These projects gave me "
        "direct experience with IT compliance requirements, structured process documentation, "
        "and the operational discipline that regulated environments demand."
    ),
    (
        "Through my work as an AI Model Evaluation Contractor at Browserbase, I conducted "
        "over 600 structured assessments of AI systems, applying systematic risk "
        "identification frameworks to detect failure patterns and edge cases in "
        "high-reliability contexts. Translating this to EWERK's advisory scope: the "
        "core competency is identical - structured analysis of complex systems, "
        "documentation of risk scenarios, and clear communication of findings to "
        "support informed decision-making. I am now actively building my knowledge "
        "of ISO 27001, IT security frameworks, and KRITIS regulatory requirements "
        "to formalise this transition."
    ),
    (
        "EWERK's positioning at the intersection of digital transformation and "
        "critical infrastructure security is precisely the domain I want to grow into. "
        "The combination of a technically grounded consulting approach with real-world "
        "impact across the energy, finance, and healthcare sectors aligns directly "
        "with both my engineering background and my long-term direction. My fluency "
        "in German (B2, actively developing toward C1) and English ensures I can "
        "communicate effectively with your clients and international partners from day one."
    ),
    (
        "I would welcome the opportunity to discuss how my analytical background and "
        "genuine commitment to IT security and compliance advisory can contribute to "
        "EWERK's team and clients."
    ),
]

# ── Build PDF ─────────────────────────────────────────────────────────────────
c = canvas.Canvas(OUTPUT, pagesize=A4)

y = PAGE_H - T_MARGIN

# ── Header ────────────────────────────────────────────────────────────────────
# Name
c.setFont("Times-Bold", 22)
c.setFillColor(BLACK)
c.drawCentredString(PAGE_W / 2, y, NAME)
y -= 20

# Contact line
contact_line = f"{LOCATION}  \xb7  {PHONE}  \xb7  {EMAIL}"
c.setFont("Times-Roman", 10)
c.drawCentredString(PAGE_W / 2, y, contact_line)
y -= 15

# LinkedIn
c.setFillColor(LINK_BLUE)
c.setFont("Times-Roman", 10)
link_w = c.stringWidth(LINKEDIN, "Times-Roman", 10)
link_x = (PAGE_W - link_w) / 2
c.drawString(link_x, y, LINKEDIN)
c.setLineWidth(0.6)
c.setStrokeColor(LINK_BLUE)
c.line(link_x, y - 1.5, link_x + link_w, y - 1.5)
y -= 10

# Horizontal rule
c.setFillColor(BLACK)
c.setStrokeColor(BLACK)
c.setLineWidth(0.8)
c.line(L_MARGIN, y, PAGE_W - R_MARGIN, y)
y -= 22

# ── Company block + letter body via Frame ─────────────────────────────────────
body_style = ParagraphStyle(
    "body",
    fontName="Times-Roman",
    fontSize=11,
    leading=17,
    spaceBefore=9,
    alignment=TA_JUSTIFY,
)
left_style = ParagraphStyle(
    "left",
    fontName="Times-Roman",
    fontSize=11,
    leading=15,
    spaceBefore=5,
    alignment=TA_LEFT,
)
bold_left = ParagraphStyle(
    "bold_left",
    fontName="Times-Bold",
    fontSize=11,
    leading=15,
    spaceBefore=8,
    alignment=TA_LEFT,
)
small_gap = ParagraphStyle(
    "gap",
    fontName="Times-Roman",
    fontSize=4,
    leading=6,
    spaceBefore=0,
    alignment=TA_LEFT,
)

story = []
story.append(Paragraph(COMPANY_NAME, left_style))
story.append(Paragraph(COMPANY_ADDRESS, left_style))
story.append(Paragraph(DATE_STR, left_style))
story.append(Paragraph(" ", small_gap))
story.append(Paragraph(f"<b>Application for {ROLE} - Start Date: {START_DATE}</b>", bold_left))
story.append(Paragraph(" ", small_gap))
story.append(Paragraph(f"Dear {SALUTATION},", left_style))
story.append(Paragraph(" ", small_gap))

for para in body_paragraphs:
    story.append(Paragraph(para, body_style))

story.append(Paragraph(" ", small_gap))
story.append(Paragraph("Warm regards,", left_style))
story.append(Paragraph(NAME + ".", left_style))

# Calculate available height for body
body_h = y - 20 * mm
frame = Frame(
    L_MARGIN, 20 * mm,
    CONTENT_W, body_h,
    leftPadding=0, rightPadding=0,
    topPadding=0, bottomPadding=0,
)
frame.addFromList(story, c)

c.save()
print(f"Cover letter saved: {OUTPUT}")

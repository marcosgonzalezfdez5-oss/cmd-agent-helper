from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT

OUT = r"C:\Users\Marcos\Documents\Projects\cmd-agent-helper\outputs\cover_letter.pdf"

PAGE_W, PAGE_H = A4
L_MARGIN  = 25 * mm
R_MARGIN  = 25 * mm
T_MARGIN  = 28 * mm
CONT_W    = PAGE_W - L_MARGIN - R_MARGIN
BLACK     = colors.black
LINK_BLUE = colors.HexColor("#1155CC")

# ── Letter content ──────────────────────────────────────────────────────────
NAME     = "Marcos Gonzalez Fernandez"
LOCATION = "Leipzig, Germany"
PHONE    = "+34 603786521"
EMAIL    = "marcos.gonzalezfdez5@gmail.com"
LINKEDIN = "linkedin.com/in/marcos-gonzalez-fdez5/"

COMPANY  = "Siemens Global Business Services"
ADDRESS  = "Western Europe & Africa Hub, Germany"
DATE_STR = "22 April 2026"
ROLE     = "Junior Digitalization Consultant"
START    = "By mutual agreement"
SALUT    = "Hiring Team"

BODY = [
    (
        "During my time at Carl Zeiss, I saw firsthand what it takes to turn a business process "
        "problem into a deployed digital solution — from gathering stakeholder requirements during "
        "a SAP-to-Salesforce migration, to building the Power BI KPI dashboard that made the "
        "transformation measurable. That experience of bridging the gap between business needs and "
        "technical delivery is precisely what drew me to Siemens GBS's Junior Digitalization "
        "Consultant role in Digital Advisory."
    ),
    (
        "My profile covers both sides of what this role demands. On the analysis side, I have "
        "documented business requirements, identified process inefficiencies, and translated them "
        "into data-driven solutions — most recently cutting reporting cycle time by 50% at Carl "
        "Zeiss by migrating manual SAP Analytics workflows to an automated Power BI dashboard. "
        "On the AI side, I have deployed an AI agent solution that reduced operational overhead "
        "by 40% across 20 manufacturing facilities, and completed over 600 structured evaluations "
        "of GenAI systems through Browserbase — giving me a grounded, practical understanding of "
        "where AI-driven automation creates genuine business value and where it fails."
    ),
    (
        "Siemens GBS's Digital Solutions portfolio — spanning GenAI, Agentic AI, Advanced "
        "Analytics, and RPA — maps directly to the skills I am actively building. Your WEA Hub's "
        "diversity (50+ nationalities across 14 countries) and my own multilingual, five-country "
        "background make this an environment where I know I will contribute and grow quickly. "
        "I am ready to support AI workshops, assist in business case development, and help "
        "deliver digitalization initiatives from day one."
    ),
    (
        "I would welcome the opportunity to discuss how my analytical background and applied AI "
        "experience can contribute to Siemens GBS's digitalization mission."
    ),
]

# ── Build PDF ────────────────────────────────────────────────────────────────
c = canvas.Canvas(OUT, pagesize=A4)
y = PAGE_H - T_MARGIN

# Name
c.setFont("Times-Bold", 22)
c.setFillColor(BLACK)
c.drawCentredString(PAGE_W / 2, y, NAME)
y -= 20

# Contact line
contact = f"{LOCATION}  ·  {PHONE}  ·  {EMAIL}"
c.setFont("Times-Roman", 10)
c.drawCentredString(PAGE_W / 2, y, contact)
y -= 14

# LinkedIn
c.setFillColor(LINK_BLUE)
c.setFont("Times-Roman", 10)
lw = c.stringWidth(LINKEDIN, "Times-Roman", 10)
lx = (PAGE_W - lw) / 2
c.drawString(lx, y, LINKEDIN)
c.line(lx, y - 1, lx + lw, y - 1)
y -= 10

# Horizontal rule
c.setFillColor(BLACK)
c.setStrokeColor(BLACK)
c.setLineWidth(0.8)
c.line(L_MARGIN, y, PAGE_W - R_MARGIN, y)
y -= 22

# Company block
body_top = y

story = []
base = ParagraphStyle(
    "base",
    fontName="Times-Roman",
    fontSize=11,
    leading=16,
    spaceBefore=0,
    spaceAfter=6,
    alignment=TA_LEFT,
)
just = ParagraphStyle("just", parent=base, alignment=TA_JUSTIFY, spaceBefore=10)
bold_left = ParagraphStyle("bl", parent=base, fontName="Times-Bold")

story.append(Paragraph(COMPANY, base))
story.append(Paragraph(ADDRESS, base))
story.append(Paragraph(DATE_STR, base))
story.append(Paragraph("&nbsp;", base))
story.append(Paragraph(f"<b>Application for {ROLE} — Start date: {START}</b>", base))
story.append(Paragraph("&nbsp;", base))
story.append(Paragraph(f"Dear {SALUT},", base))
story.append(Paragraph("&nbsp;", base))

for para in BODY:
    story.append(Paragraph(para, just))

story.append(Paragraph("&nbsp;", base))
story.append(Paragraph("Warm regards,", base))
story.append(Paragraph(f"<b>{NAME}</b>", base))

body_h = body_top - 20 * mm
frame = Frame(
    L_MARGIN, 20 * mm,
    CONT_W, body_h,
    leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
)
frame.addFromList(story, c)

c.save()
print(f"Cover letter saved to {OUT}")

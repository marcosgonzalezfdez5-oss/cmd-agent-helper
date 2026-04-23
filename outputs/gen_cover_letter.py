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

COMPANY  = "BCG Platinion"
ADDRESS  = "Cologne, Germany"
DATE_STR = "23 April 2026"
ROLE     = "AI and Agentic Systems Engineer"
START    = "By agreement"
SALUT    = "Leonie Kutschera Gross and Team"

BODY = [
    (
        "My path to this application runs through a practical question: when you deploy an autonomous "
        "AI agent to coordinate operations across 20 manufacturing plants, how do you govern it at scale? "
        "At Stumpp Schuele, I designed and deployed the LLM-based agentic AI solution that raised "
        "operational efficiency by 40% across those facilities. Getting it right meant translating plant "
        "managers' requirements into precise, testable agent specifications and defining the rule sets "
        "that governed agent behavior from day one. Turning business intent into governed AI execution "
        "is exactly what BCG Platinion builds into enterprise architectures, and it "
        "is where I want to build expertise."
    ),
    (
        "In parallel, I spent over two months at Browserbase conducting 600+ structured evaluations "
        "of frontier LLM and agentic AI systems. The work goes beyond running benchmarks: it is "
        "systematic observability analysis of where agent loops break, how tool use degrades under "
        "edge cases, and where evaluation frameworks need to flag behavior that looks compliant but "
        "is not. That grounded understanding of AI coding agent failure modes and governance "
        "requirements maps directly to the evaluation and SDLC-wide coding agent frameworks BCG "
        "Platinion builds for enterprise clients."
    ),
    (
        "What draws me to BCG Platinion specifically is the enterprise scale and the consulting "
        "dimension. At Carl Zeiss, I learned that the hardest part of a digital transformation is "
        "not the technology itself; it is communicating what the system does, and why it can be "
        "trusted, to stakeholders across business and technical teams. BCG Platinion operates at "
        "that intersection on every engagement. My multilingual background in Spanish, English (C1), "
        "and German (B2), combined with experience across five countries, means I am comfortable "
        "working in that kind of global, interdisciplinary environment. The direction toward "
        "autonomous delivery architectures such as the Dark Software Factory is one I find "
        "genuinely compelling."
    ),
    (
        "I would welcome the opportunity to discuss how my experience in agentic AI deployment "
        "and LLM evaluation can contribute to BCG Platinion's work."
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
    leading=14,
    spaceBefore=0,
    spaceAfter=3,
    alignment=TA_LEFT,
)
just = ParagraphStyle("just", parent=base, alignment=TA_JUSTIFY, spaceBefore=6)
bold_left = ParagraphStyle("bl", parent=base, fontName="Times-Bold")

story.append(Paragraph("&nbsp;", base))
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
story.append(Paragraph("Marcos Gonzalez Fernandez", base))

body_h = body_top - 10 * mm
frame = Frame(
    L_MARGIN, 20 * mm,
    CONT_W, body_h,
    leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
)
frame.addFromList(story, c)

c.save()
print(f"Cover letter saved to {OUT}")

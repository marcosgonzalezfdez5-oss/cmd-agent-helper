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

COMPANY  = "Vetaion GmbH"
ADDRESS  = "Garching, Munich"
DATE_STR = "28 April 2026"
ROLE     = "AI Automation Engineer"
START    = "As soon as possible"
SALUT    = "Vetaion Team"

BODY = [
    (
        "At Stumpp Schuele & Somappa Springs, I built and shipped an AI automation platform for "
        "20 manufacturing plants. Not a prototype — a live system running across production "
        "facilities in India, built in Python and SQL, with data architecture I designed and a "
        "backend I wrote end to end. When I read what Vetaion is building, that project is the "
        "closest thing I have done to it."
    ),
    (
        "At Browserbase, I evaluated over 600 AI systems under production conditions. That work "
        "gave me a clear understanding of where AI holds up and where it does not — which matters "
        "when you are building automation that real manufacturing lines depend on. Combined with "
        "the Stumpp Schuele deployment, I can point to shipped systems in both AI evaluation and "
        "AI automation. I write Python, SQL, and JavaScript. I have owned data architecture, "
        "automated pipelines, and multi-site IT integration from specification to go-live."
    ),
    (
        "I want this role because of the scope. Building the AI layer of a manufacturing OS from "
        "0 to 1, at a company rethinking how control cabinets get made, is the kind of technically "
        "hard problem I am looking for. The electrical design and EPLAN side is new to me, but "
        "picking up an unfamiliar technical domain quickly is something I have done in every role "
        "so far. My BSc in Software Engineering (First Class Honours, Lancaster University), "
        "combined with hands-on experience across five countries, means I contribute from day one."
    ),
    (
        "I would welcome the chance to discuss this at your Garching office."
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

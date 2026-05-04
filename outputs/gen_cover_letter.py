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

COMPANY  = "[COMPANY NAME]"
ADDRESS  = "[LOCATION]"
DATE_STR = "4th of May, 2026"
ROLE     = "Junior Automation Consultant"
START    = "As soon as possible"
SALUT    = "Hiring Team"


BODY = [
    (
        "Before applying to this role, I built an AI automation bot to automate my own job application process - "
        "researching job descriptions, generating tailored documents, and delivering output end to end. That is not "
        "a side experiment. It runs in production and produces results. That is also how I approach every process: "
        "find the manual work, understand it, and build the automated replacement."
    ),
    (
        "At Stumpp Schuele, I designed and deployed an AI automation platform across 20 manufacturing sites. "
        "Requirements, architecture, development, testing, go-live - owned without hand-offs, resulting in a 40% "
        "operational efficiency improvement. At Meerkats AI, I built agentic workflows from scratch in a startup, "
        "mapping manual operations and replacing them with automated processes running against real business data."
    ),
    (
        "What draws me to this role specifically is the development path: joining an Innovation & Technology team, "
        "working on real projects from day one, and growing into the Automation Consultant role step by step. "
        "Analytical and structured by default, I learn fast and build independently. I am looking for an environment "
        "where the work is real and the growth is genuine."
    ),
    (
        "I would welcome the chance to discuss the role in more detail."
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
story.append(Paragraph(f"<b>Application for {ROLE} - Start date: {START}</b>", base))
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

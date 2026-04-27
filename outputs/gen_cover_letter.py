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

COMPANY  = "McKinsey & Company"
ADDRESS  = "Germany"
DATE_STR = "27 April 2026"
ROLE     = "Junior Fellow – Tech & AI"
START    = "06 July 2026"
SALUT    = "McKinsey Recruiting Team"

BODY = [
    (
        "When I deployed an AI-driven system across 20 manufacturing plants, the hardest part was "
        "not the technology itself. It was turning vague requirements into a system that operations "
        "teams across Germany and India would actually trust and use — gathering their input, "
        "explaining the architecture, and making sure the solution fit how they worked rather "
        "than how I assumed they worked. That process is what I found most interesting, and it "
        "is close to what McKinsey's Junior Fellow Tech & AI role describes."
    ),
    (
        "My technical work spans two directions. At Carl Zeiss AG, I built data analysis dashboards "
        "and automated reporting pipelines that cut global budget tracking time by 50%; I also led "
        "a cross-functional team of five interns and managed delivery to project leadership. At "
        "Browserbase, I conducted 600+ structured research evaluations of AI systems, ran systematic "
        "data analysis on model behavior, and produced findings that the development team used "
        "directly. Neither role was purely technical — both required communicating clearly with "
        "non-technical stakeholders and organizing work independently under time pressure."
    ),
    (
        "McKinsey is where I want to take this further. The chance to work on AI-driven technology "
        "projects for Fortune 500 and DAX companies — and to learn consulting from people who do "
        "it at that level — is not something I can replicate elsewhere. My First Class Honours "
        "degree in Software Engineering, combined with fluency in German (B2) and English (C1) "
        "and working experience across five countries, means I can contribute in an international "
        "team from day one."
    ),
    (
        "I would welcome the chance to discuss how my background fits the Junior Fellow Tech & AI "
        "role."
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

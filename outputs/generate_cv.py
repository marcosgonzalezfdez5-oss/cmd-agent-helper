"""
CV Generator — Marcos Gonzalez Fernandez
ATS-optimized for: Business Analyst – Cyber Advisory / Compliance @ EWERK Consulting GmbH
Design: two-column A4, teal #4A7FA5 accents, Helvetica, sidebar contact block
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import Paragraph
import textwrap

OUTPUT = r"c:\Users\mg929\OneDrive\Documentos\MarkzProjects\cmd-agent-helper\outputs\cv_output.pdf"

# ── Colors ──────────────────────────────────────────────────────────────────
TEAL = colors.HexColor("#4A7FA5")
DARK = colors.HexColor("#1A1A2E")
GRAY = colors.HexColor("#666666")
WHITE = colors.white
SIDEBAR_BG = colors.HexColor("#F0F4F8")

# ── Layout ───────────────────────────────────────────────────────────────────
PAGE_W, PAGE_H = A4          # 595.27 x 841.89 pts
MARGIN = 14 * mm
SIDEBAR_W = PAGE_W * 0.30
SIDEBAR_X = MARGIN
MAIN_X = MARGIN + SIDEBAR_W + 6 * mm
MAIN_W = PAGE_W - MAIN_X - MARGIN
TOP_Y = PAGE_H - MARGIN

def draw_section_header(c, x, y, width, text):
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(TEAL)
    text_w = c.stringWidth(text, "Helvetica-Bold", 8)
    gap = 3 * mm
    line_w = (width - text_w - 2 * gap) / 2
    mid_y = y - 3
    c.setStrokeColor(TEAL)
    c.setLineWidth(0.6)
    c.setDash(2, 3)
    c.line(x, mid_y, x + line_w, mid_y)
    c.line(x + line_w + gap + text_w + gap, mid_y, x + width, mid_y)
    c.setDash()
    c.drawString(x + line_w + gap, y - 6, text.upper())
    return y - 16

def wrap_text_lines(text, font, size, max_width, c):
    """Return list of wrapped lines."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        if c.stringWidth(test, font, size) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

def draw_bullet(c, x, y, text, max_width, size=8.2):
    """Draw a bullet line with word-wrap. Returns updated y."""
    DOT_R = 1.2
    INDENT = 5 * mm
    c.setFillColor(TEAL)
    c.circle(x + 2 * mm, y - 2.8, DOT_R, fill=1, stroke=0)
    c.setFillColor(DARK)
    c.setFont("Helvetica", size)
    lines = wrap_text_lines(text, "Helvetica", size, max_width - INDENT, c)
    for i, line in enumerate(lines):
        c.drawString(x + INDENT, y - 6, line)
        if i < len(lines) - 1:
            y -= 11
    return y - 13

def draw_sidebar_text(c, x, y, text, font="Helvetica", size=8, color=DARK, max_width=None):
    if max_width:
        lines = wrap_text_lines(text, font, size, max_width, c)
        for line in lines:
            c.setFont(font, size)
            c.setFillColor(color)
            c.drawString(x, y, line)
            y -= 11
        return y
    else:
        c.setFont(font, size)
        c.setFillColor(color)
        c.drawString(x, y, text)
        return y - 11

# ── Data ─────────────────────────────────────────────────────────────────────
personal = {
    "name": "Marcos Gonzalez Fernandez",
    "headline": "IT Business Analyst | Software Engineering | Data Analytics & Process Documentation",
    "phone": "+34 603 786 521",
    "email": "marcos.gonzalezfdez5@gmail.com",
    "location": "Leipzig, Germany",
    "linkedin": "linkedin.com/in/marcos-gonzalez-fdez5",
}

summary = (
    "Software Engineering graduate with hands-on experience in structured data analysis, "
    "IT process documentation, and enterprise system governance across international environments. "
    "Strong analytical and detail-oriented mindset, with exposure to IT governance through "
    "compliance-critical system migrations and structured quality evaluation frameworks. "
    "Motivated to apply technical foundations in IT security consulting and compliance advisory."
)

experience = [
    {
        "company": "Browserbase",
        "title": "AI Model Evaluation Contractor",
        "location": "Remote",
        "dates": "Feb 2025 – Present",
        "bullets": [
            "Conducted 600+ structured evaluations of AI systems, applying systematic risk identification frameworks to assess model reliability and failure patterns across diverse use cases",
            "Documented edge cases and failure modes using structured reporting methodologies, producing actionable quality improvement insights aligned to governance requirements",
            "Applied rigorous, independent analytical assessment in high-reliability environments requiring consistent structured documentation",
        ],
    },
    {
        "company": "Carl Zeiss AG",
        "title": "Working Student — IT Reporting & Data Governance",
        "location": "Oberkochen, Germany",
        "dates": "Nov 2024 – Aug 2025",
        "bullets": [
            "Developed a centralized Power BI governance dashboard consolidating SAP Analytics and Excel data for global budget tracking, improving reporting efficiency by 50%",
            "Coordinated a 5-person intern team, managing task prioritization, workload distribution, and delivery of compliance-critical reporting outputs",
            "Supported data-driven decision-making through automated pipelines, contributing to IT process standardization and digital transformation objectives",
        ],
    },
    {
        "company": "Carl Zeiss AG",
        "title": "Intern — IT Compliance & System Migration",
        "location": "Oberkochen, Germany",
        "dates": "Jun 2024 – Aug 2024",
        "bullets": [
            "Built a KPI compliance monitoring dashboard to track data governance metrics during SAP-to-Salesforce digital transformation migration",
            "Managed Salesforce project access controls and delivered structured data reporting aligned to migration compliance and IT governance requirements",
        ],
    },
    {
        "company": "Carl Zeiss BV",
        "title": "Intern — Infrastructure Documentation",
        "location": "Breda, Netherlands",
        "dates": "Jul 2023 – Aug 2023",
        "bullets": [
            "Created technical and process documentation for platform infrastructure, supporting knowledge management and IT process transparency",
            "Supported inventory management and operational process documentation",
        ],
    },
    {
        "company": "Carl Zeiss Mexico",
        "title": "Intern",
        "location": "Mexico City, Mexico",
        "dates": "Aug 2022 – Sep 2022",
        "bullets": [
            "Developed a marketing campaign for a medical product, increasing social media visibility by 5%",
        ],
    },
]

education = [
    {
        "degree": "BSc Software Engineering",
        "institution": "Lancaster University",
        "location": "Leipzig, Germany",
        "dates": "Oct 2021 – Jul 2025",
        "grade": "First Class Honours (18.0)",
    }
]

skills_tools = ["Power BI", "Microsoft Excel", "Salesforce", "Tableau", "SAP (basic)"]
skills_prog = ["Python", "SQL", "Java", "JavaScript", "TypeScript"]

languages = [
    ("Spanish", "Native"),
    ("English", "C1"),
    ("German", "B2"),
    ("French", "B1"),
]

# ── Build PDF ─────────────────────────────────────────────────────────────────
c = canvas.Canvas(OUTPUT, pagesize=A4)

# Sidebar background
c.setFillColor(SIDEBAR_BG)
c.rect(0, 0, MARGIN + SIDEBAR_W, PAGE_H, fill=1, stroke=0)

# ── MAIN COLUMN — Header ──────────────────────────────────────────────────────
header_x = MAIN_X
y = TOP_Y

# Name
c.setFont("Helvetica-Bold", 22)
c.setFillColor(TEAL)
c.drawString(header_x, y, personal["name"].upper())
y -= 16

# Headline
headline_lines = wrap_text_lines(personal["headline"], "Helvetica-Oblique", 9.5, MAIN_W, c)
c.setFont("Helvetica-Oblique", 9.5)
c.setFillColor(TEAL)
for line in headline_lines:
    c.drawString(header_x, y, line)
    y -= 12
y -= 4

# Horizontal rule
c.setStrokeColor(TEAL)
c.setLineWidth(0.8)
c.line(header_x, y, PAGE_W - MARGIN, y)
y -= 14

# ── Summary ───────────────────────────────────────────────────────────────────
y = draw_section_header(c, header_x, y, MAIN_W, "Professional Summary")
c.setFont("Helvetica", 8.5)
c.setFillColor(DARK)
sum_lines = wrap_text_lines(summary, "Helvetica", 8.5, MAIN_W, c)
for line in sum_lines:
    c.drawString(header_x, y, line)
    y -= 11
y -= 6

# ── Experience ────────────────────────────────────────────────────────────────
y = draw_section_header(c, header_x, y, MAIN_W, "Professional Experience")

for exp in experience:
    if y < 80:
        c.showPage()
        c.setFillColor(SIDEBAR_BG)
        c.rect(0, 0, MARGIN + SIDEBAR_W, PAGE_H, fill=1, stroke=0)
        y = TOP_Y

    # Company name + location/dates on same line
    c.setFont("Helvetica-Bold", 9.5)
    c.setFillColor(DARK)
    c.drawString(header_x, y, exp["company"])

    loc_date = f'{exp["location"]}  |  {exp["dates"]}'
    c.setFont("Helvetica", 8)
    c.setFillColor(GRAY)
    ld_w = c.stringWidth(loc_date, "Helvetica", 8)
    c.drawString(header_x + MAIN_W - ld_w, y, loc_date)
    y -= 12

    # Role title
    c.setFont("Helvetica-Oblique", 9)
    c.setFillColor(TEAL)
    c.drawString(header_x, y, exp["title"])
    y -= 12

    # Bullets
    for bullet in exp["bullets"]:
        y = draw_bullet(c, header_x, y, bullet, MAIN_W)

    y -= 5

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
side_x = SIDEBAR_X
side_w = SIDEBAR_W - 4 * mm
sy = TOP_Y

# Contact block
sy = draw_section_header(c, side_x, sy, side_w, "Contact")
sy = draw_sidebar_text(c, side_x, sy, personal["phone"], size=8.2, max_width=side_w)
sy = draw_sidebar_text(c, side_x, sy, personal["email"], size=7.8, max_width=side_w)
sy = draw_sidebar_text(c, side_x, sy, personal["location"], size=8.2, max_width=side_w)
sy = draw_sidebar_text(c, side_x, sy, personal["linkedin"], size=7.5, color=colors.HexColor("#1155CC"), max_width=side_w)
sy -= 6

# Education
sy = draw_section_header(c, side_x, sy, side_w, "Education")
for edu in education:
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(DARK)
    c.drawString(side_x, sy, edu["degree"])
    sy -= 11
    sy = draw_sidebar_text(c, side_x, sy, edu["institution"], size=8, max_width=side_w)
    sy = draw_sidebar_text(c, side_x, sy, edu["location"], size=7.8, color=GRAY, max_width=side_w)
    sy = draw_sidebar_text(c, side_x, sy, edu["dates"], size=7.8, color=GRAY, max_width=side_w)
    c.setFont("Helvetica-Oblique", 7.8)
    c.setFillColor(TEAL)
    c.drawString(side_x, sy, edu["grade"])
    sy -= 12
sy -= 4

# Technical Skills
sy = draw_section_header(c, side_x, sy, side_w, "Technical Skills")
c.setFont("Helvetica-Bold", 7.8)
c.setFillColor(TEAL)
c.drawString(side_x, sy, "Tools & Platforms")
sy -= 10
for s in skills_tools:
    sy = draw_sidebar_text(c, side_x + 2*mm, sy, f"• {s}", size=8, max_width=side_w - 2*mm)
sy -= 4
c.setFont("Helvetica-Bold", 7.8)
c.setFillColor(TEAL)
c.drawString(side_x, sy, "Programming")
sy -= 10
for s in skills_prog:
    sy = draw_sidebar_text(c, side_x + 2*mm, sy, f"• {s}", size=8, max_width=side_w - 2*mm)
sy -= 6

# Languages
sy = draw_section_header(c, side_x, sy, side_w, "Languages")
for lang, level in languages:
    # Language name bold + level gray inline
    c.setFont("Helvetica-Bold", 8.2)
    c.setFillColor(DARK)
    c.drawString(side_x, sy, lang)
    lw = c.stringWidth(lang, "Helvetica-Bold", 8.2)
    c.setFont("Helvetica", 8.2)
    c.setFillColor(GRAY)
    c.drawString(side_x + lw + 4, sy, f"— {level}")
    sy -= 11
sy -= 4

# Additional
sy = draw_section_header(c, side_x, sy, side_w, "Additional")
sy = draw_sidebar_text(c, side_x, sy, "Personal Investment Portfolio", font="Helvetica-Bold", size=7.8, max_width=side_w)
sy = draw_sidebar_text(c, side_x, sy, "20%+ cumulative return,", size=7.8, max_width=side_w)
sy = draw_sidebar_text(c, side_x, sy, "self-managed (2025–)", size=7.8, max_width=side_w)

c.save()
print(f"CV saved: {OUTPUT}")

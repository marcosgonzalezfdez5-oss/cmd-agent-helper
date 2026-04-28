"""
gen_cv.py  —  Marcos Gonzalez Fernandez CV
Matches design-reference.pdf layout:
  - Teal diagonal banner top-left with name
  - Circular profile photo top-center
  - Contact block top-right
  - Full-width single-column body
  - Teal dashed section headers
  - Bold company + italic teal role + gray right-aligned loc/dates
  - Bullet points with teal dots

Usage:
  python gen_cv.py
  python gen_cv.py --photo path/to/photo.jpg
  python gen_cv.py --photo photo.jpg --out my_cv.pdf

Requires: pip install reportlab Pillow --break-system-packages
"""

import sys
import os
import io
import re
import argparse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

# ── Output ────────────────────────────────────────────────────────────────────
OUT      = "cv_Marcos_Gonzalez_Fernandez.pdf"
PHOTO    = r"C:\Users\Marcos\Documents\Projects\cmd-agent-helper\cv-creating\assets\profile-pic.jpg"

# ── Design tokens ─────────────────────────────────────────────────────────────
TEAL       = colors.HexColor("#4A7FA5")
TEAL_LIGHT = colors.HexColor("#EDF3F8")
DARK       = colors.HexColor("#1A1A2E")
GRAY       = colors.HexColor("#888888")
WHITE      = colors.white

PAGE_W, PAGE_H = A4          # 595.28 x 841.89 pts
MARGIN    = 14 * mm
BODY_X    = MARGIN
BODY_W    = PAGE_W - 2 * MARGIN
HEADER_H  = 40 * mm          # height of the top banner area


# ── Helpers ───────────────────────────────────────────────────────────────────

def wrap(c, text, font, size, max_w):
    """Word-wrap text into lines fitting max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if c.stringWidth(test, font, size) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def section_header(c, x, y, width, text):
    """Draw  ---- TITLE ----  in teal. Returns updated y."""
    label = text.upper()
    c.setFont("Helvetica-Bold", 8)
    tw = c.stringWidth(label, "Helvetica-Bold", 8)
    gap = 3 * mm
    lw  = (width - tw - 2 * gap) / 2
    mid = y - 3
    c.setStrokeColor(TEAL)
    c.setLineWidth(0.6)
    c.setDash(2, 3)
    c.line(x, mid, x + lw, mid)
    c.line(x + lw + gap + tw + gap, mid, x + width, mid)
    c.setDash()
    c.setFillColor(TEAL)
    c.drawString(x + lw + gap, y - 6, label)
    return y - 16


def _parse_segments(text):
    """Split '**word**' markup into [(text, is_bold)] segments."""
    parts = re.split(r'\*\*(.+?)\*\*', text)
    return [(p, i % 2 == 1) for i, p in enumerate(parts) if p]


def bullet(c, x, y, text, max_w):
    """Draw a teal-dot bullet with wrapped text and **bold** keyword support."""
    INDENT = 5 * mm
    SIZE   = 8.5
    NORM   = "Helvetica"
    BOLD_F = "Helvetica-Bold"
    SP_W   = c.stringWidth(" ", NORM, SIZE)

    # Flatten into (word, is_bold) list
    words = []
    for seg, is_bold in _parse_segments(text):
        for w in seg.split():
            words.append((w, is_bold))

    # Word-wrap into lines
    lines, cur_line, cur_w = [], [], 0.0
    for word, is_bold in words:
        ww   = c.stringWidth(word, BOLD_F if is_bold else NORM, SIZE)
        need = (SP_W if cur_line else 0) + ww
        if cur_w + need <= max_w - INDENT or not cur_line:
            cur_line.append((word, is_bold))
            cur_w += need
        else:
            lines.append(cur_line)
            cur_line, cur_w = [(word, is_bold)], ww
    if cur_line:
        lines.append(cur_line)

    # Bullet dot
    c.setFillColor(TEAL)
    c.circle(x + 2 * mm, y - 2.5, 1.2, fill=1, stroke=0)

    # Draw word by word
    for line_words in lines:
        cx = x + INDENT
        for i, (word, is_bold) in enumerate(line_words):
            if i:
                cx += SP_W
            font = BOLD_F if is_bold else NORM
            c.setFont(font, SIZE)
            c.setFillColor(TEAL if is_bold else DARK)
            c.drawString(cx, y - 6, word)
            cx += c.stringWidth(word, font, SIZE)
        y -= 11

    return y - 2


def draw_circle_image(c, img_path, cx, cy, radius):
    """
    Draw an image clipped to a circle centred at (cx, cy) with given radius.
    Requires Pillow.
    """
    try:
        from PIL import Image, ImageDraw as PILDraw
        img = Image.open(img_path).convert("RGBA")

        # Crop to square from centre
        w, h  = img.size
        side  = min(w, h)
        left  = (w - side) // 2
        top   = (h - side) // 2
        img   = img.crop((left, top, left + side, top + side))

        # Create circular mask
        mask  = Image.new("L", (side, side), 0)
        draw  = PILDraw.Draw(mask)
        draw.ellipse((0, 0, side - 1, side - 1), fill=255)
        img.putalpha(mask)

        # Save to bytes as PNG (preserves transparency)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        # Draw on canvas — wrap in ImageReader so ReportLab accepts BytesIO
        from reportlab.lib.utils import ImageReader
        d = radius * 2
        c.drawImage(ImageReader(buf), cx - radius, cy - radius, width=d, height=d, mask="auto")

        # Teal circle border
        c.setStrokeColor(TEAL)
        c.setLineWidth(2)
        c.circle(cx, cy, radius, fill=0, stroke=1)

    except Exception as e:
        print(f"  [photo] Could not load image: {e}", file=sys.stderr)
        # Placeholder
        c.setFillColor(TEAL_LIGHT)
        c.setStrokeColor(TEAL)
        c.setLineWidth(2)
        c.circle(cx, cy, radius, fill=1, stroke=1)
        c.setFillColor(GRAY)
        c.setFont("Helvetica", 7)
        c.drawCentredString(cx, cy - 3, "Add photo")


def draw_header(c, photo_path=None):
    """
    Draw the top banner matching design-reference.pdf:
      - Teal trapezoid left covering ~60% of width
      - White name + title on the teal area
      - Circular photo placed at top-centre / right of teal shape
      - Contact block to the right of the photo
    """
    banner_bottom = PAGE_H - HEADER_H

    # ── Teal diagonal shape ───────────────────────────────────────────────────
    path = c.beginPath()
    path.moveTo(0, PAGE_H)
    path.lineTo(PAGE_W * 0.60, PAGE_H)
    path.lineTo(PAGE_W * 0.44, banner_bottom)
    path.lineTo(0, banner_bottom)
    path.close()
    c.setFillColor(TEAL)
    c.drawPath(path, fill=1, stroke=0)

    # ── Name ──────────────────────────────────────────────────────────────────
    name_x = MARGIN
    name_y = PAGE_H - 10 * mm

    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 19)
    c.drawString(name_x, name_y,      "MARCOS GONZALEZ")
    c.drawString(name_x, name_y - 21, "FERNANDEZ")

    c.setFont("Helvetica-Oblique", 8.5)
    c.setFillColor(colors.HexColor("#D0E8F5"))
    c.drawString(name_x, name_y - 36, "Data Analysis  |  AI & Technology  |  Software Engineering")

    # ── Profile photo ─────────────────────────────────────────────────────────
    photo_r  = 17 * mm
    photo_cx = PAGE_W * 0.60 + 3 * mm
    photo_cy = PAGE_H - HEADER_H / 2

    draw_circle_image(c, photo_path, photo_cx, photo_cy, photo_r) if (
        photo_path and os.path.exists(photo_path)
    ) else (lambda: [
        c.setFillColor(TEAL_LIGHT),
        c.setStrokeColor(TEAL),
        c.setLineWidth(1.5),
        c.circle(photo_cx, photo_cy, photo_r, fill=1, stroke=1),
        c.setFillColor(GRAY),
        c.setFont("Helvetica", 7),
        c.drawCentredString(photo_cx, photo_cy - 3, "Add photo"),
    ])()

    # ── Contact block ─────────────────────────────────────────────────────────
    contact_x = photo_cx + photo_r + 5 * mm
    contact_y = PAGE_H - 9 * mm

    contacts = [
        ("Tel:",   "+34 603786521"),
        ("Email:", "marcos.gonzalezfdez5@gmail.com"),
        ("Addr:",  "Leipzig, Germany"),
        ("Web:",   "linkedin.com/in/marcos-gonzalez-fdez5"),
    ]

    for label, text in contacts:
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(TEAL)
        c.drawString(contact_x, contact_y, label)
        lw = c.stringWidth(label, "Helvetica-Bold", 7.5)
        c.setFont("Helvetica", 7.5)
        c.setFillColor(DARK)
        c.drawString(contact_x + lw + 2, contact_y, text)
        contact_y -= 9.5

    # ── Rule under header ─────────────────────────────────────────────────────
    c.setStrokeColor(TEAL)
    c.setLineWidth(0.8)
    c.line(MARGIN, banner_bottom - 2 * mm, PAGE_W - MARGIN, banner_bottom - 2 * mm)


# ── CV Data ───────────────────────────────────────────────────────────────────

SUMMARY = (
    "Software Engineering graduate (First Class Honours, Lancaster University) who builds AI automation "
    "systems and deploys them end to end. Designed and shipped an AI automation platform across 20 "
    "manufacturing plants in India, evaluated 600+ AI systems at Browserbase to understand real-world "
    "model behavior, and built data architecture, data pipelines, and analytics tools across production "
    "environments. Python, SQL, JavaScript. Fluent in German (B2) and English (C1)."
)

EXPERIENCE = [
    {
        "company": "Stumpp Schuele & Somappa Springs",
        "role":    "Junior IT Project Manager",
        "loc":     "Bangalore, India",
        "dates":   "Apr 2026 – Present",
        "bullets": [
            "Designed and deployed an **AI automation** platform using Python, SQL, and Next.js across 20 **manufacturing** plants in India; integrated site-wide **IT infrastructure** and eliminated manual registration overhead across all sites",
            "Built **data architecture** and automated **data analysis** pipelines that improved operational efficiency by **40%** — defined the schema, wrote the backend, and ran end-to-end production deployment",
            "Led **cross-functional** collaboration across engineering and operations teams; gathered requirements from stakeholders with conflicting priorities, translated them into clear system specifications, and drove delivery from first brief to go-live",
        ],
    },
    {
        "company": "Browserbase",
        "role":    "AI Research Contractor",
        "loc":     "Remote",
        "dates":   "Feb 2026 – Present",
        "bullets": [
            "Conducted **600+ structured** evaluations of AI systems; applied **analytical thinking** to identify edge cases, failure patterns, and model behavior gaps across diverse use cases",
            "Synthesized findings into prioritized improvement recommendations used directly by the development team — communicated technical conclusions clearly to non-technical stakeholders",
        ],
    },
    {
        "company": "Carl Zeiss AG",
        "role":    "Working Student – Data & Analytics",
        "loc":     "Oberkochen, Germany",
        "dates":   "Nov 2024 – Aug 2025",
        "bullets": [
            "Built a centralized **Power BI** dashboard replacing fragmented **Excel** and SAP Analytics reports; cut global budget reporting time by **50%**",
            "Led a team of 5 interns through a shifting project scope — coordinated priorities, adapted the delivery plan when requirements changed, and reported progress to global project leadership",
            "Designed automated data pipelines and analytics dashboards supporting **data-driven** decision-making across a global programme",
        ],
    },
    {
        "company": "Carl Zeiss AG",
        "role":    "Intern – Digital Transformation",
        "loc":     "Oberkochen, Germany",
        "dates":   "Jun 2024 – Aug 2024",
        "bullets": [
            "Built a **Power BI** KPI dashboard to monitor NPS and track digital transformation progress during SAP-to-Salesforce migration",
            "Gathered stakeholder requirements, managed platform access, and delivered **data-driven** reports to global project leadership",
        ],
    },
    {
        "company": "Carl Zeiss BV",
        "role":    "Operations Intern",
        "loc":     "Breda, Netherlands",
        "dates":   "Jul 2023 – Aug 2023",
        "bullets": [
            "Produced technical documentation for platform **IT infrastructure**; supported digital operations across sales and inventory workflows",
        ],
    },
    {
        "company": "Carl Zeiss Mexico",
        "role":    "Marketing Intern",
        "loc":     "Mexico City, Mexico",
        "dates":   "Aug 2022 – Sep 2022",
        "bullets": [
            "Designed a **data-driven** marketing campaign for a medical product, increasing social media reach by 5%",
        ],
    },
]

EDUCATION = [
    {
        "school": "Lancaster University",
        "degree": "Bachelor of Science (BSc) Software Engineering — First Class Honours (18.0)",
        "loc":    "Leipzig, Germany",
        "dates":  "Oct 2021 – Jul 2025",
    },
]

SKILLS = {
    "Analysis":     ["Power BI", "Excel", "SQL", "SAP Analytics", "Salesforce", "Tableau"],
    "Technology":   ["Python", "JavaScript", "TypeScript", "Java", "React", "Git"],
    "AI & Research":["AI Automation", "AI Systems Evaluation", "LLM Research", "Agentic AI", "Claude Code"],
    "Languages":    ["Spanish (Native)", "English (C1)", "German (B2)", "French (B1)"],
}

ADDITIONAL = (
    "Personal Investment Portfolio (Mar 2025 – Present): independently managing a personal equity portfolio, "
    "applying data analysis to allocation decisions; 20%+ cumulative return. "
    "AI Agent Development (Mar 2026 – Present): built a custom AI system to automate application workflows "
    "using technology-driven optimization; 30% increase in interview invitations."
)


# ── Main generation ────────────────────────────────────────────────────────────

def generate(photo_path=None, out_path=OUT):
    c = canvas.Canvas(out_path, pagesize=A4)

    # ── Header ────────────────────────────────────────────────────────────────
    draw_header(c, photo_path)

    # Body starts below header rule
    y = PAGE_H - HEADER_H - 8 * mm

    # ── PROFILE ───────────────────────────────────────────────────────────────
    y = section_header(c, BODY_X, y, BODY_W, "PROFILE")
    for ln in wrap(c, SUMMARY, "Helvetica", 8.5, BODY_W):
        c.setFont("Helvetica", 8.5)
        c.setFillColor(DARK)
        c.drawString(BODY_X, y - 6, ln)
        y -= 11
    y -= 8

    # ── EXPERIENCE ────────────────────────────────────────────────────────────
    y = section_header(c, BODY_X, y, BODY_W, "PROFESSIONAL EXPERIENCE")

    for exp in EXPERIENCE:
        # Company (bold dark) + right-aligned gray loc | dates
        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(DARK)
        c.drawString(BODY_X, y, exp["company"])

        right = f"{exp['loc']}  |  {exp['dates']}"
        rw    = c.stringWidth(right, "Helvetica", 7.5)
        c.setFont("Helvetica", 7.5)
        c.setFillColor(GRAY)
        c.drawString(BODY_X + BODY_W - rw, y, right)
        y -= 12

        # Role (italic teal)
        c.setFont("Helvetica-Oblique", 9)
        c.setFillColor(TEAL)
        c.drawString(BODY_X, y, exp["role"])
        y -= 12

        for b in exp["bullets"]:
            y = bullet(c, BODY_X, y, b, BODY_W)
        y -= 6

    # ── EDUCATION ─────────────────────────────────────────────────────────────
    y = section_header(c, BODY_X, y, BODY_W, "EDUCATION")

    for edu in EDUCATION:
        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(DARK)
        c.drawString(BODY_X, y, edu["school"])

        rt = f"{edu['loc']}  |  {edu['dates']}"
        c.setFont("Helvetica", 7.5)
        c.setFillColor(GRAY)
        c.drawString(BODY_X + BODY_W - c.stringWidth(rt, "Helvetica", 7.5), y, rt)
        y -= 12

        c.setFont("Helvetica-Oblique", 9)
        c.setFillColor(TEAL)
        c.drawString(BODY_X, y, edu["degree"])
        y -= 16

    y -= 2

    # ── SKILLS & LANGUAGES ────────────────────────────────────────────────────
    y = section_header(c, BODY_X, y, BODY_W, "SKILLS & LANGUAGES")

    for category, items in SKILLS.items():
        c.setFont("Helvetica-Bold", 8.5)
        c.setFillColor(TEAL)
        label = f"{category}: "
        c.drawString(BODY_X, y - 6, label)
        lw = c.stringWidth(label, "Helvetica-Bold", 8.5)
        c.setFont("Helvetica", 8.5)
        c.setFillColor(DARK)
        # Wrap remaining text if it overflows
        remaining = "  •  ".join(items)
        skill_lines = wrap(c, remaining, "Helvetica", 8.5, BODY_W - lw)
        for i, ln in enumerate(skill_lines):
            if i == 0:
                c.drawString(BODY_X + lw, y - 6, ln)
            else:
                y -= 11
                c.drawString(BODY_X + lw, y - 6, ln)
        y -= 12

    y -= 4

    # ── ADDITIONAL ────────────────────────────────────────────────────────────
    y = section_header(c, BODY_X, y, BODY_W, "ADDITIONAL")
    for ln in wrap(c, ADDITIONAL, "Helvetica", 8.5, BODY_W):
        c.setFont("Helvetica", 8.5)
        c.setFillColor(DARK)
        c.drawString(BODY_X, y - 6, ln)
        y -= 11

    c.save()
    print(f"CV saved -> {out_path}")
    return out_path


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Marcos CV as PDF")
    parser.add_argument(
        "--photo", "-p",
        default=PHOTO,
        help="Path to profile photo (default: cv-creating/assets/profile-pic.jpg)",
    )
    parser.add_argument(
        "--out", "-o",
        default=OUT,
        help=f"Output PDF path (default: {OUT})",
    )
    args = parser.parse_args()
    generate(photo_path=args.photo, out_path=args.out)
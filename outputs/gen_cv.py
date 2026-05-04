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
OUT      = "cv_Marcos_Gonzalez.pdf"
PHOTO    = r"C:\Users\Marcos\Documents\Projects\cmd-agent-helper\cv-creating\assets\profile-pic.jpg"

# ── Design tokens ─────────────────────────────────────────────────────────────
TEAL       = colors.HexColor("#4A7FA5")
TEAL_LIGHT = colors.HexColor("#EDF3F8")
DARK       = colors.HexColor("#1A1A2E")
GRAY       = colors.HexColor("#888888")
WHITE      = colors.white

PAGE_W, PAGE_H = A4          # 595.28 x 841.89 pts
MARGIN        = 14 * mm
BODY_X        = MARGIN
BODY_W        = PAGE_W - 2 * MARGIN
HEADER_H      = 40 * mm      # height of the top banner area
BOTTOM_MARGIN = 10 * mm      # minimum y before content clips off the page


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


def _teal_right_edge_at(y):
    """Right x boundary of the diagonal teal banner shape at vertical position y."""
    banner_bottom = PAGE_H - HEADER_H
    t = max(0.0, min(1.0, (y - banner_bottom) / HEADER_H))
    return PAGE_W * 0.44 + (PAGE_W * 0.60 - PAGE_W * 0.44) * t


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

    # Auto-shrink name font so both lines stay within the teal shape
    name_sz = 19
    name_line1 = "MARCOS GONZALEZ"
    name_line2 = "FERNANDEZ"
    for line in (name_line1, name_line2):
        avail = _teal_right_edge_at(name_y) - name_x - 4 * mm
        while name_sz > 12 and c.stringWidth(line, "Helvetica-Bold", name_sz) > avail:
            name_sz -= 0.5

    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", name_sz)
    line_gap = name_sz + 2
    c.drawString(name_x, name_y,            name_line1)
    c.drawString(name_x, name_y - line_gap, name_line2)

    # Auto-shrink subtitle so it stays within the teal shape at that y
    subtitle_text = "AI & Automation  |  End-to-End Process Automation"
    subtitle_y = name_y - line_gap - 15
    avail_sub = _teal_right_edge_at(subtitle_y) - name_x - 4 * mm
    sub_sz = 8.5
    while sub_sz > 6.0 and c.stringWidth(subtitle_text, "Helvetica-Oblique", sub_sz) > avail_sub:
        sub_sz -= 0.25
    c.setFont("Helvetica-Oblique", sub_sz)
    c.setFillColor(colors.HexColor("#D0E8F5"))
    c.drawString(name_x, subtitle_y, subtitle_text)

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
    "Software Engineering graduate (First Class Honours, Lancaster University) who builds automation systems. "
    "Deployed end-to-end AI automation across 20 manufacturing sites at Stumpp Schuele - requirements, architecture, "
    "development, testing, and go-live owned without hand-offs, achieving 40% operational efficiency improvement. "
    "Built an agentic AI platform at Meerkats AI, mapping manual processes and replacing them with automated workflows. "
    "Built an AI automation bot independently to automate own job application process - in production, producing results. "
    "Applies Gen-AI and scripting to optimize work as a matter of course. Analytical and structured by default. "
    "English C1, German B2."
)

EXPERIENCE = [
    {
        "company": "Meerkats AI",
        "role":    "AI Founder Associate",
        "loc":     "Remote",
        "dates":   "Apr 2026 – Present",
        "bullets": [
            "Built an **agentic AI** automation platform from the ground up in a **startup** environment, engineering multi-step **workflow** automation against real business data and driving a **25%** uplift in user engagement",
            "Mapped business **workflows**, identified manual processes as **automation** targets, and shipped a **multi-agent** communication system into the founding team's live operations - from idea to MVP",
            "Applied **AI** and **automation** tools to optimize internal processes, iterating rapidly on outputs and improving reliability across the full deployment lifecycle",
        ],
    },
    {
        "company": "Stumpp Schuele & Somappa Springs",
        "role":    "Junior IT Project Manager",
        "loc":     "Bangalore, India",
        "dates":   "Apr 2026 – Present",
        "bullets": [
            "Designed and deployed an **AI**-powered **automation** platform across **20** manufacturing sites using **Python**, **TypeScript**, and **SQL**; achieved **40%** operational efficiency improvement through systematic **process optimization** of high-volume manual **workflows**",
            "Mapped manual process bottlenecks across a distributed industrial environment, designed automated replacement systems, and delivered end to end: requirements, architecture, development, **testing**, and **go-live** without hand-offs",
            "Built automated backend pipelines eliminating manual coordination; **documented** processes, requirements, and architecture for long-term maintainability across the full site network",
        ],
    },
    {
        "company": "Browserbase",
        "role":    "AI Research Contractor",
        "loc":     "Remote",
        "dates":   "Feb 2026 – Present",
        "bullets": [
            "Evaluated **600+ real AI** outputs in production, systematically identifying edge cases and failure modes using **structured analytical** frameworks across diverse real-world use cases",
            "Developed practical **analytical** intuition for how frontier **AI** models perform under real conditions, translating findings into **quality** improvement priorities for the development team",
        ],
    },
    {
        "company": "Carl Zeiss AG",
        "role":    "Working Student – Data & Analytics",
        "loc":     "Oberkochen, Germany",
        "dates":   "Nov 2024 – Aug 2025",
        "bullets": [
            "Drove **data-driven** reporting for a global programme by consolidating fragmented Excel and SAP Analytics sources into centralized **data pipelines**, cutting reporting time by **50%**",
            "Built and maintained a **Power BI** dashboard for global budget tracking, supporting strategic decision-making with automated real-time data integration for international project leadership",
            "Coordinated a team of 5 interns through shifting project scope, managing priorities and communicating progress to global stakeholders",
        ],
    },
    {
        "company": "Carl Zeiss AG",
        "role":    "Intern – Digital Transformation",
        "loc":     "Oberkochen, Germany",
        "dates":   "Jun 2024 – Aug 2024",
        "bullets": [
            "Supported a large-scale digital transformation (SAP to Salesforce migration): gathered stakeholder requirements, built Power BI reporting solutions, and delivered data-driven insights enabling informed decisions throughout the transition",
        ],
    },
]

EDUCATION = [
    {
        "school": "Lancaster University",
        "degree": "Bachelor of Science (BSc) Software Engineering, First Class Honours (18.0)",
        "loc":    "Leipzig, Germany",
        "dates":  "Oct 2021 – Jul 2025",
    },
]

SKILLS = {
    "Automation":    ["Process Automation", "Workflow Design", "Process Optimization", "AI Automation", "Scripting", "Python", "TypeScript", "SQL"],
    "AI":            ["Agentic AI", "Gen-AI", "LLM Integration", "AI Evaluation", "Prompt Engineering", "Claude"],
    "Analytics":     ["Power BI", "Microsoft Excel", "SAP Analytics", "Tableau", "Salesforce"],
    "Technical":     ["Java", "JavaScript", "React", "Next.js", "Git", "Maven", "JUnit (Testing)"],
    "Languages":     ["Spanish (Native)", "English (C1)", "German (B2)", "French (B1)"],
}

ADDITIONAL = (
    "Custom AI Automation Bot (Mar 2026 – Present): built a multi-agent AI bot from scratch to automate own job "
    "application workflows end to end - document generation, process automation, and scripted output delivery; "
    "30% increase in interview invitations. Built independently, without existing infrastructure. "
    )


# ── Main generation ───────────────────────────────────────────────────────────

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
        y -= 10
    y -= 3

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
        y -= 11

        # Role (italic teal)
        c.setFont("Helvetica-Oblique", 9)
        c.setFillColor(TEAL)
        c.drawString(BODY_X, y, exp["role"])
        y -= 11

        for b in exp["bullets"]:
            y = bullet(c, BODY_X, y, b, BODY_W)
        y -= 2

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
        y -= 14

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
        y -= 11

    y -= 2

    # ── ADDITIONAL ────────────────────────────────────────────────────────────
    additional_lines = wrap(c, ADDITIONAL, "Helvetica", 8.5, BODY_W)
    # Estimate space needed: section header (~16) + lines * 11 + padding
    space_needed = 16 + len(additional_lines) * 11 + 6
    if y - space_needed < BOTTOM_MARGIN:
        print(
            f"  [layout] WARNING: ADDITIONAL section needs ~{space_needed:.0f}pt but only "
            f"{y - BOTTOM_MARGIN:.0f}pt remain — content will be clipped.",
            file=sys.stderr,
        )

    y = section_header(c, BODY_X, y, BODY_W, "ADDITIONAL")
    clipped = False
    for ln in additional_lines:
        if y - 6 < BOTTOM_MARGIN:
            clipped = True
            break
        c.setFont("Helvetica", 8.5)
        c.setFillColor(DARK)
        c.drawString(BODY_X, y - 6, ln)
        y -= 11

    c.save()

    # ── Post-generation layout report ─────────────────────────────────────────
    _report_layout(out_path, y, clipped)

    return out_path


def _report_layout(out_path, final_y, clipped):
    """Print a layout summary after PDF generation."""
    margin_pts = BOTTOM_MARGIN
    remaining  = final_y - margin_pts
    status     = "OK" if (remaining >= 0 and not clipped) else "WARNING"

    print(f"\n{'='*52}")
    print(f"  Layout report: {out_path}")
    print(f"{'='*52}")
    if clipped:
        print("  [FAIL] ADDITIONAL section was clipped — content did not fit.")
        print("         Shorten the ADDITIONAL text or reduce other sections.")
    elif remaining < 0:
        print(f"  [FAIL] Content overflowed page by {-remaining:.1f}pt ({-remaining/mm:.1f}mm).")
        print("         Reduce content or tighten line spacing.")
    else:
        print(f"  [{status}]  Final y = {final_y:.1f}pt — {remaining:.1f}pt ({remaining/mm:.1f}mm) above bottom margin.")
    print(f"{'='*52}\n")


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
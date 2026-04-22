---
name: cv-template
description: >
  Use this skill to produce an ATS-optimized CV as a styled PDF matching a professional design template. Trigger whenever the user wants to: create or rewrite a CV/resume as a PDF, optimize an existing CV for a job description, generate a polished resume from scratch, tailor a CV for a specific role, or produce a CV that matches a visual template. Also trigger on phrases like "make my CV", "update my resume", "tailor my CV for this job", "build my CV as a PDF", or when the user uploads a CV and wants a designed PDF output. Always use this skill when a PDF CV is the expected deliverable.
---

# CV Template Skill

Produces an ATS-optimized CV as a styled **PDF** matching the reference design.

## Reference Asset

`assets/design-reference.pdf` serves **two purposes**:

1. **Content example** — study it to understand what a strong CV looks like: clear structure, concise bullets with measurable outcomes, good use of roles/dates, a tight summary statement. Use this as your quality bar for the candidate's content.
2. **Visual template** — replicate its exact design in the PDF output.

Read the reference cv.json at the start of every run then study its layout visually.

### Design Spec (extracted from reference)

| Element | Value |
|---|---|
| **Page size** | A4 |
| **Margins** | ~14mm all sides |
| **Layout** | Two-column: left sidebar ~25% + right main body ~75% |
| **Accent color** | `#4A7FA5` (teal/steel blue) |
| **Name** | 22–24pt, bold, teal, all-caps |
| **Job title** | 11pt, teal, italic, directly under name |
| **Section headers** | 9pt, bold, all-caps, teal, centered — flanked by dashed rules in same teal |
| **Body font** | Helvetica, 9pt |
| **Experience entry** | Company bold 9.5pt, Role italic teal, Location + Dates right-aligned in gray |
| **Bullets** | Small filled circle, indented ~8mm, 8.5pt body text |
| **Contact block** | Sidebar top — phone, email, address stacked |
| **Languages / Skills** | Sidebar bottom, below a section divider |

---

## Workflow

### Step 1 — Gather Inputs

You need:
- Candidate CV content (text, extracted PDF, or JSON)
- Job description (for ATS optimization)

If either is missing, ask before proceeding. If only a CV is provided, optimize for clarity and impact without keyword tailoring and note this in the summary.

### Step 2 — ATS Content Optimization

**Extract keywords** from the job description:
- Technical skills, tools, technologies
- Methodologies and domain terminology
- Soft skills explicitly called out

**Gap analysis** — compare against candidate's CV:
- Missing or underrepresented keywords
- Weak bullets (vague, no action verb, no measurable outcome)

**Rewrite rules:**
- Lead every bullet with a strong action verb (Engineered, Delivered, Automated, Reduced, Led, Launched…)
- Add measurable outcomes where truthful data exists (%, time saved, team size, revenue impact)
- Weave keywords in naturally — no stuffing

**Hard constraints:**
- NEVER fabricate skills or experience
- NEVER add technologies the candidate clearly doesn't know
- Every claim must be truthful and verifiable

### Step 3 — Build the PDF with ReportLab

Use `reportlab` (Python). Install: `pip install reportlab --break-system-packages`

#### Page and Layout Constants
```python
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm

TEAL  = colors.HexColor("#4A7FA5")
DARK  = colors.HexColor("#1A1A2E")
GRAY  = colors.HexColor("#666666")

PAGE_W, PAGE_H = A4          # 595 x 842 pts
MARGIN    = 14 * mm
SIDEBAR_W = PAGE_W * 0.30
MAIN_X    = MARGIN + SIDEBAR_W + 6 * mm
MAIN_W    = PAGE_W - MAIN_X - MARGIN
```

#### Two-Column Layout
Track two independent `y` cursors — one for the sidebar (`side_y`) and one for the main body (`main_y`). Draw sidebar content within `x ∈ [MARGIN, MARGIN + SIDEBAR_W]`, main body content starting at `MAIN_X`.

#### Section Divider Helper
```python
def draw_section_header(c, x, y, width, text):
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(TEAL)
    text_w = c.stringWidth(text, "Helvetica-Bold", 8)
    gap = 3 * mm
    line_w = (width - text_w - 2 * gap) / 2
    mid_y = y - 3
    c.setStrokeColor(TEAL)
    c.setDash(2, 3)
    c.line(x, mid_y, x + line_w, mid_y)
    c.line(x + line_w + gap + text_w + gap, mid_y, x + width, mid_y)
    c.setDash()
    c.drawString(x + line_w + gap, y - 6, text.upper())
    return y - 14  # return updated y
```

#### Bullet Helper
```python
def draw_bullet_line(c, x, y, text, max_width, font="Helvetica", size=8.5):
    # Draw bullet dot
    c.setFillColor(TEAL)
    c.circle(x + 2*mm, y - 2.5, 1.2, fill=1, stroke=0)
    # Draw text (wrap manually if needed)
    c.setFillColor(DARK)
    c.setFont(font, size)
    c.drawString(x + 5*mm, y - 6, text)
    return y - 12
```

For long bullet text, use ReportLab's `Paragraph` with `ParagraphStyle` for proper word-wrapping, or implement manual word-wrap using `stringWidth`.

#### Mixed Bold/Normal on One Line
Draw segments individually, advancing `x` by `stringWidth` between segments:
```python
c.setFont("Helvetica-Bold", 9.5); c.setFillColor(DARK)
c.drawString(x, y, company_name)
bold_w = c.stringWidth(company_name, "Helvetica-Bold", 9.5)
c.setFont("Helvetica-Oblique", 9); c.setFillColor(TEAL)
c.drawString(x, y - 12, role_title)
```

### Step 4 — Validate and Deliver

```bash
python -c "from pypdf import PdfReader; r=PdfReader('cv_output.pdf'); print(len(r.pages), 'pages OK')"
```

Copy to `/mnt/user-data/outputs/cv_output.pdf` and use `present_files` to deliver.

Include a brief text summary alongside the file:
- Keywords added and which bullets were rewritten
- Any skill gaps (what the JD requires that the candidate lacks — do not fabricate these)

---

## Output Checklist

Before delivering, verify:
- [ ] Name and title in teal at the top of the main column
- [ ] Sidebar has contact info, languages, additional skills
- [ ] All section headers use the teal dashed-rule style
- [ ] Experience bullets lead with action verbs and have measurable outcomes where possible
- [ ] Dates and locations right-aligned in gray
- [ ] Two-column layout visually matches `assets/design-reference.pdf`
- [ ] ATS keywords integrated naturally
- [ ] No fabricated skills or experience
- [ ] PDF renders correctly (validate page count and open visually if possible)
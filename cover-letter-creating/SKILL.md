---
name: cover-letter-creating
description: >
  Use this skill to produce a tailored, ATS-optimized cover letter as a styled PDF that matches the professional reference design. Trigger whenever the user wants to: write or rewrite a cover letter, generate a job application letter, tailor a cover letter to a specific job description, or produce a cover letter PDF from a CV + job description. Also trigger on phrases like "write me a cover letter", "draft a cover letter for this job", "make a cover letter matching my CV", "cover letter PDF", or when the user provides a CV and job description and wants application materials. Always use this skill when a cover letter PDF is the expected output.
---

# Cover Letter Skill

Produces a tailored, ATS-optimized cover letter as a **PDF** that matches the reference design in `assets/design-reference.pdf`.

## Reference Asset

`assets/design-reference.pdf` is the visual and structural template. Study it before every run.

### Design Spec (from the reference)

| Element | Spec |
|---|---|
| **Page** | A4 (596 × 842 pts), ~25mm left/right margins, ~30mm top margin |
| **Header — Name** | Centered, ~24pt, bold, Times New Roman or STIXTwoText-Bold, black |
| **Header — Contact line** | Centered, ~10pt, regular, location · phone · email separated by `·` |
| **Header — LinkedIn/URL** | Centered, ~10pt, hyperlink blue underlined |
| **Divider** | Full-width horizontal rule (~0.8pt, black), immediately below the URL line |
| **Company block** | Left-aligned, ~11pt regular — Company name, Address, Date (each on its own line, ~6pt spacing between) |
| **Subject line** | Left-aligned, **bold**, ~11pt — "Application for [Role] - Start Date: [Date]" |
| **Salutation** | Left-aligned, ~11pt regular — "Dear [Name]," with one blank line above and below |
| **Body paragraphs** | Justified, ~11pt, ~16pt line spacing, ~10pt spacing between paragraphs |
| **Closing** | Left-aligned — "Warm regards," then full name on next line |
| **Body font** | STIXTwoText-Regular (fallback: Times New Roman) |
| **Bold font** | STIXTwoText-Bold (fallback: Times New Roman Bold) |
| **No color anywhere** — pure black and white except the LinkedIn hyperlink blue |

---

## Workflow

### Step 1 — Gather Inputs

You need all three:
1. **Candidate CV** — for skills, experience, and personal details to draw from
2. **Job description** — for keyword extraction and role-specific tailoring
3. **Basic letter details** — company name, hiring manager name (if known), role title, desired start date, company address

If anything is missing, ask before writing.

### Step 2 — Keyword Extraction & CV Matching

**From the job description, extract:**
- Core technical skills and tools explicitly mentioned
- Domain / industry keywords (e.g. "digital transformation", "financial sector", "agile")
- Soft skills called out (e.g. "analytical thinking", "client-facing", "problem-solving")
- Any specific methodologies, frameworks, or certifications

**From the CV, identify:**
- Experiences that directly map to the JD keywords
- Quantified achievements that can anchor the letter's narrative
- Skills that match — these become the backbone of the letter's evidence

**Matching logic:**
- Every keyword used in the letter must map to something real in the CV
- Never mention a skill or tool the candidate doesn't have on their CV
- If the JD asks for something absent from the CV, skip it silently — do not fabricate

### Step 3 — Write the Letter

**Structure (follow the reference exactly):**

```
[Name — centered bold]
[Location · Phone · Email — centered]
[LinkedIn URL — centered, underlined]
────────────────────────────────────────

[Company Name]
[Company Address]
[Date]

Application for [Role Title] - Start Date: [Date]

Dear [Hiring Manager Name] and [Team],

OPENING PARAGRAPH
Hook — connect the candidate's background directly to the role.
Name-drop the company and role explicitly. State the core value proposition.

EVIDENCE PARAGRAPH (1–2 paragraphs)
Tell a specific story from the CV that maps to a JD keyword.
Use concrete details: what the candidate did, what tool/method they used,
what measurable result they achieved. Mirror JD language naturally.

MOTIVATION PARAGRAPH
Why this company specifically — reference something real about the company
(their work, sector focus, culture, values) that aligns to the candidate.
Avoid generic praise. Connect to the candidate's stated direction.

CLOSING PARAGRAPH
Brief call to action. Express enthusiasm. Sign off.

Warm regards,
[Full Name].
```

**Tone guidelines:**
- Professional but not stiff — confident, direct, specific
- First person throughout
- Avoid filler phrases: "I am writing to apply for…", "I believe I would be a great fit…"
- Lead with substance, not pleasantries
- Each paragraph should have one clear job — no paragraph tries to do two things
- NEVER state soft skills directly ("I am a collaborative and analytical person…")
  Soft skills must be shown through specific situations and outcomes, not named.
  Examples:
    ✗  "I am an adaptable and problem-solving oriented professional"
    ✓  "When requirements shifted mid-project, I restructured the delivery plan and kept the timeline"
    ✓  "I gathered input from teams with conflicting priorities and turned it into a single spec"

### Step 4 — Build the PDF with ReportLab

Install: `pip install reportlab --break-system-packages`

#### Page Setup
```python
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, pt
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT

PAGE_W, PAGE_H = A4          # 595.27 x 841.89 pts
L_MARGIN = 25 * mm
R_MARGIN = 25 * mm
T_MARGIN = 30 * mm
CONTENT_W = PAGE_W - L_MARGIN - R_MARGIN

BLACK = colors.black
LINK_BLUE = colors.HexColor("#1155CC")
```

#### Fonts
Use `Times-Roman` and `Times-Bold` (built-in ReportLab fonts that closely match the reference STIXTwoText). Do NOT use Helvetica — the reference is a serif document.

```python
# Register nothing — use built-in:
# "Times-Roman", "Times-Bold", "Times-Italic", "Times-BoldItalic"
```

#### Header Block
```python
def draw_header(c, name, location, phone, email, linkedin_url, y_start):
    # Name
    c.setFont("Times-Bold", 24)
    c.setFillColor(BLACK)
    c.drawCentredString(PAGE_W / 2, y_start, name.upper() if False else name)
    y = y_start - 18

    # Contact line: "City · +xx · email"
    contact_line = f"{location}  ·  {phone}  ·  {email}"
    c.setFont("Times-Roman", 10)
    c.drawCentredString(PAGE_W / 2, y, contact_line)
    y -= 14

    # LinkedIn — draw as underlined blue text
    c.setFillColor(LINK_BLUE)
    c.setFont("Times-Roman", 10)
    link_w = c.stringWidth(linkedin_url, "Times-Roman", 10)
    link_x = (PAGE_W - link_w) / 2
    c.drawString(link_x, y, linkedin_url)
    c.line(link_x, y - 1, link_x + link_w, y - 1)  # underline
    y -= 10

    # Horizontal rule
    c.setFillColor(BLACK)
    c.setStrokeColor(BLACK)
    c.setLineWidth(0.8)
    c.line(L_MARGIN, y, PAGE_W - R_MARGIN, y)
    return y - 18  # return y cursor after rule + padding
```

#### Body Text with Justification
Use ReportLab's `Paragraph` + `Frame` for justified, word-wrapped body text:

```python
body_style = ParagraphStyle(
    "body",
    fontName="Times-Roman",
    fontSize=11,
    leading=16,        # line spacing
    spaceBefore=10,    # paragraph gap
    alignment=TA_JUSTIFY,
)
bold_style = ParagraphStyle("bold", parent=body_style, fontName="Times-Bold")
left_style = ParagraphStyle("left", parent=body_style, alignment=TA_LEFT)

# Build story list then draw via Frame
story = []
story.append(Paragraph(company_name, left_style))
story.append(Paragraph(address, left_style))
story.append(Paragraph(date_str, left_style))
story.append(Paragraph("&nbsp;", left_style))  # blank line
story.append(Paragraph(f"<b>Application for {role} - Start Date: {start_date}</b>", left_style))
story.append(Paragraph("&nbsp;", left_style))
story.append(Paragraph(f"Dear {salutation},", left_style))
story.append(Paragraph("&nbsp;", left_style))
for para in body_paragraphs:
    story.append(Paragraph(para, body_style))
story.append(Paragraph("&nbsp;", left_style))
story.append(Paragraph("Warm regards,", left_style))
story.append(Paragraph(candidate_name + ".", left_style))

# Draw the frame
frame = Frame(L_MARGIN, 20*mm, CONTENT_W, body_area_height,
              leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
frame.addFromList(story, c)
```

#### Inline bold in body text
Use ReportLab XML tags inside `Paragraph`:
```python
Paragraph("I have worked with <b>Power BI</b> and <b>SAP Analytics</b> to...", body_style)
```

### Step 5 — Validate and Deliver

```bash
python -c "from pypdf import PdfReader; r=PdfReader('cover_letter.pdf'); print(len(r.pages), 'pages OK')"
```

Copy to `/mnt/user-data/outputs/cover_letter.pdf` and use `present_files`.

Also output inline:
- The 5–8 JD keywords used in the letter
- Which CV experiences were mapped to each keyword
- Any JD requirements not addressed (and why — missing from CV)

---

## Output Checklist

Before delivering, verify:
- [ ] Header: Name bold centered, contact line centered, LinkedIn underlined blue, horizontal rule
- [ ] Company block left-aligned with line breaks between each field
- [ ] Subject line bold
- [ ] Salutation with blank line above and below
- [ ] Body paragraphs justified, serif font, correct leading
- [ ] Every claim maps to a real CV entry — nothing fabricated
- [ ] JD keywords woven in naturally (not stuffed)
- [ ] Closing: "Warm regards," then candidate name on next line
- [ ] PDF is A4, single page if possible
- [ ] Validates without errors
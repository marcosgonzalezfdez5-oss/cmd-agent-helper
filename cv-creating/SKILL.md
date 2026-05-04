---
name: cv-template
description: >
  Use this skill to produce an ATS-optimized CV as a styled PDF matching a professional design template. Trigger whenever the user wants to: create or rewrite a CV/resume as a PDF, optimize an existing CV for a job description, generate a polished resume from scratch, tailor a CV for a specific role, or produce a CV that matches a visual template. Also trigger on phrases like "make my CV", "update my resume", "tailor my CV for this job", "build my CV as a PDF", or when the user uploads a CV and wants a designed PDF output. Always use this skill when a PDF CV is the expected deliverable.
---

# CV Template Skill

Produces an ATS-optimized CV as a styled **PDF** matching the reference design.

This skill uses the existing `gen_cv.py` file to generate the final PDF output.  
Do not recreate the PDF generator logic manually — always use the existing script.

---

## Reference Asset

`assets/design-reference.pdf` serves **two purposes**:

1. **Content example** — study it to understand what a strong CV looks like: clear structure, concise bullets with measurable outcomes, good use of roles/dates, a tight summary statement. Use this as your quality bar for the candidate's content.
2. **Visual template** — the generated PDF must visually match this design.

Also read the reference `cv.json` at the start of every run to understand the expected structure and formatting.

---

## Workflow

---

### Step 1 — Gather Inputs

You need:

- Candidate CV content (text, extracted PDF, or JSON)
- Job description (for ATS optimization)

If either is missing, ask before proceeding.

If only a CV is provided:
- optimize for clarity and impact
- improve ATS readability
- do not perform keyword tailoring
- mention this clearly in the final summary

---

### Step 2 — ATS Content Optimization

Extract keywords from the job description:

- Technical skills
- Tools and technologies
- Methodologies
- Domain terminology
- Required soft skills

Perform gap analysis:

- Missing or weak keywords
- Vague bullets
- Missing measurable outcomes
- Weak action verbs

Rewrite rules:

- Start every bullet with a strong action verb  
  (Engineered, Built, Automated, Reduced, Led, Delivered, Optimized, Designed, Implemented…)

- Add measurable outcomes where truthful data exists  
  (% improvement, time saved, users impacted, team size, revenue, etc.)

- Integrate ATS keywords naturally  
  (never keyword stuffing)

Hard constraints:

- NEVER fabricate experience
- NEVER invent skills
- NEVER add technologies the candidate does not know
- Every statement must remain truthful and verifiable
- NEVER list soft skills as a standalone section (e.g. "Soft Skills: Problem Solving, Collaborative…")
  Soft skills must be demonstrated through experience bullet wording, not stated as traits.
  Examples:
    ✗  "Soft Skills: Problem Solving, Adaptability, Leadership"
    ✓  "gathered requirements from stakeholders with conflicting priorities" → shows problem solving
    ✓  "adapted the delivery plan when requirements changed" → shows adaptability
    ✓  "led a team of 5 interns through a shifting project scope" → shows leadership

---

### Step 3 — Prepare Structured CV Data

Convert the optimized CV into the expected structured format required by `gen_cv.py`.

Use a clean structure like:

```json
{
  "name": "",
  "title": "",
  "contact": {},
  "summary": "",
  "experience": [],
  "education": [],
  "skills": [],
  "languages": []
}
```

---

### Step 4 — Generate and Deliver

Run the generator:

```bash
py outputs/gen_cv.py
```

**Output filename rule:**  
Always output to `outputs/cv_Marcos_Gonzalez.pdf` — this overwrites the existing file.  
Never create job-specific filenames like `cv_Marcos_Vetaion.pdf` or `cv_output.pdf`.  
The single fixed path ensures the output folder stays clean and the latest version is always findable.

---

### Step 5 — Post-generation Layout Check (mandatory)

After generation, the script prints a layout report. **Always read it before declaring success.**

**Interpret the output:**

| Report line | Meaning | Action |
|---|---|---|
| `[OK]` with positive remaining | Content fits cleanly | Deliver the PDF |
| `[WARNING]` ADDITIONAL clipped | ADDITIONAL text overflowed page | Shorten ADDITIONAL or trim bullets in earlier sections |
| `[FAIL]` Content overflowed | Total content too long | Trim bullets / shorten summary / reduce skills rows |

**Banner overflow:**  
The generator auto-shrinks the name and subtitle to stay within the teal diagonal shape. If it shrank below 14pt (name) or 7pt (subtitle), the title/name is too long — shorten it.

**Rules:**
- Never deliver a PDF without checking the layout report
- If content is clipped, fix the content and re-run — do not skip
- The ADDITIONAL section is the first to be cut; trim it first before touching other sections
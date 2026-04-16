---
name: keywords-extracting
description: >
  Use this skill to extract, categorize, and map job description keywords against a candidate's CV for application targeting. Trigger whenever the user wants to: analyze a job description for keywords, understand what a job is really looking for, find gaps between their CV and a job posting, get a keyword map before writing or optimizing a CV or cover letter, or understand which of their skills to emphasize. Also trigger on phrases like "what keywords does this job have", "what does this job want", "analyze this job description", "what skills are they looking for", "what's missing from my CV for this job", "what should I emphasize", or any time a job description is provided alongside a CV before creating application materials. Always run this skill BEFORE the cv-template or cover-letter skills when a job description is available — the keyword map it produces feeds directly into both.
---

# JD Keyword Extractor

Extracts and categorizes keywords from a job description, then maps them to the candidate's CV to identify matches, gaps, and emphasis opportunities. The output feeds the `cv-template`, `cover-letter`, and `ats-score` skills.

---

## How This Differs from the JD Parser

The `job-description-parser` skill (in `/mnt/skills/user/job-description-parser/SKILL.md`) returns raw structured JSON from a JD alone. **This skill goes further** — it cross-references the JD against the candidate's CV to produce an actionable keyword map: what the candidate already has, what's missing, and exactly where each keyword should appear in the application documents.

Use the JD parser for raw extraction. Use this skill when you have both a JD and a CV and need application strategy.

---

## Inputs Required

1. **Job description** — paste, PDF, or URL
2. **Candidate CV** — text, PDF, or the output of the `cv-template` skill (`/mnt/user-data/outputs/cv_output.pdf`)

If the CV is a PDF, extract it first:
```bash
pdftotext -layout /mnt/user-data/outputs/cv_output.pdf /tmp/cv_text.txt
cat /tmp/cv_text.txt
```

---

## Workflow

### Step 1 — Extract Keywords from the JD

Scan the job description and extract keywords across six categories:

**A. Hard Skills** — specific tools, technologies, platforms, languages, certifications
- Examples: Power BI, Python, Salesforce, SQL, SAP, Agile, PMP

**B. Domain Keywords** — industry/function terms that signal context
- Examples: digital transformation, financial services, CRM migration, KPI reporting

**C. Role Action Keywords** — verbs and phrases describing what the person will do
- Examples: stakeholder management, data-driven decision-making, cross-functional collaboration

**D. Seniority & Scope Signals** — words indicating level and ownership
- Examples: lead, own, manage, junior, client-facing, strategy

**E. Soft Skills & Culture Signals** — adjectives and traits explicitly called out
- Examples: analytical, detail-oriented, adaptable, fast-paced, proactive

**F. ATS Exact-Match Strings** — phrases likely used as literal ATS filters
- Include job title variants, certification names, methodology names
- These must be kept verbatim from the JD — do not paraphrase

For each keyword, record:
- The category (A–F above)
- Whether it appears under a "Required" heading or "Nice to Have" heading
- The exact sentence it was found in (for context)

### Step 2 — Map Keywords Against the CV

For every keyword extracted in Step 1, check the CV text (case-insensitive):

- **✓ PRESENT** — keyword or close synonym found in CV
- **~ PARTIAL** — the concept is present but the exact term isn't (e.g., CV says "dashboard reporting" but JD says "KPI reporting")
- **✗ MISSING** — no evidence of this keyword in the CV at all

For PARTIAL matches, note what the CV says vs. what the JD uses — these are prime rewrite targets.

### Step 3 — Build the Keyword Map

Produce a structured keyword map in this format:

---

## Output Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  JD KEYWORD MAP
  Role: [Job Title] @ [Company]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ROLE SUMMARY (2 sentences)
[What this role is and who it serves — paraphrased from JD]

SENIORITY LEVEL: [intern / junior / mid / senior / lead]

━━━━ KEYWORD ANALYSIS ━━━━

HARD SKILLS
  ✓  Power BI              → CV: "Power BI dashboard" (Carl Zeiss bullet)
  ✓  SQL                   → CV: listed in Additional Skills
  ~  KPI reporting         → CV says "dashboard visibility" — rewrite to "KPI reporting"
  ✗  Tableau               → Not in CV [REQUIRED]
  ✗  Agile                 → Not in CV [NICE TO HAVE]

DOMAIN KEYWORDS
  ✓  digital transformation → CV: cover letter, Carl Zeiss description
  ~  financial sector       → CV has "budget tracking" — weaker signal
  ✗  CRM strategy           → Not in CV [REQUIRED]

ROLE ACTION KEYWORDS
  ✓  stakeholder reporting  → CV: "stakeholder decision-making"
  ~  client-facing          → CV has team coordination but not client-facing
  ✗  project management     → Not explicitly stated [REQUIRED]

SENIORITY & SCOPE
  ✓  cross-functional       → CV: "team of 5 interns", multiple internships

SOFT SKILLS & CULTURE
  ✓  analytical             → CV summary: "analytical and detail-oriented"
  ~  problem-solving        → Present in cover letter only, not in CV
  ✗  entrepreneurial        → Not in CV [NICE TO HAVE]

ATS EXACT-MATCH STRINGS (verbatim from JD)
  ✓  "Power BI"
  ✓  "data-driven"
  ✗  "digital transformation consultant"   [HIGH PRIORITY — add to CV title/summary]
  ✗  "change management"                   [REQUIRED]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  SUMMARY COUNTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Total keywords identified:   XX
  ✓ Present:                   XX  (XX%)
  ~ Partial match:             XX  (XX%)  ← highest-value rewrites
  ✗ Missing (required):        XX
  ✗ Missing (nice to have):    XX

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  RECOMMENDED ACTIONS (prioritized)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[CRITICAL — required keywords completely absent]
1. "change management" is required but absent. The Carl Zeiss Power BI project
   involved managing the transition from Excel to BI tools — reframe that bullet
   to reference "change management" explicitly.

[HIGH VALUE — partial matches to sharpen]
2. Replace "dashboard visibility" with "KPI reporting and dashboard visibility"
   in the Carl Zeiss Working Student bullet. Adds an exact ATS match with no
   fabrication.
3. "client-facing" is partially covered by your internship coordination work —
   add "client and stakeholder-facing reporting" to the Carl Zeiss BV bullet.

[ADDITIVE — missing nice-to-have keywords]
4. "Agile" is not in the CV. If any of your projects used iterative delivery or
   sprint-style work, add "Agile methodology" to the skills section.

[COVER LETTER EMPHASIS]
5. Lead with "digital transformation" in the opening paragraph — it is both a
   required JD term and the role title. Currently it appears only in the second
   paragraph of the reference cover letter.
```

---

## Rules

- **Never suggest fabricating** — every CRITICAL or HIGH VALUE action must reference a real CV experience
- **Partial matches are the highest ROI** — adding one exact term to an existing bullet costs nothing and can flip an ATS filter
- **ATS exact-match strings are highest priority** — these are the literal strings ATS software scans for; missing these is a binary fail
- **Keep domain keywords even if "obvious"** — candidates often omit industry terms because they feel redundant; ATS doesn't think, it scans
- **If a required keyword is genuinely absent from the CV** — flag it clearly as a gap, do not suggest how to fake it; suggest whether it's learnable or should be addressed in the cover letter instead

---

## Passing the Output Forward

After generating the keyword map, tell the user:

> "This keyword map is ready to use. You can now:
> - Run the **cv-template** skill to rebuild your CV with these keywords integrated
> - Run the **cover-letter** skill to write a tailored letter using the COVER LETTER EMPHASIS keywords
> - Run the **ats-score** skill after to verify the final match percentage"
---
name: ats-calculating
description: >
  Use this skill to calculate an ATS (Applicant Tracking System) match score and generate improvement tips for a candidate's application materials against a job description. Trigger whenever the user wants to: score or evaluate a CV against a job, check ATS compatibility, calculate a match percentage, get feedback on how well their CV or cover letter fits a role, or improve their chances of passing ATS screening. Also trigger on phrases like "how well does my CV match", "what's my ATS score", "will I pass the ATS", "score my application", "check my CV against the job", "give me tips to improve my CV", or when the user has already created a CV and/or cover letter and wants to know how strong the application is. Always use this skill when an ATS percentage or application quality assessment is expected.
---

# ATS Score Skill

Reads the candidate's CV and/or cover letter PDFs, extracts their content, compares against a job description, and produces a structured ATS score report with a percentage match and prioritized improvement tips.

---

## Input Sources

The skill reads from files produced by the `cv-template` and `cover-letter` skills. Check these locations first:

```
/mnt/user-data/outputs/cv_output.pdf        ← from cv-template skill
/mnt/user-data/outputs/cover_letter.pdf     ← from cover-letter skill
```

If neither exists, ask the user to provide their CV and/or cover letter (as PDF, text, or paste). The job description must always be provided — ask if not given.

---

## Workflow

### Step 1 — Extract Text from PDFs

Use `pdftotext` for layout-aware extraction:

```bash
pdftotext -layout /mnt/user-data/outputs/cv_output.pdf /tmp/cv_text.txt
pdftotext -layout /mnt/user-data/outputs/cover_letter.pdf /tmp/cl_text.txt
cat /tmp/cv_text.txt
cat /tmp/cl_text.txt
```

If a file doesn't exist, skip it and note which documents are being scored.

### Step 2 — Parse the Job Description

Apply the same extraction logic as the `job-description-parser` skill. From the JD, extract:

```
required_skills    — must-have technical skills and experience
nice_to_have       — preferred but not blocking
keywords_ats       — exact strings ATS systems will scan for (8–25 terms)
seniority_level    — intern / junior / mid / senior / lead / etc.
culture_signals    — values and soft skills explicitly called out
```

### Step 3 — Score Each Document

Score the **CV** and **cover letter** independently, then combine into an overall score.

#### 3a — Keyword Match Rate

For each `keywords_ats` term, check if it appears in the document text (case-insensitive, partial match allowed for compound terms like "Power BI" matching "PowerBI").

```
keyword_score = (matched_keywords / total_keywords) × 100
```

#### 3b — Required Skills Coverage

```
required_score = (matched_required_skills / total_required_skills) × 100
```

#### 3c — Seniority Alignment

Compare the candidate's experience level (inferred from CV: years, job titles, scope) against `seniority_level` from the JD.

- Perfect match → 100
- One level off → 70
- Two+ levels off → 40

#### 3d — Structure & ATS Formatting Signals (CV only)

Check for ATS-hostile patterns that cause parsing failures:
- Standard section headings present (Experience, Education, Skills) → good
- No tables used for core content → good
- No text in headers/footers only → good
- Contact info in body → good
- Dates in consistent format → good

Each present signal adds to a 0–100 sub-score.

#### 3e — Culture & Soft Skills Alignment

Count how many `culture_signals` from the JD appear (by concept, not exact string) across both documents.

```
culture_score = (matched_signals / total_signals) × 100
```

#### 3f — Weighted Overall Score

| Component | Weight | Applies To |
|---|---|---|
| Keyword Match | 35% | CV + Cover Letter |
| Required Skills Coverage | 30% | CV |
| Seniority Alignment | 15% | CV |
| Structure / Formatting | 10% | CV only |
| Culture Alignment | 10% | CV + Cover Letter |

```
overall_score = (keyword × 0.35) + (required × 0.30) + (seniority × 0.15) + (structure × 0.10) + (culture × 0.10)
```

Round to nearest integer. Cap at 98 — a perfect 100 is never realistic; 98 signals top-tier match.

### Step 4 — Generate the Report

Output a clean, structured report directly in the conversation (no separate file needed unless the user asks).

---

## Report Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ATS MATCH REPORT
  Role: [Job Title] @ [Company]
  Documents scored: CV / Cover Letter / Both
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OVERALL SCORE:  XX%   [★★★★☆ visual rating /5]

SCORE BREAKDOWN
  Keyword Match Rate        XX%   (XX/XX keywords matched)
  Required Skills Coverage  XX%   (XX/XX skills present)
  Seniority Alignment       XX%   (candidate: mid / role: mid)
  ATS Structure             XX%
  Culture Alignment         XX%   (XX/XX signals matched)

MATCHED KEYWORDS ✓
  [list each matched keyword]

MISSING KEYWORDS ✗
  [list each keyword not found in the documents]

MISSING REQUIRED SKILLS ✗  ← only if any are absent
  [list skills from JD requirements not found in CV]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  IMPROVEMENT TIPS  (prioritized by impact)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[HIGH IMPACT — do these first]

1. [Specific, actionable tip — name the exact keyword/section to fix]
   → Where to add it: [Experience bullet / Skills section / Summary / Cover Letter]
   → Example: Add "digital transformation" to your Carl Zeiss bullet that describes
     the Power BI dashboard project.

2. [Next tip...]

[MEDIUM IMPACT]

3. [Tip...]

[QUICK WINS — easy to do, small boost]

5. [Tip...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[2–3 sentence honest assessment of the application's strengths and
the single biggest risk factor that could cause an ATS rejection.]
```

---

## Improvement Tip Quality Rules

Every tip must be:

1. **Specific** — name the exact keyword, section, or bullet to change. Never say "add more keywords."
2. **Truthful** — only suggest additions that are supported by the candidate's actual CV. Never suggest inventing experience.
3. **Placed** — tell the candidate exactly where in the document to make the change (which bullet, which section).
4. **Exemplified** — show a concrete before/after or example sentence where helpful.
5. **Prioritized by impact** — tips that fix missing required skills come before tips about nice-to-have keywords.

**Tip categories to cover (in priority order):**
- Missing required skills that appear nowhere in the documents
- High-frequency ATS keywords from the JD not present in either document
- Weak or generic bullets that could be rewritten to include a JD keyword
- Missing quantified results (where the CV has a relevant achievement but no number)
- Culture/soft skills present in the JD but absent from both documents
- Structural issues (e.g., skills buried in bullets instead of a dedicated Skills section)
- Cover letter gaps — important JD themes not addressed in the letter

---

## Scoring Interpretation Guide

| Score | Label | Meaning |
|---|---|---|
| 85–98% | 🟢 Strong Match | Likely to pass ATS; competitive for human review |
| 70–84% | 🟡 Good Match | Will probably pass ATS; some gaps to address |
| 55–69% | 🟠 Partial Match | May pass ATS; several important keywords missing |
| 40–54% | 🔴 Weak Match | High risk of ATS rejection; significant gaps |
| <40% | ⛔ Poor Match | Very likely to be filtered out; major rework needed |

Always show this label next to the score in the report.

---

## Edge Cases

**Only CV provided (no cover letter):** Score CV only, note cover letter is unscored, add tip recommending they create one using the `cover-letter` skill.

**Only cover letter provided:** Score cover letter only, flag that CV scoring is unavailable.

**No documents at all (user pastes raw text):** Treat the pasted content as the CV text and score it. Note that layout/structure scoring is skipped.

**JD is very short (<100 words):** Note the JD is sparse, flag that keyword extraction may be incomplete, proceed with what's available.

**Score inflation warning:** If all required skills are present AND keyword match is >80%, double-check — scan for keyword stuffing patterns (same keyword repeated 3+ times without meaningful context). If detected, cap the score at 75% and add a tip about natural integration.
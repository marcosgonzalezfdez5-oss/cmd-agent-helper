---
name: ats-calculating
description: >
  Use this skill to calculate an ATS (Applicant Tracking System) match score and generate improvement tips for a candidate's application materials against a job description. Trigger whenever the user wants to: score or evaluate a CV against a job, check ATS compatibility, calculate a match percentage, get feedback on how well their CV or cover letter fits a role, or improve their chances of passing ATS screening. Also trigger on phrases like "how well does my CV match", "what's my ATS score", "will I pass the ATS", "score my application", "check my CV against the job", "give me tips to improve my CV", or when the user has already created a CV and/or cover letter and wants to know how strong the application is. Always use this skill when an ATS percentage or application quality assessment is expected.
---

# ATS Score Skill

Scores the candidate's CV against a job description by running `ats-calc.py`.
All computation is done by the script — your job is to extract keywords, run it, and format the report.

---

## Workflow

### Step 1 — Extract Keywords from the JD

Read the job description and produce `ats-calculating/assets/jd_keywords.json` with this exact schema:

```json
{
  "ats_keywords": ["8–25 exact ATS terms the JD uses — tools, technologies, methodologies, domain terms"],
  "required_skills": ["must-have skills and experience explicitly listed as required"],
  "culture_signals": ["soft skills and values explicitly mentioned in the JD"],
  "seniority_score": 85,
  "seniority_note": "one sentence: role level vs candidate level and why you chose this score"
}
```

**`seniority_score` guidance (0–100):**
- Candidate level matches role exactly → 85–95
- One level off (e.g. junior applying to entry-level) → 65–75
- Two+ levels off → 40–55

Save the file before proceeding.

---

### Step 2 — Run the Script

```bash
py ats-calculating/assets/ats-calc.py
```

The script reads `cv-creating/assets/cv.json` + `ats-calculating/assets/jd_keywords.json`
and writes `ats-calculating/assets/scores.json`.

---

### Step 3 — Read the Scores

```bash
cat ats-calculating/assets/scores.json
```

Use the JSON to populate the report. All numbers come from the file — do not recompute.

---

### Step 4 — Generate the Report

Output the report in the conversation using the format below.

---

## Report Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ATS MATCH REPORT
  Role: [Job Title] @ [Company]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OVERALL SCORE:  XX%   [label from table below]

SCORE BREAKDOWN
  Keyword Match Rate        XX%   (XX/XX keywords matched)
  Required Skills Coverage  XX%   (XX/XX skills present)
  Seniority Alignment       XX%
  ATS Structure             XX%
  Culture Alignment         XX%   (XX/XX signals matched)

MATCHED KEYWORDS ✓
  [list each matched keyword]

MISSING KEYWORDS ✗
  [list each keyword not found]

MISSING REQUIRED SKILLS ✗  ← only if any are absent
  [list missing required skills]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  IMPROVEMENT TIPS  (prioritized by impact)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[HIGH IMPACT]
1. [Specific tip — name the exact keyword and section to fix]
   → Where: [Experience bullet / Skills section / Summary / Cover Letter]
   → Example: [concrete before/after]

[MEDIUM IMPACT]
2. [Tip...]

[QUICK WINS]
3. [Tip...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[2–3 sentence honest assessment: strengths and the single biggest ATS risk.]
```

---

## Score Interpretation

| Score  | Label            | Meaning |
|--------|------------------|---------|
| 85–98% | 🟢 Strong Match  | Likely to pass ATS; competitive for human review |
| 70–84% | 🟡 Good Match    | Will probably pass ATS; some gaps to address |
| 55–69% | 🟠 Partial Match | May pass ATS; several important keywords missing |
| 40–54% | 🔴 Weak Match    | High risk of ATS rejection; significant gaps |
| <40%   | ⛔ Poor Match    | Very likely filtered out; major rework needed |

---

## Improvement Tip Rules

Every tip must be:
1. **Specific** — name the exact keyword, section, or bullet to change
2. **Truthful** — only suggest additions supported by the candidate's real CV
3. **Placed** — say exactly where in the document to make the change
4. **Prioritized** — missing required skills before nice-to-have keywords

Tip priority order:
1. Missing required skills
2. High-frequency ATS keywords not present in the CV
3. Weak bullets that could be rewritten to include a JD keyword naturally
4. Missing quantified results where a relevant achievement exists
5. Culture/soft skills in JD but absent from CV

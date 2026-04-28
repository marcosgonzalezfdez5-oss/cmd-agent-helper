#!/usr/bin/env python3
"""
ATS Score Calculator
Reads cv.json + jd_keywords.json, computes all scoring dimensions, writes scores.json.

Usage: py ats-calc.py
"""

import json
import re
from pathlib import Path

BASE         = Path(__file__).parent
CV_PATH      = BASE.parent.parent / "cv-creating" / "assets" / "cv.json"
KEYWORDS_PATH = BASE / "jd_keywords.json"
OUTPUT_PATH  = BASE / "scores.json"

WEIGHTS = {
    "keyword_match":    0.35,
    "required_skills":  0.30,
    "seniority":        0.15,
    "structure":        0.10,
    "culture":          0.10,
}


def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9 ]", " ", text.lower())


def cv_to_text(cv: dict) -> str:
    parts = []
    pi = cv.get("personal_info", {})
    parts.append(pi.get("headline", ""))
    parts.append(pi.get("name", ""))
    parts.append(cv.get("summary", ""))

    for exp in cv.get("experience", []):
        parts.append(exp.get("title", ""))
        parts.append(exp.get("company", ""))
        parts.extend(exp.get("description", []))

    for edu in cv.get("education", []):
        parts.append(edu.get("degree", ""))
        parts.append(edu.get("institution", ""))

    skills = cv.get("skills", {})
    parts.extend(skills.get("tools", []))
    parts.extend(skills.get("programming", []))
    parts.extend(skills.get("soft-skills", []))

    for lang in cv.get("languages", []):
        parts.append(lang.get("language", ""))

    for add in cv.get("additional_experience", []):
        parts.append(add.get("activity", ""))
        parts.append(add.get("description", ""))

    return " ".join(str(p) for p in parts if p)


def match_terms(cv_norm: str, terms: list) -> tuple:
    matched, missing = [], []
    for term in terms:
        if normalize(term) in cv_norm:
            matched.append(term)
        else:
            missing.append(term)
    return matched, missing


def pct(matched: list, total: int) -> float:
    if total == 0:
        return 100.0
    return round(len(matched) / total * 100, 1)


def check_structure(cv: dict) -> tuple:
    checks = {
        "experience section":   bool(cv.get("experience")),
        "education section":    bool(cv.get("education")),
        "skills section":       bool(cv.get("skills")),
        "contact email":        bool(cv.get("personal_info", {}).get("email")),
        "contact phone":        bool(cv.get("personal_info", {}).get("phone")),
        "consistent dates":     True,  # enforced by cv.json schema
    }
    present = [k for k, v in checks.items() if v]
    return round(len(present) / len(checks) * 100, 1), present


def main():
    if not CV_PATH.exists():
        raise FileNotFoundError(f"CV not found: {CV_PATH}")
    if not KEYWORDS_PATH.exists():
        raise FileNotFoundError(
            f"Keywords file not found: {KEYWORDS_PATH}\n"
            "Create jd_keywords.json from the job description first."
        )

    with open(CV_PATH, encoding="utf-8") as f:
        cv = json.load(f)
    with open(KEYWORDS_PATH, encoding="utf-8") as f:
        kw = json.load(f)

    cv_norm = normalize(cv_to_text(cv))

    ats_keywords    = kw.get("ats_keywords", [])
    required_skills = kw.get("required_skills", [])
    culture_signals = kw.get("culture_signals", [])
    seniority_score = float(kw.get("seniority_score", 70))
    seniority_note  = kw.get("seniority_note", "")

    kw_matched,  kw_missing  = match_terms(cv_norm, ats_keywords)
    req_matched, req_missing = match_terms(cv_norm, required_skills)
    cul_matched, cul_missing = match_terms(cv_norm, culture_signals)
    struct_score, struct_ok  = check_structure(cv)

    kw_score  = pct(kw_matched,  len(ats_keywords))
    req_score = pct(req_matched, len(required_skills))
    cul_score = pct(cul_matched, len(culture_signals))

    overall = round(
        kw_score       * WEIGHTS["keyword_match"]
        + req_score    * WEIGHTS["required_skills"]
        + seniority_score * WEIGHTS["seniority"]
        + struct_score * WEIGHTS["structure"]
        + cul_score    * WEIGHTS["culture"]
    )
    overall = min(overall, 98)

    result = {
        "overall": overall,
        "keyword_match": {
            "score":   kw_score,
            "matched": kw_matched,
            "missing": kw_missing,
            "total":   len(ats_keywords),
        },
        "required_skills": {
            "score":   req_score,
            "matched": req_matched,
            "missing": req_missing,
            "total":   len(required_skills),
        },
        "seniority": {
            "score": seniority_score,
            "note":  seniority_note,
        },
        "structure": {
            "score":          struct_score,
            "signals_present": struct_ok,
        },
        "culture": {
            "score":   cul_score,
            "matched": cul_matched,
            "missing": cul_missing,
            "total":   len(culture_signals),
        },
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(f"Overall ATS score: {overall}%")
    print(f"  Keyword match:    {kw_score}%  ({len(kw_matched)}/{len(ats_keywords)})")
    print(f"  Required skills:  {req_score}%  ({len(req_matched)}/{len(required_skills)})")
    print(f"  Seniority:        {seniority_score}%")
    print(f"  Structure:        {struct_score}%")
    print(f"  Culture:          {cul_score}%  ({len(cul_matched)}/{len(culture_signals)})")
    print(f"\nFull results written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()


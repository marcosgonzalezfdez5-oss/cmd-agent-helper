# cmd-agent-helper

**cmd-agent-helper** is a suite of Python-based CLI agents designed to interact with Claude to automate and optimize the job application workflow. From extracting keywords to calculating ATS (Applicant Tracking System) compatibility, this helper acts as a bridge between your professional data and AI-driven career optimization.

## 🚀 Features

The repository is organized into specialized agents, each handling a specific part of the recruitment cycle:

* **ATS Calculating:** Embedded calculations to determine how well your CV matches a specific job description.
* **Keywords Extracting:** Automatically identifies core competencies and required technologies from job postings.
* **CV & Cover Letter Creation:** Tailors your professional documents to highlight the most relevant experience for a given role.
* **Humanizer:** Refines AI-generated text to ensure it maintains a natural, professional tone.

## 📂 Project Structure

```text
├── ats-calculating/      # Tools for scoring CV/JD alignment
├── keywords-extracting/   # NLP scripts to pull requirements from text
├── cv-creating/           # Templates and logic for resume generation
├── cover-letter-creating/ # Automated cover letter drafting
├── humanize/             # Post-processing for natural language
└── outputs/              # Default directory for generated documents
```

## 🛠️ Getting Started

### Prerequisites
* Python 3.x
* Claude API Key (Anthropic)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/marcosgonzalezfdez5-oss/cmd-agent-helper.git
   cd cmd-agent-helper
   ```
2. Install dependencies (if applicable):
   ```bash
   pip install -r requirements.txt
   ```

## 🤖 Usage

Each agent can be run from its respective directory. For example, to run the keyword extractor:
```bash
python keywords-extracting/main.py --input "job_description.txt"
```
*(Note: Replace with your actual entry point commands if they differ.)*

## 📝 Configuration
Refer to `CLAUDE.md` for specific instructions on environment variables and agent-specific prompts.

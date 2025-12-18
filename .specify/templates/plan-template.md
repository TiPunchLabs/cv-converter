# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

**Language/Version**: Python 3.x
**Primary Dependencies**: BeautifulSoup4 4.12.3, python-docx 1.1.0, WeasyPrint, lxml 5.1.0
**Storage**: N/A (file-based input/output)
**Testing**: pytest (if tests are added)
**Target Platform**: Linux, macOS, Windows (CLI)
**Project Type**: Single Python script (CLI tool)
**Performance Goals**: Convert typical CV in < 5 seconds
**Constraints**: No external services required, offline-capable
**Scale/Scope**: Single-user CLI tool, one file at a time

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Simplicité et Efficacité | PASS/FAIL | [Does feature keep CLI simple?] |
| II. Compatibilité ATS | PASS/FAIL | [Does DOCX output remain ATS-compatible?] |
| III. Préservation du Style | PASS/FAIL | [Is visual fidelity maintained?] |
| IV. Support Multilingue | PASS/FAIL | [Are FR/EN both supported correctly?] |
| V. Robustesse | PASS/FAIL | [Are errors handled gracefully?] |

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (if applicable)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
cv-converter/
├── cv_converter.py        # Main script - CVConverter class + CLI
├── requirements.txt       # Python dependencies
├── README.md             # Usage documentation
├── tests/                # Tests directory (if tests added)
│   ├── __init__.py
│   ├── test_converter.py
│   ├── test_pdf_generation.py
│   ├── test_docx_generation.py
│   └── fixtures/         # Sample HTML files for testing
│       ├── sample_fr.html
│       └── sample_en.html
└── terraform/            # Infrastructure (GitHub repo)
```

**Structure Decision**: Single-file Python CLI tool. All conversion logic in `cv_converter.py` with `CVConverter` class. Tests in separate `tests/` directory if needed.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., Adding config file] | [current need] | [why CLI args insufficient] |

## Implementation Approach

### CVConverter Class Structure

The main class handles:
1. **Language detection** - From filename, HTML lang attribute, or content keywords
2. **HTML parsing** - BeautifulSoup extracts sections by CSS classes
3. **PDF generation** - WeasyPrint preserves CSS styling
4. **DOCX generation** - python-docx builds structured document

### Key CSS Classes Expected

| Class | Purpose | Required |
|-------|---------|----------|
| `.header` | CV header with name | Yes |
| `.subtitle` | Job title | Yes |
| `.contact-info` | Contact details | Yes |
| `.section` | Generic section wrapper | Yes |
| `.profile-text` | Professional summary | No |
| `.skills-grid` | Skills container | No |
| `.experience-item` | Work experience entry | No |
| `.education-item` | Education entry | No |
| `.cert-list` | Certifications list | No |
| `.projects-list` | GitHub projects | No |

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| WeasyPrint dependencies | Installation complexity | Document system requirements |
| HTML structure variations | Parsing failures | Graceful handling with warnings |
| Large file processing | Slow performance | N/A for typical CV sizes |

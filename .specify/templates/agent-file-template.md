# CV Converter Development Guidelines

Auto-generated from project analysis. Last updated: 2025-12-18

## Active Technologies

- **Language**: Python 3.10+
- **Package Manager**: uv (pyproject.toml)
- **HTML Parsing**: BeautifulSoup4 4.12.3, lxml 5.1.0
- **PDF Generation**: WeasyPrint (CSS-preserving PDF rendering)
- **DOCX Generation**: python-docx 1.1.0
- **Infrastructure**: Terraform (GitHub repository management)

## Project Structure

```text
cv-converter/
├── pyproject.toml        # Project config & dependencies (uv)
├── uv.lock               # Dependency lockfile (generated)
├── cv_converter.py       # Main conversion script (CLI)
├── README.md             # Usage documentation
├── LICENSE               # Project license
├── .envrc                # Environment configuration
├── .pre-commit-config.yaml
├── .gitignore
├── terraform/            # GitHub repository IaC
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── versions.tf
│   └── terraform.tfvars
├── .claude/              # Claude Code commands
│   └── commands/         # Speckit slash commands
└── .specify/             # Speckit documentation
    ├── memory/
    │   └── constitution.md
    ├── templates/
    │   ├── spec-template.md
    │   ├── plan-template.md
    │   ├── tasks-template.md
    │   ├── checklist-template.md
    │   └── agent-file-template.md
    └── scripts/
        └── bash/
```

## Commands

### Installation with uv

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Install with dev dependencies
uv sync --dev
```

### Running the Converter

```bash
# Basic usage (auto-detect language)
uv run cv_converter.py cv.html

# French CV with custom output names
uv run cv_converter.py cv_fr.html Xavier_GUERET_CV.pdf Xavier_GUERET_CV.docx

# English CV with custom output names
uv run cv_converter.py cv_en.html Xavier_GUERET_Resume.pdf Xavier_GUERET_Resume.docx

# Via entry point
uv run cv-converter cv.html
```

### Development

```bash
# Add a dependency
uv add <package>

# Add a dev dependency
uv add --dev <package>

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov

# Run linter
uv run ruff check

# Run pre-commit hooks
pre-commit install
pre-commit run --all-files
```

### Infrastructure (Terraform)

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

## Code Style

### Python
- **Docstrings**: French, using triple quotes
- **Variables/Functions**: English, snake_case
- **Classes**: English, PascalCase
- **Constants**: English, UPPER_SNAKE_CASE
- **User Messages**: French with emojis for visual feedback
- **Encoding**: UTF-8 throughout
- **Linting**: ruff (configured in pyproject.toml)
- **Testing**: pytest

### HTML CV Structure Expected

The converter expects specific CSS classes in the input HTML:
- `.header` - CV header section
- `.subtitle` - Job title subtitle
- `.contact-info` - Contact information
- `.section` - Generic section container
- `.profile-text` - Professional summary
- `.skills-grid`, `.skill-item`, `.skill-category`, `.skill-list` - Skills section
- `.cert-list` - Certifications list
- `.experience-item`, `.job-title`, `.company-name`, `.date-range`, `.responsibilities`, `.tech-stack` - Experience entries
- `.education-item` - Education entries
- `.projects-list` - GitHub projects section

## Recent Changes

### v1.1.0 (2025-12-18)
- Migration from requirements.txt to pyproject.toml (uv)
- Added ruff for linting
- Added pytest for testing
- Updated documentation for uv workflow

### v1.0.0 (2025-12-18)
- Core HTML to PDF/DOCX conversion functionality
- Bilingual support (FR/EN) with automatic language detection
- ATS-compatible DOCX output with preserved styling
- CSS-preserving PDF generation via WeasyPrint
- Terraform setup for GitHub repository management

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->

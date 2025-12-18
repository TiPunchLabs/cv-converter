```
 ██████╗██╗   ██╗     ██████╗ ██████╗ ███╗   ██╗██╗   ██╗███████╗██████╗ ████████╗███████╗██████╗
██╔════╝██║   ██║    ██╔════╝██╔═══██╗████╗  ██║██║   ██║██╔════╝██╔══██╗╚══██╔══╝██╔════╝██╔══██╗
██║     ██║   ██║    ██║     ██║   ██║██╔██╗ ██║██║   ██║█████╗  ██████╔╝   ██║   █████╗  ██████╔╝
██║     ╚██╗ ██╔╝    ██║     ██║   ██║██║╚██╗██║╚██╗ ██╔╝██╔══╝  ██╔══██╗   ██║   ██╔══╝  ██╔══██╗
╚██████╗ ╚████╔╝     ╚██████╗╚██████╔╝██║ ╚████║ ╚████╔╝ ███████╗██║  ██║   ██║   ███████╗██║  ██║
 ╚═════╝  ╚═══╝       ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
                        HTML → PDF & DOCX | ATS Compatible | FR/EN
```

Convertisseur de CV HTML vers PDF et DOCX avec préservation du design et compatibilité ATS (Applicant Tracking System).

## Fonctionnalités

- **Conversion HTML → PDF** : Préserve fidèlement le style CSS grâce à WeasyPrint
- **Conversion HTML → DOCX** : Structure optimisée pour les systèmes ATS
- **Support multilingue** : Français et Anglais avec détection automatique
- **Nommage intelligent** : Suffixe automatique `_FR` ou `_EN` selon la langue détectée

## Installation

### Prérequis

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) - Gestionnaire de paquets Python

### Installation de uv

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Installation du projet

```bash
# Cloner le projet
git clone https://github.com/xgueret/cv-converter.git
cd cv-converter

# Installer les dépendances avec uv
uv sync
```

### Dépendances système (WeasyPrint)

**Ubuntu/Debian** :
```bash
sudo apt-get install libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0
```

**macOS** :
```bash
brew install pango
```

**Windows** : Voir la [documentation WeasyPrint](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#windows)

## Utilisation

### Templates inclus

Le projet inclut des templates prêts à l'emploi dans le dossier `files/` :

```
files/
├── cv_fr.html         # Template CV français (classique)
├── cv_en.html         # Template CV anglais (classique)
├── cv_fr_design.html  # Template CV français (design moderne)
└── cv_en_design.html  # Template CV anglais (design moderne)
```

| Template | Style | Description |
|----------|-------|-------------|
| `cv_fr.html` / `cv_en.html` | Classique | Design simple, une colonne, optimisé ATS |
| `cv_fr_design.html` / `cv_en_design.html` | Moderne | Design deux colonnes avec sidebar, barres de compétences |

Modifiez ces fichiers avec vos informations personnelles.

### Conversion automatique (recommandé)

Sans argument, le convertisseur cherche automatiquement `cv_fr.html` ou `cv_en.html` dans `files/` :

```bash
uv run cv-converter
```

Les fichiers PDF et DOCX sont générés dans le dossier `output/`.

### :fr: Version française

```bash
uv run cv-converter files/cv_fr.html
```

Avec noms de fichiers personnalisés :

```bash
uv run cv-converter files/cv_fr.html output/mon_cv.pdf output/mon_cv.docx
```

### :gb: Version anglaise

```bash
uv run cv-converter files/cv_en.html
```

Avec noms de fichiers personnalisés :

```bash
uv run cv-converter files/cv_en.html output/my_resume.pdf output/my_resume.docx
```

## Détection de la langue

La langue est détectée automatiquement selon cet ordre de priorité :

1. **Nom du fichier** : `cv_fr.html` → Français, `cv_en.html` → Anglais
2. **Attribut HTML** : `<html lang="fr">` ou `<html lang="en">`
3. **Contenu** : Mots-clés français (Compétences, Expérience) ou anglais (Skills, Experience)
4. **Par défaut** : Français

## Structure HTML attendue

Le convertisseur s'attend à trouver ces classes CSS dans votre fichier HTML :

| Classe | Description | Requis |
|--------|-------------|--------|
| `.header` | En-tête du CV (nom, titre) | Oui |
| `.subtitle` | Sous-titre (poste actuel) | Oui |
| `.contact-info` | Informations de contact | Oui |
| `.section` | Conteneur de section | Oui |
| `.profile-text` | Résumé professionnel | Non |
| `.skills-grid` | Grille de compétences | Non |
| `.skill-item` | Élément de compétence | Non |
| `.cert-list` | Liste des certifications | Non |
| `.experience-item` | Entrée d'expérience | Non |
| `.job-title` | Titre du poste | Non |
| `.company-name` | Nom de l'entreprise | Non |
| `.date-range` | Période | Non |
| `.responsibilities` | Liste des responsabilités | Non |
| `.tech-stack` | Technologies utilisées | Non |
| `.education-item` | Entrée de formation | Non |
| `.projects-list` | Projets GitHub | Non |

## Fichiers générés

Les fichiers sont générés dans le dossier `output/` :

| Entrée | Sortie PDF | Sortie DOCX |
|--------|------------|-------------|
| `files/cv.html` (FR détecté) | `output/cv_FR.pdf` | `output/cv_FR.docx` |
| `files/cv_en.html` | `output/cv_EN.pdf` | `output/cv_EN.docx` |
| `files/cv_fr.html` | `output/cv_FR.pdf` | `output/cv_FR.docx` |

## Dépendances

| Package | Version | Usage |
|---------|---------|-------|
| beautifulsoup4 | >=4.12.3 | Parsing HTML |
| lxml | >=5.1.0 | Parser HTML performant |
| python-docx | >=1.1.0 | Génération DOCX |
| weasyprint | >=62.0 | Génération PDF (CSS) |

## Développement

### Installation des dépendances de dev

```bash
uv sync --dev
```

### Lancer les tests

```bash
uv run pytest
```

### Lancer les tests avec couverture

```bash
uv run pytest --cov
```

## Compatibilité ATS

Le fichier DOCX généré est optimisé pour les systèmes ATS :

- Structure de document claire avec titres hiérarchiques
- Texte extractible et indexable
- Pas d'images bloquant l'extraction de texte
- Mise en forme compatible avec les parseurs automatiques

## Licence

MIT License - Voir le fichier [LICENSE](LICENSE) pour plus de détails.

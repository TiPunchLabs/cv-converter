```
 ██████╗██╗   ██╗     ██████╗ ██████╗ ███╗   ██╗██╗   ██╗███████╗██████╗ ████████╗███████╗██████╗
██╔════╝██║   ██║    ██╔════╝██╔═══██╗████╗  ██║██║   ██║██╔════╝██╔══██╗╚══██╔══╝██╔════╝██╔══██╗
██║     ██║   ██║    ██║     ██║   ██║██╔██╗ ██║██║   ██║█████╗  ██████╔╝   ██║   █████╗  ██████╔╝
██║     ╚██╗ ██╔╝    ██║     ██║   ██║██║╚██╗██║╚██╗ ██╔╝██╔══╝  ██╔══██╗   ██║   ██╔══╝  ██╔══██╗
╚██████╗ ╚████╔╝     ╚██████╗╚██████╔╝██║ ╚████║ ╚████╔╝ ███████╗██║  ██║   ██║   ███████╗██║  ██║
 ╚═════╝  ╚═══╝       ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
                             HTML → PDF | ATS Compatible | FR/EN
```

Convertisseur de CV HTML vers PDF avec préservation du design et compatibilité ATS (Applicant Tracking System).

## Fonctionnalités

- **Conversion HTML → PDF** : Rendu fidèle du CSS via Playwright (Chromium headless)
- **Support multilingue** : Français et Anglais avec détection automatique
- **Nommage intelligent** : Suffixe automatique `-FR` ou `-EN` selon la langue détectée

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

### Navigateur Playwright

Le rendu PDF s'appuie sur Chromium, à installer une fois après `uv sync` :

```bash
uv run playwright install --with-deps chromium
```

## Utilisation

### Templates inclus

Le projet inclut deux templates anonymisés dans le dossier `files/` :

```
files/
├── template-fr.html   # Template CV français
└── template-en.html   # Template CV anglais
```

| Template | Description |
|----------|-------------|
| `template-fr.html` / `template-en.html` | Deux colonnes avec sidebar, section « expériences détaillées », optimisé ATS |

Copiez un template sous un autre nom, puis remplissez-le avec vos informations :

```bash
cp files/template-fr.html files/mon-cv-fr.html
```

> **Vos CV ne sont pas versionnés.** Le `.gitignore` exclut tout `files/*.html` ainsi que
> `files/archive/`, à la seule exception de `files/template-*.html`. Vos données
> personnelles ne partent donc jamais sur le dépôt distant.

### Conversion automatique (recommandé)

Sans argument, le convertisseur cherche un CV dans `files/`, en préférant la version française :

```bash
uv run cv-converter
```

Les fichiers PDF sont générés dans le dossier `output/`.

### :fr: Version française

```bash
uv run cv-converter files/mon-cv-fr.html
```

Avec un nom de fichier de sortie personnalisé :

```bash
uv run cv-converter files/mon-cv-fr.html output/mon-cv.pdf
```

### :gb: Version anglaise

```bash
uv run cv-converter files/mon-cv-en.html
```

Avec un nom de fichier de sortie personnalisé :

```bash
uv run cv-converter files/mon-cv-en.html output/my-resume.pdf
```

## Détection de la langue

La langue est détectée automatiquement selon cet ordre de priorité :

1. **Nom du fichier** : marqueur `fr` ou `en` séparé par `-`, `_` ou un espace
   (`mon-cv-fr.html`, `cv_en.html`, `cv en.html`)
2. **Attribut HTML** : `<html lang="fr">` ou `<html lang="en">`
3. **Contenu** : Mots-clés français (Compétences, Expérience) ou anglais (Skills, Experience)
4. **Par défaut** : Français

## Fichiers générés

Les fichiers sont générés dans le dossier `output/` :

Le nom de sortie est normalisé en kebab-case, le marqueur de langue final est
remplacé par un suffixe `-FR` ou `-EN` :

| Entrée | Sortie PDF |
|--------|------------|
| `files/template-fr.html` | `output/template-FR.pdf` |
| `files/mon_cv_en.html` | `output/mon-cv-EN.pdf` |
| `files/cv.html` (FR détecté au contenu) | `output/cv-FR.pdf` |

## Dépendances

| Package | Version | Usage |
|---------|---------|-------|
| beautifulsoup4 | >=4.12.3 | Parsing HTML |
| lxml | >=5.1.0 | Parser HTML performant |
| playwright | >=1.40.0 | Génération PDF (Chromium headless) |

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

Le PDF généré est optimisé pour les systèmes ATS :

- Structure de document claire avec titres hiérarchiques
- Texte extractible et indexable
- Pas d'images bloquant l'extraction de texte
- Mise en forme compatible avec les parseurs automatiques

### Analyse ATS de votre CV

Un prompt d'analyse ATS est disponible dans [`docs/ats-analysis-prompt.md`](docs/ats-analysis-prompt.md). Utilisez-le avec un LLM (ChatGPT, Claude, etc.) pour :

- Obtenir un score de compatibilité ATS
- Identifier les mots-clés manquants
- Detecter les risques de filtrage
- Recevoir des recommandations d'amelioration

## Licence

MIT License - Voir le fichier [LICENSE](LICENSE) pour plus de détails.

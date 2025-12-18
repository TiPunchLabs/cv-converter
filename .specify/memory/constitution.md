# CV Converter Constitution

## Core Principles

### I. Simplicité et Efficacité
Le projet doit rester un outil en ligne de commande simple et efficace. Toute fonctionnalité ajoutée doit servir directement l'objectif principal : convertir des CV HTML en formats PDF et DOCX de haute qualité.

### II. Compatibilité ATS
Les fichiers générés (particulièrement DOCX) doivent être optimisés pour les systèmes de suivi de candidatures (Applicant Tracking Systems). La structure du document doit être lisible par les parseurs automatiques.

### III. Préservation du Style
Le design visuel du CV HTML source doit être préservé autant que possible dans les formats de sortie. Le PDF doit être visuellement identique à l'original, le DOCX doit maintenir la hiérarchie et le style.

### IV. Support Multilingue
Le système doit supporter nativement le français et l'anglais avec détection automatique de la langue. Les traductions des sections doivent être cohérentes et professionnelles.

### V. Robustesse
Le convertisseur doit gérer gracieusement les erreurs (fichiers manquants, HTML malformé, etc.) avec des messages clairs et utiles pour l'utilisateur.

## Contraintes Techniques

### Stack Technologique
- **Langage** : Python 3.10+
- **Gestionnaire de paquets** : uv (pyproject.toml)
- **Parsing HTML** : BeautifulSoup4 + lxml
- **Génération PDF** : WeasyPrint (préserve le CSS)
- **Génération DOCX** : python-docx
- **Aucune dépendance externe** : pas de navigateur headless, pas de service cloud

### Gestion des dépendances avec uv

```bash
# Installation des dépendances
uv sync

# Installation avec dépendances de dev
uv sync --dev

# Exécution du script
uv run cv_converter.py <fichier.html>

# Ajout d'une dépendance
uv add <package>

# Ajout d'une dépendance de dev
uv add --dev <package>
```

### Structure du projet

```
cv-converter/
├── pyproject.toml      # Configuration projet et dépendances (uv)
├── uv.lock             # Lockfile des dépendances (généré)
├── cv_converter.py     # Script principal
├── README.md           # Documentation
├── LICENSE             # Licence MIT
├── files/              # Templates HTML et CV sources
│   ├── cv_fr.html          # Template CV français (classique)
│   ├── cv_en.html          # Template CV anglais (classique)
│   ├── cv_fr_design.html   # Template CV français (design moderne)
│   └── cv_en_design.html   # Template CV anglais (design moderne)
├── output/             # Fichiers générés (PDF/DOCX) - ignoré par git
└── .specify/           # Documentation Speckit
```

### Templates HTML

Le projet propose deux styles de templates :

| Style | Fichiers | Description |
|-------|----------|-------------|
| Classique | `cv_fr.html`, `cv_en.html` | Design une colonne, optimisé ATS |
| Moderne | `cv_fr_design.html`, `cv_en_design.html` | Design deux colonnes avec sidebar |

Le convertisseur supporte automatiquement les deux formats de templates.

### Conventions de Code
- Code documenté en français (commentaires, docstrings)
- Noms de variables et fonctions en anglais (snake_case)
- Messages utilisateur en français avec emojis pour la clarté
- Tests unitaires avec pytest (`uv run pytest`)
- Linting avec ruff (`uv run ruff check`)

### Structure des Fichiers de Sortie
- Fichiers générés dans le dossier `output/` (créé automatiquement)
- Suffixe automatique selon la langue : `_FR.pdf`, `_EN.pdf`
- Nommage cohérent entre PDF et DOCX
- Suppression des suffixes de langue du fichier source avant génération
- Le dossier `output/` est ignoré par git

## Workflow de Développement

### Modification du Code
1. Tester sur au moins un CV en français et un en anglais
2. Vérifier la compatibilité ATS du DOCX généré
3. S'assurer que le PDF est visuellement correct
4. Lancer les tests : `uv run pytest`
5. Vérifier le linting : `uv run ruff check`

### Ajout de Fonctionnalités
1. La fonctionnalité doit être justifiée par un cas d'usage réel
2. Elle ne doit pas complexifier l'interface CLI de base
3. Préférer les arguments optionnels aux changements de comportement par défaut
4. Ajouter les tests correspondants

### Ajout de Dépendances
1. Utiliser `uv add <package>` pour les dépendances runtime
2. Utiliser `uv add --dev <package>` pour les dépendances de développement
3. Justifier l'ajout dans le message de commit
4. Éviter les dépendances lourdes ou avec beaucoup de sous-dépendances

## Governance

Cette constitution définit les principes directeurs du projet CV Converter. Toute modification significative de l'architecture ou des fonctionnalités doit respecter ces principes.

**Version**: 1.2.0 | **Ratified**: 2025-12-18 | **Last Amended**: 2025-12-18

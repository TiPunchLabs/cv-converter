# cv-converter

cv converter html to pdf and word

## Infrastructure

Ce projet utilise Terraform pour gérer le dépôt GitHub.

### Prérequis

- [Terraform](https://www.terraform.io/) >= 1.0
- Un token GitHub avec les permissions nécessaires

- [direnv](https://direnv.net/) pour la gestion des variables d'environnement
- [pass](https://www.passwordstore.org/) pour le stockage sécurisé du token


### Configuration


1. Initialiser Terraform :
   ```bash
   cd terraform
   terraform init
   ```


### Déploiement

```bash
cd terraform
terraform plan
terraform apply
```

## Pre-commit

Ce projet utilise [pre-commit](https://pre-commit.com/) pour maintenir la qualité du code.

### Installation

```bash
# Installer pre-commit
pip install pre-commit

# Installer les hooks
pre-commit install
```

### Utilisation

Les hooks s'exécutent automatiquement avant chaque commit. Pour les exécuter manuellement :

```bash
# Sur tous les fichiers
pre-commit run --all-files

# Sur les fichiers stagés uniquement
pre-commit run
```

## Licence

MIT

#!/usr/bin/env python3
"""
Convertisseur de CV HTML vers PDF
Préserve le design et la compatibilité ATS
Support multilingue : FR / EN
"""

import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


class CVConverter:
    """Convertit un CV HTML en PDF avec préservation du style"""

    # Dictionnaire de traduction des sections
    TRANSLATIONS = {
        "fr": {
            "profil": "PROFIL PROFESSIONNEL",
            "skills": "COMPÉTENCES TECHNIQUES",
            "certs": "CERTIFICATIONS PROFESSIONNELLES",
            "experience": "EXPÉRIENCE PROFESSIONNELLE",
            "education": "FORMATION",
            "projects": "PROJETS GITHUB",
        },
        "en": {
            "profil": "PROFESSIONAL PROFILE",
            "skills": "TECHNICAL SKILLS",
            "certs": "PROFESSIONAL CERTIFICATIONS",
            "experience": "PROFESSIONAL EXPERIENCE",
            "education": "EDUCATION",
            "projects": "GITHUB PROJECTS",
        },
    }

    def __init__(self, html_file):
        self.html_file = Path(html_file)
        if not self.html_file.exists():
            raise FileNotFoundError(f"Fichier non trouvé: {self.html_file}")

        raw = self.html_file.read_text(encoding="utf-8")
        self.language = self._detect_language(raw)
        self.html_content = self._deobfuscate_cf_email(raw)
        self.soup = BeautifulSoup(self.html_content, "lxml")

        lang_display = "🇬🇧 Anglais" if self.language == "en" else "🇫🇷 Français"
        print(f"✓ Fichier HTML chargé: {self.html_file}")
        print(f"✓ Langue détectée: {lang_display}")

    def _detect_language(self, content):
        """Détecte la langue du fichier HTML"""
        filename = self.html_file.stem.lower()

        # Détection par nom de fichier (accepte -fr, _fr, espace fr en fin ou au milieu)
        match = re.search(r"[-_\s](fr|en)(?:[-_\s]|$)", filename)
        if match:
            return match.group(1)

        # Cherche <html lang="xx">
        match = re.search(r'<html[^>]+lang=["\'](\w+)["\']', content)
        if match:
            lang = match.group(1).lower()
            if lang.startswith("en"):
                return "en"
            elif lang.startswith("fr"):
                return "fr"

        # Cherche des mots-clés français dans le contenu
        if any(word in content for word in ["Compétences", "Expérience", "Formation"]):
            return "fr"
        elif any(word in content for word in ["Skills", "Experience", "Education"]):
            return "en"

        # Par défaut, français
        return "fr"

    @staticmethod
    def _deobfuscate_cf_email(html: str) -> str:
        """Decode Cloudflare email-obfuscated spans (headless browsers don't run CF's JS)."""

        def _decode(match: re.Match) -> str:
            data = bytes.fromhex(match.group(1))
            key = data[0]
            return bytes(b ^ key for b in data[1:]).decode()

        return re.sub(
            r'<a[^>]+class="__cf_email__"[^>]+data-cfemail="([0-9a-f]+)"[^>]*>\[email[^<]*\]</a>',
            _decode,
            html,
        )

    def _build_output_path(self, extension: str) -> Path:
        """Construit le chemin de sortie avec suffixe de langue, normalisé en kebab-case"""
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)
        stem = re.sub(r"[-_\s]+(fr|en)$", "", self.html_file.stem, flags=re.IGNORECASE)
        stem = re.sub(r"[-_\s]+", "-", stem).strip("-")
        suffix = "EN" if self.language == "en" else "FR"
        return output_dir / f"{stem}-{suffix}.{extension}"

    def generate_pdf(self, output_path=None):
        """Génère le PDF via Playwright (headless Chromium) pour un rendu fidèle"""
        if output_path is None:
            output_path = self._build_output_path("pdf")

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                try:
                    page = browser.new_page()
                    page.set_content(self.html_content, wait_until="networkidle")
                    page.pdf(
                        path=str(output_path),
                        format="A4",
                        margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
                        print_background=True,
                    )
                finally:
                    browser.close()

            print(f"✓ PDF généré: {output_path}")
            return output_path

        except Exception as e:
            print(f"✗ Erreur lors de la génération PDF: {e}")
            raise

    def convert_all(self, pdf_path=None):
        """Convertit le CV en PDF"""
        lang_flag = "🇬🇧" if self.language == "en" else "🇫🇷"
        print(f"\n🔄 Début de la conversion ({lang_flag})...\n")

        pdf_file = self.generate_pdf(pdf_path)

        print("\n✅ Conversion terminée avec succès!")
        print(f"   📄 PDF:  {pdf_file}")

        return pdf_file


BANNER = """
 ██████╗██╗   ██╗     ██████╗ ██████╗ ███╗   ██╗██╗   ██╗███████╗██████╗ ████████╗███████╗██████╗
██╔════╝██║   ██║    ██╔════╝██╔═══██╗████╗  ██║██║   ██║██╔════╝██╔══██╗╚══██╔══╝██╔════╝██╔══██╗
██║     ██║   ██║    ██║     ██║   ██║██╔██╗ ██║██║   ██║█████╗  ██████╔╝   ██║   █████╗  ██████╔╝
██║     ╚██╗ ██╔╝    ██║     ██║   ██║██║╚██╗██║╚██╗ ██╔╝██╔══╝  ██╔══██╗   ██║   ██╔══╝  ██╔══██╗
╚██████╗ ╚████╔╝     ╚██████╗╚██████╔╝██║ ╚████║ ╚████╔╝ ███████╗██║  ██║   ██║   ███████╗██║  ██║
 ╚═════╝  ╚═══╝       ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
                             HTML → PDF | ATS Compatible | FR/EN
"""


DEFAULT_FILES_DIR = Path(__file__).parent / "files"
DEFAULT_OUTPUT_DIR = Path(__file__).parent / "output"


def find_default_cv():
    """Cherche un CV dans le dossier files/, en préférant la version française"""
    if not DEFAULT_FILES_DIR.exists():
        return None

    candidates = sorted(f for f in DEFAULT_FILES_DIR.glob("*.html") if f.is_file())
    if not candidates:
        return None

    for cv_file in candidates:
        if re.search(r"[-_\s]fr(?:[-_\s]|$)", cv_file.stem, flags=re.IGNORECASE):
            return cv_file

    return candidates[0]


def print_help():
    """Affiche l'aide avec le banner"""
    print(BANNER)
    print("Usage: cv-converter [fichier_html] [pdf_output]")
    print("\nSi aucun fichier n'est spécifié, cherche automatiquement")
    print("un CV dans le dossier files/")
    print("\nLes fichiers générés sont placés dans le dossier output/")
    print("\nExemples:")
    print("  cv-converter                                              # Auto-détection")
    print("  cv-converter files/cv-xavier-gueret-en.html")
    print("  cv-converter files/cv-xavier-gueret-fr.html output/mon_cv.pdf")
    print("\nDétection automatique de la langue:")
    print("  - Par nom de fichier: cv_en.html → Anglais, cv_fr.html → Français")
    print("  - Par attribut HTML: <html lang='en'> ou <html lang='fr'>")
    print("  - Par défaut: Français")


def main():
    """Point d'entrée du script"""
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print_help()
        sys.exit(0)

    # Déterminer le fichier HTML à utiliser
    if len(sys.argv) >= 2:
        html_file = sys.argv[1]
    else:
        # Recherche automatique dans files/
        html_file = find_default_cv()
        if html_file is None:
            print(BANNER)
            print("❌ Aucun fichier CV trouvé!")
            print("\n   Placez votre fichier HTML dans le dossier files/")
            print(f"   Dossier inspecté: {DEFAULT_FILES_DIR}")
            print("\n   Ou spécifiez un fichier: cv-converter <fichier.html>")
            sys.exit(1)
        print(f"📂 Fichier détecté automatiquement: {html_file}")

    pdf_output = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        converter = CVConverter(html_file)
        converter.convert_all(pdf_output)

    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

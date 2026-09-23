"""Tests pour le convertisseur de CV"""

import re
from pathlib import Path

import pytest

from cv_converter import CVConverter, find_default_cv


class TestLanguageDetection:
    """Tests pour la détection de langue"""

    def test_detect_french_from_filename(self, tmp_path):
        """Détecte le français depuis le nom de fichier"""
        html_file = tmp_path / "cv_fr.html"
        html_file.write_text("<html><body></body></html>")
        converter = CVConverter(html_file)
        assert converter.language == "fr"

    def test_detect_english_from_filename(self, tmp_path):
        """Détecte l'anglais depuis le nom de fichier"""
        html_file = tmp_path / "cv_en.html"
        html_file.write_text("<html><body></body></html>")
        converter = CVConverter(html_file)
        assert converter.language == "en"

    def test_detect_french_from_html_lang(self, tmp_path):
        """Détecte le français depuis l'attribut lang"""
        html_file = tmp_path / "cv.html"
        html_file.write_text('<html lang="fr"><body></body></html>')
        converter = CVConverter(html_file)
        assert converter.language == "fr"

    def test_detect_english_from_html_lang(self, tmp_path):
        """Détecte l'anglais depuis l'attribut lang"""
        html_file = tmp_path / "cv.html"
        html_file.write_text('<html lang="en"><body></body></html>')
        converter = CVConverter(html_file)
        assert converter.language == "en"

    def test_detect_french_from_content(self, tmp_path):
        """Détecte le français depuis le contenu"""
        html_file = tmp_path / "cv.html"
        html_file.write_text("<html><body>Compétences techniques</body></html>")
        converter = CVConverter(html_file)
        assert converter.language == "fr"

    def test_detect_english_from_content(self, tmp_path):
        """Détecte l'anglais depuis le contenu"""
        html_file = tmp_path / "cv.html"
        html_file.write_text("<html><body>Skills and Experience</body></html>")
        converter = CVConverter(html_file)
        assert converter.language == "en"

    def test_default_to_french(self, tmp_path):
        """Par défaut, retourne français"""
        html_file = tmp_path / "cv.html"
        html_file.write_text("<html><body>Hello World</body></html>")
        converter = CVConverter(html_file)
        assert converter.language == "fr"


class TestOutputPath:
    """Tests pour le chemin de sortie (normalisation kebab-case)"""

    def test_french_suffix(self, tmp_path):
        """Suffixe -FR pour le français"""
        html_file = tmp_path / "cv_fr.html"
        html_file.write_text("<html><body></body></html>")
        converter = CVConverter(html_file)
        assert converter._build_output_path("pdf").stem == "cv-FR"

    def test_english_suffix(self, tmp_path):
        """Suffixe -EN pour l'anglais"""
        html_file = tmp_path / "cv_en.html"
        html_file.write_text("<html><body></body></html>")
        converter = CVConverter(html_file)
        assert converter._build_output_path("pdf").stem == "cv-EN"

    def test_dash_separator_preserved(self, tmp_path):
        """Nom avec tirets reste avec tirets"""
        html_file = tmp_path / "cv-xavier-gueret-fr.html"
        html_file.write_text("<html><body></body></html>")
        converter = CVConverter(html_file)
        assert converter._build_output_path("pdf").stem == "cv-xavier-gueret-FR"

    def test_underscores_normalized_to_dashes(self, tmp_path):
        """Les underscores sont convertis en tirets"""
        html_file = tmp_path / "cv_xavier_gueret_fr.html"
        html_file.write_text("<html><body></body></html>")
        converter = CVConverter(html_file)
        assert converter._build_output_path("pdf").stem == "cv-xavier-gueret-FR"

    def test_mixed_separators_normalized(self, tmp_path):
        """Nom mixte (- et _) normalisé en tirets uniquement"""
        html_file = tmp_path / "cv-xavier_gueret-fr.html"
        html_file.write_text("<html><body></body></html>")
        converter = CVConverter(html_file)
        assert converter._build_output_path("pdf").stem == "cv-xavier-gueret-FR"

    def test_spaces_normalized_to_dashes(self, tmp_path):
        """Les espaces sont convertis en tirets"""
        html_file = tmp_path / "cv xavier gueret en.html"
        html_file.write_text("<html><body></body></html>")
        converter = CVConverter(html_file)
        assert converter._build_output_path("pdf").stem == "cv-xavier-gueret-EN"

    def test_no_language_suffix_in_filename(self, tmp_path):
        """Stem sans suffixe langue : le suffixe est ajouté via la détection HTML"""
        html_file = tmp_path / "mon_cv.html"
        html_file.write_text('<html lang="en"><body></body></html>')
        converter = CVConverter(html_file)
        assert converter._build_output_path("pdf").stem == "mon-cv-EN"


class TestFileNotFound:
    """Tests pour les erreurs de fichier"""

    def test_file_not_found(self):
        """Lève une erreur si le fichier n'existe pas"""
        with pytest.raises(FileNotFoundError):
            CVConverter("/nonexistent/path/cv.html")


class TestFindDefaultCV:
    """Tests pour find_default_cv"""

    def test_returns_none_if_no_files_dir(self, monkeypatch):
        """Retourne None si le dossier files n'existe pas"""
        import cv_converter

        monkeypatch.setattr(cv_converter, "DEFAULT_FILES_DIR", Path("/nonexistent"))
        assert find_default_cv() is None


class TestTemplatePrintFidelity:
    """Tests garantissant que les templates rendent à l'identique en PDF"""

    TEMPLATES_DIR = Path(__file__).parent.parent / "files"

    @staticmethod
    def _templates():
        """Retourne les templates HTML livrés avec le projet"""
        return sorted(TestTemplatePrintFidelity.TEMPLATES_DIR.glob("*.html"))

    def test_templates_exist(self):
        """Le projet livre au moins un template"""
        assert self._templates()

    def test_width_breakpoints_are_scoped_to_screen(self):
        """Chromium compose le PDF à la largeur du papier (A4 = 794px CSS).

        Une media query `max-width` non restreinte à `screen` s'applique donc
        aussi à l'impression et fait s'effondrer la mise en page du modèle.
        """
        offenders = []
        for template in self._templates():
            css = template.read_text(encoding="utf-8")
            for query in re.findall(r"@media([^{]+)\{", css):
                if "max-width" in query and "screen" not in query:
                    offenders.append(f"{template.name}: @media{query.strip()}")

        assert not offenders, (
            "media query `max-width` non restreinte à `screen` — "
            f"elle s'appliquera au PDF: {offenders}"
        )

"""Tests pour le convertisseur de CV"""

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


class TestOutputSuffix:
    """Tests pour le suffixe de sortie"""

    def test_french_suffix(self, tmp_path):
        """Suffixe _FR pour le français"""
        html_file = tmp_path / "cv_fr.html"
        html_file.write_text("<html><body></body></html>")
        converter = CVConverter(html_file)
        assert converter._get_output_suffix() == "_FR"

    def test_english_suffix(self, tmp_path):
        """Suffixe _EN pour l'anglais"""
        html_file = tmp_path / "cv_en.html"
        html_file.write_text("<html><body></body></html>")
        converter = CVConverter(html_file)
        assert converter._get_output_suffix() == "_EN"


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

#!/usr/bin/env python3
"""
Convertisseur de CV HTML vers PDF et DOCX
Préserve le design et la compatibilité ATS
Support multilingue : FR / EN
"""

import os
import sys
import re
from pathlib import Path
from bs4 import BeautifulSoup
from weasyprint import HTML, CSS
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


class CVConverter:
    """Convertit un CV HTML en PDF et DOCX avec préservation du style"""
    
    # Dictionnaire de traduction des sections
    TRANSLATIONS = {
        'fr': {
            'profil': 'PROFIL PROFESSIONNEL',
            'skills': 'COMPÉTENCES TECHNIQUES',
            'certs': 'CERTIFICATIONS PROFESSIONNELLES',
            'experience': 'EXPÉRIENCE PROFESSIONNELLE',
            'education': 'FORMATION',
            'projects': 'PROJETS GITHUB'
        },
        'en': {
            'profil': 'PROFESSIONAL PROFILE',
            'skills': 'TECHNICAL SKILLS',
            'certs': 'PROFESSIONAL CERTIFICATIONS',
            'experience': 'PROFESSIONAL EXPERIENCE',
            'education': 'EDUCATION',
            'projects': 'GITHUB PROJECTS'
        }
    }
    
    def __init__(self, html_file):
        self.html_file = Path(html_file)
        self.soup = None
        self.language = self._detect_language()
        self.load_html()
        
    def _detect_language(self):
        """Détecte la langue du fichier HTML"""
        filename = self.html_file.stem.lower()
        
        # Détection par nom de fichier
        if '_en' in filename or filename.endswith('_en'):
            return 'en'
        elif '_fr' in filename or filename.endswith('_fr'):
            return 'fr'
        
        # Détection par attribut lang si le fichier existe
        if self.html_file.exists():
            with open(self.html_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Cherche <html lang="xx">
                match = re.search(r'<html[^>]+lang=["\'](\w+)["\']', content)
                if match:
                    lang = match.group(1).lower()
                    if lang.startswith('en'):
                        return 'en'
                    elif lang.startswith('fr'):
                        return 'fr'
                
                # Cherche des mots-clés français dans le contenu
                if any(word in content for word in ['Compétences', 'Expérience', 'Formation']):
                    return 'fr'
                elif any(word in content for word in ['Skills', 'Experience', 'Education']):
                    return 'en'
        
        # Par défaut, français
        return 'fr'
    
    def load_html(self):
        """Charge et parse le fichier HTML"""
        if not self.html_file.exists():
            raise FileNotFoundError(f"Fichier non trouvé: {self.html_file}")
        
        with open(self.html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        self.html_content = content
        self.soup = BeautifulSoup(content, 'html.parser')
        
        lang_display = "🇬🇧 Anglais" if self.language == 'en' else "🇫🇷 Français"
        print(f"✓ Fichier HTML chargé: {self.html_file}")
        print(f"✓ Langue détectée: {lang_display}")
    
    def _get_output_suffix(self):
        """Retourne le suffixe pour les fichiers de sortie"""
        return '_EN' if self.language == 'en' else '_FR'
    
    def _get_output_dir(self):
        """Retourne le dossier de sortie, le cree si necessaire"""
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)
        return output_dir

    def generate_pdf(self, output_path=None):
        """Génère le PDF en préservant le CSS avec la bonne échelle"""
        if output_path is None:
            # Ajoute le suffixe de langue
            stem = self.html_file.stem
            # Enlève les suffixes existants
            stem = re.sub(r'_(fr|en)$', '', stem, flags=re.IGNORECASE)
            output_path = self._get_output_dir() / f"{stem}{self._get_output_suffix()}.pdf"
        
        try:
            # CSS additionnel pour corriger le zoom et l'impression
            additional_css = CSS(string='''
                @page {
                    size: A4;
                    margin: 0;
                }
                body {
                    margin: 0;
                    padding: 0;
                    zoom: 1;
                    -webkit-print-color-adjust: exact;
                    print-color-adjust: exact;
                }
                .print-button {
                    display: none !important;
                }
            ''')
            
            # Lit le HTML avec les styles
            html_content = HTML(string=self.html_content, base_url=str(self.html_file.parent))
            
            # Génère le PDF avec le CSS additionnel
            html_content.write_pdf(output_path, stylesheets=[additional_css])
            
            print(f"✓ PDF généré: {output_path}")
            return output_path
        
        except Exception as e:
            print(f"✗ Erreur lors de la génération PDF: {e}")
            raise
    
    def generate_docx(self, output_path=None):
        """Génère le DOCX en préservant la structure et le style"""
        if output_path is None:
            # Ajoute le suffixe de langue
            stem = self.html_file.stem
            # Enlève les suffixes existants
            stem = re.sub(r'_(fr|en)$', '', stem, flags=re.IGNORECASE)
            output_path = self._get_output_dir() / f"{stem}{self._get_output_suffix()}.docx"
        
        try:
            doc = Document()
            
            # Configuration des marges
            sections = doc.sections
            for section in sections:
                section.top_margin = Inches(0.5)
                section.bottom_margin = Inches(0.5)
                section.left_margin = Inches(0.7)
                section.right_margin = Inches(0.7)
            
            # Extraction du contenu
            self._add_header(doc)
            self._add_profile(doc)
            self._add_skills(doc)
            self._add_certifications(doc)
            self._add_experience(doc)
            self._add_education(doc)
            self._add_projects(doc)
            
            # Sauvegarde
            doc.save(output_path)
            print(f"✓ DOCX généré: {output_path}")
            return output_path
        
        except Exception as e:
            print(f"✗ Erreur lors de la génération DOCX: {e}")
            raise
    
    def _add_header(self, doc):
        """Ajoute l'en-tête avec fond coloré"""
        header = self.soup.find('div', class_='header')
        if not header:
            return

        # Nom
        h1 = header.find('h1')
        if h1:
            name = h1.text.strip()
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(name)
            run.font.size = Pt(24)
            run.font.bold = True
            run.font.color.rgb = RGBColor(30, 64, 175)

        # Sous-titre
        subtitle_div = header.find('div', class_='subtitle')
        if subtitle_div:
            subtitle = subtitle_div.text.strip()
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(subtitle)
            run.font.size = Pt(12)
            run.font.color.rgb = RGBColor(59, 130, 246)

        # Contact - cherche d'abord dans header, sinon dans tout le document
        contact_div = header.find('div', class_='contact-info')
        if not contact_div:
            # Template design: contact-info est dans une section separee
            contact_div = self.soup.find('div', class_='contact-info')

        if contact_div:
            contact = contact_div.get_text(separator=' | ', strip=True)
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(contact)
            run.font.size = Pt(10)

        # Ligne de séparation
        self._add_horizontal_line(doc)
        doc.add_paragraph()
    
    def _add_profile(self, doc):
        """Ajoute le profil professionnel"""
        # Cherche le profil dans tout le document
        profile_text = self.soup.find('p', class_='profile-text')
        if profile_text:
            self._add_section_title(doc, self.TRANSLATIONS[self.language]['profil'])
            p = doc.add_paragraph(profile_text.text.strip())
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            for run in p.runs:
                run.font.size = Pt(10)
            doc.add_paragraph()
    
    def _add_skills(self, doc):
        """Ajoute les compétences techniques"""
        skills_added = False

        # Format classique: skills-grid avec skill-item
        skills_grid = self.soup.find('div', class_='skills-grid')
        if skills_grid:
            self._add_section_title(doc, self.TRANSLATIONS[self.language]['skills'])
            for skill_item in skills_grid.find_all('div', class_='skill-item'):
                category = skill_item.find('span', class_='skill-category')
                skill_list = skill_item.find('span', class_='skill-list')

                if category and skill_list:
                    p = doc.add_paragraph()
                    run = p.add_run(category.text.strip() + ": ")
                    run.font.bold = True
                    run.font.size = Pt(10)
                    run.font.color.rgb = RGBColor(30, 64, 175)
                    run = p.add_run(skill_list.text.strip())
                    run.font.size = Pt(10)
            skills_added = True

        # Format design: skill-bar-container dans la sidebar
        if not skills_added:
            skill_bars = self.soup.find_all('div', class_='skill-bar-container')
            if skill_bars:
                self._add_section_title(doc, self.TRANSLATIONS[self.language]['skills'])
                for skill_bar in skill_bars:
                    label = skill_bar.find('div', class_='skill-bar-label')
                    if label:
                        spans = label.find_all('span')
                        if len(spans) >= 2:
                            skill_name = spans[0].text.strip()
                            skill_level = spans[1].text.strip()
                            p = doc.add_paragraph()
                            run = p.add_run(f"{skill_name}: ")
                            run.font.bold = True
                            run.font.size = Pt(10)
                            run.font.color.rgb = RGBColor(30, 64, 175)
                            run = p.add_run(skill_level)
                            run.font.size = Pt(10)
                skills_added = True

        if skills_added:
            doc.add_paragraph()
    
    def _add_certifications(self, doc):
        """Ajoute les certifications"""
        cert_list = self.soup.find('ul', class_='cert-list')
        if cert_list:
            self._add_section_title(doc, self.TRANSLATIONS[self.language]['certs'])
            for cert in cert_list.find_all('li'):
                text = cert.get_text(strip=True)
                # Evite de doubler le checkmark si deja present
                if not text.startswith('✓'):
                    text = "✓ " + text
                p = doc.add_paragraph(style='List Bullet')
                run = p.add_run(text)
                run.font.size = Pt(10)
            doc.add_paragraph()
    
    def _add_experience(self, doc):
        """Ajoute l'expérience professionnelle"""
        experiences = self.soup.find_all('div', class_='experience-item')
        if not experiences:
            return

        self._add_section_title(doc, self.TRANSLATIONS[self.language]['experience'])
        for exp in experiences:
            # Titre du poste
            job_title = exp.find('div', class_='job-title')
            if job_title:
                p = doc.add_paragraph()
                run = p.add_run(job_title.text.strip())
                run.font.bold = True
                run.font.size = Pt(12)
                run.font.color.rgb = RGBColor(30, 64, 175)
            
            # Entreprise
            company = exp.find('div', class_='company-name')
            if company:
                p = doc.add_paragraph(company.text.strip())
                for run in p.runs:
                    run.font.size = Pt(10)
                    run.font.italic = True
            
            # Dates
            date_range = exp.find('div', class_='date-range')
            if date_range:
                p = doc.add_paragraph(date_range.text.strip())
                for run in p.runs:
                    run.font.size = Pt(9)
                    run.font.color.rgb = RGBColor(156, 163, 175)
            
            # Responsabilités
            responsibilities = exp.find('ul', class_='responsibilities')
            if responsibilities:
                for li in responsibilities.find_all('li'):
                    p = doc.add_paragraph(li.text.strip(), style='List Bullet')
                    for run in p.runs:
                        run.font.size = Pt(10)
            
            # Stack technique
            tech_stack = exp.find('div', class_='tech-stack')
            if tech_stack:
                p = doc.add_paragraph()
                p_format = p.paragraph_format
                p_format.left_indent = Inches(0.3)
                
                run = p.add_run(tech_stack.get_text(strip=True))
                run.font.size = Pt(9)
                run.font.italic = True
                run.font.color.rgb = RGBColor(59, 130, 246)
            
            doc.add_paragraph()
    
    def _add_education(self, doc):
        """Ajoute la formation"""
        education_items = self.soup.find_all('div', class_='education-item')
        if not education_items:
            return

        self._add_section_title(doc, self.TRANSLATIONS[self.language]['education'])
        for edu in education_items:
            job_title = edu.find('div', class_='job-title')
            if job_title:
                p = doc.add_paragraph()
                run = p.add_run("🎓 " + job_title.text.strip())
                run.font.bold = True
                run.font.size = Pt(11)
            
            company = edu.find('div', class_='company-name')
            if company:
                p = doc.add_paragraph(company.text.strip())
                for run in p.runs:
                    run.font.size = Pt(10)
            
            date_range = edu.find('div', class_='date-range')
            if date_range:
                p = doc.add_paragraph(date_range.text.strip())
                for run in p.runs:
                    run.font.size = Pt(9)
                    run.font.italic = True
            
            # Formations supplémentaires
            responsibilities = edu.find('ul', class_='responsibilities')
            if responsibilities:
                for li in responsibilities.find_all('li'):
                    p = doc.add_paragraph(li.text.strip(), style='List Bullet')
                    for run in p.runs:
                        run.font.size = Pt(9)
            
            doc.add_paragraph()
    
    def _add_projects(self, doc):
        """Ajoute les projets GitHub"""
        projects_added = False

        # Format avec repo-card (classique et design)
        repo_cards = self.soup.find_all('div', class_='repo-card')
        if repo_cards:
            self._add_section_title(doc, self.TRANSLATIONS[self.language]['projects'])
            for card in repo_cards:
                # Nom du projet
                link = card.find('a')
                if link:
                    p = doc.add_paragraph()
                    run = p.add_run(link.get_text(strip=True))
                    run.font.bold = True
                    run.font.size = Pt(10)
                    run.font.color.rgb = RGBColor(30, 64, 175)

                # Description
                desc = card.find('div', class_='repo-description')
                if desc:
                    p = doc.add_paragraph()
                    run = p.add_run(desc.get_text(strip=True))
                    run.font.size = Pt(9)
                    run.font.italic = True

                # Technologies
                tech = card.find('div', class_='repo-tech')
                if tech:
                    tech_text = ', '.join([span.get_text(strip=True) for span in tech.find_all('span')])
                    if tech_text:
                        p = doc.add_paragraph()
                        run = p.add_run(tech_text)
                        run.font.size = Pt(8)
                        run.font.color.rgb = RGBColor(59, 130, 246)

            projects_added = True

        # Fallback: format projects-list simple
        if not projects_added:
            projects_list = self.soup.find('div', class_='projects-list')
            if projects_list:
                self._add_section_title(doc, self.TRANSLATIONS[self.language]['projects'])
                text = projects_list.get_text(separator='\n', strip=True)
                p = doc.add_paragraph(text)
                for run in p.runs:
                    run.font.size = Pt(10)
                projects_added = True

        # Fallback: format projects-grid (design)
        if not projects_added:
            projects_grid = self.soup.find('div', class_='projects-grid')
            if projects_grid:
                self._add_section_title(doc, self.TRANSLATIONS[self.language]['projects'])
                text = projects_grid.get_text(separator='\n', strip=True)
                p = doc.add_paragraph(text)
                for run in p.runs:
                    run.font.size = Pt(10)
                projects_added = True

        # Lien GitHub profile
        if projects_added:
            github_profile = self.soup.find('div', class_='github-profile')
            if github_profile:
                link = github_profile.find('a')
                if link:
                    p = doc.add_paragraph()
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    run = p.add_run(f"Portfolio: {link.get('href', link.get_text(strip=True))}")
                    run.font.size = Pt(9)
                    run.font.color.rgb = RGBColor(59, 130, 246)
    
    def _add_section_title(self, doc, title):
        """Ajoute un titre de section stylisé"""
        p = doc.add_paragraph()
        run = p.add_run(title)
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(30, 64, 175)
        
        # Ligne sous le titre
        self._add_horizontal_line(doc, '3b82f6')
    
    def _add_horizontal_line(self, doc, color='3b82f6'):
        """Ajoute une ligne horizontale"""
        p = doc.add_paragraph()
        p_format = p.paragraph_format
        p_format.space_after = Pt(6)
        
        pPr = p._element.get_or_add_pPr()
        pBdr = OxmlElement('w:pBdr')
        
        bottom = OxmlElement('w:bottom')
        bottom.set(qn('w:val'), 'single')
        bottom.set(qn('w:sz'), '12')
        bottom.set(qn('w:space'), '1')
        bottom.set(qn('w:color'), color)
        
        pBdr.append(bottom)
        pPr.append(pBdr)
    
    def convert_all(self, pdf_path=None, docx_path=None):
        """Convertit en PDF et DOCX"""
        lang_flag = "🇬🇧" if self.language == 'en' else "🇫🇷"
        print(f"\n🔄 Début de la conversion ({lang_flag})...\n")
        
        pdf_file = self.generate_pdf(pdf_path)
        docx_file = self.generate_docx(docx_path)
        
        print(f"\n✅ Conversion terminée avec succès!")
        print(f"   📄 PDF:  {pdf_file}")
        print(f"   📝 DOCX: {docx_file}")
        
        return pdf_file, docx_file


BANNER = """
 ██████╗██╗   ██╗     ██████╗ ██████╗ ███╗   ██╗██╗   ██╗███████╗██████╗ ████████╗███████╗██████╗
██╔════╝██║   ██║    ██╔════╝██╔═══██╗████╗  ██║██║   ██║██╔════╝██╔══██╗╚══██╔══╝██╔════╝██╔══██╗
██║     ██║   ██║    ██║     ██║   ██║██╔██╗ ██║██║   ██║█████╗  ██████╔╝   ██║   █████╗  ██████╔╝
██║     ╚██╗ ██╔╝    ██║     ██║   ██║██║╚██╗██║╚██╗ ██╔╝██╔══╝  ██╔══██╗   ██║   ██╔══╝  ██╔══██╗
╚██████╗ ╚████╔╝     ╚██████╗╚██████╔╝██║ ╚████║ ╚████╔╝ ███████╗██║  ██║   ██║   ███████╗██║  ██║
 ╚═════╝  ╚═══╝       ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
                        HTML → PDF & DOCX | ATS Compatible | FR/EN
"""


DEFAULT_FILES_DIR = Path(__file__).parent / "files"
DEFAULT_OUTPUT_DIR = Path(__file__).parent / "output"
DEFAULT_CV_FILES = ["cv_fr.html", "cv_en.html", "cv_fr_design.html", "cv_en_design.html"]


def find_default_cv():
    """Cherche un fichier CV par défaut dans le dossier files/"""
    if not DEFAULT_FILES_DIR.exists():
        return None

    for cv_file in DEFAULT_CV_FILES:
        cv_path = DEFAULT_FILES_DIR / cv_file
        if cv_path.exists():
            return cv_path

    return None


def print_help():
    """Affiche l'aide avec le banner"""
    print(BANNER)
    print("Usage: cv-converter [fichier_html] [pdf_output] [docx_output]")
    print("\nSi aucun fichier n'est spécifié, cherche automatiquement")
    print("files/cv_fr.html ou files/cv_en.html")
    print("\nLes fichiers générés sont placés dans le dossier output/")
    print("\nExemples:")
    print("  cv-converter                                              # Auto-détection")
    print("  cv-converter files/cv_en.html")
    print("  cv-converter files/cv_fr.html output/mon_cv.pdf output/mon_cv.docx")
    print("\nDétection automatique de la langue:")
    print("  - Par nom de fichier: cv_en.html → Anglais, cv_fr.html → Français")
    print("  - Par attribut HTML: <html lang='en'> ou <html lang='fr'>")
    print("  - Par défaut: Français")


def main():
    """Point d'entrée du script"""
    if len(sys.argv) > 1 and sys.argv[1] in ('-h', '--help'):
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
            print(f"\n   Placez votre fichier HTML dans le dossier files/")
            print(f"   Fichiers recherchés: {', '.join(DEFAULT_CV_FILES)}")
            print(f"\n   Ou spécifiez un fichier: cv-converter <fichier.html>")
            sys.exit(1)
        print(f"📂 Fichier détecté automatiquement: {html_file}")

    pdf_output = sys.argv[2] if len(sys.argv) > 2 else None
    docx_output = sys.argv[3] if len(sys.argv) > 3 else None

    try:
        converter = CVConverter(html_file)
        converter.convert_all(pdf_output, docx_output)
    
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
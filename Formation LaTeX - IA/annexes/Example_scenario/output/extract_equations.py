import fitz  # PyMuPDF
import re

pdf_path = r"C:\Users\Utilisateur\Documents\Perso\Projets\tests\Formation_LaTeX\annexes\Example_scenario\input\Cartes auto-correctives équations.pdf"

# Ouvrir le PDF
pdf_document = fitz.open(pdf_path)

print(f"Nombre de pages : {len(pdf_document)}")

equations = []
solutions = []

# Extraire le texte de chaque page
for page_num in range(min(4, len(pdf_document))):  # Limiter aux 4 premières pages pour tester
    page = pdf_document[page_num]
    text = page.get_text()
    
    print(f"\n{'='*50}")
    print(f"PAGE {page_num + 1}")
    print(f"{'='*50}")
    print(text[:1000])  # Afficher les 1000 premiers caractères
    
    # Rechercher des patterns d'équations
    # Pattern pour les équations simples
    eq_patterns = [
        r'([0-9x\+\-\=\s\(\)\/]+)',  # équations basiques
        r'([0-9]x\s*[\+\-]\s*[0-9]+\s*=\s*[0-9]+)',  # forme ax + b = c
        r'x²\s*[\+\-]\s*[0-9]+x\s*[\+\-]\s*[0-9]+\s*=\s*0',  # équations du second degré
    ]
    
    for pattern in eq_patterns:
        matches = re.findall(pattern, text)
        if matches:
            print(f"\nÉquations trouvées avec pattern {pattern}:")
            for match in matches[:10]:  # Limiter à 10 résultats
                if len(match.strip()) > 3:  # Éviter les matches trop courts
                    print(f"  - {match.strip()}")

pdf_document.close()

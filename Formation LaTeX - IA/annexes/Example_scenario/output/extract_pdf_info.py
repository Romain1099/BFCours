import PyPDF2
import fitz  # PyMuPDF
from PIL import Image
import os

pdf_path = r"C:\Users\Utilisateur\Documents\Perso\Projets\tests\Formation_LaTeX\annexes\Example_scenario\input\Cartes auto-correctives équations.pdf"
output_dir = r"C:\Users\Utilisateur\Documents\Perso\Projets\tests\Formation_LaTeX\annexes\Example_scenario\output\images"

# Créer le répertoire images
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Ouvrir le PDF
pdf_document = fitz.open(pdf_path)

print(f"Nombre de pages : {len(pdf_document)}")

# Extraire le texte et les images
for page_num in range(len(pdf_document)):
    page = pdf_document[page_num]
    
    # Extraire le texte
    text = page.get_text()
    if page_num == 0:  # Afficher le texte de la première page
        print(f"\nTexte de la page {page_num + 1}:")
        print(text[:500])  # Premiers 500 caractères
    
    # Extraire les images
    image_list = page.get_images()
    
    for img_index, img in enumerate(image_list):
        # Récupérer l'image
        xref = img[0]
        pix = fitz.Pixmap(pdf_document, xref)
        
        if pix.n - pix.alpha < 4:  # GRAY ou RGB
            img_path = os.path.join(output_dir, f"page{page_num+1}_img{img_index+1}.png")
            pix.save(img_path)
        else:  # CMYK
            pix = fitz.Pixmap(fitz.csRGB, pix)
            img_path = os.path.join(output_dir, f"page{page_num+1}_img{img_index+1}.png")
            pix.save(img_path)
        
        pix = None
        print(f"Image extraite : {img_path}")

pdf_document.close()

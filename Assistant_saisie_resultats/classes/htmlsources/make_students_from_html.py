import os
import glob
import csv
from bs4 import BeautifulSoup
from tkinter import Tk
from tkinter.filedialog import askopenfilenames



# Get all HTML files matching the pattern "*.html"
#html_files = glob.glob('*.html')
def csv_from_html_students(list_files):
    for filename in html_files:
        # Extract the class code and établissement from the filename (e.g., "6eA" and "jam" from "6eA-jam.html")
        base_name = os.path.splitext(filename)[0]  # Remove the .html extension
        parts = base_name.split('-')
        class_name = parts[0]
        etablissement = parts[1] if len(parts) > 1 else ''

        # Prepare the output CSV filename
        output_csv = f"{class_name}-{etablissement}.csv"

        # Open and parse the HTML file
        with open(filename, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

            # Find all <p class="div-like"> elements
            p_elements = soup.find_all('p', class_='div-like')

            # List to store student data for this file
            students = []

            for p in p_elements:
                # Find the NOM and PRENOM within the <span> tags
                nom_span = p.find('span', class_='b-like text--uppercase')
                prenom_span = p.find('span', class_='text--slate-dark')

                if nom_span and prenom_span:
                    nom = nom_span.get_text(strip=True)
                    prenom = prenom_span.get_text(strip=True)

                    # Add the student data to the list
                    students.append({
                        'Nom': nom,
                        'Prenom': prenom
                    })

        # Write the student data to a CSV file
        with open(output_csv, 'w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['Nom', 'Prenom']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

            writer.writeheader()
            for student in students:
                writer.writerow(student)

        print(f"CSV file '{output_csv}' has been created successfully.")

if __name__=="__main__":
    # Configurer tkinter pour ne pas afficher une fenêtre principale
    Tk().withdraw()

    # Ouvrir une boîte de dialogue pour sélectionner plusieurs fichiers HTML
    html_files = askopenfilenames(
        title="Sélectionnez les fichiers HTML",
        filetypes=[("Fichiers HTML", "*.html"), ("Tous les fichiers", "*.*")]
    )

    if html_files:
        csv_from_html_students(list_files=html_files)

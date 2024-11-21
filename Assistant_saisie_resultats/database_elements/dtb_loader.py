
import pathlib
from pathlib import Path
import csv
import json 

class DtbLoader():
    """
    Classe regroupant les méthodes de chargement à partir de la database.
    """
    def __init__(self):
        self.number_of_access = 0

    def load_csv(self,filepath_to_load:Path)-> list:
        # Ouvrir le fichier et lire les données
        with open(filepath_to_load, newline='') as csvfile:
            reader = csv.DictReader(csvfile,delimiter=';')
            
            # Créer une liste pour stocker les lignes sous forme de dictionnaires
            data = []
            
            # Lire chaque ligne du CSV
            for row in reader:
                data.append(row)
        
        self.number_of_access +=1
        data = json.dumps(data, indent=4,ensure_ascii=False)
        return data
    
def use_case_one():
    loader=DtbLoader()
    lines=loader.load_csv(filepath_to_load=Path("devoirs_effectues/3e6-beu/csv/27_05_2024.csv"))
    print(lines)
    print(loader.number_of_access)

if __name__ == "__main__":
    use_case_one()
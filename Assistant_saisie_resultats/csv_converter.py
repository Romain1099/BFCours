import csv

class CSVConverter:
    """
    Classe pour convertir un fichier CSV avec les colonnes spécifiques et reformater les données.
    """
    def __init__(self, input_csv, output_csv):
        self.input_csv = input_csv
        self.output_csv = output_csv
        self.error_code = ""

    def read_and_convert(self):
        """
        Lit le fichier CSV d'entrée, convertit selon les spécifications, et écrit le résultat dans un nouveau fichier CSV.
        """
        try:
            with open(self.input_csv, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=';')
                exercises = {}
                output_data = []

                for row in reader:
                    if not exercises:
                        exercises = self._extract_exercises(row['Exercices'])
                    converted_row = self._convert_row(row, exercises)
                    output_data.append(converted_row)

                self._write_to_csv(output_data, exercises)
        except Exception as e:
            self.error_code = str(e)
            print(f"Error while processing the file: {self.error_code}")

    def _extract_exercises(self, exercises_str):
        """
        Extrait et renomme les exercices depuis la chaîne de caractères Exercices.
        """
        exercises = exercises_str.split(',')
        return {i + 1: f"EXO{i + 1}" for i in range(len(exercises))}

    def _convert_row(self, row, exercises):
        """
        Convertit une ligne du CSV en formatant les exercices dans des colonnes séparées.
        """
        new_row = {'Nom': row['Nom'], 'Prenom': row['Prenom']}
        exercise_scores = row['Exercices'].split(',')
        for i, score in enumerate(exercise_scores):
            new_row[exercises[i + 1]] = score
        return new_row

    def _write_to_csv(self, data, exercises):
        """
        Écrit les données converties dans un nouveau fichier CSV.
        """
        headers = ['Nom', 'Prenom'] + [exercises[i] for i in sorted(exercises)]
        try:
            with open(self.output_csv, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=headers, delimiter=';')
                writer.writeheader()
                writer.writerows(data)
        except Exception as e:
            self.error_code = str(e)
            print(f"Error while writing to the file: {self.error_code}")
    def revert_to_original_format(self, date, explications, barmes):
        """
        Reconvertit le fichier CSV transformé au format original avec les colonnes Date, Exercices, Bareme et Explications.
        :param date: Date à ajouter à chaque ligne.
        :param explications: Liste des explications à ajouter.
        :param barmes: Liste des barèmes pour chaque exercice.
        """
        try:
            with open(self.output_csv, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=';')
                original_data = []

                for row in reader:
                    original_row = self._revert_row(row, date, explications, barmes)
                    original_data.append(original_row)

            self._write_to_original_csv(original_data, date, explications, barmes)
        except Exception as e:
            self.error_code = str(e)
            print(f"Error while processing the file: {self.error_code}")

    def _revert_row(self, row, date, explications, barmes):
        """
        Aide à reconvertir une ligne au format original avec les données supplémentaires.
        """
        exercises = sorted([key for key in row.keys() if key.startswith('EXO')])
        exercises_scores = [row[ex] for ex in exercises]
        exercises_str = ','.join(exercises_scores)
        barmes_str = ','.join(barmes)

        original_row = {
            'Nom': row['Nom'],
            'Prenom': row['Prenom'],
            'Date': date,
            'Exercices': exercises_str,
            'Bareme': barmes_str,
            'Explications': ','.join(explications)
        }
        return original_row

    def _write_to_original_csv(self, data, date, explications, barmes):
        """
        Écrit les données reconverties dans le fichier CSV initial.
        """
        headers = ['Nom', 'Prenom', 'Date', 'Exercices', 'Bareme', 'Explications']
        try:
            with open(self.input_csv, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=headers, delimiter=';')
                writer.writeheader()
                writer.writerows(data)
        except Exception as e:
            self.error_code = str(e)
            print(f"Error while writing to the file: {self.error_code}")

    def sort_csv_by_name(self,input_filepath,output_filepath):
        """
        Trie le fichier CSV par la colonne 'Nom' en ordre alphabétique.
        """
        try:
            with open(input_filepath, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=';')
                data_sorted = sorted(reader, key=lambda row: row['Nom'])

            # Réécriture du fichier CSV trié
            with open(output_filepath, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=reader.fieldnames, delimiter=';')
                writer.writeheader()
                writer.writerows(data_sorted)
            print("CSV trié par ordre alphabétique selon la colonne 'Nom'.")
        except Exception as e:
            self.error_code = str(e)
            print(f"Error while sorting the file: {self.error_code}")


if __name__ == "__main__":
    # Chemins vers les fichiers CSV d'entrée et de sortie
    input_csv_path = '04_04_2024.csv'
    output_csv_path = 'BB_3e3_04_04_2024_sorted.csv'
    
    # Création d'une instance de CSVConverter
    converter = CSVConverter(input_csv_path, output_csv_path)
    
    # Premier cas d'utilisation : Convertir le CSV original au nouveau format
    converter.sort_csv_by_name("18_04_2024.csv","18_04_2024.csv")
    print("Conversion au nouveau format CSV terminée.")
    
    """# Deuxième cas d'utilisation : Revenir au format CSV original
    # Spécifiez la date, les explications et les barmes
    date = "04_04_2024"
    explications = [""] * 6  # Adaptez la taille de cette liste au nombre d'exercices
    barmes = ["18", "16", "14", "20", "16", "16"]  # Barèmes pour chaque exercice
    
    # Réutilisation du fichier output pour lire les données converties et les rétablir au format initial
    converter.output_csv = output_csv_path  # Assurez-vous que ce soit le fichier transformé
    converter.input_csv = 'BB_04_04_2024_reverted.csv'
    converter.revert_to_original_format(date, explications, barmes)
    print("Reconversion au format original terminée.")"""

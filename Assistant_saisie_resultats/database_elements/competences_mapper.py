import csv
import json
import numpy as np
import os

class CompetenceEvaluator:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []
        self.headers = []
        self.competence_mapping = self.load_competence_mapping()

    def load_competence_mapping(self):
        json_file_path = os.path.splitext(self.file_path)[0] + '.json'
        with open(json_file_path, mode='r', encoding='utf-8') as file:
            json_data = json.load(file)
            return json_data['competences']

    def open_csv_file(self):
        with open(self.file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            self.headers = next(reader)
            self.data = [row for row in reader]

    def parse_data(self):
        idx_exercises = self.headers.index('Exercices')
        idx_bareme = self.headers.index('Bareme')
        
        exercises_scores = []
        bareme_scores = []
        
        for row in self.data:
            exercises_scores.append(list(map(float, row[idx_exercises].split(','))))
            bareme_scores.append(list(map(float, row[idx_bareme].split(','))))
        
        return exercises_scores, bareme_scores

    def distribute_scores(self, exercises_scores, bareme_scores):
        competence_scores = {}
        competence_max_scores = {}

        for ex_idx, exercise in enumerate(exercises_scores):
            ex_key = f'ex{ex_idx + 1}'
            if ex_key in self.competence_mapping:
                for comp_name, comp_data in self.competence_mapping[ex_key].items():
                    if comp_name not in competence_scores:
                        competence_scores[comp_name] = 0
                        competence_max_scores[comp_name] = 0
                    
                    proportion = float(comp_data['proportion'])
                    competence_scores[comp_name] += sum(exercise) * proportion
                    competence_max_scores[comp_name] += sum(bareme_scores[ex_idx]) * proportion
        
        return competence_scores, competence_max_scores

    def evaluate_competences(self, competence_scores, competence_max_scores):
        competence_evaluation = {}

        for ex_key, comp_data in self.competence_mapping.items():
            for sub_comp_name, sub_comp_data in comp_data.items():
                obtained_points = competence_scores.get(sub_comp_name, 0)
                max_points = competence_max_scores.get(sub_comp_name, 0)
                percentage = (obtained_points / max_points) * 100 if max_points != 0 else 0
                
                if percentage >= 85:
                    label = "TBM"
                elif percentage >= 50:
                    label = "MS"
                elif percentage >= 25:
                    label = "MF"
                else:
                    label = "MI"
                
                competence_evaluation[sub_comp_name] = {
                    'nomcomplet': sub_comp_data['nomcomplet'],
                    'code': sub_comp_data['code'],
                    'obtained_points': obtained_points,
                    'max_points': max_points,
                    'percentage': percentage,
                    'label': label
                }
        
        return competence_evaluation

    def evaluate_global_competences(self):
        global_competence_scores = {}
        global_competence_max_scores = {}

        exercises_scores, bareme_scores = self.parse_data()

        for exercise, bareme in zip(exercises_scores, bareme_scores):
            competence_scores, competence_max_scores = self.distribute_scores([exercise], [bareme])
            for comp in competence_scores:
                if comp not in global_competence_scores:
                    global_competence_scores[comp] = 0
                    global_competence_max_scores[comp] = 0
                global_competence_scores[comp] += competence_scores[comp]
                global_competence_max_scores[comp] += competence_max_scores[comp]

        return self.evaluate_competences(global_competence_scores, global_competence_max_scores)

    def add_competence_columns(self):
        idx_exercises = self.headers.index('Exercices')
        idx_bareme = self.headers.index('Bareme')
        
        # Vérifier si les colonnes existent déjà
        if 'Competences' in self.headers:
            idx_competences = self.headers.index('Competences')
        else:
            idx_competences = -1
            self.headers.append('Competences')
        
        if 'CompetencesM' in self.headers:
            idx_competencesM = self.headers.index('CompetencesM')
        else:
            idx_competencesM = -1
            self.headers.append('CompetencesM')
        
        new_data = []

        for row in self.data:
            exercises_scores = list(map(float, row[idx_exercises].split(',')))
            bareme_scores = list(map(float, row[idx_bareme].split(',')))

            competence_scores, competence_max_scores = self.distribute_scores([exercises_scores], [bareme_scores])
            evaluation = self.evaluate_competences(competence_scores, competence_max_scores)

            percentages = [f"{comp['percentage']:.2f}" for comp in evaluation.values()]
            labels = [comp['label'] for comp in evaluation.values()]

            if idx_competences == -1:
                row.append(','.join(percentages))
            else:
                row[idx_competences] = ','.join(percentages)

            if idx_competencesM == -1:
                row.append(','.join(labels))
            else:
                row[idx_competencesM] = ','.join(labels)

            new_data.append(row)
        
        # Écrire les nouvelles données dans le fichier d'origine
        with open(self.file_path, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(self.headers)
            writer.writerows(new_data)

    def export_evaluation(self, evaluation):
        for comp_name, comp_data in evaluation.items():
            print(f"Compétence: {comp_name}")
            print(f"Nom complet: {comp_data['nomcomplet']}")
            print(f"Code: {comp_data['code']}")
            print(f"Points obtenus: {comp_data['obtained_points']:.2f}")
            print(f"Points maximum: {comp_data['max_points']:.2f}")
            print(f"Pourcentage de réussite: {comp_data['percentage']:.2f}%")
            print(f"Évaluation: {comp_data['label']}\n")

def use_case_one():
    # Utilisation de la classe
    file_path = 'database_elements/test_comp_mapping.csv'
    evaluator = CompetenceEvaluator(file_path)
    evaluator.open_csv_file()
    exercises_scores, bareme_scores = evaluator.parse_data()
    competence_scores, competence_max_scores = evaluator.distribute_scores(exercises_scores, bareme_scores)
    evaluation = evaluator.evaluate_competences(competence_scores, competence_max_scores)
    evaluator.export_evaluation(evaluation)
def use_case_two():
    # Utilisation de la classe avec ajout des colonnes 'Competences' et 'CompetencesM'
    file_path = 'database_elements/test_comp_mapping.csv'
    evaluator = CompetenceEvaluator(file_path)
    evaluator.open_csv_file()
    evaluator.add_competence_columns()
    # Évaluation globale des compétences pour l'ensemble de la classe
    global_evaluation = evaluator.evaluate_global_competences()
    evaluator.export_evaluation(global_evaluation)
if __name__=="__main__":
    use_case_two()
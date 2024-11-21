import os
import csv
from typing import Dict, List
import pandas as pd
import json
import datetime
from students_statistics_latex_files import statisticsLatexFile
from latexcompiler import LaTeXCompiler

def capitalize_name(name:str)->str:
            # Séparer le nom en segments basés sur les tirets
            segments = name.split('-')
            # Capitaliser chaque segment
            capitalized_segments = [segment.capitalize() for segment in segments]
            # Recombiner les segments avec des tirets
            capitalized_name = '-'.join(capitalized_segments)
            return capitalized_name
class Student:
    def __init__(self, class_code:str="non précisé",date_devoir=""):
        self.class_code=class_code
        self.output_devoirs_info_dir=f"devoirs_effectues/{class_code}/pdf"
        self.csv_file = f"classes/{self.class_code}.csv"
        self.json_file = f"classes/{self.class_code}.json"
        self.students={}
        self.date_devoir=date_devoir
        self.initiate_directories(class_code=class_code)
    def initiate_directories(self,class_code):
        """
        permet de vérifier si les dossier suivants existent : f"devoirs_effectues/{class_code}/tex", f"devoirs_effectues/{class_code}/csv",f"devoirs_effectues/{class_code}/pdf"
        la fonction crée ces répertoires s'il ne sont pas déjà créés
        la fonction ne fait rien si le class_code n'est pas précisé
        """
        if not class_code:
            # Si aucun class_code n'est fourni, la fonction ne fait rien.
            print("entrer  un code classe est primordial.")
            return
        # Liste des types de dossiers à créer pour le code de classe donné.
        folder_types = ['tex', 'csv', 'pdf']
        base_directory = 'devoirs_effectues'
        
        # Création des dossiers si nécessaire
        for folder_type in folder_types:
            directory_path = os.path.join(base_directory, class_code, folder_type)
            os.makedirs(directory_path, exist_ok=True)
            print(f"Le répertoire {directory_path} a été vérifié et créé si nécessaire.")

    def load_students(self):
        """
        Définis les modalités de chargement des élèves de la classe. 
        Dans le cas ou les élèves sont chargés pour la première fois via un csv, les informations sont présentées dans le json file. 

        """
        # Vérifie si le fichier JSON existe
        if os.path.exists(self.json_file):
            self.students = self.load_students_from_json()
        else:#if not self.students:
            if os.path.exists(self.csv_file):  # Vérifie si le fichier CSV existe
                self.students = self.load_students_from_csv()
                self.save_students_to_json()
            else:
                # Aucun fichier n'est trouvé, affiche un popup d'erreur
                print("Fichier de données étudiant non trouvé : Ni le fichier JSON ni le fichier CSV spécifié n'a été trouvé.")


    def load_students_from_csv(self) -> Dict:
        """Charge les données des étudiants depuis un fichier CSV de manière dynamique."""
        students = {}
        base_dir = f"resultats_par_etudiant/{self.class_code}"
        print(f"self.csv_file de load_student_from_csv : {self.csv_file}")
        with open(self.csv_file, mode='r', newline='', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                print(f"load_students_from_csv : {row}")

                student = {key: value.strip().title() for key, value in row.items()}
                if 'Prenom' in student and 'Nom' in student:
                    dir_name = f"{student['Nom'].upper()}_{student['Prenom']}"
                    dir_path = os.path.join(base_dir, dir_name)
                    dir_devoir = os.path.join(dir_path, 'devoirs')
                    json_file_path = os.path.join(dir_path, f"{dir_name}.json")
                    csv_file_path = os.path.join(dir_path, f"{dir_name}.csv")
                    tex_file_path = os.path.join(dir_path, f"{dir_name}.tex")
                    student['json_file_path'] = json_file_path
                    student['csv_file_path'] = csv_file_path
                    student['devoirs_path'] = dir_devoir
                    student['tex_file_path'] = tex_file_path
                    os.makedirs(dir_path, exist_ok=True)

                    student['devoirs']=self.check_student_devoirs(dir_devoir)
                    student_key=f"{student['Nom'].upper()}_{student['Prenom']}"
                    students[student_key]=student
                    print(students[student_key])
        return students
    
    def load_students_from_json(self):
        """Charge les données des étudiants depuis un fichier JSON spécifié."""
        if not os.path.exists(self.json_file):
            raise FileNotFoundError(f"Le fichier {self.json_file} n'existe pas.")
        students={}
        with open(self.json_file, 'r', encoding='utf-8') as file:
            students = json.load(file)  # Charge les données du fichier JSON
        # Itération sur chaque étudiant si les étudiants sont stockés dans un dictionnaire de dictionnaires
        for student_key, student_data in students.items():
            if 'devoirs_path' in student_data:
                # Mise à jour des devoirs pour chaque étudiant
                student_data['devoirs'] = self.check_student_devoirs(student_data['devoirs_path'])
            else:
                raise KeyError(f"Chemin des devoirs manquant pour l'étudiant {student_key}")

        return students


    def check_student_devoirs(self,directory:str="")->List[str]:
        """
        Charge et retourne les noms de fichiers avec l'extension '.tex' dans un répertoire spécifié.

        Args:
        directory (str): Chemin du répertoire à analyser.

        Returns:
        List[str]: Liste des noms de fichiers '.tex' trouvés dans le répertoire.
        """
        if directory!="":
            # Créer le répertoire s'il n'existe pas
            os.makedirs(directory, exist_ok=True)
            
            # Lister tous les fichiers dans le répertoire qui finissent par '.tex'
            return [file for file in os.listdir(directory) if file.endswith('.tex')]
        return []  # Retourner une liste vide si aucun répertoire n'est spécifié

    def add_student_data_by_csv(self, csv_filepath: str = ""):
        """
        Charge des données supplémentaires d'un fichier CSV et met à jour le dictionnaire self.students.
        
        Args:
        csv_filepath (str): Chemin vers le fichier CSV à charger.
        """
        print(f"add_student_data_by_csv : {csv_filepath}")
        if not csv_filepath:  # Si aucun chemin n'est fourni, utiliser le fichier CSV par défaut de la classe
            csv_filepath = self.csv_file
        if not os.path.exists(csv_filepath):
            raise FileNotFoundError(f"Le fichier {csv_filepath} n'existe pas.")

        with open(csv_filepath, mode='r', newline='', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                nom = row.get('Nom', '').strip().upper()
                prenom = row.get('Prenom', '').strip()
                student_key = f"{nom}_{prenom}"
                if student_key not in self.students:
                    self.students[student_key] = {}
                for key, value in row.items():
                    if key not in self.students[student_key]:  # Créer l'entrée si elle n'existe pas
                        print(f"étudiant créé student_key : {student_key}, key : {key} ")
                        self.students[student_key][key] = value.strip().title()
                        
    def add_student_data_by_csv_old(self, csv_filepath: str = ""):
        """
        Charge des données supplémentaires d'un fichier CSV et met à jour le dictionnaire self.students.
        
        Args:
        csv_filepath (str): Chemin vers le fichier CSV à charger.
        """
        print(f"add_student_data_by_csv : {csv_filepath}")
        if not csv_filepath:  # Si aucun chemin n'est fourni, utiliser le fichier CSV par défaut de la classe
            csv_filepath = self.csv_file
        if not os.path.exists(csv_filepath):
            raise FileNotFoundError(f"Le fichier {csv_filepath} n'existe pas.")

        with open(csv_filepath, mode='r', newline='', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file, delimiter=';')
            print(reader.__str__())
            for row in reader:
                nom = row.get('Nom', '').strip().upper()
                print(f"nom : {nom}")
                prenom = row.get('Prenom', '').strip()
                student_key = f"{nom}_{prenom}"
                if student_key not in self.students:
                    self.students[student_key] = {}
                    print('clé non connue , on lajoute')
                for key, value in row.items():
                    if key not in self.students[student_key]:  # Créer l'entrée si elle n'existe pas
                        print(f"étudiant créé student_key : {student_key}, key : {key} ")
                        self.students[student_key][key] = value.strip().title()
    def save_students_to_json(self, json_file: str=""):
        """Sauvegarde les informations des étudiants dans un fichier JSON."""
        if json_file=="":
            json_file=self.json_file
        with open(json_file, 'w', encoding='utf-8') as file:
            #print(f'saved {json_file}')
            json.dump(self.students, file, indent=4, ensure_ascii=False)

    def __str__(self):
        student_info = []
        for student_key, student in self.students.items():
            details = [f"{key} : {value}" for key, value in student.items()]
            student_info.append('\n'.join(details) + '\n')
        return '\n'.join(student_info)

    def normaliser_csv(self,input_file: str, output_file: str = "output_normalized.csv"):
        """
        Fusionne les lignes cassées d'un fichier CSV (se terminant par une barre oblique inversée)
        et écrit les lignes normalisées dans un nouveau fichier CSV.

        :param input_file: Chemin du fichier CSV d'entrée.
        :param output_file: Chemin du fichier CSV de sortie normalisé.
        """
        # Lire les lignes brutes du fichier CSV d'entrée
        with open(input_file, 'r', newline='', encoding='utf-8-sig') as infile:
            lines = infile.read().splitlines()
        
        # Fusionner les lignes qui se terminent par une barre oblique inversée
        normalized_lines = []
        current_line = ""
        for line in lines:
            if line.endswith('\\'):
                current_line += line[:-1]  # Supprimer la barre oblique et continuer la ligne
            else:
                current_line += line
                normalized_lines.append(current_line)
                current_line = ""  # Réinitialiser pour la prochaine ligne

        # Écrire les lignes fusionnées dans un fichier CSV de sortie
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as outfile:
            writer = csv.writer(outfile, delimiter=';')
            for row in normalized_lines:
                writer.writerow(row.split(';'))
                
    def add_devoir_to_students(self,theme="",class_code="",date="",themes="",title=""):
        csv_filepath=f"devoirs_effectues/{class_code}/csv/devoir_{title}_{date}.csv"
        self.normaliser_csv(csv_filepath,csv_filepath)
        self.statistic_manager=statisticsLatexFile("",csv_filename=csv_filepath,themes=themes,titre={title})
        self.statistics=self.statistic_manager.statistics
        
        full_latex_content=""
        tex_final_filepath=f"devoirs_effectues/{class_code}/tex/devoir_{title}_{date}.tex"
        pdf_filepath=tex_final_filepath.replace('tex','pdf')
        compiler = LaTeXCompiler([tex_final_filepath])
        print(f"add_devoir_to_students : {self.students}")
        with open(csv_filepath, mode='r', newline='', encoding='utf-8-sig') as file:
            # Spécifier le délimiteur ';' pour csv.DictReader
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                prenom=row.get('Prenom','Prenom')
                nom=row.get('Nom','Nom')
                nom=nom.upper()
                prenom=capitalize_name(prenom)
                # Gestion de la date avec une valeur par défaut utilisant la date actuelle si non spécifiée
                date_devoir = row.get('Date', '').strip() or datetime.datetime.now().strftime('%d_%m_%Y')
                
                # Utilisation de row.get pour éviter KeyError et gestion des valeurs par défaut
                bareme_str = row.get('Bareme', '')
                resultats_str = row.get('Exercices', '')
                explications=row.get('Explications', '')
                #print(f"resultats_str : {resultats_str}")
                #print(f"explications depuis add_devoir_to_student : {explications}")
                # S'assurer que les données ne sont pas vides avant de les diviser
                bareme = bareme_str.split(',') if bareme_str else []
                explications = explications.split(',') if explications else []

                resultats = resultats_str.split(',') if resultats_str else []
                
                print(list(self.students.keys()))

                student_key=f"{nom}_{prenom}"
                student=self.students[student_key]
                
                try:
                    student_csv_path = student['csv_file_path']
                    #raise KeyError(f"Student a un csv_file_path_key : \n {student}")
                except:
                    raise KeyError(f"Student n'a pas de csv_file_path_key : \n {student}")
                local_tex_path = os.path.join(student['devoirs_path'], f"devoir_{date_devoir}_texrecap.tex")
                
                # Appel de la fonction pour ajouter des données de devoir au fichier CSV de l'étudiant
                self.append_devoir_to_csv(student_csv_path, date_devoir, bareme, resultats)
                
                # Création d'un récapitulatif LaTeX pour le devoir et ajout au fichier TeX de l'étudiant
                contenu_recap = self.create_devoir_texrecap(local_tex_path, self.date_devoir, bareme, resultats,student_label=f"{nom.upper()} {prenom}",theme=theme,date_devoir=date_devoir,explications=explications)
                full_latex_content += self.only_begin_document(contenu_recap)
                full_latex_content+="""
                \\newpage
                """

                #self.append_tex_to_student_file(student['tex_file_path'], contenu_recap)
        commandes="""
% Définition d'une nouvelle tcolorbox minimaliste
                \\usepackage{siunitx}
                \\sisetup{output-decimal-marker={,}} 
                \\newcommand\\boitesignature[2]{
                \\begin{multicols}{2}
                    \\begin{tcolorbox}[nobeforeafter,colframe=white, % Couleur de la bordure
                    colback=white, % Couleur de fond
                    boxsep=0pt, % Pas d'espace entre le texte et les bords de la boîte
                    top=0pt, bottom=0pt, left=0pt, right=0pt, % Pas de marges intérieures
                    boxrule=0pt, % Pas de bordure visible
                    height=3cm,
                    arc=0pt, % Coins non arrondis
                    ]
                        #1
                    \\end{tcolorbox}
                    
                    \\columnbreak
                    
                    \\begin{tcolorbox}[nobeforeafter,height=3cm,title=\\bfseries Résultat obtenu au contrôle :,halign title=flush left,fonttitle=\\bfseries,colbacktitle=black,coltitle=white,colback=white]%red!50!black
                        #2
                    \\end{tcolorbox}
                \\end{multicols}
                }
""" 
        calculated_bareme=self.statistic_manager.bareme#[1,2,2,3,2]
        prof_statistics=self.statistic_manager.make_full_prof_recap(bareme=calculated_bareme,explications=explications,tips_title="",tips="")#explications=["","","","","",""]#18,16,14,20,16,16
        #if os.path.exists(tex_final_filepath):
        #    double_compile_option = False
        #else:
        #    double_compile_option = True
        double_compile_option = True
        with open(tex_final_filepath, mode='w', encoding='utf-8') as file:
            #\\documentclass[12pt]{{article}}
            full_latex_content= f"""
                \documentclass[a4paper,11pt,fleqn]{{article}}
                \\usepackage[utf8]{{inputenc}}
                \\usepackage[left=1cm,right=0.5cm,top=0.5cm,bottom=2cm]{{geometry}}

                \\usepackage{{bfcours}}
                \\usepackage{{datatool}}
                \\usepackage{{geometry}}
                \\usepackage{{pgfplots}}
                \\pgfplotsset{{compat=1.18}}
                \\usepgfplotslibrary{{polar}}
                \\usepackage{{pgfplotstable}}
                \\usepackage{{float}}
                \\usepackage{{multicol}}
                \\usepackage[most]{{tcolorbox}}
                \\usepackage{{hyperref}}

                \\DTLsetseparator{{;}} % Assurez-vous que cela correspond au séparateur de votre fichier CSV.
                \\hypersetup{{
                    pdfauthor={{R.Deschamps}},
                    pdfsubject={{}},
                    pdfkeywords={{}},
                    pdfproducer={{LuaLaTeX}},
                    pdfcreator={{Boum Factory}}
                }}
                {commandes}
                \\def\\rdifficulty{{1}}
                \\def\\points{{1}}
                \\setrdexo{{%left skip=1cm,
                display exotitle,
                exo header = tcolorbox,
                %display tags,
                skin = bouyachakka,
                lower ={{box=crep}},
                display score,
                display level,
                save lower,
                score=\\points,
                level=\\rdifficulty,
                overlay={{\\node[inner sep=0pt,
                anchor=west,rotate=90, yshift=0.3cm]%,xshift=-3em], yshift=0.45cm
                at (frame.south west) {{\\thetags[0]}} ;}}
                ]%obligatoire
                }}
                \\setrdcrep{{seyes, correction=true, correction color=monrose, correction font = \\large\\bfseries}}
                \\title{{Analyse du devoir : {title}}}
                \\author{{R.Deschamps}}
                \\begin{{document}}
                \\setcounter{{pagecounter}}{{0}}
                \\setcounter{{ExoMA}}{{0}}
                \\setcounter{{prof}}{{0}}
                \\chapitre[Prof]{{
                {title}
                }}{{
                Collège% type_etablissement : Collège,Lycée
                }}{{
                % nom_etablissement : Amadis Jamyn,Eugène Belgrand
                }}{{
                %
                }}{{
                Analyse du devoir : 
                }}

                \\tableofcontents
                
                \\newpage

                {prof_statistics}

                \\newpage

                {full_latex_content}
                \\end{{document}}
            """
            file.write(full_latex_content)
        if compiler.compile_and_open(document_path=tex_final_filepath, output_directory=self.output_devoirs_info_dir, double_compile=double_compile_option):
            print("Opération réussie.")
            compiler.destroy_auxiliary_files(pdf_filepath)
        else:
            print("Erreur de compilation:", compiler.error_code)
    def only_begin_document(self, content: str) -> str:
        """
        Extracts and returns the content between LaTeX document delimiters.
        
        Args:
        content (str): The string containing the full LaTeX content.

        Returns:
        str: The content between the \begin{document} and \end{document} delimiters.
        """
        # Finding the start index of \begin{document} and adding length of \begin{document} to find the actual start
        start_index = content.find(r'\\begin{document}') + 16
        
        # Finding the end index of \end{document}
        end_index = content.find(r'\\end{document}')
        
        # Extracting the content between the found indices
        if start_index != -1 and end_index != -1 and start_index < end_index:
            modified_content = content[start_index:end_index].strip()
        else:
            modified_content = content
            self.error_code = "Invalid LaTeX document structure."  # Error handling if delimiters are not properly placed

        # Uncomment the next line for debugging purposes to see the extracted content
        #print("######## by only_begin_document ########\n", modified_content)

        return modified_content
    
    def append_devoir_to_csv(self, student_csv_path, date, bareme, details):
        # Lire le contenu du fichier CSV existant, s'il existe
        rows = []
        if os.path.exists(student_csv_path):
            with open(student_csv_path, mode='r', newline='', encoding='utf-8-sig') as file:
                reader = csv.reader(file)
                headers = next(reader)  # lire les en-têtes
                for row in reader:
                    rows.append(row)

        # Convertir les barèmes et détails en chaînes de caractères
        bareme_str = ','.join(map(str, bareme))
        details_str = ','.join(map(str, details))

        # Vérifier si une ligne avec la même date existe déjà
        updated = False
        for row in rows:
            if row[0] == date:
                row[1] = bareme_str
                row[2] = details_str
                updated = True
                break

        # Si aucune ligne n'a été mise à jour, ajouter une nouvelle ligne
        if not updated:
            rows.append([date, bareme_str, details_str])

        # Écrire le contenu mis à jour dans le fichier CSV
        with open(student_csv_path, mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(['date', 'bareme', 'details'])  # en-têtes
            writer.writerows(rows)

    def create_devoir_texrecap(self, tex_path, date, bareme, details,student_label="",theme="",date_devoir="",explications=[]):
        statistics_content=f"""
        Devoir Recap: {date}\\newline
        Bareme: {','.join(map(str, bareme))}\\newline
        Details: {','.join(map(str, details))}\\newline
        """
        if date_devoir!=self.date_devoir:
            self.date_devoir=date_devoir
        if explications==[]:
            print("pas d'explications dans create_devoir_texrecap")
            explications = [""] * len(details)
        #print(f"details : {details}")
        statistics_content = self.statistic_manager.make_full_student_recap(list(details),list(bareme),explications=explications,student_label=student_label,tips_title="",tips="",theme=theme,date_devoir=self.date_devoir)
        
        content=f"""
        \\documentclass[12pt]{{article}}
        \\usepackage{{bfcours}}
        \\usepackage[utf8]{{inputenc}}
        \\usepackage{{datatool}}
        \\usepackage{{geometry}}
        \\usepackage{{pgfplots}}
        \\pgfplotsset{{compat=1.18}}
        \\usepgfplotslibrary{{polar}}
        \\usepackage{{pgfplotstable}}
        \\usepackage{{float}}
        \\usepackage{{multicol}}
        \\usepackage[most]{{tcolorbox}}
        \\geometry{{left=1cm,right=1cm,top=2cm,bottom=2cm}}
        \\usepackage{{hyperref}}

        \\DTLsetseparator{{;}} % Assurez-vous que cela correspond au séparateur de votre fichier CSV.
        \\usepackage{{siunitx}}
        \\sisetup{{output-decimal-marker={{,}}}}
        \\newcommand\\boitesignature[2]{{
        \\begin{{multicols}}{{2}}
            \\begin{{tcolorbox}}[nobeforeafter,colframe=white, % Couleur de la bordure
            colback=white, % Couleur de fond
            boxsep=0pt, % Pas d'espace entre le texte et les bords de la boîte
            top=0pt, bottom=0pt, left=0pt, right=0pt, % Pas de marges intérieures
            boxrule=0pt, % Pas de bordure visible
            height=3cm,
            arc=0pt, % Coins non arrondis
            ]
                #1
            \\end{{tcolorbox}}
            
            \\columnbreak
            
            \\begin{{tcolorbox}}[nobeforeafter,height=3cm,title=\\bfseries Résultat obtenu au contrôle :,halign title=flush left,fonttitle=\\bfseries,colbacktitle=black,coltitle=white,colback=white]%red!50!black
                #2
            \\end{{tcolorbox}}
        \\end{{multicols}}
        }}
        \\begin{{document}}
            {statistics_content}
        \\end{{document}}
        """
        with open(tex_path, 'w', encoding='utf-8') as file:
            file.write(content)
        return statistics_content

    def make_year_prof_recap(self,class_code="",students_informations="",date_min="",date_max=""):
        print("""A implémenter : 
              précision sur l'entete, vérifier si on peut pas utiliser la structure de classe pour récupérer plus facilement les informations directement. 
              Notamment l'utilisation du student_json qui contient globalement tous les chemins...
              
              tirer au clair cette histoire d'itérations sur les student_informations

              Il faut aussi implémenter la partie UI pour déclencher la creation et la compilation du recap en s'inspirant de create_devoir_and_compile je pense.
              """)
        if class_code==""or students_informations=="":
            print("Saisir le code classe et insérer le dictionnaire des étudiants")
            return
        elif not isinstance(students_informations,dict):
            print("la liste des étudiants doit être un dictionnaire ou un DataFrame")
            return
        year_tex_content=""
        for student in students_informations:#eventuellement besoin d'un iter
            nom=student['Nom']
            prenom=student['Prenom']
            
            full_year_student_csv_path=f"resultats_par_etudiant/{class_code}/{nom}_{prenom}/{nom}_{prenom}.csv"
            student_tex_main_file=f"resultats_par_etudiant/{class_code}/{nom}_{prenom}/{nom}_{prenom}.tex"
            year_tex_content+=self.make_full_year_student_recap(full_year_student_csv=full_year_student_csv_path,student_tex_main_file=student_tex_main_file,date_min=date_min,date_max=date_max,save_option=False)
            year_tex_content+="\\newpage"
        if date_max=="" and date_min=="":
            tex_year_recap_filepath=f"devoirs_effectues/{class_code}/bilan_annuel_{class_code}.tex"
        else:
            tex_year_recap_filepath=f"devoirs_effectues/{class_code}/bilan_du_{date_min}_au_{date_max}_{class_code}.tex"
        with open(tex_year_recap_filepath,'w',encoding='utf-8') as file:
            en_tete=""
            ender=""
            year_tex_content=en_tete + year_tex_content + ender
            file.write(year_tex_content) 

            


        
    def make_full_year_student_recap(self, full_year_student_csv="", student_tex_main_file="", date_min="", date_max="",save_option=False):
        if full_year_student_csv == "" or student_tex_main_file == "":
            print("Renseigner les chemin vers la liste des devoirs de l'étudiant et le chemin vers le récapitulatif tex des devoirs de l'étudiant")
            return

        # Lire les lignes du fichier CSV
        df = pd.read_csv(full_year_student_csv, sep=';')

        # Convertir les dates en datetime
        df['Date'] = pd.to_datetime(df['Date'], format='%d_%m_%Y')

        # Filtrer les dates si date_min et date_max sont renseignées
        if date_min:
            date_min = datetime.datetime.strptime(date_min, '%d_%m_%Y')
            df = df[df['Date'] >= date_min]
        if date_max:
            date_max = datetime.datetime.strptime(date_max, '%d_%m_%Y')
            df = df[df['Date'] <= date_max]

        recap = []
        dates = []
        percentages = []

        for index, row in df.iterrows():
            date = row['Date']
            dates.append(date)
            exercices = list(map(float, row['Exercices'].split(',')))
            bareme = list(map(float, row['Bareme'].split(',')))
            total_note = sum(exercices)
            total_bareme = sum(bareme)
            percentage = (total_note / total_bareme) * 100 if total_bareme != 0 else 0
            percentages.append(percentage)
            recap.append((date, total_note, total_bareme, percentage))

        # Créer le code TeX pour le tableau
        tex_table = "\\begin{tabular}{|c|c|c|}\n\\hline\nDate & Note totale/Bareme total & Pourcentage de réussite \\\\\n\\hline\n"
        for date, total_note, total_bareme, percentage in recap:
            tex_table += f"{date.strftime('%d/%m/%Y')} & {total_note}/{total_bareme} & {percentage:.2f}\% \\\\\n\\hline\n"
        tex_table += "\\end{tabular}\n"

        # Créer le code TeX pour le graphique avec TikZ
        tex_graph = (
            "\\begin{tikzpicture}\n"
            "\\begin{axis}[\n"
            "    date coordinates in=x,\n"
            "    xticklabel=\year-\month-\day,\n"
            "    xticklabel style={rotate=90, anchor=near xticklabel},\n"
            "    xlabel=Date,\n"
            "    ylabel={Pourcentage de réussite},\n"
            "    ymin=0, ymax=100,\n"
            "    grid=major,\n"
            "    width=\\textwidth,\n"
            "    height=0.4\\textheight\n"
            "]\n"
            "\\addplot coordinates {\n"
        )
        
        for date, percentage in zip(dates, percentages):
            tex_graph += f"    ({date.strftime('%Y-%m-%d')}, {percentage})\n"
        
        tex_graph += (
            "};\n"
            "\\end{axis}\n"
            "\\end{tikzpicture}\n"
        )

        # Calcul de la moyenne des pourcentages
        average_percentage = sum(percentages) / len(percentages) if percentages else 0
        note_sur_20 = (average_percentage / 100) * 20

        # Entête du document TeX
        tex_header = (
            "\\documentclass{article}\n"
            "\\usepackage{pgfplots}\n"
            "\\pgfplotsset{compat=1.18}\n"
            "\\usepackage{graphicx}\n"
            "\\usepackage[utf8]{inputenc}\n"
            "\\usepackage[T1]{fontenc}\n"
            "\\usepackage{lmodern}\n"
            "\\begin{document}\n"
        )

        # Structure du document TeX
        tex_content = (
            tex_header +
            "\\section*{Tableau récapitulatif des devoirs}\n" +
            tex_table +
            "\\section*{Graphique de progression}\n" +
            tex_graph +
            "\\section*{Note moyenne}\n" +
            f"Note moyenne sur 20 : {note_sur_20:.2f}/20\n" +
            "\\end{document}\n"
        )

        # Écrire le contenu dans le fichier TeX
        if save_option==True:
            with open(student_tex_main_file, 'w', encoding='utf-8') as tex_file:
                tex_file.write(tex_content)
            print(f"Le fichier TeX récapitulatif a été créé avec succès et enregistré sous {student_tex_main_file}")

        else:
            return self.only_begin_document(tex_content)


    def append_tex_to_student_file(self, tex_file_path, tex_content):
        """
        Appends a new content to the student's main TeX file just before the \\end{document} command.

        Args:
        tex_file_path (str): The path to the main TeX file of the student.
        tex_content_path (str): The path to the TeX content to be appended.
        """
        if not os.path.exists(tex_file_path):
            with open(tex_file_path, 'w', encoding='utf-8') as file:
                file.write("\\documentclass[12pt]{article}\n\\begin{document}\n\\end{document}")

        # Read the existing content from the main TeX file
        with open(tex_file_path, 'r', encoding='utf-8') as file:
            content = file.readlines()

        # Locate the last occurrence of '\end{document}' and split the content
        end_document_index = -1
        for i, line in enumerate(content):
            if '\\end{document}' in line:
                end_document_index = i
                break
        
        if end_document_index == -1:  # If \end{document} was not found, just append at the end
            end_document_index = len(content)

        new_content = tex_content

        # Insert new content just before \end{document}
        new_file_content = content[:end_document_index] + ['\\newpage\n'] + [new_content + '\n'] + content[end_document_index:]

        # Write back the modified content
        with open(tex_file_path, 'w', encoding='utf-8') as file:
            file.writelines(new_file_content)
    

    

    
class dtbSender():
    def __init__(self):
        self.students:list[Student]=[]

    def create_global_statistics(self):
        file_created=False
        file_content=""

        return file_created
    
    def create_specific_student_file(self):
        file_created=False
        file_content=""

        return file_created

def main():
    # Exemple d'utilisation
    #student_manager = Student('3e3-beu',"04/04/2024")
    student_manager = Student('6eA-jam',"18/04/2024")

    #charger les données depuis un csv basique ( initialisation de la classe )
    #student_manager.students=student_manager.load_students_from_csv()

    student_manager.add_student_data_by_csv(csv_filepath= "classes/6eA-jam.csv")
    #charger les données depuis le json de la classe
    #student_manager.students=student_manager.load_students_from_json()

    #méthode unifiée pour charger selon le mode voulu :
    student_manager.load_students()
    #ajouter un devoir pour les étudiants
    '''student_manager.add_devoir_to_students("18_04_2024.csv",theme="""
    \\begin{itemize}
        \item Symétrie axiale
        \item Proportionnalité
    \\end{itemize}
""")'''

    print(student_manager)  # Afficher la liste des étudiants

    #sauvegarder les données dans le json de la classe
    student_manager.save_students_to_json()

if __name__== "__main__":
    main()
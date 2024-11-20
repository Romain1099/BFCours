import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, Toplevel
from tkinter import StringVar
from UI_elements.classe_selector import UIClasseSelector
from UI_elements.devoir_creator_simple import HomeworkSetupUI
from UI_elements.full_year_selector import UIYearSelector
from database_elements.year_recapitulator import YearRecap
import customtkinter as ctk
from latexcompiler import LaTeXCompiler
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"
import pandas as pd
import csv
import os
import subprocess
from datetime import date
from csv_converter import CSVConverter
from database_sender import Student
from UI_elements.datetime_selector import day_ui
from tkinter import ttk
from email_sender import emailSender


instructions_compilation = '''pyinstaller --onefile --noconsole --icon=enroute.ico UI_basic_v3.py '''
class HomeworkManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestionnaire de Devoirs")
        self.homework_info = {}
        self.students_df = None
        self.wanted_email_send=False
        
        # Interface de sélection initiale
        self.setup_initial_interface()

        #self.root.withdraw()  # Cache la fenêtre principale
        #self.create_dialog()
    def make_email(self,row):
        return ""
    def send_homework(self,csv_filepath):
        if self.wanted_email_send==False:
            return
        with open(csv_filepath,'r',encoding="utf-8") as file:
            reader=file.readlines()
        nom=f"{row['Nom']} {row['Prenom']}"
        for row in reader:
            if row['Email']:
                email=row['Email']
                if row['recap_filepath']:
                    piece_jointe=row['recap_filepath']
                    bool_piece_jointe=True
                else:
                    piece_jointe=""
                    bool_piece_jointe=False
                mail_content=self.make_email(row)
                
                sender=emailSender(filepath=piece_jointe,email=email,content=mail_content)
                response=sender.send_email(attachment=bool_piece_jointe)
                print_status=f"Mail de {nom} : {response.json()['Messages']['Status']}"
                print(print_status)
    
    def load_existing_homework(self):
        def update_devoirs(*args):
            # Mise à jour des fichiers de devoirs basée sur la sélection du code classe
            selected_class = combo_class_code.get()
            devoirs_directory = f"devoirs_effectues/{selected_class}/csv"
            if os.path.exists(devoirs_directory):
                devoirs_files = [f.replace('.csv', '') for f in os.listdir(devoirs_directory) if f.endswith('.csv')]
            else:
                devoirs_files = []
            #combo_devoirs['values'] = devoirs_files
            combo_devoirs.configure(values=devoirs_files)
            if devoirs_files:
                #combo_devoirs.current(0)  # Sélectionne le premier fichier par défaut
                combo_devoirs.set(devoirs_files[0])
            else:
                combo_devoirs.set('')
        def on_ok():
            code_classe=combo_class_code.get()
            self.class_code=code_classe
            devoir_choisi=combo_devoirs.get()
            filename=f"devoirs_effectues/{code_classe}/csv/{devoir_choisi}.csv"
            if filename:
                self.students_df = pd.read_csv(filename, sep=';', encoding='utf-8')
                self.homework_info['title'] = os.path.splitext(os.path.basename(filename))[0].split('_')[1]
                print(f"title du homework info : {self.homework_info['title']}")
                self.homework_info['date'] = self.students_df.iloc[0]['Date']  # Assumer la date dans la première ligne
                
                # Extraire les exercices et les barèmes à partir de la ligne de barème
                exercises= self.students_df.iloc[0]['Exercices']
                bareme = self.students_df.iloc[0]['Bareme']
                self.homework_info['bareme'] = [x.strip() for x in bareme.split(',')]
                """try:
                    self.homework_info['exercises'] = [x.strip() for x in exercises.split(',')]
                except AttributeError:
                    self.homework_info['exercises'] = [0] * len(self.homework_info['bareme'])
                    self.students_df.iloc[0]['Exercices']=[0] * len(self.homework_info['bareme'])"""
                
                top.destroy()
                self.setup_student_buttons()

        """# Création de la fenêtre principale
        root = tk.Tk()
        root.withdraw()  # Cache la fenêtre principale"""

        # Création d'une fenêtre de dialogue en second plan
        top = ctk.CTkToplevel(self.root)
        def on_close():
            self.root.deiconify()
            top.destroy()

        top.protocol("WM_DELETE_WINDOW", on_close)

        self.root.iconify()
        top.title("Setup - Charger un devoir de la base de données")
        # Obtention des dimensions de la fenêtre principale
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()

        # Calcul de la nouvelle position pour 'top'
        new_x = root_x
        new_y = root_y + root_height+50
        # Configuration de la géométrie de 'top' pour qu'elle apparaisse juste en dessous de 'self.root'
        top.geometry(f"+{new_x}+{new_y}")
        # Menu déroulant pour les codes de classe
        label_class_code = ctk.CTkLabel(top, text="Choisissez un code de classe :")
        label_class_code.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        class_directory = 'classes'
        class_code_files = [f.replace('.csv', '') for f in os.listdir(class_directory) if f.endswith('.csv')]
        combo_class_code = ctk.CTkComboBox(top,command=update_devoirs, values=class_code_files, state="readonly")
        combo_class_code.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        #combo_class_code.bind('<<ComboboxSelected>>', update_devoirs)

        # Menu déroulant pour les devoirs, mis à jour dynamiquement
        label_devoirs = ctk.CTkLabel(top, text="Choisissez un devoir dans la liste :")
        label_devoirs.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        combo_devoirs = ctk.CTkComboBox(top, state="readonly")
        combo_devoirs.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Bouton OK pour confirmer la sélection
        ok_button = ctk.CTkButton(top, text="OK", command=on_ok)
        ok_button.grid(row=2, column=0, columnspan=2, pady=20)
    def load_existing_homework_old(self):
        print("""
            A modifier : on veut pouvoir choisir un devoir qui a déja été importé et le sélectionner via ou champ de sélection.
              """)
        initial_directory = os.path.join(os.getcwd(),"devoirs_effectues")  # Obtient le répertoire courant du programme
        filename = filedialog.askopenfilename(initialdir=initial_directory, filetypes=[("CSV files", "*.csv")])
        if filename:
            self.students_df = pd.read_csv(filename, sep=';', encoding='utf-8')
            self.homework_info['title'] = os.path.splitext(os.path.basename(filename))[0]
            print(f"title du homework info : {self.homework_info['title']}")
            self.homework_info['date'] = self.students_df.iloc[0]['Date']  # Assumer la date dans la première ligne
            
            # Extraire les exercices et les barèmes à partir de la ligne de barème
            exercises= self.students_df.iloc[0]['Exercices']
            bareme = self.students_df.iloc[0]['Bareme']
            self.homework_info['exercises'] = [x.strip() for x in exercises.split(',')]
            self.homework_info['bareme'] = [x.strip() for x in bareme.split(',')]
            self.setup_student_buttons()

    def setup_initial_interface(self):
        # Boutons de manipulation des classes
        ctk.CTkButton(self.root, text="Importer une classe par csv", command=self.import_class_csv).grid(row=0, column=0, sticky="ew")

        # Boutons de manipulation des devoirs
        ctk.CTkButton(self.root, text="Créer un nouveau devoir manuellement", command=self.setup_homework_interface_new).grid(row=1, column=0, sticky="ew")
        ctk.CTkButton(self.root, text="Importer un devoir au format .csv", command=self.setup_homework_import).grid(row=1, column=1, sticky="ew")
        ctk.CTkButton(self.root, text="Modifier un devoir de la base de données", command=self.load_existing_homework).grid(row=1, column=2, sticky="ew")
        #ctk.CTkButton(self.root, text="Exporter un devoir en .csv", command=self.convert_csv_file).grid(row=2, column=0, sticky="ew")
        ctk.CTkButton(self.root, text="Exporter un bilan annuel", command=self.export_year_pdf).grid(row=2, column=0, sticky="ew")

        ctk.CTkButton(self.root, text="Exporter un devoir en .pdf", command=self.export_to_pdf).grid(row=2, column=1, sticky="ew")
        ctk.CTkButton(self.root, text="Ouvrir le dossier d'un devoir", command=self.open_homework_folder).grid(row=2, column=2, sticky="ew")
    

    def import_class_csv(self):
        """
        présente un champ pour saisir le code classe en présentant le mode de saisie conventionnel avec une indication de bonne pratique : "classe-etab" exemple "6e5-jac
        présente une indication claire et courte pour la structuration du fichier : il faut une colonne Nom et une colonne Prenom on sépare les colonnes par des points virgules .
        préciser que : les caractères spéciaux doivent respecter l'encodage utf-8.
        présente un bouton ok qui déclenche l'ouverture d'un askopenfiledialog pour que l'utilisateur choisisse le csv d'une classe.
        une fois le document choisi, on crée le fichier "classes/{code_classe}.csv"
        pour chaque extension dans extension = ['csv','tex','pdf'] on crée le répertoire f"devoirs effectues/{code_classe}/{extension}"
        ensuite pour chaque extension dans extension = ['csv','tex','pdf'] on crée le répertoire f"resultats_par_etudiant/{code_classe}"
        Initialisation du student associé à la classe pour peupler les répertoires créés. :
        student_manager = Student(f"{code_classe}","")
        student_manager.add_student_data_by_csv(csv_filepath= f"classes/{code_classe}.csv")
        student_manager.load_students()
                """

        top = ctk.CTkToplevel(self.root)
        def on_close():
            self.root.deiconify()
            top.destroy()

        top.protocol("WM_DELETE_WINDOW", on_close)
        
        self.root.iconify()
        top.title("Importer une classe par CSV")
        top.geometry("400x300")

        def on_ok():
            code_classe = entry_code_classe.get().strip()
            if not code_classe:
                messagebox.showerror("Erreur", "Le code de la classe ne peut pas être vide.")
                return
            
            # Demande de sélection du fichier CSV
            csv_filepath = filedialog.askopenfilename(
                title="Sélectionnez le fichier CSV de la classe",
                filetypes=[("CSV files", "*.csv")]
            )
            if not csv_filepath:
                messagebox.showerror("Erreur", "Aucun fichier sélectionné.")
                return

            # Création des répertoires
            os.makedirs(f"classes", exist_ok=True)
            os.makedirs(f"devoirs_effectues/{code_classe}/csv", exist_ok=True)
            os.makedirs(f"devoirs_effectues/{code_classe}/tex", exist_ok=True)
            os.makedirs(f"devoirs_effectues/{code_classe}/pdf", exist_ok=True)
            os.makedirs(f"resultats_par_etudiant/{code_classe}", exist_ok=True)

            # Copier le fichier CSV dans le répertoire classes
            class_csv_path = f"classes/{code_classe}.csv"
            with open(csv_filepath, 'r', encoding='utf-8') as src_file:
                with open(class_csv_path, 'w', encoding='utf-8') as dest_file:
                    dest_file.write(src_file.read())

            # Initialisation du student_manager
            student_manager = Student(code_classe, "")
            student_manager.add_student_data_by_csv(csv_filepath=class_csv_path)
            student_manager.load_students()
            print(f"student manager : {student_manager.__str__()}")
            messagebox.showinfo("Succès", "Les données de la classe ont été importées avec succès.")
            # Interface de sélection initiale
            self.setup_initial_interface()
            top.destroy()
            

        # Interface graphique pour saisir le code de la classe
        frame = ctk.CTkFrame(top)
        frame.pack(pady=20, padx=20, fill='both', expand=True)

        label_code_classe = ctk.CTkLabel(frame, text="Code de la classe (exemple : '6e5-jac'):")
        label_code_classe.pack(anchor='w', pady=5)

        entry_code_classe = ctk.CTkEntry(frame)
        entry_code_classe.pack(fill='x', pady=5)

        button_ok = ctk.CTkButton(top, text="OK", command=on_ok)
        button_ok.pack(pady=20)

        # Indication de la structure du fichier
        label_instruction = ctk.CTkLabel(
            top, 
            text=("Le fichier CSV doit contenir deux colonnes : 'Nom' et 'Prenom', séparées par des points-virgules.\n"
                  "Les caractères spéciaux doivent respecter l'encodage UTF-8."),
            justify='left'
        )
        label_instruction.pack(pady=10, padx=20, anchor='w')
    def open_homework_folder(self):
        def on_ok():
            # Actions à effectuer quand l'utilisateur clique sur OK
            selected_class = combo_class_code.get()
            selected_devoir = combo_devoirs.get()
            print(f"Code de classe sélectionné: {selected_class}")
            print(f"Devoir sélectionné: {selected_devoir}")
            
            # Construire le chemin absolu du dossier contenant le fichier PDF
            base_dir = os.path.abspath('devoirs_effectues')  # Obtient le chemin absolu vers 'devoirs_effectues'
            pdf_directory = os.path.join(base_dir, selected_class, 'pdf')
            
            # Vérifier si le dossier existe
            if not os.path.exists(pdf_directory):
                messagebox.showerror("Erreur", "Le dossier spécifié n'existe pas.")
                return
            
            # Essayer d'ouvrir le dossier dans l'explorateur de fichiers
            try:
                subprocess.run(f'explorer "{pdf_directory}"', shell=True)#, check=True
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Erreur lors de l'ouverture du dossier", str(e))

            # Détruire la fenêtre popup
            top.destroy()
        def update_devoirs(*args):
            # Mise à jour des fichiers de devoirs basée sur la sélection du code classe
            selected_class = combo_class_code.get()
            devoirs_directory = f"devoirs_effectues/{selected_class}/csv"
            if os.path.exists(devoirs_directory):
                devoirs_files = [f.replace('.csv', '') for f in os.listdir(devoirs_directory) if f.endswith('.csv')]
            else:
                devoirs_files = []
            #combo_devoirs['values'] = devoirs_files
            combo_devoirs.configure(values=devoirs_files)
            if devoirs_files:
                #combo_devoirs.current(0)  # Sélectionne le premier fichier par défaut
                combo_devoirs.set(devoirs_files[0])
            else:
                combo_devoirs.set('')
        """# Création de la fenêtre principale
        root = tk.Tk()
        root.withdraw()  # Cache la fenêtre principale"""

        # Création d'une fenêtre de dialogue en second plan
        top = ctk.CTkToplevel(self.root)
        def on_close():
            self.root.deiconify()
            top.destroy()

        top.protocol("WM_DELETE_WINDOW", on_close)
        
        self.root.iconify()
        top.title("Setup - Ouverture du dossier d'un devoir")
        # Obtention des dimensions de la fenêtre principale
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()

        # Calcul de la nouvelle position pour 'top'
        new_x = root_x
        new_y = root_y + root_height+50
        # Configuration de la géométrie de 'top' pour qu'elle apparaisse juste en dessous de 'self.root'
        top.geometry(f"+{new_x}+{new_y}")
        # Menu déroulant pour les codes de classe
        label_class_code = ctk.CTkLabel(top, text="Choisissez un code de classe :")
        label_class_code.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        class_directory = 'classes'
        class_code_files = [f.replace('.csv', '') for f in os.listdir(class_directory) if f.endswith('.csv')]
        combo_class_code = ctk.CTkComboBox(top,command=update_devoirs, values=class_code_files, state="readonly")
        combo_class_code.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        #combo_class_code.bind('<<ComboboxSelected>>', update_devoirs)

        # Menu déroulant pour les devoirs, mis à jour dynamiquement
        label_devoirs = ctk.CTkLabel(top, text="Choisissez un devoir dans la liste :")
        label_devoirs.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        combo_devoirs = ctk.CTkComboBox(top, state="readonly")
        combo_devoirs.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Bouton OK pour confirmer la sélection
        ok_button = ctk.CTkButton(top, text="OK", command=on_ok)
        ok_button.grid(row=2, column=0, columnspan=2, pady=20)
    def setup_homework_import(self):
        print("""
              A implémenter : 
              permet à l'utilisateur de choisir un fichier de notes qui a lui même fabriqué avant 
              on ouvre un popup demandant de saisir les informations courantes pour notre appli
              on permet un bouton qui ouvre une boite de dialogue recherche de fichier, ou alors on permet la possibilité de drag and drop un document. 
                On vérifie que le document est bien mis suivant nos standard et on précise tout ce qu'il faut changer pour convenir à notre présentation souhaitée. 
              Ensuite on enregistre au bon endroit suivant le class code et la date le devoir (supposé saisi à ce stade).
              """)
        def on_ok():
            # Demande de sélection du fichier CSV
            csv_filepath = filedialog.askopenfilename(
                title="Sélectionnez le fichier CSV de la classe",
                filetypes=[("CSV files", "*.csv")]
            )
            if not csv_filepath:
                messagebox.showerror("Erreur", "Aucun fichier sélectionné.")
                return
            is_standard=self.check_csv_structure_standards(csv_filepath)
            if is_standard :
                class_code=combo_class_code.get()
                self.add_csv_into_database(csv_filepath,class_code=class_code)  
            else:
                return
            self.setup_initial_interface()

            top.destroy()
        # Création d'une fenêtre de dialogue en second plan
        top = ctk.CTkToplevel(self.root)
        def on_close():
            self.root.deiconify()
            top.destroy()

        top.protocol("WM_DELETE_WINDOW", on_close)
        
        self.root.iconify()
        top.title("Paramètres du devoir")
        # Obtention des dimensions de la fenêtre principale
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()

        # Calcul de la nouvelle position pour 'top'
        new_x = root_x
        new_y = root_y + root_height+50
        # Configuration de la géométrie de 'top' pour qu'elle apparaisse juste en dessous de 'self.root'
        top.geometry(f"+{new_x}+{new_y}")
        # Menu déroulant pour les codes de classe
        label_class_code = ctk.CTkLabel(top, text="Choisissez un code de classe :")
        label_class_code.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        class_directory = 'classes'
        class_code_files = [f.replace('.csv', '') for f in os.listdir(class_directory) if f.endswith('.csv')]
        combo_class_code = ctk.CTkComboBox(top, values=class_code_files, state="readonly")#,command=update_devoirs
        combo_class_code.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        # Bouton OK pour confirmer la sélection
        ok_button = ctk.CTkButton(top, text="OK", command=on_ok)
        ok_button.grid(row=2, column=0, columnspan=2, pady=20)

    def check_csv_structure_standards(self, csv_filepath):
        # Vérifie que le CSV existe
        if not os.path.isfile(csv_filepath):
            messagebox.showerror("Erreur", "Le fichier CSV n'existe pas.")
            return False
        
        # Charger le fichier CSV
        try:
            df = pd.read_csv(csv_filepath, sep=';')
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la lecture du fichier CSV: {e}")
            return False

        # Vérifie si le CSV possède les colonnes requises
        required_columns = ['Nom', 'Prenom', 'Bareme', 'Exercices']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            messagebox.showerror("Erreur", f"Colonnes manquantes: {', '.join(missing_columns)}. "
                                           "Veuillez structurer le CSV avec les colonnes nécessaires séparées par des points-virgules.")
            return False

        # Vérifie les colonnes 'Bareme' et 'Exercices'
        try:
            bareme_list = [float(x.strip()) for x in df.iloc[0]['Bareme'].split(',')]
        except ValueError:
            messagebox.showerror("Erreur", "Les éléments de la colonne 'Bareme' doivent être une liste de nombres séparés par des virgules.")
            return False

        exercises = df.iloc[0]['Exercices']
        if isinstance(exercises, str) and exercises.strip() != "":
            try:
                exercises_list = [float(x.strip()) for x in exercises.split(',')]
            except ValueError:
                messagebox.showerror("Erreur", "Les éléments de la colonne 'Exercices' doivent être une liste de nombres séparés par des virgules.")
                return False
        
        return True

    def add_csv_into_database(self, csv_filepath, class_code=""):
        if class_code == "":
            messagebox.showerror("Erreur", "Pas de code classe dans add_csv_into_database")
            return
        
        # Charger le fichier CSV
        try:
            df = pd.read_csv(csv_filepath, sep=';', encoding='utf-8')
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la lecture du fichier CSV: {e}")
            return
        
        # Déterminer la longueur de la colonne 'Bareme'
        bareme_list = [x.strip() for x in df.iloc[0]['Bareme'].split(',')]
        bareme_length = len(bareme_list)

        # Initialiser les éléments vides de la colonne 'Exercices' avec des zéros
        df['Exercices'] = df['Exercices'].apply(lambda x: ','.join(['0'] * bareme_length) if pd.isna(x) or x.strip() == "" else x)

        # Vérifie si la colonne "Date" est présente dans le CSV, sinon demander la date
        if 'Date' not in df.columns:
            date_popup = ctk.CTkToplevel()
            date_popup.title("Saisir la date")
            date_popup.geometry("300x150")
            
            def on_confirm():
                date_value = date_entry.get().strip()
                if date_value:
                    df['Date'] = date_value.replace('/', '_')
                    date_popup.destroy()
                else:
                    messagebox.showerror("Erreur", "La date ne peut pas être vide.")
            
            label = ctk.CTkLabel(date_popup, text="Saisir la date (format : JJ/MM/AAAA) :")
            label.pack(pady=10)
            
            date_entry = ctk.CTkEntry(date_popup)
            date_entry.pack(pady=10)
            
            confirm_button = ctk.CTkButton(date_popup, text="Confirmer", command=on_confirm)
            confirm_button.pack(pady=10)
            
            date_popup.grab_set()
            date_popup.wait_window()

        # Créer le répertoire s'il n'existe pas
        destination_dir = f"devoirs_effectues/{class_code}/csv"
        os.makedirs(destination_dir, exist_ok=True)

        # Utiliser la date dans le nom du fichier
        if 'Date' in df.columns:
            date_value = df.iloc[0]['Date']
            destination_filepath = os.path.join(destination_dir, f"{date_value}.csv")
        else:
            destination_filepath = os.path.join(destination_dir, os.path.basename(csv_filepath))
        
        # Copier le fichier CSV en enregistrant les modifications
        try:
            df.to_csv(destination_filepath, sep=';', index=False, encoding='utf-8')
            messagebox.showinfo("Succès", f"Le fichier a été copié dans {destination_filepath}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la copie du fichier: {e}")


    
    def convert_csv_file(self):
        print("""
              A implémenter : 
              1. demande à l'utilisateur de choisir le fichier du devoir qu'il souhaite convertir 
              2. applique la fonction de conversion via le module csv_converter
              """)
    def export_to_pdf(self):
        devoir_selector=UIClasseSelector(self.root,parent_caller=self,function_name=self.create_recap_and_compile,topmost=False)

    def export_to_pdf_old(self):
        """
              1. demande à l'utilisateur de choisir un devoir parmi les devoirs existants ainsi que le code classe parmi les codes classes existants.
                on fait ça via une boite de dialogue menu déroulant en affichant les noms des csv contenus "dans classes" sans leur extension
              2. via le module database_sender on produit les fichiers récap
                on fait ça en créant un student
              3. via le module latexcompiler on compile et on ouvre le devoir. 
                 option de compilation : si on détecte un fichier auxiliaire produit pour ce devoir alors on compile en simple compilation (double compile= False) et s'il n'y a pas de fichier auxiliaire alors on compile en double compilation ( double compile = True )
              """
        def on_ok():
            # Actions à effectuer quand l'utilisateur clique sur OK
            selected_class = combo_class_code.get()
            selected_devoir = combo_devoirs.get()
            theme=theme_entry.get()
            print(f"Code de classe sélectionné: {selected_class}")
            print(f"Devoir sélectionné: {selected_devoir}")
            # Fermer la fenêtre après sélection
            self.create_recap_and_compile(selected_class,selected_devoir,theme=theme)
            on_close()

        def update_devoirs(*args):
            # Mise à jour des fichiers de devoirs basée sur la sélection du code classe
            selected_class = combo_class_code.get()
            devoirs_directory = f"devoirs_effectues/{selected_class}/csv"
            if os.path.exists(devoirs_directory):
                devoirs_files = [f.replace('.csv', '') for f in os.listdir(devoirs_directory) if f.endswith('.csv')]
            else:
                devoirs_files = []
            #combo_devoirs['values'] = devoirs_files
            combo_devoirs.configure(values=devoirs_files)
            if devoirs_files:
                #combo_devoirs.current(0)  # Sélectionne le premier fichier par défaut
                combo_devoirs.set(devoirs_files[0])
            else:
                combo_devoirs.set('')
        """# Création de la fenêtre principale
        root = tk.Tk()
        root.withdraw()  # Cache la fenêtre principale"""

        # Création d'une fenêtre de dialogue en second plan
        top = ctk.CTkToplevel(self.root)
        def on_close():
            self.root.deiconify()
            top.destroy()

        top.protocol("WM_DELETE_WINDOW", on_close)
        
        self.root.iconify()
        top.title("Setup - Export pdf")
        # Obtention des dimensions de la fenêtre principale
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()

        # Calcul de la nouvelle position pour 'top'
        new_x = root_x
        new_y = root_y + root_height+50
        # Configuration de la géométrie de 'top' pour qu'elle apparaisse juste en dessous de 'self.root'
        top.geometry(f"+{new_x}+{new_y}")
        # Menu déroulant pour les codes de classe
        label_class_code = ctk.CTkLabel(top, text="Choisissez un code de classe :")
        label_class_code.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        class_directory = 'classes'
        class_code_files = [f.replace('.csv', '') for f in os.listdir(class_directory) if f.endswith('.csv')]
        combo_class_code = ctk.CTkComboBox(top,command=update_devoirs, values=class_code_files, state="readonly")
        combo_class_code.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        #combo_class_code.bind('<<ComboboxSelected>>', update_devoirs)

        # Menu déroulant pour les devoirs, mis à jour dynamiquement
        label_devoirs = ctk.CTkLabel(top, text="Choisissez un devoir dans la liste :")
        label_devoirs.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        combo_devoirs = ctk.CTkComboBox(top, state="readonly")
        combo_devoirs.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        """# Bouton OK pour confirmer la sélection
        ok_button = tk.Button(top, text="OK", command=on_ok)
        ok_button.grid(row=2, column=0, columnspan=2, pady=20)"""

        # Champ pour entrer le thème du devoir
        label_theme = ctk.CTkLabel(top, text="Entrez le thème du devoir :")
        label_theme.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        
        theme_entry = ctk.CTkEntry(top)
        theme_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Bouton OK pour confirmer la sélection
        ok_button = ctk.CTkButton(top, text="OK", command=on_ok)
        ok_button.grid(row=3, column=0, columnspan=2, pady=20)
    
    def setup_goback_to_menu_button(self):
        #fabrique un bouton associé à la commande qui fait les choses suivantes : 
        #destroy son parent et lance la fonction self.setup_initial_interface au clic
        pass
    def setup_homework_interface_new(self):
        self.homework_creation_interface = HomeworkSetupUI(root=self.root,callback=self.set_homework_datas)
        self.root.iconify()
    def set_homework_datas(self,datas,classe_code):
        self.homework_info = datas
        self.generate_csv(classe_code=classe_code)

    def setup_homework_interface(self):
        #self.clear_widget(self.root)
        #self.root.withdraw()
        # Création d'une fenêtre de dialogue en second plan
        self.homework_creation_interface = ctk.CTkToplevel(self.root)
        def on_close():
            self.root.deiconify()
            self.homework_creation_interface.destroy()

        self.homework_creation_interface.protocol("WM_DELETE_WINDOW", on_close)
        
        self.root.iconify()
        self.homework_creation_interface.attributes("-topmost", True)
        # Obtention des dimensions de la fenêtre principale
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()

        # Calcul de la nouvelle position pour 'top'
        new_x = root_x
        new_y = root_y + root_height+50

        # Configuration de la géométrie de 'top' pour qu'elle apparaisse juste en dessous de 'self.root'
        self.homework_creation_interface.geometry(f"+{new_x}+{new_y}")
        self.homework_creation_interface.title("Setup - Création manuelle d'un devoir")

        class_directory = 'classes'
        class_code_files = [f.replace('.csv', '') for f in os.listdir(class_directory) if f.endswith('.csv')]
        self.combo_class_code = ctk.CTkComboBox(self.homework_creation_interface, values=class_code_files, state="normal")
        self.combo_class_code.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        ctk.CTkLabel(self.homework_creation_interface, text="Choisir le code classe :").grid(row=0, column=0)

        self.homework_title_entry = ctk.CTkEntry(self.homework_creation_interface)
        self.homework_title_entry.grid(row=1, column=1)
        ctk.CTkLabel(self.homework_creation_interface, text="Titre du devoir:").grid(row=1, column=0)
        
        # Entrée pour la date
        self.homework_date_entry = day_ui(self.homework_creation_interface)#ctk.CTkEntry(self.homework_creation_interface)
        self.homework_date_entry.grid(row=2, column=1)
        ctk.CTkLabel(self.homework_creation_interface, text="Date (JJ/MM/AAAA):").grid(row=2, column=0)
        
        # Entrée pour les exercices et le barème
        self.exercises_entry = ctk.CTkEntry(self.homework_creation_interface)
        self.exercises_entry.grid(row=3, column=1)
        ctk.CTkLabel(self.homework_creation_interface, text="Barème (ex: 2,5,3):").grid(row=3, column=0)

        # Entrée pour les explications
        self.explanations_entry = ctk.CTkEntry(self.homework_creation_interface)
        self.explanations_entry.grid(row=4, column=1)
        ctk.CTkLabel(self.homework_creation_interface, text="Explications (ex: explication 1,explication 2,...):").grid(row=4, column=0)
        
        ctk.CTkButton(self.homework_creation_interface, text="Créer Devoir", command=self.create_homework).grid(row=5, column=0, columnspan=2)
        

    def create_homework(self):
        print("allo")
        classe_code=self.combo_class_code.get()
        print("classe_code_ok")
        self.class_code=classe_code
        title = self.homework_title_entry.get()
        print("title_ok")
        try:
            date_devoir = self.homework_date_entry.submit(option = "underscore")
            print(date_devoir)
        except ValueError:
            return
        if date_devoir =="":
            date_devoir = date.today().strftime("%d_%m_%Y")  # Formats the date as 'YYYY-MM-DD'
        bareme = self.exercises_entry.get().split(',')
        exercises=[0]*len(bareme)
        #if self.explanations_entry=="":
        explication=self.explanations_entry.get().split(',')
        #print(explication)
        self.homework_info = {
            'title': title,
            'date': date_devoir,
            'exercises': exercises,
            'bareme': bareme,
            'explications': explication
        }
        self.homework_creation_interface.destroy()
        self.generate_csv(classe_code)

    def generate_csv(self,classe_code=""):
        # Charger le fichier CSV de la classe s'il n'est pas déjà chargé
        if self.students_df is None:
            if classe_code=="":
                class_code = simpledialog.askstring("Code Classe", "Entrez le code de la classe:")
            else:
                class_code=classe_code
            try:
                self.students_df = pd.read_csv(f"classes/{class_code}.csv", sep=";")
                print(f"self.students_df : \n{self.students_df}")
            except FileNotFoundError:
                messagebox.showerror("Erreur", "Fichier de classe non trouvé")
                return
        if not hasattr(self,'class_code'):
            self.class_code=class_code
        # Préparer les nouvelles colonnes s'il y a lieu
        if 'Date' not in self.students_df.columns:
            self.students_df['Date'] = self.homework_info['date']
        if 'Exercices' not in self.students_df.columns:
            liste=['0']*len(self.homework_info['bareme'])
            self.students_df['Exercices'] = ','.join(liste)#','.join(self.homework_info['exercises'])
        if 'Bareme' not in self.students_df.columns:
            self.students_df['Bareme'] = ','.join(self.homework_info['bareme'])
        if 'Explications' not in self.students_df.columns:
            self.students_df['Explications'] = ','.join(self.homework_info['explications'])
        if 'Competences' not in self.students_df.columns:
            comps=[value for key,value in self.homework_info['competences'].items()]
            labels = []
            for v in comps:
                labels.append(' et '.join([f"{subvalue['code']} - {subvalue['nomcomplet']}" for key,subvalue in v.items()]))
            self.students_df['Competences'] = ','.join(labels)
        # Vérification et mise à jour des données de chaque ligne
        for i, row in self.students_df.iterrows():
            if pd.isnull(row['Date']):
                self.students_df.at[i, 'Date'] = self.homework_info['date']
            if pd.isnull(row['Exercices']):
                self.students_df.at[i, 'Exercices'] = ','.join(self.homework_info['exercises'])
            if pd.isnull(row['Bareme']):
                self.students_df.at[i, 'Bareme'] = ','.join(self.homework_info['bareme'])
            if pd.isnull(row['Explications']):
                self.students_df.at[i, 'Explications'] = ','.join(self.homework_info['explications'])
        # Sauvegarder le fichier CSV modifié
        output_csv_filepath = f"devoirs_effectues/{class_code}/csv/devoir_{self.homework_info['title']}_{self.homework_info['date']}.csv"
        os.makedirs(f'devoirs_effectues/{class_code}/csv', exist_ok=True)
        self.students_df.to_csv(output_csv_filepath, sep=';', index=False, quoting=csv.QUOTE_NONE, quotechar="", escapechar="\\")

        # Reconfigurer les boutons pour les étudiants après mise à jour du fichier
        self.setup_student_buttons()

    def setup_student_buttons(self):
        
        top = ctk.CTkToplevel(self.root)
        def on_close():
            self.root.deiconify()
            top.destroy()

        top.protocol("WM_DELETE_WINDOW", on_close)
        
        self.root.iconify()
        self.clear_widget(top)
        top.title("Sélection des Élèves")
        #top.attributes("-topmost", True)
        # Configurez ici la largeur de la fenêtre si nécessaire
        window_width = 180  # Exemple de largeur fixe
        
        # Obtenez la largeur de l'écran
        screen_width = self.root.winfo_screenwidth()
        
        # Calculez la position X pour que la fenêtre apparaisse à droite
        position_x = 0
        
        # Définissez la géométrie de la fenêtre
        top.geometry(f"{window_width}x500+{position_x}+180")
        print(f"iterrows : {self.students_df.iterrows()}")
        for i, student in self.students_df.iterrows():
            #name = f"{student['Nom']} {student['Prenom']}"
            button = ctk.CTkButton(top, text=f"{student['Nom']} {student['Prenom']}", command=lambda s=student, t=top: self.open_grade_entry(s,t))
            button.pack(fill='x')

    def open_grade_entry(self, student, parent):
        parent.iconify()
        
        popup = ctk.CTkToplevel(self.root)
        def on_close():
            parent.deiconify()
            popup.destroy()

        popup.protocol("WM_DELETE_WINDOW", on_close)
        
        popup.title(f"{student['Prenom']} {student['Nom']} - Notes")
        popup.geometry('+0+0')
        popup.attributes("-topmost", True)  # Keeps window on top
        entries = []

        # Comptage du nombre d'exercices à partir de la liste des exercices
        num_exercises = len(self.homework_info['bareme'])

        # Stocke les valeurs actuelles des exercices de l'étudiant qui seront utilisées plus tard dans les placeholders
        try:
            placeholder_exo:list = student['Exercices'].split(',')
            print(placeholder_exo)
            for index,x in enumerate(placeholder_exo):
                if x=='':
                    placeholder_exo[index]=0
            somme = sum([float(x) for x in placeholder_exo])
        except AttributeError or ValueError:
            placeholder_exo = ['0'] * num_exercises
            somme=0
        
        # Variable pour le label de la note actuelle
        current_grade_text = StringVar()
        current_grade_text.set(f"Note actuelle : {somme} / {sum(map(float, self.homework_info['bareme']))}")

        def update_current_grade():
            try:
                total_grade = sum(float(entry.get() or 0) for entry in entries)
                total_bareme = sum(map(float, self.homework_info['bareme']))
                current_grade_text.set(f"Note actuelle : {total_grade} / {total_bareme}")
            except ValueError:
                messagebox.showerror("Erreur", "Veuillez entrer des nombres valides pour les notes.")

        # Ajout des entrées pour chaque exercice
        for i in range(num_exercises):
            ctk.CTkLabel(popup, text=f"Note pour l'exercice {i+1}:").grid(row=i, column=0)
            entry = ctk.CTkEntry(popup, placeholder_text=placeholder_exo[i])
            entry.insert(0,placeholder_exo[i])
            
            entry.grid(row=i, column=1)
            entry.bind("<KeyRelease>", lambda event, e=entry: update_current_grade())
            entry.bind("<Return>", lambda event, i=i: on_enter_press(event, i))
            entries.append(entry)
            ctk.CTkLabel(popup, text=f"/{self.homework_info['bareme'][i]} (barème)").grid(row=i, column=2)
            #if i == 0:  # Positionne le curseur dans le premier Entry créé
        

        # Ajout du label de la note actuelle
        ctk.CTkLabel(popup, textvariable=current_grade_text).grid(row=num_exercises, columnspan=3, pady=10)


        def save_grades():
            grades = ""
            for entry in entries:
                grades += ("," + entry.get()) if entry.get() else ",0"  # Utilisation de 0 comme note par défaut si rien n'est entré
            grades = grades[1:]  # Supprimer la première virgule

            # Mise à jour des notes pour l'étudiant concerné dans le DataFrame
            condition = (self.students_df['Nom'] == student['Nom']) & (self.students_df['Prenom'] == student['Prenom'])
            self.students_df.loc[condition, 'Exercices'] = grades

            student['Exercices']=grades
            # Sauvegarder les modifications dans le CSV
            self.students_df.to_csv(f"devoirs_effectues/{self.class_code}/csv/devoir_{self.homework_info['title']}_{self.homework_info['date']}.csv", sep=';', index=False)
            parent.deiconify()
            popup.destroy()

        # Gestion de l'appui sur Entrée
        def on_enter_press(event, index):
            if index < num_exercises - 1:
                entries[index + 1].focus_set()
                entries[index + 1].select_range(0, 'end')
                entries[index + 1].icursor('end')
            else:
                save_grades()
        
        # Modifier l'utilisation du bouton et du bind pour utiliser une fonction lambda
        ctk.CTkButton(popup, text="Valider", command=lambda: save_grades()).grid(row=num_exercises+1, column=0, columnspan=2)
        #popup.bind("<Return>", lambda event: save_grades())
        popup.update()
        entries[0].focus_set()
        entries[0].select_range(0, 'end')
        entries[0].icursor('end')
        entries[0].grid(row=0, column=1)
        #ctk.CTkLabel(popup, text=f"/{self.homework_info['bareme'][0]} (barème)").grid(row=0, column=1)

    def clear_widget(self, parent):
        for widget in parent.winfo_children():
            widget.destroy()
    def setup_compilation_parameters(self):
        print("""
                A implémenter : 
              permet via l'ouverture d'un formulaire adapté de demander à l'utilisateur de préciser les paramètres suivants : 
              1. la date qui sera convertie au format %dd_%mm_%yyyy : 3 entrées texte demandant une date avec le label au dessus de la case qui indique JJ , MM ou YYYY pour préciser le format attendu.
              2. le code classe : menu déroulant permettant de choisir la classe ( déterminés à partir des noms des sous répertoires dans le dossier "devoirs_effectues" )
              3. le devoir : menu déroulant permettant de choisir quel devoir sera compilé. les devoirs présents ici seront les intitulés des fichiers csv présents dans le dossier f"devoirs_effectues/{code_classe}/{date}.csv"
              4. le code latex décrivant les thèmes abordés. ( exemple montré avec un begin itemize theme 1 ,item theme 2 etc pour montrer a l'utilisateur la bonne pratique)
              une fois ces paramètres déterminés, on permet à l'utilisateur de compiler via un bouton "Fabriquer le récapitulatif du devoir".
              Pour cela on appelle la fonction : create_recapt_and_compile
              """)
    def create_full_year_and_compile(self,code_classe,date_min,date_max):
        #fabrication du student pour le recap :
        tex_report_maker = YearRecap(f"{code_classe}",date_min,date_max)
        tex_report=tex_report_maker.make_tex_recap()
        print(tex_report)

    def create_recap_and_compile(self,code_classe,date_avec_underscores,theme=""):
        
        date_under = date_avec_underscores.split('_')[-3:]
        title='_'.join(date_avec_underscores.split('_')[:-3][1:])
        #print(title)
        if theme=="":
            theme=title
        
        date_avec_underscores='_'.join(date_under)
        #print(date_under)
        #fabriquation d'une date au format jj/mm/yyyy à partir de la date précédemment recueillie
        date_classique='/'.join(date_under)#self._format_date_underscore_to_classical('_'.join(date_under))

        #fabrication du student du devoir :
        student_manager = Student(f"{code_classe}",f"{date_classique}")
        student_manager.add_student_data_by_csv(csv_filepath= f"classes/{code_classe}.csv")
        student_manager.load_students()
        student_manager.add_devoir_to_students(theme=theme,class_code=f"{code_classe}",date=date_avec_underscores,themes=theme,title=title)
        #student_manager.add_devoir_to_students(f"devoirs_effectues/{code_classe}/csv/{date_avec_underscores}.csv",theme=theme,mode="flat")
        student_manager.save_students_to_json()
        '''print("""
             on applique les fonctionnalités du module database_sender :
              1. fabriquation d'une date au format jj/mm/yyyy à partir de la date précédemment recueillie
              2. fabrication du student du devoir :
                    student_manager = Student(f"{code_classe}","{date_nouvellement_fabriquee}")
              3. Chargement des données dans le student : 
                    student_manager.add_student_data_by_csv(csv_filepath= "classes/{code_classe}.csv")
              4. Chargement supplémentaire permettant d'initier un certain nombre de choses : 
                    student_manager.load_students()
              5. Ajouter le devoir aux étudiants : 
              student_manager.add_devoir_to_students(f"devoirs_effectues/{code_classe}/csv/{date_avec_underscores}.csv",theme={theme})
              6. Sauvegarder le devoir pour les étudiants :
                    student_manager.save_students_to_json()
        """)'''
    def _format_date_underscore_to_classical(self, date_str):
        """
        Convertit une date au format aaaa_mm_jj en jj/mm/yyyy.
        """
        day, month,year  = date_str.split('_')
        formatted_date = f"{day}/{month}/{year}"
        return formatted_date
    def _format_date_classical_to_underscore(self,date_str):
        day,month,year=date_str.split('\\')
        if year and month and day :
            formatted_date=f"{day}_{month}_{year}"
        else:
            formatted_date=date_str
        return formatted_date
    def export_year_pdf(self):
        interface_selector=UIYearSelector(function_caller=self,parent=self.root,topmost=True)

if __name__ == "__main__":
    root = ctk.CTk()
    app = HomeworkManager(root)
    root.mainloop()

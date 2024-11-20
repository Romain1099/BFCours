import os
import shutil
import re
import customtkinter as ctk
from tkinter import filedialog,messagebox
import time
import pygetwindow as gw
import pyautogui
from document_handlers.document_handler import DocumentHandler
from document_handlers.model_modder import ModelModder
import sys
# Gestion des chemins en mode compilé
from datetime import date, datetime
import time
import mysql.connector
import json
import subprocess  # Pour exécuter des commandes externes comme VSCode

# Importer les modules après avoir ajouté le chemin
from document_handlers.scrollable_dropdown import CTkScrollableDropdownFrame, CTkScrollableDropdown
# Initialiser CustomTkinter
ctk.set_appearance_mode("System")  # Système ou "Light" ou "Dark"
ctk.set_default_color_theme("blue")  # Thème "blue", "dark-blue", "green"

class PreferencesForm(ctk.CTkToplevel):
    def __init__(self, master=None, preferences_file="document_cfg/app_preferences.json"):
        super().__init__(master)
        
        self.title("Préférences")
        self.geometry("400x300")
        
        self.preferences_file = preferences_file
        self.preferences = self.load_preferences()  # Charger les préférences depuis le fichier

        # Créer les champs du formulaire en fonction des préférences
        self.create_form()

    def create_form(self):
        """Créer les champs de préférences pour l'interface graphique"""
        # Example: Ajouter une préférence pour ouvrir dans VSCode ou non
        self.open_in_vscode = ctk.CTkSwitch(self, text="Ouvrir dans VSCode")
        self.open_in_vscode.pack(pady=10)
        self.open_in_vscode.select() if self.preferences["open_in_vscode"] == "True" else self.open_in_vscode.deselect()
        
        # Example: Ajouter une préférence pour ouvrir dans VSCode ou non
        label=ctk.CTkLabel(self,text="Chemin vers VSCode")
        label.pack(pady=10)
        self.vscode_path = ctk.CTkEntry(self)#, text=r"C:\Users\Utilisateur\AppData\Local\Programs\Microsoft VS Code\Code.exe")
        self.vscode_path.pack(pady=10,fill="both",expand=True)
        self.vscode_path.insert(0, self.preferences.get("vscode_path", r"C:\Users\Utilisateur\AppData\Local\Programs\Microsoft VS Code\Code.exe"))

        # Ajouter d'autres préférences ici, comme par exemple la langue ou le thème
        self.theme = ctk.CTkOptionMenu(self, values=["Clair", "Sombre"], width=200)
        self.theme.pack(pady=10,fill="both",expand=True)
        self.theme.set(self.preferences.get("theme", "Clair"))

        # Bouton pour enregistrer les préférences
        self.save_button = ctk.CTkButton(self, text="Enregistrer", command=self.save_preferences)
        self.save_button.pack(pady=20,fill="both",expand=True)

    def load_preferences(self):
        """Charger les préférences depuis un fichier"""
        if os.path.exists(self.preferences_file):
            try:
                with open(self.preferences_file, "r") as f:
                    return json.load(f)
            except:

                return {
                    "open_in_vscode": False,
                    "vscode_path":r"C:\Users\Utilisateur\AppData\Local\Programs\Microsoft VS Code\Code.exe",
                    "theme": "Clair",
                }
        else:
            # Si le fichier n'existe pas, retourner des préférences par défaut
            return {
                "open_in_vscode": False,
                "vscode_path":r"C:\Users\Utilisateur\AppData\Local\Programs\Microsoft VS Code\Code.exe",
                "theme": "Clair",
            }

    def save_preferences(self):
        """Enregistrer les préférences dans un fichier"""
        preferences = {
            "open_in_vscode": str(self.open_in_vscode.get() == 1),
            "theme": self.theme.get(),
            "vscode_path": self.vscode_path.get()
        }
        print(preferences)
        with open(self.preferences_file, "w") as f:
            json.dump(preferences, f, indent=4)

        messagebox.showinfo("Préférences", "Les préférences ont été enregistrées avec succès.")
        self.destroy()

one_file_instructions = '''pyinstaller --onefile --name Nouveau_document_tex_par_modele --icon connaisseur.ico --hidden-import "document_handlers" --add-data "creer_document_tex/document_handlers/*:document_handlers" --noconsole creer_document_tex/Creer_v4.py'''
class Application:
    def __init__(self, root):
        self.root = root
        self.open_preferences = True
        self.dynamic_entries = {}
        self.model_combobox = None
        self.selected_model = None
        self.user_inputs = None  # Variable pour stocker les entrées de l'utilisateur
        self.document_model_folder = "document_model"
        self.document_cfg = "document_cfg"
        self.preferences_file = f"{self.document_cfg}/app_preferences.json"

        self.selected_folder = self.get_folder_path()
        self.title_config_dict = self.get_title_config_dict()
        self.perso_compiler_path=self.load_vscode_path()
        self.versions_needed = self.load_versions_needed()

        # Configurer l'application en fonction des préférences
        try:
            self.preferences=self.load_preferences()

            if self.preferences.get("theme") == "Sombre":
                ctk.set_appearance_mode("dark")
            else:
                ctk.set_appearance_mode("light")
        except:
            option_tab = PreferencesForm(self.root,preferences_file=self.preferences_file)

        self.load_additionnal_commands()
        if not self.selected_folder:
            print("Aucun fichier sélectionné.")
            return
        self.setup_interface()
    def load_vscode_path(self):
        perso_path = self.title_config_dict.get("vscode_path",r"C:\Users\Utilisateur\AppData\Local\Programs\Microsoft VS Code\Code.exe")
        
        return perso_path
    def load_preferences(self):
        """Charger les préférences depuis le fichier JSON"""

        if os.path.exists(self.preferences_file):
            try:
                with open(self.preferences_file, "r") as f:
                    return json.load(f)
            except:
                raise AttributeError()
        else:
            return {
                "open_in_vscode": False,
                "theme": "Clair"
            }

    def open_preferences_form(self):
        """Ouvrir la fenêtre des préférences"""
        PreferencesForm(master=self.root)
    def open_models_modder(self):
        """Ouvrir la fenêtre des préférences"""
        ModelModder(master=self.root,models_folder=self.document_model_folder)
    def load_additionnal_commands(self):
        # Charger et exécuter les définitions de commandes depuis commandes.txt
        with open(f'{self.document_cfg}/commandes.txt', 'r', encoding='utf-8') as command_file:
            command_code = command_file.read()
            exec(command_code, globals())  # Charger les fonctions définies dans commandes.txt

    def get_title_config_dict(self):
        # Définir le chemin vers le fichier config_title.txt
        config_file_path = os.path.join(self.document_cfg, "config_title.txt")
        
        # Lire le contenu du fichier
        #with open(config_file_path, 'r', encoding='utf-8') as file:
        #    file_content = file.read()
        
        # Initialiser un dictionnaire vide
        TITLE_CONFIG_DICT = {}

        try:
            # Lire le fichier ligne par ligne
            with open(config_file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    # Ignorer les lignes vides ou les commentaires
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue

                    # Extraire les clés et valeurs
                    if ":" in line:
                        key, value = line.split(":", 1)  # Diviser la ligne à partir du premier :
                        key = key.strip().strip('"')  # Retirer les guillemets et les espaces
                        value = value.strip().strip('"').strip(",")  # Nettoyer la valeur
                        
                        # Ajouter au dictionnaire
                        TITLE_CONFIG_DICT[key] = value

            return TITLE_CONFIG_DICT

        except FileNotFoundError:
            print(f"Le fichier {config_file_path} est introuvable.")
            return None
        except Exception as e:
            print(f"Erreur lors du chargement du fichier de configuration : {e}")
            return None

    def get_folder_path(self, title="Choisir un dossier"):
        folder_selected = filedialog.askdirectory(parent=self.root, title=title)
        return folder_selected

    def copy_file(self, source, destination, new_name):
        if not os.path.exists(destination):
            os.makedirs(destination)
            #print(f'dossier créé : {destination}')
        shutil.copy(source, os.path.join(destination, new_name))

    def setup_interface(self):
        # Obtenir la largeur et la hauteur de l'écran
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculer une taille adaptée (par exemple 80% de la largeur et 80% de la hauteur de l'écran)
        window_width = int(screen_width * 0.8)
        self.window_width=window_width
        window_height = int(screen_height * 0.7)
        self.window_height = window_height
        # Appliquer cette taille à la fenêtre
        self.root.geometry(f"{window_width}x{window_height}")

        # Centrer la fenêtre à l'écran
        x_position = int((screen_width - window_width) / 2 -200)
        y_position = int((screen_height - window_height) / 2 -166)
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Configurer la grille pour l'adapter dynamiquement
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Label pour sélection du modèle
        model_label = ctk.CTkLabel(self.root, text="Sélectionnez un modèle :")
        model_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Combobox pour la liste des modèles
        values = self.get_available_models()
        self.model_combobox = ctk.CTkComboBox(self.root, values=values, width=300, command=self.on_model_selected)
        self.model_combobox.grid(row=0, column=1,columnspan=2, padx=10, pady=10, sticky="nsew")
        if "Exercices light" in values:
            self.model_combobox.set("Exercices light")

        # Label pour sélection du modèle
        model_label = ctk.CTkLabel(self.root, text="Titre du document :")
        model_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        self.title_entry = ctk.CTkEntry(self.root, width=300)
        
        self.title_entry.insert(0, "Nouveau_document")
        self.title_entry.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Label pour sélection du modèle
        #model_label = ctk.CTkLabel(self.root, text="Créer un dossier pour le document :")
        #model_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        # CheckBox pour créer un dossier, lié à une variable de self
        self.create_folder_var = ctk.BooleanVar(value=True)
        self.create_folder_checkbox = ctk.CTkCheckBox(self.root, variable=self.create_folder_var,text="Créer un dossier pour le document :")
        self.create_folder_checkbox.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # Afficher le bouton pour ouvrir les préférences
        self.button_preferences = ctk.CTkButton(self.root, text="Ouvrir les Préférences", command=self.open_preferences_form)
        self.button_preferences.grid(row=2, column=2, columnspan=1, padx=10, pady=10, sticky="nsew")
        
        # Afficher le bouton pour gérer les modèles
        self.button_model_mod = ctk.CTkButton(self.root, text="Gérer les Modèles", command=self.open_models_modder)
        self.button_model_mod.grid(row=2, column=1, columnspan=1, padx=10, pady=10, sticky="nsew")
        
        # Frame dynamique à l'intérieur du Canvas
        self.dynamic_field_frame = ctk.CTkScrollableFrame(self.root,height=window_height-330)
        self.dynamic_field_frame.grid(row=4,columnspan=3, padx=10, pady=30, sticky="nsew")
        
        # Bouton de soumission
        submit_button = ctk.CTkButton(self.root, text="Soumettre", command=self.submit_user_inputs)
        submit_button.grid(row=5, columnspan=2, padx=10, pady=20)
                    
        self.on_model_selected("Exercices light")

    def get_available_models(self):
        directory = self.document_model_folder#"document_model"
        models = [f.replace(".tex","") for f in os.listdir(directory) if f.endswith('.tex')]
        return models

    def on_model_selected(self, choice):
        self.selected_model : str = f"{os.path.join(self.document_model_folder, choice)}.tex"
        self.change_title_for_model(choice=f"{choice}.tex")
        self.update_dynamic_fields()

    def change_title_for_model(self,choice):
        # Vérifier si le choix existe dans le dictionnaire
        if choice in self.title_config_dict:
            # Récupérer la commande à exécuter
            command = self.title_config_dict[choice]
            
            try:
                # Si la commande est une fonction définie dans le fichier commandes.txt, l'exécuter via globals()
                if command in globals():
                    result = globals()[command]()  # Exécuter la fonction
                else:
                    result = command  # Si ce n'est pas une fonction, l'utiliser tel quel comme un titre
                
                
                # Insérer le titre généré dans l'entrée de titre
                self.title_entry.delete(0, "end")  # Supprimer le contenu existant
                self.title_entry.insert(0, f"{result}")  # Insérer le nouveau titre

            except Exception as e:
                print(f"Erreur lors de l'exécution de la commande pour {choice} : {e}")
        else:
            print(f"Aucun titre configuré pour le modèle {choice}")

    def update_dynamic_fields(self):
        # Effacer les anciens champs
        for widget in self.dynamic_field_frame.winfo_children():
            widget.destroy()

        # Charger les nouveaux champs depuis le modèle sélectionné
        replacement_fields = self.detect_replacement_fields(self.selected_model)

        # Affichage dynamique des champs à remplacer dans le modèle
        self.dynamic_entries = {}
        row = 1
        i=0
        j=0
        # Configurer la grille principale pour que les colonnes aient le même poids
        # Définir une largeur constante pour les `Entry` et les `Label`
        entry_width = 275
        label_width = 100  # Largeur minimum pour les labels afin d'aligner correctement les colonnes

        for col in range(3):
            self.dynamic_field_frame.grid_columnconfigure(col, weight=1)  # Poids égal pour chaque colonne

        for field, default_value in replacement_fields.items():
            subframe = ctk.CTkFrame(self.dynamic_field_frame)
            subframe.grid(row=i, column=j, padx=10, pady=10, sticky="nsew")

            # Création du label avec une largeur fixe
            label = ctk.CTkLabel(subframe, text=f"{field} :", width=label_width, anchor="w")  # Aligné à gauche avec anchor="w"
            label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

            # Si plusieurs options, on les met dans un combobox déroulant
            if ',' in default_value:
                options = [opt.strip() for opt in default_value.split(',')]
                frame = ctk.CTkFrame(subframe)
                frame.grid(row=0, column=1, padx=10, pady=5, sticky="e")
                
                # Créer un champ d'entrée avec une largeur fixe
                entry = ctk.CTkEntry(frame, width=entry_width)
                entry.grid(row=0, column=0, padx=10, pady=5, sticky="w")

                # Dropdown avec autocomplétion
                dropdown = CTkScrollableDropdown(entry, values=options, command=lambda e, label_entry=entry: self.insert_method(e, label=label_entry), autocomplete=True)
                self.insert_method(options[0], entry)

            else:
                frame = ctk.CTkFrame(subframe)
                frame.grid(row=0, column=1, padx=10, pady=5, sticky="e")
                
                # Créer un champ d'entrée avec une largeur fixe
                entry = ctk.CTkEntry(frame, width=entry_width)
                entry.insert(0, default_value)
                entry.grid(row=0, column=1, padx=10, pady=5, sticky="e")

            # Stocker l'entrée dans le dictionnaire
            self.dynamic_entries[field] = entry

            # Gestion des colonnes et lignes
            j += 1
            if j > 2:  # Passer à la ligne suivante après 3 colonnes
                j = 0
                i += 1
                    
        
        # Rafraîchir la frame pour s'assurer que tout est bien affiché
        #self.dynamic_field_frame.update_idletasks()
    
         
    def detect_replacement_fields(self, model_path):
        fields = {}
        field_pattern = r"%\s*(\w+)\s*:\s*(.*)"  # Pattern pour détecter les champs
        command_pattern = r"commande\((\w+)\((.*?)\)\)"
        command_pattern_2 = r"\\\w+\{commande\((\w+)\((.*?)\)\)\}"  # Nouveau pattern pour détecter les commandes dans \messageIntro

        # Charger le contenu du fichier LaTeX
        with open(model_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Trouver tous les champs définis par % nom_champ : valeur
        matches = re.findall(field_pattern, content)

        if matches:
            
            for match in matches:

                field_name = match[0]  # nom_champ
                try:
                    default_value = match[1]  # valeur ou commande
                except IndexError:
                    default_value = ""

                # Vérifier si la valeur du champ correspond à une commande
                command_match = re.match(command_pattern, default_value)
                command_match_2 = re.match(command_pattern_2, default_value)
                if command_match or command_match_2:
                    if command_match:
                        command_name = command_match.group(1)  # Récupérer le nom de la commande
                        try:
                            command_param = command_match.group(3)  # Récupérer un éventuel paramètre
                        except:
                            command_param = None
                    if not command_match and command_match_2:
                        command_name = command_match_2.group(1)  # Récupérer le nom de la commande
                        try:
                            command_param = command_match_2.group(3)  # Récupérer un éventuel paramètre
                        except:
                            command_param = None
                    # Vérifier si la commande est définie dans commandes.txt
                    if command_name in globals():
                        try:
                            if command_param:
                                # Exécuter la commande avec un paramètre
                                globals()[command_name](command_param)
                                fields[field_name] = globals()[command_name](command_param)
                            else:
                                # Exécuter la commande sans paramètre
                                #globals()[command_name]()
                                fields[field_name] = globals()[command_name]()
                        except Exception as e:
                            print(f"Erreur lors de l'exécution de la commande '{command_name}': {e}")
                    else:
                        print(f"La commande '{command_name}' n'est pas définie dans commandes.txt.")
                else:
                    # Si ce n'est pas une commande, enregistrer la valeur par défaut
                    fields[field_name] = default_value
        return fields

    def insert_method(self, e, label):
        label.delete(0, 'end')
        try:
            entry_text = e
            label.insert(0, entry_text)
        except IndexError:
            label.insert(0, e)

    def submit_user_inputs(self):
        self.user_inputs = {}
        #print("submit_user_inputs")
        for field, entry in self.dynamic_entries.items():
            self.user_inputs[field] = entry.get()
            #print(f"field {field} : get {entry.get()}")
        self.use_case_two()

        
    def replace_fields_in_model(self, model_content):
        # Utiliser les valeurs saisies pour remplacer les champs dynamiques dans le modèle
        for field, user_value in self.user_inputs.items():
            #print(f"% {field}")
            model_content = model_content.replace(f"% {field}", f"{user_value}%")
        return model_content

    def create_folder(self, folder_path):
        """
        Crée le dossier spécifié s'il n'existe pas déjà.
        """
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Dossier créé : {folder_path}")
        else:
            raise ValueError(f"Le dossier {folder_path} existe déjà.")

    def detect_input_files(self, model_content: str) -> list:
        """
        Analyse le contenu du modèle LaTeX pour détecter les fichiers inclus via \input{} ou \include{}.
        Retourne une liste des noms de fichiers.
        """
        input_files = []
        # Regex pour détecter les \input{filename} ou \include{filename}
        input_pattern = r"\\(?:input|include|inputImprim)\{(.+?)\}"
        matches = re.findall(input_pattern, model_content)
        if matches:
            input_files.extend(matches)
        #print(input_files)
        input_files = {file for file in input_files if file != r'\impressFileName'}
        #print(input_files)
        input_files = [file for file in input_files]
        #print(input_files)
        return input_files

    def create_files(self, folder_path, input_files: list):
        """
        Crée les fichiers spécifiés dans la liste 'input_files' dans le dossier 'folder_path'.
        """
        for file_name in input_files:
            file_path = os.path.join(folder_path, f"{file_name}.tex")
            if not os.path.exists(file_path):
                open(file_path, 'w').close()  # Crée un fichier vide
                print(f"Fichier créé : {file_path}")
            else:
                raise ValueError(f"Le fichier {file_path} existe déjà.")
    def load_versions_needed(self):
        # Initialiser un dictionnaire vide
        VERSIONS_CONFIG_DICT = {}
        cfg_file=f"{self.document_cfg}/config_versions.txt"
        try:
            # Lire le fichier ligne par ligne
            with open(cfg_file, 'r', encoding='utf-8') as file:
                for line in file:
                    # Ignorer les lignes vides ou les commentaires
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue

                    # Extraire les clés et valeurs
                    if ":" in line:
                        key, value = line.split(":", 1)  # Diviser la ligne à partir du premier :
                        key = key.strip().strip('"')  # Retirer les guillemets et les espaces
                        value = value.strip().strip('"').strip(",")  # Nettoyer la valeur
                        
                        # Ajouter au dictionnaire
                        VERSIONS_CONFIG_DICT[key] = value

            return VERSIONS_CONFIG_DICT
        
        except FileNotFoundError:
            print(f"Le fichier {cfg_file} est introuvable.")
            return None
        except Exception as e:
            print(f"Erreur lors du chargement du fichier de configuration : {e}")
            return None
    def get_versions_needed(self,folder_path,file_name)->list[str]:
        """
        Renvoie la liste des paths des versions à créer pour le type de document sélectionné
        """
        versions = self.versions_needed[self.selected_model].split("-")
        liste = [os.path.join(folder_path, f"{v}_{file_name}.tex") for v in versions]
        return liste
    def use_case_two(self):
        if self.user_inputs is None:
            return  # Handle the case where the user cancels the input

        new_folder_wanted=self.create_folder_var.get()
        if new_folder_wanted:
            new_folder = os.path.join(self.selected_folder, self.title_entry.get())
            try:
                self.create_folder(new_folder)
            except ValueError as e:
                messagebox.showerror("Erreur", f"{e}")
                raise ValueError
        else:
            new_folder = self.selected_folder
        chemin_fichier_copie = os.path.join(new_folder, f"{self.title_entry.get()}.tex")

        # Lire le modèle
        with open(self.selected_model, 'r', encoding='utf-8') as file:
            model_content = file.read()
        
        # Remplacer les champs dynamiques dans le modèle
        model_content = self.replace_fields_in_model(model_content)

        input_file_names:list = self.detect_input_files(model_content)
        versions=self.get_versions_needed()
        input_file_names.extend(versions)
        try:
            self.create_files(new_folder,input_file_names)
        except ValueError as e:
            messagebox.showerror("Erreur", f"{e}")
            raise(ValueError)

        # Créer le fichier final avec le contenu mis à jour
        with open(chemin_fichier_copie, 'w', encoding='utf-8') as file:
            file.write(model_content)

        # Organiser les fenêtres avec les fichiers générés
        self.organiser_fenetres(chemin_fichier_copie, chemin_fichier_copie, chemin_fichier_copie, self.user_inputs.get("Nom du fichier", "Test"))
        
    def organiser_fenetres(self, chemin_fichier_copie, chemin_input_enonce, chemin_input_solution, titre_fenetre_principale):
        # Ouvrir le dossier contenant le fichier principal
        chemin_dossier_principal = os.path.dirname(os.path.abspath(chemin_fichier_copie))
        if self.open_preferences:
            self.ouvrir_dossier(chemin_dossier_principal)
        else:
            self.ouvrir_dossier(chemin_dossier_principal)    
            # Ouvrir les fichiers
            self.ouvrir_dossier(chemin_fichier_copie)

    def ouvrir_dossier(self, chemin):
        if self.open_preferences:
            vscode_path=self.perso_compiler_path
            if vscode_path:
                subprocess.Popen([vscode_path, chemin])
            else:
                os.startfile(chemin)  # Ouvrir avec l'application par défaut
        else:
            os.startfile(chemin)

    def ouvrir_dossier_old(self, chemin):
        os.startfile(chemin)


# Exemple d'utilisation
if __name__ == "__main__":
    root = ctk.CTk()  # Créer l'objet root (la fenêtre principale)
    app = Application(root)
    root.mainloop()  # Démarrer la boucle principale de la fenêtre

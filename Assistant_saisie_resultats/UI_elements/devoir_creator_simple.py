import customtkinter as ctk
import os
import json
#from competence_displayer import CompetenceDisplayer
try:
    from datetime_selector import day_ui
    from scrollable_dropdown import CTkScrollableDropdown
except:
    from UI_elements.datetime_selector import day_ui
    from UI_elements.scrollable_dropdown import CTkScrollableDropdown
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"
import mysql.connector
def get_db_config():
    # Configuration de la connexion à la base de données
    return {
        'host': 'localhost',
        'user': 'admin',
        'password': 'mot_de_passe',  # Remplacez par votre mot de passe
        'database': 'coursdb'
    }
default_db_manager=False
def get_data_as_json(query,params=None):
    if default_db_manager == False:
        return {}
    db_config=get_db_config()

    # Connexion à la base de données
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Exécuter la requête
    if params:
        cursor.execute(query,params=params)
    else:
        cursor.execute(query)

    # Récupérer les noms des colonnes
    columns = [desc[0] for desc in cursor.description]

    # Récupérer les résultats (liste de tuples)
    result = cursor.fetchall()

    # Convertir les résultats en une liste de dictionnaires
    result_as_dict = [dict(zip(columns, row)) for row in result]

    # Fermer la connexion
    cursor.close()
    conn.close()

    # Convertir le résultat en JSON
    return json.loads(json.dumps(result_as_dict, indent=4))


class HomeworkSetupUI:
    def __init__(self, root,callback):
        self.root = root
        self.callback=callback
        self.exercises="1"
        self.db_competencies=self.get_competencies_from_database()
        self.competencies={}
        self.competencies_window=None
        self.homework_creation_interface=None
        self.number_of_competencies_var = ctk.IntVar(value=1)
        self.competency_selectors = {}
        self.number_of_competencies_vars = {}
        self.number_of_exercises_var:int= 1
        self.displayer = None
        self.setup_homework_interface()
        

    def setup_homework_interface(self):
        # Création d'une fenêtre de dialogue en second plan
        if self.homework_creation_interface:
            self.homework_creation_interface.destroy()
        self.homework_creation_interface = ctk.CTkToplevel(self.root)
        
        def on_close():
            self.root.deiconify()
            self.homework_creation_interface.destroy()

        self.homework_creation_interface.protocol("WM_DELETE_WINDOW", on_close)
        
        self.root.iconify()
        #self.homework_creation_interface.attributes("-topmost", True)
        self.homework_creation_interface.title("Setup - Création manuelle d'un devoir")

        class_directory = 'classes'
        class_code_files = [f.replace('.csv', '') for f in os.listdir(class_directory) if f.endswith('.csv')]
        self.combo_class_code = ctk.CTkComboBox(self.homework_creation_interface, values=class_code_files, state="normal")
        self.combo_class_code.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        ctk.CTkLabel(self.homework_creation_interface, text="Choisir le code classe :").grid(row=0, column=0)

        self.homework_title_entry = ctk.CTkEntry(self.homework_creation_interface)
        self.homework_title_entry.grid(row=1, column=1,sticky="nsew")
        ctk.CTkLabel(self.homework_creation_interface, text="Titre du devoir:").grid(row=1, column=0)
        
        self.homework_date_entry = day_ui(self.homework_creation_interface)
        self.homework_date_entry.grid(row=2, column=1,sticky="nsew")
        ctk.CTkLabel(self.homework_creation_interface, text="Date (JJ/MM/AAAA) :").grid(row=2, column=0)
        
        self.exercises_entry = ctk.CTkEntry(self.homework_creation_interface)
        # Bind the <KeyRelease> event to the callback function
        self.exercises_entry.bind("<KeyRelease>", self.analyze_exercices_entry_content)
        
        self.exercises_entry.insert(0,self.exercises)
        self.exercises_entry.grid(row=3, column=1,sticky="nsew")
        ctk.CTkLabel(self.homework_creation_interface, text="Barème (ex: 2,5,3):").grid(row=3, column=0)

        #self.competency_selector.bind("<KeyRelease>",self.add_competence_controls)
        #ctk.CTkLabel(self.homework_creation_interface, text="Nombre de compétences:").grid(row=4, column=0)

        # Ajouter une section pour configurer les exercices avec des onglets
        self.tabs = ctk.CTkTabview(self.homework_creation_interface)
        self.tabs.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.exercises_competences = {}
        self.add_competence_controls()

        ctk.CTkButton(self.homework_creation_interface, text="Créer Devoir", command=self.create_homework).grid(row=9, column=0, columnspan=2, pady=10,sticky="nsew")
    
    def analyze_exercices_entry_content(self, event):
        # Get the content of the CTkEntry widget
        entry_content = self.exercises_entry.get()
        # Split the content by commas
        elements = entry_content.split(',')
        # Remove any empty strings resulting from consecutive commas or leading/trailing spaces
        elements = [elem.strip() for elem in elements if elem.strip()]
        # Determine the length of the list
        length_of_list = len(elements)
        # Update the label with the length of the list
        self.number_of_exercises_var=int(length_of_list)
        self.add_competence_controls()

    def add_explanations_controls(self,tabs=None,*args):
        if tabs is not None:
            print(f"add_explanations_controls({tabs}) a implémenter")
            exo_setup_tabs = tabs
            self.explanations_entry={}
            return

        else:
            self.explanations_tabs = ctk.CTkTabview(self.homework_creation_interface)
            self.explanations_tabs.grid(row=7, column=6, columnspan=5, padx=10, pady=10, sticky="ew")
            self.explanations_entry={}

        for i in range(0, self.number_of_exercises_var):
            tab = self.explanations_tabs.add(f"Ex {i+1}")
            frame = ctk.CTkFrame(tab)
            frame.grid(row=i, column=0, pady=5, sticky="ew")
            self.explanations_entry[f'exercice_{i}'] = ctk.CTkTextbox(frame, width=300, height=100)
            self.explanations_entry[f'exercice_{i}'].grid(row=1, column=0, columnspan=3, rowspan=2, padx=10, pady=10, sticky="ew")
            ctk.CTkLabel(frame, text=f"Explication en cas de non-réussite à l'exercice {i+1}:").grid(row=0, column=0)

    def add_competence_controls(self,*args):
        """A implémenter de toute urgence"""
        # Ajouter une section pour configurer les compétences avec des onglets
        if not self.tabs:
            self.tabs = ctk.CTkTabview(self.homework_creation_interface)
            self.tabs.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        explanations_entry={}

        for i in range(0, self.number_of_exercises_var):  # Suppose 4 exercises for now, adjust as needed
            try:
                comp_label=self.competencies[i]['Code']
            except:
                comp_label=f"Ex {i+1}"
            print(self.tabs._tab_dict)
            
            if comp_label not in self.tabs._tab_dict:
                tab = self.tabs.add(comp_label)
            else:
                tab=self.tabs._tab_dict[comp_label]
            for widget in tab.winfo_children():
                if widget.widgetName!="frame":
                    widget.destroy()
                else:
                    comp_frame = widget
                
            key = f'ex{i}'
            try:
                if self.number_of_competencies_vars[i]:
                    number_of_competencies=int(self.competency_selectors[i].get())
                else:
                    self.number_of_competencies_vars[i]=ctk.IntVar(value=1)
                    number_of_competencies=int(self.number_of_competencies_vars[i].get())
            except:
                self.number_of_competencies_vars[i]=ctk.IntVar(value=1)
                number_of_competencies=int(self.number_of_competencies_vars[i].get())
            self.competency_selectors[i] = ctk.CTkOptionMenu(tab, variable=self.number_of_competencies_vars[i],
                                                    values=[str(i) for i in range(11)],command=self.add_competence_controls)  # assuming a max of 10 competencies
            self.competency_selectors[i].grid(row=0, column=1)

            #ctk.CTkLabel(self.homework_creation_interface, text="Nombre de compétences:").grid(row=4, column=0)
        
            if key not in self.exercises_competences or not self.exercises_competences[key]:
                self.exercises_competences[f'ex{i}'] = {}

            competences=[f"C{i+1}" for i in range(number_of_competencies)]#['competence1', 'competence2', 'competence3']
            
            max_j=len(competences)
            for j, comp in enumerate(competences):
                first_key = f'ex{i}'
                second_key = f'comp{j}'
                for key,value in tab.__dict__.items():
                    print(f"{key} : {value}")

                frame = ctk.CTkFrame(tab)
                frame.grid(row=j+1, column=0,columnspan=2, pady=5, sticky="nsew")


                if second_key not in self.exercises_competences[first_key] or not self.exercises_competences[first_key][second_key]:
                    self.exercises_competences[f'ex{i}'][f'comp{j}']={}
                    checkbox_state="disabled"
                    number_selector_value = ""
                    initial_number=0
                    part_label = ctk.CTkLabel(frame, text=comp).grid(row=1, column=0, padx=5)
                else:
                    checkbox_state = "disabled"
                    try:
                        number_selector_value = self.exercises_competences[f'ex{i}'][f'comp{j}']['number_selector'].get()
                    except:
                        number_selector_value = ""
                    part_label = ctk.CTkLabel(frame, text=comp).grid(row=1, column=0, padx=5)
                    
                    initial_number = self.exercises_competences[f'ex{i}'][f'comp{j}']['number_var']

                competence_selector = ctk.CTkEntry(frame,width=300)
                competence_code_selector = ctk.CTkEntry(frame,width=100)

                competence_selector.insert(0,number_selector_value)
                cc_values = [f"{e['nomCompetence']} ( {e['idCompetence']} )" for e in self.db_competencies]
                dropdown = CTkScrollableDropdown(competence_selector, values=cc_values, command=lambda e, label_entry=competence_selector,cname_entry=competence_code_selector: self.competencies_n_insert_method(e, label=label_entry,code_entry=cname_entry), autocomplete=True)

                competence_selector.grid(row=1, column=1, padx=5,sticky="nsew")
                #competence_code_selector = ctk.CTkEntry(frame)
                dd_values = [f"{e['code_competence']} ( {e['idCompetence']} )" for e in self.db_competencies]
                dropdown = CTkScrollableDropdown(competence_code_selector, values=dd_values, command=lambda e, label_entry=competence_code_selector,cname_entry=competence_selector: self.competencies_insert_method(e, label=label_entry,name_entry=cname_entry), autocomplete=True)

                competence_code_selector.insert(0,number_selector_value)

                competence_code_selector.grid(row=1, column=2, padx=5,sticky="nsew")
                self.exercises_competences[f'ex{i}'][f'comp{j}'] = {
                    'checkbox': "",
                    'number_selector': competence_selector,
                    'comp_code_selector':competence_code_selector,
                    'part_label': part_label,
                    'number_var': initial_number
                }

                for widget in frame.winfo_children():
                    for key,value in widget.__dict__.items():
                        print(f"{key} : {value}")
                    #if widget.widgetName == "frame":
                    for child in widget.winfo_children():
                        print(child._name)
                        print(child._name[-1:])
                        if child.widgetName[-1:].isdigit() and int(child.widgetName[-1:])>=max_j:
                            child.destroy()
            #self.exercises_competences[f'ex{i}']['ratio_label']= ratio_label
            ratio_label_top = ctk.CTkLabel(tab, text="Compétences liées à l'exercice")
            ratio_label_top.grid(row=0, column=0,padx=5)
            
            if 'explanation_entry' in self.exercises_competences[f'ex{i}']:
                #print(self.exercises_competences[f'ex{i}'][f'explanation_entry'].get("0.0","end"))
                temp_text=""#self.exercises_competences[f'ex{i}'][f'explanation_entry'].get("0.0","end")
                explanations_entry[f'exercice_{i}'] = ctk.CTkTextbox(tab, width=300, height=100)
                explanations_entry[f'exercice_{i}'].insert("0.0",temp_text)
            else:
                explanations_entry[f'exercice_{i}'] = ctk.CTkTextbox(tab, width=300, height=100)
            explanations_entry[f'exercice_{i}'].grid(row=1, column=3, columnspan=3, rowspan=2, padx=10, pady=10, sticky="ew")
            
                
            #explanations_entry[f'exercice_{i}'].insert("0",)
            ctk.CTkLabel(tab, text=f"Explication en cas de non-réussite à l'exercice {i+1}:").grid(row=0, column=3,sticky='ew')
            self.exercises_competences[f'ex{i}'][f'explanation_entry'] = explanations_entry[f'exercice_{i}']
        self.explanations_entry = explanations_entry
    def get_competencies_from_database(self)->json:
        print(f"get_competencies")
        wanted_attributes = ['nomCompetence', 'code_competence','idCompetence']
        query = f"SELECT {', '.join(wanted_attributes)} FROM competence;"

        json_data = get_data_as_json(query)
        print(json_data)
        return json_data
    def competencies_n_insert_method(self,event:str, label,code_entry):
        print(f"inserting new_competence_content : event {event}, label {label}")
        label.delete(0, 'end')
        code_entry.delete(0, 'end')
        try:
            entry_text = event.split("(")[0].strip()
            print(f"entry_text : {entry_text}")
            id = event.split("(")[1].split(")")[0].strip()
            print(f"id : {id}")
            name_text= ','.join([e['code_competence'] for e in self.db_competencies if str(e['idCompetence']) == id])
            print(f"name_text : {name_text}")
            label.insert(0, entry_text)
            code_entry.insert(0,name_text)
        except IndexError:
            label.insert(0, event)

    def competencies_insert_method(self,event:str, label,name_entry):
        print(f"inserting new_competence_content : event {event}, label {label}")
        label.delete(0, 'end')
        name_entry.delete(0, 'end')
        try:
            entry_text = event.split("(")[0].strip()
            print(f"entry_text : {entry_text}")
            id = event.split("(")[1].split(")")[0].strip()
            print(f"id : {id}")
            name_text= ','.join([e['nomCompetence'] for e in self.db_competencies if str(e['idCompetence']) == id])
            print(f"name_text : {name_text}")
            label.insert(0, entry_text)
            name_entry.insert(0,name_text)
        except IndexError:
            label.insert(0, event)

    def create_homework(self):
        # Gather all data and create the JSON structure
        try:
            date_devoir = self.homework_date_entry.submit(option = "underscore")
        except Exception as e:
            print("erreur dans la création du devoir : ",e)
            return
        bareme = self.exercises_entry.get().split(",")
        homework_data = {
            "title": self.homework_title_entry.get(),
            "date": date_devoir,
            "explications":[],
            "exercises":[0]*len(bareme),
            "bareme":bareme,
            "competences": {}
        }
        competencies = {}
        explanations_list=[]
        entry_content = self.exercises_entry.get()
        # Split the content by commas
        elements = entry_content.split(',')
        # Remove any empty strings resulting from consecutive commas or leading/trailing spaces
        elements = [elem.strip() for elem in elements if elem.strip()]
        for i in range(0, self.number_of_exercises_var):  # Adjust according to the number of exercises
            exercise_key = f'ex{i}'
            comp_key = f'Ex {i+1}'
            homework_data["competences"][exercise_key] = {}
            competencies[comp_key]={}
            explanations_list.append(self.exercises_competences[exercise_key]['explanation_entry'].get("0.0","end").strip())
            #competencies[comp_key]['explications']=explanations
            j=0
            for key,value in self.exercises_competences[exercise_key].items():
                if key.startswith("comp"):
                    print(f"comp !!! {key} : {value}")
                    comp_label = f"C{j+1}"
                    j+=1
                    comp_name = self.exercises_competences[exercise_key][key]['number_selector'].get()
                    comp_code = self.exercises_competences[exercise_key][key]['comp_code_selector'].get()
                    competencies[comp_key][comp_label]= {
                        'nomcomplet': f"{comp_name}",
                        'code': f"{comp_code}",
                    }
        homework_data["competences"] = competencies
        homework_data["explications"] = explanations_list
        json_file_path = f"homework_{self.homework_title_entry.get().replace(' ', '_').lower()}.json"
        """
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(homework_data, json_file, indent=4, ensure_ascii=False)
        """
        print(json.dumps(homework_data,indent=4,ensure_ascii=False))
        ctk.CTkLabel(self.homework_creation_interface, text=f"Devoir créé et sauvegardé sous {json_file_path}").grid(row=7, column=0, columnspan=2)
        class_code=self.combo_class_code.get()
        print(f"combo_class_code : {self.combo_class_code.get()}")
        self.callback(datas = homework_data,classe_code=class_code)
if __name__=="__main__":
    # Initialiser l'application
    root = ctk.CTk()
    ui = HomeworkSetupUI(root)
    root.mainloop()

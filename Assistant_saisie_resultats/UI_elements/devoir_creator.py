import customtkinter as ctk
import os
import json
from competence_displayer import CompetenceDisplayer
from datetime_selector import day_ui
class HomeworkSetupUI:
    def __init__(self, root):
        self.root = root
        self.exercises="1"
        self.competencies={}
        self.competencies_window=None
        self.homework_creation_interface=None
        self.number_of_competencies_var = ctk.IntVar(value=1)
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
        self.combo_class_code.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        ctk.CTkLabel(self.homework_creation_interface, text="Choisir le code classe :").grid(row=0, column=0)

        self.homework_title_entry = ctk.CTkEntry(self.homework_creation_interface)
        self.homework_title_entry.grid(row=1, column=1)
        ctk.CTkLabel(self.homework_creation_interface, text="Titre du devoir:").grid(row=1, column=0)
        
        self.homework_date_entry = day_ui(self.homework_creation_interface)
        self.homework_date_entry.grid(row=2, column=1)
        ctk.CTkLabel(self.homework_creation_interface, text="Date (JJ/MM/AAAA) :").grid(row=2, column=0)
        
        self.exercises_entry = ctk.CTkEntry(self.homework_creation_interface)
        # Bind the <KeyRelease> event to the callback function
        self.exercises_entry.bind("<KeyRelease>", self.analyze_exercices_entry_content)
        
        self.exercises_entry.insert(0,self.exercises)
        self.exercises_entry.grid(row=3, column=1)
        ctk.CTkLabel(self.homework_creation_interface, text="Barème (ex: 2,5,3):").grid(row=3, column=0)

        
        self.competency_selector = ctk.CTkOptionMenu(self.homework_creation_interface, variable=self.number_of_competencies_var,
                                                     values=[str(i) for i in range(11)],command=self.add_competence_controls)  # assuming a max of 10 competencies
        self.competency_selector.grid(row=4, column=1)
        #self.competency_selector.bind("<KeyRelease>",self.add_competence_controls)
        ctk.CTkLabel(self.homework_creation_interface, text="Nombre de compétences:").grid(row=4, column=0)
        
        #self.no_evaluation_label = ctk.CTkLabel(self.homework_creation_interface, text="pas d'évaluation par compétence")
        #self.no_evaluation_label.grid(row=5, column=0, columnspan=2)

        self.configure_competencies_button = ctk.CTkButton(self.homework_creation_interface, text="Paramétrer les compétences",
                                                           command=self.open_competencies_window)
        self.configure_competencies_button.grid(row=6, column=0, columnspan=2, pady=10)

        # Ajouter une section pour configurer les compétences avec des onglets
        self.tabs = ctk.CTkTabview(self.homework_creation_interface)
        self.tabs.grid(row=7, column=0, columnspan=5, padx=10, pady=10, sticky="ew")

        self.exercises_competences = {}
        self.add_competence_controls()
        # Ajouter une section pour configurer les compétences avec des onglets
        
        self.add_explanations_controls(tabs=self.tabs)

        ctk.CTkButton(self.homework_creation_interface, text="Créer Devoir", command=self.create_homework).grid(row=9, column=0, columnspan=2, pady=10)
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

    def open_competencies_window(self):
        num_competencies = self.number_of_competencies_var.get()
        if self.displayer == None:
            self.displayer = CompetenceDisplayer(root, num_competencies)
        self.displayer.open_competencies_window()
        self.competencies_window=self.displayer.competencies_window
        
    def open_competencies_window_old(self):
        num_competencies = self.number_of_competencies_var.get()
        if num_competencies == 0:
            return  # no competencies to configure
        if self.competencies_window:
            self.competencies_window.destroy()
        self.competencies_window = ctk.CTkToplevel(self.root)
        self.competencies_window.attributes("-topmost", True)

        self.competencies_window.protocol("WM_DELETE_WINDOW", self.get_competencies)

        self.competencies_window.title("Paramétrage des Compétences")
        self.comp_widget={}
        self.find_competencies()
        for i in range(num_competencies):
            ctk.CTkLabel(self.competencies_window, text=f"Compétence {i+1}").grid(row=i*3, column=0, columnspan=2, pady=5)
            self.comp_widget[i]={}
            ctk.CTkLabel(self.competencies_window, text="Compétence :").grid(row=i*3+1, column=0, sticky='e')
            self.comp_widget[i]["Nom"]=ctk.CTkComboBox(self.competencies_window)
            #self.comp_widget[i]["Nom"].configure(values=)
            self.comp_widget[i]["Nom"].grid(row=i*3+1, column=1)

            ctk.CTkLabel(self.competencies_window, text="Code:").grid(row=i*3+2, column=0, sticky='e')
            self.comp_widget[i]["Code"]=ctk.CTkEntry(self.competencies_window)
            self.comp_widget[i]["Code"].insert(0,f"C{i+1}")
            self.comp_widget[i]["Code"].grid(row=i*3+2, column=1)

            """ctk.CTkLabel(self.competencies_window, text="Proportion:").grid(row=i*4+3, column=0, sticky='e')
            self.comp_widget[i]["Proportion"]=ctk.CTkEntry(self.competencies_window)
            self.comp_widget[i]["Proportion"].grid(row=i*4+3, column=1)"""
    def get_competencies(self):
        for i in range(len(self.comp_widget)):
            self.competencies[i]={}
            for label in ["Nom","Code"]:
                self.competencies[i][label]=self.comp_widget[i][label].get()
        
        self.homework_creation_interface.deiconify()
        self.competencies_window.destroy()

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
            self.tabs.grid(row=7, column=0, columnspan=6, padx=10, pady=10, sticky="ew")
        number_of_competencies=int(self.competency_selector.get())
        #self.number_of_competencies_var.get()

        explanations_entry={}
        print(f"self.number_of_exercises_var : {self.number_of_exercises_var}\nnumber_of_competencies : {number_of_competencies}")
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
            key = f'ex{i}'
            if key not in self.exercises_competences or not self.exercises_competences[key]:
                self.exercises_competences[f'ex{i}'] = {}

            competences=[f"C{i+1}" for i in range(number_of_competencies)]#['competence1', 'competence2', 'competence3']
            
            
            for j, comp in enumerate(competences):
                first_key = f'ex{i}'
                second_key = f'comp{j}'
                frame = ctk.CTkFrame(tab)
                frame.grid(row=j+1, column=0, pady=5, sticky="ew")


                if second_key not in self.exercises_competences[first_key] or not self.exercises_competences[first_key][second_key]:
                    self.exercises_competences[f'ex{i}'][f'comp[{j}]']={}
                    checkbox_state="disabled"
                    initial_number=0
                else:
                    checkbox_state = self.exercises_competences[f'ex{i}'][f'comp{j}']['checkbox'].cget('state')
                    number_selector_value = self.exercises_competences[f'ex{i}'][f'comp{j}']['number_selector']
                    part_label = self.exercises_competences[f'ex{i}'][f'comp{j}']['part_label']
                    
                    print(checkbox_state)
                    initial_number = self.exercises_competences[f'ex{i}'][f'comp{j}']['number_var']
                checkbox = ctk.CTkCheckBox(frame, text=comp, command=lambda i=i, j=j: self.toggle_competence(i, j))
                #print(checkbox_state) if checkbox_state else print(checkbox._state)
                #number_var = ctk.IntVar(value=1)  # Default value is 1
                number_selector = ctk.CTkEntry(frame)
                number_selector.insert(0,initial_number)
                #number_selector.insert(0, "1")
                number_selector.bind("<KeyRelease>", lambda event, i=i, j=j: self.modify_ratio_label(event,i, j))
                
                number_selector.configure(state=checkbox_state)
                part_label = ctk.CTkLabel(frame, text="part du ratio")
                    
                    #number_selector.cget()
                
                checkbox.grid(row=1, column=0, sticky="w")

                number_selector.grid(row=1, column=2, padx=5)
                part_label.grid(row=1, column=1, padx=5)
                """button_up = ctk.CTkButton(frame, text="↑", command=lambda i=i, j=j: self.move_competence_up(i, j))
                button_up.grid(row=0, column=3, padx=5)
                button_down = ctk.CTkButton(frame, text="↓", command=lambda i=i, j=j: self.move_competence_down(i, j))
                button_down.grid(row=0, column=4, padx=5)"""
                
                #add_axplanations_controls 
                self.exercises_competences[f'ex{i}'][f'comp{j}'] = {
                    'checkbox': checkbox,
                    'number_selector': number_selector,
                    'part_label': part_label,
                    'number_var': initial_number
                }
            # Calculate and display the ratio label
            ratio_label_text = self.calculate_ratio_label_text(i)
            ratio_label = ctk.CTkLabel(tab, text=ratio_label_text)
            ratio_label.grid(row=len(competences)+1, column=0, pady=10, sticky="ew")
            
            self.exercises_competences[f'ex{i}']['ratio_label']= ratio_label
            ratio_label_top = ctk.CTkLabel(tab, text="Option de calcul par compétence")
            ratio_label_top.grid(row=0, column=0,padx=5)
            if 'explanation_entry' in self.exercises_competences[f'ex{i}']:
                #print(self.exercises_competences[f'ex{i}'][f'explanation_entry'].get("0.0","end"))
                temp_text=self.exercises_competences[f'ex{i}'][f'explanation_entry'].get("0.0","end")
                explanations_entry[f'exercice_{i}'] = ctk.CTkTextbox(tab, width=300, height=100)
                explanations_entry[f'exercice_{i}'].insert("0.0",temp_text)
            else:
                explanations_entry[f'exercice_{i}'] = ctk.CTkTextbox(tab, width=300, height=100)
            explanations_entry[f'exercice_{i}'].grid(row=1, column=3, columnspan=3, rowspan=2, padx=10, pady=10, sticky="ew")
            
            
            #explanations_entry[f'exercice_{i}'].insert("0",)
            ctk.CTkLabel(tab, text=f"Explication en cas de non-réussite à l'exercice {i+1}:").grid(row=0, column=3,sticky='ew')
            self.exercises_competences[f'ex{i}'][f'explanation_entry'] = explanations_entry[f'exercice_{i}']
        #self.add_explanations_controls()
     
    def modify_ratio_label(self,event, exercice_number, comp_number):
        print(f"from modify_ratio_label \n\tExercice number {exercice_number}\n\tcomp_number : {comp_number}")
        new_number=self.exercises_competences[f'ex{exercice_number}'][f'comp{comp_number}']['number_selector'].get()
        self.exercises_competences[f'ex{exercice_number}'][f'comp{comp_number}']['number_var']=new_number
        new_label = self.calculate_ratio_label_text(exercice_number)
        self.exercises_competences[f'ex{exercice_number}']['ratio_label'].configure(text=new_label)
        """if exercice_number == 0 or comp_number == 0:
            return"""
        """print(f"event {event}")
        new_label = self.calculate_ratio_label_text(exercice_number)
        if f'ratio_label' in self.exercises_competences[f'ex{exercice_number}']:
            self.exercises_competences[f'ex{exercice_number}']['ratio_label'].configure(text=new_label)"""
        pass
    #print(new_label)
        #print(self.exercises_competences[f'ex{exercice_number}'][f'comp{comp_number}'])#['ratio_label'].configure(text=new_label)
    def calculate_ratio_label_text(self, exercise_idx):
        number_comp=int(self.competency_selector.get())
        ratios=[]
        for comp_index in range(number_comp):
            ratios.append(self.exercises_competences[f'ex{exercise_idx}'][f'comp{comp_index}']['number_var'])
        ratio_text = ":".join(map(str, ratios))
        return f"Le ratio pour l'évaluation par compétence de l'exercice {exercise_idx + 1} sera : {ratio_text}"


    def toggle_competence(self, exercise_index, comp_index):
        if self.exercises_competences[f'ex{exercise_index}'][f'comp{comp_index}']['number_selector'].cget("state")=="disabled":
            self.exercises_competences[f'ex{exercise_index}'][f'comp{comp_index}']['number_selector'].configure(state="normal")
        else:
            self.exercises_competences[f'ex{exercise_index}'][f'comp{comp_index}']['number_selector'].configure(state="disabled")
        

    def update_proportion(self, value, exercise_index, comp_index):
        # Update proportion logic
        pass

    def move_competence_up(self, exercise_index, comp_index):
        if comp_index > 0:
            self.swap_competences(exercise_index, comp_index, comp_index - 1)

    def move_competence_down(self, exercise_index, comp_index):
        if comp_index < len(self.exercises_competences[f'ex{exercise_index}']) - 1:
            self.swap_competences(exercise_index, comp_index, comp_index + 1)

    def swap_competences(self, exercise_index, index1, index2):
        self.exercises_competences[f'ex{exercise_index}'][index1], self.exercises_competences[f'ex{exercise_index}'][index2] = \
            self.exercises_competences[f'ex{exercise_index}'][index2], self.exercises_competences[f'ex{exercise_index}'][index1]
        self.update_competence_positions(exercise_index)

    def update_competence_positions(self, exercise_index):
        for idx, comp in enumerate(self.exercises_competences[f'ex{exercise_index}']):
            comp['checkbox'].grid(row=idx, column=0, sticky="w")
            comp['slider'].grid(row=idx, column=1, padx=5)
            comp['up'].grid(row=idx, column=2, padx=5)
            comp['down'].grid(row=idx, column=3, padx=5)

    def create_homework(self):
        # Gather all data and create the JSON structure
        try:
            date_devoir = self.homework_date_entry.submit(option = "underscore")
        except Exception as e:
            print("erreur dans la création du devoir : ",e)
            return
        homework_data = {
            "title": self.homework_title_entry.get(),
            "date": date_devoir,
            "competences": {}
        }

        for i in range(1, 5):  # Adjust according to the number of exercises
            exercise_key = f'ex{i}'
            homework_data["competences"][exercise_key] = {}
            for j, comp in enumerate(self.exercises_competences[exercise_key]):
                if comp['checkbox'].get():
                    comp_name = comp['checkbox'].cget('text')
                    proportion = comp['slider'].get()
                    homework_data["competences"][exercise_key][comp_name] = {
                        'nomcomplet': f"Nom complet {comp_name}",
                        'code': f"Code {comp_name}",
                        'proportion': f"{proportion:.2f}"
                    }

        json_file_path = f"homework_{self.homework_title_entry.get().replace(' ', '_').lower()}.json"
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(homework_data, json_file, indent=4, ensure_ascii=False)

        ctk.CTkLabel(self.homework_creation_interface, text=f"Devoir créé et sauvegardé sous {json_file_path}").grid(row=7, column=0, columnspan=2)
if __name__=="__main__":
    # Initialiser l'application
    root = ctk.CTk()
    ui = HomeworkSetupUI(root)
    root.mainloop()

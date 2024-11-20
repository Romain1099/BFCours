import customtkinter as ctk
import tkinter as tk
import json
import os
# Activer le mode sombre
ctk.set_appearance_mode("dark")
class CompetenceDisplayer:
    def __init__(self, root, num_competencies_var):
        self.root = root
        self.number_of_competencies_var = num_competencies_var
        self.competencies_window = None
        self.comp_widget = {}
        self.data = {}

    def load_data(self):
        # Charger toutes les données en mémoire
        themes_path = 'competences'
        for theme in os.listdir(themes_path):
            theme_path = os.path.join(themes_path, theme)
            if os.path.isdir(theme_path):
                self.data[theme] = {}
                for file_name in os.listdir(theme_path):
                    if file_name.endswith('.json'):
                        file_path = os.path.join(theme_path, file_name)
                        with open(file_path, 'r',encoding='utf-8') as file:
                            self.data[theme][file_name] = json.load(file)

    def open_competencies_window(self):
        self.load_data()  # Charger les données avant de créer l'interface utilisateur
        num_competencies = self.number_of_competencies_var.get()
        if num_competencies == 0:
            return  # no competencies to configure
        if self.competencies_window:
            self.competencies_window.destroy()
        self.competencies_window = ctk.CTkToplevel(self.root)
        self.competencies_window.geometry(f"{600}x{600}")
        self.competencies_window.attributes("-topmost", True)
        
        #self.competencies_window.protocol("WM_DELETE_WINDOW", self.get_competencies)
        self.competencies_window.title("Paramétrage des Compétences")

        # Ajouter une scrollbar
        self.scrollable_frame = ctk.CTkFrame(self.competencies_window)#self.canvas,width=600)
        self.scrollable_frame.grid(row=0,columns=3, padx=10, pady=10, sticky="nsew")

        self.comp_widget = {}

        columns = 2
        rows = (num_competencies + columns - 1) // columns

        for i in range(num_competencies):
            frame = ctk.CTkFrame(self.scrollable_frame)
            frame.grid(row=i // columns, column=i % columns, padx=10, pady=10, sticky="nsew")
            frame.grid_columnconfigure(1, weight=1)
            self.scrollable_frame.grid_columnconfigure(i % columns, weight=1)
            self.scrollable_frame.grid_rowconfigure(i // columns, weight=1)

            self.comp_widget[i] = {}

            theme_var = tk.StringVar()
            file_var = tk.StringVar()
            comp_var = tk.StringVar()
            code_var = tk.StringVar()

            self.comp_widget[i]['ThemeVar'] = theme_var
            self.comp_widget[i]['FileVar'] = file_var
            self.comp_widget[i]['CompVar'] = comp_var
            self.comp_widget[i]['CodeVar'] = code_var

            ctk.CTkLabel(frame, text=f"Compétence {i+1}").grid(row=0, column=0, columnspan=2, pady=5, sticky="nsew")
            ctk.CTkLabel(frame, text="Thème:").grid(row=1, column=0, sticky='e')
            theme_combobox = ctk.CTkComboBox(frame, values=list(self.data.keys()), command=lambda choice, index=i: self.update_theme_var(choice, index))
            theme_combobox.grid(row=1, column=1, sticky="ew")

            ctk.CTkLabel(frame, text="Fichier:").grid(row=2, column=0, sticky='e')
            file_combobox = ctk.CTkComboBox(frame, command=lambda choice, index=i: self.update_file_var(choice, index))
            file_combobox.grid(row=2, column=1, sticky="ew")

            ctk.CTkLabel(frame, text="Compétence :").grid(row=3, column=0, sticky='e')
            comp_combobox = ctk.CTkComboBox(frame, command=lambda choice, index=i: self.update_comp_var(choice, index))
            comp_combobox.grid(row=3, column=1, sticky="ew")

            ctk.CTkLabel(frame, text="Code:").grid(row=4, column=0, sticky='e')
            code_entry = ctk.CTkEntry(frame, textvariable=code_var)
            code_entry.grid(row=4, column=1, sticky="ew")

            details_text = ctk.CTkTextbox(frame, height=100)
            details_text.grid(row=5, column=0, columnspan=2, pady=5, sticky="nsew")
            
            self.comp_widget[i]["ThemeCombobox"] = theme_combobox
            self.comp_widget[i]["FileCombobox"] = file_combobox
            self.comp_widget[i]["CompCombobox"] = comp_combobox
            self.comp_widget[i]["CodeEntry"] = code_entry
            self.comp_widget[i]["Details"] = details_text

        for i in range(rows):
            self.scrollable_frame.grid_rowconfigure(i, weight=1)
        for j in range(columns):
            self.scrollable_frame.grid_columnconfigure(j, weight=1)

    def update_theme_var(self, choice, index):
        theme_var = self.comp_widget[index]['ThemeVar']
        theme_var.set(choice)
        self.load_subdirectories(index)

    def update_file_var(self, choice, index):
        file_var = self.comp_widget[index]['FileVar']
        file_var.set(choice)
        self.load_competencies(index)

    def update_comp_var(self, choice, index):
        comp_var = self.comp_widget[index]['CompVar']
        comp_var.set(choice)
        self.display_competence_details(index)

    def load_subdirectories(self, index):
        theme = self.comp_widget[index]['ThemeVar'].get()
        files = list(self.data[theme].keys())
        if files:
            self.comp_widget[index]["FileCombobox"].configure(values=files)
            first_file = files[0]
            self.comp_widget[index]['FileVar'].set(first_file)
            self.update_file_var(first_file, index)

    def load_competencies(self, index):
        theme = self.comp_widget[index]['ThemeVar'].get()
        file_name = self.comp_widget[index]['FileVar'].get()
        competencies = [competency['code'] for competency in self.data[theme][file_name]]
        self.comp_widget[index]["CompetenciesData"] = self.data[theme][file_name]
        if competencies:
            self.comp_widget[index]["CompCombobox"].configure(values=competencies)
            first_comp = competencies[0]
            self.comp_widget[index]['CompVar'].set(first_comp)
            self.update_comp_var(first_comp, index)

    def display_competence_details(self, index):
        selected_code = self.comp_widget[index]['CompVar'].get()
        competencies = self.comp_widget[index]["CompetenciesData"]
        for competency in competencies:
            if competency['code'] == selected_code:
                details = f"Intitulé: {competency.get('intitulé', 'N/A')}\nNiveau Estimé: {competency.get('niveau_estime', 'N/A')}\nDescription: {competency.get('description', 'N/A')}"
                self.comp_widget[index]["Details"].delete("1.0", tk.END)
                self.comp_widget[index]["Details"].insert(tk.END, details)
                self.comp_widget[index]['CodeVar'].set(selected_code)
                break



def use_case_one():
    root = ctk.CTk()  # Or your existing root window
    num_competencies_var = tk.IntVar(value=3)  # Or your existing variable
    displayer = CompetenceDisplayer(root, num_competencies_var)
    displayer.open_competencies_window()
    root.mainloop()
 #Usage:
if __name__=="__main__":
    use_case_one()


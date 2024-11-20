import os
import tkinter as tk
import customtkinter as ctk

class UIYearSelector():#ctk.CTkTopLevel):
    def __init__(self,function_caller,parent,on_validate_selected="",topmost:bool=False):
        #super().__init__()
        self.title="Paramètres du bilan périodique"
        self.parent=parent
        self.function_caller=function_caller
        self.validate_function=on_validate_selected
        if self.validate_function =="":
            print("Fonction de validation non spécifiée")
            self.validate_function=self.default_function
        self.class_directory="classes"
        self.topmost_option=topmost
        self.setup_ui()
        self.setup_buttons()

    def default_function(self,*args):
        print(f"default_function de {self.title}")

    def setup_ui(self):
        self.window = ctk.CTkToplevel(self.parent)
        

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.parent.iconify()
        self.window.title(self.title)
        if self.topmost_option:
            self.window.attributes("-topmost", True)

    def on_ok(self):
        selected_class = self.combo_class_code.get()
        selected_date_min = self.date_min_selector.get()
        selected_date_max = self.date_max_selector.get()
        self.function_caller.create_full_year_and_compile(code_classe=selected_class,date_min=selected_date_min,date_max=selected_date_max)
        self.on_close()

    def update_devoirs(self,*args):
        selected_class = self.combo_class_code.get()
        if os.path.exists(self.devoir_directory):
            devoirs_files = [f.replace('.csv', '') for f in os.listdir(self.devoir_directory) if f.endswith('.csv')]
        else:
            print(f"le devoir {self.devoir_directory} n'a pas été trouvé")
            return
        self.combo_devoirs.configure(values=devoirs_files)
        if devoirs_files:
            self.combo_devoirs.set(devoirs_files[0])
        else:
            self.combo_devoirs.set('')

    def on_close(self):
        try:
            self.parent.deiconify()
            self.window.destroy()
        except:
            print("Erreur dans le deiconify du parent")
            self.window.destroy()

    def setup_buttons(self):
        root_x = self.window.winfo_x()
        root_y = self.window.winfo_y()
        root_width = self.window.winfo_width()
        root_height = self.window.winfo_height()

        new_x = root_x
        new_y = root_y + root_height + 50
        self.window.geometry(f"+{new_x}+{new_y}")

        self.label_class_code = ctk.CTkLabel(self.window, text="Choisissez un code de classe :")
        self.label_class_code.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        class_code_files = [f.replace('.csv', '') for f in os.listdir(self.class_directory) if f.endswith('.csv')]
        self.combo_class_code = ctk.CTkComboBox(self.window, command=self.default_function, values=class_code_files, state="readonly")
        self.combo_class_code.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.label_date_min = ctk.CTkLabel(self.window, text="Date de départ du bilan :")
        self.label_date_min.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.date_min_selector = ctk.CTkEntry(self.window)
        placeholder_date_min_text="01_09_23"
        self.date_min_selector.insert(0,placeholder_date_min_text)
        self.date_min_selector.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.label_date_min = ctk.CTkLabel(self.window, text="Date de fin du bilan :")
        self.label_date_min.grid(row=0, column=2, padx=10, pady=10, sticky="w")
           
        self.date_max_selector = ctk.CTkEntry(self.window)
        placeholder_date_max_text="01_07_24"
        self.date_max_selector.insert(0,placeholder_date_max_text)  
        self.date_max_selector.grid(row=1, column=2, padx=10, pady=5, sticky="ew")

        """self.label_theme = ctk.CTkLabel(self.parent, text="Entrez le thème du devoir :")
        self.label_theme.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        
        self.theme_entry = ctk.CTkEntry(self.parent)
        self.theme_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")"""

        self.ok_button = ctk.CTkButton(self.window, text="Exporter le bilan", command=self.on_ok)
        self.ok_button.grid(row=3, column=0, columnspan=3, pady=20)
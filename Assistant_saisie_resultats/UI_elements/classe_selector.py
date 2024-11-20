import os
import tkinter as tk
import customtkinter as ctk

class UIClasseSelector():#ctk.CTkTopLevel):
    def __init__(self,parent_widget,parent_caller,function_name,topmost:bool=True):
        #super().__init__()
        self.title= "Sélectionner un devoir"
        self.parent=parent_widget
        self.parent_caller=parent_caller
        if parent_caller=="":
            self.validate_function=self.pass_function
        else:
            self.validate_function=self.function_to_call_from_parent
            self.function_name=function_name
        self.pass_function_count=0
        self.classes_directory="classes"
        self.devoir_directory=""
        self.topmost_option=topmost
        self.setup_ui()
        self.setup_buttons()

    def function_to_call_from_parent(self,selected_class="", selected_devoir="", theme=""):
        self.function_name(selected_class, selected_devoir, theme)

    def setup_ui(self):
        self.window = ctk.CTkToplevel(self.parent)
        
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.parent.iconify()
        self.window.title(self.title)
        if self.topmost_option:
            self.window.attributes("-topmost", True)

    def pass_function(self,selected_class="", selected_devoir="", theme=""):#,selected_class="", selected_devoir="", theme=""k):
        print("pass_function")
        self.pass_function_count+=1
        pass

    def on_ok(self):
        selected_class = self.combo_class_code.get()
        selected_devoir = self.combo_devoirs.get()
        theme = self.theme_entry.get()
        self.validate_function(selected_class=selected_class, selected_devoir=selected_devoir, theme=theme)
        self.on_close()

    def update_devoirs(self,*args):
        selected_class = self.combo_class_code.get()
        self.class_code=selected_class

        self.devoir_directory=f"devoirs_effectues/{selected_class}/csv"
        print(f"current devoir directory : {self.devoir_directory}")
        if os.path.exists(self.devoir_directory):
            devoirs_files = [f.replace('.csv', '') for f in os.listdir(self.devoir_directory) if f.endswith('.csv')]
        else:
            print(f"le répertoire {self.devoir_directory} n'a pas été trouvé")
            return
        self.combo_devoirs.configure(values=devoirs_files)
        if devoirs_files:
            self.combo_devoirs.set(devoirs_files[0])
        else:
            self.combo_devoirs.set('')

    def on_close(self):
        self.parent.deiconify()
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

        class_code_files = [f.replace('.csv', '') for f in os.listdir(self.classes_directory) if f.endswith('.csv')]
        self.combo_class_code = ctk.CTkComboBox(self.window, command=self.update_devoirs, values=class_code_files, state="readonly")
        self.combo_class_code.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.label_devoirs = ctk.CTkLabel(self.window, text="Choisissez un devoir dans la liste :")
        self.label_devoirs.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.combo_devoirs = ctk.CTkComboBox(self.window, state="readonly")
        self.combo_devoirs.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.label_theme = ctk.CTkLabel(self.window, text="Entrez le thème du devoir :")
        self.label_theme.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        
        self.theme_entry = ctk.CTkEntry(self.window)
        self.theme_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.ok_button = ctk.CTkButton(self.window, text="OK", command=self.on_ok)
        self.ok_button.grid(row=3, column=0, columnspan=2, pady=20)
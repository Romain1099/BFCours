import customtkinter as ctk
import os
class ModelModder(ctk.CTkToplevel):
    """
    Classe destinée à faciliter la gestion de modèles à l'utilisateur.
    Fonctionnalités : 
    - Ouverture du dossier contenant les modèles
    """
    def __init__(self, master=None,models_folder:str=""):
        if master:
            super().__init__(master)
        else:
            raise ValueError(f"Master is empty")
        if models_folder and models_folder != "":
            self.models_folder= models_folder
        else:
            raise ValueError(f"Master is empty")
        self.open_model_directory()
        
    def open_model_directory(self):
        os.startfile(self.models_folder)
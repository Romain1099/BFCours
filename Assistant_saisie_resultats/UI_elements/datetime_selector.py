import customtkinter as ctk
from tkinter import ttk
from datetime import datetime
from functools import partial
import calendar
from typing import Tuple

class DatetimeSelectorUI(ctk.CTkFrame):
    def __init__(self, master, fields=None,put_demo_values=False,put_submit_button=False):
        super().__init__(master)
        self.put_submit_button=put_submit_button

        self.fields = fields if fields else ['day', 'month', 'year']
        self.create_widgets()
        if put_demo_values:
            self.put_demo_values()

    def create_widgets(self):
        col = 0
        self.entries = {}
        
        # Conteneur pour organiser les champs
        frame = ctk.CTkFrame(self)
        frame.pack(padx=5, pady=5)

        if 'day' in self.fields:
            #ctk.CTkLabel(frame, text='Date :').pack(side="left", padx=5, pady=5)
            self.entries['day'] = ctk.CTkEntry(frame, width=30)  # Ajusté pour 2 caractères en pixels
            self.entries['day'].pack(side="left", padx=1, pady=5)
        
        if 'month' in self.fields:
            ctk.CTkLabel(frame, text='/').pack(side="left", padx=1, pady=5)
            self.entries['month'] = ctk.CTkEntry(frame, width=30)  # Ajusté pour 2 caractères en pixels
            self.entries['month'].pack(side="left", padx=1, pady=5)

        if 'year' in self.fields:
            ctk.CTkLabel(frame, text='/').pack(side="left", padx=1, pady=5)
            self.entries['year'] = ctk.CTkEntry(frame, width=50)  # Ajusté pour 4 caractères en pixels
            self.entries['year'].pack(side="left", padx=1, pady=5)

        if 'hour' in self.fields:
            ctk.CTkLabel(frame, text=' à ').pack(side="left", padx=1, pady=5)
            self.entries['hour'] = ctk.CTkEntry(frame, width=30)  # Ajusté pour 2 caractères en pixels
            self.entries['hour'].pack(side="left", padx=1, pady=5)

        if 'minute' in self.fields:
            ctk.CTkLabel(frame, text='h').pack(side="left", padx=1, pady=5)
            self.entries['minute'] = ctk.CTkEntry(frame, width=30)  # Ajusté pour 2 caractères en pixels
            self.entries['minute'].pack(side="left", padx=1, pady=5)

        if 'second' in self.fields:
            ctk.CTkLabel(frame, text='min').pack(side="left", padx=1, pady=5)
            self.entries['second'] = ctk.CTkEntry(frame, width=30)  # Ajusté pour 2 caractères en pixels
            self.entries['second'].pack(side="left", padx=1, pady=5)
            ctk.CTkLabel(frame, text='s').pack(side="left", padx=1, pady=5)

        if self.put_submit_button:
            self.submit_button = ctk.CTkButton(self, text='Submit', command=self.submit)
            self.submit_button.pack(padx=5, pady=5)
    
    # Méthode pour valider les entrées
    def validate_entry(self, entry, min_value, max_value)->Tuple[int, bool]:
        value = entry.get()
        try:
            value = int(value)
            if min_value <= value <= max_value:
                # Colorer en noir le champ correct
                entry.configure(text_color='green')
                print("val_entry_ok")
                return value, True
            else:
                # Colorer en rouge le champ défectueux
                entry.configure(text_color='red')
                # Renvoyer la valeur min ou max selon les cas
                if value > max_value:
                    return max_value, False
                elif value < min_value:
                    return min_value, False
        except ValueError:
            # Colorer en rouge le champ défectueux
            entry.configure(text_color='red')
            return min_value, False

    # Méthode pour obtenir la date et l'heure
    def get_time(self)->Tuple[datetime, bool]:
        validations = []
        day,vd = self.validate_entry(self.entries['day'], 1, 31) if 'day' in self.entries else tuple([1,0])
        validations.append(vd)
        month,vm = self.validate_entry(self.entries['month'], 1, 12) if 'month' in self.entries else tuple([1,0])
        validations.append(vm)
        year,vy = self.validate_entry(self.entries['year'], 1900, 2100) if 'year' in self.entries else tuple([2000,0])
        validations.append(vy)
        hour,vh = self.validate_entry(self.entries['hour'], 0, 23) if 'hour' in self.entries else tuple([0,0])
        validations.append(vh)
        minute,vmi = self.validate_entry(self.entries['minute'], 0, 59) if 'minute' in self.entries else tuple([0,0])
        validations.append(vmi)
        second,vs = self.validate_entry(self.entries['second'], 0, 59) if 'second' in self.entries else tuple([0,0])
        validations.append(vs)
        # Ajustement du jour selon le mois et l'année
        try:
            max_day = calendar.monthrange(year, month)[1]
        except:
            max_day = 31
            validations.append(False)
        if day>max_day:
            validations.append(False)
        day = min(day, max_day)
        print(sum(validations),len(self.fields),self.fields)
        if sum(validations)==len(self.fields):
            all_validate=True
        else:
            all_validate=False
            return datetime.today(),all_validate
            
        return datetime(year, month, day, hour, minute, second),all_validate
    
    def submit(self,option=""):
        
        selected_datetime,validated = self.get_time()
        if not validated:
            print(f"La date n'a pas été validée : {selected_datetime}")
        # Format français dynamique
        date_format = "%d / %m / %Y"
        time_format = "%Hh %Mmin"
        full_time_format = "%Hh %Mmin %Ss"
        if 'hour' in self.fields or 'minute' in self.fields:
            if 'second' in self.fields:
                formatted_datetime = selected_datetime.strftime(f"{date_format} à {full_time_format}")
            else:
                formatted_datetime = selected_datetime.strftime(f"{date_format} à {time_format}")
        else:
            formatted_datetime = selected_datetime.strftime(date_format)
        if option == "demo":
            print(f"Selected datetime: {formatted_datetime} ")
        if option == "underscore":
            formatted_datetime = formatted_datetime.replace("/","_").replace(" ","")
        return formatted_datetime
    
    def put_demo_values(self):
        #peuple les champs avec les valeurs suivantes : 13/03/1994 à 15h57min38sec
        #il faut bien sur repérer quels sont les champs à remplir. 
        today=datetime.today()

        demo_values = {
            'day': today.day,
            'month': today.month,
            'year': today.year,
            'hour': today.hour,
            'minute': today.minute,
            'second': today.second
        }
        print(f"self entries : {self.entries}")
        for field, value in demo_values.items():
            if field in self.entries:
                self.entries[field].insert(0, str(value))


def setup_datetime_selector(root,fields:list,put_demo_values:bool=False,put_submit_button=False)->DatetimeSelectorUI:
    return DatetimeSelectorUI(root,fields,put_demo_values,put_submit_button)

datetime_ui = partial(setup_datetime_selector,fields = ['day', 'month', 'year', 'hour', 'minute'],put_submit_button=False)
datetime_ui_validator = partial(setup_datetime_selector,fields = ['day', 'month', 'year', 'hour', 'minute'],put_submit_button=True)
datetime_ui_demo = partial(setup_datetime_selector,fields = ['day', 'month', 'year', 'hour', 'minute'],put_demo_values=True,put_submit_button=True)

day_ui = partial(setup_datetime_selector,fields = ['day', 'month', 'year'],put_demo_values=True,put_submit_button=False)
day_ui_validator = partial(setup_datetime_selector,fields = ['day', 'month', 'year'],put_demo_values=True,put_submit_button=True)
day_ui_demo = partial(setup_datetime_selector,fields = ['day', 'month', 'year'],put_demo_values=True,put_submit_button=True)


full_datetime_ui = partial(setup_datetime_selector,fields=['day', 'month', 'year', 'hour', 'minute','second'],put_submit_button=False)
full_datetime_ui_demo = partial(setup_datetime_selector,fields=['day', 'month', 'year', 'hour', 'minute','second'],put_demo_values=True,put_submit_button=True)
full_datetime_ui_validator = partial(setup_datetime_selector,fields=['day', 'month', 'year', 'hour', 'minute','second'],put_submit_button=True)

def use_case_one():
    root = ctk.CTk()
    root.geometry('950x400')
    
    # Use case 1: Only day, month, year, hour and minute
    frame1 = day_ui(root)#, fields=['day', 'month', 'year', 'hour', 'minute'])
    frame1.pack(pady=20)

    # Use case 2: Only day, month, year, hours, minute
    frame2 = datetime_ui(root)#, fields=['day', 'month', 'year'])
    frame2.pack(pady=20)
    
    # Use case 3: Day, month, year, hour, and minute and second
    frame3 = full_datetime_ui(root)#, fields=['day', 'month', 'year', 'hour', 'minute', 'second'])
    frame3.pack(pady=20)
    
    root.mainloop()

def use_case_two():
    root = ctk.CTk()
    root.geometry('950x400')
    
    # Use case 1: Only day, month, year, hour and minute
    frame1 = day_ui_validator(root)#, fields=['day', 'month', 'year', 'hour', 'minute'])
    frame1.pack(pady=20)

    # Use case 2: Only day, month, year, hours, minute
    frame2 = datetime_ui_validator(root)#, fields=['day', 'month', 'year'])
    frame2.pack(pady=20)
    
    # Use case 3: Day, month, year, hour, and minute and second
    frame3 = full_datetime_ui_validator(root)#, fields=['day', 'month', 'year', 'hour', 'minute', 'second'])
    frame3.pack(pady=20)
    
    root.mainloop()


def use_case_demo():
    root = ctk.CTk()
    root.geometry('950x400')
    
    # Use case 1: Only day, month, year, hour and minute
    frame1 = day_ui_demo(root)#, fields=['day', 'month', 'year', 'hour', 'minute'])
    frame1.pack(pady=20)

    # Use case 2: Only day, month, year, hours, minute
    frame2 = datetime_ui_demo(root)#, fields=['day', 'month', 'year'])
    frame2.pack(pady=20)
    
    # Use case 3: Day, month, year, hour, and minute and second
    frame3 = full_datetime_ui_demo(root)#, fields=['day', 'month', 'year', 'hour', 'minute', 'second'])
    frame3.pack(pady=20)
    
    #Récupération des infos de date : 
    frame1.submit(option="demo")
    frame2.submit(option="demo")
    frame3.submit(option="demo")
    
    root.mainloop()

# Exemple d'utilisation de la classe
if __name__ == '__main__':
    #use_case_one()
    #use_case_two()
    use_case_demo()

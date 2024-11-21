

class YearRecap():
    def __init__(self,class_code,date_min,date_max):
        self.class_code=class_code
        self.date_min_underscore=date_min.replace("/","_")
        self.date_min_slash=date_min.replace("_","/")
        self.date_max_underscore=date_max.replace("/","_")
        self.date_max_slash=date_max.replace("_","/")

    def make_tex_recap(self):
        if isinstance(self.class_code,str):
            tex_code=f"""
code tex du recapitulatif :
    classe ciblée : {self.class_code}
    date de début du bilan : {self.date_min_slash}
    date de fin du bilan : {self.date_max_slash}
"""
        elif isinstance(self.class_code,list):
            tex_code=f"""
code tex du recapitulatif :
    classes ciblées : {', '.join(self.class_code)}
    date de début du bilan : {self.date_min_slash}
    date de fin du bilan : {self.date_max_slash}
"""
        return tex_code


import re
class DocumentHandler:
    def __init__(self,*args):
        self.__names=["title_of_document", "niveau", "theme", "type_etablissement", "nom_etablissement", "supplement", "type_document"]
        [self.__setattr__(self.__names[index],arg) for index,arg in enumerate(args)]
        self.model_content = self.load_model_content(getattr(self,"type_document")) if hasattr(self,"type_document") else None
        self.replace_chapter()
        print(self.model_content)

    def load_model_content(self,type_document):
        with open(f"document_model/{type_document}.tex",'r',encoding="utf-8") as file:
            content = file.read()
        return content

    def replace_chapter(self):
        for key,value in self.__dict__.items():
            if key == "niveau":
                self.model_content = self.model_content.replace(f"% {key}",f"${value}$")
            if not key.startswith("_"):
                self.model_content = self.model_content.replace(f"% {key}",f"{value}")
                name=f"% {key}"

        
    def __repr__(self) -> str:
        return "\n\t".join([f'{arg} : "{value}" ' for arg,value in self.__dict__.items()])

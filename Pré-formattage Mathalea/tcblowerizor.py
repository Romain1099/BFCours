import re
#import tikzdiff
from tkinter import filedialog, messagebox
import insert_responses_in_exo as rep
import def_points_for_exos as points
#import os
from get_comp_by_code import get_comp_by_code  
instructions_compilation = "py -3.13-64 -m PyInstaller --onefile --noconsole --icon=C:/Users/Utilisateur/Desktop/Faire/Macros/Programmes_de_facilitation/lateximp_dmP_icon.ico Mathalea_adapter/tcblowerizor.py" 

def find_EXO(content, patterns):
    final=[]
    print("Début de l'opération de recherche.")
    content=re.sub(r'\\begin{multicols}',r'%\\begin{multicols}',content)
    content= re.sub(r'\\begin{enumerate}',r'\\begin{tcbenumerate}[2]% ',content)
    content=re.sub(r'\\end{multicols}',r'%\\end{multicols}',content)
    content=re.sub(r'\\columnbreak',r'%\\columnbreak',content)
    content= re.sub(r'\\end{enumerate}',r'\\end{tcbenumerate}% ',content)
    for index, pattern in enumerate(patterns):
        exos = re.findall(pattern, content, re.DOTALL)
        if exos:
            # Imprime le motif trouvé et l'index dans la liste des motifs
            print(f"Motif trouvé pattern n° {index}: '{pattern}'")
            # Imprime chaque exercice trouvé avec ce motif
            for exo_index, exo in enumerate(exos):
                print(f"  Exercice {exo_index} : {exo}")  # Affiche les 30 premiers caractères de l'exo
                #print("Fin de l'opération de recherche des exercices.")
                

            
            final.extend(exos)
        print(f"Aucun motif trouvé pour le pattern {pattern}.")
    print("Fin de l'opération de recherche des exercices.")
    return final


def separer_correction(content):
    # Détermine si le contenu utilise le séparateur textuel "CORRECTION" ou les balises \begin{Correction}...\end{Correction}
    if "CORRECTION" in content:
        parts = re.split(r'\s*CORRECTION\s*', content, maxsplit=1)
        if len(parts) == 2:
            print(f"Enoncé : \n{parts[0]}\nSolutions : \n{parts[1]}")
            return parts[0], parts[1]
    elif "\\begin{Correction}" in content and "\\end{Correction}" in content:
        # Utilise re.search pour capturer le contenu entre les balises \begin{Correction} et \end{Correction}
        match = re.search(r'\\begin{Correction}(.*?)\\end{Correction}', content, flags=re.DOTALL)
        if match:
            # Sépare le contenu avant et après les balises de Correction
            before_correction = content.split(match.group(0))[0]
            correction_content = match.group(1)  # Capture le contenu entre les balises
            print(f"Enoncé : \n{before_correction}\nSolutions : \n{correction_content}")
            return before_correction, correction_content
    else:
        print("Le séparateur de CORRECTION ou les balises \\begin{Correction} et \\end{Correction} ne sont pas trouvés.")
        return

    print("Erreur dans la séparation du contenu.")
    return

def latex_exo_final_formatter(result_of_the_research_enonce:list[str],result_of_the_research_solution:list[str])->str:
    #TODO: faire la fonction qui lie code compétence et énoncé de la compétence.
    competency_enonce=get_comp_by_code(result_of_the_research_enonce[1]) # placeholder mais on voudrait faire search_enonce_comp_for_code(result_of_the_research_enonce[1])
    content=f"""
\\begin{{EXO}}{{{competency_enonce}}}{{{result_of_the_research_enonce[1]}}}
    {result_of_the_research_enonce[0]} 

    {result_of_the_research_enonce[2]}

\\exocorrection

    {result_of_the_research_solution[2]}

\\end{{EXO}}
"""
    return content

def enlever_contenu_latex(content, tag_debut, tag_fin):
    if tag_fin:  # Si un tag de fin est spécifié
        pattern = r'\\' + re.escape(tag_debut) + r'.*?\\' + re.escape(tag_fin)
    else:  # Si aucun tag de fin n'est spécifié, comme pour \clearpage
        pattern = r'\\' + re.escape(tag_debut)
    return re.sub(pattern, '', content, flags=re.DOTALL)

def enlever_document_et_clearpage(content):
    # Correction des noms des tags pour assurer l'échappement correct
    content = enlever_contenu_latex(content, 'begin\{document\}', 'end\{document\}')
    content = enlever_contenu_latex(content, 'clearpage', None)  # Pas de tag de fin pour clearpage
    return content

def put_itemsep_to_one(text: str) -> str:
    # Remplacer "itemsep=1.5em" par "itemsep=1em" dans le texte
    mod_text = re.sub(r"itemsep=1.5em", "itemsep=1em", text)
    return mod_text

def auto_indent(text:str)->str:
    # Remove existing indentation
    content:str = re.sub(r'^[ \t]+', '', text, flags=re.MULTILINE)
    # Split content into lines for processing
    lines_list = content.splitlines()
    print(lines_list[:3])

    lines = []
    for line in lines_list:
        print(f"line {line}")
        lines.extend(line.split(r"\\"))
    indent_level = 0
    indent = ' ' * 4
    indented_lines = []
    inside_environment = False
    open_braces = 0
    open_brackets = 0
    pending_indent_increase = False

    for line in lines:
        stripped_line = line.strip()

        # Check for \begin{...} and increase indent level
        if re.match(r'\\begin\{.*\}', stripped_line):
            #print(f"begin_triggered : {stripped_line}")
            indented_lines.append(indent * indent_level + stripped_line)
            indent_level += 1
        # Check for \end{...} and decrease indent level
        elif re.match(r'\\end\{.*\}', stripped_line):
            indent_level -= 1
            indented_lines.append(indent * indent_level + stripped_line)
        # Check for closing braces or brackets on their own line
        elif stripped_line == '}' or stripped_line == ']':
            indent_level -= 1
            indented_lines.append(indent * indent_level + stripped_line)
        else:
            # Update count of open braces and brackets
            opening_braces = stripped_line.count('{')
            closing_braces = stripped_line.count('}')
            opening_brackets = stripped_line.count('[')
            closing_brackets = stripped_line.count(']')

            # Adjust indent level before appending the line if there are unmatched closing braces or brackets
            if closing_braces > opening_braces:
                indent_level -= (closing_braces - opening_braces)
            if closing_brackets > opening_brackets:
                indent_level -= (closing_brackets - opening_brackets)

            indented_lines.append(indent * indent_level + stripped_line)

            # Adjust indent level after appending the line if there are unmatched opening braces or brackets
            if opening_braces > closing_braces:
                indent_level += (opening_braces - closing_braces)
            if opening_brackets > closing_brackets:
                indent_level += (opening_brackets - closing_brackets)

    # Join the lines back into a single string
    indented_content = '\n'.join(indented_lines)
    return indented_content
def tcblowerize(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = enlever_document_et_clearpage(content=content)
    parts=separer_correction(content)
    if not parts:
        print("Le séparateur de CORRECTION n'est pas trouvé dans le fichier d'entrée.")
        return
    enonce_part, solution_part = parts
    #enlever_document_et_clearpage(enonce_part)
    #enlever_document_et_clearpage(solution_part)
    exo_pattern = r'\\begin{EXO}(.*?)\\end{EXO}'
    patterns = [
    r'\\begin{EXO}\n{(.*?)}\n{(.*?)}\n(.*?)\\end{EXO}',
    r'\\begin{EXO}\n{(.*?)}{(.*?)}\n(.*?)\\end{EXO}',
    r'\\begin{EXO}{(.*?)}{(.*?)}\n(.*?)\\end{EXO}',
    r'\\begin{EXO}\n{(.*?)}{(.*?)}(.*?)\\end{EXO}',
    r'\\begin{EXO}\n{(.*?)}{(.*?)}\n(.*?)\\end{EXO}',
    r'\\begin{EXO}{(.*?)}\n{(.*?)}\n(.*?)\\end{EXO}',
    r'\\begin{EXO}{(.*?)}\n{(.*?)}(.*?)\\end{EXO}',
    r'\\begin{EXO}\n{(.*?)}\n{(.*?)}(.*?)\\end{EXO}',
    r'\\begin{EXO}\n{(.*?)}{(.*?)}\n(.*?)\\end{EXO}',
    # Ajoutez ici d'autres patterns possibles
]

    enonce_exos = find_EXO(enonce_part, patterns)
    solution_exos = find_EXO(solution_part, patterns)

    if len(enonce_exos) != len(solution_exos):
        print("Nombre d'exercices et de solutions ne correspondent pas.")
        return
    # Supposons que 'enonce_exos' contient l'énoncé des exercices et 'solution_part' contient les solutions
    final_contents = []
    with open(output_file_path, 'w',encoding='utf-8') as f:
        for enonce, solution in zip(enonce_exos, solution_exos):
            # Construit la chaîne avec l'énoncé, le séparateur et la solution
            temp_content = latex_exo_final_formatter(enonce, solution)
            #temp_content = rep.include_latex_answer_into_question(temp_content)
            temp_content = points.def_points_for_exos(temp_content)
            temp_content = put_itemsep_to_one(temp_content)
            # Écrit dans le fichier et ajoute deux sauts de ligne après chaque paire
            final_contents.append(temp_content)
        final_content = '\n'.join(final_contents)
        auto_indent(final_content)
        #final_content = points.def_points_for_exos(final_content)
        f.write(final_content)

def use_case_one():
    fichier_latex = filedialog.askopenfilename(filetypes=[("LaTeX Files", "*.tex")])
    if not fichier_latex or fichier_latex == '':
        return
    fichier_sortie = fichier_latex.replace('.tex', '_TOOLS.tex')
    tcblowerize(input_file_path=fichier_latex, output_file_path=fichier_sortie) 
    # Afficher une boîte de dialogue de confirmation
    messagebox.showinfo("Confirmation", f"Les modifications ont été enregistrées dans :\n{fichier_sortie}")
    #print(f"Les modifications ont été enregistrées dans :\n{fichier_sortie}")

if __name__=="__main__":
    use_case_one()

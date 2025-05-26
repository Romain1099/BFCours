import re
from tkinter import filedialog

def search_exos_in_text(text: str) -> list[str]:
    pattern = re.compile(r'\\begin{EXO}.*?\\end{EXO}', re.DOTALL)
    output_list = pattern.findall(text)
    return output_list
def determine_itempoint_in_text(text: str) -> str:
    # Définir le modèle de recherche pour les itempoints avec capture du nombre dans les crochets
    enonce=text.split(r'\exocorrection')[0]

    pattern = re.compile(r'\\itempoint\[(\d+(?:\.\d+)?)\]', re.DOTALL)
    
    # Trouver toutes les occurrences de itempoint avec un nombre de points
    points = pattern.findall(enonce)
    
    # Calculer la somme totale des points trouvés
    number_points = sum(float(point) for point in points)
    # Si la somme est un entier (par exemple 7.0), on renvoie un int
    try:
        if number_points.is_integer():
            return str(int(number_points))
        else:
            return str(number_points)
    except Exception as e:
        print(f"Error {e}\nValeur 1 retournée.")
        return str(1)
    

def determine_points_in_exo(exo: str) -> str:
    points_dict = {
        "item": 1,
    }
    number_points_in_exo = 0

    for key, value in points_dict.items():
        points=exo.count(key) * value
        number_points_in_exo += points
    return str(number_points_in_exo)
def put_itempoint_if_not(exo: str) -> str:
    # Expression régulière pour trouver les \item qui ne sont pas suivis de \itempoint
    enonce,solution = exo.split(r"\exocorrection")
    # Permet de capturer les \item sans \itempoint en ignorant les espaces et sauts de ligne
    pattern = re.compile(r'(\\item)(?!\s*\\itempoint)', re.DOTALL)
    solution = re.sub(r'\\item ',r'\\tcbitem ',solution)
    # Remplacer chaque \item sans \itempoint par \item \itempoint[1]
    mod_enonce = pattern.sub(r'\1 \\tcbitempoint{1}[0][1cm]', enonce)
    mod_enonce = re.sub(r'(\\itempoint{\d+(?:\.\d+)?})\s+', r'\1', mod_enonce)
    mod_enonce = re.sub(r'\\item ', r'\\tcbitem ', mod_enonce)
    mod_exo = f"{mod_enonce}\n\\exocorrection\n{solution}"
    return mod_exo
def determine_difficulty(points:str,exo:str):
    points=float(points)
    if points>=4:
        difficulty=2
    else:
        difficulty=1
    return difficulty

def def_points_for_exos(text: str) -> str:
    liste_exos = search_exos_in_text(text)
    modified_contents = []
    for exo in liste_exos:
        exo = put_itempoint_if_not(exo)
        points = determine_itempoint_in_text(exo).replace('.','{,}')
        difficulty=determine_difficulty(points,exo)
        modified_content = f"\\def\\rdifficulty{{{difficulty}}}\n{exo}" #avant on faisait \\def\\points{{{points}}}
        modified_contents.append(modified_content)
    return '\n\n'.join(modified_contents)

if __name__=="__main__":
    fichier_latex = filedialog.askopenfilename(filetypes=[("LaTeX Files", "*.tex")])
    with open(fichier_latex, 'r') as f:
        content = f.read()
    fichier_sortie = fichier_latex.replace('.tex', '_POINTS.tex')
    final_content = def_points_for_exos(content)
    with open(fichier_sortie, 'w') as f:
        f.write(final_content)
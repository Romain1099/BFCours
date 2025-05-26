import re
def extract_questions_and_solutions(exercise_text):
    """Extrait les questions et les solutions de l'exercice."""
    questions_part, solutions_part = exercise_text.split('\\tcblower')
    # Divise le texte en lignes
    lines = exercise_text.split('\n')

    # Initialise le header à None
    header = None

    # Parcourt toutes les lignes pour trouver celle qui contient \begin{EXO}
    for line in lines:
        if '\\begin{EXO}' in line:
            header = line
            break

    # Assure-toi d'avoir trouvé un header avant de continuer
    if header is None:
        raise ValueError("Header non trouvé dans le texte de l'exercice.")
    questions = re.findall(r'\\item(.*?)\n', questions_part, re.DOTALL)
    solutions = re.findall(r'\\item(.*?)\n', solutions_part, re.DOTALL)
    
    return questions, solutions,solutions_part,header

def associate_questions_solutions(questions, solutions):
    """Associe chaque question à sa solution correspondante."""
    associated_content = []
    for question, solution in zip(questions, solutions):
        associated_content.append((question.strip(), solution.strip()))
    return associated_content

def reconstruct_exercise(associated_content,solution_part,header):
    """Reconstruit l'exercice avec les solutions incluses dans les questions."""
    reconstructed_text = f"""{header}
\\vspace{{-0.5cm}}
\\begin{{multicols}}{{2}}
    \\begin{{enumerate}}

"""
    number_item=0
    for question, solution in associated_content:
        if number_item==0:
            after_item="\n\n      \\columnbreak\n\n"
            number_item+=1
        elif number_item==1:
            after_item="""
    \\end{enumerate}
\\end{multicols}
\\vspace{-0.5cm}
\\begin{multicols}{2}
    \\begin{enumerate}[start=3]
"""
            number_item=0
        else:
            print("Bug avec la reconstruction des items... aucun cas trouvé.")
        reconstructed_text += f"\\item {question} \\repsim[1.5cm]{{{solution}}}%auto{after_item}"
        
    if "\\end{EXO}" in solution_part:
        solution_part=solution_part.replace("\\end{EXO}","")
    reconstructed_text+=f"""
    \\end{{enumerate}}
\\end{{multicols}}

\\tcblower \n {solution_part}"""
    reconstructed_text += """
\\end{EXO}
"""

    reconstructed_text = reconstructed_text.replace("%auto", "")
    reconstructed_text=replace_sequence_in_text_only_if_empty(reconstructed_text)
    return reconstructed_text
def replace_sequence_in_text_only_if_empty(text: str) -> str:
    # Définition du motif à rechercher
    pattern = re.compile(
        re.escape(r'\end{enumerate}') + r'\s*' + 
        re.escape(r'\end{multicols}') + r'\s*' +
        re.escape(r'\vspace{-0.5cm}') + r'\s*' + 
        re.escape(r'\begin{multicols}{2}') + r'\s*' +
        re.escape(r'\begin{enumerate}[start=3]') + r'\s*' +
        # Vérification qu'il n'y a que des espaces blancs ou des sauts de ligne jusqu'au \end{enumerate}
        # Cela signifie que nous cherchons à remplacer seulement si c'est vide entre \begin{enumerate}[start=3] et \end{enumerate}
        r'(\n\s*\n)' +
        re.escape(r'\end{enumerate}') + r'\s*' +
        re.escape(r'\end{multicols}'),
        re.DOTALL
    )
    
    # Remplacement de la séquence trouvée par \end{enumerate}, si elle est vide
    replaced_text = pattern.sub(r'\\end{enumerate}\n\\end{multicols}', text)
    print("Une séquence remplacée avec un enumerate vide.")
    return replaced_text
def include_latex_answer_into_question(exercise_text):
    """Intègre les solutions aux questions et reconstruit l'exercice."""
    questions, solutions,solution_part,header = extract_questions_and_solutions(exercise_text)
    associated_content = associate_questions_solutions(questions, solutions)
    
    return reconstruct_exercise(associated_content,solution_part,header)

if __name__=="__main__":
    # Exemple d'utilisation
    exercise_text = r"""
    \begin{EXO}{Poser et effectuer les calculs suivants.}{6C30-0}

    \begin{enumerate}[itemsep=2em]
        \item $7{,}725\times46{,}39$
        \item $4{,}564\times52{,}79$
        \item $9{,}542\times67{,}42$
        \item $2{,}956\times12{,}66$
    \end{enumerate}

    \tcblower

    \begin{enumerate}[itemsep=1em]
    \item \opmul[displayshiftintermediary=all,decimalsepsymbol={,},voperator=bottom,voperation=top]{7.725}{46.39}$\phantom{espace}$\opmul[displayshiftintermediary=all,decimalsepsymbol={,},voperator=bottom,voperation=top]{46.39}{7.725}
    \item \opmul[displayshiftintermediary=all,decimalsepsymbol={,},voperator=bottom,voperation=top]{4.564}{52.79}$\phantom{espace}$\opmul[displayshiftintermediary=all,decimalsepsymbol={,},voperator=bottom,voperation=top]{52.79}{4.564}
    \item \opmul[displayshiftintermediary=all,decimalsepsymbol={,},voperator=bottom,voperation=top]{9.542}{67.42}$\phantom{espace}$\opmul[displayshiftintermediary=all,decimalsepsymbol={,},voperator=bottom,voperation=top]{67.42}{9.542}
    \item \opmul[displayshiftintermediary=all,decimalsepsymbol={,},voperator=bottom,voperation=top]{2.956}{12.66}$\phantom{espace}$\opmul[displayshiftintermediary=all,decimalsepsymbol={,},voperator=bottom,voperation=top]{12.66}{2.956}
    \end{enumerate}

    \end{EXO}
    """

    included_solution = include_latex_answer_into_question(exercise_text)
    print(included_solution)

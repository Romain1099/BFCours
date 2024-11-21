import csv
import json
import numpy as np

class statisticsLatexFile():
    """
    classe facilitant la création de documents latex pour les statistiques d'un devoir
    """
    def __init__(self,content:str="",csv_filename:str="",additionnal_packages="",themes="",titre=""):
        self.brut_content=content
        self.titre=titre
        self.tex_certified_content=""
        self.tools_content=""
        self.available_content_types=["brut"]
        self.filepath=csv_filename
        self.statistics=self.make_prof_statistics(self.filepath)
        self.date_devoir=self.get_date(self.filepath)
        print(f"self date devoir : {self.date_devoir}")
        self.theme_devoir=themes if themes else ""
        self.bareme=self.relever_bareme(self.filepath)
        self.alternate_rowcol = 0
        package="""
\\documentclass[a4paper]{article}
\\geometry{left=1cm,right=1cm,top=2cm,bottom=2cm}

\\usepackage{bfcours}
\\usepackage[utf8]{inputenc}
\\usepackage{datatool}
\\usepackage{geometry}
\\usepackage{pgfplots}
\\pgfplotsset{compat=1.18}
\\usepgfplotslibrary{polar}
\\usepackage{pgfplotstable}
\\usepackage{float}
\\usepackage{multicol}
\\usepackage[most]{tcolorbox}
\\usepackage{hyperref}

\\geometry{left=1cm,right=1cm,top=2cm,bottom=2cm}
\\DTLsetseparator{;} % Assurez-vous que cela correspond au séparateur de votre fichier CSV."""
        if additionnal_packages=="":
            self.packages=package
        else:
            self.packages=package+str(additionnal_packages)
        self.commands="""

% Définition d'une nouvelle tcolorbox minimaliste
\newtcolorbox{NoneBox}[1][]{
    colframe=white, % Couleur de la bordure
    colback=white, % Couleur de fond
    boxsep=0pt, % Pas d'espace entre le texte et les bords de la boîte
    top=0pt, bottom=0pt, left=0pt, right=0pt, % Pas de marges intérieures
    boxrule=0pt, % Pas de bordure visible
    width=6cm,
    height=3cm,
    arc=0pt, % Coins non arrondis
    #1 % Permettre des options supplémentaires à la volée
}

\\newcommand\\boitesignature[1][]{
\\begin{multicols}{2}
    \\begin{NoneBox}
        #1
    \\end{NoneBox}
    
    \\columnbreak
    
    \\begin{tcolorbox}[nobeforeafter,width=5cm,height=3cm,title=\\bfseries Signature des parents :,halign title=flush left,fonttitle=\\bfseries,colbacktitle=black,coltitle=white,colback=white]%red!50!black
        \\vspace{2cm}
    \\end{tcolorbox}
\\end{multicols}
}
"""

        self.printable_content=self.make_printable()
        #self.csv_content=self.open_csv_file(csv_filename)

    def get_date(self, filepath: str) -> str:
        """
        Lit un fichier CSV et extrait la première date notée dans la colonne des dates.

        Args:
        filepath (str): Le chemin d'accès au fichier CSV.

        Returns:
        str: La première date trouvée dans la colonne appropriée, ou une chaîne vide si aucune date n'est trouvée ou si une erreur survient.
        """
        try:
            with open(filepath, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                headers = next(reader)  # Lecture de la première ligne pour obtenir les en-têtes

                # Trouver l'index de la colonne 'date'
                date_index = headers.index('Date')

                # Parcourir les lignes pour trouver la première date non vide
                for row in reader:
                    if row[date_index].strip():  # Vérifier si la date n'est pas vide
                        return row[date_index].strip()

            return ""  # Retourner une chaîne vide si aucune date n'est trouvée
        except FileNotFoundError:
            self.error_code = "Le fichier spécifié n'a pas été trouvé."  # Gestion des erreurs de fichier non trouvé
            return ""
        except ValueError:
            self.error_code = "La colonne 'date' est introuvable."  # Gestion des erreurs si la colonne 'date' n'est pas présente
            return ""
        except Exception as e:
            self.error_code = f"Erreur lors de la lecture du fichier: {str(e)}"  # Gestion des autres erreurs potentielles
            return ""
    def search_best_content(self)->str:
        order=['brut','tex_certified','tools']
        # Trouver le contenu disponible avec la plus haute priorité
        highest_priority_type = None
        for content_type in order:
            if content_type in self.available_content_types:
                highest_priority_type = content_type

        # Si un type de contenu prioritaire est trouvé, utiliser son contenu associé
        if highest_priority_type:
            return getattr(self, f"{highest_priority_type}_content")
        else:
            return None
    
    def make_printable(self)->str:
        
        introduced_content=self.search_best_content()
        printable_content=f"""
%%% Début - Zone d'insertion des packages %%%
    {self.packages}
%%% Fin - Zone d'insertion des packages %%%

%%% Début - Zone d'insertion des commandes %%%
    {self.commands}
%%% Fin - Zone d'insertion des commandes %%%

\\begin{{document}}

    {introduced_content}

\\end{{document}}
        """
        return printable_content
    def relever_bareme(self,input_file: str):
        """
        Calcule la note totale possible selon le barème indiqué dans la colonne 'Bareme' d'un fichier CSV,
        où chaque entrée de 'Bareme' contient plusieurs valeurs numériques séparées par des virgules.

        Cette fonction lit le fichier CSV, trouve la colonne 'Bareme', extrait toutes les valeurs,
        les convertit en float et additionne toutes ces valeurs pour calculer la note totale.

        :param input_file: Chemin du fichier CSV d'entrée.
        :return: Note totale possible selon le barème, en float.
        """
        with open(input_file, 'r', newline='', encoding='utf-8') as infile:
            reader = csv.DictReader(infile, delimiter=';')
            
            for row in reader:
                if 'Bareme' in row and row['Bareme'].strip():
                    # Séparer les valeurs du barème et additionner après conversion en float
                    bareme_values = row['Bareme'].split(',')
                    break
        return bareme_values
    
    def open_csv_file(self, filepath):
        """
        Opens a CSV file and reads its content securely.
        """
        self.filepath = filepath
        try:
            with open(filepath, newline='', encoding='utf-8') as file:
                return list(csv.reader(file, delimiter=';', escapechar='\\'))
        except FileNotFoundError:
            self.error_code = "File not found"
            return None
        except Exception as e:
            self.error_code = "Error opening file: " + str(e)
            return None

    def make_prof_statistics(self,filepath=""):
        """
        Calculate statistics such as mean, first and third quartiles for student performance data.
        """
        if filepath=="":
            if self.filepath=="":
                return "Chemin vers le fichier csv non saisi"
            else:
                use_path=self.filepath
        else:
            use_path = filepath

        content = self.open_csv_file(use_path)
        
        if content is None:
            return []

        headers = content[0]
        data = content[1:]
        print(headers,data)
        # Find index for exercises
        idx_exercises = headers.index('Exercices')
        # Initialize a dictionary to hold scores for each exercise across all students
        exercises_scores = {}

        # Collect scores for each exercise from each student
        for item in data:
            #print(f"item : {item} \n idx_exercises :{idx_exercises}")
            #print(f"ce qu'on veut : {item[idx_exercises]}")
            scores = list(map(float, item[idx_exercises].split(',')))
            for i, score in enumerate(scores):
                if i not in exercises_scores:
                    exercises_scores[i] = []
                exercises_scores[i].append(score)
            #print(f"exercises_scores={exercises_scores}")
            #print(scores)
        statistics = {
            'means': [],
            '1st_quartiles': [],
            '3rd_quartiles': [],
            'medianes': [],
            'global_mean': 0,
            'global_1st_quartile': 0,
            'global_3rd_quartile': 0,
            'global_median': 0
        }
        
        # Compute statistics for each exercise and store them in the dictionary
        for i, scores in exercises_scores.items():
            statistics['means'].append(f"{np.mean(scores):.2f}")
            statistics['1st_quartiles'].append(f"{np.percentile(scores, 25):.2f}")
            statistics['3rd_quartiles'].append(f"{np.percentile(scores, 75):.2f}")
            statistics['medianes'].append(f"{np.median(scores):.2f}")
        
        # Calculate total scores for each student
        num_students = len(data)
        total_scores = [0] * num_students

        for idx, item in enumerate(data):
            scores = list(map(float, item[idx_exercises].split(',')))
            total_scores[idx] = sum(scores)
        
        # Compute global statistics
        statistics['global_mean'] = f"{np.mean(total_scores):.2f}"
        statistics['global_1st_quartile'] = f"{np.percentile(total_scores, 25):.2f}"
        statistics['global_3rd_quartile'] = f"{np.percentile(total_scores, 75):.2f}"
        statistics['global_median'] = f"{np.median(total_scores):.2f}"

        # Print statistics for verification
        print(f"statistics : {statistics}")
        
        return statistics
    
    def make_prof_latex_content(self,filepath,baremes):
        """
        Cette fonction permet de calculer les moyennes et quartiles du csv.
        Elle met en forme ces datas pour constituer un document latex complet constituant un rapport détaillé du devoir.
        Pour cela elle appelle plusieurs méthodes annexes, qu'il faudra implémenter sur la base de l'exemple que je vais te montrer ( c'était pour la version élève ). 
        1 : tableau_prof un tableau dans lequel on verra la moyenne à chaque exercice, le bareme de chaque exercices ainsi que les quartiles. 
            En mode : stats & {\scriptsize 1er quartile} - $\mathbf{moyenne}$ - {\scriptsize 3ème quartile} \\
                \hline
                bareme & ...
        2 : radar_prof un radar similaire à celui élève mais il doit avoir en rouge la moyenne à l'exercice, en vert foncé le 3eme quartile, et en orange le 1er quartile
            on fait ça avec des addplot. 
        3 : commentaires avec les exercices qu'il faudra retravailler en remédiation suivant que la moyenne ou le 3eme quartile sont en dessous de 50% du bareme
        """
        produced_latex_content=""
        
        table = self.make_prof_table(self.statistics, baremes)
        radar = self.make_radar(self.statistics['means'], baremes,modality="prof")
        comments = ""#self.make_prof_comments(self.statistics['means'], self.statistics['baremes'])



        return produced_latex_content
    
    def produce_latex_file(self,output_filepath):
        modified_content=False
        #modifications de self.content en stockant dans modified_content
        content=self.make_printable()
        with open(output_filepath,'w', encoding='utf-8') as file:
            file.write(content)
            modified_content=True
        
        return modified_content
    
    """
    commandes destinées à etre utilisées pour designer des éléments de contenu des fichiers stats
    """
    def radar_xtickslabels(self,exercice=[],bareme=[]):
        xticks=""
        xtickslabels=""
        marks=""
        #print(f"\n\n\n exercice : {exercice}")
        delta=360/len(exercice)

        for index,points in enumerate(exercice):
            xtick=str(index*delta)
            mark_point=float(points)*100/float(bareme[index])
            xticks+=xtick
            xtickslabels+=f"\\huge \\bfseries Ex.{index+1}"
            marks+=f"({xtick},{str(mark_point)})  "
            if index+1<len(exercice):
                xticks+=","
                xtickslabels+=","
 
        return xticks,xtickslabels,marks
    def make_additionnal_radar_plot(self,fill="none",color="blue",opacity="0.5",marks=""):
        latex_content=f"""
        \\addplot+[mark=none,fill={fill},opacity={opacity},line width = 2pt,dashed,color={color}] coordinates {{
                    {marks}
                }} -- cycle;
        """
        return latex_content
    def make_radar(self,exercices:list[float],bareme:list[float],scale="0.5",modality="")->str:
        
        xticks,xtickslabels,marks=self.radar_xtickslabels(exercices,bareme)#\large \bfseries EX1, \large \bfseries EX2, \large \bfseries EX3       {0,120,240}
        additionnal_content=""#
        if modality=="":
            additionnal_content=""#
        elif modality=="student":
            means=self.statistics["means"]
            student_xticks,student_xtickslabels,student_marks=self.radar_xtickslabels(means,bareme)#\large \bfseries EX1, \large \bfseries EX2, \large \bfseries EX3       {0,120,240}
        
            additionnal_content=self.make_additionnal_radar_plot(color="red",opacity="1",marks=student_marks)
        elif modality=="prof":
            
            quartile_up=self.statistics["1st_quartiles"]
            print(f"quartile_up : {quartile_up}")
            quartile_up_xticks,quartile_up_xtickslabels,quartile_up_marks=self.radar_xtickslabels(quartile_up,bareme)#\large \bfseries EX1, \large \bfseries EX2, \large \bfseries EX3       {0,120,240}
            additionnal_content+=self.make_additionnal_radar_plot(color="black",opacity="1",marks=quartile_up_marks)
            quartile_down=self.statistics["3rd_quartiles"]
            quartile_down_xticks,quartile_down_xtickslabels,quartile_down_marks=self.radar_xtickslabels(quartile_down,bareme)#\large \bfseries EX1, \large \bfseries EX2, \large \bfseries EX3       {0,120,240}
            additionnal_content+=self.make_additionnal_radar_plot(color="black",opacity="1",marks=quartile_down_marks)
        color="blue"
        scale=scale
        radar=f"""
\\begin{{center}}
    \\begin{{tikzpicture}}[scale={scale}]
        \\begin{{polaraxis}}[
            width=0.8\\textwidth,
            xtick={{{xticks}}},
            xticklabels={{{xtickslabels}}},
            ymin=0, ymax=100,
            ytick={{0,25,50,75,100}},
            yticklabels={{\\large \\bfseries MI,\\large \\bfseries MF,\\large \\bfseries MS,\\large \\bfseries TBM, }}
        ]
        \\addplot+[mark=none,fill={color},opacity=0.5] coordinates {{
            {marks}
        }} -- cycle;
        {additionnal_content}
        \\end{{polaraxis}}
    \\end{{tikzpicture}}
\\end{{center}}
"""
        return radar
    
    
    def get_table_params(self,exercices,bareme):

        columns_geometry="|c|"
        columns_headers=""
        points_table=""
        bareme_table=""
        for index,points in enumerate(exercices):
            columns_geometry+= "c|"
            columns_headers+= " & " + f"\\bfseries Exercice {index+1} "
            points_table+= " & " + str(points)
            bareme_table+= " & " + str(bareme[index])
        return columns_geometry,columns_headers,points_table,bareme_table
    def get_results_table_params(self,exercices,bareme):

        columns_geometry="c|c|c|c|"
        columns_headers="\\rowcolor{blue!75!black}\\bfseries \\color{white}Nom & \\bfseries \\color{white}Prenom & \\bfseries \\color{white}Total"
        points_table=""
        bareme_table=""
        for index,points in enumerate(exercices):
            columns_geometry+= "c|"
            columns_headers+= " & " + f"\\bfseries \\color{{white}}E{index+1} "
            points_table+= " & " + str(points)
            bareme_table+= " & " + str(bareme[index])
        
        return columns_geometry,columns_headers,points_table,bareme_table
    def make_table(self,exercices:list[float],bareme:list[float])->str:
        columns_geometry,columns_headers,row_points,row_bareme=self.get_table_params(exercices,bareme)
        table=f"""
\\begin{{tcbtab}}[Par exercice :]{{{columns_geometry}}}
      \hline
      {columns_headers} \\\\
      \hline
      \\bfseries Points {row_points} \\\\
      \hline
      \\bfseries Barème {row_bareme} \\\\
      \hline
\end{{tcbtab}}
"""
        return table
    def make_prof_table(self,statistics="", bareme=[]) -> str:
        if self.statistics is None:
            return "Statistics not calculated yet."

        # Start building the LaTeX table
        table_latex = "\\begin{tcbtab}[Statistiques]{c|c|c|c|c}\n\\hline\n"
        table_latex += " & q1 & Moyenne & q3 & Barème \\\\ \\hline\n"
        
        # Iterate over exercises and build the row for each
        for i in range(len(self.statistics['means'])):
            # Assume the statistics lists are synchronized and have the same length as bareme
            quartile1 = self.statistics['1st_quartiles'][i]
            mean = self.statistics['means'][i]
            quartile3 = self.statistics['3rd_quartiles'][i]
            bar = bareme[i]
            mean = str(mean).replace(".","{,}")
            quartile1 = str(quartile1).replace(".","{,}")
            quartile3 = str(quartile3).replace(".","{,}")
            # Format the stats for each exercise
            stats_formatted = f"{{\\scriptsize {quartile1}}} & $\\mathbf{{{mean}}}$ & {{\\scriptsize {quartile3}}}"
            
            # Add the formatted statistics and bareme to the table
            table_latex += f"Exercice {i+1} & {stats_formatted} & {bar} \\\\ \\hline\n"
        
        # Close the table environment
        table_latex += "\\end{tcbtab}"

        return table_latex
    
    def make_tips(self,title="",tips=""):
        if title=="":
                tip_title="Comment retravailler un exercice ?"
        else:
            tip_title=title
        if tips=="":
            tip=f"""
            \\begin{{itemize}}
                \\item Relire la correction une fois.
                \\item Cacher la correction puis \\textbf{{effectuer à nouveau}} l'exercice.
                \\item Comparer la correction avec la nouvelle réponse. \\textbf{{Recommencer}} chaque jour tant que ce n'est pas parfait. 
            \\end{{itemize}}
            """
        else:
            tip=f"""
            {tips}
            """
        return tip_title,tip
    def make_explications(self,exercice,bareme,explications,tips_title="",tips=""):
        content=""
        catch_phrase=""
        first=True
        """if not isinstance(explications,list):
            explications=[""] * len(exercice)"""
        for index,points in enumerate(exercice):
            if float(points)/float(bareme[index])<0.5:
                catch_phrase+=f"""\\item \\textbf{{Exercice {index+1}}} à retravailler."""
                if explications[index]:
                    catch_phrase+=f"""\\\\ 
                    {explications[index]}
                    """
                catch_phrase+=f"""
            """
        if catch_phrase:
            content=f"""
            \\begin{{itemize}}

                {catch_phrase}
            \\end{{itemize}}

    """
        else:
            content="Les compétences semblent suffisamment maîtrisées, \\textbf{bien joué} !"
        return content
    def make_int_or_half(self,note):
        note = round(note * 2) / 2
        if note.is_integer():  # Vérifie si note est un entier (pas de partie fractionnaire)
            note = int(note)   # Convertit en int si c'est vrai
        return note
    def make_final_note(self,exercices,bareme):
        """
        1. additionne les float de exercices. assigne à note
        2. fait de même avec les float de bareme. assigne à total
        """
        note=0
        total=0
        # Addition des points obtenus dans chaque exercice
        for ex in exercices:
            note += float(ex)

        # Addition des points maximaux pour chaque exercice du barème
        for bm in bareme:
            total += float(bm)
        # Arrondi de la note au demi-point le plus proche
        note = round(note * 2) / 2
        if note.is_integer():  # Vérifie si note est un entier (pas de partie fractionnaire)
            note = int(note)   # Convertit en int si c'est vrai

        # Arrondi du total au demi-point le plus proche
        total = round(total * 2) / 2
        if total.is_integer():  # Vérifie si total est un entier
            total = int(total)  # Convertit en int si c'est vrai
        return note,total
    
    def make_full_student_recap(self,exercices,bareme,explications,student_label,tips_title,tips,theme="",date_devoir=""):
        #print(f"exercices : {exercices}")
        if date_devoir!=self.date_devoir and date_devoir!="":
            self.date_devoir=date_devoir
        table=self.make_table(exercices,bareme)
        radar=self.make_radar(exercices,bareme,modality="student")
        explication=self.make_explications(exercices,bareme,explications,tips=tips)
        tip_title,tip=self.make_tips(title=tips_title,tips=tips)
        note,total=self.make_final_note(exercices,bareme)
        note = str(note).replace(".","{,}")
        total = str(total).replace(".","{,}")
        if date_devoir!=self.date_devoir:
            date_devoir=self.date_devoir
        theme=self.theme_devoir
        latex_date_devoir=date_devoir.replace('_','/')
        tip_tex_aborted="""\\boite{{{tip_title}}}{{
            {tip}
        }}"""
        latex=f"""
\\section{{Résultats de {student_label}}}

    %%% debut - tableau %%%
    \\boitesignature{{
    \\textbf{{Titre : }}{self.titre}
    \\textbf{{Contrôle effectué le : {latex_date_devoir}}} \\\\
    \\textbf{{Thèmes abordés : }}{theme}
    }}{{\\begin{{center}}\\bfseries\\huge{{{note}/{total}}} \\end{{center}}}}

    \\begin{{center}}
        {table}
    \\end{{center}}

    %%% fin - tableau %%%

\\begin{{multicols}}{{2}}

    %%% debut - explications %%%
    \\boite{{Commentaires :}}{{
        {explication}
    }}
    %%% fin - explications %%%
    
    \\columnbreak

    %%% debut - radar %%%
    
    {radar}

    %%% fin - radar %%%

\\end{{multicols}}
"""
        self.available_content_types.append("tools")
        self.tools_content=latex
        return latex
    def read_baremes(self,type="Total"):
        """
        Lit le fichier CSV et extrait les barèmes de la deuxième ligne du fichier.
        """
        with open(self.filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            # Sauter la première ligne (qui est normalement l'en-tête)
            next(reader, None)  # Ignore l'en-tête si pas déjà fait par DictReader
            second_line = next(reader, None)  # Lire la deuxième ligne
            if second_line and 'Bareme' in second_line:
                baremes = [float(n) for n in second_line['Bareme'].split(',')]
                if type == "Total":
                    return sum(baremes)
                else:
                    return baremes
            else:
                raise ValueError("La ligne contenant les barèmes est manquante ou mal formatée.")
    def determine_notes(self):
        """
        Lit les données d'un fichier CSV et calcule la somme des notes pour chaque ligne.
        """
        notes = []
        bareme=self.read_baremes()
        with open(self.filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            
            for row in reader:
                if 'Exercices' in row:  # Vérifie que la colonne existe
                    note = [float(n) for n in row['Exercices'].split(',')]
                    
                    notes.append(sum(note))
                else:
                    raise ValueError("La colonne 'Exercices' est manquante dans le fichier CSV.")
        return notes, bareme
    def get_cellcoll_by_note(self,n,idx)->str:
        indic= n/idx
        if indic<0.25:
            color="red"
        elif 0.25<indic<0.5:
            color="orange"
        elif 0.5<indic<0.75:
            color="blue"
        elif indic>=0.75:
            color="green"
        else:
            color="blue"
        return f"{color}!15!white"
    
    def get_alternate_rowcol(self):
        if self.alternate_rowcol == 0:
            self.alternate_rowcol +=1
            return "blue!10!white"
        else:
            self.alternate_rowcol = 0
            return "blue!5!white"
    def make_result_table(self,filepath):
        notes = []
        with open(self.filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            bareme_sample = self.read_baremes(type="List")

            columns_geometry,columns_headers,row_points,row_bareme=self.get_results_table_params(bareme_sample,bareme_sample)
            table=f"""
    \\begin{{center}}
        \\begin{{tcbtab}}{{{columns_geometry}}}
        \hline
        {columns_headers} \\\\
        \hline
"""
            for row in reader:
                nom_lab = '\ufeffNom'
                if 'Exercices' in row:
                    if f"{nom_lab}" in row :
                        if 'Prenom' in row:  # Vérifie que la colonne existe
                            print("1")
                        else:
                            raise ValueError("La colonne 'Prenom' est manquante dans le fichier CSV.")
                    else:
                        raise ValueError(f"La colonne {nom_lab} est manquante dans le fichier CSV.")
                    note = [float(n) for n in row['Exercices'].split(',')]
                    tex_note = '& '.join([f"\\num{{{int(n)}}}" if n.is_integer() else f"\\num{{{n}}}" for idx,n in enumerate(note)])
                    sumnote = int(sum(note)) if sum(note).is_integer() else sum(note)
                    total = sum(bareme_sample)
                    row_points = f"\\rowcolor{{{self.get_alternate_rowcol()}}}\\bfseries {row[nom_lab]} & \\bfseries {row['Prenom']} & \\cellcolor{{{self.get_cellcoll_by_note(sumnote,total)}}} \\color{{black}}\\bfseries\\num{{{sumnote}}} & {tex_note}"
                    table+=f"""
      {row_points} \\\\
      \\hline
"""
                    notes.append(sum(note))
                else:
                    raise ValueError("La colonne 'Exercices' est manquante dans le fichier CSV.")
                
        table+=f"""
\\end{{tcbtab}}
\\end{{center}}
"""
        return table
    def make_diagram(self, filepath, number_classes=10):
        """
        Retourne le code TikZ pour un diagramme de répartition des notes réparties en nombre spécifié de classes.
        """
        print(filepath)
        notes, bareme = self.determine_notes()

        # On s'assure que la note minimum est 0 et qu'on couvre jusqu'au barème maximum
        max_note = max(bareme, max(notes))
        min_note = 0
        
        # Calcul de l'intervalle en fonction du nombre de classes
        interval = (max_note - min_note) / number_classes
        bins = [0] * number_classes
        
        # Comptage des notes dans chaque classe
        for note in notes:
            index = int((note - min_note) / interval)
            index = min(index, number_classes - 1)  # Assurer que l'indice reste dans les limites des classes
            bins[index] += 1

        # Largeur des barres ajustée
        bar_width = 1 / (number_classes + 1)  # Ajuste ce facteur pour l'espacement et largeur des barres

        # Positions et étiquettes des graduations
        xtick_positions = [min_note + (i + 0.5) * interval for i in range(number_classes)]  # Centrer les ticks
        xtick_labels = [f'{min_note + i * interval:.1f}' for i in range(number_classes + 1)]  # Affichage propre des labels

        print(f"""
            bins : {bins}
                xticks pos : {xtick_positions}
                xticks lab : {xtick_labels}
            """
            )

        # Génération du code TikZ
        tikz_code = "\\begin{tikzpicture}\n\\begin{axis}[\n" \
                    "width=\\textwidth,\n" \
                    "ybar=1.0,\n" \
                    f"bar width={bar_width * 10}cm,\n" \
                    "height=8cm,\n" \
                    "ylabel={Nombre d'étudiants},\n" \
                    "xlabel={Notes},\n" \
                    "xtick=data,\n" \
                    "xtick align=inside,\n" \
                    "xticklabel style={align=center},\n" \
                    "xtick={%s},\n" \
                    "xticklabels={%s},\n" \
                    "nodes near coords,\n" \
                    "area style,\n" \
                    "]\n" % (
                        ', '.join(f'{x:.1f}' for x in xtick_positions),
                        ', '.join(xtick_labels)
                    )

        # Ajouter les données dans TikZ
        tikz_code += "\\addplot coordinates {\n"
        for i in range(number_classes):
            tikz_code += f"({xtick_positions[i]:.2f}, {bins[i]}) "

        tikz_code += "};\n\\end{axis}\n\\end{tikzpicture}"

        return tikz_code


    def make_diagram_old(self, filepath, number_classes):
        """
        Retourne le code TikZ pour un diagramme de répartition des notes réparties en nombre spécifié de classes.
        """
        print(filepath)
        notes, bareme = self.determine_notes()
        max_note = max(notes) if notes else 0
        min_note = min(notes) if notes else 0
        interval = (bareme - 0) / number_classes if max_note != min_note else 1
        bins = [0] * number_classes
        for note in notes:
            index = int(note / interval)
            index = min(index, number_classes - 1)  # Ajuste l'indice pour éviter un dépassement de liste
            bins[index] += 1

        # On ajuste la largeur des barres pour qu'elles occupent l'espace entre deux ticks
        bar_width = 1 / (number_classes - 2)  # Ajuste ce facteur pour contrôler l'espacement entre les barres

        xtick_positions = [int(i * interval) for i in range(number_classes+1)]
        #bar_width=max(xtick_positions[1]-xtick_positions[0],bar_width)
        print(f"bar_width : {bar_width}")
        xtick_labels = [f'{int(i * interval)}' for i in range(number_classes+1)]#:.2f
        print(f"""
              bins : {bins}
                xticks pos : {xtick_positions}
                xticks lab : {xtick_labels}
              """
              )

        tikz_code = "\\begin{tikzpicture}\n\\begin{axis}[\n" \
                    "width=\\textwidth,\n" \
                    "ybar=1.0,\n" \
                    f"bar width={bar_width * 10}cm,\n" \
                    "height=8cm,\n" \
                    "ylabel={Nombre d'étudiants},\n" \
                    "xlabel={Notes},\n" \
                    "xtick=data,\n" \
                    "xtick align=inside,\n" \
                    "xticklabel style={align=center},\n" \
                    "xtick={%s},\n" \
                    "xticklabels={%s},\n" \
                    "nodes near coords,\n" \
                    "area style,\n"\
                    "]\n" \
                    "\\addplot coordinates {\n" % (
                        ', '.join(f'{x}' for x in xtick_positions),#:.2f
                        ', '.join(xtick_labels)
                    )

        for i in range(number_classes):
            tikz_code += f"({min_note + i * interval + interval / 2:.2f}, {bins[i]}) "

        tikz_code += "};\n\\end{axis}\n\\end{tikzpicture}"

        return tikz_code

    def make_prof_explication(self, means,bareme):
        """
        Génère une liste d'éléments pour LaTeX en regroupant les exercices selon leur niveau de réussite,
        en se basant sur les moyennes fournies pour chaque exercice.

        Args:
        means (list of float): Liste des moyennes pour chaque exercice.
        """
        categories = {
            'Très difficile': [],
            'Difficile': [],
            'Bien': [],
            'Excellent': []
        }
        
        for index, mean in enumerate(means, start=1):
            use_mean=float(mean)
            bareme_use=float(bareme[index-1])
            calculation=use_mean/bareme_use*100
            if calculation < 25:
                categories['Très difficile'].append(str(index))
            elif calculation < 50:
                categories['Difficile'].append(str(index))
            elif calculation < 75:
                categories['Bien'].append(str(index))
            else:
                categories['Excellent'].append(str(index))

        tex_content = "\\begin{itemize}\n"
        if categories['Très difficile']:
            tex_content += f"\\item Exercices non réussis : {', '.join(categories['Très difficile'])}\n"
        if categories['Difficile']:
            tex_content += f"\\item Exercices peu réussis : {', '.join(categories['Difficile'])}\n"
        if categories['Bien']:
            tex_content += f"\\item Exercices bien réussis : {', '.join(categories['Bien'])}\n"
        if categories['Excellent']:
            tex_content += f"\\item Exercices très bien réussis : {', '.join(categories['Excellent'])}\n"
        tex_content += "\\end{itemize}\n"

        return tex_content
    def make_prof_comp_table(self, filepath):
        notes = []
        with open(self.filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            bareme_sample = self.read_baremes(type="List")

            for row in reader:
                if 'Competences' in row:
                    exp = [n for n in 'et'.join(row['Competences'].split(',')).split('et')]
                    text = '\\\\\n'.join([e for e in exp])
                else:
                    raise ValueError("La colonne 'Competences' est manquante dans le fichier CSV.")

        return text
    def make_full_prof_recap(self,bareme,explications,tips_title,tips):

        diagram = self.make_diagram(self.filepath,10)
        table = self.make_prof_table(self.statistics, bareme)
        competences_table = self.make_prof_comp_table(self.filepath)
        radar = self.make_radar(self.statistics['means'], bareme,modality="prof")
        note,total=self.make_final_note(self.statistics['means'],bareme)
        note = str(note).replace(".","{,}")
        total = str(total).replace(".","{,}")
        result_table = self.make_result_table(self.filepath)
        analyse_texte=self.make_prof_explication(self.statistics['means'],bareme)
        item_explications ='\n'.join([f"\\item Exercice {i+1} :\\\\ {exp}" if exp else f"\\item Exercice {i+1} : Pas d'explication donnée\\\\ " for i,exp in enumerate(explications)])
        explication = f"""
        Note moyenne obtenue au contrôle : \\begin{{center}} $\\mathbf{{{note}/{total}}}$\\end{{center}}
        Explications pour les exercices : 
        \\begin{{itemize}}
            {item_explications}
        \\end{{itemize}}
        """
        #self.make_prof_comments(self.statistics['means'], self.statistics['baremes'])
        tip_title,tip=self.make_tips(title=tips_title,tips=tips)
        latex_date_devoir=self.date_devoir.replace('_','/')
        latex=f"""
\\section{{Analyse du devoir du {latex_date_devoir}}}

    \\subsection{{\\'Etude de la répartition des résultats}}

    %%% debut - Répartition des résultats %%%

    \\begin{{center}}
        {diagram}
    \\end{{center}}

    %%% fin - Répartition des résultats %%%
    
    \\subsection{{Compétences du devoir}}

    %%% debut - tableau %%%
    
    \\begin{{center}}
        {competences_table}
    \\end{{center}}

    %%% fin - tableau %%%

\\newpage

\\subsection{{Tableau d'analyse des résultats}}

    %%% debut - Tableau des résultats %%%

    {result_table}

    %%% fin - Tableau des résultats %%%

\\newpage
    
\\subsection{{Analyse par exercices}}

\\begin{{multicols}}{{2}}

    %%% debut - explications %%%
    \\boite{{Commentaires :}}{{
    
        %%% debut - analyse %%%

        {analyse_texte}

        %%% fin - analyse %%%

        {explication}

    }}
    %%% fin - explications %%%
    
    \\columnbreak

    %%% debut - tableau %%%
    
    \\begin{{center}}
        {table}
    \\end{{center}}

    %%% fin - tableau %%%

    %%% debut - radar %%%
    
    {radar}

    %%% fin - radar %%%

\\end{{multicols}}

"""
        self.available_content_types.append("tools")
        self.tools_content=latex
        return latex
def main():
    filepath='test8.csv'
    latex_manager=statisticsLatexFile("Hello World",csv_filename='test8.csv')
    #print(latex_manager.printable_content)
    #latex_manager.make_prof_statistics(filepath)

    #print(latex_manager.make_full_student_recap(exercices=[1,3,5,5,2],bareme=[3,4,5,10,5],explications=["C'est une question de cours qui doit être appris tous les jours.","C'est un exercice d'application très simple, tu devrais pouvoir y arriver !","","",""],student_label="TESTNOM Jean-Eudes",tips_title="",tips=""))
    #latex_manager.printable_content=latex_manager.make_printable()
    print(latex_manager.make_full_prof_recap(bareme=[1,3,5],explications="",tips_title="",tips=""))
    latex_manager.printable_content=latex_manager.make_printable()
    print(latex_manager.statistics)

if __name__=="__main__":
    main()
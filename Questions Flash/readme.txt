#A venir prochainement : Le logiciel QFgen permettant d'éditer les questions Flash

# Pour le modèle : 
L'image flash_eclair est définie par défaut comme image centrale…
Il est possible de paramétrer la commande \dbincopath dans l'entete 'bfcours-icons_insert' en sélectionnant un chemin absolu vers un répertoire d'images. 
Une fois ce dossier donné, il suffit de démute la commande \getrandomiconpath pour obtenir une image aléatoire dans ce dossier.

#Fonctionnalités : 

#Sélection de questions via une banque d'exercices en format json ( détails dans la doc )
structure : sous forme de liste : 
	{
                "enonce": "\\textbf{Calculer} la \\textbf{somme} des nombres relatifs $-12$ et $-8$.",
                "reponse": "$-20$",
                "details": "\\textbf{Calculer} la \\textbf{somme} des nombres relatifs $-12$ et $-8$ revient à \\textbf{additionner} ces deux nombres :\n$$ (-12) + (-8) = -12 - 8 $$\n\nOn applique la propriété de \\textbf{somme} des nombres relatifs, selon laquelle additionner deux nombres négatifs revient à additionner leurs valeurs absolues avec le signe négatif :\n$$ \\Rightarrow -12 - 8 = - (12 + 8) $$\n\\[\n- (12 + 8) = -20\n\\]\n\nAinsi, la \\textbf{somme} des nombres relatifs $-12$ et $-8$ est \\textcolor{red}{$-20$}.",
                "theme": "Addition",
                "prompt": "une question de calcul sur les additions de nombres  relatifs genre : -12 + ( -8)"
        }

# Interfaces de saisies : 
	Mode réduit 1 fenetre par catégorie ( question, réponse, réponse courte)
	Mode plein écran pour chaque fenetre possible sur ctrl + double clic
	Mode utilisation de macro sur sélection de texte via ctrl + clic droit sur la sélection
	Mode (hyper efficace pour les questions simples) implémentation complète d'une question par IA sur un prompt du type "Une question sur la somme de deux nombres relatifs"
	Mode implémentation particulier pour chaque fenetre avec appel intégré à l'IA

# Mode compilation 
	Le logiciel s'occupe de la compilation et ouvre le pdf produit. 

# Gestionnaire de groupes : 
	Le logiciel s'occupe du rangement : classement par niveau, les questions sont datées. 
# Export facile : 
	A venir : le logiciel s'occupera de constituer un dossier composé de questions choisies, prêt au transfert sur clé...

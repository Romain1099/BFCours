# Plan de transcription : Cartes auto-correctives équations

## Structure attendue du document

D'après le titre, il s'agit d'un document de cartes auto-correctives sur les équations. 
Ce type de document contient généralement :

1. **Cartes recto-verso** avec :
   - Recto : Une équation à résoudre
   - Verso : La solution détaillée
   
2. **Mise en page** :
   - Plusieurs cartes par page (probablement 4 ou 6)
   - Format cartes de révision
   - Possibilité de découper les cartes

3. **Contenu mathématique** :
   - Équations du premier degré
   - Équations du second degré
   - Systèmes d'équations
   - Équations avec fractions

## Structure proposée du projet LaTeX

```
Cartes_equations/
├── Cartes_equations.tex       # Fichier principal
├── enonce.tex                 # Contenu des cartes
├── images/                    # Images extraites du PDF
│   └── *.png
└── configuration.tex          # Définition de la tcolorbox pour les cartes
```

## Étapes de réalisation

1. Créer une tcolorbox personnalisée pour les cartes
2. Définir le système de mise en page avec tcbraster
3. Transcrire le contenu des cartes
4. Gérer le système recto-verso

## Commandes à définir

- `\carte{numero}{equation}{solution}` : Pour créer une carte complète
- `\carterecto{equation}` : Pour le recto seul
- `\carteverso{solution}` : Pour le verso seul

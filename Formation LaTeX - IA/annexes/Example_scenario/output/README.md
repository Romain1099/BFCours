# Cartes auto-correctives - Équations

## Description du projet

Ce projet LaTeX génère des cartes auto-correctives pour l'apprentissage de la résolution d'équations mathématiques. Les cartes sont conçues pour être imprimées en recto-verso avec une correspondance parfaite entre questions et réponses.

## Structure du projet

```
Cartes_equations/
├── Cartes_equations.tex       # Fichier principal (bfcours)
├── Cartes_equations_simple.tex # Fichier principal simplifié
├── configuration.tex          # Configuration des styles de cartes
├── enonce.tex                # Contenu (énoncés et solutions alternés)
└── README.md                 # Ce fichier
```

## Caractéristiques

### Format des cartes
- **4 cartes par page** (2×2)
- **Dimensions** : 9cm × 13cm par carte
- **Alternance** : Pages d'énoncés suivies de pages de solutions
- **Impression recto-verso** : Correspondance parfaite des positions

### Organisation des pages
- Page 1 : Énoncés 1-4
- Page 2 : Solutions 1-4
- Page 3 : Énoncés 5-8
- Page 4 : Solutions 5-8
- ...et ainsi de suite

### Types d'équations incluses
- **Cartes 1-8** : Équations du premier degré simples
- **Cartes 9-12** : Équations avec fractions
- **Cartes 13-16** : Équations du second degré

### Design
- **Énoncés** : Cadre bleu, fond blanc, texte grand et gras
- **Solutions** : Cadre vert, fond bleu clair, solution détaillée étape par étape
- **Numérotation** : Automatique en haut de chaque carte

## Compilation

### Avec pdfLaTeX (recommandé pour les tests)
```bash
pdflatex Cartes_equations_simple.tex
```

### Avec LuaLaTeX (pour bfcours complet)
```bash
lualatex Cartes_equations.tex
```

## Utilisation pédagogique

1. **Imprimer** en recto-verso (retourner sur le bord court)
2. **Vérifier** l'alignement : carte 1 doit correspondre à solution 1 au verso
3. **Découper** les cartes selon les bordures
4. **Utiliser** : 
   - L'élève lit l'équation au recto
   - Il tente de la résoudre sur papier
   - Il retourne la carte pour vérifier sa solution

## Personnalisation

### Ajouter de nouvelles cartes
Respectez l'alternance des pages dans `enonce.tex` :

```latex
% Page d'énoncés (4 cartes)
\begin{pageenonces}
    \begin{tcolorbox}[carteenonce={17}]
        \eqcarte{votre équation}
    \end{tcolorbox}
    % ... 3 autres cartes
\end{pageenonces}

% Page de solutions correspondantes
\begin{pagesolutions}
    \begin{tcolorbox}[cartesolution={17}]
        \solcarte{solution détaillée}
    \end{tcolorbox}
    % ... 3 autres solutions
\end{pagesolutions}
```

### Modifier les dimensions
Dans `configuration.tex` :
- `\largeurcarte` : Largeur des cartes (9cm par défaut)
- `\hauteurcarte` : Hauteur des cartes (13cm par défaut)
- `raster column skip` : Espace horizontal entre cartes
- `raster row skip` : Espace vertical entre cartes

### Changer les couleurs
- `cartebleu` : Couleur du cadre des énoncés
- `cartevert` : Couleur du cadre des solutions

## Notes importantes

- Les environnements `pageenonces` et `pagesolutions` gèrent automatiquement la mise en page
- Le `tcbraster` est contenu dans une `tcolorbox` blanker pour stabilité
- Respecter l'ordre énoncés/solutions pour l'impression recto-verso
- Les équations utilisent `\displaystyle` pour une meilleure lisibilité

## Résolution des problèmes

### Overfull hbox
Les avertissements d'overfull hbox sont normaux et n'affectent pas la qualité du PDF.

### Compilation avec bfcours
Si LuaLaTeX échoue, utilisez la version simplifiée avec pdfLaTeX.
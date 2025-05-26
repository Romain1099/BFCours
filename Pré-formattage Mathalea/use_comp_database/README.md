# Gestionnaire de base de données de compétences Mathalea

Ce module permet d'extraire, stocker et gérer des compétences à partir du fichier HTML de Mathalea. Il fournit une base de données simple pour les opérations CRUD (Create, Read, Update, Delete) sur les compétences.

## Structure du projet

```
use_comp_database/
├── db/                      # Dossier contenant la base de données JSON
├── src/
│   ├── models/              # Modèles de données
│   │   └── competence.js    # Modèle pour les compétences
│   ├── services/            # Services pour la logique métier
│   │   ├── competenceDatabase.js  # Service pour la gestion de la base de données
│   │   └── extractionService.js   # Service pour l'extraction des compétences
│   └── utils/               # Utilitaires
│       └── extractionUtils.js     # Fonctions utilitaires pour l'extraction
├── source.html              # Fichier HTML source contenant les compétences
├── index.js                 # Point d'entrée principal
├── test.js                  # Script de test
├── example.js               # Exemple d'utilisation
└── package.json             # Fichier de configuration npm
```

## Installation

1. Assurez-vous d'avoir Node.js installé sur votre machine
2. Installez les dépendances :

```bash
npm install
```

## Utilisation

### Extraction des compétences

Pour extraire les compétences à partir du fichier HTML source :

```javascript
const CompetenceManager = require('./index');
const manager = new CompetenceManager();

// Extraire les compétences
await manager.extractFromHtml();
```

### Récupération de compétences

```javascript
// Récupérer une compétence par son code
const competence = await manager.getCompetenceByCode('6C10-0', null);

// Récupérer certaines propriétés d'une compétence
const properties = await manager.getCompetenceByCode('6C10-0', ['intitule', 'niveau']);
console.log(properties); // ['Résoudre une Rose additive', '6ème']

// Récupérer toutes les compétences
const allCompetences = await manager.getAllCompetences();

// Rechercher par niveau
const sixiemeCompetences = await manager.getCompetencesByNiveau('6ème');

// Rechercher par mot-clé
const additionCompetences = await manager.searchCompetences('addition');
```

### Modification de compétences

```javascript
// Ajouter une nouvelle compétence
await manager.addCompetence({
  code: '6C10-99',
  intitule: 'Nouvelle compétence',
  enonceLong: 'Description détaillée',
  niveau: '6ème',
  exempleReussite: 'Exemple de réussite'
});

// Mettre à jour une compétence existante
await manager.updateCompetence('6C10-0', {
  enonceLong: 'Nouvelle description',
  exempleReussite: 'Nouvel exemple'
});

// Supprimer une compétence
await manager.deleteCompetence('6C10-99');
```

## Exécution des scripts

```bash
# Exécuter les tests
npm test

# Extraire les compétences
npm run extract

# Exécuter l'exemple
npm run example
```

## Structure des données

Chaque compétence contient les champs suivants :

- `code` : Code unique de la compétence (ex: 6C10-0)
- `intitule` : Intitulé court de la compétence
- `enonceLong` : Énoncé détaillé de la compétence (peut être vide)
- `niveau` : Niveau scolaire concerné (CP, CE1, ..., Tle)
- `exempleReussite` : Exemple de réussite sous forme de code LaTeX ou lien vers image

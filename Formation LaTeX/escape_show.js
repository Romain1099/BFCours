const fs = require('fs');

//TODO : Faire en sorte que le code produit mette un saut de ligne à la fin d'un environnement ou d'une comma ( via \\ ). La raison c'est que ça met une présentation clean. 

//TODO : Régler le probleme des showcmd qui n'affichent pas le contenu quand pas de paramètre. 

// Fonction principale
function processLatexFile(inputFile, outputFile) {
  try {
    // Lire le fichier
    const input = fs.readFileSync(inputFile, 'utf8');
    
    // Traitement du code LaTeX
    const processed = processLatex(input);
    
    // Écrire le résultat
    fs.writeFileSync(outputFile, processed);
    console.log(`Traitement terminé avec succès. Résultat écrit dans ${outputFile}`);
  } catch (error) {
    console.error('Erreur:', error.message);
  }
}

// Fonction pour échapper les caractères spéciaux dans les commandes
function escapeForCmd(text) {
  return text
    .replace(/&/g, '\\&')
    .replace(/\\/g, '$\\backslash$') // Échapper les backslash
    .replace(/\{/g, '\\{')
    .replace(/\}/g, '\\}')
    .replace(/\$/g, '\\$')
    .replace(/%/g, '\\%')
    .replace(/_/g, '\\_')
    .replace(/#/g, '\\#')
    .replace(/~/g, '\\~{}')
    .replace(/\^/g, '\\^{}');
}

// Fonction pour échapper les caractères spéciaux dans les paramètres d'environnement
function escapeForEnv(text) {
  return text
    .replace(/&/g, '\\\\&')
    .replace(/\$/g, '\\$')
    .replace(/\\/g, '$\\backslash$') // Échapper les backslash
    .replace(/\{/g, '\\{')
    .replace(/\}/g, '\\}')
    .replace(/%/g, '\\%')
    .replace(/_/g, '\\_')
    .replace(/#/g, '\\#')
    .replace(/~/g, '\\~{}')
    .replace(/\^/g, '\\^{}');
}

// Traiter le code LaTeX ligne par ligne (approche plus simple)
function processLatex(input) {
  // Diviser en lignes pour un traitement plus simple
  const lines = input.split('\n');
  let output = [];
  let envStack = [];
  
  for (let i = 0; i < lines.length; i++) {
    let line = lines[i];
    
    // Traiter les commandes \begin
    const beginMatch = line.match(/\\begin\{([^{}]+)\}/);
    if (beginMatch) {
      const envName = beginMatch[1];
      envStack.push(envName);
      
      // Extraire les paramètres après \begin{env}
      let params = '';
      let rest = line.substring(line.indexOf('}') + 1).trim();
      
      // Vérifier s'il y a des paramètres entre accolades ou crochets
      let paramMatch = rest.match(/^(\{[^{}]*\}|\[[^\[\]]*\])+/);
      if (paramMatch) {
        params = paramMatch[0];
        // Échapper les paramètres correctement
        params = escapeForEnv(params);
      }
      
      // Remplacer la ligne par \showenv
      line = line.replace(/\\begin\{([^{}]+)\}(\{[^{}]*\}|\[[^\[\]]*\])*/, 
        `\\showenv{${envName}}[${params}][`);
    }
    
    // Traiter les commandes \end
    const endMatch = line.match(/\\end\{([^{}]+)\}/);
    if (endMatch) {
      const envName = endMatch[1];
      
      // Vérifier que c'est la fin de l'environnement en cours
      if (envStack.length > 0 && envStack[envStack.length - 1] === envName) {
        envStack.pop();
        
        // Remplacer la ligne par ]
        line = line.replace(/\\end\{([^{}]+)\}/, ']');
      }
    }
    
    // Traiter les commandes simples (après avoir traité begin/end)
    if (!beginMatch && !endMatch) {
      line = processCommandsInLine(line);
    }
    
    output.push(line);
  }
  
  return output.join('\n');
}

// Traiter les commandes dans une ligne
function processCommandsInLine(line) {
  // Ignorer les commandes déjà traitées
  if (line.includes('\\showenv') || line.includes('\\showcmd') || 
      line.includes('\\showcmdpar') || line.includes('\\NewDocumentCommand') ||
      line.includes('\\NewTotalTCBox') || line.includes('\\cmbox') ||
      line.includes('\\envbox')) {
    return line;
  }
  
  // Remplacer les commandes par \showcmd
  return line.replace(/\\([a-zA-Z]+)(\[[^\]]*\])?(\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\})?/g, 
    (match, cmd, options = '', args = '', argsContent = '') => {
      // Ignorer les commandes spéciales
      if (['begin', 'end'].includes(cmd)) {
        return match;
      }
      
      // Formater les options
      options = options || '';
      
      // Échapper correctement les arguments
      let escapedArgs = '';
      if (args) {
        // Enlever les accolades extérieures
        const argsWithoutBraces = args.substring(1, args.length - 1);
        escapedArgs = escapeForCmd(argsWithoutBraces);
      }
      
      // Utiliser showcmdpar pour les arguments longs, sinon showcmd
      if (args && (argsContent.length > 20 || argsContent.includes('\n'))) {
        return `\\showcmdpar{${cmd}${options}}[${escapedArgs}]`;
      } else if (args) {
        return `\\showcmd{${cmd}${options}}[${escapedArgs}]`;
      } else {
        return `\\showcmd{${cmd}${options}}[]`;
      }
    });
}

// Point d'entrée du programme
if (process.argv.length < 3) {
  console.log('Usage: node latex-processor.js <input-file> [output-file]');
  process.exit(1);
}

const inputFile = process.argv[2];
const outputFile = process.argv.length > 3 ? process.argv[3] : 'output.tex';
processLatexFile(inputFile, outputFile);
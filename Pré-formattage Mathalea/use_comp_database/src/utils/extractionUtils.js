/**
 * Utilitaires pour l'extraction des compétences à partir du fichier HTML
 */

/**
 * Extrait le code de la compétence
 * @param {string} text - Texte contenant le code 
 * @returns {string} - Le code de la compétence extrait
 */
function extractCode(text) {
  // Format attendu: <span class="font-bold">6C10-0 - </span>
  const codeRegex = /<span class="font-bold">([^<]+) - <\/span>/;
  const match = text.match(codeRegex);
  
  if (match && match[1]) {
    return match[1].trim();
  }
  
  return "";
}

/**
 * Extrait l'intitulé de la compétence
 * @param {string} text - Texte contenant l'intitulé
 * @param {string} code - Code de la compétence pour aider à l'extraction
 * @returns {string} - L'intitulé de la compétence extrait
 */
function extractIntitule(text, code) {
  if (!code) return "";
  
  // Format attendu: <span class="font-bold">6C10-0 - </span>Résoudre une Rose additive
  const pattern = new RegExp(`<span class="font-bold">${code.replace(/[-]/g, '\\-')} - <\\/span>([^<]+)`);
  const match = text.match(pattern);
  
  if (match && match[1]) {
    return match[1].trim();
  }
  
  return "";
}

/**
 * Détermine le niveau de la compétence en fonction de son code
 * @param {string} code - Code de la compétence
 * @returns {string} - Niveau scolaire (CP, CE1, ..., Tle)
 */
function determineNiveau(code) {
  // Les codes commencent généralement par le niveau
  // Par exemple: 6C10-0 => 6ème
  const niveauMap = {
    'CP': 'CP',
    'CE1': 'CE1',
    'CE2': 'CE2',
    'CM1': 'CM1',
    'CM2': 'CM2',
    '6': '6ème',
    '5': '5ème',
    '4': '4ème',
    '3': '3ème',
    '2': '2nde',
    '1': '1ère',
    'T': 'Tle'
  };
  
  // Récupération du niveau à partir du premier caractère du code
  const firstChar = code.charAt(0);
  
  if (niveauMap[firstChar]) {
    return niveauMap[firstChar];
  }
  
  // Si le code commence par 2 chiffres (ex: 2nde)
  if (code.startsWith('2n')) {
    return '2nde';
  }
  
  // Si le code commence par 1 suivi d'une lettre (ex: 1S, 1ES, etc.)
  if (code.startsWith('1') && code.length > 1 && isNaN(parseInt(code.charAt(1)))) {
    return '1ère';
  }
  
  // Si le code commence par T (ex: TS, TES, etc.)
  if (code.startsWith('T') && code.length > 1) {
    return 'Tle';
  }
  
  return "";
}

module.exports = {
  extractCode,
  extractIntitule,
  determineNiveau
};

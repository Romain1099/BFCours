/**
 * Script d'extraction des compétences à partir du fichier HTML source
 */

const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');
const Competence = require('../models/competence');
const CompetenceDatabase = require('../services/competenceDatabase');
const { extractCode, extractIntitule, determineNiveau } = require('../utils/extractionUtils');

// Chemins de fichiers
const SOURCE_HTML_PATH = path.resolve(__dirname, '../../source.html');
const DB_PATH = path.resolve(__dirname, '../../db/competences.json');

/**
 * Extrait les compétences du fichier HTML et les ajoute à la base de données
 */
async function extractCompetences() {
  try {
    // Vérifier que le fichier source existe
    if (!fs.existsSync(SOURCE_HTML_PATH)) {
      console.error(`Erreur: Le fichier source ${SOURCE_HTML_PATH} n'existe pas.`);
      return;
    }
    
    // Lire le contenu du fichier HTML
    const htmlContent = fs.readFileSync(SOURCE_HTML_PATH, 'utf8');
    
    // Initialiser la base de données
    const db = new CompetenceDatabase(DB_PATH);
    await db.load();
    
    // Parse le HTML avec JSDOM
    const dom = new JSDOM(htmlContent);
    const document = dom.window.document;
    
    // Sélectionner tous les boutons qui contiennent des compétences
    const competenceButtons = document.querySelectorAll('button[type="button"]');
    
    let competencesCount = 0;
    
    for (const button of competenceButtons) {
      // Récupérer le HTML du bouton
      const buttonHTML = button.innerHTML;
      
      // Vérifier si ce bouton contient une compétence (contient un span avec font-bold)
      if (buttonHTML.includes('<span class="font-bold">') && !buttonHTML.includes('id="titre-liste')) {
        // Extraire le code et l'intitulé
        const code = extractCode(buttonHTML);
        const intitule = extractIntitule(buttonHTML, code);
        
        // Si un code valide a été trouvé
        if (code && intitule) {
          // Déterminer le niveau à partir du code
          const niveau = determineNiveau(code);
          
          // Créer la nouvelle compétence (avec des champs vides pour l'énoncé long et l'exemple de réussite)
          const competence = new Competence(code, intitule, "", niveau, "");
          
          // Ajouter ou mettre à jour la compétence dans la base de données
          await db.addCompetence(competence);
          competencesCount++;
        }
      }
    }
    
    console.log(`Extraction terminée: ${competencesCount} compétences extraites et enregistrées dans la base de données.`);
    
  } catch (error) {
    console.error('Erreur lors de l\'extraction des compétences:', error);
  }
}
/**
 * Affiche les compétences extraites
 */
async function displayCompetences() {
  try {
    const db = new CompetenceDatabase(DB_PATH);
    await db.load();
    
    const competences = await db.getAllCompetences();
    
    if (competences.length === 0) {
      console.log('Aucune compétence n\'a été trouvée dans la base de données.');
      return;
    }
    
    console.log(`Nombre total de compétences: ${competences.length}`);
    console.log('Exemples de compétences:');
    
    // Afficher les 5 premières compétences
    competences.slice(0, 5).forEach(comp => {
      console.log(`- ${comp.code}: ${comp.intitule} (${comp.niveau || 'Niveau non défini'})`);
    });
    
  } catch (error) {
    console.error('Erreur lors de l\'affichage des compétences:', error);
  }
}

/**
 * Récupère une compétence par son code avec les propriétés spécifiées
 * @param {string} code - Code de la compétence
 * @param {Array<string>} itemList - Liste des propriétés à récupérer
 * @returns {Promise<Array<any>|null>} - Tableau des valeurs des propriétés demandées ou null
 */
async function get_comp_by_code(code, itemList) {
  try {
    const db = new CompetenceDatabase(DB_PATH);
    return await db.getCompetenceByCode(code, itemList);
  } catch (error) {
    console.error(`Erreur lors de la récupération de la compétence ${code}:`, error);
    return null;
  }
}

// Exporter les fonctions
module.exports = {
  extractCompetences,
  displayCompetences,
  get_comp_by_code
};

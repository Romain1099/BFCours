/**
 * Script de test pour vérifier le bon fonctionnement de l'extraction
 * et des opérations CRUD sur les compétences
 */

const path = require('path');
const Competence = require('./src/models/competence');
const CompetenceDatabase = require('./src/services/competenceDatabase');
const { extractCompetences, displayCompetences, get_comp_by_code } = require('./src/services/extractionService');

const DB_PATH = path.resolve(__dirname, './db/competences.json');

/**
 * Fonction principale qui exécute les tests
 */
async function runTests() {
  console.log('=== Test de l\'extraction des compétences ===');
  
  // Étape 1: Extraction des compétences
  console.log('\n1. Extraction des compétences à partir du fichier HTML...');
  await extractCompetences();
  
  // Étape 2: Affichage des compétences extraites
  console.log('\n2. Affichage des compétences extraites:');
  await displayCompetences();
  
  // Étape 3: Test de récupération par code
  console.log('\n3. Test de la fonction get_comp_by_code:');
  
  // Test avec un code existant (à adapter selon vos données)
  const testCode = '6C10-0';
  console.log(`\nRécupération de la compétence ${testCode} avec intitulé et niveau:`);
  const result1 = await get_comp_by_code(testCode, ['intitule', 'niveau']);
  console.log('Résultat:', result1);
  
  console.log(`\nRécupération de la compétence ${testCode} avec intitulé uniquement:`);
  const result2 = await get_comp_by_code(testCode, ['intitule']);
  console.log('Résultat:', result2);
  
  // Étape 4: Test des opérations CRUD
  console.log('\n4. Test des opérations CRUD:');
  
  // Initialiser la base de données
  const db = new CompetenceDatabase(DB_PATH);
  await db.load();
  
  // Test de mise à jour
  console.log('\nMise à jour d\'une compétence:');
  const updateResult = await db.updateCompetence(testCode, {
    enonceLong: 'Résoudre une rose additive pour développer les compétences en calcul mental',
    exempleReussite: '\\begin{array}{c|c} 12 & 8 \\\\ \\hline 7 & ? \\end{array}'
  });
  
  console.log('Mise à jour réussie:', updateResult);
  
  // Vérification de la mise à jour
  const updatedComp = await db.getCompetenceByCode(testCode);
  console.log('Compétence mise à jour:', updatedComp);
  
  // Test de recherche par niveau
  console.log('\nRecherche de compétences de niveau 6ème:');
  const sixiemeComps = await db.getCompetencesByNiveau('6ème');
  console.log(`Nombre de compétences trouvées: ${sixiemeComps.length}`);
  
  // Test de recherche par mot-clé
  console.log('\nRecherche de compétences contenant "addition":');
  const additionComps = await db.searchCompetences('addition');
  console.log(`Nombre de compétences trouvées: ${additionComps.length}`);
  
  console.log('\n=== Tous les tests sont terminés ===');
}

// Exécuter les tests
runTests().catch(error => {
  console.error('Erreur lors de l\'exécution des tests:', error);
});

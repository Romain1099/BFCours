/**
 * Exemple d'utilisation du gestionnaire de compétences
 */

const CompetenceManager = require('./index');

/**
 * Fonction de démonstration d'utilisation
 */
async function runExample() {
  // Créer une instance du gestionnaire de compétences
  const manager = new CompetenceManager();
  
  console.log('=== Démonstration du gestionnaire de compétences ===\n');
  
  // 1. Extraire les compétences du fichier HTML
  console.log('1. Extraction des compétences depuis le fichier HTML...');
  await manager.extractFromHtml();
  
  // 2. Récupérer toutes les compétences
  console.log('\n2. Récupération de toutes les compétences...');
  const allCompetences = await manager.getAllCompetences();
  console.log(`Nombre de compétences extraites: ${allCompetences.length}`);
  
  // Afficher les 3 premières
  if (allCompetences.length > 0) {
    console.log('\nExemples de compétences:');
    allCompetences.slice(0, 3).forEach(comp => {
      console.log(`- ${comp.code}: ${comp.intitule} (Niveau: ${comp.niveau || 'Non défini'})`);
    });
  }
  
  // 3. Démonstration de la fonction get_comp_by_code
  console.log('\n3. Démonstration de la fonction get_comp_by_code...');
  
  // Utiliser le code de la première compétence pour la démo
  const demoCode = allCompetences.length > 0 ? allCompetences[0].code : '6C10-0';
  
  console.log(`\nRécupération de l'intitulé et niveau pour la compétence ${demoCode}:`);
  const result = await manager.getCompetenceByCode(demoCode, ['intitule', 'niveau']);
  console.log('Résultat:', result);
  
  // 4. Mise à jour d'une compétence
  console.log('\n4. Mise à jour d\'une compétence...');
  const updateResult = await manager.updateCompetence(demoCode, {
    enonceLong: 'Description plus détaillée de la compétence',
    exempleReussite: 'Exemple de réussite mis à jour'
  });
  
  console.log('Mise à jour réussie:', updateResult);
  
  // Vérifier la mise à jour
  const updatedComp = await manager.getCompetenceByCode(demoCode, null);
  console.log('\nCompétence mise à jour:');
  console.log('- Code:', updatedComp.code);
  console.log('- Intitulé:', updatedComp.intitule);
  console.log('- Niveau:', updatedComp.niveau);
  console.log('- Énoncé long:', updatedComp.enonceLong);
  console.log('- Exemple de réussite:', updatedComp.exempleReussite);
  
  // 5. Recherche par niveau
  console.log('\n5. Recherche de compétences par niveau...');
  const niveauComps = await manager.getCompetencesByNiveau('6ème');
  console.log(`Nombre de compétences de niveau 6ème: ${niveauComps.length}`);
  
  // 6. Recherche par mot-clé
  console.log('\n6. Recherche de compétences par mot-clé...');
  const keywordComps = await manager.searchCompetences('résoudre');
  console.log(`Nombre de compétences contenant "résoudre": ${keywordComps.length}`);
  
  console.log('\n=== Démonstration terminée ===');
}

// Exécuter l'exemple
runExample().catch(error => {
  console.error('Erreur lors de l\'exécution de l\'exemple:', error);
});

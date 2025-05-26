/**
 * Point d'entrée principal pour la gestion des compétences
 * Fournit une interface pour interagir avec la base de données
 */

const path = require('path');
const Competence = require('./src/models/competence');
const CompetenceDatabase = require('./src/services/competenceDatabase');
const { extractCompetences, get_comp_by_code } = require('./src/services/extractionService');

// Chemin vers la base de données
const DB_PATH = path.resolve(__dirname, './db/competences.json');

// Initialiser la base de données
const db = new CompetenceDatabase(DB_PATH);

/**
 * Interface principale pour la gestion des compétences
 */
class CompetenceManager {
  /**
   * Initialise le gestionnaire de compétences
   */
  constructor() {
    this.db = db;
  }

  /**
   * Extrait les compétences du fichier HTML source
   * @returns {Promise<boolean>} - True si l'extraction a réussi, false sinon
   */
  async extractFromHtml() {
    try {
      await extractCompetences();
      return true;
    } catch (error) {
      console.error('Erreur lors de l\'extraction des compétences:', error);
      return false;
    }
  }

  /**
   * Récupère une compétence par son code
   * @param {string} code - Code de la compétence
   * @param {Array<string>} itemList - Liste des propriétés à récupérer
   * @returns {Promise<Array<any>|Competence|null>} - Compétence ou liste des propriétés demandées
   */
  async getCompetenceByCode(code, itemList) {
    return get_comp_by_code(code, itemList);
  }

  /**
   * Ajoute une nouvelle compétence
   * @param {Object} competenceData - Données de la compétence à ajouter
   * @returns {Promise<boolean>} - True si l'ajout a réussi, false sinon
   */
  async addCompetence(competenceData) {
    try {
      await this.db.load();
      
      const { code, intitule, enonceLong, niveau, exempleReussite } = competenceData;
      const competence = new Competence(code, intitule, enonceLong, niveau, exempleReussite);
      
      return await this.db.addCompetence(competence);
    } catch (error) {
      console.error('Erreur lors de l\'ajout de la compétence:', error);
      return false;
    }
  }
  /**
   * Met à jour une compétence existante
   * @param {string} code - Code de la compétence à mettre à jour
   * @param {Object} updates - Données à mettre à jour
   * @returns {Promise<boolean>} - True si la mise à jour a réussi, false sinon
   */
  async updateCompetence(code, updates) {
    try {
      await this.db.load();
      return await this.db.updateCompetence(code, updates);
    } catch (error) {
      console.error('Erreur lors de la mise à jour de la compétence:', error);
      return false;
    }
  }

  /**
   * Supprime une compétence
   * @param {string} code - Code de la compétence à supprimer
   * @returns {Promise<boolean>} - True si la suppression a réussi, false sinon
   */
  async deleteCompetence(code) {
    try {
      await this.db.load();
      return await this.db.deleteCompetence(code);
    } catch (error) {
      console.error('Erreur lors de la suppression de la compétence:', error);
      return false;
    }
  }

  /**
   * Récupère toutes les compétences
   * @returns {Promise<Array<Competence>>} - Tableau de toutes les compétences
   */
  async getAllCompetences() {
    try {
      await this.db.load();
      return await this.db.getAllCompetences();
    } catch (error) {
      console.error('Erreur lors de la récupération des compétences:', error);
      return [];
    }
  }

  /**
   * Recherche des compétences par niveau
   * @param {string} niveau - Niveau scolaire à rechercher
   * @returns {Promise<Array<Competence>>} - Tableau des compétences correspondantes
   */
  async getCompetencesByNiveau(niveau) {
    try {
      await this.db.load();
      return await this.db.getCompetencesByNiveau(niveau);
    } catch (error) {
      console.error('Erreur lors de la recherche par niveau:', error);
      return [];
    }
  }

  /**
   * Recherche des compétences par mot-clé
   * @param {string} keyword - Mot-clé à rechercher
   * @returns {Promise<Array<Competence>>} - Tableau des compétences correspondantes
   */
  async searchCompetences(keyword) {
    try {
      await this.db.load();
      return await this.db.searchCompetences(keyword);
    } catch (error) {
      console.error('Erreur lors de la recherche par mot-clé:', error);
      return [];
    }
  }
}

// Exporter l'interface
module.exports = CompetenceManager;

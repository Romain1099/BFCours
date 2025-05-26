/**
 * Service de base de données pour la gestion des compétences
 * Gère la persistance et les opérations CRUD sur les compétences
 */

const fs = require('fs');
const path = require('path');
const Competence = require('../models/competence');

class CompetenceDatabase {
  /**
   * Crée une instance de la base de données de compétences
   * @param {string} dbPath - Chemin vers le fichier de base de données
   */
  constructor(dbPath) {
    this.dbPath = dbPath;
    this.competences = [];
    this.loaded = false;
  }

  /**
   * Charge les données depuis le fichier de base de données
   * @returns {Promise<boolean>} - True si le chargement a réussi, false sinon
   */
  async load() {
    try {
      // Vérifier si le fichier existe
      if (fs.existsSync(this.dbPath)) {
        const data = fs.readFileSync(this.dbPath, 'utf8');
        const jsonData = JSON.parse(data);
        
        this.competences = jsonData.map(json => Competence.fromJSON(json));
        this.loaded = true;
        return true;
      } else {
        // Initialiser avec un tableau vide si le fichier n'existe pas
        this.competences = [];
        this.loaded = true;
        return false;
      }
    } catch (error) {
      console.error('Erreur lors du chargement de la base de données:', error);
      return false;
    }
  }
  /**
   * Sauvegarde les données dans le fichier de base de données
   * @returns {Promise<boolean>} - True si la sauvegarde a réussi, false sinon
   */
  async save() {
    try {
      const data = JSON.stringify(this.competences.map(comp => comp.toJSON()), null, 2);
      
      // Créer le répertoire s'il n'existe pas
      const dirname = path.dirname(this.dbPath);
      if (!fs.existsSync(dirname)) {
        fs.mkdirSync(dirname, { recursive: true });
      }
      
      fs.writeFileSync(this.dbPath, data, 'utf8');
      return true;
    } catch (error) {
      console.error('Erreur lors de la sauvegarde de la base de données:', error);
      return false;
    }
  }

  /**
   * Ajoute une compétence à la base de données
   * @param {Competence} competence - La compétence à ajouter
   * @returns {Promise<boolean>} - True si l'ajout a réussi, false sinon
   */
  async addCompetence(competence) {
    if (!this.loaded) await this.load();
    
    // Vérifier si la compétence existe déjà
    const existingIndex = this.competences.findIndex(c => c.code === competence.code);
    
    if (existingIndex !== -1) {
      // Mettre à jour la compétence existante
      this.competences[existingIndex] = competence;
    } else {
      // Ajouter la nouvelle compétence
      this.competences.push(competence);
    }
    
    return this.save();
  }
  /**
   * Récupère une compétence par son code
   * @param {string} code - Le code de la compétence à rechercher
   * @param {Array<string>} [itemList] - Liste des propriétés à retourner (facultatif)
   * @returns {Promise<Competence|Array<any>|null>} - La compétence trouvée, la liste des propriétés demandées, ou null si non trouvée
   */
  async getCompetenceByCode(code, itemList = null) {
    if (!this.loaded) await this.load();
    
    const competence = this.competences.find(c => c.code === code);
    
    if (!competence) return null;
    
    // Si une liste de propriétés est demandée, retourner uniquement ces propriétés
    if (Array.isArray(itemList) && itemList.length > 0) {
      return itemList.map(item => competence[item]);
    }
    
    return competence;
  }

  /**
   * Récupère toutes les compétences
   * @returns {Promise<Array<Competence>>} - Tableau de toutes les compétences
   */
  async getAllCompetences() {
    if (!this.loaded) await this.load();
    return this.competences;
  }

  /**
   * Supprime une compétence par son code
   * @param {string} code - Le code de la compétence à supprimer
   * @returns {Promise<boolean>} - True si la suppression a réussi, false sinon
   */
  async deleteCompetence(code) {
    if (!this.loaded) await this.load();
    
    const initialLength = this.competences.length;
    this.competences = this.competences.filter(c => c.code !== code);
    
    // Vérifier si une compétence a été supprimée
    if (this.competences.length < initialLength) {
      return this.save();
    }
    
    return false;
  }
  /**
   * Met à jour une compétence existante
   * @param {string} code - Le code de la compétence à mettre à jour
   * @param {Object} updates - Les champs à mettre à jour
   * @returns {Promise<boolean>} - True si la mise à jour a réussi, false sinon
   */
  async updateCompetence(code, updates) {
    if (!this.loaded) await this.load();
    
    const competenceIndex = this.competences.findIndex(c => c.code === code);
    
    if (competenceIndex === -1) return false;
    
    // Mettre à jour uniquement les champs fournis
    Object.keys(updates).forEach(key => {
      if (key !== 'code' && key in this.competences[competenceIndex]) {
        this.competences[competenceIndex][key] = updates[key];
      }
    });
    
    return this.save();
  }

  /**
   * Recherche des compétences par niveau
   * @param {string} niveau - Le niveau scolaire à rechercher
   * @returns {Promise<Array<Competence>>} - Tableau des compétences du niveau demandé
   */
  async getCompetencesByNiveau(niveau) {
    if (!this.loaded) await this.load();
    
    return this.competences.filter(c => c.niveau === niveau);
  }

  /**
   * Recherche des compétences par mot-clé dans l'intitulé
   * @param {string} keyword - Le mot-clé à rechercher
   * @returns {Promise<Array<Competence>>} - Tableau des compétences correspondantes
   */
  async searchCompetences(keyword) {
    if (!this.loaded) await this.load();
    
    const lowerKeyword = keyword.toLowerCase();
    
    return this.competences.filter(c => 
      c.intitule.toLowerCase().includes(lowerKeyword) || 
      c.enonceLong.toLowerCase().includes(lowerKeyword)
    );
  }
}

module.exports = CompetenceDatabase;

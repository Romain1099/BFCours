/**
 * Modèle de données pour les compétences
 * Représente la structure d'une compétence avec tous ses attributs
 */

class Competence {
  /**
   * Crée une nouvelle instance de Competence
   * @param {string} code - Code unique de la compétence (ex: 6C10-0)
   * @param {string} intitule - Intitulé court de la compétence
   * @param {string} enonceLong - Énoncé détaillé de la compétence (peut être vide)
   * @param {string} niveau - Niveau scolaire concerné (CP, CE1, ..., Tle)
   * @param {string} exempleReussite - Exemple de réussite sous forme de code LaTeX ou lien vers image
   */
  constructor(code, intitule, enonceLong = "", niveau = "", exempleReussite = "") {
    this.code = code;
    this.intitule = intitule;
    this.enonceLong = enonceLong;
    this.niveau = niveau;
    this.exempleReussite = exempleReussite;
  }

  /**
   * Convertit l'objet Competence en format JSON
   * @returns {Object} Représentation JSON de la compétence
   */
  toJSON() {
    return {
      code: this.code,
      intitule: this.intitule,
      enonceLong: this.enonceLong,
      niveau: this.niveau,
      exempleReussite: this.exempleReussite
    };
  }

  /**
   * Crée une instance de Competence à partir d'un objet JSON
   * @param {Object} json - Objet JSON représentant une compétence
   * @returns {Competence} Instance de Competence
   */
  static fromJSON(json) {
    return new Competence(
      json.code,
      json.intitule,
      json.enonceLong,
      json.niveau,
      json.exempleReussite
    );
  }
}

module.exports = Competence;

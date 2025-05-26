import json
import os

def get_comp_by_code(code, item_list=None):
    """
    Récupère une compétence par son code directement à partir du fichier JSON
    
    Args:
        code (str): Le code de la compétence à récupérer
        item_list (list, optional): Liste des propriétés à récupérer. Par défaut ['intitule']
    
    Returns:
        Union[list, str, None]: Liste des valeurs des propriétés demandées, 
                               l'intitulé de la compétence si item_list est None,
                               ou None si la compétence n'est pas trouvée
    """
    # Valeur par défaut pour item_list si non spécifié
    if item_list is None:
        item_list = ['intitule']
    
    # Chemin vers le fichier JSON des compétences (dans le même répertoire que l'exécutable)
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'competences.json')
    
    try:
        # Charger les données depuis le fichier JSON
        with open(json_path, 'r', encoding='utf-8') as f:
            competences = json.load(f)
        
        # Rechercher la compétence avec le code spécifié
        competence = None
        for comp in competences:
            if comp.get('code') == code:
                competence = comp
                break
        
        if not competence:
            return None
        
        # Si une liste de propriétés est demandée, retourner uniquement ces propriétés
        if isinstance(item_list, list) and item_list:
            result = [competence.get(item, '') for item in item_list]
            # Si un seul élément est demandé, renvoyer directement la valeur
            if len(item_list) == 1:
                return result[0]
            return result
        
        # Si aucune propriété spécifique n'est demandée, retourner la compétence complète
        return competence
        
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier de compétences: {e}")
        return None

# Exemple d'utilisation:
if __name__ == "__main__":
    # Récupérer l'intitulé d'une compétence
    intitule = get_comp_by_code("6C10-0")
    print(f"Intitulé: {intitule}")
    
    # Récupérer plusieurs propriétés
    properties = get_comp_by_code("6C10-0", ["intitule", "niveau"])
    print(f"Propriétés: {properties}")
import mysql.connector
import json

def get_db_config():
    # Configuration de la connexion à la base de données
    return {
        'host': 'localhost',
        'user': 'admin',
        'password': 'motdepasse',  # Remplacez par votre mot de passe
        'database': 'coursdb'
    }

def get_data_as_json(query):
    db_config=get_db_config()

    # Connexion à la base de données
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Exécuter la requête
    cursor.execute(query)

    # Récupérer les noms des colonnes
    columns = [desc[0] for desc in cursor.description]

    # Récupérer les résultats (liste de tuples)
    result = cursor.fetchall()

    # Convertir les résultats en une liste de dictionnaires
    result_as_dict = [dict(zip(columns, row)) for row in result]

    # Fermer la connexion
    cursor.close()
    conn.close()

    # Convertir le résultat en JSON
    return json.dumps(result_as_dict, indent=4)


def get_student_by_substring(substring,wanted_attributes='*',all_datas=False):
    size = len(substring)
    # Exemple d'utilisation de la fonction
    query = f"""SELECT {wanted_attributes} FROM eleve
    WHERE SUBSTRING(eleve.nom, 1, {size}) = '{substring}';"""
    json_data = get_data_as_json(query)
    json_data = json.loads(json_data)
    number_of_students_found = len(json_data)
    if number_of_students_found==1:
        return json_data[0]
    elif number_of_students_found == 0:
        print(f"Aucun étudiant trouvé pour la requete {substring} dans le NOM...\nRecherches pour la clé PRENOM...")
        query = f"""SELECT {wanted_attributes} FROM eleve
        WHERE SUBSTRING(eleve.prenom, 1, {size}) = '{substring}';"""
        json_data = get_data_as_json(query)
        json_data = json.loads(json_data)
        number_of_students_found = len(json_data)
        if number_of_students_found==1:
            return json_data[0]
        else:
            raise FileNotFoundError(f"Aucun étudiant trouvé pour la requete {substring}")
    else:
        noms=[]
        for eleve in json_data:
            noms.append(f"nom : {eleve['nom']}\nid : {eleve['idEleve']};\n")
        many_users_message = '\n'.join(noms)
        print(f"Plusieurs options ont été trouvées : \n{many_users_message}\nPar défaut seule la première entrée trouvée est retournée, paramétrer 'all_datas' à True pour obtenir toute la liste.")
        if all_datas==True:
            return json_data
        else:
            return json_data[0]


if __name__=="__main__" :
    print(get_student_by_substring('gDoth',wanted_attributes='nom, prenom, numtel'))
# globasoft-countries

Application web développée dans le cadre du test technique Globasoft.
Elle permet d'importer, de stocker et d'analyser les données des pays via l'API publique RestCountries.


##  Fonctionnalités Clés

* **Importation Robuste** : Script de commande personnalisé avec gestion des erreurs et **Retry automatique** (3 tentatives) pour l'API RestCountries.
* **Consultation** : Liste des pays avec pagination, **recherche textuelle** et **filtres par région**.
* **Visualisation** : Tableau de bord (/stats) avec **graphiques interactifs (Chart.js)** pour la population, la superficie et la répartition géographique.
* **Architecture** : Base de données SQLite locale pour la performance (pas d'appels API en temps réel lors de la navigation).
* **Design** : Interface moderne et responsive réalisée avec **Bootstrap 5**.

---

##  Installation & Démarrage

Vous avez deux méthodes pour lancer le projet.

### Méthode 1 : Via Docker (Recommandée) 
L'environnement est entièrement conteneurisé. Prérequis : Docker Desktop installé.

1.  **Lancer le conteneur** :
    ```bash
    docker-compose up --build
    ```
2.  **Initialiser la base de données** (dans un autre terminal) :
    ```bash
    docker-compose exec web python manage.py migrate
    ```
3.  **Lancer l'importation des données** :
    ```bash
    docker-compose exec web python manage.py import_countries
    ```
4.  **Accéder au site** : [http://127.0.0.1:8000/countries/](http://127.0.0.1:8000/countries/)

---

### Méthode 2 : Installation Locale (Sans Docker) 
Prérequis : Python 3.10+ installé.

1.  **Cloner le projet et créer l'environnement virtuel** :
    ```bash
    git clone [https://github.com/amarimanel/globasoft-countries.git](https://github.com/amarimanel/globasoft-countries.git)
    cd globasoft-countries
    python -m venv venv
    
    # Activation (Windows)
    venv\Scripts\activate
    # Activation (Mac/Linux)
    source venv/bin/activate
    ```

2.  **Installer les dépendances** :
    ```bash
    pip install -r requirements.txt
    ```

3.  **Préparer la base de données** :
    ```bash
    python manage.py migrate
    ```

4.  **Importer les pays** :
    ```bash
    python manage.py import_countries
    ```

5.  **Lancer le serveur** :
    ```bash
    python manage.py runserver
    ```

---

## 🔗 URLs et Navigation

Une fois le serveur lancé, voici les accès :

| Page | URL | Description |
| :--- | :--- | :--- |
| **Accueil / Liste** | `/countries/` | Liste paginée, recherche et filtres. |
| **Statistiques** | `/countries/stats/` | Dashboard avec graphiques Chart.js. |
| **Détail Pays** | `/countries/FRA/` | Exemple pour la France (utilise le code CCA3). |
| **Administration** | `/admin/` | Interface d'administration Django. |

---

##  Qualité du Code (Tests)

Le projet inclut des tests unitaires pour valider les modèles et les vues.
Pour les lancer :

**Via Docker :**
```bash
docker-compose exec web python manage.py test


**En local :**

Bash

python manage.py test

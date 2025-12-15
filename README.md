# 🎬 MovieLens Dashboard

Un tableau de bord interactif pour explorer et analyser le dataset MovieLens avec un système de recommandation de films basé sur la similarité cosine.


## 📋 Table des matières

- [Aperçu](#aperçu)
- [Fonctionnalités](#fonctionnalités)
- [Technologies utilisées](#technologies-utilisées)
- [Installation](#installation)
- [Structure du projet](#structure-du-projet)
- [Utilisation](#utilisation)
- [Algorithme de recommandation](#algorithme-de-recommandation)
- [Auteur](#auteur)

## 🎯 Aperçu

Ce projet est une application web Flask qui permet d'explorer le dataset MovieLens de manière interactive. Il offre des visualisations, des statistiques et un système de recommandation de films personnalisé.

## ✨ Fonctionnalités

### 🏆 Top Films
- **Top 10 par note moyenne** : Films les mieux notés (minimum 50 votes)
- **Top 10 par popularité** : Films les plus notés par les utilisateurs

### 🎭 Analyse par Genre
- Exploration des films par catégorie
- Statistiques détaillées par genre :
  - Nombre de films
  - Note moyenne
  - Nombre total de notes

### 🎯 Système de Recommandation
- Recommandations personnalisées basées sur la **similarité cosine**
- Top 5 des films similaires pour chaque film
- Scores de similarité affichés visuellement
- Interface intuitive avec sélection de films

### 📊 Analyse Exploratoire (EDA)
- Statistiques générales du dataset
- Top 10 des genres les plus représentés
- Top 10 des films les mieux notés

## 🛠 Technologies utilisées

### Backend
- **Python 3.8+**
- **Flask** : Framework web
- **Pandas** : Manipulation et analyse de données
- **NumPy** : Calculs numériques
- **Scikit-learn** : Calcul de similarité cosine

### Frontend
- **HTML5** : Structure
- **CSS3** : Styles et animations
- **Jinja2** : Templates (moteur de template Flask)

## 📦 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner le repository**
```bash
git clone https://github.com/votre-username/movielens-dashboard.git
cd movielens-dashboard
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv

# Sur Windows
venv\Scripts\activate

# Sur macOS/Linux
source venv/bin/activate
```



3. **Préparer les données**
- Placez vos fichiers CSV dans le dossier `data/` :
  - `movies.csv`
  - `ratings.csv`
- Format attendu pour `movies.csv` : `movieId;title;genres`
- Format attendu pour `ratings.csv` : `userId;movieId;rating;timestamp`

4. **Lancer l'application**
```bash
python app.py
```

5. **Accéder à l'application**
- Ouvrez votre navigateur à l'adresse : `http://localhost:5000`

## 📁 Structure du projet

```
movielens-dashboard/
│
├── app.py                  # Application Flask principale
├
├── README.md              # Documentation
│
├── data/                  # Dossier des données
│   ├── movies.csv        # Dataset des films
│   └── ratings.csv       # Dataset des notes
│
├── static/               # Fichiers statiques
│   └── style.css        # Feuille de styles CSS
│
└── templates/           # Templates HTML
    ├── base.html       # Template de base
    ├── top.html        # Page Top Films
    ├── genre.html      # Page Analyse par Genre
    ├── reco.html       # Page Recommandations
    └── eda.html        # Page EDA
```

## 🚀 Utilisation

### Page d'accueil
Point d'entrée avec présentation des fonctionnalités et navigation rapide.

### Top Films
```
/top
```
Consultez les films les mieux notés et les plus populaires.

### Analyse par Genre
```
/genre
```
1. Sélectionnez un genre dans la liste déroulante
2. Cliquez sur "Analyser ce genre"
3. Consultez les statistiques détaillées

### Recommandations
```
/reco
```
1. Choisissez un film dans la liste
2. Cliquez sur "Obtenir des Recommandations"
3. Découvrez 5 films similaires avec leurs scores

### EDA (Analyse Exploratoire)
```
/eda
```
Visualisez les statistiques globales du dataset.

## 🧮 Algorithme de recommandation

### Similarité Cosine

Le système utilise la **similarité cosine** pour recommander des films. Cette méthode calcule l'angle entre deux vecteurs de notation.

#### Fonctionnement
1. **Création de la matrice utilisateur-film** : Chaque ligne représente un utilisateur, chaque colonne un film
2. **Calcul de similarité** : Pour chaque paire de films, on calcule :

```
sim(A,B) = (A · B) / (||A|| × ||B||)
```

Où :
- `A · B` = produit scalaire des vecteurs
- `||A||` = norme du vecteur A
- `||B||` = norme du vecteur B

3. **Recommandations** : Les 5 films avec les scores de similarité les plus élevés sont recommandés

#### Avantages
- ✅ Robuste aux données éparses
- ✅ Rapide et efficace
- ✅ Scores toujours positifs (entre 0 et 1)
- ✅ Standard de l'industrie
- ✅ Ne nécessite pas de normalisation préalable

#### Interprétation des scores
- **0.8 - 1.0** : Très forte similarité
- **0.6 - 0.8** : Forte similarité
- **0.4 - 0.6** : Similarité modérée
- **0.0 - 0.4** : Faible similarité

## 📝 Format des données

### movies.csv
```
movieId;title;genres
1;Toy Story (1995);Adventure|Animation|Children|Comedy|Fantasy
2;Jumanji (1995);Adventure|Children|Fantasy
```

### ratings.csv
```
userId;movieId;rating;timestamp
1;1;4.0;964982703
1;3;4.0;964981247
```

## 🔧 Configuration

### Modifier le port
Dans `app.py`, ligne finale :
```python
app.run(debug=True, port=5000)  # Changez 5000 par le port souhaité
```

### Ajuster le seuil de votes minimum
Dans `app.py`, route `/top` :
```python
top_rating = top_rating_df[top_rating_df['num_ratings'] >= 50]  # Modifier 50
```

## 🐛 Dépannage

### Erreur : "File not found"
Vérifiez que les fichiers CSV sont dans le dossier `data/` avec les bons noms.

### Erreur : Module non trouvé
Réinstallez les dépendances :
```bash
pip install -r requirements.txt
```

### Le serveur ne démarre pas
Vérifiez qu'aucun autre service n'utilise le port 5000 :
```bash
# Windows
netstat -ano | findstr :5000

# macOS/Linux
lsof -i :5000
```

## 📈 Améliorations futures

- [ ] Ajouter un système de filtrage avancé
- [ ] Implémenter des graphiques interactifs (Plotly)
- [ ] Ajouter la possibilité de noter des films
- [ ] Créer un système de profils utilisateurs
- [ ] Intégrer des posters de films via API
- [ ] Ajouter des tests unitaires
- [ ] Optimiser les performances avec cache

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche (`git checkout -b feature/amelioration`)
3. Commit vos changements (`git commit -m 'Ajout nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/amelioration`)
5. Ouvrir une Pull Request



## 👤 Auteurs

**Noura Seddouki**  **Douae Haddad**
- GitHub: [NouraS57](https://github.com/NouraS57)
- Email: nouraseddouki77@gmail.com
- GitHub: [douae123456](https://github.com/douae123456)
- Email: douaehaddad06@gmail.com

## 🙏 Remerciements

- Dataset MovieLens fourni par [GroupLens Research](https://grouplens.org/datasets/movielens/)
- Flask et la communauté Python
- Tous les contributeurs du projet


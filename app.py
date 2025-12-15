from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from types import SimpleNamespace

app = Flask(__name__)

# Chemins vers les datasets
MOVIES_PATH = 'data/movies.csv'
RATINGS_PATH = 'data/ratings.csv'

#Chargement des données 
def load_data():
    movies = pd.read_csv(MOVIES_PATH, sep=';', engine='python', encoding='utf-8')
    ratings = pd.read_csv(RATINGS_PATH, sep=';', engine='python', encoding='utf-8')

    ratings['rating'] = pd.to_numeric(ratings['rating'], errors='coerce')
    ratings = ratings.dropna(subset=['rating'])
    merged = pd.merge(ratings, movies, on='movieId')
    movies['genres_list'] = movies['genres'].str.split('|')

    # Matrice user-movie
    user_movie_matrix = merged.pivot_table(index='userId', columns='title', values='rating').fillna(0)

    # Similarité Cosine 
    cosine_sim = cosine_similarity(user_movie_matrix.T)
    cosine_df = pd.DataFrame(cosine_sim, index=user_movie_matrix.columns, columns=user_movie_matrix.columns)

    print(f"✅ Données chargées: {len(movies)} films, {len(ratings)} ratings")
    print(f"✅ Matrice Cosine: valeurs > 0.1 = {(cosine_df > 0.1).sum().sum()}")

    return {
        'movies': movies,
        'ratings': ratings,
        'merged': merged,
        'user_movie_matrix': user_movie_matrix,
        'similarity_cosine': cosine_df
    }

app_data = load_data()

#Routes 
@app.route('/')
def home():
    return render_template('base.html', page='home')

@app.route('/top')
def top():
    merged = app_data['merged']

    # Top par note moyenne
    top_rating_df = merged.groupby('title')['rating'].agg(['mean', 'count']).reset_index()
    top_rating_df.rename(columns={'mean': 'avg_rating', 'count': 'num_ratings'}, inplace=True)
    top_rating = top_rating_df[top_rating_df['num_ratings'] >= 50].sort_values('avg_rating', ascending=False).head(10)

    # Top par popularité
    top_popularity_df = merged.groupby('title')['rating'].agg(['mean', 'count']).reset_index()
    top_popularity_df.rename(columns={'mean': 'avg_rating', 'count': 'num_ratings'}, inplace=True)
    top_popularity = top_popularity_df.sort_values('num_ratings', ascending=False).head(10)

    return render_template('top.html',
                           top_rating=top_rating.to_dict('records'),
                           top_popularity=top_popularity.to_dict('records'))

@app.route('/genre', methods=['GET', 'POST'])
def genre():
    genres = sorted(app_data['movies'].explode('genres_list')['genres_list'].dropna().unique())
    selected_genre = None
    genre_info = None

    if request.method == 'POST':
        selected_genre = request.form.get('genre')
        movies_exploded = app_data['movies'].explode('genres_list')
        genre_data = pd.merge(app_data['ratings'], movies_exploded, on='movieId')
        genre_data = genre_data[genre_data['genres_list'] == selected_genre]

        if not genre_data.empty:
            nb_movies = genre_data['title'].nunique()
            avg_rating = genre_data['rating'].mean()
            num_ratings = genre_data['rating'].count()

            genre_info = SimpleNamespace(
                num_movies=nb_movies,
                avg_rating=round(avg_rating, 2),
                num_ratings=num_ratings,
                films=genre_data[['title', 'rating']].drop_duplicates().to_dict('records')
            )

    return render_template('genre.html',
                           genres=genres,
                           selected_genre=selected_genre,
                           genre_info=genre_info)

@app.route('/reco', methods=['GET', 'POST'])
def reco():
    movies_list = sorted(app_data['merged']['title'].unique())
    selected_movie = None
    recommendations = None
    error = None

    if request.method == 'POST':
        selected_movie = request.form.get('movie')

        try:
            sim_matrix = app_data['similarity_cosine']
            similar_scores = sim_matrix[selected_movie].sort_values(ascending=False)
            
            recommendations = [
                {'title': title, 'score': f"{score:.3f}"}
                for title, score in similar_scores.iloc[1:6].items()
            ]
            
        except KeyError:
            error = f"Film '{selected_movie}' non trouvé."

    return render_template('reco.html',
                           movies=movies_list,
                           selected_movie=selected_movie,
                           recommendations=recommendations,
                           error=error)

@app.route('/eda')
def eda():
    movies = app_data['movies']
    ratings = app_data['ratings']
    merged = app_data['merged']

    stats = {
        'num_movies': movies.shape[0],
        'num_ratings': ratings.shape[0],
        'num_users': ratings['userId'].nunique()
    }

    genres_list = movies.explode('genres_list')
    top_genres = genres_list['genres_list'].value_counts().head(10).to_dict()

    top_movies = merged.groupby('title')['rating'].mean().sort_values(ascending=False).head(10).to_dict()

    return render_template('eda.html',
                           stats=stats,
                           top_genres=top_genres,
                           top_movies=top_movies)

#Lancement 
if __name__ == '__main__':
    app.run(debug=True, port=5000)
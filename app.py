from flask import Flask, render_template, request
import difflib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load the movies data
movies = pd.read_csv('movies.csv')

# Preprocess the data
selected_features = ['genres', 'keywords', 'tagline', 'cast', 'director']
for feature in selected_features:
    movies[feature] = movies[feature].fillna('')
combined_features = movies['genres'] + ' ' + movies['keywords'] + ' ' + movies['tagline'] + ' ' + movies['cast'] + ' ' + movies['director']

# Convert text data to feature vectors
vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(combined_features)

# Calculate similarity scores
similarity = cosine_similarity(feature_vectors)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def recommend():
    movie_name = request.form['movie_name']
    
    # Find close match for the provided movie name
    list_of_all_titles = movies['title'].tolist()
    find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)

    if not find_close_match:
        # Handle the case when no close match is found
        error_message = "No close match found for the provided movie name."
        return render_template('index.html', error_message=error_message)
    close_match = find_close_match[0]
    index_of_the_movie = movies[movies['title'] == close_match]['index'].values[0]

    # Calculate similarity scores for the selected movie
    similarity_score = list(enumerate(similarity[index_of_the_movie]))
    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

    # Get the top recommended movies
    recommended_movies = []
    i = 1
    for movie in sorted_similar_movies:
        index = movie[0]
        title_from_index = movies.loc[index, 'title']
        if i < 11:
            recommended_movies.append(f"{i}. {title_from_index}")
            i += 1
        else:
            break

    # Pass the recommended movies to the HTML template
    return render_template('index.html', movies=recommended_movies)

if __name__ == '__main__':
    app.run(debug=True)

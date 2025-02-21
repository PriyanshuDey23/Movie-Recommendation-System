import pickle
import streamlit as st
import numpy as np
import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MOVIE_API_KEY = os.getenv("MOVIE_API_KEY") # https://developer.themoviedb.org/reference/intro/authentication

# Ensure the API key is loaded
if not MOVIE_API_KEY:
    st.error("Error: MOVIE_API_KEY is missing! Check your .env file.")
    st.stop()

# Streamlit UI setup
st.header("Movie Recommender System")

# Load the movie data and similarity scores
movies = pickle.load(open('artifacts\\movie_list\\movie_list.pkl', 'rb'))
similarity = pickle.load(open('artifacts\\similarity_score\\similarity_score.pkl', 'rb'))

# Function to fetch movie poster using TMDb v4 Authentication
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US" 
    
    headers = {
        "Authorization": f"Bearer {MOVIE_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)

        data = response.json()

        if 'poster_path' in data and data['poster_path']:
            return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster+Available"

    except requests.exceptions.RequestException as err:
        st.error(f"API request error: {err}")
        return "https://via.placeholder.com/500x750?text=Error+Fetching+Poster"

# Function to get movie recommendations
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
    except IndexError:
        st.error("Movie not found in database.")
        return [], []

    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:  # Get top 5 recommendations
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Dropdown for movie selection
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# Button to show recommendations
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    if recommended_movie_names:
        cols = st.columns(5)
        for i, col in enumerate(cols):
            with col:
                st.text(recommended_movie_names[i])
                st.image(recommended_movie_posters[i])

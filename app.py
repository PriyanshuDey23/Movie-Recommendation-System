import pickle
import  streamlit as st
import numpy as np
import requests

# Launch my webpage in my local host
st.header("Movie Recommender System")


# Load the artifacts
movies = pickle.load(open('artifacts\\movie_list\\movie_list.pkl','rb'))
similarity = pickle.load(open('artifacts\\similarity_score\\similarity_score.pkl','rb'))

# Fetch Poster(If I pass the movie id , It will give me the poster)
def fetch_poster(movie_id):
    # API key and base URLs
    api_key="https://developer.themoviedb.org/reference/intro/authentication"
    base_url = "https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US"
    
    
    # Construct the URL for the movie
    url = base_url.format(movie_id,)
    
    try:
        # Make the request to fetch the movie data
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)

        # Parse the JSON response
        data = response.json()

        # Check if poster_path exists
        if 'poster_path' in data:
            poster_path = data['poster_path']
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        else:
            print("Poster path not found.")
            return None

    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return None


# Recommend Function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id # Selecting the 5 movie id
        recommended_movie_posters.append(fetch_poster(movie_id)) # Fetch the poster through movie index 
        recommended_movie_names.append(movies.iloc[i[0]].title)  # Add the title

    return recommended_movie_names,recommended_movie_posters




# Create selecting box  in which all the book name will be present
movie_list=movies['title'].values
selected_movie=st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0]) # Headline 
        st.image(recommended_movie_posters[0])  # Url
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])


import streamlit as st
import pickle
import requests
import tmdbsimple as tmdb
from dotenv import load_dotenv
import os

load_dotenv("api_key.env")  

tmdb.API_KEY = os.getenv("TMDB_API_KEY")

with open('movie_data.pkl', 'rb') as f:
    movies, cosine_sim = pickle.load(f)

def get_recommendations(title,cosine_sim=cosine_sim):
    idx = movies[movies["title"].str.lower()==title.lower()].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key= lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [x[0] for x in sim_scores]
    return movies[['movie_id','title']].iloc[movie_indices]

def fetch_poster(movie_id):
    poster_path = tmdb.Movies(movie_id).info()['poster_path']
    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
    return poster_url


st.title("🍿 Flick Finder AI 🔍")

selected_movie = st.selectbox("Select a Movie",movies['title'])

if st.button('Find'):
    recommendations = get_recommendations(selected_movie)
    st.write("Top 10 recommended movies:")

    for i in range(0, 10, 5):  
        cols = st.columns(5)  
        for col, j in zip(cols, range(i, i+5)):
            if j < len(recommendations):
                movie_title = recommendations.iloc[j]['title']
                movie_id = recommendations.iloc[j]['movie_id']
                poster_url = fetch_poster(movie_id)
                with col:
                    st.image(poster_url, width=130)
                    st.write(movie_title)

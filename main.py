import streamlit as st
import pickle
import pandas as pd
import requests
import time

def fetch_poster(movie_id):
    try:
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=84e76a926e4a5f095b99da6d6c84ef41&language=en-US')
        response.raise_for_status() # Raises an error for bad status codes
        data = response.json()

        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            # Return a placeholder if the movie has no poster
            return "https://via.placeholder.com/500x750.png?text=No+Poster+Available"

    except requests.exceptions.RequestException as e:
        # Return a different placeholder if the API request fails
        print(f"API request failed: {e}")
        return "https://via.placeholder.com/500x750.png?text=Could+Not+Load"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances=similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies=[]
    recommended_movies_posters=[]
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
        time.sleep(0.05)
    return recommended_movies,recommended_movies_posters

movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))



st.title('Movies Recommender System')

selected_movie_name = st.selectbox('How would you be like to contacted?',
                      movies['title'].values)

if st.button('Recommend'):
    names,poster=recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(poster[0])
    with col2:
        st.text(names[1])
        st.image(poster[1])
    with col3:
        st.text(names[2])
        st.image(poster[2])
    with col4:
        st.text(names[3])
        st.image(poster[3])
    with col5:
        st.text(names[4])
        st.image(poster[4])

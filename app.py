import pickle
import streamlit as st
import requests

# Function to fetch poster using TMDB API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    return ""

# Recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# Streamlit page configuration
st.set_page_config(page_title='Movie Recommender System', layout='wide')

# Style adjustments for new look with background colors
st.markdown(
    """
    <style>
    body {
        background-color: #1f2f3f;
        color: #ececec;
        font-family: 'Helvetica', sans-serif;
    }
    .stButton>button {
        background-color: #4ca1af;
        color: #ffffff;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #3498db;
    }
    .stTextInput>div>div>input {
        color: #333;
        font-weight: bold;
    }
    .header-container {
        background-color: #35495e;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: #ffffff;
    }
    .movie-container {
        background-color: #2e3c4f;
        padding: 15px;
        border-radius: 10px;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# App Header with background styling
st.markdown("<div class='header-container'><h1>🎬 Movie Recommender System</h1><h3>Get personalized movie recommendations</h3></div>", unsafe_allow_html=True)

# Load movies and similarity data
movies = pickle.load(open(r'D:\Downloads\movie-recommender-system-tmdb-dataset-main\movie-recommender-system\movie_list.pkl', 'rb'))
similarity = pickle.load(open(r'D:\Downloads\movie-recommender-system-tmdb-dataset-main\movie-recommender-system\similarity.pkl', 'rb'))

# Movie selection with background styling
st.markdown("<div class='movie-container'>", unsafe_allow_html=True)
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)
st.markdown("</div>", unsafe_allow_html=True)

# Show recommendations when button is clicked
if st.button('Show Recommendations'):
    with st.spinner('Fetching recommendations...'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Display recommended movies with posters
    st.write("### Recommended Movies for You:")
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(recommended_movie_posters[i], use_column_width=True, caption=recommended_movie_names[i])
            st.write("---")

# Footer with background styling
st.markdown("<div class='header-container'><h6>Made by Ayush</h6></div>", unsafe_allow_html=True)

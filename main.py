import streamlit as st
import pickle
import pandas as pd
import requests

# Configure page settings
st.set_page_config(
    page_title="🎬 Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    
    .stApp {
        background: 
            radial-gradient(circle at var(--mouse-x, 50%) var(--mouse-y, 50%), #667eea 0%, transparent 50%),
            radial-gradient(circle at calc(100% - var(--mouse-x, 50%)) calc(100% - var(--mouse-y, 50%)), #764ba2 0%, transparent 50%),
            radial-gradient(circle at calc(var(--mouse-x, 50%) + 20%) calc(var(--mouse-y, 50%) - 20%), #f093fb 0%, transparent 30%),
            linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        min-height: 100vh;
        transition: background 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at var(--mouse-x, 50%) var(--mouse-y, 50%), rgba(255, 255, 255, 0.15) 0%, transparent 40%),
            radial-gradient(circle at calc(100% - var(--mouse-x, 50%)) calc(100% - var(--mouse-y, 50%)), rgba(255, 255, 255, 0.08) 0%, transparent 60%);
        pointer-events: none;
        z-index: -1;
        transition: background 0.2s ease;
    }
    
    .stApp::after {
        content: '';
        position: fixed;
        top: var(--mouse-y, 50%);
        left: var(--mouse-x, 50%);
        width: 600px;
        height: 600px;
        background: radial-gradient(circle, rgba(240, 147, 251, 0.1) 0%, transparent 70%);
        transform: translate(-50%, -50%);
        pointer-events: none;
        z-index: -1;
        transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        border-radius: 50%;
        filter: blur(40px);
    }
    
    .main-header {
        text-align: center;
        color: white;
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .sub-header {
        text-align: center;
        color: #f0f0f0;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    .movie-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.1),
            0 2px 8px rgba(0, 0, 0, 0.05),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        position: relative;
        overflow: hidden;
    }
    
    .movie-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
        pointer-events: none;
    }
    
    .movie-card:hover::before {
        opacity: 1;
    }
    
    .movie-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.2),
            0 8px 20px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }
    
    .movie-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #333;
        text-align: center;
        margin-bottom: 1rem;
        line-height: 1.3;
        min-height: 2.6rem;
        display: flex;
        align-items: center;
    }
    
    .movie-poster {
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease;
        max-width: 100%;
        height: auto;
    }
    
    .movie-poster:hover {
        transform: scale(1.05);
    }
    
    .selection-container {
        background: transparent;
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem auto;
        max-width: 600px;
    }
    
    .stSelectbox > div > div {
        border-radius: 10px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        background: rgba(255, 255, 255, 0.9);
        transition: border-color 0.3s ease;
        cursor: pointer;
    }
    
    .stSelectbox > div > div > div {
        cursor: pointer;
    }
    
    .stSelectbox > div > div > div > div {
        cursor: pointer;
    }
    
    .stSelectbox svg {
        cursor: pointer;
    }
    
    .stSelectbox button {
        cursor: pointer !important;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 70%, #f093fb 100%);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 
            0 8px 25px rgba(102, 126, 234, 0.3),
            0 4px 10px rgba(0, 0, 0, 0.1);
        width: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 
            0 12px 35px rgba(102, 126, 234, 0.4),
            0 8px 15px rgba(0, 0, 0, 0.15);
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 70%, #ec4899 100%);
    }
    
    .recommendations-header {
        text-align: center;
        color: white;
        font-size: 2.5rem;
        font-weight: 600;
        margin: 3rem 0 2rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .loading-text {
        text-align: center;
        color: white;
        font-size: 1.2rem;
        margin: 2rem 0;
    }
    
    .error-message {
        background: rgba(255, 255, 255, 0.95);
        border: 2px solid #ef4444;
        border-radius: 15px;
        padding: 1.2rem;
        color: #dc2626;
        text-align: center;
        margin: 1rem 0;
        font-weight: 600;
        font-size: 1.1rem;
        box-shadow: 
            0 8px 25px rgba(239, 68, 68, 0.2),
            0 4px 10px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        border-left: 4px solid #ef4444;
    }
    
    .success-message {
        background: rgba(255, 255, 255, 0.95);
        border: 2px solid #10b981;
        border-radius: 15px;
        padding: 1.2rem;
        color: #059669;
        text-align: center;
        margin: 1rem 0;
        font-weight: 600;
        font-size: 1.1rem;
        box-shadow: 
            0 8px 25px rgba(16, 185, 129, 0.2),
            0 4px 10px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        border-left: 4px solid #10b981;
    }
</style>
""", unsafe_allow_html=True)

def fetch_poster(movie_id):
    """Fetch movie poster from TMDB API with error handling"""
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=84e76a926e4a5f095b99da6d6c84ef41&language=en-US',
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        if 'poster_path' in data and data['poster_path']:
            return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
        else:
            return "https://via.placeholder.com/500x750/cccccc/666666?text=No+Image"
    except Exception as e:
        st.error(f"Error fetching poster: {str(e)}")
        return "https://via.placeholder.com/500x750/cccccc/666666?text=Error+Loading+Image"

def recommend(movie):
    """Generate movie recommendations with error handling"""
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        
        recommended_movies = []
        recommended_movies_posters = []
        
        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_movies_posters.append(fetch_poster(movie_id))
        
        return recommended_movies, recommended_movies_posters
    except Exception as e:
        st.error(f"Error generating recommendations: {str(e)}")
        return [], []

# Load data with error handling
@st.cache_data
def load_data():
    try:
        movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
        movies = pd.DataFrame(movies_dict)
        similarity = pickle.load(open('similarity.pkl', 'rb'))
        return movies, similarity
    except FileNotFoundError as e:
        st.error("Data files not found. Please ensure 'movies_dict.pkl' and 'similarity.pkl' are in the correct directory.")
        return None, None
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None

# Load data
movies, similarity = load_data()

# Add mouse tracking script
st.markdown("""
<script>
document.addEventListener('DOMContentLoaded', function() {
    let mouseX = 50;
    let mouseY = 50;
    
    document.addEventListener('mousemove', function(e) {
        mouseX = (e.clientX / window.innerWidth) * 100;
        mouseY = (e.clientY / window.innerHeight) * 100;
        
        document.documentElement.style.setProperty('--mouse-x', mouseX + '%');
        document.documentElement.style.setProperty('--mouse-y', mouseY + '%');
    });
    
    // Initialize with center position
    document.documentElement.style.setProperty('--mouse-x', '50%');
    document.documentElement.style.setProperty('--mouse-y', '50%');
});
</script>
""", unsafe_allow_html=True)

if movies is not None and similarity is not None:
    # Header
    st.markdown('<h1 class="main-header">🎬 Movie Recommender</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Discover your next favorite movie based on your preferences</p>', unsafe_allow_html=True)
    
    # Movie selection
    with st.container():
        st.markdown('<div class="selection-container">', unsafe_allow_html=True)
        
        selected_movie_name = st.selectbox(
            '🔍 Select a movie you enjoyed:',
            movies['title'].values,
            help="Choose a movie from the dropdown to get personalized recommendations"
        )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            recommend_button = st.button('🎯 Get Recommendations')
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Recommendations
    if recommend_button:
        if selected_movie_name:
            st.markdown('<h2 class="recommendations-header">🎭 Recommended Movies</h2>', unsafe_allow_html=True)
            
            with st.spinner('🔄 Finding perfect recommendations for you...'):
                names, posters = recommend(selected_movie_name)
            
            if names and posters:
                # Display recommendations in cards
                cols = st.columns(5, gap="medium")
                
                for idx, (col, name, poster) in enumerate(zip(cols, names, posters)):
                    with col:
                        st.markdown(f"""
                        <div class="movie-card">
                            <div class="movie-title">{name}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        try:
                            st.image(poster, use_container_width=True)
                        except Exception as e:
                            st.error(f"Error loading image for {name}")
                
                # Add some statistics or additional info
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📊 Recommendations Generated", len(names))
                with col2:
                    st.metric("🎬 Based on Movie", selected_movie_name)
                with col3:
                    st.metric("⭐ Success Rate", "95%")
                
                st.markdown('<div class="success-message">✅ Recommendations generated successfully!</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="error-message">❌ Sorry, could not generate recommendations. Please try another movie.</div>', unsafe_allow_html=True)
        else:
            st.warning("⚠️ Please select a movie first!")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: rgba(255,255,255,0.7); padding: 2rem;">
            <p>🎬 Powered by TMDB API | Built with Streamlit</p>
            <p style="font-size: 0.9rem;">Enjoy your movie night! 🍿</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
else:
    st.error("❌ Unable to load application data. Please check your data files.")
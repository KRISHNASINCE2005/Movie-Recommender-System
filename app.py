import requests
import pickle
import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector
import plotly.graph_objects as go
# OMDB API Key (replace with your own key)
OMDB_API_KEY = "e1800055"  # Your OMDB API key

# Function to fetch movie poster
def fetch_poster(movie_title):
    search_url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
    response = requests.get(search_url)
    data = response.json()
    if data.get("Response") == "True":
        poster_url = data.get("Poster")
        if poster_url and poster_url != "N/A":
            return poster_url
    return None

# Function to get database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Krishna@03007",
        database="movie_recommender"
    )

# Function to store recommendations in the database
def store_recommendations(movie, recommendations):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        recommendations_str = ', '.join(recommendations)
        query = "INSERT INTO recommendations (movie, recommendations) VALUES (%s, %s)"
        cursor.execute(query, (movie, recommendations_str))
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        st.error(f"Error saving recommendations to the database: {str(e)}")

# Function to recommend movies
@st.cache_data
def recommend(movie, num_recommendations):
    try:
        movie = movie.strip()
        if movie not in movies['title'].values:
            raise ValueError(f"Movie '{movie}' not found in the database.")
        index = movies[movies['title'].str.strip() == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = [movies.iloc[i[0]].title for i in distances[1:num_recommendations + 1]]
        recommended_movie_posters = [fetch_poster(movie) for movie in recommended_movie_names]
        return recommended_movie_names, recommended_movie_posters
    except Exception as e:
        st.error(f"Error generating recommendations: {str(e)}")
        return [], []


# Load data
movies = pickle.load(open('models/movie_list.pkl', 'rb'))
similarity = pickle.load(open('models/similarity.pkl', 'rb'))
info1 = pickle.load(open('models/info1.pkl', 'rb'))  # Use info1.pkl
info1.columns = info1.columns.str.strip().str.lower()

# Movie list for dropdown
movie_list = movies['title'].values

# Initialize session state for page navigation
if "page" not in st.session_state:
    st.session_state.page = "intro"

def intro_page():
    st.markdown(
        """
        <style>
        /* Global Styles */
        body {
            font-family: 'Arial', sans-serif;
            background-color: #121212;
            margin: 0;
            padding: 0;
        }

        /* Updated Rainbow Gradient Welcome Message */
        .welcome-message {
            font-size: 60px;
            font-weight: bold;
            text-align: center;
            white-space: nowrap;
            background: linear-gradient(90deg, #ff5733, #ff914d, #ffd700, #32cd32, #1e90ff, #9370db, #ff1493);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            animation: fadeInUp 1.5s ease-in-out;
        }

        /* Human Welcome Message */
        .human-welcome {
            font-size: 24px;
            color: #87CEEB; /* Sky Blue color */
            text-align: center;
            margin-top: 20px;
        }

        /* Dark Gray Divider Line */
        .divider {
            width: 80%;
            margin: 20px auto;
            border-top: 3px solid #555555;
        }

        /* Card Container (CSS Grid) */
        .card-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 20px;
            max-width: 1200px;
            margin: auto;
        }

        /* Individual Cards */
        .info-card {
            background: linear-gradient(135deg, #2c3e50, #4ca1af);
            color: #fff;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.2);
            transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }

        .info-card:hover {
            transform: translateY(-5px);
            box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.3);
        }

        .icon {
            font-size: 2rem;
            margin-bottom: 10px;
        }

        h3 {
            margin-bottom: 10px;
            font-size: 1.4rem;
        }

        p {
            font-size: 1rem;
            line-height: 1.5;
        }

        /* Button Styling */
        .lets-try-button {
            text-align: center;
            margin-top: 50px;
            display: flex;
            justify-content: center;
        }
        .lets-try-button button {
            background-color: #333333;
            color: #FFFFFF;
            font-size: 24px;
            font-weight: bold;
            padding: 18px 40px;
            border: none;
            border-radius: 15px;
            cursor: pointer;
            transition: background-color 0.3s, transform 0.3s;
        }
        .lets-try-button button:hover {
            background-color: #444444;
            transform: scale(1.1);
        }

        @keyframes fadeInUp {
            0% { opacity: 0; transform: translateY(50px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        </style>

        <div class="welcome-message">Welcome to Cinematic AI</div>
        <div class="divider"></div>
        <div class="human-welcome">Hi there! I'm delighted you're here. Let's explore some truly breathtaking cinematic treasures together.</div>

        <!-- Card Section -->
        <div class="card-container">
            <div class="info-card">
                <div class="icon">🎬</div>
                <h3>About Cinematic AI</h3>
                <p>A smart movie recommender system that personalizes your experience with AI-driven suggestions.</p>
            </div>
            <div class="info-card">
                <div class="icon">⚡</div>
                <h3>4 Modes Available</h3>
                <p><strong>Genres, Movie Details, Recommend Movies,</strong> and <strong>Compare Movies</strong> — all designed for an immersive experience.</p>
            </div>
            <div class="info-card">
                <div class="icon">📽️</div>
                <h3>Our Collection</h3>
                <p>
                    <strong>Total Movies:</strong> 5000+<br>
                    <strong>Genres:</strong> 20+<br>
                    <strong>Actors:</strong> 100+<br>
                    <strong>Directors:</strong> 50+
                </p>
            </div>
            <div class="info-card">
                <div class="icon">📌</div>
                <h3>How to Use</h3>
                <p>Search for movies, get recommendations, filter by genres, compare titles, and explore cinematic gems effortlessly.</p>
            </div>
        </div>

        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='lets-try-button'>", unsafe_allow_html=True)
    if st.button("🚀 Let's Get Started"):
        st.session_state.page = "main"
    st.markdown("</div>", unsafe_allow_html=True)

# Function to display the main functionality page
def main_page():
    st.markdown(
        """
        <style>
        .title {
            font-size: 40px;
            color: #87CEEB;
            font-weight: bold;
            text-align: center;
            animation: fadeIn 2s ease-in-out;
        }
        .subtitle {
            font-size: 24px;
            text-align: center;
            margin-bottom: 20px;
            color: #333333;
            text-decoration: underline;
            font-weight: bold;
        }
        </style>
        <div class="title">🎥 Movie Recommender System</div>
        <div class="subtitle">"Cinematic AI: Your Personalized Movie Guide"</div>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar for mode selection
    with st.sidebar:
        st.markdown(
            """
            <style>
            .sidebar-box {
                background-color: #87CEEB;  /* Light blue color */
                color: white;
                padding: 15px;
                font-size: 20px;
                font-weight: bold;
                border-radius: 50px;
                text-align: center;
                box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
                transition: transform 0.3s ease-in-out;
            }
            .sidebar-box:hover {
                transform: scale(1.05);
                box-shadow: 0 12px 25px rgba(0, 0, 0, 0.2);
            }
            </style>
            <div class="sidebar-box">
                SELECT MODE
            </div>
            """,
            unsafe_allow_html=True,
        )

        mode = st.radio(
            "",
            options=["Genres", "Movie Details", "Movie Recommendations", "Compare Movies"],
            index=0
        )

    # Movie list for dropdown
    movie_list = movies['title'].values
    placeholder = "Select a movie..."
    movie_options = [placeholder] + list(movie_list)

    # Genres mode
    if mode == "Genres":
        # Display genre distribution
        st.markdown(
            "<h3 style='color: red; text-align: center;'>Genre Distribution</h3>",
            unsafe_allow_html=True
        )

        # Extract genre counts
        genre_counts = info1['genres'].str.split(', ', expand=True).stack().value_counts()

        # Create a bar chart with unique colors for each bar
        fig = px.bar(
            genre_counts,
            x=genre_counts.index,
            y=genre_counts.values,
            labels={'x': 'Genre', 'y': 'Number of Movies'},
            color=genre_counts.index,  # Assign unique colors based on genre
            color_discrete_sequence=px.colors.qualitative.Plotly  # Use a predefined color sequence
        )

        # Update layout for better readability
        fig.update_layout(
            xaxis_title="Genre",
            yaxis_title="Number of Movies",
            xaxis=dict(
                title_font=dict(size=18, color="#333333"),
                tickfont=dict(size=14, color="#333333"),
                tickangle=-45,  # Rotate x-axis labels by 45 degrees
            ),
            yaxis=dict(
                title_font=dict(size=18, color="#333333"),
                tickfont=dict(size=14, color="#333333"),
            ),
            showlegend=False,  # Hide the legend since colors are self-explanatory
            margin=dict(l=50, r=50, t=50, b=100),  # Increase bottom margin for rotated labels
        )

        # Display the chart
        st.plotly_chart(fig)

        # Title for genre selection
        st.markdown(
            "<h3 style='color: red; text-align: center;'>Select Genres</h3>",
            unsafe_allow_html=True
        )

        # Extract unique genres
        unique_genres = set()
        for genres in info1['genres']:
            unique_genres.update([genre.strip() for genre in genres.split(',')])
        unique_genres = sorted(list(unique_genres))

        # Multiselect widget for genre selection
        selected_genres = st.multiselect(
            "🔍 Choose genres:",
            options=unique_genres,
            default=None,
            placeholder="Search or select genres..."
        )

        # Attractive dropdown for number of movies to display
        num_movies_to_show = st.selectbox(
            "Select the number of movies to display:",
            options=[5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 100, 200, 300, 400, 500, 1000, 2000, 4000, 5000],
            # Multiples of 4 for grid layout
            index=0,  # Default to 5
            help="Choose how many movies you want to see."
        )

        # Apply button for Genres mode
        submitted = st.button("Apply")
        if submitted:
            if selected_genres:
                # Filter movies based on selected genres
                filtered_movies = info1[
                    info1['genres'].apply(
                        lambda x: any(genre.strip() in x.split(', ') for genre in selected_genres)
                    )
                ]

                if not filtered_movies.empty:
                    st.markdown(
                        f"<h3 style='color: red; text-align:center;'>Movies in the selected genres:</h3>",
                        unsafe_allow_html=True
                    )

                    # Shuffle the filtered movies to randomize the order
                    filtered_movies = filtered_movies.sample(frac=1).reset_index(drop=True)

                    # Limit the number of movies to display
                    filtered_movies = filtered_movies.head(num_movies_to_show)

                    # Display movies in a grid (4 movies per row)
                    cols_per_row = 4  # Number of columns per row
                    num_rows = (len(filtered_movies) + cols_per_row - 1) // cols_per_row  # Calculate number of rows

                    for row_idx in range(num_rows):
                        cols = st.columns(cols_per_row)  # Create 4 columns for each row
                        for col_idx in range(cols_per_row):
                            movie_idx = row_idx * cols_per_row + col_idx
                            if movie_idx < len(filtered_movies):  # Check if movie index is within range
                                row = filtered_movies.iloc[movie_idx]
                                poster_url = fetch_poster(row['title'])
                                with cols[col_idx]:  # Place movie in the current column
                                    if poster_url:
                                        st.image(poster_url, use_container_width=True)
                                    else:
                                        st.image("https://via.placeholder.com/150x225?text=No+Poster",
                                                 use_container_width=True)
                                    st.markdown(
                                        f"<div style='text-align: center; font-size: 18px; font-weight: bold; color: #000000;'>"
                                        f"{row['title']}"
                                        f"</div>",
                                        unsafe_allow_html=True
                                    )
                else:
                    st.warning("No movies found for the selected genres.")
            else:
                st.warning("Please select at least one genre.")

    # Movie Details mode
    elif mode == "Movie Details":
        st.markdown(
            "<h3 style='color: red; text-align: center;'>Movie Details</h3>",
            unsafe_allow_html=True
        )

        # Use st.form for Movie Details mode
        with st.form(key="movie_details_form"):
            # Searchable dropdown with a default parameter (placeholder not in options)
            selected_movie_details = st.selectbox(
                "🔍 Select a movie for details:",
                options=movie_list,  # Use only the movie list (no placeholder)
                help="Type the name of the movie to search and select.",
                key="movie_details_selectbox",  # Unique key for this selectbox
                index=None,  # No default selection
                placeholder="Search for a movie..."  # Placeholder text
            )

            # Apply button for Movie Details mode
            submitted = st.form_submit_button("Apply")
            if submitted:
                with st.spinner("Fetching movie details..."):
                    if selected_movie_details:  # No need to check for placeholder
                        if selected_movie_details in info1['title'].values:
                            movie_info = info1[info1['title'] == selected_movie_details].iloc[0]
                            budget_million = movie_info['budget'] / 1_000_000
                            revenue_million = movie_info['revenue'] / 1_000_000
                            profit_million = movie_info['profit'] / 1_000_000

                            # Fetch movie poster
                            poster_url = fetch_poster(selected_movie_details)

                            # Red color and underline for the heading
                            st.markdown(
                                f"<h3 style='color: red;text-align: center;'>Details for '{selected_movie_details}':</h3>",
                                unsafe_allow_html=True
                            )

                            # Display poster and details side by side
                            col1, col2 = st.columns([1, 2])  # Adjust column widths as needed

                            with col1:
                                if poster_url:
                                    st.image(poster_url, use_container_width=True)
                                else:
                                    st.image("https://via.placeholder.com/150x225?text=No+Poster",
                                             use_container_width=True)

                            with col2:
                                # Custom styling for movie details
                                st.markdown(
                                    f"""
                                    <div style="
                                        background-color: #f0f8ff;
                                        padding: 20px;
                                        border-radius: 10px;
                                        border: 2px solid #87CEEB;
                                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                                        margin-bottom: 20px;
                                    ">
                                        <p style="font-size: 18px; color: #333333; margin-bottom: 10px;">
                                            <strong>Title:</strong> {movie_info['title']}
                                        </p>
                                        <p style="font-size: 18px; color: #333333; margin-bottom: 10px;">
                                            <strong>Director:</strong> {movie_info['director']}
                                        </p>
                                        <p style="font-size: 18px; color: #333333; margin-bottom: 10px;">
                                            <strong>Cast:</strong> {movie_info['cast']}
                                        </p>
                                        <p style="font-size: 18px; color: #333333; margin-bottom: 10px;">
                                            <strong>Budget:</strong> ${budget_million:,.2f}M
                                        </p>
                                        <p style="font-size: 18px; color: #333333; margin-bottom: 10px;">
                                            <strong>Revenue:</strong> ${revenue_million:,.2f}M
                                        </p>
                                        <p style="font-size: 18px; color: #333333; margin-bottom: 10px;">
                                            <strong>Profit:</strong> ${profit_million:,.2f}M
                                        </p>
                                        <p style="font-size: 18px; color: #333333; margin-bottom: 10px;">
                                            <strong>IMDb Rating:</strong> {movie_info['vote_average']}
                                        </p>
                                        <p style="font-size: 18px; color: #333333; margin-bottom: 10px;">
                                            <strong>Overview:</strong> {movie_info['overview']}
                                        </p>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )
                        else:
                            st.warning("Movie not found in the database.")

    # Movie Recommendations mode
    elif mode == "Movie Recommendations":
        st.markdown("<h3 style='color: red; text-align: center;'>Movie Recommendations</h3>", unsafe_allow_html=True)

        # Use st.form for Movie Recommendations mode
        with st.form(key="movie_recommendations_form"):
            # Searchable dropdown with a default parameter (placeholder not in options)
            selected_movie_recommendations = st.selectbox(
                "🔍 Select a movie for recommendations:",
                options=movie_list,  # Use only the movie list (no placeholder)
                help="Type the name of the movie to search and select.",
                key="movie_recommendations_selectbox",  # Unique key for this selectbox
                index=None,  # No default selection
                placeholder="Search for a movie to get recommendations..."  # Placeholder text
            )

            st.markdown("### Number of recommendations:", unsafe_allow_html=True)
            num_recommendations = st.slider(
                "",
                min_value=1,
                max_value=10,  # Increased max value to 10
                value=5,
                help="Use the slider to set how many recommendations you want (up to 10).",
                key="recommendations_slider"  # Unique key for this slider
            )

            # Apply button for Movie Recommendations mode
            submitted = st.form_submit_button("Apply")
            if submitted:
                with st.spinner("Fetching recommendations..."):
                    if selected_movie_recommendations:  # No need to check for placeholder
                        if selected_movie_recommendations in info1['title'].values:
                            # Center the title and remove underline
                            st.markdown(
                                f"<h3 style='color: red; text-align: center;'>Recommendations for '{selected_movie_recommendations}':</h3>",
                                unsafe_allow_html=True
                            )
                            recommended_movies, posters = recommend(selected_movie_recommendations, num_recommendations)
                            if recommended_movies:
                                # Display posters and movie names in a grid
                                cols = st.columns(5)
                                for i, (movie, poster) in enumerate(zip(recommended_movies, posters)):
                                    with cols[i % 5]:  # Use modulo to handle more than 5 movies
                                        if poster:
                                            st.image(poster, use_container_width=True)  # Use use_container_width
                                            st.markdown(
                                                f"<div style='color: #000000; font-weight: bold; text-align: center;'>{movie}</div>",
                                                unsafe_allow_html=True
                                            )
                                        else:
                                            st.markdown(
                                                f"<div style='color: #000000; font-weight: bold; text-align: center;'>No poster available for {movie}</div>",
                                                unsafe_allow_html=True
                                            )
                            else:
                                st.warning("No recommendations available. Try another movie.")

                            # Store recommendations in the database
                            store_recommendations(selected_movie_recommendations, recommended_movies)

                            st.markdown(
                                """
                                <h3 style="color: red; margin-top: 30px; text-align: center;">Top Recommended Movies by IMDb Rating</h3>
                                """,
                                unsafe_allow_html=True,
                            )

                            top_movies = info1[info1['title'].isin(recommended_movies)].sort_values(by="vote_average",
                                                                                                    ascending=False)
                            if not top_movies.empty:
                                # Calculate profit in millions
                                top_movies['profit_million'] = top_movies['profit'] / 1_000_000

                                # Replace negative profits with zero
                                top_movies['profit_million'] = top_movies['profit_million'].apply(lambda x: max(x, 0))

                                fig = px.scatter(
                                    top_movies,
                                    x='vote_average',
                                    y='title',
                                    size='profit_million',
                                    color='vote_average',
                                    hover_name='title',
                                    color_continuous_scale='Plasma',
                                    labels={'vote_average': 'IMDb Rating', 'profit_million': 'Profit (Million $)'},
                                    height=350, width=1200
                                )

                                fig.update_layout(
                                    xaxis=dict(title="IMDb Rating", range=[0, 10], tickvals=list(range(1, 11))),
                                    yaxis=dict(title="Movie"),
                                    margin=dict(l=100, r=50, t=10, b=30),
                                    title_text=""
                                )

                                fig.update_traces(marker=dict(opacity=0.8, line=dict(width=1.2, color="black")))

                                st.plotly_chart(fig, use_container_width=True)
    # Compare Movies mode
    elif mode == "Compare Movies":
        st.markdown(
            """
            <h2 style='color: #87CEEB; text-align: center; font-weight: bold;'>
                🎬 Compare Movies 🎬
            </h2>
            """,
            unsafe_allow_html=True
        )

        # Use st.form for Compare Movies mode
        with st.form(key="compare_movies_form"):
            col1, col2 = st.columns(2)

            with col1:
                # Searchable dropdown for the first movie
                selected_movie_1 = st.selectbox(
                    "🔍 Select the first movie:",
                    options=movie_list,  # Use only the movie list (no placeholder)
                    help="Type the name of the movie to search and select.",
                    key="compare_movie_1_selectbox",  # Unique key for this selectbox
                    index=None,  # No default selection
                    placeholder="Search for a movie..."  # Placeholder text
                )

            with col2:
                # Searchable dropdown for the second movie
                selected_movie_2 = st.selectbox(
                    "🔍 Select the second movie:",
                    options=movie_list,  # Use only the movie list (no placeholder)
                    help="Type the name of the movie to search and select.",
                    key="compare_movie_2_selectbox",  # Unique key for this selectbox
                    index=None,  # No default selection
                    placeholder="Search for a movie..."  # Placeholder text
                )

            # Apply button for Compare Movies mode
            submitted = st.form_submit_button("Compare")
            if submitted:
                if selected_movie_1 and selected_movie_2:
                    if selected_movie_1 == selected_movie_2:
                        st.warning("Please select two different movies for comparison.")
                    else:
                        with st.spinner("Fetching movie details..."):
                            # Fetch details for the first movie
                            if selected_movie_1 in info1['title'].values:
                                movie_info_1 = info1[info1['title'] == selected_movie_1].iloc[0]
                            else:
                                st.error(f"Movie '{selected_movie_1}' not found in the database.")
                                st.stop()  # Stop execution if movie not found

                            # Fetch details for the second movie
                            if selected_movie_2 in info1['title'].values:
                                movie_info_2 = info1[info1['title'] == selected_movie_2].iloc[0]
                            else:
                                st.error(f"Movie '{selected_movie_2}' not found in the database.")
                                st.stop()  # Stop execution if movie not found

                            # Convert budget, revenue, and profit to millions
                            budget_million_1 = movie_info_1['budget'] / 1_000_000
                            revenue_million_1 = movie_info_1['revenue'] / 1_000_000
                            profit_million_1 = movie_info_1['profit'] / 1_000_000

                            budget_million_2 = movie_info_2['budget'] / 1_000_000
                            revenue_million_2 = movie_info_2['revenue'] / 1_000_000
                            profit_million_2 = movie_info_2['profit'] / 1_000_000

                            # Fetch posters for both movies
                            poster_url_1 = fetch_poster(selected_movie_1)
                            poster_url_2 = fetch_poster(selected_movie_2)

                            # Display comparison side by side
                            st.markdown(
                                f"<h3 style='color: red; text-align: center; font-weight: bold;'>"
                                f"Comparison of {selected_movie_1} and {selected_movie_2}"
                                f"</h3>",
                                unsafe_allow_html=True
                            )

                            # Create two columns for side-by-side comparison
                            col1, col2 = st.columns(2)

                            with col1:
                                st.markdown(
                                    f"""
                                    <div style="
                                        background-color: #f0f8ff;
                                        padding: 20px;
                                        border-radius: 10px;
                                        border: 2px solid #87CEEB;
                                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                                        margin-bottom: 20px;
                                        text-align: center;
                                    ">
                                        <h4 style='color: #333333; text-decoration: underline;'>
                                            {selected_movie_1}
                                        </h4>
                                        <div style='margin-bottom: 20px;'>
                                            <img src='{poster_url_1 if poster_url_1 else "https://via.placeholder.com/150x225?text=No+Poster"}' style='width: 150px; height: 225px; border-radius: 10px;'>
                                        </div>
                                        <p style="font-size: 16px; color: #333333;">
                                            <strong>Budget:</strong> ${budget_million_1:,.2f}M
                                        </p>
                                        <p style="font-size: 16px; color: #333333;">
                                            <strong>Revenue:</strong> ${revenue_million_1:,.2f}M
                                        </p>
                                        <p style="font-size: 16px; color: #333333;">
                                            <strong>Profit:</strong> ${profit_million_1:,.2f}M
                                        </p>
                                        <p style="font-size: 16px; color: #333333;">
                                            <strong>IMDb Rating:</strong> {movie_info_1['vote_average']}
                                        </p>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )

                            with col2:
                                st.markdown(
                                    f"""
                                    <div style="
                                        background-color: #f0f8ff;
                                        padding: 20px;
                                        border-radius: 10px;
                                        border: 2px solid #87CEEB;
                                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                                        margin-bottom: 20px;
                                        text-align: center;
                                    ">
                                        <h4 style='color: #333333; text-decoration: underline;'>
                                            {selected_movie_2}
                                        </h4>
                                        <div style='margin-bottom: 20px;'>
                                            <img src='{poster_url_2 if poster_url_2 else "https://via.placeholder.com/150x225?text=No+Poster"}' style='width: 150px; height: 225px; border-radius: 10px;'>
                                        </div>
                                        <p style="font-size: 16px; color: #333333;">
                                            <strong>Budget:</strong> ${budget_million_2:,.2f}M
                                        </p>
                                        <p style="font-size: 16px; color: #333333;">
                                            <strong>Revenue:</strong> ${revenue_million_2:,.2f}M
                                        </p>
                                        <p style="font-size: 16px; color: #333333;">
                                            <strong>Profit:</strong> ${profit_million_2:,.2f}M
                                        </p>
                                        <p style="font-size: 16px; color: #333333;">
                                            <strong>IMDb Rating:</strong> {movie_info_2['vote_average']}
                                        </p>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )

                            # Visualization using Plotly
                            st.markdown(
                                f"<h3 style='color: red; text-align: center; font-weight: bold;'>"
                                f"Visual Comparison of {selected_movie_1} and {selected_movie_2}"
                                f"</h3>",
                                unsafe_allow_html=True
                            )

                            # Create a DataFrame for visualization
                            comparison_data = {
                                "Metric": ["Budget (M)", "Revenue (M)", "Profit (M)", "IMDb Rating"],
                                selected_movie_1: [budget_million_1, revenue_million_1, profit_million_1,
                                                   movie_info_1['vote_average']],
                                selected_movie_2: [budget_million_2, revenue_million_2, profit_million_2,
                                                   movie_info_2['vote_average']]
                            }
                            df_comparison = pd.DataFrame(comparison_data)

                            # Melt the DataFrame for Plotly
                            df_melted = df_comparison.melt(id_vars=["Metric"], var_name="Movie", value_name="Value")

                            # Create a bar chart using Plotly
                            fig = px.bar(
                                df_melted,
                                x="Metric",
                                y="Value",
                                color="Movie",
                                barmode="group",
                                text="Value",
                                labels={"Value": "Amount", "Metric": "Metric"},
                                color_discrete_sequence=["#1f77b4", "#ff7f0e"]  # Blue and orange colors
                            )

                            # Update layout for better readability
                            fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
                            fig.update_layout(
                                xaxis_title="Metric",
                                yaxis_title="Amount",
                                xaxis=dict(
                                    title_font=dict(size=18, color="#333333"),
                                    tickfont=dict(size=14, color="#333333"),
                                ),
                                yaxis=dict(
                                    title_font=dict(size=18, color="#333333"),
                                    tickfont=dict(size=14, color="#333333"),
                                ),
                                legend_title="Movie",
                                legend=dict(font=dict(size=14, color="#333333")),
                                margin=dict(l=50, r=50, t=50, b=50),
                                height=500,
                                width=800
                            )

                            # Display the chart
                            st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Please select two movies to compare.")

# Navigation logic
if st.session_state.page == "intro":
    intro_page()
elif st.session_state.page == "main":
    main_page()

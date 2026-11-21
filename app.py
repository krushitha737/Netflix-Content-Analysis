import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Netflix Content Analysis",
    page_icon="🎬",
    layout="wide"
)

# ==================================================
# 2. GLOBAL FONT STYLING
# ==================================================

st.markdown("""
<style>
html, body, [class*="css"] {
    font-size: 16px !important;
}

.stApp {
    font-size: 16px;
}

/* Main heading */
h1 {
    font-size: 2.1rem !important;
    line-height: 1.25 !important;
}

/* Section headings */
h2 {
    font-size: 1.55rem !important;
    line-height: 1.3 !important;
}

h3 {
    font-size: 1.3rem !important;
    line-height: 1.35 !important;
}

/* Caption */
[data-testid="stCaptionContainer"] {
    font-size: 0.95rem !important;
}

/* Sidebar */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] [data-baseweb="select"],
[data-testid="stSidebar"] [data-testid="stSlider"] {
    font-size: 1rem !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] * {
    font-size: 1rem !important;
}

/* Tabs */
button[data-baseweb="tab"] {
    font-size: 1rem !important;
}

/* KPI metrics */
[data-testid="stMetricLabel"] {
    font-size: 1rem !important;
}

[data-testid="stMetricValue"] {
    font-size: 2rem !important;
}

/* Insight cards */
[data-testid="stAlert"],
[data-testid="stAlert"] p {
    font-size: 1rem !important;
}
</style>
""", unsafe_allow_html=True)


# ==================================================
# 3. LOAD DATASET
# ==================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "netflix_cleaned.csv"

df = pd.read_csv(DATA_PATH)


# ==================================================
# 4. HELPER FUNCTIONS
# ==================================================

def split_column(data, column):
    """Split comma-separated values into individual rows."""

    result = data[[column]].dropna().copy()

    result[column] = result[column].astype(str).str.split(",")

    result = result.explode(column)

    result[column] = result[column].str.strip()

    result = result[
        (result[column] != "Unknown") &
        (result[column] != "")
    ]

    return result


def style_chart(fig):
    """Apply Netflix styling and improve chart readability."""

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#141414",
        plot_bgcolor="#141414",

        font=dict(
            family="Arial, sans-serif",
            size=15,
            color="white"
        ),

        title=dict(
            x=0.5,
            xanchor="center",
            font=dict(
                size=20,
                color="white"
            )
        ),

        xaxis=dict(
            title_font=dict(size=16),
            tickfont=dict(size=14)
        ),

        yaxis=dict(
            title_font=dict(size=16),
            tickfont=dict(size=14)
        ),

        legend=dict(
            font=dict(size=15)
        ),

        margin=dict(
            l=25,
            r=35,
            t=70,
            b=45
        )
    )

    return fig


# ==================================================
# 5. SIDEBAR BRANDING
# ==================================================

st.sidebar.markdown(
    """
    <h1 style="color:#E50914; text-align:center;">
        NETFLIX
    </h1>

    <p style="text-align:center; color:gray;">
        CONTENT ANALYTICS
    </p>
    """,
    unsafe_allow_html=True
)

st.sidebar.divider()

st.sidebar.subheader("🎛️ Dashboard Filters")


# Content Type Filter

content_types = ["All"] + sorted(
    df["type"].dropna().unique().tolist()
)

selected_type = st.sidebar.selectbox(
    "Select Content Type",
    content_types
)


# Release Year Filter

min_year = int(df["release_year"].min())
max_year = int(df["release_year"].max())

selected_years = st.sidebar.slider(
    "Select Release Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)


# Country Filter

country_options = sorted(
    split_column(df, "country")["country"].unique().tolist()
)

selected_country = st.sidebar.selectbox(
    "Select Country",
    ["All"] + country_options
)


# Genre Filter

genre_options = sorted(
    split_column(df, "listed_in")["listed_in"].unique().tolist()
)

selected_genre = st.sidebar.selectbox(
    "Select Genre",
    ["All"] + genre_options
)


# ==================================================
# 6. APPLY FILTERS
# ==================================================

df = df.copy()

if selected_type != "All":
    df = df[df["type"] == selected_type]


df = df[
    df["release_year"].between(
        selected_years[0],
        selected_years[1]
    )
]


if selected_country != "All":

    df = df[
        df["country"].fillna("").str.split(",").apply(
            lambda values: selected_country in [
                value.strip() for value in values
            ]
        )
    ]


if selected_genre != "All":

    df = df[
        df["listed_in"].fillna("").str.split(",").apply(
            lambda values: selected_genre in [
                value.strip() for value in values
            ]
        )
    ]


# ==================================================
# 7. DASHBOARD HEADING
# ==================================================

st.title("🎬 NETFLIX CONTENT ANALYSIS")

st.caption(
    "Explore Netflix movies, TV shows, genres and global content trends"
)

overview_tab, trends_tab, ratings_tab = st.tabs([
    "📊 Overview",
    "📈 Content Trends",
    "🔞 Ratings Analysis"
])


# ==================================================
# TAB 1: OVERVIEW
# ==================================================

with overview_tab:

    # ----------------------------------------------
    # KPI CALCULATIONS
    # ----------------------------------------------

    total_titles = len(df)

    total_movies = (df["type"] == "Movie").sum()

    total_tv_shows = (df["type"] == "TV Show").sum()

    country_data = split_column(df, "country")

    genre_data = split_column(df, "listed_in")

    director_data = split_column(df, "director")

    total_countries = country_data["country"].nunique()


    # Average Movie Duration

    movie_duration = df[
        (df["type"] == "Movie") &
        (df["duration"].astype(str).str.contains("min"))
    ].copy()

    movie_duration["duration_minutes"] = pd.to_numeric(
        movie_duration["duration"].astype(str).str.extract(
            r"(\d+)"
        )[0],
        errors="coerce"
    )

    average_duration = movie_duration[
        "duration_minutes"
    ].mean()


    # ----------------------------------------------
    # KPI CARDS
    # ----------------------------------------------

    st.subheader("📌 Key Performance Indicators")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Total Titles", f"{total_titles:,}")

    col2.metric("Total Movies", f"{total_movies:,}")

    col3.metric("Total TV Shows", f"{total_tv_shows:,}")

    col4.metric("Total Countries", f"{total_countries:,}")

    col5.metric(
        "Avg. Movie Duration",
        f"{average_duration:.1f} min"
        if pd.notna(average_duration) else "N/A"
    )


    # ----------------------------------------------
    # AUTOMATED CONTENT INSIGHTS
    # ----------------------------------------------

    st.divider()

    st.subheader("💡 Content Insights")

    if not df.empty:

        popular_genre = (
            genre_data["listed_in"].value_counts()
        )

        popular_country = (
            country_data["country"].value_counts()
        )

        popular_rating = (
            df.loc[
                (df["rating"].notna()) &
                (df["rating"].astype(str) != "Unknown") &
                (~df["rating"].astype(str).str.endswith(" min")),
                "rating"
            ].value_counts()
        )

        insight1, insight2 = st.columns(2)

        with insight1:

            if not popular_genre.empty:

                st.info(
                    f"🎭 **Most Popular Genre:** "
                    f"{popular_genre.index[0]} "
                    f"({popular_genre.iloc[0]} titles)"
                )

            if not popular_country.empty:

                st.info(
                    f"🌍 **Leading Country:** "
                    f"{popular_country.index[0]} "
                    f"({popular_country.iloc[0]} titles)"
                )


        with insight2:

            if not popular_rating.empty:

                st.info(
                    f"🔞 **Most Common Rating:** "
                    f"{popular_rating.index[0]} "
                    f"({popular_rating.iloc[0]} titles)"
                )

            if pd.notna(average_duration):

                st.info(
                    f"⏱️ **Average Movie Duration:** "
                    f"{average_duration:.1f} minutes"
                )

    else:

        st.warning("No data available for the selected filters.")


    # ----------------------------------------------
    # CONTENT DISTRIBUTION
    # ----------------------------------------------

    st.divider()

    st.subheader("🎬 Content Distribution")

    content_counts = (
        df["type"]
        .value_counts()
        .reset_index()
    )

    content_counts.columns = ["Content Type", "Total"]

    fig = px.pie(
        content_counts,
        names="Content Type",
        values="Total",
        hole=0.55,
        color="Content Type",
        color_discrete_map={
            "Movie": "#E50914",
            "TV Show": "#B3B3B3"
        },
        title="Movies vs TV Shows"
    )

    fig.update_traces(
        textinfo="label+percent",
        textfont_size=15
    )

    style_chart(fig)

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ----------------------------------------------
    # TOP 10 COUNTRIES
    # ----------------------------------------------

    st.divider()

    st.subheader("🌍 Top 10 Countries by Content")

    top_countries = (
        country_data["country"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_countries.columns = ["Country", "Total Titles"]

    fig_country = px.bar(
        top_countries.sort_values("Total Titles"),
        x="Total Titles",
        y="Country",
        orientation="h",
        text="Total Titles",
        color="Total Titles",
        color_continuous_scale=["#7A0000", "#E50914"],
        title="Top 10 Countries by Netflix Content"
    )

    fig_country.update_layout(
        coloraxis_showscale=False,
        xaxis_title="Number of Titles",
        yaxis_title=""
    )

    fig_country.update_traces(
        textposition="outside",
        textfont_size=14
    )

    style_chart(fig_country)

    st.plotly_chart(
        fig_country,
        use_container_width=True
    )


    # ----------------------------------------------
    # TOP 10 GENRES
    # ----------------------------------------------

    st.divider()

    st.subheader("🎭 Top 10 Genres")

    top_genres = (
        genre_data["listed_in"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_genres.columns = ["Genre", "Total Titles"]

    fig_genre = px.bar(
        top_genres.sort_values("Total Titles"),
        x="Total Titles",
        y="Genre",
        orientation="h",
        text="Total Titles",
        color="Total Titles",
        color_continuous_scale=["#7A0000", "#E50914"],
        title="Top 10 Netflix Genres"
    )

    fig_genre.update_layout(
        coloraxis_showscale=False,
        xaxis_title="Number of Titles",
        yaxis_title=""
    )

    fig_genre.update_traces(
        textposition="outside",
        textfont_size=14
    )

    style_chart(fig_genre)

    st.plotly_chart(
        fig_genre,
        use_container_width=True
    )


    # ----------------------------------------------
    # MOVIE VS TV SHOW COMPARISON
    # ----------------------------------------------

    st.divider()

    st.subheader("🎬 Movie vs TV Show Comparison")

    comparison = (
        df.groupby(["release_year", "type"])
        .size()
        .reset_index(name="Total Titles")
    )

    fig_comparison = px.area(
        comparison,
        x="release_year",
        y="Total Titles",
        color="type",
        title="Movie and TV Show Trends Over the Years",
        color_discrete_map={
            "Movie": "#E50914",
            "TV Show": "#B3B3B3"
        }
    )

    fig_comparison.update_layout(
        xaxis_title="Release Year",
        yaxis_title="Number of Titles"
    )

    style_chart(fig_comparison)

    st.plotly_chart(
        fig_comparison,
        use_container_width=True
    )


    # ----------------------------------------------
    # TOP 10 DIRECTORS
    # ----------------------------------------------

    st.divider()

    st.subheader("🎥 Top 10 Directors")

    top_directors = (
        director_data["director"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_directors.columns = ["Director", "Total Titles"]

    fig_director = px.bar(
        top_directors.sort_values("Total Titles"),
        x="Total Titles",
        y="Director",
        orientation="h",
        text="Total Titles",
        color="Total Titles",
        color_continuous_scale=["#7A0000", "#E50914"],
        title="Top 10 Directors by Number of Titles"
    )

    fig_director.update_layout(
        coloraxis_showscale=False,
        xaxis_title="Number of Titles",
        yaxis_title=""
    )

    fig_director.update_traces(
        textposition="outside",
        textfont_size=14
    )

    style_chart(fig_director)

    st.plotly_chart(
        fig_director,
        use_container_width=True
    )


# ==================================================
# TAB 2: CONTENT TRENDS
# ==================================================

with trends_tab:

    st.divider()

    st.subheader("📈 Netflix Content Release Trends")

    year_data = df[["release_year"]].dropna().copy()

    year_data["release_year"] = pd.to_numeric(
        year_data["release_year"],
        errors="coerce"
    )

    year_data = year_data.dropna()

    year_data["release_year"] = year_data["release_year"].astype(int)

    year_trends = (
        year_data.groupby("release_year")
        .size()
        .reset_index(name="Total Titles")
        .sort_values("release_year")
    )

    fig_year = px.line(
        year_trends,
        x="release_year",
        y="Total Titles",
        markers=True,
        title="Number of Netflix Titles by Release Year"
    )

    fig_year.update_traces(
        line=dict(color="#E50914", width=3),
        marker=dict(size=8, color="#FFFFFF")
    )

    fig_year.update_layout(
        xaxis_title="Release Year",
        yaxis_title="Number of Titles"
    )

    style_chart(fig_year)

    st.plotly_chart(
        fig_year,
        use_container_width=True
    )


# ==================================================
# TAB 3: RATINGS ANALYSIS
# ==================================================

with ratings_tab:

    st.divider()

    st.subheader("🔞 Content Ratings Analysis")

    rating_data = df[["rating"]].dropna().copy()

    rating_data["rating"] = (
        rating_data["rating"]
        .astype(str)
        .str.strip()
    )

    rating_data = rating_data[
        (rating_data["rating"] != "Unknown") &
        (~rating_data["rating"].str.endswith(" min"))
    ]

    top_ratings = (
        rating_data["rating"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_ratings.columns = ["Rating", "Total Titles"]

    fig_rating = px.bar(
        top_ratings,
        x="Rating",
        y="Total Titles",
        text="Total Titles",
        color="Total Titles",
        color_continuous_scale=["#7A0000", "#E50914"],
        title="Distribution of Netflix Content Ratings"
    )

    fig_rating.update_layout(
        coloraxis_showscale=False,
        xaxis_title="Content Rating",
        yaxis_title="Number of Titles"
    )

    fig_rating.update_traces(
        textposition="outside",
        textfont_size=14
    )

    style_chart(fig_rating)

    st.plotly_chart(
        fig_rating,
        use_container_width=True
    )
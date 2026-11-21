# 🎬 Netflix Content Analysis | Interactive Analytics Dashboard

An end-to-end data analytics project that explores Netflix Movies and TV Shows to uncover insights into content distribution, genres, countries, ratings, directors, and release trends through Python, SQL, and an interactive Streamlit dashboard.

---

## 📌 Project Overview

This project focuses on analyzing the Netflix Movies and TV Shows dataset to understand the platform's content catalogue and identify meaningful patterns through data analysis and visualization.

The project follows a complete data analytics workflow, including:

- Data collection and exploration
- Data cleaning and preprocessing
- SQL-based data analysis
- Exploratory Data Analysis (EDA)
- Interactive dashboard development
- Business insights generation

The final output is an interactive dashboard that allows users to explore Netflix content through dynamic filters and visualizations.

## 🎯 Project Objectives

- Analyze the distribution of Movies and TV Shows.
- Identify countries contributing the highest number of titles.
- Discover popular genres and directors.
- Understand content ratings and their distribution.
- Explore content release trends over the years.
- Calculate average movie duration.
- Generate meaningful insights through interactive visualizations.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Data analysis and preprocessing |
| Pandas | Data manipulation and cleaning |
| SQL Server | Database management and querying |
| Streamlit | Interactive dashboard development |
| Plotly | Interactive data visualization |
| VS Code | Development environment |

## 📂 Dataset

**Dataset:** Netflix Movies and TV Shows

**Source:** [Netflix Movies and TV Shows – Kaggle](https://www.kaggle.com/datasets/shivamb/netflix-shows)

**Dataset Details:**

- Total Records: 8,807
- Total Features: 12
- Includes information about movies and TV shows.

The dataset contains information such as:

- Show ID
- Type
- Title
- Director
- Cast
- Country
- Date Added
- Release Year
- Rating
- Duration
- Listed In (Genres)
- Description

## ⚙️ Project Workflow

### 1. Data Collection

- Imported the Netflix dataset in CSV format.
- Examined the dataset structure and data types.

### 2. Data Cleaning and Preprocessing

- Identified missing values.
- Handled missing values in relevant columns.
- Checked and handled duplicate records.
- Converted date fields into appropriate formats.
- Prepared the cleaned dataset for analysis.

### 3. SQL Analysis

Used SQL Server to perform analytical queries, including:

- Movies vs TV Shows distribution.
- Top countries by number of titles.
- Most popular genres.
- Top directors.
- Content distribution by release year.
- Ratings distribution.

### 4. Exploratory Data Analysis

Used Python and Pandas to explore patterns and trends in the dataset.

### 5. Dashboard Development

Developed an interactive Streamlit dashboard with Plotly visualizations and dynamic filters.

## 📊 Dashboard Features

### Interactive Filters

- Content Type
- Release Year Range
- Country
- Genre

### Key Performance Indicators (KPIs)

- Total Titles
- Total Movies
- Total TV Shows
- Total Countries
- Average Movie Duration

### Visualizations

- Movies vs TV Shows Distribution
- Top 10 Countries by Content
- Top 10 Genres
- Movie vs TV Show Comparison Over the Years
- Top 10 Directors
- Netflix Content Release Trends
- Content Ratings Distribution

### Automated Content Insights

- Most Popular Genre
- Leading Country
- Most Common Content Rating
- Average Movie Duration

All dashboard metrics, insights, and visualizations respond to the selected filters.

## 📁 Project Structure

```text
Netfix_Content_Analysis/
│
├── data/
│   ├── netflix_titles.csv
│   └── netflix_cleaned.csv
│
├── visualizations/
│   ├── content_distribution.png
│   ├── top_countries.png
│   └── top_genres.png
│
├── app.py
├── netflix_analysis.py
├── netflix_analysis.sql
└── README.md
```

## 🚀 Installation and Execution

### Prerequisites

- Python 3.10 or later
- SQL Server (for running the SQL analysis)
- VS Code or another Python IDE

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### Step 2: Navigate to the Project Directory

```bash
cd Netfix_Content_Analysis
```

### Step 3: Install Dependencies

```bash
pip install pandas streamlit plotly
```

### Step 4: Run the Dashboard

```bash
python -m streamlit run app.py
```

The dashboard will open in your browser.

## 💡 Key Analytical Outcomes

The analysis provides insights into:

- The balance between Movies and TV Shows.
- Countries with the largest content contributions.
- Popular genres across the catalogue.
- Directors with the highest number of listed titles.
- Distribution of content ratings.
- Changes in title release counts across different years.
- Average movie duration.

## 📚 Skills Demonstrated

- Data Cleaning and Preprocessing
- Exploratory Data Analysis (EDA)
- Python Programming
- Pandas Data Manipulation
- SQL Querying
- Data Visualization
- Interactive Dashboard Development
- Analytical Thinking
- Data Storytelling

## 🔮 Future Enhancements

- Deploy the dashboard online using Streamlit Community Cloud.
- Add more advanced analytical visualizations.
- Introduce additional content insights.
- Improve dashboard performance and user experience.

## 👩‍💻 Author

**Krushitha**

B.Tech – Computer Science and Engineering

**Project:** Netflix Content Analysis

---

⭐ If you find this project interesting, consider giving the repository a star!
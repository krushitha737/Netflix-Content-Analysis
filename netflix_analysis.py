
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 1. LOAD THE DATASET
# ==========================================

df = pd.read_csv("data/netflix_titles.csv")

print("First 5 Records:")
print(df.head())

print("\nDataset Information:")
print(df.info())

print("\nNumber of Rows and Columns:")
print(df.shape)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:", df.duplicated().sum())

print("\nContent Type Distribution:")
print(df["type"].value_counts())

print("\nStatistical Summary:")
print(df.describe())


# ==========================================
# 2. DATA CLEANING
# ==========================================

df_clean = df.copy()

# Fill missing categorical values
columns_to_fill = [
    "director",
    "cast",
    "country",
    "rating",
    "duration"
]

for column in columns_to_fill:
    df_clean[column] = df_clean[column].fillna("Unknown")

# Convert date_added into datetime format
df_clean["date_added"] = pd.to_datetime(
    df_clean["date_added"].str.strip(),
    errors="coerce"
)

print("\nMissing Values After Cleaning:")
print(df_clean.isnull().sum())

print("\nUpdated Data Types:")
print(df_clean.dtypes)


# ==========================================
# 3. EXPLORATORY DATA ANALYSIS (EDA)
# ==========================================

# 1. Movies vs TV Shows
print("\nContent Type Distribution:")
print(df_clean["type"].value_counts())

# 2. Top 10 Individual Countries
# Split country combinations into individual countries
countries = (
    df_clean["country"]
    .str.split(", ")
    .explode()
)

countries = countries[countries != "Unknown"]

print("\nTop 10 Countries:")
print(countries.value_counts().head(10))

# 3. Top 10 Genres
genres = df_clean["listed_in"].str.split(", ").explode()

print("\nTop 10 Genres:")
print(genres.value_counts().head(10))

# 4. Top 10 Release Years
print("\nTop 10 Release Years:")
print(df_clean["release_year"].value_counts().head(10))


# ==========================================
# 4. DATA VISUALIZATION
# ==========================================

# ==========================================
# 4. DATA VISUALIZATION - NETFLIX DARK THEME
# ==========================================

# Netflix-inspired theme
BG_COLOR = "#141414"
RED = "#E50914"
LIGHT_RED = "#B20710"
TEXT_COLOR = "#FFFFFF"
GRID_COLOR = "#404040"

plt.rcParams.update({
    "figure.facecolor": BG_COLOR,
    "axes.facecolor": BG_COLOR,
    "text.color": TEXT_COLOR,
    "axes.labelcolor": TEXT_COLOR,
    "xtick.color": TEXT_COLOR,
    "ytick.color": TEXT_COLOR,
    "font.family": "DejaVu Sans"
})


# ------------------------------------------
# 1. MOVIE VS TV SHOW DISTRIBUTION
# ------------------------------------------

content_counts = df_clean["type"].value_counts()

fig, ax = plt.subplots(figsize=(9, 6))

wedges, texts, autotexts = ax.pie(
    content_counts,
    labels=content_counts.index,
    autopct="%1.1f%%",
    startangle=90,
    colors=[RED, "#777777"],
    pctdistance=0.78,
    textprops={"color": TEXT_COLOR, "fontsize": 12},
    wedgeprops={"width": 0.42, "edgecolor": BG_COLOR}
)

for autotext in autotexts:
    autotext.set_fontweight("bold")
    autotext.set_fontsize(13)

ax.text(
    0, 0,
    f"{content_counts.sum():,}\nTOTAL TITLES",
    ha="center",
    va="center",
    color=TEXT_COLOR,
    fontsize=14,
    fontweight="bold"
)

ax.set_title(
    "NETFLIX CONTENT DISTRIBUTION",
    fontsize=17,
    fontweight="bold",
    color=TEXT_COLOR,
    pad=20
)

ax.legend(
    wedges,
    content_counts.index,
    loc="lower center",
    bbox_to_anchor=(0.5, -0.10),
    ncol=2,
    frameon=False,
    labelcolor=TEXT_COLOR
)

plt.tight_layout()
plt.savefig(
    "visualizations/content_distribution.png",
    dpi=300,
    facecolor=BG_COLOR,
    bbox_inches="tight"
)
plt.show()


# ------------------------------------------
# 2. TOP 10 COUNTRIES
# ------------------------------------------

countries = (
    df_clean["country"]
    .str.split(", ")
    .explode()
)

countries = countries[countries != "Unknown"]
top_countries = countries.value_counts().head(10)

fig, ax = plt.subplots(figsize=(11, 7))

bars = ax.barh(
    top_countries.sort_values().index,
    top_countries.sort_values().values,
    color=RED,
    height=0.65
)

ax.bar_label(
    bars,
    fmt="%,.0f",
    padding=8,
    color=TEXT_COLOR,
    fontsize=10
)

ax.set_title(
    "TOP 10 COUNTRIES BY NETFLIX TITLES",
    fontsize=17,
    fontweight="bold",
    color=TEXT_COLOR,
    pad=20
)

ax.set_xlabel("Number of Titles", fontsize=11)
ax.set_ylabel("")

ax.grid(
    axis="x",
    linestyle="--",
    alpha=0.2,
    color=GRID_COLOR
)

ax.set_axisbelow(True)

for spine in ax.spines.values():
    spine.set_visible(False)

ax.tick_params(axis="both", length=0, labelsize=10)
ax.set_xlim(0, top_countries.max() * 1.15)

plt.tight_layout()
plt.savefig(
    "visualizations/top_countries.png",
    dpi=300,
    facecolor=BG_COLOR,
    bbox_inches="tight"
)
plt.show()


# ------------------------------------------
# 3. TOP 10 GENRES
# ------------------------------------------

genres = df_clean["listed_in"].str.split(", ").explode()
top_genres = genres.value_counts().head(10)

fig, ax = plt.subplots(figsize=(11, 7))

sorted_genres = top_genres.sort_values()

bars = ax.barh(
    sorted_genres.index,
    sorted_genres.values,
    color=RED,
    height=0.65
)

ax.bar_label(
    bars,
    fmt="%,.0f",
    padding=8,
    color=TEXT_COLOR,
    fontsize=10
)

ax.set_title(
    "TOP 10 NETFLIX GENRES",
    fontsize=17,
    fontweight="bold",
    color=TEXT_COLOR,
    pad=20
)

ax.set_xlabel("Number of Titles", fontsize=11)
ax.set_ylabel("")

ax.grid(
    axis="x",
    linestyle="--",
    alpha=0.2,
    color=GRID_COLOR
)

ax.set_axisbelow(True)

for spine in ax.spines.values():
    spine.set_visible(False)

ax.tick_params(axis="both", length=0, labelsize=10)
ax.set_xlim(0, top_genres.max() * 1.15)

plt.tight_layout()
plt.savefig(
    "visualizations/top_genres.png",
    dpi=300,
    facecolor=BG_COLOR,
    bbox_inches="tight"
)
plt.show()

print("All three professional visualizations saved successfully!")


# ==========================================
# 5. SAVE CLEANED DATASET
# ==========================================

df_clean.to_csv("data/netflix_cleaned.csv", index=False)

print("\nCleaned dataset saved successfully!")


# ==========================================
# 6. VALIDATE CLEANED CSV FILE
# ==========================================

check_df = pd.read_csv("data/netflix_cleaned.csv")

print("\nCSV VALIDATION")
print("Total rows:", len(check_df))
print("Missing dates:", check_df["date_added"].isna().sum())
print("Missing durations:", check_df["duration"].isna().sum())

print("\nSample Date Values:")
print(
    check_df[
        ["show_id", "title", "date_added"]
    ].head(15)
)

print("\nRows with Missing Dates:")
print(
    check_df[
        check_df["date_added"].isna()
    ][
        ["show_id", "title", "date_added"]
    ].head(15)
)

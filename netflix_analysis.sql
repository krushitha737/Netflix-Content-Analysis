-- =========================================
-- NETFLIX CONTENT ANALYSIS
-- SQL BUSINESS ANALYSIS
-- =========================================

USE NetflixDB;

-- QUESTION 1:
-- Count Movies and TV Shows

SELECT
    type,
    COUNT(*) AS total_titles
FROM NetflixTitles
GROUP BY type;


-- QUESTION 2:
-- Top 10 Countries by Netflix Titles

SELECT TOP 10
    country,
    COUNT(*) AS total_titles
FROM NetflixTitles
WHERE country <> 'Unknown'
GROUP BY country
ORDER BY total_titles DESC;

-- QUESTION 3:
-- Top 10 Netflix Genres

SELECT TOP 10
    LTRIM(RTRIM(value)) AS genre,
    COUNT(*) AS total_titles
FROM NetflixTitles
CROSS APPLY STRING_SPLIT(listed_in, ',')
GROUP BY LTRIM(RTRIM(value))
ORDER BY total_titles DESC;


-- QUESTION 4:
-- Top 10 Release Years

SELECT TOP 10
    release_year,
    COUNT(*) AS total_titles
FROM NetflixTitles
GROUP BY release_year
ORDER BY total_titles DESC;


-- QUESTION 5:
-- Most Common Content Ratings

SELECT
    rating,
    COUNT(*) AS total_titles
FROM NetflixTitles
WHERE rating <> 'Unknown'
  AND rating NOT LIKE '% min'
GROUP BY rating
ORDER BY total_titles DESC;


-- QUESTION 6:
-- Top 10 Directors

SELECT TOP 10
    director,
    COUNT(*) AS total_titles
FROM NetflixTitles
WHERE director <> 'Unknown'
GROUP BY director
ORDER BY total_titles DESC;


-- QUESTION 7:
-- Top 10 Countries for TV Shows

SELECT TOP 10
    country,
    COUNT(*) AS total_tv_shows
FROM NetflixTitles
WHERE type = 'TV Show'
  AND country <> 'Unknown'
GROUP BY country
ORDER BY total_tv_shows DESC;


-- QUESTION 8:
-- Average Movie Duration in Minutes

SELECT
    AVG(
        CAST(REPLACE(duration, ' min', '') AS FLOAT)
    ) AS average_movie_duration
FROM NetflixTitles
WHERE type = 'Movie'
  AND duration LIKE '% min';


-- QUESTION 9:
-- Top 10 Years for Movie Releases

SELECT TOP 10
    release_year,
    COUNT(*) AS total_movies
FROM NetflixTitles
WHERE type = 'Movie'
GROUP BY release_year
ORDER BY total_movies DESC;


-- QUESTION 10:
-- Top 10 Directors by Movie Count

SELECT TOP 10
    director,
    COUNT(*) AS total_movies
FROM NetflixTitles
WHERE type = 'Movie'
  AND director <> 'Unknown'
GROUP BY director
ORDER BY total_movies DESC;

CREATE DATABASE sportradar_db;
USE sportradar_db;

CREATE USER 'sports_user'@'localhost' IDENTIFIED BY 'Horse1@@';
GRANT ALL PRIVILEGES ON sportradar_db.* TO 'sports_user'@'localhost';
FLUSH PRIVILEGES;

USE sportradar_db;

-- 1️. Categories Table
CREATE TABLE Categories (
  category_id VARCHAR(50) PRIMARY KEY,
  category_name VARCHAR(100)
);

-- 2️. Competitions Table
CREATE TABLE Competitions (
  competition_id VARCHAR(50) PRIMARY KEY,
  competition_name VARCHAR(100),
  category_id VARCHAR(50),
  type VARCHAR(50),
  gender VARCHAR(20),
  FOREIGN KEY (category_id) REFERENCES Categories(category_id)
);

-- 3️. Complexes Table
CREATE TABLE Complexes (
  complex_id VARCHAR(50) PRIMARY KEY,
  complex_name VARCHAR(100)
);

-- 4️. Venues Table
CREATE TABLE Venues (
  venue_id VARCHAR(50) PRIMARY KEY,
  venue_name VARCHAR(100),
  city_name VARCHAR(100),
  country_name VARCHAR(100),
  timezone VARCHAR(50),
  complex_id VARCHAR(50),
  FOREIGN KEY (complex_id) REFERENCES Complexes(complex_id)
);

-- 5️. Competitors Table
CREATE TABLE Competitors (
  competitor_id VARCHAR(50) PRIMARY KEY,
  name VARCHAR(100),
  country VARCHAR(100),
  country_code VARCHAR(10)
);

-- 6️. Competitor Rankings Table
CREATE TABLE Competitor_Rankings (
  rank_id INT AUTO_INCREMENT PRIMARY KEY,
  competitor_id VARCHAR(50),
  rank_position INT,
  movement INT,
  points DECIMAL(10,2),
  FOREIGN KEY (competitor_id) REFERENCES Competitors(competitor_id)
);

USE sportradar_db;

SELECT * FROM Categories;
SELECT * FROM Competitions;
SELECT * FROM Complexes;
SELECT * FROM Venues;
SELECT * FROM Competitors;
SELECT * FROM Competitor_Rankings;

-- List all competitions with category names-- 
SELECT 
    c.competition_id,
    c.competition_name,
    c.type,
    c.gender,
    cat.category_name
FROM competitions c
JOIN categories cat ON c.category_id = cat.category_id;

-- Count the number of competitions in each category--  
SELECT 
    cat.category_name,
    COUNT(c.competition_id) AS total_competitions
FROM competitions c
JOIN categories cat ON c.category_id = cat.category_id
GROUP BY cat.category_name
ORDER BY total_competitions DESC;

-- Find competitions of type ‘doubles’--
SELECT 
    competition_id,
    competition_name,
    type,
    gender
FROM competitions
WHERE type = 'doubles';
  
-- Get competitions in a specific category (e.g., ITF Men)-- 
SELECT 
    c.competition_name,
    c.type,
    c.gender
FROM competitions c
JOIN categories cat ON c.category_id = cat.category_id
WHERE cat.category_name = 'ITF Men';

ALTER TABLE competitions ADD COLUMN parent_id VARCHAR(50);

-- Identify parent competitions and their sub-competitions--
SELECT 
    p.competition_id AS parent_competition_id,
    p.competition_name AS parent_competition_name,
    c.competition_id AS sub_competition_id,
    c.competition_name AS sub_competition_name
FROM 
    Competitions c
JOIN 
    Competitions p
    ON c.parent_id = p.competition_id
ORDER BY 
    p.competition_name, c.competition_name;


-- Analyze distribution of competition types by category--  
SELECT 
    cat.category_name,
    c.type,
    COUNT(c.competition_id) AS total_competitions
FROM competitions c
JOIN categories cat ON c.category_id = cat.category_id
GROUP BY cat.category_name, c.type
ORDER BY cat.category_name;

-- List all top-level competitions (no parent). --
SELECT 
    competition_id,
    competition_name,
    category_id,
    type,
    gender
FROM 
    Competitions
WHERE 
    parent_id IS NULL;


-- List all venues along with their associated complex names-- 
SELECT 
    v.venue_id,
    v.venue_name,
    v.city_name,
    v.country_name,
    v.timezone,
    c.complex_name
FROM 
    Venues v
JOIN 
    Complexes c 
    ON v.complex_id = c.complex_id
ORDER BY 
    c.complex_name, v.venue_name;

-- Count the number of venues in each complex--  
SELECT 
    c.complex_name,
    COUNT(v.venue_id) AS venue_count
FROM 
    Complexes c
LEFT JOIN 
    Venues v 
    ON c.complex_id = v.complex_id
GROUP BY 
    c.complex_name
ORDER BY 
    venue_count DESC;

-- Get details of venues in a specific country (e.g., 'CHILE')--  
SELECT 
    venue_id,
    venue_name,
    city_name,
    country_name,
    timezone
FROM 
    Venues
WHERE 
    country_name = 'CHILE';

-- Identify all venues with their timezones--  
SELECT 
    venue_id,
    venue_name,
    country_name,
    timezone
FROM 
    Venues
ORDER BY 
    country_name, timezone;

-- Find complexes with more than one venue--  
SELECT 
    c.complex_name,
    COUNT(v.venue_id) AS venue_count
FROM 
    Complexes c
JOIN 
    Venues v 
    ON c.complex_id = v.complex_id
GROUP BY 
    c.complex_name
HAVING 
    COUNT(v.venue_id) > 1;

-- List venues grouped by country -- 
SELECT 
    country_name,
    COUNT(venue_id) AS total_venues
FROM 
    Venues
GROUP BY 
    country_name
ORDER BY 
    total_venues DESC;

-- Find all venues for a specific complex--
SELECT 
    v.venue_id,
    v.venue_name,
    v.city_name,
    v.country_name,
    v.timezone
FROM 
    Venues v
JOIN 
    Complexes c 
    ON v.complex_id = c.complex_id
WHERE 
    c.complex_name = 'Nacional';
  
-- Get all competitors with their rank and points--  
SELECT 
    c.competitor_id,
    c.name AS competitor_name,
    c.country,
    cr.rank_position,
    cr.points
FROM 
    Competitor_Rankings cr
JOIN 
    Competitors c 
    ON cr.competitor_id = c.competitor_id
ORDER BY 
    cr.rank_position ASC;

-- Find competitors ranked in the top 5--
SELECT 
    c.competitor_id,
    c.name AS competitor_name,
    c.country,
    cr.rank_position,
    cr.points
FROM 
    Competitor_Rankings cr
JOIN 
    Competitors c 
    ON cr.competitor_id = c.competitor_id
WHERE 
    cr.rank_position <= 5
ORDER BY 
    cr.rank_position ASC;
  
-- List competitors with no rank movement (stable rank)--
SELECT 
    c.competitor_id,
    c.name AS competitor_name,
    cr.rank_position,
    cr.movement,
    cr.points
FROM 
    Competitor_Rankings cr
JOIN 
    Competitors c 
    ON cr.competitor_id = c.competitor_id
WHERE 
    cr.movement = 0
ORDER BY 
    cr.rank_position ASC;
    
-- Get the total points of competitors from a specific country (e.g., ‘Great Britain’)--
SELECT 
    c.country,
    SUM(cr.points) AS total_points
FROM 
    Competitor_Rankings cr
JOIN 
    Competitors c 
    ON cr.competitor_id = c.competitor_id
WHERE 
    c.country = 'Great Britain'
GROUP BY 
    c.country;

-- Count competitors per country--
SELECT 
    c.country,
    COUNT(c.competitor_id) AS total_competitors
FROM 
    Competitors c
GROUP BY 
    c.country
ORDER BY 
    total_competitors DESC;
        
-- Find competitors with the highest points in the current week--
SELECT 
    c.competitor_id,
    c.name AS competitor_name,
    c.country,
    cr.rank_position,
    cr.points
FROM 
    Competitor_Rankings cr
JOIN 
    Competitors c 
    ON cr.competitor_id = c.competitor_id
WHERE 
    cr.points = (
        SELECT MAX(points) 
        FROM Competitor_Rankings
    );
      
-- Creation of tables for the FootballHub database

-- Table of countries (for nationalities and locations)
CREATE TABLE countries (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- Table of positions (to standardize player positions)
CREATE TABLE positions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- Table of event types (for goals, assists, cards, etc.)
CREATE TABLE event_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- Table of stadiums (where matches are held)
CREATE TABLE stadiums (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    country_id INTEGER NOT NULL REFERENCES countries(id)
);

-- Table of teams
CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    nickname VARCHAR(50),
    city VARCHAR(100),
    country_id INTEGER NOT NULL REFERENCES countries(id),
    founding_date DATE
);

-- Table of players
CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    birth_date DATE,
    country_id INTEGER NOT NULL REFERENCES countries(id),
    position_id INTEGER NOT NULL REFERENCES positions(id),
    team_id INTEGER REFERENCES teams(id)
);

-- Table of championships
CREATE TABLE championships (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country_id INTEGER REFERENCES countries(id),
    type VARCHAR(50),
    season VARCHAR(20)
);

-- Table of matches
CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    home_team_id INTEGER NOT NULL REFERENCES teams(id),
    away_team_id INTEGER NOT NULL REFERENCES teams(id),
    championship_id INTEGER NOT NULL REFERENCES championships(id),
    date DATE NOT NULL,
    stadium_id INTEGER NOT NULL REFERENCES stadiums(id),
    home_score INTEGER,
    away_score INTEGER,
    CONSTRAINT chk_different_teams CHECK (home_team_id <> away_team_id)
);

-- Table of match events (goals, assists, cards, etc.)
CREATE TABLE match_events (
    id SERIAL PRIMARY KEY,
    match_id INTEGER NOT NULL REFERENCES matches(id),
    player_id INTEGER NOT NULL REFERENCES players(id),
    event_type_id INTEGER NOT NULL REFERENCES event_types(id),
    minute INTEGER NOT NULL
);

-- Table of substitutions
CREATE TABLE substitutions (
    id SERIAL PRIMARY KEY,
    match_id INTEGER NOT NULL REFERENCES matches(id),
    player_out_id INTEGER NOT NULL REFERENCES players(id),
    player_in_id INTEGER NOT NULL REFERENCES players(id),
    minute INTEGER NOT NULL,
    CONSTRAINT chk_different_players CHECK (player_out_id <> player_in_id)
);

-- Table of lineups (players who started the match)
CREATE TABLE lineups (
    id SERIAL PRIMARY KEY,
    match_id INTEGER NOT NULL REFERENCES matches(id),
    team_id INTEGER NOT NULL REFERENCES teams(id),
    player_id INTEGER NOT NULL REFERENCES players(id),
    position VARCHAR(50)
);

-- Adding constraint to avoid duplicates in lineups
ALTER TABLE lineups ADD CONSTRAINT unique_lineup UNIQUE (match_id, team_id, player_id);

-- Table of championship participations (teams participating in a championship)
CREATE TABLE championship_participations (
    id SERIAL PRIMARY KEY,
    championship_id INTEGER NOT NULL REFERENCES championships(id),
    team_id INTEGER NOT NULL REFERENCES teams(id),
    season VARCHAR(20),
    CONSTRAINT unique_participation UNIQUE (championship_id, team_id, season)
);
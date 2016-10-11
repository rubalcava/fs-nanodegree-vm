-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- If there's already a database, delete it
DROP DATABASE IF EXISTS tournament;
DROP VIEW IF EXISTS won_matches;
DROP VIEW IF EXISTS lost_matches;
DROP VIEW IF EXISTS number_of_matches;

CREATE DATABASE tournament;
-- Load the database
\c tournament;

CREATE TABLE players(id serial primary key, name text, wins integer DEFAULT 0);

CREATE TABLE matches(winner integer primary key REFERENCES players,
                     loser integer REFERENCES players);

CREATE VIEW won_matches AS SELECT id, wins from players ORDER BY id;

CREATE VIEW lost_matches AS SELECT players.id as id, count(matches.loser) as losses from players LEFT JOIN matches ON (players.id = matches.loser) GROUP BY players.id ORDER BY players;

CREATE VIEW number_of_matches as SELECT won_matches.id, (won_matches.wins + lost_matches.losses) AS matches FROM won_matches JOIN lost_matches ON (won_matches.id = lost_matches.id) ORDER BY won_matches.id;

CREATE VIEW player_standings as SELECT players.id, players.name, players.wins, number_of_matches.matches as matches FROM players LEFT JOIN number_of_matches ON (players.id = number_of_matches.id) GROUP BY players.id, number_of_matches.matches ORDER BY players.wins;

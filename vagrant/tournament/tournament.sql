-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- If there's already a database, delete it
DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;
-- Load the database
\c tournament;

CREATE TABLE players(id serial primary key, name text, wins integer, matches integer);

CREATE TABLE matches(winner integer, loser integer);

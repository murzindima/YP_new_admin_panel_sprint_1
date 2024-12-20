CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
    genre_id uuid REFERENCES content.genre(id),
    film_work_id uuid REFERENCES content.film_work(id),
    created timestamp with time zone,
    UNIQUE (genre_id, film_work_id)
);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    person_id uuid REFERENCES content.person(id) NOT NULL,
    film_work_id uuid REFERENCES content.film_work(id) NOT NULL,
    role TEXT NOT NULL,
    created timestamp with time zone,
    UNIQUE (person_id, film_work_id, role)
);

CREATE INDEX idx_film_work_title ON content.film_work(title);
CREATE INDEX idx_film_work_creation_date ON content.film_work(creation_date);
CREATE INDEX idx_film_work_rating ON content.film_work(rating);
CREATE INDEX idx_person_full_name ON content.person(full_name);

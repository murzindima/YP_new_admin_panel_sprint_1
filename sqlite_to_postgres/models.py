from uuid import uuid4
from dataclasses import dataclass


@dataclass
class FilmWork:
    id: uuid4
    title: str
    description: str
    creation_date: str
    rating: float
    type: str
    created_at: str
    updated_at: str


@dataclass
class Genre:
    id: uuid4
    name: str
    description: str
    created_at: str
    updated_at: str


@dataclass
class Person:
    id: uuid4
    full_name: str
    created_at: str
    updated_at: str


@dataclass
class GenreFilmWork:
    id: uuid4
    film_work_id: str
    genre_id: str
    created_at: str


@dataclass
class PersonFilmWork:
    id: uuid4
    film_work_id: str
    person_id: str
    role: str
    created_at: str

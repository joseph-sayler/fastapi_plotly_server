from typing import Dict, List, Optional, Union
from tmdbv3api import TMDb, Movie, Genre
import pandas as pd


def get_popular_movies(
    pages: int = 1, genres: Optional[List[Dict[str, Union[int, str]]]] = None
) -> List[Dict[str, Union[int, str]]]:
    """Fetch a list of popular movies from TMDb. The number of movies depends on the value supplied to the `pages` parameter

    :param pages: number of `pages` to fetch from API, defaults to 1
    :type pages: int, optional
    :param genres: group of genres, with `id` is an integer representing the value from API and `name` as a string indicating the name of the genre, defaults to None
    :type genres: Optional[List[Dict[str, Union[int, str]]]], optional
    :return: group of movies containing properties such as `TMDb id`, `title`, `release date`, `popularity`, `overview`, etc.
    :rtype: List[Dict[str, Union[int, str]]]
    """
    p = pages if pages else 1
    popular_movies = [
        [
            format_movie_listing(data=m, genre_list=genres)
            for m in movie.popular(page=x + 1)
        ]
        for x in range(p)
    ]
    pm_flat = [item for sublist in popular_movies for item in sublist]
    return pm_flat


def format_movie_listing(
    data: Dict[str, Union[int, str]],
    genre_list: Optional[List[Dict[str, Union[int, str]]]] = None,
) -> Dict[str, Union[int, str]]:
    """Format a movie listing obtained from TMDb API. Converts the genre id from TMDb to an actual string value

    :param data: movie data from TMDb API
    :type data: Dict[str, Union[int, str]]
    :param genre_list: genre data indicating the `genre id` and `genre name` from TMDb
    :type genre_list: List
    :return: TMDb data compiled into categories
    :rtype: Dict[str, Union[int, str]]
    """
    return {
        "id": data.id,
        "title": data.title,
        "released": data.release_date,
        "popularity": data.popularity,
        "average_stars": data.vote_average,
        "total_votes": data.vote_count,
        "genres": process_genres(d=data.genre_ids, g=genre_list)
        if genre_list
        else data.genre_ids,
        "overview": data.overview,
    }


def process_genres(d: List[int], g: List[Dict[str, Union[int, str]]]) -> List[str]:
    """Process the genre from a numeric ID to a string value

    :param d: data to convert
    :type d: List[int]
    :param g: genres with ID and name
    :type g: List[Dict[str, Union[int, str]]]
    :return: genre IDs converted to string values
    :rtype: List[str]
    """
    output = []
    # flatten list of dicts to one dict where id is key and name is value
    proc_list = {str(x["id"]): x["name"] for x in g}
    for n in d:
        genre = proc_list.get(str(n))
        output.append(genre if genre else "Unknown")
    return output


tmdbobj = TMDb()

TMDb.api_key = "6f15568d9aa3d15d0261a5454578c28b"
tmdbobj.language = "en"
tmdbobj.debug = True

movie = Movie()

# current list of genres as per 2022/08/12
# call new list from API if this list out of date
g_list = [
    {"id": 28, "name": "Action"},
    {"id": 12, "name": "Adventure"},
    {"id": 16, "name": "Animation"},
    {"id": 35, "name": "Comedy"},
    {"id": 80, "name": "Crime"},
    {"id": 99, "name": "Documentary"},
    {"id": 18, "name": "Drama"},
    {"id": 10751, "name": "Family"},
    {"id": 14, "name": "Fantasy"},
    {"id": 36, "name": "History"},
    {"id": 27, "name": "Horror"},
    {"id": 10402, "name": "Music"},
    {"id": 9648, "name": "Mystery"},
    {"id": 10749, "name": "Romance"},
    {"id": 878, "name": "Science Fiction"},
    {"id": 10770, "name": "TV Movie"},
    {"id": 53, "name": "Thriller"},
    {"id": 10752, "name": "War"},
    {"id": 37, "name": "Western"},
]
# g_list = Genre().movie_list()
pages = 29

p = get_popular_movies(pages=pages, genres=g_list)

data = pd.DataFrame(p)
data.to_csv(path_or_buf="../data/popular_movies_data.csv", index=False)

""" Get full movie details from the OMDB API """
import os

import requests
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv('OMDB_API_KEY')

BASE_URL = f'http://www.omdbapi.com/?apikey={API_KEY}&'


def get_movie_by_title(title: str) -> dict:
    """ Get a movie by its title """
    url = f'{BASE_URL}t={title}'
    response = requests.get(url)
    if response.status_code == 200:
        return {
            'title': response.json()['Title'],
            'year': response.json()['Year'],
            'poster': response.json()['Poster'],
            'directors': [director.strip() for director in response.json()['Director'].split(',')],
        }
    return {}



if __name__ == '__main__':
    get_movie_by_title('The Matrix')
import os

from openai import OpenAI
from dotenv import load_dotenv

from models.user import User

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(
    api_key=OPENAI_API_KEY
)

SYSTEM_PROMPT = ('You add AI movie recommendation\n'
                 'your input is a list of movies a user watched with their rating\n'
                 'and you should give a movie recommendation based on that list.\n'
                 'Your output should just be the name of the movie you recommend.')


def get_recommended_movie_name(user: User) -> str:
    """ Get a recommended movie name """
    user_movies = []

    if user.movies:
        for user_movie in user.movies:
            user_movies.append({
                'title': user_movie.movie.title,
                'rating': user_movie.rating
            })

        prompt = f'User has watched the following movies and rated them:\n'
        for user_movie in user_movies:
            prompt += f'```{user_movie["title"]}``` - {user_movie["rating"]}/10\n'
    else:
        prompt = 'User has not watched any movies yet. Recommend a movie, that is generally well received.'

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': prompt}
        ]
    )

    return response.choices[0].message.content
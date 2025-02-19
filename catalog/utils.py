import requests

def get_movie_details(tmdb_id):
    api_key = '746380f35f478dc2fa82a6825e3d5446'
    url = f'https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={api_key}'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None
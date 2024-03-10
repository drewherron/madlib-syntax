import requests
import os

def fetch_gif_url(query):
    api_key = os.getenv('GIPHY_API_KEY')
    base_url = 'https://api.giphy.com/v1/gifs/search'
    params = {
        'api_key': api_key,
        'q': query,
        'limit': 1,
        'rating': 'pg'
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['data']:
            downsized = data['data'][0]['images']['downsized']['url']
            return downsized
    return None


if __name__ == "__main__":

    test_query = "funny cat"
    gif_url = fetch_gif_url(test_query)
    if gif_url:
        print("GIF URL:", gif_url)
    else:
        print("No GIF found for the query.")
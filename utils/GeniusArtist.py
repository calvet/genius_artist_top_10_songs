import os
import json
import uuid
import requests
import unidecode
from utils.RedisCache import RedisCache
import requests.packages.urllib3.exceptions

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


class GeniusArtist:
    def __init__(self):
        self.genius_access_token = os.getenv('GENIUS_ACCESS_TOKEN')

        self.redis_cache = RedisCache()

    def get_artist_top_songs(self, artist_input_name, cache):
        if cache:
            artist_cache = self.redis_cache.get_artist(artist_input_name)

            if artist_cache is not None:
                print('Está utilizando cache!')
                artist_cache = artist_cache.decode('utf-8')
                artist_cache = str(artist_cache).replace("'", '"')
                artist_cache = json.loads(artist_cache)

                return True, artist_cache

        print('Nao está utilizando cache!')

        song_status, artist_data = self.get_artist_songs(artist_input_name, 10, 1)

        if not song_status:
            return song_status, artist_data

        return song_status, artist_data

    def get_artist_songs(self, search_term, quantity, page):
        artists_search_list = {}

        songs_dict = {}
        songs_list = []

        artist_dict = {}

        try:
            get_artist = requests.get(
                url=f'http://api.genius.com/search?q={search_term}',
                headers={
                    'Authorization': f'Bearer {self.genius_access_token}'
                },
                timeout=30,
                verify=False
            )

            artist_data = get_artist.json()

            if artist_data['meta']['status'] != 200:
                return False, artist_dict

            for hit in artist_data['response']['hits']:
                artist_hist_id = hit['result']['primary_artist']['id']
                artist_hit_name = hit['result']['primary_artist']['name']

                if artist_hist_id not in artists_search_list:
                    artists_search_list[artist_hist_id] = {
                        'artist_id': artist_hist_id,
                        'artist_name': artist_hit_name,
                        'occurrences': 1
                    }
                else:
                    artists_search_list[artist_hist_id]['occurrences'] += 1

            get_artist_most_occurrences = max(artists_search_list, key=lambda item: artists_search_list[item]['occurrences'])

            artist_dict['transaction_uuid'] = str(uuid.uuid4())
            artist_dict['artist_id'] = artists_search_list[get_artist_most_occurrences]['artist_id']
            artist_dict['artist_name'] = artists_search_list[get_artist_most_occurrences]['artist_name']
            artist_dict['search_term'] = search_term

            get_artist_songs = requests.get(
                url=f'http://api.genius.com/artists/{get_artist_most_occurrences}/songs',
                params={'sort': 'popularity', 'per_page': str(quantity), 'page': str(page)},
                headers={
                    'Authorization': f'Bearer {self.genius_access_token}'
                },
                timeout=30,
                verify=False
            )

            artist_songs_data = get_artist_songs.json()

            if artist_songs_data['meta']['status'] != 200:
                return False, artist_dict

            for song in artist_songs_data['response']['songs']:
                song_id = song['id']
                song_name = song['full_title']

                if song_id not in songs_dict:
                    songs_dict[song_id] = {
                        'song_id': song_id,
                        'song_name': unidecode.unidecode(song_name)
                    }

                    songs_list.append(unidecode.unidecode(song_name))

            artist_dict['song_list'] = songs_list

            self.redis_cache.set_artist(search_term, artist_dict)

            return True, artist_dict
        except Exception as e:
            print(e)

            return False, artist_dict

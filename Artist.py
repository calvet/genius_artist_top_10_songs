import os
import requests
import unidecode
import requests.packages.urllib3.exceptions

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


class Artist:
    def __init__(self):
        self.genius_access_token = os.getenv('GENIUS_ACCESS_TOKEN')

    def get_artist_id(self, artist_name):
        try:
            get_artirst = requests.get(
                url=f'http://api.genius.com/search?q={artist_name}',
                headers={
                    'Authorization': f'Bearer {self.genius_access_token}'
                },
                timeout=30,
                verify=False
            )

            artist_data = get_artirst.json()

            artists_list = {}

            if artist_data['meta']['status'] != 200:
                return False, -1

            for hit in artist_data['response']['hits']:
                artist_id = hit['result']['primary_artist']['id']

                if artist_id not in artists_list:
                    artist_dict = {
                        # 'transaction_id': uuid4(),
                        'artist_name': artist_name,
                        'artist_id': artist_id,
                        'occurrences': 1
                    }

                    artists_list[artist_id] = artist_dict
                else:
                    artists_list[artist_id]['occurrences'] += 1

            get_artist_most_occurrences = max(artists_list, key=lambda item: artists_list[item]['occurrences'])

            print(get_artist_most_occurrences)

            return True, get_artist_most_occurrences
        except Exception as e:
            print(e)

            return False, -1

    def get_artist_top_songs(self, artist_id, quantity):
        songs_list = {}

        try:
            get_artist_popular_songs = requests.get(
                url=f'http://api.genius.com/artists/{artist_id}/songs',
                params={'sort': 'popularity', 'per_page': str(quantity), 'page': '1'},
                headers={
                    'Authorization': f'Bearer {self.genius_access_token}'
                },
                timeout=30,
                verify=False
            )

            artist_popular_songs_data = get_artist_popular_songs.json()

            if artist_popular_songs_data['meta']['status'] != 200:
                return False, songs_list

            for song in artist_popular_songs_data['response']['songs']:
                song_id = song['id']
                song_name = song['full_title']

                if song_id not in songs_list:
                    song_dict = {
                        # 'transaction_id': uuid4(),
                        'artist_id': artist_id,
                        'song_name': unidecode.unidecode(song_name),
                        'song_id': song_id
                    }

                    songs_list[song_id] = song_dict

            return True, songs_list
        except Exception as e:
            print(e)

            return False, songs_list

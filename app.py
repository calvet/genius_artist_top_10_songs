import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from utils.GeniusArtist import GeniusArtist

load_dotenv()

app = Flask(__name__)

GENIUS_ACCESS_TOKEN = os.getenv('GENIUS_ACCESS_TOKEN')

artist = GeniusArtist()


@app.route('/api/v1/get_artist_top_songs/<artist_name>')
def get_artist_top_songs(artist_name):
    try:
        artist_name = artist_name.strip()

        if len(artist_name) < 3 or len(artist_name) > 30:
            raise Exception('O nome pesquisado e invalido! [minimo 3, maximo 30 caracteres]')

        cache_param = request.args.get('cache')

        cache = False if cache_param is not None and cache_param == 'False' else True

        status, artist_data = artist.get_artist_top_songs(artist_name, cache)

        if not status:
            raise Exception('Nao foi possivel encontrar musicas deste artista!')

        return jsonify(
            {
                'status': 'success',
                'search_term': artist_name,
                'message': f'Foram encontrados as top {len(artist_data["song_list"])} musicas deste artista!',
                'artist_name': artist_data['artist_name'],
                'songs_list': artist_data['song_list']
            }
        )
    except Exception as e:
        return jsonify(
            {
                'status': 'error',
                'search_term': artist_name,
                'message': str(e),
                'artist_name': None,
                'songs_list': []
            }
        )


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)

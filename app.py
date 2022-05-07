import os

from uuid import uuid4
from Artist import Artist
from flask import Flask, request, jsonify


app = Flask(__name__)

GENIUS_ACCESS_TOKEN = os.getenv('GENIUS_ACCESS_TOKEN')


artist = Artist()


@app.route('/api/v1/get_artist_top_songs/<artist_name>/<quantity>')
def get_artist_top_songs(artist_name, quantity):
    artist_name = artist_name.strip()
    # quantity = int()

    # cache = request.args.get('cache')

    if not quantity.isdigit() or 1 > int(quantity) > 100:
        return jsonify(
            {
                'status': 'error',
                'message': 'Quantidade inválida de musicas! (minimo 1, maximo 100)',
                'songs_list': []
            }
        )

    if len(artist_name) < 3:
        return jsonify(
            {
                'status': 'error',
                'message': 'Nome de artista inválido! (minimo 3 caracteres)',
                'songs_list': []
            }
        )

    # if cache:

    status, artist_id = artist.get_artist_id(artist_name)

    if not status:
        return jsonify(
            {
                'status': 'error',
                'message': 'Não foi possível encontrar este artista!',
                'songs_list': []
            }
        )
    else:
        status, song_list = artist.get_artist_top_songs(artist_id, quantity)

        if not status:
            return jsonify(
                {
                    'status': 'error',
                    'message': 'Não foi possível encontrar musicas deste artista!',
                    'songs_list': []
                }
            )
        else:
            return jsonify(
                {
                    'status': 'success',
                    'message': f'Foi encontrado as top {len(song_list)} musicas deste artista!',
                    'songs_list': song_list
                }
            )


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5050)

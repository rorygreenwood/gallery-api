import json
import urllib.request

from flask import Flask, send_from_directory

# Filepaths
_ARTISTS_FILEPATH = 'artists.json'
_ARTWORKS_FILEPATH = 'artworks.json'
_SETTINGS_FILEPATH = 'settings.json'

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/api/playlist', methods=['GET'])
def playlist():
    """Reads settings to gather criteria, and then searches for artworks"""
    settings = json.load(open(_SETTINGS_FILEPATH))
    j_artists = json.loads(open(_ARTISTS_FILEPATH).read())
    j_artworks = json.loads(open(_ARTWORKS_FILEPATH).read())

    filters = settings['filters']
    filtered_artists = []
    outputs = []

    # Top priority is artists, it is the most specific
    if filters.get('artists'):
        for artist in j_artists:
            if artist['artist_id'] in filters['artists']:
                filtered_artists.append(artist)

    # If no artists, go by country
    elif filters.get('countries'):
        j_artists = json.loads(open(_ARTWORKS_FILEPATH).read())
        for artist in j_artists:
            if artist['nationality'] in filters['nationalities']:
                filtered_artists.append(artist)

    # Genre is the broadest filter, if nothing else, select this
    elif filters.get('tags'):
        for artist in j_artists:
            tags = artist['tags']
            for tag in tags:
                if tag in filters['tags']:
                    filtered_artists.append(artist)
    else:
        return {'err': 'no filters supplied'}

    for artist in filtered_artists:
        for artwork in j_artworks:
            if artwork['artist_id'] == artist['artist_id']:
                outputs.append(artwork)

    return outputs


@app.route('/api/artists', methods=['GET'])
def artists():
    with open(_ARTISTS_FILEPATH) as json_file:
        artists = json.load(json_file)
    return artists

@app.route('/api/artworks', methods=['GET'])
def artworks():
    with open(_ARTWORKS_FILEPATH) as json_file:
        artworks = json.load(json_file)
    return artworks

@app.route('/admin/edit', methods=['POST'])
def edit():
    pass

@app.route('/api/download/<path:filename>', methods=['GET'])
def get_image(filename):
    try:
        return send_from_directory(directory='gallery',
                                   path=filename,
                                   as_attachment=False)
    except FileNotFoundError:
        return {'File not found'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

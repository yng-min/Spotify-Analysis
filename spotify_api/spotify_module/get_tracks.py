from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import traceback
import json

with open(r"./spotify_api/config.json", "rt", encoding="UTF8") as configJson:
	config = json.load(configJson)


def getTracks(url: str):
	"""
	Spotify의 트랙 데이터를 요청하는 함수

	매개변수:
		- url: 트랙 URL
	"""
	try:
		if url.find("https://") >= 0:
			uri = "spotify:track:" + url.split("track/")[1].split("?si=")[0]
		else:
			uri = url

		client_credentials_manager = SpotifyClientCredentials(
			client_id=config['client_id'],
			client_secret=config['client_secret']
		)
		sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
		trackData = sp.track(uri)

		track_id = trackData['id']
		track_name = trackData['name']
		track_artists = []
		for i in range(len(trackData['artists'])):
			track_artists.append({
				"id": trackData['artists'][i]['id'],
				"name": trackData['artists'][i]['name']
			})
		track_popularity = trackData['popularity']
		track_explicit = trackData['explicit']
		track_preview_url = trackData['preview_url']
		album_id = trackData['album']['id']
		album_name = trackData['album']['name']
		album_image = trackData['album']['images'][0]['url']
		album_release_date = trackData['album']['release_date']

		data = {
			"trackInfo": {
				"id": track_id,
				"name": track_name
			},
			"trackDetails": {
				"popularity": track_popularity,
				"explicit": track_explicit,
				"preview_url": track_preview_url
			},
			"albumInfo": {
				"id": album_id,
				"name": album_name,
				"image": album_image,
				"release_date": album_release_date
			},
			"artistInfo": track_artists,
		}
		return { "error": False, "code": "SUCCESS", "message": "성공적으로 데이터를 불러왔습니다.", "data": data }

	except Exception as error:
		return { "error": True, "code": "UNKNOWN", "message": f"알 수 없는 오류가 발생했습니다.\n{error}", "error_detail": traceback.format_exc(), "data": None }

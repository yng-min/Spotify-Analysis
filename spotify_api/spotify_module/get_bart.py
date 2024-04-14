from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import traceback


def getBart(reco_type: int, reco_str: str):
	"""
	Spotify의 BART AI에게 음악 추천을 요청하는 함수

	reco_type: 추천 타입(0: 아티스트 | 1: 트랙 | 2: 장르)
	reco_str: 추천 받을 요소
	"""
	try:
		client_credentials_manager = SpotifyClientCredentials(
			client_id="7c8e50dae33c41c88e48909166bef20e",
			client_secret="4fb5615b21b544edb5f647ab68dabcbd"
		)
		sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

		bartData = {}
		if reco_type == 0:
			if reco_str.find("spotify:artist:") >= 0:
				artist = reco_str.split("artist:")[1]
			elif reco_str.find("https://") >= 0:
				artist = reco_str.split("artist/")[1]
			else:
				results = sp.search(q="artist:" + reco_str, type="artist")
				artist = results['artists']['items'][0]['id']
			bartData = sp.recommendations(seed_artists=[artist], limit=10)

		elif reco_type == 1:
			if reco_str.find("https://") >= 0:
				track = "spotify:track:" + reco_str.split("track/")[1].split("?si=")[0]
			else:
				track = reco_str
			bartData = sp.recommendations(seed_tracks=[track], limit=10)

		elif reco_type == 2:
			genre = reco_type.split(", ")
			bartData = sp.recommendations(seed_genres=genre, limit=10)

		track_id = []
		track_name = []
		track_track_number = []
		track_popularity = []
		track_durationMs = []
		track_explicit = []
		track_preview_url = []
		album_id = []
		album_name = []
		album_image = []
		album_totalTracks = []
		album_release_date = []
		artists_id = []
		artists_name = []
		for i in range(len(bartData['tracks'])):
			track_id.append(bartData['tracks'][i]['id'])
			track_name.append(bartData['tracks'][i]['name'])
			track_track_number.append(bartData['tracks'][i]['track_number'])
			track_popularity.append(bartData['tracks'][i]['popularity'])
			track_durationMs.append(bartData['tracks'][i]['duration_ms'])
			track_explicit.append(bartData['tracks'][i]['explicit'])
			track_preview_url.append(bartData['tracks'][i]['preview_url'])
			album_id.append(bartData['tracks'][i]['album']['id'])
			album_name.append(bartData['tracks'][i]['album']['name'])
			album_image.append(bartData['tracks'][i]['album']['images'][0]['url'])
			album_totalTracks.append(bartData['tracks'][i]['album']['total_tracks'])
			album_release_date.append(bartData['tracks'][i]['album']['release_date'])
			artist_id, artist_name = "", ""
			for j in range(len(bartData['tracks'][i]['artists'])):
				artist_id += f"{bartData['tracks'][i]['artists'][j]['id']};; "
				artist_name += f"{bartData['tracks'][i]['artists'][j]['name']};; "
			artists_id.append(artist_id[:-3])
			artists_name.append(artist_name[:-3])

		data = {
			"trackInfo": {
				"id": track_id,
				"name": track_name,
				"track_number": track_track_number,
				"popularity": track_popularity,
				"duration_ms": track_durationMs,
				"explicit": track_explicit,
				"preview_url": track_preview_url
			},
			"albumInfo": {
				"id": album_id,
				"name": album_name,
				"image": album_image,
				"total_tracks": album_totalTracks,
				"release_date": album_release_date
			},
			"artistInfo": {
				"id": artists_id,
				"name": artists_name
			}
		}
		return { "error": False, "code": "SUCCESS", "message": "성공적으로 데이터를 불러왔습니다.", "data": data }

	except Exception as error:
		return { "error": True, "code": "UNKNOWN", "message": f"알 수 없는 오류가 발생했습니다.\n{error}", "error_detail": traceback.format_exc(), "data": None }

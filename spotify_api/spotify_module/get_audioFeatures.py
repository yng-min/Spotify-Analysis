from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import traceback


def getAudioFeatures(url: str):
	"""
	Spotify의 트랙 오디오 피처 데이터를 요청하는 함수

	url: 트랙 URL
	"""
	try:
		if url.find("https://") >= 0:
			uri = "spotify:track:" + url.split("track/")[1].split("?si=")[0]
		else:
			uri = url

		client_credentials_manager = SpotifyClientCredentials(
			client_id="7c8e50dae33c41c88e48909166bef20e",
			client_secret="4fb5615b21b544edb5f647ab68dabcbd"
		)
		sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
		sp.trace = True
		trackFeatures = sp.audio_features(uri)

		track_id = trackFeatures[0]['id']
		track_duration_ms = trackFeatures[0]['duration_ms']
		track_danceability = trackFeatures[0]['danceability']
		track_energy = trackFeatures[0]['energy']
		track_speechiness = trackFeatures[0]['speechiness']
		track_acousticness = trackFeatures[0]['acousticness']
		track_instrumentalness = trackFeatures[0]['instrumentalness']
		track_liveness = trackFeatures[0]['liveness']
		track_valence = trackFeatures[0]['valence']

		data = {
			"trackInfo": {
				"id": track_id,
				"duration_ms": track_duration_ms
			},
			"trackFeatures": {
				"danceability": track_danceability,
				"energy": track_energy,
				"speechiness": track_speechiness,
				"acousticness": track_acousticness,
				"instrumentalness": track_instrumentalness,
				"liveness": track_liveness,
				"valence": track_valence,
			}
		}
		return { "error": False, "code": "SUCCESS", "message": "성공적으로 데이터를 불러왔습니다.", "data": data }

	except Exception as error:
		return { "error": True, "code": "UNKNOWN", "message": f"알 수 없는 오류가 발생했습니다.\n{error}", "error_detail": traceback.format_exc(), "data": None }

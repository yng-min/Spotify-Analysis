from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import traceback
import json

with open(r"./spotify_api/config.json", "rt", encoding="UTF8") as configJson:
	config = json.load(configJson)


def getAudioAnalysis(url: str):
	"""
	Spotify의 트랙 아날리시스 데이터를 요청하는 함수

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
		trackAnalysis = sp.audio_analysis(uri)

		if trackAnalysis['meta']['status_code'] != 0:
			return { "error": True, "code": "EMPTY_DATA", "message": f"트랙 분석 데이터가 없습니다.\n{error}", "error_detail": traceback.format_exc(), "data": None }

		track_analysis_sample_rate = trackAnalysis['track']['analysis_sample_rate']
		track_analysis_channels = trackAnalysis['track']['analysis_channels']
		track_tempo = trackAnalysis['track']['tempo']
		track_tempo_confidence = trackAnalysis['track']['tempo_confidence']
		track_key = trackAnalysis['track']['key']
		track_key_confidence = trackAnalysis['track']['key_confidence']
		track_mode = trackAnalysis['track']['mode']
		track_mode_confidence = trackAnalysis['track']['mode_confidence']
		track_time_signature = trackAnalysis['track']['time_signature']
		track_time_signature_confidence = trackAnalysis['track']['time_signature_confidence']
		track_loudness = trackAnalysis['track']['loudness']

		data = {
			"trackInfo": {
				"id": uri.split("track:")[1]
			},
			"trackAnalysis": {
				"analysis_sample_rate": track_analysis_sample_rate,
				"analysis_channels": track_analysis_channels,
				"tempo": track_tempo,
				"tempo_confidence": track_tempo_confidence,
				"key": track_key,
				"key_confidence": track_key_confidence,
				"mode": track_mode,
				"mode_confidence": track_mode_confidence,
				"time_signature": track_time_signature,
				"time_signature_confidence": track_time_signature_confidence,
				"loudness": track_loudness
			}
		}
		return { "error": False, "code": "SUCCESS", "message": "성공적으로 데이터를 불러왔습니다.", "data": data }

	except Exception as error:
		return { "error": True, "code": "UNKNOWN", "message": f"알 수 없는 오류가 발생했습니다.\n{error}", "error_detail": traceback.format_exc(), "data": None }

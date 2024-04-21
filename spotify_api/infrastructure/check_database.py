import threading
import sqlite3
import os
import requests
import traceback
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from spotify_api.infrastructure.get_api import SpotifyData
from infrastructure.database import DatabaseCharts, DatabaseTracks


## 공통 변수 설정
headers = { "Content-Type": "application/json" }
globalChartURL = "https://charts-spotify-com-service.spotify.com/public/v0/charts"


class CheckCharts:

	def __init__(self) -> None:
		pass

	def check():
		if not os.path.isfile(r"./spotify_api/database/charts_global_top50.sqlite"):
			DatabaseCharts.setup()

		result = requests.get(url=globalChartURL, headers=headers)
		playlist_latestDate = ""
		chartResult = {}
		if 200 <= result.status_code < 300:
			chartResult = result.json()['chartEntryViewResponses'][0]
			playlist_latestDate = chartResult['displayChart']['chartMetadata']['dimensions']['latestDate']

		else:
			playlist_latestDate = None
			print(f"[Check Charts] 서버와의 통신 과정 중 오류가 발생했습니다.\nStatus Code: {result.status_code}\nResponse: {result}")

		chartsDB = sqlite3.connect(r"./spotify_api/database/charts_global_top50.sqlite", isolation_level=None).cursor()
		try:
			latestDate = chartsDB.execute("SELECT latestDate FROM chartInfo").fetchone()[0]

			try:
				if playlist_latestDate is None:
					print("[Check Charts] 정보를 불러올 수 없습니다.")

				elif playlist_latestDate == latestDate:
					pass

				elif playlist_latestDate != latestDate:
					print("[Check Tracks] 차트 데이터가 변경되어 최신 정보로 저장합니다...")
					import time
					start = time.time()
					DatabaseCharts.save(data=SpotifyData.get_charts())
					delta = time.time() - start
					print(f"[Check Tracks] 최신 정보 저장을 완료했습니다. ({delta}초 소요)")

			except Exception as error:
				print(f"[Check Charts] 다음의 오류가 발생했습니다. '{error}'")
				print(traceback.format_exc())

		except:
			print("[Check Tracks] 차트 데이터가 변경되어 최신 정보로 저장합니다...")
			import time
			start = time.time()
			DatabaseCharts.save(data=SpotifyData.get_charts())
			delta = time.time() - start
			print(f"[Check Tracks] 최신 정보 저장을 완료했습니다. ({delta}초 소요)")

		threading.Timer(1800, CheckCharts.check).start()

class CheckTracks:

	def __init__(self) -> None:
		pass

	def check():
		if not os.path.isfile(r"./spotify_api/database/tracks.sqlite"):
			DatabaseTracks.setup()

		## 트랙 정보
		tracks_id = []
		tracks_name = []
		## 트랙 특징 정보
		tracks_preview_url = []
		tracks_duration_ms = []
		tracks_popularity = []
		tracks_explicit = []
		tracks_danceability = []
		tracks_energy = []
		tracks_speechiness = []
		tracks_acousticness = []
		tracks_instrumentalness = []
		tracks_liveness = []
		tracks_valence = []
		## 트랙 분석 정보
		tracks_analysis_sample_rate = []
		tracks_analysis_channels = []
		tracks_tempo = []
		tracks_tempo_confidence = []
		tracks_key = []
		tracks_key_confidence = []
		tracks_mode = []
		tracks_mode_confidence = []
		tracks_time_signature = []
		tracks_time_signature_confidence = []
		tracks_loudness = []
		## 앨범 정보
		albums_id = []
		albums_name = []
		albums_image = []
		albums_release_date = []
		## 아티스트 정보
		artists_id = []
		artists_name = []
		## 순위 정보
		ranks_currentRank = []
		ranks_previousRank = []
		ranks_entryStatus = []

		result = requests.get(url=globalChartURL, headers=headers)
		playlist_latestDate = ""
		chartResult = {}
		if 200 <= result.status_code < 300:
			chartResult = result.json()['chartEntryViewResponses'][0]
			playlist_latestDate = chartResult['displayChart']['chartMetadata']['dimensions']['latestDate']

		else:
			playlist_latestDate = None
			print(f"[Check Tracks] 서버와의 통신 과정 중 오류가 발생했습니다.\nStatus Code: {result.status_code}\nResponse: {result}")

		tracksCONN = sqlite3.connect(r"./spotify_api/database/tracks.sqlite", isolation_level=None)
		tracksDB = tracksCONN.cursor()
		try:
			latestDate = tracksDB.execute("SELECT latestDate FROM databaseInfo").fetchone()[0]
			tracksCONN.close()

			try:
				if playlist_latestDate is None:
					print("[Check Tracks] 정보를 불러올 수 없습니다.")

				elif playlist_latestDate == latestDate:
					pass

				elif playlist_latestDate != latestDate:
					print("[Check Tracks] 차트 데이터가 변경되어 최신 정보로 저장합니다...")
					import time
					start = time.time()

					for i in range(len(chartResult['entries'])):
						time.sleep(0.1) # Spotify API ratelimit에 대처하기 위한 딜레이
						print(f"- Track: {i+1}")
						time.sleep(0.1) # Spotify API ratelimit에 대처하기 위한 딜레이
						track = SpotifyData.get_tracks(url=chartResult['entries'][i]['trackMetadata']['trackUri'])
						print(track)
						time.sleep(0.1) # Spotify API ratelimit에 대처하기 위한 딜레이
						feature = SpotifyData.get_audioFeatures(url=chartResult['entries'][i]['trackMetadata']['trackUri'])
						print(feature)
						time.sleep(0.1) # Spotify API ratelimit에 대처하기 위한 딜레이
						analysis = SpotifyData.get_audioAnalysis(url=chartResult['entries'][i]['trackMetadata']['trackUri'])
						print(analysis)

						tracks_id.append(track['data']['trackInfo']['id'])
						tracks_name.append(track['data']['trackInfo']['name'])

						tracks_preview_url.append(track['data']['trackDetails']['preview_url'])
						tracks_duration_ms.append(feature['data']['trackInfo']['duration_ms'])
						tracks_explicit.append(track['data']['trackDetails']['explicit'])
						tracks_popularity.append(track['data']['trackDetails']['popularity'])
						tracks_danceability.append(feature['data']['trackFeatures']['danceability'])
						tracks_energy.append(feature['data']['trackFeatures']['energy'])
						tracks_speechiness.append(feature['data']['trackFeatures']['speechiness'])
						tracks_acousticness.append(feature['data']['trackFeatures']['acousticness'])
						tracks_instrumentalness.append(feature['data']['trackFeatures']['instrumentalness'])
						tracks_liveness.append(feature['data']['trackFeatures']['liveness'])
						tracks_valence.append(feature['data']['trackFeatures']['valence'])

						if analysis['code'] == "EMPTY_DATA":
							tracks_analysis_sample_rate.append(None)
							tracks_analysis_channels.append(None)
							tracks_tempo.append(None)
							tracks_tempo_confidence.append(None)
							tracks_key.append(None)
							tracks_key_confidence.append(None)
							tracks_mode.append(None)
							tracks_mode_confidence.append(None)
							tracks_time_signature.append(None)
							tracks_time_signature_confidence.append(None)
							tracks_loudness.append(None)
						else:
							tracks_analysis_sample_rate.append(analysis['data']['trackAnalysis']['analysis_sample_rate'])
							tracks_analysis_channels.append(analysis['data']['trackAnalysis']['analysis_channels'])
							tracks_tempo.append(analysis['data']['trackAnalysis']['tempo'])
							tracks_tempo_confidence.append(analysis['data']['trackAnalysis']['tempo_confidence'])
							tracks_key.append(analysis['data']['trackAnalysis']['key'])
							tracks_key_confidence.append(analysis['data']['trackAnalysis']['key_confidence'])
							tracks_mode.append(analysis['data']['trackAnalysis']['mode'])
							tracks_mode_confidence.append(analysis['data']['trackAnalysis']['mode_confidence'])
							tracks_time_signature.append(analysis['data']['trackAnalysis']['time_signature'])
							tracks_time_signature_confidence.append(analysis['data']['trackAnalysis']['time_signature_confidence'])
							tracks_loudness.append(analysis['data']['trackAnalysis']['loudness'])

						albums_id.append(track['data']['albumInfo']['id'])
						albums_name.append(track['data']['albumInfo']['name'])
						albums_image.append(track['data']['albumInfo']['image'])
						albums_release_date.append(track['data']['albumInfo']['release_date'])

						artist_id, artist_name = "", ""
						for j in range(len(track['data']['artistInfo'])):
							artist_id += f"{track['data']['artistInfo'][j]['id']};; "
							artist_name += f"{track['data']['artistInfo'][j]['name']};; "
						artists_id.append(artist_id)
						artists_name.append(artist_name)

						ranks_currentRank.append(chartResult['entries'][i]['chartEntryData']['currentRank'])
						ranks_previousRank.append(chartResult['entries'][i]['chartEntryData']['previousRank'])
						ranks_entryStatus.append(chartResult['entries'][i]['chartEntryData']['entryStatus'])

					data = {
						"databaseInfo": {
							"latestDate": playlist_latestDate
						},
						"trackInfo": {
							"id": tracks_id,
							"name": tracks_name
						},
						"trackDetails": {
							"preview_url": tracks_preview_url,
							"duration_ms": tracks_duration_ms,
							"explicit": tracks_explicit,
							"popularity": tracks_popularity,
							"danceability": tracks_danceability,
							"energy": tracks_energy,
							"speechiness": tracks_speechiness,
							"acousticness": tracks_acousticness,
							"instrumentalness": tracks_instrumentalness,
							"liveness": tracks_liveness,
							"valence": tracks_valence
						},
						"trackAnalysis": {
							"analysis_sample_rate": tracks_analysis_sample_rate,
							"analysis_channels": tracks_analysis_channels,
							"tempo": tracks_tempo,
							"tempo_confidence": tracks_tempo_confidence,
							"key": tracks_key,
							"key_confidence": tracks_key_confidence,
							"mode": tracks_mode,
							"mode_confidence": tracks_mode_confidence,
							"time_signature": tracks_time_signature,
							"time_signature_confidence": tracks_time_signature_confidence,
							"loudness": tracks_loudness
						},
						"albumInfo": {
							"id": albums_id,
							"name": albums_name,
							"image": albums_image,
							"release_date": albums_release_date
						},
						"artistInfo": {
							"id": artists_id,
							"name": artists_name
						},
						"rankInfo": {
							"currentRank": ranks_currentRank,
							"previousRank": ranks_previousRank,
							"entryStatus": ranks_entryStatus
						}
					}
					DatabaseTracks.reset()
					DatabaseTracks.save(data=data)
					delta = time.time() - start
					print(f"[Check Tracks] 최신 정보 저장을 완료했습니다. ({delta}초 소요)")

			except Exception as error:
				try: tracksDB = tracksCONN.cursor()
				except: pass
				print(f"[Check Tracks] 다음의 오류가 발생했습니다. '{error}'")
				print(traceback.format_exc())

		except:
			print("[Check Tracks] 차트 데이터가 변경되어 최신 정보로 저장합니다...")
			import time
			start = time.time()

			for i in range(len(chartResult['entries'])):
				time.sleep(0.1) # Spotify API ratelimit에 대처하기 위한 딜레이
				print(f"- Track: {i+1}")
				time.sleep(0.1) # Spotify API ratelimit에 대처하기 위한 딜레이
				track = SpotifyData.get_tracks(url=chartResult['entries'][i]['trackMetadata']['trackUri'])
				print(track)
				time.sleep(0.1) # Spotify API ratelimit에 대처하기 위한 딜레이
				feature = SpotifyData.get_audioFeatures(url=chartResult['entries'][i]['trackMetadata']['trackUri'])
				print(feature)
				time.sleep(0.1) # Spotify API ratelimit에 대처하기 위한 딜레이
				analysis = SpotifyData.get_audioAnalysis(url=chartResult['entries'][i]['trackMetadata']['trackUri'])
				print(analysis)

				tracks_id.append(track['data']['trackInfo']['id'])
				tracks_name.append(track['data']['trackInfo']['name'])

				tracks_preview_url.append(track['data']['trackDetails']['preview_url'])
				tracks_duration_ms.append(feature['data']['trackInfo']['duration_ms'])
				tracks_explicit.append(track['data']['trackDetails']['explicit'])
				tracks_popularity.append(track['data']['trackDetails']['popularity'])
				tracks_danceability.append(feature['data']['trackFeatures']['danceability'])
				tracks_energy.append(feature['data']['trackFeatures']['energy'])
				tracks_speechiness.append(feature['data']['trackFeatures']['speechiness'])
				tracks_acousticness.append(feature['data']['trackFeatures']['acousticness'])
				tracks_instrumentalness.append(feature['data']['trackFeatures']['instrumentalness'])
				tracks_liveness.append(feature['data']['trackFeatures']['liveness'])
				tracks_valence.append(feature['data']['trackFeatures']['valence'])

				if analysis['code'] == "EMPTY_DATA":
					tracks_analysis_sample_rate.append(None)
					tracks_analysis_channels.append(None)
					tracks_tempo.append(None)
					tracks_tempo_confidence.append(None)
					tracks_key.append(None)
					tracks_key_confidence.append(None)
					tracks_mode.append(None)
					tracks_mode_confidence.append(None)
					tracks_time_signature.append(None)
					tracks_time_signature_confidence.append(None)
					tracks_loudness.append(None)
				else:
					tracks_analysis_sample_rate.append(analysis['data']['trackAnalysis']['analysis_sample_rate'])
					tracks_analysis_channels.append(analysis['data']['trackAnalysis']['analysis_channels'])
					tracks_tempo.append(analysis['data']['trackAnalysis']['tempo'])
					tracks_tempo_confidence.append(analysis['data']['trackAnalysis']['tempo_confidence'])
					tracks_key.append(analysis['data']['trackAnalysis']['key'])
					tracks_key_confidence.append(analysis['data']['trackAnalysis']['key_confidence'])
					tracks_mode.append(analysis['data']['trackAnalysis']['mode'])
					tracks_mode_confidence.append(analysis['data']['trackAnalysis']['mode_confidence'])
					tracks_time_signature.append(analysis['data']['trackAnalysis']['time_signature'])
					tracks_time_signature_confidence.append(analysis['data']['trackAnalysis']['time_signature_confidence'])
					tracks_loudness.append(analysis['data']['trackAnalysis']['loudness'])

				albums_id.append(track['data']['albumInfo']['id'])
				albums_name.append(track['data']['albumInfo']['name'])
				albums_image.append(track['data']['albumInfo']['image'])
				albums_release_date.append(track['data']['albumInfo']['release_date'])

				artist_id, artist_name = "", ""
				for j in range(len(track['data']['artistInfo'])):
					artist_id += f"{track['data']['artistInfo'][j]['id']};; "
					artist_name += f"{track['data']['artistInfo'][j]['name']};; "
				artists_id.append(artist_id)
				artists_name.append(artist_name)

				ranks_currentRank.append(chartResult['entries'][i]['chartEntryData']['currentRank'])
				ranks_previousRank.append(chartResult['entries'][i]['chartEntryData']['previousRank'])
				ranks_entryStatus.append(chartResult['entries'][i]['chartEntryData']['entryStatus'])

			data = {
				"databaseInfo": {
					"latestDate": playlist_latestDate
				},
				"trackInfo": {
					"id": tracks_id,
					"name": tracks_name
				},
				"trackDetails": {
					"preview_url": tracks_preview_url,
					"duration_ms": tracks_duration_ms,
					"explicit": tracks_explicit,
					"popularity": tracks_popularity,
					"danceability": tracks_danceability,
					"energy": tracks_energy,
					"speechiness": tracks_speechiness,
					"acousticness": tracks_acousticness,
					"instrumentalness": tracks_instrumentalness,
					"liveness": tracks_liveness,
					"valence": tracks_valence
				},
				"trackAnalysis": {
					"analysis_sample_rate": tracks_analysis_sample_rate,
					"analysis_channels": tracks_analysis_channels,
					"tempo": tracks_tempo,
					"tempo_confidence": tracks_tempo_confidence,
					"key": tracks_key,
					"key_confidence": tracks_key_confidence,
					"mode": tracks_mode,
					"mode_confidence": tracks_mode_confidence,
					"time_signature": tracks_time_signature,
					"time_signature_confidence": tracks_time_signature_confidence,
					"loudness": tracks_loudness
				},
				"albumInfo": {
					"id": albums_id,
					"name": albums_name,
					"image": albums_image,
					"release_date": albums_release_date
				},
				"artistInfo": {
					"id": artists_id,
					"name": artists_name
				},
				"rankInfo": {
					"currentRank": ranks_currentRank,
					"previousRank": ranks_previousRank,
					"entryStatus": ranks_entryStatus
				}
			}
			DatabaseTracks.reset()
			DatabaseTracks.save(data=data)
			delta = time.time() - start
			print(f"[Check Tracks] 최신 정보 저장을 완료했습니다. ({delta}초 소요)")

		threading.Timer(1800, CheckTracks.check).start()

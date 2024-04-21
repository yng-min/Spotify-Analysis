import sqlite3
import os


class DatabaseCharts:

	def __init__(self) -> None:
		pass

	def setup():
		"""
		Spotify 차트 데이터를 저장하기 위한 데이터베이스 초기 설정을 담당하는 함수
		"""
		if os.path.isfile(r"./spotify_api/database/charts_global_top50.sqlite"):
			return

		chartsCONN = sqlite3.connect(r"./spotify_api/database/charts_global_top50.sqlite", isolation_level=None)
		chartsDB = chartsCONN.cursor()
		chartsDB.execute("""
			CREATE TABLE IF NOT EXISTS chartInfo(
				title TEXT,
				latestDate TEXT
			)
		""")
		chartsDB.execute("""
			CREATE TABLE IF NOT EXISTS rankInfo(
				currentRank INTEGER,
				previousRank INTEGER,
				entryStatus TEXT
			)
		""")
		chartsDB.execute("""
			CREATE TABLE IF NOT EXISTS trackInfo(
				name TEXT,
				artists TEXT,
				url TEXT,
				image TEXT
			)
		""")
		chartsCONN.close()

	def save(data: dict):
		"""
		Spotify 차트 데이터의 저장을 담당하는 함수입니다.

		data: Spotify 차트 데이터('spotify_module/get_charts.py'에서 받아와야 함.)
		"""
		if not os.path.isfile(r"./spotify_api/database/charts_global_top50.sqlite"):
			DatabaseCharts.setup()

		chartsCONN = sqlite3.connect(r"./spotify_api/database/charts_global_top50.sqlite", isolation_level=None)
		chartsDB = chartsCONN.cursor()
		## DB 초기화
		chartsDB.execute("DELETE FROM chartInfo")
		chartsDB.execute("DELETE FROM rankInfo")
		chartsDB.execute("DELETE FROM trackInfo")
		## chartInfo 저장
		chartsDB.execute("INSERT INTO chartInfo(title, latestDate) VALUES(?, ?)", (data['data']['chartInfo']['title'], data['data']['chartInfo']['latestDate']))
		## rankInfo 저장
		for i in range(len(data['data']['rankInfo']['currentRank'])):
			chartsDB.execute("INSERT INTO rankInfo(currentRank, previousRank, entryStatus) VALUES(?, ?, ?)", (data['data']['rankInfo']['currentRank'][i], data['data']['rankInfo']['previousRank'][i], data['data']['rankInfo']['entryStatus'][i]))
		## trackInfo 저장
		for i in range(len(data['data']['trackInfo']['name'])):
			artists = ""
			for j in range(len(data['data']['trackInfo']['artists'][i])):
				artists += f"{data['data']['trackInfo']['artists'][i][j]};; "
			chartsDB.execute("INSERT INTO trackInfo(name, artists, url, image) VALUES(?, ?, ?, ?)", (data['data']['trackInfo']['name'][i], artists[:-3], data['data']['trackInfo']['url'][i], data['data']['trackInfo']['image'][i]))

		chartsDB.close()

	def read():
		"""
		데이터베이스에 저장된 Spotify 차트 데이터 읽기를 담당하는 함수입니다.
		"""
		if not os.path.isfile(r"./spotify_api/database/charts_global_top50.sqlite"):
			return { "error": False, "code": "NODATA", "message": "저장된 데이터가 없습니다.", "data": None }

		chartsCONN = sqlite3.connect(r"./spotify_api/database/charts_global_top50.sqlite", isolation_level=None)
		chartsCONN.row_factory = sqlite3.Row
		chartsDB = chartsCONN.cursor()

		playlist_title = ""
		playlist_latestDate = ""
		track_currentRank = []
		track_previousRank = []
		track_entryStatus = []
		track_name = []
		track_artists = []
		track_url = []
		track_imageUrl = []

		## chartInfo 읽기
		chartInfo = chartsDB.execute("SELECT * FROM chartInfo").fetchall()[0]
		playlist_title = chartInfo['title']
		playlist_latestDate = chartInfo['latestDate']
		## rankInfo 읽기
		rankInfo = chartsDB.execute("SELECT * FROM rankInfo").fetchall()
		for i in range(len(rankInfo)):
			track_currentRank.append(rankInfo[i]['currentRank'])
			track_previousRank.append(rankInfo[i]['previousRank'])
			track_entryStatus.append(rankInfo[i]['entryStatus'])
		## trackInfo 읽기
		trackInfo = chartsDB.execute("SELECT * FROM trackInfo").fetchall()
		for i in range(len(trackInfo)):
			track_name.append(trackInfo[i]['name'])
			track_artists.append(trackInfo[i]['artists'])
			track_url.append(trackInfo[i]['url'])
			track_imageUrl.append(trackInfo[i]['image'])

		chartsCONN.close()

		data = {
			"chartInfo": {
				"title": playlist_title,
				"latestDate": playlist_latestDate
			},
			"rankInfo": {
				"currentRank": track_currentRank,
				"previousRank": track_previousRank,
				"entryStatus": track_entryStatus
			},
			"trackInfo": {
				"name": track_name,
				"artists": track_artists,
				"url": track_url,
				"image": track_imageUrl
			}
		}
		return { "error": False, "code": "SUCCESS", "message": "성공적으로 데이터를 불러왔습니다.", "data": data }

class DatabaseTracks:

	def __init__(self) -> None:
		pass

	def setup():
		"""
		Spotify 트랙 데이터를 저장하기 위한 데이터베이스 초기 설정을 담당하는 함수입니다.
		"""
		if os.path.isfile(r"./spotify_api/database/tracks.sqlite"):
			return

		tracksCONN = sqlite3.connect(r"./spotify_api/database/tracks.sqlite")
		tracksDB = tracksCONN.cursor()
		tracksDB.execute("""
			CREATE TABLE IF NOT EXISTS databaseInfo(
				latestDate TEXT
			)
		""")
		tracksDB.execute("""
			CREATE TABLE IF NOT EXISTS trackInfo(
				id TEXT,
				name TEXT
			)
		""")
		tracksDB.execute("""
			CREATE TABLE IF NOT EXISTS trackDetails(
				preview_url TEXT,
				duration_ms INTEGER,
				explicit INTEGER,
				popularity INTEGER,
				danceability REAL,
				energy REAL,
				speechiness REAL,
				acousticness REAL,
				instrumentalness REAL,
				liveness REAL,
				valence REAL
			)
		""")
		tracksDB.execute("""
			CREATE TABLE IF NOT EXISTS trackAnalysis(
				analysis_sample_rate INTEGER,
				analysis_channels INTEGER,
				tempo REAL,
				tempo_confidence REAL,
				key INTEGER,
				key_confidence REAL,
				mode INTEGER,
				mode_confidence INTEGER,
				time_signature INTEGER,
				time_signature_confidence REAL,
				loudness REAL
			)
		""")
		tracksDB.execute("""
			CREATE TABLE IF NOT EXISTS albumInfo(
				id TEXT,
				name TEXT,
				image TEXT,
				release_date TEXT
			)
		""")
		tracksDB.execute("""
			CREATE TABLE IF NOT EXISTS artistInfo(
				id TEXT,
				name TEXT
			)
		""")
		tracksDB.execute("""
			CREATE TABLE IF NOT EXISTS rankInfo(
				currentRank INTEGER,
				previousRank INTEGER,
				entryStatus TEXT
			)
		""")
		tracksCONN.commit()
		tracksCONN.close()

	def reset():
		"""
		Spotify 트랙 데이터 데이터베이스의 초기화를 담당하는 함수입니다.
		"""
		if not os.path.isfile(r"./spotify_api/database/tracks.sqlite"):
			DatabaseTracks.setup()

		tracksCONN = sqlite3.connect(r"./spotify_api/database/tracks.sqlite")
		tracksDB = tracksCONN.cursor()
		## databaseInfo 초기화
		tracksDB.execute("DELETE FROM databaseInfo")
		## trackInfo 초기화
		tracksDB.execute("DELETE FROM trackInfo")
		## trackDetails 초기화
		tracksDB.execute("DELETE FROM trackDetails")
		## trackAnalysis 초기화
		tracksDB.execute("DELETE FROM trackAnalysis")
		## albumInfo 초기화
		tracksDB.execute("DELETE FROM albumInfo")
		## artistInfo 초기화
		tracksDB.execute("DELETE FROM artistInfo")
		## rankInfo 초기화
		tracksDB.execute("DELETE FROM rankInfo")
		tracksCONN.commit()
		tracksCONN.close()

	def save(data: dict):
		"""
		Spotify 트랙 데이터의 저장을 담당하는 함수입니다.

		매개변수:
			- data: Spotify 트랙 데이터와 특징 데이터, 분석 데이터
				> 트랙 데이터: 'spotify_module/get_tracks.py'를 통해 'infrastructure/check_database.py'에서 받아와야 함.
				> 특징 데이터: 'spotify_module/get_audioFeatures.py'를 통해 'infrastructure/check_database.py'에서 받아와야 함.
				> 분석 데이터: 'spotify_module/get_audioAnalysis.py'를 통해 'infrastructure/check_database.py'에서 받아와야 함.
		"""
		if not os.path.isfile(r"./spotify_api/database/tracks.sqlite"):
			DatabaseTracks.setup()

		tracksCONN = sqlite3.connect(r"./spotify_api/database/tracks.sqlite")
		tracksDB = tracksCONN.cursor()
		## databaseInfo 저장
		tracksDB.execute("INSERT INTO databaseInfo(latestDate) VALUES(?)", (data['databaseInfo']['latestDate'],))
		## 트랙 데이터 저장
		for i in range(len(data['trackInfo']['id'])):
			tracksDB.execute("INSERT INTO trackInfo(id, name) VALUES(?, ?)", (data['trackInfo']['id'][i], data['trackInfo']['name'][i]))
			tracksDB.execute("INSERT INTO trackDetails(preview_url, duration_ms, explicit, popularity, danceability, energy, speechiness, acousticness, instrumentalness, liveness, valence) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (data['trackDetails']['preview_url'][i], data['trackDetails']['duration_ms'][i], data['trackDetails']['explicit'][i], data['trackDetails']['popularity'][i], data['trackDetails']['danceability'][i], data['trackDetails']['energy'][i], data['trackDetails']['speechiness'][i], data['trackDetails']['acousticness'][i], data['trackDetails']['instrumentalness'][i], data['trackDetails']['liveness'][i], data['trackDetails']['valence'][i]))
			tracksDB.execute("INSERT INTO trackAnalysis(analysis_sample_rate, analysis_channels, tempo, tempo_confidence, key, key_confidence, mode, mode_confidence, time_signature, time_signature_confidence, loudness) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (data['trackAnalysis']['analysis_sample_rate'][i], data['trackAnalysis']['analysis_channels'][i], data['trackAnalysis']['tempo'][i], data['trackAnalysis']['tempo_confidence'][i], data['trackAnalysis']['key'][i], data['trackAnalysis']['key_confidence'][i], data['trackAnalysis']['mode'][i], data['trackAnalysis']['mode_confidence'][i], data['trackAnalysis']['time_signature'][i], data['trackAnalysis']['time_signature_confidence'][i], data['trackAnalysis']['loudness'][i]))
			tracksDB.execute("INSERT INTO albumInfo(id, name, image, release_date) VALUES(?, ?, ? ,?)", (data['albumInfo']['id'][i], data['albumInfo']['name'][i], data['albumInfo']['image'][i], data['albumInfo']['release_date'][i]))
			tracksDB.execute("INSERT INTO artistInfo(id, name) VALUES(?, ?)", (data['artistInfo']['id'][i][:-3], data['artistInfo']['name'][i][:-3]))
			tracksDB.execute("INSERT INTO rankInfo(currentRank, previousRank, entryStatus) VALUES(?, ?, ?)", (data['rankInfo']['currentRank'][i], data['rankInfo']['previousRank'][i], data['rankInfo']['entryStatus'][i]))

		tracksCONN.commit()
		tracksCONN.close()

	def read():
		"""
		데이터베이스에 저장된 Spotify 트랙 데이터 읽기를 담당하는 함수입니다.
		"""
		if not os.path.isfile(r"./spotify_api/database/tracks.sqlite"):
			return { "error": False, "code": "NODATA", "message": "저장된 데이터가 없습니다.", "data": None }

		tracksCONN = sqlite3.connect(r"./spotify_api/database/tracks.sqlite", isolation_level=None)
		tracksCONN.row_factory = sqlite3.Row
		tracksDB = tracksCONN.cursor()

		## 차트 마지막 수정일자
		database_lateseDate = ""
		## 트랙 정보
		tracks_id = []
		tracks_name = []
		## 트랙 특징 정보
		tracks_preview_url = []
		tracks_duration_ms = []
		tracks_explicit = []
		tracks_popularity = []
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

		## databaseInfo 읽기
		database_lateseDate = tracksDB.execute("SELECT latestDate FROM databaseInfo").fetchone()
		## trackInfo 읽기
		trackInfo = tracksDB.execute("SELECT * FROM trackInfo").fetchall()
		for i in range(len(trackInfo)):
			tracks_id.append(trackInfo[i]['id'])
			tracks_name.append(trackInfo[i]['name'])
		## trackDetails 읽기
		trackDetails = tracksDB.execute("SELECT * FROM trackDetails").fetchall()
		for i in range(len(trackDetails)):
			tracks_preview_url.append(trackDetails[i]['preview_url'])
			tracks_duration_ms.append(trackDetails[i]['duration_ms'])
			tracks_explicit.append(trackDetails[i]['explicit'])
			tracks_popularity.append(trackDetails[i]['popularity'])
			tracks_danceability.append(trackDetails[i]['danceability'])
			tracks_energy.append(trackDetails[i]['energy'])
			tracks_speechiness.append(trackDetails[i]['speechiness'])
			tracks_acousticness.append(trackDetails[i]['acousticness'])
			tracks_instrumentalness.append(trackDetails[i]['instrumentalness'])
			tracks_liveness.append(trackDetails[i]['liveness'])
			tracks_valence.append(trackDetails[i]['valence'])
		## trackAnalysis 읽기
		trackAnalysis = tracksDB.execute("SELECT * FROM trackAnalysis").fetchall()
		for i in range(len(trackAnalysis)):
			tracks_analysis_sample_rate.append(trackAnalysis[i]['analysis_sample_rate'])
			tracks_analysis_channels.append(trackAnalysis[i]['analysis_channels'])
			tracks_tempo.append(trackAnalysis[i]['tempo'])
			tracks_tempo_confidence.append(trackAnalysis[i]['tempo_confidence'])
			tracks_key.append(trackAnalysis[i]['key'])
			tracks_key_confidence.append(trackAnalysis[i]['key_confidence'])
			tracks_mode.append(trackAnalysis[i]['mode'])
			tracks_mode_confidence.append(trackAnalysis[i]['mode_confidence'])
			tracks_time_signature.append(trackAnalysis[i]['time_signature'])
			tracks_time_signature_confidence.append(trackAnalysis[i]['time_signature_confidence'])
			tracks_loudness.append(trackAnalysis[i]['loudness'])
		## albumInfo 읽기
		albumInfo = tracksDB.execute("SELECT * FROM albumInfo").fetchall()
		for i in range(len(albumInfo)):
			albums_id.append(albumInfo[i]['id'])
			albums_name.append(albumInfo[i]['name'])
			albums_image.append(albumInfo[i]['image'])
			albums_release_date.append(albumInfo[i]['release_date'])
		## artistInfo 읽기
		artistInfo = tracksDB.execute("SELECT * FROM artistInfo").fetchall()
		for i in range(len(artistInfo)):
			artists_id.append(artistInfo[i]['id'])
			artists_name.append(artistInfo[i]['name'])
		## rankInfo 읽기
		rankInfo = tracksDB.execute("SELECT * FROM rankInfo").fetchall()
		for i in range(len(rankInfo)):
			ranks_currentRank.append(rankInfo[i]['currentRank'])
			ranks_previousRank.append(rankInfo[i]['previousRank'])
			ranks_entryStatus.append(rankInfo[i]['entryStatus'])

		tracksCONN.close()

		data = {
			"databaseInfo": {
				"latestDate": database_lateseDate
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
		return { "error": False, "code": "SUCCESS", "message": "성공적으로 데이터를 불러왔습니다.", "data": data }

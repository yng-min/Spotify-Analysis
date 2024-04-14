import requests
import traceback


## 공통 변수 설정
headers = { "Content-Type": "application/json" }
globalChartURL = "https://charts-spotify-com-service.spotify.com/public/v0/charts"


def getGlobalWeeklyCharts(url: str = globalChartURL):
	"""
	Spotify의 글로벌 위클리 차트 데이터를 요청하는 함수

	url: 차트 요청 API URL
	"""
	try:
		result = requests.get(url=url, headers=headers)

		if 200 <= result.status_code < 300:
			chartResult = result.json()['chartEntryViewResponses'][0]

			## 글로벌 Top50 플레이리스트 관련 스트링 자료
			playlist_chartData = chartResult['displayChart']['chartMetadata']
			# 글로벌 Top50 플레이리스트 제목
			playlist_title = playlist_chartData['readableTitle']
			# # 글로벌 Top50 플레이리스트 스포티파이 URL *uri가 정상적으로 요청되지 않아 비활성화*
			# playlist_urlSplit = playlist_chartData['uri'].split("chart:")[1]
			# playlist_url = f"https://open.spotify.com/chart/{playlist_urlSplit}"
			# 글로벌 Top50 플레이리스트 수정 시각
			playlist_latestDate = playlist_chartData['dimensions']['latestDate']

			## 트랙 관련 리스트 자료
			track_chartData = chartResult['entries']
			track_currentRank = []
			track_previousRank = []
			track_entryStatus = []
			track_name = []
			track_artists = []
			track_url = []
			track_image = []

			print(len(track_chartData))
			for i in range(len(track_chartData)):
				# 현재 트랙 순위
				track_currentRank.append(track_chartData[i]['chartEntryData']['currentRank'])
				# 이전 트랙 순위 (지난주)
				track_previousRank.append(track_chartData[i]['chartEntryData']['previousRank'])
				# 순위 변동 수치
				track_entryStatus.append(track_chartData[i]['chartEntryData']['entryStatus'])
				# 트랙 이름
				track_name.append(track_chartData[i]['trackMetadata']['trackName'])
				# 트랙 아티스트 이름
				artists = []
				for j in range(len(track_chartData[i]['trackMetadata']['artists'])):
					artists.append(track_chartData[i]['trackMetadata']['artists'][j]['name'])
				track_artists.append(artists)
				# 트랙 이미지 URL
				track_image.append(track_chartData[i]['trackMetadata']['displayImageUri'])
				# 트랙 스포티파이 URL
				TrackUrlSplit = track_chartData[i]['trackMetadata']['trackUri'].split("track:")[1]
				track_url.append(f"https://open.spotify.com/track/{TrackUrlSplit}")

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
					"image": track_image
				}
			}
			return { "error": False, "code": "SUCCESS", "message": "성공적으로 데이터를 불러왔습니다.", "data": data }

		else:
			return { "error": True, "code": "NOTSENT", "message": f"서버와의 통신 과정 중 오류가 발생했습니다.\nStatus Code: {result.status_code}\nResponse: {result}", "data": None }

	except Exception as error:
		return { "error": True, "code": "UNKNOWN", "message": f"알 수 없는 오류가 발생했습니다.\n{error}", "error_detail": traceback.format_exc(), "data": None }

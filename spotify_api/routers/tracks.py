from fastapi import APIRouter, Response

from spotify_api.infrastructure import SpotifyData, DatabaseTracks


router = APIRouter(prefix="/tracks")

@router.get("/", name="tracks", tags=['tracks'])
def tracks(response: Response, uri: str = None):
	data = DatabaseTracks.read()['data']
	bart = SpotifyData.get_bart(reco_type=1, reco_str=uri)['data']

	for i in range(len(data['trackInfo']['id'])):
		if data['trackInfo']['id'][i] == uri:
			# html 구축
			html = "<!DOCTYPE html>"
			html += "<html lang='ko'>"

			html += "<head>"
			html += "<meta charset='utf-8'>"
			html += "<title>Spotify Track Analysis - '{}'</title>".format(data['trackInfo']['name'][i])
			html += "</head>"

			html += "<body>"
			html += "<h1>Spotify Track Analysis</h1>"
			html += "<h2>{artists} - {name}</h2>".format(artists=data['artistInfo']['name'][i].replace(";;", ","), name=data['trackInfo']['name'][i])

			html += "<h5>트랙 정보</h5>"
			html += "<table border='1'; style='border-collapse: collapse; border-spacing: 0;'>"
			html += "<tr>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>#</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>#</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>인기도</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>곡 길이</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>앨범</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>발매일</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>미리 들어보기</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>스포티파이에서 듣기</th>"
			html += "<tr>"
			rank = ""
			html += "<td align='center'>{}위</td>".format(data['rankInfo']['currentRank'][i])
			if data['rankInfo']['previousRank'][i] == -1:
				rank = "New"
			else:
				rank = (data['rankInfo']['previousRank'][i] - data['rankInfo']['currentRank'][i])
				if rank == 0:
					rank = " - "
				elif rank > 0:
					rank = f"↑{rank}"
				elif rank < 0:
					rank = f"↓{-rank}"
			html += "<td align='center'>{}</td>".format(rank)
			html += "<td align='center'>{}점</td>".format(data['trackDetails']['popularity'][i])
			duration = data['trackDetails']['duration_ms'][i] / 1000
			minutes = round(duration // 60)
			seconds = round(duration - minutes * 60)
			if len(str(seconds)) < 2:
				seconds = f"0{seconds}"
			m_s = f"{minutes}:{seconds}"
			html += "<td align='center'>{}</td>".format(m_s)
			html += "<td align='center'>{}</td>".format(data['albumInfo']['name'][i])
			html += "<td align='center'>{}</td>".format(data['albumInfo']['release_date'][i])
			if data['trackDetails']['preview_url'][i] != None:
				html += "<td align='center'><a href='{}' target='_blank'>30초 미리듣기</a></td>".format(data['trackDetails']['preview_url'][i])
			else:
				html += "<td align='center'>(링크 없음)</td>"
			html += "<td align='center'><a href='{}' target='_blank'>스포티파이에서 듣기</a></td>".format("https://open.spotify.com/track/" + data['trackInfo']['id'][i])
			html += "</tr>"
			html += "</table>"

			html += "<h5>트랙 분석</h5>"
			html += "<table border='1'; style='border-collapse: collapse; border-spacing: 0;'>"
			html += "<tr>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>리듬 안정성 수치</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>에너지 수치</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>음성 단어 수치</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>음향 수치</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>기악곡 수치</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>라이브 수치</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>분위기 수치</th>"
			html += "<tr>"
			desc = "높음" if data['trackDetails']['danceability'][i] >= 0.5 else "낮음"
			html += "<td align='center'>{value}({description})</td>".format(value=data['trackDetails']['danceability'][i], description=desc)
			desc = "높음" if data['trackDetails']['energy'][i] >= 0.5 else "낮음"
			html += "<td align='center'>{value}({description})</td>".format(value=data['trackDetails']['energy'][i], description=desc)
			desc = "높음" if data['trackDetails']['speechiness'][i] >= 0.5 else "낮음"
			html += "<td align='center'>{value}({description})</td>".format(value=data['trackDetails']['speechiness'][i], description=desc)
			desc = "높음" if data['trackDetails']['acousticness'][i] >= 0.5 else "낮음"
			html += "<td align='center'>{value}({description})</td>".format(value=data['trackDetails']['acousticness'][i], description=desc)
			desc = "높음" if data['trackDetails']['instrumentalness'][i] >= 0.5 else "낮음"
			html += "<td align='center'>{value}({description})</td>".format(value=data['trackDetails']['instrumentalness'][i], description=desc)
			desc = "높음" if data['trackDetails']['liveness'][i] >= 0.5 else "낮음"
			html += "<td align='center'>{value}({description})</td>".format(value=data['trackDetails']['liveness'][i], description=desc)
			desc = "높음" if data['trackDetails']['valence'][i] >= 0.5 else "낮음"
			html += "<td align='center'>{value}({description})</td>".format(value=data['trackDetails']['valence'][i], description=desc)
			html += "</tr>"
			html += "</table>"

			html += "<h5>BART AI 추천곡</h5>"
			html += "<table border='1'; style='border-collapse: collapse; border-spacing: 0;'>"
			html += "<tr>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>트랙/수록곡</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>곡 길이</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>곡 제목</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>아티스트</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>앨범</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>발매일</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>미리 들어보기</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>스포티파이에서 듣기</th>"
			for j in range(len(bart['trackInfo'])):
				html += "<tr>"
				html += "<td align='center'>{track_number}/{total_tracks}</td>".format(track_number=bart['trackInfo']['track_number'][j], total_tracks=bart['albumInfo']['total_tracks'][j])
				b_duration = bart['trackInfo']['duration_ms'][j] / 1000
				b_minutes = round(b_duration // 60)
				b_seconds = round(b_duration - b_minutes * 60)
				if len(str(b_seconds)) < 2:
					b_seconds = f"0{b_seconds}"
				m_s = f"{b_minutes}:{b_seconds}"
				html += "<td align='center'>{}</td>".format(m_s)
				html += "<td align='center'>{}</td>".format(bart['trackInfo']['name'][j])
				html += "<td align='center'>{}</td>".format(bart['artistInfo']['name'][j].replace(";;", ","))
				html += "<td align='center'>{}</td>".format(bart['albumInfo']['name'][j])
				html += "<td align='center'>{}</td>".format(bart['albumInfo']['release_date'][j])
				if bart['trackInfo']['preview_url'][j] != None:
					html += "<td align='center'><a href='{}' target='_blank'>30초 미리듣기</a></td>".format(bart['trackInfo']['preview_url'][j])
				else:
					html += "<td align='center'>(링크 없음)</td>"
				html += "<td align='center'><a href='{}' target='_blank'>스포티파이에서 듣기</a></td>".format("https://open.spotify.com/track/" + bart['trackInfo']['id'][j])
			html += "</tr>"
			html += "</table>"

	html += "</body>"
	html += "</html>"
	import re
	html = re.sub(r"\"", r"'", html)

	response.headers['Content-Type'] = "text/html"
	return html

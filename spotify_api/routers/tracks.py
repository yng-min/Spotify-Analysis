from fastapi import APIRouter, Response

from spotify_api.infrastructure import SpotifyData, DatabaseTracks


router = APIRouter(prefix="/tracks")

@router.get("/", name="tracks", tags=['tracks'])
def tracks(response: Response, tid: str = None):
	data = DatabaseTracks.read()['data']
	bart = SpotifyData.get_bart(reco_type=1, reco_str=tid)['data']

	for i in range(len(data['trackInfo']['id'])):
		if data['trackInfo']['id'][i] == tid:
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

			html += "<hr>"
			html += "<h3>- 트랙 정보</h3>"
			html += "<table border='1'; style='border-collapse: collapse; border-spacing: 0;'>"
			html += "<tr>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>#</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>#</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>인기도</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>곡 길이</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>앨범</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>발매일</th>"
			# html += "<th align='center' style='color: grey; font-size: 12px;'>유해성 콘텐츠</th>"
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
					rank = "&nbsp;-&nbsp;"
				elif rank > 0:
					rank = f"&nbsp;↑{rank}&nbsp;"
				elif rank < 0:
					rank = f"&nbsp;↓{-rank}&nbsp;"
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
			# html += "<td align='center'>{}</td>".format("X" if data['trackDetails']['explicit'][i] == False else "O")
			if data['trackDetails']['preview_url'][i] != None:
				html += "<td align='center'><a href='{}' target='_blank'>30초 미리듣기</a></td>".format(data['trackDetails']['preview_url'][i])
			else:
				html += "<td align='center'>(링크 없음)</td>"
			html += "<td align='center'><a href='{}' target='_blank'>스포티파이 바로가기</a></td>".format("https://open.spotify.com/track/" + data['trackInfo']['id'][i])
			html += "</tr>"
			html += "</table>"

			html += "<h3>- 트랙 세부정보</h3>"
			html += "<table border='1'; style='border-collapse: collapse; border-spacing: 0;'>"
			html += "<tr>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>BPM</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>BPM 정확도</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>Key</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>Key 정확도</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>박자표</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>박자표 정확도</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>라우드니스(dB)</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>분석 샘플레이트</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>분석 채널</th>"
			html += "<tr>"
			html += "<td align='center'>{}</td>".format(f"{round(data['trackAnalysis']['tempo'][i])}bpm" if data['trackAnalysis']['tempo'][i] != None else "(데이터 없음)")
			html += "<td align='center'>{}</td>".format(f"{round(data['trackAnalysis']['tempo_confidence'][i] * 100, ndigits=2)}%" if data['trackAnalysis']['tempo_confidence'][i] != None else "(데이터 없음)")
			key, mode = None, None
			if data['trackAnalysis']['key'][i] == -1 or data['trackAnalysis']['key'][i] == None:
				key = None
			elif data['trackAnalysis']['key'][i] == 0:
				key = "C"
			elif data['trackAnalysis']['key'][i] == 1:
				key = "C#/Db"
			elif data['trackAnalysis']['key'][i] == 2:
				key = "D"
			elif data['trackAnalysis']['key'][i] == 3:
				key = "D#/Eb"
			elif data['trackAnalysis']['key'][i] == 4:
				key = "E"
			elif data['trackAnalysis']['key'][i] == 5:
				key = "F"
			elif data['trackAnalysis']['key'][i] == 6:
				key = "F#/Gb"
			elif data['trackAnalysis']['key'][i] == 7:
				key = "G"
			elif data['trackAnalysis']['key'][i] == 8:
				key = "G#/Ab"
			elif data['trackAnalysis']['key'][i] == 9:
				key = "A"
			elif data['trackAnalysis']['key'][i] == 10:
				key = "A#/Bb"
			elif data['trackAnalysis']['key'][i] == 11:
				key = "B"
			if data['trackAnalysis']['mode'][i] == None:
				mode = None
			elif data['trackAnalysis']['mode'][i] == 0:
				mode = "minor"
			elif data['trackAnalysis']['mode'][i] == 1:
				mode = "Major"
			if key == None:
				key_mode = "(데이터 없음)"
			else:
				key_mode = f"{key} {mode}"
			html += "<td align='center'>{}</td>".format(key_mode)
			key_confidence, mode_confidence, key_mode_confidence = "", "", ""
			if data['trackAnalysis']['key_confidence'][i] != None:
				key_confidence = f"{round(data['trackAnalysis']['key_confidence'][i] * 100, ndigits=2)}%"
			if data['trackAnalysis']['mode_confidence'][i] != None:
				mode_confidence = f"{round(data['trackAnalysis']['mode_confidence'][i] * 100, ndigits=2)}%"
			if data['trackAnalysis']['mode_confidence'][i] == None:
				mode_confidence = "(데이터 없음)"
			if data['trackAnalysis']['key_confidence'][i] == None:
				key_confidence = "(데이터 없음)"
				mode_confidence = "(데이터 없음)"
			key_mode_confidence = f"{key_confidence} / {mode_confidence}"
			html += "<td align='center'>{}</td>".format(key_mode_confidence)
			html += "<td align='center'>{}</td>".format(f"{data['trackAnalysis']['time_signature'][i]}/4" if data['trackAnalysis']['time_signature'][i] != None else "(데이터 없음)")
			html += "<td align='center'>{}</td>".format(f"{round(data['trackAnalysis']['time_signature_confidence'][i] * 100, ndigits=2)}%" if data['trackAnalysis']['time_signature_confidence'][i] != None else "(데이터 없음)")
			html += "<td align='center'>{}</td>".format(f"{data['trackAnalysis']['loudness'][i]}dB" if data['trackAnalysis']['loudness'][i] != None else "(데이터 없음)")
			html += "<td align='center'>{}</td>".format(f"{data['trackAnalysis']['analysis_sample_rate'][i]}Hz" if data['trackAnalysis']['analysis_sample_rate'][i] != None else "(데이터 없음)")
			analysis_channels = ""
			if data['trackAnalysis']['analysis_channels'][i] == None:
				analysis_channels = "(데이터 없음)"
			elif data['trackAnalysis']['analysis_channels'][i] == 1:
				analysis_channels = "Mono"
			elif data['trackAnalysis']['analysis_channels'][i] == 2:
				analysis_channels = "Stereo"
			else:
				analysis_channels = "(측정되지 않음)"
			html += "<td align='center'>{}</td>".format(analysis_channels)
			html += "</tr>"
			html += "</table>"

			html += "<h3>- 트랙 분석</h3>"
			html += "<table border='1'; style='border-collapse: collapse; border-spacing: 0;'>"
			html += "<tr>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>리듬 안정성 수치</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>에너지 수치</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>음성 단어 수치</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>음향성 수치</th>"
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

			html += "<h3>- BART AI 추천곡</h3>"
			html += "<table border='1'; style='border-collapse: collapse; border-spacing: 0;'>"
			html += "<tr>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>#</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>트랙/수록곡</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>곡 길이</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>곡 제목</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>아티스트</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>앨범</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>발매일</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>미리 들어보기</th>"
			html += "<th align='center' style='color: grey; font-size: 12px;'>스포티파이 바로가기</th>"
			for j in range(len(bart['trackInfo']['id'])):
				html += "<tr>"
				html += "<td align='center'>{}</td>".format(j+1)
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

	html += "<br><br><br><br><br>"
	html += "<h3>- 분석 데이터 부가 설명</h3>"
	html += "<h4>* 리듬 안정성 수치(Danceability)</h4>"
	html += "템포, 리듬 안정성, 비트 강도 및 전반적인 규칙성을 포함한 음악적 요소의 조합을 기반으로 트랙이 춤을 즐기기에 얼마나 적합한지를 나타냅니다.<br>값이 0.0이면 춤을 추기 매우 부적합하고 1.0이면 춤을 추기에 매우 적합합니다."
	html += "<br>"
	html += "<h4>* 에너지 수치(Energy)</h4>"
	html += "0.0에서 1.0 사이의 척도이며 강도와 활동에 대한 지각적 척도를 나타냅니다.<br>일반적으로 에너지가 넘치는 트랙은 빠르고 시끄럽게 느껴집니다. 예를 들어, 데스 메탈은 에너지가 높은 반면 바흐의 전주곡은 낮은 점수를 받았습니다.<br>이 속성에 기여하는 지각적 특징에는 동적 범위, 인지된 음량, 음색, 시작 BPM 및 일반 엔트로피가 포함됩니다."
	html += "<br>"
	html += "<h4>* 음성 단어 수치(Speechiness)</h4>"
	html += "트랙에서 음성 단어의 존재를 감지합니다. 음성과 유사한 녹음(예: 토크쇼, 오디오북, 시)이 많을수록 값은 1.0에 가까워집니다.<br>0.66 이상의 값은 대부분이 음성으로 구성된 트랙을 나타냅니다. 0.33에서 0.66 사이의 값은 랩 음악과 같은 경우를 포함하여 섹션 또는 레이어로 음악과 음성을 모두 포함할 수 있는 트랙을 나타냅니다.<br>0.33 미만의 값은 음악 및 기타 음성과 유사한 트랙을 나타낼 가능성이 높습니다."
	html += "<br>"
	html += "<h4>* 음향성 수치(Acousticness)</h4>"
	html += "트랙이 전자 장치를 사용하지 않고 피아노나 드럼세트 등의 악기를 연주하는지 여부에 대한 0.0에서 1.0 사이의 신뢰도 측정값입니다. 1.0은 트랙이 음향적이라는 높은 신뢰도를 나타냅니다."
	html += "<br>"
	html += "<h4>* 기악곡 수치(Instrumentalness)</h4>"
	html += "트랙에 보컬이 포함되어 있지 않은지 여부를 예측합니다. 이 문맥에서는 '우'와 '아' 소리가 악기 소리로 간주됩니다. 랩이나 음성 트랙은 '보컬'입니다.<br>기악성 수치 값이 1.0에 가까울수록 트랙에 보컬 콘텐츠가 포함되지 않을 가능성이 커집니다. 0.5보다 큰 값은 기악 트랙을 나타내기 위한 것이지만 값이 1.0에 가까울수록 신뢰도가 높아집니다."
	html += "<br>"
	html += "<h4>* 라이브 수치(Liveness)</h4>"
	html += "트랙에서 청중의 존재를 감지합니다. 값이 높을수록 트랙이 라이브로 수행될 확률이 높아집니다. 0.8보다 큰 값은 트랙이 라이브 버전일 가능성이 높습니다."
	html += "<br>"
	html += "<h4>* 분위기 수치(Valence)</h4>"
	html += "트랙이 전달하는 음악적 긍정성을 설명하는 0.0에서 1.0 사이의 측정값입니다. 값이 높은 트랙은 긍정적으로 들리는 반면(예: 행복함, 쾌활함, 행복감), 값이 낮은 트랙은 부정적으로 들립니다(예: 슬픔, 우울, 화남)."
	html += "<br>"

	html += "</body>"
	html += "</html>"
	import re
	html = re.sub(r"\"", r"&quot;", html)

	response.headers['Content-Type'] = "text/html"
	return html

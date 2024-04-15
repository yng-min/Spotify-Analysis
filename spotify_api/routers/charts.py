from fastapi import APIRouter, Response, Request

from spotify_api.infrastructure import DatabaseCharts


router = APIRouter(prefix="/charts")
routes_to_reroute = ["/"]

@router.get("/global_top50", tags=["charts"])
def global_top50(response: Response, request: Request):
	data = DatabaseCharts.read()['data']

	# html 구축
	html = "<!DOCTYPE html>"
	html += "<html lang='ko'>"

	html += "<head>"
	html += "<meta charset='utf-8'>"
	html += "<title>Spotify Charts - Weekly Global Top 50</title>"
	html += "</head>"

	html += "<body>"
	html += "<h1>Spotify :: Global Top 50 (Weekly)</h1>"
	html += "<h4>마지막 업데이트: {}</h4>".format(data['chartInfo']['latestDate'])

	html += "<table border='1'; style='border-collapse: collapse; border-spacing: 0;'>"
	html += "<tr>"
	html += "<th align='center' style='color: grey; font-size: 12px;'>#</th>"
	html += "<th align='center' style='color: grey; font-size: 12px;'>#</th>"
	html += "<th align='center' style='color: grey; font-size: 12px;'>곡 제목</th>"
	html += "<th align='center' style='color: grey; font-size: 12px;'>아티스트</th>"
	html += "<th align='center' style='color: grey; font-size: 12px;'>분석 페이지</th>"
	html += "<th align='center' style='color: grey; font-size: 12px;'>스포티파이 URL</th>"
	for i in range(len(data['trackInfo']['name'])):
		rank = ""
		html += "<tr>"
		html += "<td align='center'>{}위</td>".format(data['rankInfo']['currentRank'][i])
		if data['rankInfo']['previousRank'][i] == -1:
			rank = "New"
		else:
			rank = (data['rankInfo']['previousRank'][i] - data['rankInfo']['currentRank'][i])
			if rank == 0:
				rank = "-"
			elif rank > 0:
				rank = f"↑{rank}"
			elif rank < 0:
				rank = f"↓{-rank}"
		html += "<td align='center'>{}</td>".format(rank)
		html += "<td align='center'>{}</td>".format(data['trackInfo']['name'][i])
		html += "<td align='center'>{}</td>".format(data['trackInfo']['artists'][i].replace(";;", ","))
		html += "<td align='center'><a href='{url}' target='_blank'>분석 페이지에서 보기</a></td>".format(url=str(request.url).split("charts/")[0] + "tracks/?uri=" + data['trackInfo']['url'][i].split("track/")[1])
		html += "<td align='center'><a href='{url}' target='_blank'>스포티파이에서 듣기</a></td>".format(url=data['trackInfo']['url'][i])
	html += "</tr>"
	html += "</table>"
	html += "</body>"
	html += "</html>"
	import re
	html = re.sub(r"\"", r"'", html)

	response.headers['Content-Type'] = "text/html"
	return html

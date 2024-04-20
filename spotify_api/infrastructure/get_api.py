from spotify_api.spotify_module import *


class SpotifyData:

	def __init__(self) -> None:
		pass

	def get_charts():
		charts = getGlobalWeeklyCharts()
		return charts

	def get_tracks(url: str):
		tracks = getTracks(url=url)
		return tracks

	def get_bart(reco_type: int, reco_str: str):
		bart = getBart(reco_type=reco_type, reco_str=reco_str)
		return bart
	
	def get_audioFeatures(url: str):
		features = getAudioFeatures(url=url)
		return features

	def get_audioAnalysis(url: str):
		analysis = getAudioAnalysis(url=url)
		return analysis

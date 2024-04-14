import uvicorn
from fastapi.responses import FileResponse

from spotify_api.application import create_app
from spotify_api.routers import charts, tracks


if __name__ == "__main__":
	app = create_app()
	app.include_router(charts.router)
	app.include_router(tracks.router)

	@app.get("/")
	def main():
		return FileResponse(path="spotify_api/index.html")

	uvicorn.run(app=app, host="127.0.0.1", port=8000)

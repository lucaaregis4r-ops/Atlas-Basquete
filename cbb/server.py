"""
FastAPI application for Basquete BR — Atlas Tático.
Serves analytical endpoints and static dashboard.
"""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path
from cbb.export.html_dashboard import generate_master_payload, BASE_DIR

app = FastAPI(
    title="Basquete BR — Atlas Tático API",
    description="API para scouting tático, modelagem de Markov e four factors do basquetebol brasileiro",
    version="1.0.0"
)

@app.get("/", response_class=HTMLResponse)
def get_index():
    index_file = BASE_DIR / "index.html"
    if index_file.exists():
        return HTMLResponse(content=index_file.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>Atlas de Basquete - Compile com 'python -m cbb export'</h1>")

@app.get("/api/payload")
def get_payload():
    return JSONResponse(content=generate_master_payload())

@app.get("/api/teams")
def get_teams():
    data = generate_master_payload()
    return JSONResponse(content=data["teams"])

@app.get("/api/players")
def get_players():
    data = generate_master_payload()
    return JSONResponse(content=data["players"])

@app.get("/api/markov")
def get_markov():
    data = generate_master_payload()
    return JSONResponse(content=data["markov_models"])

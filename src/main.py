import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.routes import router

load_dotenv()

app = FastAPI()
app.include_router(router)

dirname = os.path.join(os.path.dirname(__file__), "static")

app.mount("/", StaticFiles(directory=dirname, html=True), name="static")

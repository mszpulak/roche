from fastapi import FastAPI
from dotenv import load_dotenv
from src.routes import router
from fastapi.staticfiles import StaticFiles
import os

load_dotenv()

app = FastAPI()
app.include_router(router)

dirname = os.path.join(os.path.dirname(__file__), "static")

app.mount("/", StaticFiles(directory=dirname, html=True), name="static")

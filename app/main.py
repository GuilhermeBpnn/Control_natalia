from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database import Base, engine
from app.routes.web import router as web_router
import app.models  # noqa: F401

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title='StoreControl', version='1.0.0')
app.state.templates = Jinja2Templates(directory=str(BASE_DIR / 'templates'))
app.mount('/static', StaticFiles(directory=str(BASE_DIR / 'static')), name='static')

Base.metadata.create_all(bind=engine)
app.include_router(web_router)

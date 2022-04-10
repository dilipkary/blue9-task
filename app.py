from importlib.metadata import files
from typing import Optional
from routes.user import user
from routes.upload_data import files_route
from fastapi import FastAPI

app = FastAPI()

app.include_router(user)
app.include_router(files_route)

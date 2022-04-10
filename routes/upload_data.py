
from logging import raiseExceptions
import shutil
import os
from fastapi import APIRouter, File, Request, HTTPException, UploadFile, Depends, status
from auth.auth import get_current_user
from config.database import conn
from controllers.upload_data import download_files, gen_url, list_files, upload_files
from models.user import users
from schemas.user import Pub_user, User
from schemas.upload_data import Upload_data_files
from models.upload_data import Upload_Data
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi.responses import FileResponse
from sqlalchemy.sql.sqltypes import BLOB
files_route = APIRouter()


@files_route.post("/uploadfile/")
async def create_upload_file(files: List[UploadFile], user: Pub_user = Depends(get_current_user)):
    return upload_files(user, files)


@files_route.get("/downloadfile/{id}")
async def download_file(id, user: Pub_user = Depends(get_current_user)):
    return download_files(id)


@files_route.get("/generate_url/{filename}")
async def generate_url(filename, request: Request, user: Pub_user = Depends(get_current_user)):
    return gen_url(filename, request)


@files_route.get("/list/")
async def get_file_list(user: Pub_user = Depends(get_current_user)):
    return list_files()

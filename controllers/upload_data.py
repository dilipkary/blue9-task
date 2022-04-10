from email import message
import shutil
import os
from fastapi import HTTPException, status
from config.database import conn
from models.upload_data import Upload_Data
from fastapi.responses import FileResponse

ALLOWED_EXTENSIONS = set(['pptx', 'docx', 'xlsx'])


def upload_files(user, files):
    if user['usertype'] != "ops":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Not Authorised")
    current_path = os.getcwd()
    data = {}
    for file in files:
        f_name, f_ext = file.filename.split(".")

        if f_ext in ALLOWED_EXTENSIONS:
            conn.execute(Upload_Data.insert().values(
                userid=user['id'],
                filename=file.filename,
            ))
            with open(current_path+"\\files\\"+file.filename, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            data.update({"filename": f_name, "type": f_ext})
            return data
        else:
            raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                                detail=f"Media type {f_ext} not supported")


def list_files():
    file_obj = conn.execute(Upload_Data.select()).fetchall()
    data = {}
    file_list = []
    for i in file_obj:
        file_list.append(i['filename'])
    data.update({"files": file_list})
    return data


def gen_url(filename, request):
    url = request.url._url
    fileid = conn.execute(Upload_Data.select().where(
        Upload_Data.c.filename == filename)).fetchall()
    domain = url.split("generate")[0]
    return {"download_url": domain+"downloadfile/"+str(fileid[0]['id']), "message": "Success"}


def download_files(id):
    file = conn.execute(Upload_Data.select().where(
        Upload_Data.c.id == id)).fetchall()
    current_path = os.getcwd()
    file_path = os.path.join(current_path, "files/"+file[0]['filename'])
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="application/octet-stream", filename=file[0]['filename'])
    else:
        return {"error": "File dont exist"}

from distutils import extension
from pydantic import BaseModel


class Upload_data_files(BaseModel):
    id: int
    userid: int
    filename: str
    filedata: str
    extension: str

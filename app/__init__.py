from distutils import extension
from http import HTTPStatus
from http.client import BAD_REQUEST, CONFLICT, CREATED, UNSUPPORTED_MEDIA_TYPE
import json
import os
import os.path
from typing_extensions import IntVar
from zipfile import Path
from flask import (
    Flask, request, jsonify, send_from_directory
)

app = Flask(__name__)

# app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
# app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']

FILES_DIRECTORY= os.getenv('FILES_DIRECTORY')
MAX_CONTENT_LENGTH= int(os.getenv('MAX_CONTENT_LENGTH'))
ALLOWED_EXTENSIONS= os.getenv('ALLOWED_EXTENSIONS')

def write_file(extension ,file_name):
    with open(f"./files/{extension}/{file_name}", "wb") as f:
        f.write(request.data)

def create_directories():
    directories = ["./files", "./files/jpg", "./files/gif", "./files/png"]
    [os.system(f"mkdir {dir}") for dir in directories] 

def verify_exist_dirs():
    directories = ["./files", "./files/jpg", "./files/gif", "./files/png"]
    all(dir for dir in directories if os.path.isdir(dir))

def verify_exist_file_name(extension, file_name):
   return os.path.exists(f"{FILES_DIRECTORY}/{extension}/{file_name}")

try:
    if not verify_exist_dirs(): 
        raise KeyError
except KeyError:
        create_directories()
       
@app.post("/upload")
def upload():

    file = request.files.get("file")
    size = request.content_length

    try:
        file_name = file.filename
        extension = file.filename[-3::]

        if size > MAX_CONTENT_LENGTH:
            raise FileExistsError
        if not extension in ALLOWED_EXTENSIONS:
            raise TypeError
        if verify_exist_file_name(extension, file_name): 
            raise NameError

    except FileExistsError:
        return {"error": "file must have a maximum of 1mb"}, 413
    except TypeError:
        return {"error": "unsupported file type"}, 415
    except NameError:
        return {"error": "file name already exists"}, 409
    except (AttributeError, KeyError):
        return {"error": "file not found"}, 400
    else:
        write_file(extension, file_name)
        return {"message": "upload successful"}, 201

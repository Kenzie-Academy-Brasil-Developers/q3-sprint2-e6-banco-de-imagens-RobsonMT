import os
import os.path
from flask import (
    Flask, request, send_file, send_from_directory
)

from .kenzie import (
    create_directories, save_file, verify_exist_dirs,
    verify_exist_file_name,list_directorie, zip_path,
    filter_file
)

app = Flask(__name__)

MAX_CONTENT_LENGTH= int(os.getenv('MAX_CONTENT_LENGTH'))
ALLOWED_EXTENSIONS= os.getenv('ALLOWED_EXTENSIONS')

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
        extension = file_name.split(".")[1]
  
        if not extension in ALLOWED_EXTENSIONS:
            raise TypeError
        if size > MAX_CONTENT_LENGTH:
            raise FileExistsError
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
        save_file(file, extension)
        return {"message": "upload successful"}, 201


@app.get("/files")
def list_files():

    gif_files = list_directorie("gif")
    jpg_files = list_directorie("jpg")
    png_files = list_directorie("png")

    return {"gif": gif_files, "jpg": jpg_files, "png": png_files}, 200


@app.get("/files/<extension>")
def list_files_by_extension(extension:str):

    try:
        if not extension in ALLOWED_EXTENSIONS:
            raise KeyError
    except KeyError:
        return {"error": "file extention not found"}, 400
    else:
        files_by_extension = list_directorie(extension)

        return {f"{extension}": files_by_extension}, 200


@app.get("/download/<file_name>")
def download(file_name:str):

    extension = file_name.split(".")[1]
    filtered_file = filter_file(extension,file_name)
    directory = filtered_file[:11:]

    try:
        if not filtered_file: 
            raise NameError
    except NameError:
        return {"error": "file not found"}, 404
    else:
        return send_from_directory(
        directory=f".{directory}",
        path=file_name, 
        as_attachment=True
        ), 200


@app.get("/download-zip")    
def download_dir_as_query():
    file_extension = request.args.get("file_extension")
    compression_ratio = request.args.get("compression_ratio", default=6)

    try:
        if not file_extension in ALLOWED_EXTENSIONS:
            raise NameError
        if not file_extension:
            raise TypeError
        if int(compression_ratio) < 0 or int(compression_ratio) > 9:
            raise IndexError
    except NameError:
        return {"error": "file extension name not found"}, 404
    except TypeError:
        return {"error": "file extension no can he equal null. Review the query parameters"}, 400
    except IndexError:
        return {"error": "Compression rate not supported. Must be between 0 and 9"}, 400
    else:
        archive_zip = zip_path(file_extension,compression_ratio)

        return send_file(archive_zip, as_attachment=True), 200
    
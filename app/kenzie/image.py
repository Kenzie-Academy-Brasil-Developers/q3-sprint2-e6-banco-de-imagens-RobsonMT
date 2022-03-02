import glob
import os
import io
import pathlib
import zipfile

FILES_DIRECTORY= os.getenv('FILES_DIRECTORY')
DIRECTORIES= ["./files", "./files/jpg", "./files/gif", "./files/png"]

def create_directories():
    [os.system(f"mkdir {dir}") for dir in DIRECTORIES] 

def verify_exist_dirs():
    all(dir for dir in DIRECTORIES if os.path.isdir(dir))

def verify_exist_file_name(extension:str, file_name:str):
   return os.path.exists(f"{FILES_DIRECTORY}/{extension}/{file_name}")

def list_directorie(extension:str):
    return [
        file.replace(f"./files/{extension}/","") 
        for file in glob.glob(f"./files/{extension}/*{extension}")
    ]

def zip_path(extension:str):
    base_path = pathlib.Path(f"./files/{extension}")
    data = io.BytesIO()
    with zipfile.ZipFile(data, mode='w') as z:
        for f_name in base_path.iterdir():
            z.write(f_name)
    data.seek(0)
    return data

def filter_file(extension:str, file_name:str):
    filtered_file = "".join([
        f for f in 
        glob.glob(f"./files/{extension}/*{extension}") 
        if file_name in f
    ])
    return filtered_file

def save_file(file, extension:str):
    file.save(f"./files/{extension}/{file.filename}")
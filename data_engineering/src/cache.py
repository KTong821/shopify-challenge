import hashlib
import os
from datetime import datetime
from typing import List, Optional
import re
from .aws import list_obj, get_obj
from .constants import BUCKET

def check_auth_tokens() -> Optional[str]:
    token = None
    if ("token_cache.txt" in os.listdir("./")):
        print("Checking cached credentials.")
        
        with open("token_cache.txt") as file:
            token, expiry = tuple(file.read().split("\n"))
            if (datetime.strptime(expiry, "%Y-%m-%d %H:%M:%S.%f") < datetime.now()):
                print("Cached credentials expired, please authenticate.")
                token = None
            else:
                print("Cached tokens valid.")
    
    return token

def check_remote_file_hashes() -> List[str]:
    obj_list = list_obj(os.environ[BUCKET], "file_hashes")
    
    file_key = None
    
    for obj in obj_list["Contents"]:
        file_name = obj["Key"].split("/")[-1]
        if (re.match(r"file_hashes\.txt", file_name)):
            file_key = obj["Key"]
    
    if (file_key is None):
        print("No remote files found.")
        return ("", [], [])
    
    table = get_obj(os.environ[BUCKET], file_key).read().decode("utf-8")
    rows = [x.split(" ") for x in table.split("\n")][:-1]
    hashes = [x[0] for x in rows]
    file_names = [x[1] for x in rows]
    return (table, hashes, file_names)

                
def hash_file(file_path: str) -> bool:
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as file:
        for block in iter(lambda: file.read(4096), b""):
            sha256_hash.update(block)
        return sha256_hash.hexdigest() 

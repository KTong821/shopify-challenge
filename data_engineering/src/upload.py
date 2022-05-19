import os
from typing import List
from botocore.exceptions import ClientError
from .cache import check_remote_file_hashes, hash_file
from .aws import upload_obj
from .constants import BUCKET

def upload(prefix: str, files: List[str]): 
    
    remote_raw_str, remote_file_hashes, _ = check_remote_file_hashes()
    
    with open("file_hashes.txt", "w") as local_hash_cache:
        local_hash_cache.write(remote_raw_str)
        for file_name in files:
            file_path = os.path.join(prefix, file_name)
            hash_value = hash_file(file_path)
                        
            if (hash_value in remote_file_hashes):
                print(f"File {file_name} already uploaded, skipping...")
                continue
                        
            try:
                # AWS only supports single file uploads
                _ = upload_obj(file_path, os.environ[BUCKET], file_name)
            except ClientError as e:
                print(f"File upload for {file_name} failed, skipping...")
                print(e)
                continue
            
            print(f"File upload {file_name} succeeded.")
            remote_file_hashes.append(hash_value)
            local_hash_cache.write(hash_value + " " + file_name + "\n")
            
    _ = upload_obj("file_hashes.txt", os.environ[BUCKET], "file_hashes/file_hashes.txt")
    print("File upload complete!")
        
import os
from typing import List
from botocore.exceptions import ClientError
from .cache import check_remote_file_hashes, hash_file
from .aws import download_obj
from .constants import BUCKET

def download(prefix: str, files: List[str]): 
    _, remote_file_hashes, remote_file_names = check_remote_file_hashes()
    
    if (len(remote_file_hashes) == 0):
        return
    
    local_file_hashes = set(hash_file(os.path.join(prefix, file_name)) for file_name in files)
    hash_diff = set(remote_file_hashes) - local_file_hashes
    
    for remote_file_hash, remote_file_name in zip(remote_file_hashes, remote_file_names):
        if (remote_file_hash in hash_diff):
            try:
                download_obj(os.environ[BUCKET], remote_file_name,
                             prefix + "/" + remote_file_name)
            except ClientError as e:
                print(f"File download for {remote_file_name} failed, skipping:")
                print(e)
                continue
            
            print(f"File download {remote_file_name} succeeded.")
    
    print(f"File download complete!")
            
        
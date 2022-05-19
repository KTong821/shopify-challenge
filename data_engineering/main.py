import os
import sys
from src.auth import *
from src.cache import *
from src.aws import *
from src.download import *
from src.upload import *


# perform upload on specified directory
# directory to be passed as volume to docker container
def main(prefix: str):
    
    files = [file for file in os.listdir(
        prefix) if os.path.isfile(os.path.join(prefix, file)) and (".jpeg" in file or ".png" in file or ".jpg" in file)]
        
    token = check_auth_tokens()
    
    if (token is None):
        res = oauth()
        if (res is None):
            print("Authentication failed.")
            return
        token = res
                        
    print("Attempting AWS assume role.")
    
    assume_role(token)
    
    if (len(sys.argv) > 1 and sys.argv[1] == "sync"):
        print("Attempting file download.")
        download(prefix, files)    
    else:        
        print("Attempting file upload.")
        upload(prefix, files)
            

if __name__ == "__main__":    
    main("./data")
    
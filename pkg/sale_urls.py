import os
import json
import dotenv

dotenv.load_dotenv()
LOG_FILE = os.getenv("URL_FILE")

def write_to_url_file(urls: dict):
    file =  open(LOG_FILE, "w")
    file.write(json.dumps(urls))
        
def read_url_file() -> dict:
    with open(LOG_FILE, "r") as file:
        return json.loads(file.read())
        
        

import requests

def get_weahter() -> str:
    try:
        return requests.get("https://wttr.in/kyiv?1", params="format=1").text
    except:
        return "cant get weather"
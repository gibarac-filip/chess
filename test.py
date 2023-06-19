import requests
import json
import html_to_json

#my game with vlad
#url = "https://lichess.org/j3laLKRQ"

url = "https://lichess.org/api/player"
url = "https://lichess.org/api/games/user/username"
url = "https://lichess.org/api/games/user/" + MagnusCarlsen[1]

#magnus carlson names:
MagnusCarlsen = {
    "names": ["DrDrunkenstein", "DrNykterstein", "manwithavan",
    "STL_Carlsen", "MagnusCarlsen", "DannytheDonkey",
    "damnsaltythatsport", "DrGrekenstein"]
}
url = "https://lichess.org/api/games/user/" + MagnusCarlsen["names"][1]

params = {
    "pgnInJson": "True",
    "rated": "True",
     "moves": "True"
    }
response = requests.get(url, params=params)
   
all_games = []

while True:
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = html_to_json.convert(response.text)
        games = data["currentPageResults"]
        all_games.extend(games)
        if data["nbPages"] > data["currentPage"]:
            params["page"] = data["currentPage"] + 1
        else:
            break
    else:
        print("Error:", response.status_code)
        break

print("Total Games:", len(all_games))
import hashlib

import requests

with open("fisier.txt", "rb") as f:
    bytes = f.read()
    hash = hashlib.sha256(bytes).hexdigest()
    print("sha256 value: ", hash)

url = "https://www.virustotal.com/api/v3/files"

files = {"file": ("fisier.txt", open("fisier.txt", "rb"), "txt")}
headers = {
    "accept": "application/json",
    "x-apikey": "21d922a3798ab6fff0ea3c47cc2c6e60b0c1a74c4de28a73bcbd30d51b70ba90"
}

response = requests.post(url, files=files, headers=headers)

print(response.text)


url2 = "https://www.virustotal.com/api/v3/analyses/ZDMyMmY0MjY1MWNiZDE1MTkwY2ZmMjg1NGU0NDk0MTM6MTY4MzcxNTA4Ng=="

headers2 = {
    "accept": "application/json",
    "x-apikey": "21d922a3798ab6fff0ea3c47cc2c6e60b0c1a74c4de28a73bcbd30d51b70ba90"
}

response2 = requests.get(url2, headers=headers2)

print(response2.text)
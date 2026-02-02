import requests

BASE = "http://127.0.0.1:8080"

url = f"{BASE}/api/v1/index/create"

payload = {
    "index_name": "mindmap",
    "dim": 384,
    "space_type": "cosine",
    "precision": "float32"
}

r = requests.post(url, json=payload)

print("Status Code:", r.status_code)
print("Response:", r.text)



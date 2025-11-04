import requests

login = requests.post("http://127.0.0.1:5001/login", json={
    "usuario": "joaovitorvlb@hotmail.com",
    "senha": "1234"
})

print("Resposta do servidor:", login.text)
print("Status:", login.status_code)

token = login.json()["token"]
print("Token:", token)

headers = {"Authorization": f"Bearer {token}"}

response = requests.get("http://127.0.0.1:5001/produtos", headers=headers)

print("Status:", response.status_code)
print("Resposta:", response)

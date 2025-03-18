import requests

BASE_URL = "http://192.168.1.81:8000/api"

def login(tel, password):
    url = f"{BASE_URL}/login/"
    data = {"tel": tel, "password": password}
    response = requests.post(url, json=data)
    print("Statut HTTP :", response.status_code)
    print("Contenu brut :", response.text)  # Afficher la réponse brute

    return response.json() if response.status_code == 200 else None

if __name__ == "__main__":
    # Remplace par un utilisateur existant
    tel = "064838270"
    password = "user123"

    tokens = login(tel, password)
    print("Réponse du serveur :", tokens)

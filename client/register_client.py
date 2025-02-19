import requests

BASE_URL = "http://127.0.0.1:8000/api"

def signup(tel, password, role):
    url = f"{BASE_URL}/register/"
    data = {
        "tel": tel,
        "password": password,
        "status": role
    }
    response = requests.post(url, json=data)

    print("Statut HTTP :", response.status_code)
    print("Contenu brut :", response.text)  # Voir la réponse du serveur

    return response.json() if response.status_code == 201 else None

if __name__ == "__main__":
    new_user = signup("064838270", "user123", "client")
    print("Réponse du serveur :", new_user)

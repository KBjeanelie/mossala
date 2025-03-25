import requests

BASE_URL = "http://192.168.1.81:8000/api"

def signup(tel, password):
    url = f"{BASE_URL}/register/"
    data = {
        "lastname": "ITOUA",
        "firstname": "Yannick",
        "tel": tel,
        "password": password,
    }
    response = requests.post(url, json=data)

    print("Statut HTTP :", response.status_code)
    print("Contenu brut :", response.text)  # Voir la réponse du serveur

    return response.json() if response.status_code == 201 else None

if __name__ == "__main__":
    new_user = signup("064838070", "user123",)
    print("Réponse du serveur :", new_user)

# Nama  : Dodi Wijaya
# NIM   : F1D02310047
# Kelas : (Isi Kelas)

import requests

BASE_URL = "https://api.pahrul.my.id/api/posts"


class ApiService:

    @staticmethod
    def get_posts():
        response = requests.get(BASE_URL, timeout=10)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_post(post_id):
        response = requests.get(
            f"{BASE_URL}/{post_id}",
            timeout=10
        )

        response.raise_for_status()
        return response.json()

    @staticmethod
    def create_post(data):
        response = requests.post(
            BASE_URL,
            json=data,
            timeout=10
        )

        response.raise_for_status()
        return response.json()

    @staticmethod
    def update_post(post_id, data):
        response = requests.put(
            f"{BASE_URL}/{post_id}",
            json=data,
            timeout=10
        )

        response.raise_for_status()
        return response.json()

    @staticmethod
    def delete_post(post_id):
        response = requests.delete(
            f"{BASE_URL}/{post_id}",
            timeout=10
        )

        response.raise_for_status()
        return response.json()
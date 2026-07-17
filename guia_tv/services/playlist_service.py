import requests


class PlaylistService:

    @staticmethod
    def download(url):

        response = requests.get(
            url,
            timeout=30
        )

        response.raise_for_status()

        return response.text
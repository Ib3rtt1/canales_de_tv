import requests


class PlaylistService:

    def download(self, source):

        response = requests.get(
            source.url,
            timeout=60
        )

        response.raise_for_status()

        return response.text
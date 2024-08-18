import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from django.conf import settings


class MovieAPIService:
    def __init__(self):
        self.base_url = settings.MOVIE_API_URL
        self.auth = (settings.MOVIE_API_USERNAME, settings.MOVIE_API_PASSWORD)
        self.session = requests.Session()
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

    def get_movies(self, page=1):
        try:
            response = self.session.get(
                f"{self.base_url}?page={page}", auth=self.auth, verify=False
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return None

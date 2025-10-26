import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from django.conf import settings


class MovieAPIService:
    def __init__(self):
        self.base_url = "http://www.omdbapi.com/"
        self.api_key = settings.OMDB_API_KEY
        self.session = requests.Session()
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

    def get_movies(self, page=1, search_term="movie"):
        try:
            import ipdb; ipdb.set_trace()
            response = self.session.get(
                self.base_url,
                params={
                    "apikey": self.api_key,
                    "s": search_term,
                    "page": page,
                    "type": "movie"
                },
                verify=False
            )
            response.raise_for_status()
            result = response.json()
            return {
                "results": result.get("Search", []),
                "total_results": int(result.get("totalResults", 0)),
                "page": page
            } if result.get("Response") == "True" else None
        except requests.exceptions.RequestException as e:
            return None

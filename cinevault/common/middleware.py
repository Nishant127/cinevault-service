from django.core.cache import cache


class RequestCounterMiddleware(object):
    REQUEST_COUNT_KEY = "request_count"

    def __init__(self, get_response):
        self.get_response = get_response
        if cache.get(self.REQUEST_COUNT_KEY) is None:
            cache.set(self.REQUEST_COUNT_KEY, 0)

    def __call__(self, request):
        cache.incr(self.REQUEST_COUNT_KEY, delta=1)
        response = self.get_response(request)
        return response

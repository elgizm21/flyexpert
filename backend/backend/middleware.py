import logging

logger = logging.getLogger('django')

class RequestLoggingMiddleware:
    """ 🔹 Bütün requestləri və errorları log faylına yazır. """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(f"📌 REQUEST: {request.method} {request.path}")
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        logger.error(f"❌ ERROR: {exception}", exc_info=True)

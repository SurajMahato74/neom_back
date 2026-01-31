import logging
import time
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to log all incoming requests and responses
    """
    
    def process_request(self, request):
        request.start_time = time.time()
        
        # Log request details
        logger.info(f"Request: {request.method} {request.get_full_path()} "
                   f"from {request.META.get('REMOTE_ADDR')} "
                   f"User-Agent: {request.META.get('HTTP_USER_AGENT', 'Unknown')}")
        
        # Log CORS headers for debugging
        origin = request.META.get('HTTP_ORIGIN')
        if origin:
            logger.info(f"CORS Origin: {origin}")
    
    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            logger.info(f"Response: {response.status_code} for {request.method} "
                       f"{request.get_full_path()} in {duration:.3f}s")
        
        # Log CORS response headers
        cors_headers = {
            'Access-Control-Allow-Origin': response.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.get('Access-Control-Allow-Headers'),
        }
        
        if any(cors_headers.values()):
            logger.debug(f"CORS Response Headers: {cors_headers}")
        
        return response
    
    def process_exception(self, request, exception):
        logger.error(f"Exception in {request.method} {request.get_full_path()}: "
                    f"{type(exception).__name__}: {str(exception)}")
        return None
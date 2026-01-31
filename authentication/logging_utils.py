import logging
import functools
from django.http import JsonResponse

def get_logger(name):
    """Get a logger instance for the given name"""
    return logging.getLogger(name)

def log_api_call(func):
    """Decorator to log API function calls"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        logger.info(f"Calling {func.__name__} with args: {args[1:]} kwargs: {kwargs}")
        
        try:
            result = func(*args, **kwargs)
            logger.info(f"{func.__name__} completed successfully")
            return result
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            raise
    
    return wrapper

def log_database_query(model_name, operation, **kwargs):
    """Log database operations"""
    logger = logging.getLogger('authentication.database')
    logger.info(f"Database {operation} on {model_name}: {kwargs}")

def log_cors_error(request, error_msg):
    """Log CORS related errors"""
    logger = logging.getLogger('authentication.cors')
    origin = request.META.get('HTTP_ORIGIN', 'Unknown')
    user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
    
    logger.error(f"CORS Error: {error_msg} | Origin: {origin} | User-Agent: {user_agent}")

def create_error_response(message, status_code=400):
    """Create standardized error response with logging"""
    logger = logging.getLogger('authentication.errors')
    logger.error(f"API Error Response: {message} (Status: {status_code})")
    
    return JsonResponse({
        'error': True,
        'message': message,
        'status_code': status_code
    }, status=status_code)
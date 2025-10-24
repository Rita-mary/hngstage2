from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.exceptions import ValidationError

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if isinstance(exc, ValidationError) and response is not None:
        response.data = {
            "error": "Validation failed",
            "details": response.data
        }
        response.status_code = status.HTTP_400_BAD_REQUEST
    return response

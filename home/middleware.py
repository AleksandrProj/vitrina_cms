from django.contrib import messages
from django.shortcuts import redirect

from backend.exceptions import UsageException


class ErrorHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, UsageException):
            messages.error(request, exception.message)
            queryparams = ''
            if request.META.get("QUERY_STRING", ''):
                queryparams = "?" + request.META.get("QUERY_STRING")
            return redirect(request.path + queryparams)

from  ..constants.default_values import ResponseMessageType
from django.http import JsonResponse

def success_response(message: str, data: dict = None, redirect: str = None, message_type: str = ResponseMessageType.SUCCESS.value) -> dict:
    if data is None:
        data = {}
    response = {
        "success": True,
        "data": data,
        "message_type": message_type,
        "message": message,
    }
    if redirect:
        response["redirect"] = redirect
    return response


def error_response(message: str, data: dict = dict(), message_type: str = ResponseMessageType.ERROR.value, stack_trace: str = "") -> dict:
    return {
        "error": True,
        "data": data,
        "message": message,
        "message_type": message_type,
        "stack_trace": stack_trace,
    }


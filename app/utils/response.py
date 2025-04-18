from fastapi import HTTPException
from fastapi.responses import JSONResponse
from typing import Any


# def success_response(data: Any = None, message: str = "Success"):
#     return JSONResponse(
#         status_code=200,
#         content={
#             "status": "success",
#             "message": message,
#             "data": data,
#         },
#     )

def success_response(data=None, message="Success",pagination=None, **extra):
    response = {
        "status": "success",
        "message": message,
        "data": data,
    }
    if pagination:
        response["pagination"] = pagination
    response.update(extra)
    return response

def error_response(message: str = "An error occurred", status_code: int = 400):
    raise HTTPException(
        status_code=status_code,
        detail={
            "status": "error",
            "message": message,
        },
    )

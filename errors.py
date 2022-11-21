import json

from aiohttp import web


class APIError(web.HTTPException):

    def __init__(
        self, 
        error_msg, 
        *args,
        **kwargs
    ) -> None:
        super().__init__(
            *args,
            **kwargs,
            text = json.dumps({'error': error_msg}), 
            content_type = 'application/json'
        )


class NotFound(APIError):
    status_code = 404


class BadRequest(APIError):
    status_code = 400
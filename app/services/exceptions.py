from fastapi import Request
from fastapi.responses import JSONResponse


class GenerationException(Exception):
    def __init__(self):
        self.name = 'generation exception'
        self.detail = "превышено допустимое количество генераций."

class ValidationException(Exception):
    def __init__(self):
        self.name = 'validation exception'
        self.detail = "not validated."
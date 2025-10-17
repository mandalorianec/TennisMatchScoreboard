from typing import Mapping
from tennis_match_scoreboard.src.dto.request_dto import RequestDTO
from urllib.parse import parse_qs


def _parse_body(environ):
    try:
        content_length = environ.get("CONTENT_LENGTH", "0")
        body_length = _get_body_length(content_length)
        # Если длина 0 - возвращаем пустой словарь
        if body_length == 0:
            return {}

        # Читаем тело запроса
        body_bytes = environ["wsgi.input"].read(body_length)

        # Декодируем и парсим
        body_str = body_bytes.decode("utf-8")
        body = parse_qs(body_str)

        return body

    except (ValueError, UnicodeDecodeError, KeyError):
        return {}


def _get_body_length(content_length) -> int:
    # Если CONTENT_LENGTH пустой или не число - считаем длину 0
    if not content_length:
        body_length = 0
    else:
        body_length = int(content_length)

    # Проверяем валидность длины
    if body_length < 0:
        body_length = 0
    elif body_length > 1024 * 1024:  # Ограничение 1MB
        raise ValueError("Request body too large")
    return body_length


class RequestParser:
    @staticmethod
    def parse_request(environ: Mapping[str, str]) -> RequestDTO:
        method = environ.get("REQUEST_METHOD", "").upper()

        query_params = parse_qs(environ.get("QUERY_STRING", ""))
        if method == 'POST':
            body = _parse_body(environ)
            return RequestDTO(method, query_params, body)
        return RequestDTO(method, query_params)

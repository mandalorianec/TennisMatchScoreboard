from pathlib import Path
from typing import Mapping
from dotenv import load_dotenv
import os
from src.config import allow_origins_env
from src.dto.response_dto import ResponseDto
from src.exceptions.own_exceptions import ControllerNotFoundException, UnsupportedMethodException
from src.utils.render import Render
from src.utils.request_parser import RequestParser
from src.routing.router import Router
from src.utils.logger import get_logger, setup_logging
from src.utils.container import Container

setup_logging()
logger = get_logger()
load_dotenv()


class Application:
    def __init__(self):
        current_dir = Path(__file__).parent
        self.static_dir = str(current_dir / 'views' / 'static')
        self.parser = RequestParser()
        self.render = Render()
        self.allowed_origins = self._make_allowed_origins()
        self.containers = Container()
        self.router = Router(self.containers)

        logger.info("init app")

    def __call__(self, environ: Mapping[str, str], start_response):

        try:
            return self._handle_request(environ, start_response)
        except UnsupportedMethodException as e:
            logger.warning(f"Unsupported method: {e.error_message}")
            return self._handle_exception(e.error_code, e.error_message, start_response)
        except ControllerNotFoundException as e:
            logger.warning(f"Controller not found: {e.error_message}")
            return self._handle_exception(e.error_code, e.error_message, start_response)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            return self._handle_exception("500 Internal Server Error", "Ошибка на стороне сервера", start_response)

    def serve_static(self, path_info, start_response):  # на сервере это делает nginx
        file_path = path_info[8:]
        file_type = file_path.split('.')[-1]
        full_path = Path(self.static_dir) / file_path
        content = full_path.read_bytes()
        if len(content) > 0:
            status = '200 OK'
        else:
            status = '404 Not Found'
        logger.debug(file_type)
        logger.debug(status)
        start_response(status, [('Content-Type', f'text/{file_type}')])
        return [content]

    def _handle_exception(self, error_code: str, error_message: str, start_response):
        logger.error(f"Handling exception: {error_code}: {error_message}")
        rendered_html = self.render.render_template("error.html", {
            "error_code": error_code,
            "error_message": error_message
        })
        start_response(error_code, [('Content-Type', 'text/html')])
        return [rendered_html.encode("utf-8")]

    def _handle_request(self, environ: Mapping[str, str], start_response):
        path_info = environ.get("PATH_INFO", "/").lower()

        if path_info.startswith('/static/'):
            return self.serve_static(path_info, start_response)

        request_dto = self.parser.parse_request(environ)
        logger.info(f"{request_dto.method} - path_info: {path_info}")

        if request_dto.method.upper() == 'OPTIONS':
            return self._handle_options(environ, start_response)

        controller = self.router.find_controller(path_info)
        logger.debug(f"Found controller for {path_info}")

        response_dto = Router.perform(controller, request_dto)
        logger.info(f"Response code: {response_dto.status}")

        headers = self._get_headers(environ, response_dto)

        start_response(response_dto.status, headers)
        return [response_dto.body.encode("utf-8")]

    def _handle_options(self, environ: Mapping[str, str], start_response):
        """Обрабатывает OPTIONS запросы для CORS preflight"""
        cors_headers = self._get_cors_headers(environ)
        start_response('200 OK', cors_headers)
        return [b'']

    @staticmethod
    def _make_allowed_origins():
        if allow_origins_env:
            return [origin.strip() for origin in allow_origins_env.split(',')]

        return set()

    def _get_cors_headers(self, environ: Mapping[str, str]):
        cors_headers = [
            ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
            ('Access-Control-Allow-Headers', 'Content-Type')
        ]
        origin = environ.get("HTTP_ORIGIN")
        if origin and origin in self.allowed_origins:
            cors_headers.append(('Access-Control-Allow-Origin', origin))

        return cors_headers

    def _get_headers(self, environ: Mapping[str, str], response_dto: ResponseDto):
        cors_headers = self._get_cors_headers(environ)
        return response_dto.headers + cors_headers


app = Application()

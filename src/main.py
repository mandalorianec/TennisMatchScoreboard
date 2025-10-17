from wsgiref.simple_server import make_server
from application import app
from src.utils.logger import get_logger

HOST, PORT = '127.0.0.1', 5500

if __name__ == '__main__':
    logger = get_logger()
    logger.info(f"serving on http://{HOST}:{PORT}")
    httpd = make_server(HOST, PORT, app)
    httpd.serve_forever()

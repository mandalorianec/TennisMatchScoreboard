import logging
import logging.config
import os
from pathlib import Path


def setup_logging():
    """Настройка логирования для всего приложения"""

    # Создаем папку для логов если ее нет
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(exist_ok=True)

    # Проверяем флаг отключения логирования
    if os.getenv('DISABLE_LOGGING', 'false').lower() == 'true':
        logging.getLogger().setLevel(logging.CRITICAL)
        return


    # Конфигурация логирования
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
            'detailed': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
            },
        },
        'handlers': {
            'file': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': log_dir / 'app.log',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5,
                'formatter': 'detailed',
                'encoding': 'utf-8'
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'stream': 'ext://sys.stdout'
            },
            'error_file': {
                'level': 'ERROR',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': log_dir / 'errors.log',
                'maxBytes': 10485760,
                'backupCount': 5,
                'formatter': 'detailed',
                'encoding': 'utf-8'
            }
        },
        'loggers': {
            '': {  # Корневой логгер
                'handlers': ['console', 'file', 'error_file'],
                'level': 'DEBUG',
                'propagate': True
            },
            'src': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': False
            },
        }
    }

    logging.config.dictConfig(logging_config)


def get_logger(name=None):
    """Получить логгер с указанным именем"""
    return logging.getLogger(name)
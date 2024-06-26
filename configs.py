import argparse
import logging
from logging.handlers import RotatingFileHandler

from constants import BASE_DIR, DATETIME_FORMAT, LOG_FORMAT


def configure_argument_parser(available_modes: dict) -> argparse:
    """configurate of command args"""
    parser = argparse.ArgumentParser(description='Парсер Категорий магазина Metro')
    parser.add_argument(
        'mode',
        choices=available_modes,
        help='Режимы работы парсера'
    )
    parser.add_argument(
        '-c',
        '--clear-cache',
        action='store_true',
        help='Очистка кеша'
    )
    # Новый аргумент.
    parser.add_argument(
        '-o',
        '--output',
        choices=('pretty', 'file'),
        help='Дополнительные способы вывода данных'
    )
    return parser


def configure_logging() -> None:
    """logging of parser"""
    log_dir = BASE_DIR / 'logs'
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / 'parser.log'

    rotating_handler = RotatingFileHandler(
        log_file, maxBytes=10 ** 6, backupCount=5
    )
    logging.basicConfig(
        datefmt=DATETIME_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler())
    )

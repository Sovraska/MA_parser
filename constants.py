from pathlib import Path
from time import strftime

BASE_DIR = Path(__file__).parent

METRO_CATEGORIES = ['Фрукты', 'Овощи']

MAIN_DOC_URL = "https://online.metro-cc.ru"

DATETIME_FORMAT = strftime('%Y-%m-%d_%H-%M-%S')

LOG_FORMAT = '%(asctime)s %(message)s'

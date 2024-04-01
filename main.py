import logging

import requests_cache
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from constants import MAIN_DOC_URL, METRO_CATEGORIES
from configs import configure_argument_parser, configure_logging
from outputs import control_output
from utils import get_response, find_tag


def get_category(session: requests_cache) -> list:
    """take all versions + their statuses"""
    results = [('id', 'имя', 'ссылка', 'регулярная цена', 'промо цена')]
    for category in METRO_CATEGORIES:
        page = 0
        while True:
            if not page:
                metro_url = urljoin(MAIN_DOC_URL, f'/search?q={category}')
            else:
                metro_url = urljoin(MAIN_DOC_URL, f'/search?q={category}&page={page}')

            response = get_response(session, metro_url)
            response.encoding = '-utf-8'

            soup = BeautifulSoup(response.text, features='lxml')
            main_div = find_tag(soup, 'div', attrs={'id': 'products-inner'})
            all_carts = main_div.find_all('div', recursive=False)

            for cart in all_carts:
                if 'Раскупили' in cart.text:
                    continue
                _id = cart['id']
                name = find_tag(cart, 'span', attrs={'class': 'product-card-name__text'}).text
                name = name.replace('\n', '').replace('  ', '').split(',')[0]
                url = find_tag(cart, 'a', attrs={'class': 'product-card-photo__link reset-link'})['href']
                url = MAIN_DOC_URL + url
                actual_price_div = find_tag(cart, 'div', attrs={'class': 'product-unit-prices__actual-wrapper'})
                actual_price = find_tag(actual_price_div, 'span', attrs={'class': 'product-price__sum-rubles'}).text
                promo_price_div = find_tag(cart, 'div', attrs={'class': 'product-unit-prices__old-wrapper'})
                promo_price = promo_price_div.find('span', attrs={'class': 'product-price__sum-rubles'})
                if promo_price:
                    promo_price = promo_price.text

                results.append((_id, name, url, actual_price, promo_price))
            if page >= 3:
                break
            page += 1
    return results


MODE_TO_FUNCTION = {
    'get_category': get_category,
}


def main() -> None:
    """main func for run the parser"""
    configure_logging()
    logging.info('Парсер запущен!')

    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()

    logging.info(f'Аргументы командной строки: {args}')

    session = requests_cache.CachedSession()

    if args.clear_cache:
        session.cache.clear()
    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)

    if results is not None:
        control_output(results, args)
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()

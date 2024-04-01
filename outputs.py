# outputs.py
import logging

from prettytable import PrettyTable
from constants import BASE_DIR, DATETIME_FORMAT
import datetime as dt
import csv


def control_output(results, cli_args):
    """controlling type of output"""
    output = cli_args.output
    if output == 'pretty':
        pretty_output(results)
    elif output == 'file':
        file_output(results, cli_args)
    else:
        default_output(results)


def default_output(results):
    """default output"""
    for row in results:
        print(*row)


def pretty_output(results):
    """output uses PrettyTable"""
    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(results, cli_args):
    """output in file with time mark"""
    downloads_dir = BASE_DIR / 'results'
    results_dir = downloads_dir.mkdir(exist_ok=True)

    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = f'{BASE_DIR}/results/{file_name}'

    with open(file_path, 'w', encoding='utf-8') as file:
        writer = csv.writer(file, dialect='unix')
        writer.writerows(results)

    logging.info(f'Файл с результатами был сохранён: {file_path}')

#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Для своего варианта лабораторной работы 2.17 добавьте
# возможность хранения файла данныхв домашнем каталоге
# пользователя. Для выполнения операций с файлами
# необходимоиспользовать модуль pathlib .
# Вариант 29


import argparse
import json
import os.path
import pathlib


# Вариант 29
def add_route(staff, start, end, number):
    '''
    Добавить маршрут
    '''
    staff.append({
        'name_start': start,
        'name_end': end,
        'number': number
    })
    return staff


def list(routes):
    '''
    Вывести список маршрутов
    '''
    if routes:
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 30,
            '-' * 8
        )
        print(line)

        print('| {:^4} | {:^30} | {:^30} | {:^8} |'.format(
            "№",
            "Начальный пункт",
            "Конечный пункт",
            "Номер"
        )
        )
        print(line)

        for idx, route in enumerate(routes, 1):
            print('| {:>4} | {:<30} | {:<30} | {:>8} |'.format(
                idx,
                route.get('name_start', ''),
                route.get('name_end', ''),
                route.get('number', 0)
            )
            )
            print(line)
    else:
        print("Список маршрутов пуст.")


def save_routes(file_name, staff):
    """
    Сохранить все маршруты в файл JSON.
    """
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(staff, fout, ensure_ascii=False, indent=4)


def load_routes(file_name):
    """
    Загрузить все маршруты из файла JSON.
    """
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def select_routes(routes, command):
    '''
    Вывести выбранные маршруты
    '''
    station = command
    count = 0

    for route in routes:
        if (station.lower() == route["name_start"].lower() or
                station == route["name_end"].lower()):

            count += 1
            print('{:>4}: {}-{}, номер маршрута: {}'.format(count,
                  route["name_start"], route["name_end"], route["number"]))

    if count == 0:
        print("Маршрут не найден.")


def main(command_line=None):
    '''
    Основная функция
    '''
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename",
        action="store",
        help="The data file name"
    )
    file_parser.add_argument(
        "-g",
        "--general",
        action="store_true",
        help="Save file in general directory"
    )
    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("routes")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    subparsers = parser.add_subparsers(dest="command")
    # Создать субпарсер для добавления маршрута.
    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new route"
    )
    add.add_argument(
        "-s",
        "--start",
        action="store",
        required=True,
        help="Start position on route"
    )
    add.add_argument(
        "-e",
        "--end",
        action="store",
        help="End position on route"
    )
    add.add_argument(
        "-n",
        "--number",
        action="store",
        type=int,
        required=True,
        help="Number of route"
    )
    # Создать субпарсер для отображения всех маршрутов.
    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all routes"
    )
    # Создать субпарсер для выбора маршрутов.
    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select the routes"
    )
    select.add_argument(
        "-t",
        "--station",
        action="store",
        type=str,
        required=True,
        help="Routes with this station"
    )
    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)
    # Загрузить все маршруты из файла, если файл существует.
    is_dirty = False

    filepath = pathlib.Path.cwd() / args.filename
    if args.general:
        filepath = pathlib.Path.home() / args.filename
    if os.path.exists(filepath):
        routes = load_routes(filepath)
    else:
        routes = []

    # Добавить маршрут.
    if args.command == "add":
        if(routes is None):
            routes = []
        routes = add_route(
            routes,
            args.start,
            args.end,
            args.number
        )
        is_dirty = True
    # Отобразить все маршруты.
    elif args.command == "display":
        list(routes)

    # Выбрать требуемые маршруты.
    elif args.command == "select":
        select_routes(routes, args.station)
        print(args.station)
    # Сохранить данные в файл, если список маршрутов был изменен.
    if is_dirty:
        save_routes(filepath, routes)


if __name__ == '__main__':
    main()

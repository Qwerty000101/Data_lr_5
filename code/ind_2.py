#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Разработайте аналог утилиты tree в Linux.
# Используйте возможности модуля argparse для
# управления отображением дерева каталогов файловой
# системы. Добавьте дополнительные
# уникальные возможности в данный программный продукт.


import argparse
from pathlib import Path
import os
import datetime


def tree(directory, indent='', max_depth=0, current_depth=0,
         only_dirs=False, only_files=False, show_time=False,
         show_extension=True):
    if current_depth > max_depth:
        return

    for item in sorted(directory.iterdir(),
                       key=lambda item: (item.is_file(), item.name.lower())):
        if item.is_dir():
            if only_files:
                continue
            print(f"{indent}{item.name}/")
            tree(item, indent + '  ', max_depth, current_depth + 1,
                 only_dirs, only_files, show_time, show_extension)

        elif not only_dirs:
            file_info = (item.name if show_extension
                         else os.path.splitext(item.name)[0])

            if show_time:
                cr_time = datetime.datetime.fromtimestamp(
                    item.stat().st_ctime)
                file_info += (f" (Created: "
                              f"{cr_time.strftime('%Y-%m-%d %H:%M:%S')})")

            print(indent + file_info)


def main():
    '''
    Основная функция
    '''
    parser = argparse.ArgumentParser(description='"Tree"')
    parser.add_argument('directory', nargs='?', default='.', type=Path,
                        help='Start directory (default: current directory)')
    # Добавление параметра, задающего уровень вложенности
    parser.add_argument('--depth', type=int, default=0,
                        help='Maximum display depth of the directory tree')
    # Добавление параметра, отвечающего за отображение только директорий
    parser.add_argument('--dirs', action='store_true',
                        help='Display only directories')
    # Добавление параметра, отвечающего за отображение только файлов
    parser.add_argument('--files', action='store_true',
                        help='Display only files')
    # Добавление параметра, отвечающего за отображение времени создания файла
    parser.add_argument('--time', action='store_true',
                        help='Display file creation times')
    # Добавление параметра, отвечающего за отображение расширений файлов
    parser.add_argument('--extension', action='store_true',
                        help='Hide file extensions')

    args = parser.parse_args()

    if not args.directory.is_dir():
        print('Error: The specified directory does not exist.')
        return

    tree(args.directory, max_depth=args.depth, only_dirs=args.dirs,
         only_files=args.files, show_time=args.time,
         show_extension=args.extension)


if __name__ == '__main__':
    main()

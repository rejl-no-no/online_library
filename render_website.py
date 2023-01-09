import argparse
import json
import os

from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import select_autoescape
from livereload import Server
from livereload import shell
from more_itertools import chunked


site = argparse.ArgumentParser(description='Создание сайта по данным из файла .json')
site.add_argument('--content', default = 'page_content_json.json', help='Файл с данными для создания сайта')
args = site.parse_args()


def rebuild():
    cards_on_the_page = 10
    number_of_columns = 2

    env = Environment(loader=FileSystemLoader('.'), autoescape=select_autoescape(['html', 'xml']))
    template = env.get_template('template.html')

    with open(args.content, 'r', encoding='utf8') as file:
        books_json = file.read()
    book_descriptions = json.loads(books_json)

    os.makedirs(f'pages', exist_ok=True)
    pages = list(chunked(book_descriptions, cards_on_the_page))

    for num, page in enumerate(pages, start = 1):
        rendered_page = template.render(
            books=list(chunked(page, number_of_columns)),
            pages = range(1, len(pages)+1),
            current_page = num
        )
        with open(f'./pages/index{num}.html', 'w', encoding='utf8') as file:
            file.write(rendered_page)


def main():

    rebuild()

    server = Server()
    server.watch('template.html', rebuild)
    server.serve(root='.')


if __name__ == '__main__':
    main()
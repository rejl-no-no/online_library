import argparse
import json
import os

from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import select_autoescape
from livereload import Server
from livereload import shell
from more_itertools import chunked


def rebuild():
    number_of_cards = 10
    number_of_columns = 2

    env = Environment(loader=FileSystemLoader('.'), autoescape=select_autoescape(['html', 'xml']))
    template = env.get_template('template.html')

    with open(get_json(), 'r', encoding='utf8') as file:
        book_descriptions = json.load(file)

    os.makedirs(f'pages', exist_ok=True)
    pages = list(chunked(book_descriptions, number_of_cards))

    for num, page in enumerate(pages, start = 1):
        rendered_page = template.render(
            books=list(chunked(page, number_of_columns)),
            pages = range(1, len(pages)+1),
            current_page = num
        )
        with open(f'./pages/index{num}.html', 'w', encoding='utf8') as file:
            file.write(rendered_page)


def get_json():
    site = argparse.ArgumentParser(description='Создание сайта по данным из файла .json')
    site.add_argument('--content', default = 'page_content_json.json', help='Файл с данными для создания сайта')
    args = site.parse_args()

    return(args.content)
    

def main():
    rebuild()

    server = Server()
    server.watch('template.html', rebuild)
    server.serve(root='.')


if __name__ == '__main__':    
    main()

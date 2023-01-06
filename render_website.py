from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
from livereload import Server, shell 
from more_itertools import chunked
import os

def rebuild():
    print("Site rebuilt")

    env = Environment(loader=FileSystemLoader('.'), autoescape=select_autoescape(['html', 'xml']))
    template = env.get_template('template.html')

    with open("page_content_json.json", "r", encoding='utf8') as file:
        books_json = file.read()
    books = json.loads(books_json)

    os.makedirs(f'static', exist_ok=True)
    pages = list(chunked(books, 10))

    for num, page in enumerate(pages, start = 1):
        rendered_page = template.render(
            books=list(chunked(page, 2)),
            pages = range(1, len(pages)+1),
            current_page = num
        )
        with open(f'./static/index{num}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


rebuild()

server = Server()
server.watch('template.html', rebuild)

server.serve(root='.')





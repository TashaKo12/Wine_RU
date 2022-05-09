from datetime import datetime
import collections

from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
from pandas import read_excel


def main():
    creation_year = 1920
    winery_age = datetime.now().year - creation_year

    env = Environment(
            loader=FileSystemLoader('.'),
            autoescape=select_autoescape(['html', 'xml'])
        )
    
    wines = read_excel(
                'wine.xlsx',
                keep_default_na=False,
                na_values=None
            ).to_dict(orient="records")

    grouped_wines = collections.defaultdict(list)

    for wine in wines:
        grouped_wines[wine["Категория"]].append(wine)

    template = env.get_template('template.html')

    rendered_page = template.render(
                        winery_age=winery_age,
                        grouped_wines=grouped_wines
                    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(
                ('0.0.0.0', 8000),
                SimpleHTTPRequestHandler
            )
    server.serve_forever()


if __name__ == "__main__":
    main()

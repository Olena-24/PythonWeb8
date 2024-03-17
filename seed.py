
import json
from mongoengine.errors import NotUniqueError
from models import Author, Quote

def load_authors_from_file(filename):
    with open(filename, encoding='utf-8') as file:
        data_authors = json.load(file)
        for author_data in data_authors:
            try:
                author = Author(fullname=author_data.get('fullname'),
                                born_date=author_data.get('born_date'),
                                born_location=author_data.get('born_location'),
                                description=author_data.get('description'))
                author.save()
            except NotUniqueError:
                print(f"Author already exists: {author_data.get('fullname')}")

def load_quotes_from_file(filename):
    with open(filename, encoding='utf-8') as file:
        data_quotes = json.load(file)
        for quote_data in data_quotes:
            author, *_ = Author.objects(fullname=quote_data.get('author'))
            quote = Quote(quote=quote_data.get('quote'), tags=quote_data.get('tags'), author=author)
            quote.save()

if __name__ == '__main__':
    load_authors_from_file('authors.json')
    load_quotes_from_file('quotes.json')
import connect
import json
from models import Author, Quote

def import_authors():
    with open('authors_and_quotes/authors.json', 'r', encoding = 'utf-8') as file:
        authors_data = json.load(file)
        for author_data in authors_data:
            author = Author(**author_data)
            author.save()

def import_quotes():
    with open('authors_and_quotes/quotes.json', 'r', encoding = 'utf-8') as file:
        quotes_data = json.load(file)
        for quote_data in quotes_data:
            author_name = quote_data['author']
            author = Author.objects(fullname=author_name).first()
            if author:
                quote_data['author'] = author
                quote = Quote(**quote_data)
                quote.save()

if __name__ == "__main__":
    import_authors()
    import_quotes()
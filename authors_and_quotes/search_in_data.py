import connect
from models import Author, Quote

def search_quotes(criteria):
    if criteria.startswith('name:'):
        author_name = criteria.split(':')[1].strip()
        author = Author.objects(fullname=author_name).first()
        if author:
            quotes = Quote.objects(author=author)
            return [quote.quote for quote in quotes]
        else:
            return []

    elif criteria.startswith('tag:'):
        tag = criteria.split(':')[1].strip()
        quotes = Quote.objects(tags=tag)
        return [quote.quote for quote in quotes]

    elif criteria.startswith('tags:'):
        tags = criteria.split(':')[1].strip().split(',')
        quotes = Quote.objects(tags__in=tags)
        return [quote.quote for quote in quotes]

    elif criteria == 'exit':
        return None

if __name__ == "__main__":
    while True:
        criteria = input("Enter your search criteria: ")
        results = search_quotes(criteria)
        if results is None:
            break
        elif results:
            for result in results:
                print(result)
        else:
            print("No results found.")
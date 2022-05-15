import urllib.request,json
from . models import Quote

base_url='http://quotes.stormconsultancy.co.uk/random.json'

def get_quote():
    get_quote_url = base_url.format()
    with urllib.request.urlopen(get_quote_url) as url:
        quotes = url.read()
        get_quote_response = json.loads(quotes)
        quote_object = None
        if get_quote_response:
            quote=get_quote_response.get('quote')
            author=get_quote_response.get('author')
            quote_object = Quote(quote,author)
            print(quote_object)

    return quote_object


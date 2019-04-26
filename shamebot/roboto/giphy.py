import requests


class GiphyRequest:

    def __init__(self):
        self.api_key = ''
        self.host = 'https://api.giphy.com'
        self.response = {}

    # Following GIPHY API
    # https://developers.giphy.com/docs/#operation--gifs-search-get
    #
    # General Searches

    # Override for optional parameters
    def search(self, search_term, results=1, offset=0, rating=''):
        path = '/v1/gifs/search'
        params = {
            'api_key': self.api_key,
            'q': search_term,
            'limit': results,
            'offset': offset,
            'rating': rating
        }

        giphy_request = requests.get(self.host+path, params)

        self.response = giphy_request.json()

    def select_url(self, item_number=0):

        embed_url = self.response['data'][item_number]['embed_url']
        print("The number of items in the data response: ", len(self.response['data']))
        print("The Url you wanted: ", embed_url)


test = GiphyRequest()

test.search("potato", 20)
test.select_url(5)




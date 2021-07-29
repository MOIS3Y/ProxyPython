import sys
import json
import requests


class ProxyScan(object):
    """The class makes it easy to get available free proxy servers.
    To get a random proxy server, you can simply call the get_proxy () method.
    If you need to get a list of servers according to the specified parameters,
    add named arguments to the method in accordancewith the API.
    You can see the list of available methods at the link
    https://www.proxyscan.io/api

    Requirements: (sys, json, requests) libs

    Simple example:
        test = ProxyScan()
        response = test.get_proxy(
            format='json',
            type='https',
            limit='10',
            country='fr,us'
        )

    """
    def __init__(self):
        self.API_URL = 'https://www.proxyscan.io/api/proxy?'

    def create_url(self, parameters):
        request_str = ''
        for key, value in parameters.items():
            request_str += f'{key}={value}&'
        url = self.API_URL + request_str

        return url

    @staticmethod
    def call_api(url):
        """The method receives the url and creates a request
        to the api www.proxyscan.io.
        Receives a JSON response containing a proxy server
        or list of proxy servers. Returns a "Response" object

        Args:
            url (str): request address

        Returns:
            Response: Python requests.Response Object
        """
        with requests.Session() as session:
            try:
                response = session.get(url)
            except Exception as error:
                print('Somthing wrong, check your internet connection!')
                print(error)
                sys.exit(0)

            return response

    def get_proxy(self, **parameters):
        """The method is the interface of the class.
        Gets fields for creating a unique request to the api
        to get data about available proxy servers.
        Returns a deserialized JSON object as a Python object (list)

        Kwargs:
            field='value' field to add request address

        Returns:
            list: Python object
        """
        url = self.create_url(parameters)
        response = self.call_api(url)
        if response.status_code != 200:
            return [{'Error request to API': response.status_code}]
        else:
            try:
                return json.loads(response.text)
            except json.JSONDecodeError:
                return [{'Error request to API': 'Response is not JSON'}]


if __name__ == "__main__":
    test = ProxyScan()
    r = test.get_proxy()
    print(json.dumps(r, indent=4, sort_keys=True))

import json

import requests

from options.message import Message


class Url(Message):
    """Represents an object of type url that can be contained in the options of an action."""
    def __init__(self, structure):
        """Constructor method.

        :param structure: the url itself
        """
        self.structure = structure

    def get_data(self) -> dict:
        """Takes care of making a GET request to the url itself and returns the response data in JSON in a dict format.

        :return: the data returned by the request
        """
        url = self.structure
        content = requests.get(url).content
        data = json.loads(content)
        return data

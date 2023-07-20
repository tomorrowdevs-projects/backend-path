import requests

from action_parser.options.message import Message
from action_parser.options.url import Url


class Action:
    def __init__(self, type: str, name: str, options: dict):
        """Constructor method.

        :param type: indicates the type of action, it can be of type "HTTPRequestAction" or of type "PrintAction"
        :param name: indicates the name of the action, during execution it becomes the key of the returned event,
            if it returns content
        :param options: the content needed to execute the action, may contain a `message` or
            `url` key depending on the type
        """
        self.type = type
        self.name = name
        self.options = options

    def execute(self, event: dict) -> dict:
        """Takes an event as input and executes the action and returns an event as output.
        If the action type is `HTTPRequestAction` a get request is made to the url in the options attribute and its
        JSON is returned in the output event.
        If the type of the action is "PrintAction" the message in the options attribute is printed.

        :param event: can be empty or can contain key-value pairs where the key is the name of a previously executed
            action and its object JSON value returned from the execution of that action
        :return: the event itself given in input with in addition the result of this execution
        """
        if self.type == "HTTPRequestAction":
            url = Url(self.options["url"])
            url.format(event)
            try:
                data = url.get_data()
                event[self.name] = data
            except requests.exceptions.ConnectionError:
                quit()

        elif self.type == "PrintAction":
            message = Message(self.options["message"])
            message.format(event)
            formatted_message = message.structure
            print(formatted_message)

        return event

import requests

from action_parser.options import Options


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
            options = Options(type="Url", content=self.options["url"])
            options.format(event)
            try:
                url = options.content
                response = requests.get(url)
                if response.status_code not in range(200, 300):
                    quit()
                event[self.name] = response.json()
            except requests.exceptions.ConnectionError:
                quit()

        elif self.type == "PrintAction":
            options = Options(type="Message", content=self.options["message"])
            options.format(event)
            message = options.content
            print(message)

        return event

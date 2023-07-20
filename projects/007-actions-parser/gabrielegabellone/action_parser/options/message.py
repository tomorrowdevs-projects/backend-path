import re


class Message:
    """Represents an object of type message that can be contained in the options of an action."""
    def __init__(self, structure: str):
        """Constructor method.

        :param structure: the content of the message itself
        """
        self.structure = structure

    def is_formatted(self) -> bool:
        """Check if the message content is already formatted.

        :return: `True` if the message is already formatted, `False` otherwise
        """
        if "{{" not in self.structure:
            return True
        return False

    def format(self, variables: dict):
        """Takes care of formatting the content of the message based on the variables supplied as input.

        :param variables: the reference variables for formatting the message
        """
        message = self.structure

        message_pieces = re.split("[{}]+", message)

        substitutes = {}
        for message_piece in message_pieces:
            if "." in message_piece:
                keys = message_piece.split(".")
                try:
                    value = self.extract_value(variables, keys)
                    substitutes[message_piece] = value
                except KeyError:
                    pass

        message_to_format = "".join(message_pieces)
        for s in substitutes:
            formatted_message = message_to_format.replace(s, str(substitutes[s]))
            message_to_format = formatted_message

        self.structure = formatted_message

    @staticmethod
    def extract_value(variables: dict, keys: list):
        """It takes care of extracting a value from a dict starting from a list containing keys. For example,
        if I pass a list like the following `[1, 'name']`, the function will look inside the `variables`
        parameter, first for the value of the key 1 and inside it the value of the key 'name', and will return the
        latter.

        :param variables: dict containing the value to look up
        :param keys: contains the keys to look for in the 'variables' parameter, they are ordered so that the key at
            index 1 is contained in the value of the one at index 0 and so on
        :return: the value found
        """
        for k in keys:
            variable = variables[k]
            variables = variable
        return variable

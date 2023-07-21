from action_parser.options.message import Message


class Url(Message):
    """Represents an object of type url that can be contained in the options of an action."""
    def __init__(self, structure):
        """Constructor method.

        :param structure: the url itself
        """
        self.structure = structure

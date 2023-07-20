import re


class Message:
    """Represents an object of type message that can be contained in the options of an action."""
    def __init__(self, structure: str):
        """Constructor method.

        :param structure: the content of the message itself
        """
        self.structure = structure

    def format(self, event: dict):
        """Takes care of formatting the content of the message, replacing the words between the double braces with
        those provided by an input event.

        :param event: event containing the data with which to replace the words of the message
        """
        string_to_check = self.structure

        if "}}" in string_to_check:
            formatted_string = ""

            while "}}" in string_to_check:
                closed_brace_index = string_to_check.index("}")
                
                if string_to_check[closed_brace_index+1] == "}":
                    if "{{" in string_to_check[:closed_brace_index]:
                        open_braces_found = False
                        open_brace_index = closed_brace_index - 1
                        while not open_braces_found:
                            if string_to_check[open_brace_index] == "{" and string_to_check[open_brace_index - 1] == "{":
                                open_braces_found = True
                            open_brace_index -= 1

                        option_key = string_to_check[open_brace_index+2:closed_brace_index]
                        option_value = self.get_option_value(option_key, event)
                        formatted_string += string_to_check[:open_brace_index] + str(option_value)
                        string_to_check = string_to_check[closed_brace_index+2:]
                        if "}}" not in string_to_check:
                            formatted_string += string_to_check
                    else:
                        formatted_string += string_to_check[:closed_brace_index+2]
                        string_to_check = string_to_check[closed_brace_index+2:]
                else:
                    formatted_string += string_to_check[:closed_brace_index+1]
                    string_to_check = string_to_check[closed_brace_index+1:]

            self.structure = formatted_string

    @staticmethod
    def get_option_value(option_key: str, event: dict):
        """Takes care of returning the option value starting from an option key and a reference event.

        :param option_key: the key or a set of keys delimited by a period
        :param event: dict containing the option keys from which to extract the option value
        :return: the value found, an empty string is returned if a KeyError occurs
        """
        if "." in option_key:
            keys = option_key.split(".")
        else:
            keys = [option_key]

        try:
            for k in keys:
                value = event[k]
                event = value
        except KeyError:
            value = ""

        return value

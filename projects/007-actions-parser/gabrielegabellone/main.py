import argparse
import json

from options.message import Message
from options.url import Url


def start_story(story: dict):
    """Takes care of starting the story json file by performing the actions it contains.

    :param story: the content of the story JSON file in a dict format
    """
    responses = {}
    actions = story["actions"]

    for action in actions:
        if action["type"] == "HTTPRequestAction":
            url = Url(action["options"]["url"])
            if not url.is_formatted():
                url.format(responses)
            data = url.get_data()
            responses[action["name"]] = data

        elif action["type"] == "PrintAction":
            message = Message(action["options"]["message"])
            if not message.is_formatted():
                message.format(responses)
            formatted_message = message.structure
            print(formatted_message)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--story", type=str, help="The name of the Story JSON file with the extension.")
    args = parser.parse_args()
    story_json_path = args.story

    with open(story_json_path, "r") as story_json_file:
        file_content = story_json_file.read()

    data = json.loads(file_content)
    start_story(data)

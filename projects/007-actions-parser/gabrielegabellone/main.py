import argparse
import json

from action_parser.action import Action


def start_story(story: dict):
    """Takes care of starting the story json file by performing the actions it contains.

    :param story: the content of the story JSON file in a dict format
    """
    event_input = {}
    actions = story["actions"]

    for action in actions:
        action = Action(action["type"], action["name"], action["options"])
        event_output = action.execute(event_input)
        event_input = event_output


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--story", type=str, help="The name of the Story JSON file with the extension.")
    args = parser.parse_args()
    story_json_path = args.story

    with open(story_json_path, "r") as story_json_file:
        file_content = story_json_file.read()

    data = json.loads(file_content)
    start_story(data)

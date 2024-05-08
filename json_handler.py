import json
import os.path


class Program:
    def __init__(self, name=None, path=None, icon_path=None, duration=None, last_duration=None, count=None):
        self.name = name
        self.path = path
        self.icon_path = icon_path
        self.duration = duration
        self.last_duration = last_duration
        self.count = count

    def to_dict(self):
        return self.__dict__


json_path = "config.json"
empty_json = "[\n]"
programs = []


def save_programs(conf):
    with open(json_path, "w") as json_file:
        json.dump(conf.to_dict(), json_file, indent=4)


def load_programs():
    if not os.path.exists(json_path):
        with (open(json_path, "w") as json_file):
            json_file.write(empty_json)
    with open(json_path, "r") as json_file:
        progs = json.load(json_file)
    return progs

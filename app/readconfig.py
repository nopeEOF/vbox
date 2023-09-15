import sys
import yaml
import os

FILENAME = "./config.yaml"


def get_config():
    if file_exist(FILENAME):
        with open('config.yml', 'r') as file:
            return yaml.safe_load(file)
    else:
        print("Can not find config file: " + FILENAME)
        sys.exit(1)


def file_exist(filename: str) -> bool:
    if os.path.isfile(filename):
        return True
    return False

import json
from pathlib import Path
THIS_FOLDER = Path(__file__).parent.parent.resolve()
my_file = THIS_FOLDER / "config.json"

def read_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


config = read_json(my_file)
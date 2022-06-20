import sys
import os
from ast import literal_eval

import requests
import pandas as pd

URL = "https://remla-test.ponichtera.dev/api/correct"


def load_file(filename):
    loaded_data = pd.read_csv(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), filename),
        sep="\t",
        dtype={"title": "str"},
    )
    loaded_data = loaded_data[["title", "tags"]]

    loaded_data["tags"] = loaded_data["tags"].apply(literal_eval)
    return loaded_data


def send_data(data):
    for i in data.index:
        params = {
            "title": data["title"][i],
            "predicted": data["tags"][i],
            "actual": data["tags"][i],
        }
        print(f'{i}/{len(data.index)}:', params)
        requests.post(url=URL, json=params)  # maybe check status code


def run():
    num_args = len(sys.argv)
    if num_args != 2:
        print("Usage:", sys.argv[0], "[filename]")
        sys.exit(1)

    data = load_file(sys.argv[1])
    send_data(data)


if __name__ == "__main__":
    run()

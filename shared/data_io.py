import json

import pandas as pd


def load_json(path):
    """Read a JSON file and return the parsed data."""
    with open(path, "r") as f:
        return json.load(f)


def save_json(data, path):
    """Write data to a JSON file with indentation."""
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def load_json_as_df(path):
    """Read a JSON file and return a pandas DataFrame."""
    return pd.DataFrame(load_json(path))


def load_csv_as_df(path, **kwargs):
    """Read a CSV file and return a pandas DataFrame."""
    return pd.read_csv(path, **kwargs)

import json


def read_json_from_file(file_path):
    with open(file_path, 'r') as f:
        return json.loads(f.read())


def write_json_into_file(file_path, data):
    with open(file_path, 'w') as f:
        f.write(json.dumps(data, indent=2))

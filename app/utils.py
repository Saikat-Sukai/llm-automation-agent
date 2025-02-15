import os

def resolve_data_path(path):
    data_dir = os.path.abspath('/data')
    requested_path = os.path.abspath(os.path.join(data_dir, path.lstrip('/')))
    if not requested_path.startswith(data_dir):
        raise ValueError("Access outside /data denied")
    return requested_path
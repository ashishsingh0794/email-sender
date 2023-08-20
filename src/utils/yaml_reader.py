from pathlib import Path

import yaml


def get_config(config_file:str) -> dict:
    job_config = {}
    try:
        job_config = yaml.safe_load(Path(config_file).read_text(encoding='utf8'))
    except yaml.YAMLError as exc:
        print(exc)
    return job_config
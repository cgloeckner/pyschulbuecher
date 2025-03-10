import os
import requests


def check_local_compiler() -> bool:
    ret = os.system('which pdflatex')
    return ret == 0


def check_remote_compiler(url: str) -> bool:
    try:
        ret = requests.get(f'{url}/version')
        return ret.status_code == 200
    except requests.exceptions.ConnectionError:
        return False

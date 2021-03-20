import os

_current_file_path = os.path.abspath(__file__)
package_path = _current_file_path[:len("transplants/utils/paths.py")]


def get_abs_path(package_relative_path: str) -> str:
    return f"{package_path}{package_relative_path}"

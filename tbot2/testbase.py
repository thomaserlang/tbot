from typing import Any, TypeVar

T = TypeVar('T')


def parse_obj_as(type: type[T], obj: Any) -> T:
    from pydantic import TypeAdapter

    adapter = TypeAdapter(type)
    return adapter.validate_python(obj)


def run_file(file_: str):
    import subprocess

    subprocess.call(['pytest', '--tb=short', str(file_)])

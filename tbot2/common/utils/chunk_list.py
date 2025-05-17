from ast import TypeVar

T = TypeVar('T')


def chunk_list[T](lst: list[T], chunk_size: int) -> list[list[T]]:
    return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]

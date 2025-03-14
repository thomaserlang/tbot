import pytest


def run_file(file_: str):
    pytest.main(
        [
            '-o',
            'log_cli=true',
            '-o',
            'log_cli_level=debug',
            '-o',
            'log_cli_format=%(asctime)s.%(msecs)3d %(filename)-15s %(lineno)4d %(levelname)-8s %(message)s',
            file_,
        ]
    )

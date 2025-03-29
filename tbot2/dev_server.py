import os
from subprocess import list2cmdline

from honcho.manager import Manager  # type: ignore


def main():
    path = os.path.dirname(os.path.realpath(__file__))

    start = [
        ('api', ['python', 'runner.py', 'api'], path),
    ]

    manager = Manager()
    for name, cmd, cwd in start:
        manager.add_process( # type: ignore
            name,
            list2cmdline(cmd),
            quiet=False,
            cwd=cwd,
        )

    manager.loop()


if __name__ == '__main__':
    main()

from pathlib import Path
from subprocess import list2cmdline

from honcho.manager import Manager  # type: ignore


def main() -> None:
    path = Path(__file__).parent

    start = [
        ('api', ['python', 'runner.py', 'api'], path),
        ('tasks', ['python', 'runner.py', 'tasks'], path),
    ]

    manager = Manager()
    for name, cmd, cwd in start:
        manager.add_process(  # type: ignore
            name,
            list2cmdline(cmd),
            quiet=False,
            cwd=cwd,
        )

    manager.loop()


if __name__ == '__main__':
    main()

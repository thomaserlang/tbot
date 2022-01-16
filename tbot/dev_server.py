import os, sys
from subprocess import list2cmdline
from honcho.manager import Manager

def main():  
    path = os.path.dirname(os.path.realpath(__file__))

    start = [
        ('twitch_bot', ['python', 'runner.py', 'twitch-bot'], path),
        ('discord', ['python', 'runner.py', 'discord'], path),
        ('web', ['python', 'runner.py', 'web'], path),
        ('npm', ['npm', 'run', 'watch'], os.path.join(path, 'web/static/app')),
    ]

    manager = Manager()
    for name, cmd, cwd in start:
        manager.add_process(
            name, 
            list2cmdline(cmd),
            quiet=False, 
            cwd=cwd,
        )

    manager.loop()
    sys.exit(manager.returncode)

if __name__ == '__main__':
    main()
from circus.commands.base import Command
from circus.exc import ArgumentError
from circus.config import get_config
from circus.watcher import Watcher


class Exec(Command):
    """\
        Execute a watcher outside of circusd
        ====================================

        This command starts a watcher by os.exec()uting it, replacing the
        current process. This is useful to debug watchers ouside of circusd, as
        you can use pdb and gdb to debug the process.

        Command line
        ------------

        ::

            $ circusctl exec <config> <name>

        Options
        +++++++

        - <config>: the circus configuration file
        - <name>: name of the watcher

    """
    name = "exec"

    def message(self, *args, **opts):
        if len(args) != 2:
            raise ArgumentError("invalid number of arguments")

        config_file, name = args

        config = get_config(config_file)
        watchers = config.get('watchers', [])
        config = filter(lambda w: w['name'] == name, watchers)
        if not config:
            raise ArgumentError("watcher not found")
        config = config[0]
        config['stdout_stream'] = {'class': 'StdoutStream'}
        config['stderr_stream'] = {'class': 'StdoutStream'}
        config['_exec'] = True
        watcher = Watcher.load_from_config(config)
        # the next call will exec(), replacing the current process
        watcher.start()

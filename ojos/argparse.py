import argparse
import sys
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from typing import List

from .decorator import logging


class ArgumentParser(argparse.ArgumentParser):
    def __init__(
        self,
        prog=None,
        usage=None,
        description=None,
        epilog=None,
        parents=[],
        formatter_class=argparse.HelpFormatter,
        prefix_chars="-",
        fromfile_prefix_chars=None,
        argument_default=None,
        conflict_handler="error",
        add_help=True,
        allow_abbrev=True,
    ):
        super(ArgumentParser, self).__init__(
            prog,
            usage,
            description,
            epilog,
            parents,
            formatter_class,
            prefix_chars,
            fromfile_prefix_chars,
            argument_default,
            conflict_handler,
            add_help,
            allow_abbrev,
        )

    def _get_action_from_name(self, name):
        container = self._actions
        if name is None:
            return None
        for action in container:
            if "/".join(action.option_strings) == name:
                return action
            elif action.metavar == name:
                return action
            elif action.dest == name:
                return action

    def error(self, message):
        exc = sys.exc_info()[1]
        if exc:
            exc.argument = self._get_action_from_name(exc.argument_name)
            raise exc
        super(ArgumentParser, self).error(message)


@logging
def command_help(parser, args):
    if args.command is None:
        parser.parse_args(["--help"])
    else:
        parser.parse_args([args.command, "--help"])


@logging
def command_execute(parser: ArgumentParser, args: List[str]):
    stdout: str = ""
    with StringIO() as stderr_buf, redirect_stderr(stderr_buf):
        with StringIO() as stdout_buf, redirect_stdout(stdout_buf):
            try:
                _args: argparse.Namespace = parser.parse_args(args)
                _args.handler(parser, _args)
            except argparse.ArgumentError:
                parser.print_help()
            except SystemExit as e:
                if e.args[0] != 0:
                    parser.print_help()
            stdout = stdout_buf.getvalue()

    return stdout

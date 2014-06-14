from __future__ import unicode_literals

import argparse

from pre_commit import color
from pre_commit.commands.autoupdate import autoupdate
from pre_commit.commands.clean import clean
from pre_commit.commands.install import install
from pre_commit.commands.run import run
from pre_commit.commands.uninstall import uninstall
from pre_commit.runner import Runner
from pre_commit.util import entry


@entry
def main(argv):
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser('install', help='Intall the pre-commit script.')

    subparsers.add_parser('uninstall', help='Uninstall the pre-commit script.')

    subparsers.add_parser('clean', help='Clean out pre-commit files.')

    subparsers.add_parser('autoupdate', help='Auto-update hooks config.')

    run_parser = subparsers.add_parser('run', help='Run hooks.')
    run_parser.add_argument('hook', nargs='?', help='A single hook-id to run')
    run_parser.add_argument(
        '--all-files', '-a', action='store_true', default=False,
        help='Run on all the files in the repo.  Implies --no-stash.',
    )
    run_parser.add_argument(
        '--color', default='auto', type=color.use_color,
        help='Whether to use color in output.  Defaults to `auto`',
    )
    run_parser.add_argument(
        '--no-stash', default=False, action='store_true',
        help='Use this option to prevent auto stashing of unstaged files.',
    )
    run_parser.add_argument(
        '--verbose', '-v', action='store_true', default=False,
    )

    help = subparsers.add_parser(
        'help', help='Show help for a specific command.'
    )
    help.add_argument('help_cmd', nargs='?', help='Command to show help for.')

    # Argparse doesn't really provide a way to use a `default` subparser
    if len(argv) == 0:
        argv = ['run']
    args = parser.parse_args(argv)

    runner = Runner.create()

    if args.command == 'install':
        return install(runner)
    elif args.command == 'uninstall':
        return uninstall(runner)
    elif args.command == 'clean':
        return clean(runner)
    elif args.command == 'autoupdate':
        return autoupdate(runner)
    elif args.command == 'run':
        return run(runner, args)
    elif args.command == 'help':
        if args.help_cmd:
            parser.parse_args([args.help_cmd, '--help'])
        else:
            parser.parse_args(['--help'])
    else:
        raise NotImplementedError(
            'Command {0} not implemented.'.format(args.command)
        )

    raise AssertionError(
        'Command {0} failed to exit with a returncode'.format(args.command)
    )


if __name__ == '__main__':
    exit(main())

# -*- coding: utf-8 -*-
from ansible_generator.main import AnsibleGenerator
from argparse import ArgumentParser
from logging import DEBUG, INFO


def cli():
    parser = ArgumentParser(
        description=u'Generate an ansible playbook directory structure')

    parser.add_argument(
        u'-a',
        u'--alternate-layout',
        action=u'store_true',
        dest=u'alternate_layout')
    parser.add_argument(
        '-i',
        '--inventories',
        nargs='+',
        default=['production', 'staging'],
        dest=u'inventories',
        type=str)
    parser.add_argument(
        '-v', '--verbose', action='store_true', dest='verbosity')
    parser.add_argument(u'projects', nargs='*', default=None)

    args = parser.parse_args()

    if args.verbosity:
        verbosity = DEBUG
    else:
        verbosity = INFO

    generator = AnsibleGenerator(
        inventories=args.inventories,
        alternate_layout=args.alternate_layout,
        projects=args.projects,
        verbosity=verbosity)
    generator.run()

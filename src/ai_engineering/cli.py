"""Console entry point: `ai-engineering <subcommand> ...`."""
import argparse
import sys

from ai_engineering import installer


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    ap = argparse.ArgumentParser(prog='ai-engineering')
    sub = ap.add_subparsers(dest='command', required=True)

    install_ap = sub.add_parser('install', parents=[installer.build_arg_parser()], add_help=False,
                                 help='Copy a profile\'s rules and skills into a target project')
    install_ap.set_defaults(handler=lambda args: installer.main([
        '--project', str(args.project), '--profile', args.profile,
        *(['--dry-run'] if args.dry_run else []),
        *(['--force'] if args.force else []),
        *(['--entrypoints'] if args.entrypoints else []),
    ]))

    list_ap = sub.add_parser('list-profiles', help='List installable profile names')
    list_ap.set_defaults(handler=lambda args: installer.list_profiles())

    args = ap.parse_args(argv)
    args.handler(args)


if __name__ == '__main__':
    main()

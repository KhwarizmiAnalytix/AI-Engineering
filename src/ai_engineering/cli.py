"""Console entry point for package-owned shared engineering guidance."""

import argparse
from pathlib import Path

from ai_engineering import __version__, catalog, installer, user_setup


def main(argv=None):
    ap = argparse.ArgumentParser(prog='ai-engineering')
    ap.add_argument('--version', action='version', version='%(prog)s ' + __version__)
    sub = ap.add_subparsers(dest='command', required=True)

    setup = sub.add_parser('setup', help='Register shared guidance once for all local projects')
    setup.add_argument('--user', required=True, action='store_true', help='Install user-level registrations')
    setup.add_argument('--home', type=Path, default=Path.home(), help='User home (default: current user)')
    setup.add_argument('--tool', choices=('all', 'claude', 'cursor'), default='all')
    setup.add_argument('--dry-run', action='store_true')
    setup.add_argument('--force', action='store_true', help='Back up and replace modified managed registrations')
    setup.set_defaults(handler=lambda args: user_setup.setup(args.home, args.tool, args.dry_run, args.force))

    uninstall = sub.add_parser('uninstall', help='Remove unmodified user-level registrations')
    uninstall.add_argument('--user', required=True, action='store_true')
    uninstall.add_argument('--home', type=Path, default=Path.home())
    uninstall.add_argument('--dry-run', action='store_true')
    uninstall.set_defaults(handler=lambda args: user_setup.uninstall(args.home, args.dry_run))

    context = sub.add_parser('context', help='Print packaged rules and project context without writing files')
    context.add_argument('--project', type=Path, default=Path('.'))
    context.add_argument('--profile', help='Override profile inferred from the repository directory name')
    context.set_defaults(handler=lambda args: print(catalog.context(args.project, args.profile), end=''))

    skill = sub.add_parser('skill', help='Print a packaged task workflow')
    skill.add_argument('name', choices=catalog.skill_names())
    skill.set_defaults(handler=lambda args: print(catalog.skill(args.name), end=''))

    skills = sub.add_parser('list-skills', help='List packaged task workflows')
    skills.set_defaults(handler=lambda args: print('\n'.join(catalog.skill_names())))

    list_ap = sub.add_parser('list-profiles', help='List installable profile names')
    list_ap.set_defaults(handler=lambda args: installer.list_profiles())

    install = sub.add_parser('install', parents=[installer.build_arg_parser()], add_help=False,
                             help='Legacy: copy rules and skills into one project')
    install.set_defaults(handler=lambda args: installer.run(args))

    args = ap.parse_args(argv)
    try:
        result = args.handler(args)
    except (ValueError, OSError) as exc:
        ap.exit(1, f'ai-engineering: {exc}\n')
    return result if isinstance(result, int) else 0


if __name__ == '__main__':
    raise SystemExit(main())

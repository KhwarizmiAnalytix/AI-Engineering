"""Exercise package resources and user setup without touching the real home."""

from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
import tempfile
import unittest

from ai_engineering import catalog, user_setup
from ai_engineering.cli import main


class SharedPackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.home = self.root / 'home'
        self.project = self.root / 'Logging'
        self.project.mkdir()
        (self.project / '.git').mkdir()

    def run_cli(self, *args):
        output = StringIO()
        with redirect_stdout(output):
            result = main(list(args))
        return result, output.getvalue()

    def setup_user(self, *args):
        return self.run_cli('setup', '--user', '--home', str(self.home), *args)

    def snapshot(self):
        return {str(path.relative_to(self.home)): path.read_bytes()
                for path in self.home.rglob('*') if path.is_file()}

    def test_every_profile_and_skill_available_from_package(self):
        for name in catalog.profiles():
            output = catalog.context(self.project, name)
            self.assertIn('Profile: ' + name, output)
            self.assertIn('# C++ coding standards', output)
        for name in catalog.skill_names():
            self.assertTrue(catalog.skill(name).startswith('---\nname: '))
            self.assertTrue(catalog.skill_description(name))

    def test_context_infers_profile_from_subdirectory_without_writing(self):
        nested = self.project / 'src'
        nested.mkdir()
        before = set(self.project.rglob('*'))
        result, output = self.run_cli('context', '--project', str(nested))
        self.assertEqual(result, 0)
        self.assertIn('Profile: Logging', output)
        self.assertIn('ai-engineering skill cmake-package', output)
        self.assertEqual(set(self.project.rglob('*')), before)

    def test_unknown_repository_gets_baseline_without_guessed_profile(self):
        unknown = self.root / 'Other'
        unknown.mkdir()
        (unknown / 'pyproject.toml').write_text('[project]\nname = "Other"\n')
        output = catalog.context(unknown)
        self.assertIn('Profile: baseline', output)
        self.assertNotIn('Logging integration profile', output)

    def test_context_rejects_unknown_profile_and_skill(self):
        with self.assertRaisesRegex(ValueError, 'Unknown profile'):
            catalog.context(self.project, '../../secrets')
        with self.assertRaisesRegex(ValueError, 'Unknown skill'):
            catalog.skill('../../secrets')

    def test_dry_run_does_not_even_create_home(self):
        result, output = self.setup_user('--dry-run')
        self.assertEqual(result, 0)
        self.assertIn('no files written', output)
        self.assertFalse(self.home.exists())

    def test_setup_is_idempotent_and_uses_runtime_loaders(self):
        self.assertEqual(self.setup_user()[0], 0)
        before = self.snapshot()
        self.assertEqual(self.setup_user()[0], 0)
        self.assertEqual(self.snapshot(), before)
        self.assertFalse((self.home / '.cursor/skills').exists())
        wrapper = self.home / '.claude/skills/ai-engineering-project-build/SKILL.md'
        self.assertIn('ai-engineering skill project-build', wrapper.read_text())
        self.assertNotIn('Configure/build affected targets', wrapper.read_text())
        self.assertFalse((self.project / '.claude').exists())

    def test_cursor_only_registers_cursor_skills_and_prints_user_rule(self):
        result, output = self.setup_user('--tool', 'cursor')
        self.assertEqual(result, 0)
        self.assertTrue((self.home / '.cursor/skills/ai-engineering/SKILL.md').is_file())
        self.assertFalse((self.home / '.claude').exists())
        self.assertIn('Customize > Rules > User Rules', output)

    def test_force_never_replaces_unmanaged_file(self):
        target = self.home / '.claude/rules/ai-engineering.md'
        target.parent.mkdir(parents=True)
        target.write_text('my policy')
        result, _ = self.setup_user('--force')
        self.assertEqual(result, 1)
        self.assertEqual(target.read_text(), 'my policy')

    def test_modified_managed_files_need_force_and_backups_are_preserved(self):
        self.setup_user()
        target = self.home / '.claude/rules/ai-engineering.md'
        target.write_text('my first edit')
        self.assertEqual(self.setup_user()[0], 1)
        self.assertEqual(target.read_text(), 'my first edit')
        self.assertEqual(self.setup_user('--force')[0], 0)
        backup = target.with_name(target.name + '.ai-engineering.bak')
        self.assertEqual(backup.read_text(), 'my first edit')
        target.write_text('my second edit')
        self.setup_user('--force')
        self.assertEqual(backup.read_text(), 'my first edit')
        self.assertEqual(target.with_name(backup.name + '.1').read_text(), 'my second edit')

    def test_unmodified_registration_updates_without_force(self):
        self.setup_user()
        target = self.home / '.claude/rules/ai-engineering.md'
        target.write_text('old package loader')
        manifest = self.home / user_setup.MANIFEST
        prior = json.loads(manifest.read_text())
        prior['.claude/rules/ai-engineering.md'] = user_setup.checksum(target.read_bytes())
        manifest.write_text(json.dumps(prior))
        self.assertEqual(self.setup_user()[0], 0)
        self.assertEqual(target.read_text(), user_setup.BOOTSTRAP)

    def test_uninstall_preserves_user_files_and_modified_registrations(self):
        self.setup_user()
        user_file = self.home / '.claude/CLAUDE.md'
        user_file.write_text('native policy')
        edited = self.home / '.claude/rules/ai-engineering.md'
        edited.write_text('local changes')
        before = self.snapshot()
        self.run_cli('uninstall', '--user', '--home', str(self.home), '--dry-run')
        self.assertEqual(self.snapshot(), before)
        result, _ = self.run_cli('uninstall', '--user', '--home', str(self.home))
        self.assertEqual(result, 1)
        self.assertEqual(edited.read_text(), 'local changes')
        self.assertEqual(user_file.read_text(), 'native policy')
        self.assertFalse((self.home / '.claude/skills/ai-engineering/SKILL.md').exists())
        self.assertEqual(set(json.loads((self.home / user_setup.MANIFEST).read_text())),
                         {'.claude/rules/ai-engineering.md'})

    def test_clean_uninstall_removes_manifest_and_is_repeatable(self):
        self.setup_user()
        self.assertEqual(self.run_cli('uninstall', '--user', '--home', str(self.home))[0], 0)
        self.assertEqual(self.snapshot(), {})
        self.assertEqual(self.run_cli('uninstall', '--user', '--home', str(self.home))[0], 0)

    def test_symlink_target_is_never_overwritten_or_removed(self):
        self.setup_user()
        original = self.root / 'native.md'
        original.write_text('native policy')
        target = self.home / '.claude/rules/ai-engineering.md'
        target.unlink()
        target.symlink_to(original)
        self.assertEqual(self.setup_user('--force')[0], 1)
        self.run_cli('uninstall', '--user', '--home', str(self.home))
        self.assertTrue(target.is_symlink())
        self.assertEqual(original.read_text(), 'native policy')

    def test_manifest_cannot_remove_unrelated_files(self):
        self.setup_user()
        unrelated = self.root / 'unrelated'
        unrelated.write_text('keep me')
        manifest = self.home / user_setup.MANIFEST
        manifest.write_text(json.dumps({'../unrelated': user_setup.checksum(unrelated.read_bytes())}))
        with self.assertRaisesRegex(ValueError, 'Invalid managed path'):
            user_setup.uninstall(self.home)
        self.assertEqual(unrelated.read_text(), 'keep me')

    def test_legacy_install_remains_available(self):
        result, output = self.run_cli('install', '--project', str(self.project),
                                      '--profile', 'Logging', '--dry-run')
        self.assertEqual(result, 0)
        self.assertIn('AI_ENGINEERING.md', output)
        self.assertFalse((self.project / 'AI_ENGINEERING.md').exists())


if __name__ == '__main__':
    unittest.main()

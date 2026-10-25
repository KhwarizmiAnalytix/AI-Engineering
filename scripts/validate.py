#!/usr/bin/env python3
"""Static checks for repository metadata, frontmatter and copied plugin skills."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def main():
 profiles=json.loads((R/'profiles/profiles.json').read_text())
 marketplace=json.loads((R/'.claude-plugin/marketplace.json').read_text())
 assert marketplace['plugins']
 for entry in marketplace['plugins']:
  path=R/entry['source']
  assert (path/'.claude-plugin/plugin.json').is_file(),path
  p=json.loads((path/'.claude-plugin/plugin.json').read_text())
  assert p['name']==entry['name']
  for f in (path/'skills').glob('*/SKILL.md'):
   assert f.read_bytes()==(R/'skills'/f.parent.name/'SKILL.md').read_bytes(),f
 for f in (R/'skills').glob('*/SKILL.md'):
  s=f.read_text();assert s.startswith('---\nname: ') and '\ndescription: ' in s and '\n---\n' in s,f
 for profile,cfg in profiles.items():
  assert (R/'profiles'/f'{profile}.md').exists(),profile
  for skill in cfg['skills']:assert (R/'skills'/skill/'SKILL.md').exists(),skill
  for rule in cfg['rules']:assert (R/'rules'/f'{rule}.md').exists(),rule
 for p in R.rglob('*.md'):
  assert not p.read_text().startswith('\ufeff'),p
 print(f'PASS: {len(profiles)} profiles, {len(list((R/"skills").glob("*/SKILL.md")))} skills, {len(marketplace["plugins"])} plugins')
if __name__=='__main__':main()

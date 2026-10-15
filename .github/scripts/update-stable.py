"""Resolve paired stable desktop/core versions using only public upstream metadata."""
import json
from pathlib import Path
import re
import subprocess


def api(path):
    return json.loads(subprocess.check_output(['gh', 'api', path], text=True))


remote = subprocess.check_output([
    'git', 'ls-remote', '--tags', 'https://github.com/reF1nd/sing-box.git',
], text=True)
versions = {}
for line in remote.splitlines():
    sha, ref = line.split()
    match = re.fullmatch(r'refs/tags/(v(\d+)\.(\d+)\.(\d+)-reF1nd)(\^\{\})?', ref)
    if match:
        version = tuple(map(int, match.group(2, 3, 4)))
        # Prefer the peeled commit if an annotated tag is encountered.
        if version not in versions or match.group(5):
            versions[version] = (match.group(1), sha)
if not versions:
    raise RuntimeError('No stable reF1nd release tag found')
version = max(versions)
core_tag, core_revision = versions[version]
upstream_tag = 'v' + '.'.join(map(str, version))
release = api('repos/SagerNet/sing-box/releases/tags/' + upstream_tag)
if release['prerelease'] or release['draft']:
    raise RuntimeError('The paired SagerNet release is not stable')
desktop = api('repos/SagerNet/sing-box/contents/clients/desktop?ref=' + upstream_tag)
if not re.fullmatch('[0-9a-f]{40}', desktop['sha']):
    raise RuntimeError('Invalid desktop revision')
manifest = {
    'repository': 'reF1nd/sing-box',
    'branch': 'reF1nd-stable',
    'tag': core_tag,
    'revision': core_revision,
    'desktop_version': upstream_tag.removeprefix('v'),
    'desktop_revision': desktop['sha'],
}
Path('ref1nd-core.json').write_text(json.dumps(manifest, indent=2) + '\n')
print('Stable core:', core_tag, core_revision)
print('Stable desktop:', upstream_tag, desktop['sha'])

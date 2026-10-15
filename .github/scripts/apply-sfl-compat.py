"""Use the official SFL installation identity with the reF1nd Linux daemon."""
from pathlib import Path
import sys

root = Path(sys.argv[1])
replacements = {
    'experimental/boxdd/main.go': [
        ('const serviceName = "sing-box-daemon-reF1nd"',
         'const serviceName = "sing-box-daemon"'),
    ],
    'experimental/boxdd/cmd_service_linux.go': [
        ('"/var/lib/sing-box-daemon-reF1nd"', '"/var/lib/sing-box-daemon"'),
    ],
    'experimental/boxdd/authorize_linux.go': [
        ('"io.reF1nd.sfl.take-over-service"',
         '"io.nekohasekai.sfl.take-over-service"'),
        ('"io.reF1nd.sfl.set-insecure-mode"',
         '"io.nekohasekai.sfl.set-insecure-mode"'),
    ],
}
for name, pairs in replacements.items():
    path = root / name
    content = path.read_text()
    for original, replacement in pairs:
        if original not in content and replacement not in content:
            raise RuntimeError('Upstream changed the SFL integration field in ' + name)
        content = content.replace(original, replacement)
    path.write_text(content)

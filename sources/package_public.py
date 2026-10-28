"""Package the published binaries and QA evidence; run from any directory."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = '1.2.0'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

payload = [ROOT / p for p in (
    'AUTHORS.txt', 'OFL.txt', 'README.md', 'CHANGELOG.md', 'FONTLOG.txt',
    'manifest.json', 'css/kleyos.css', 'documentation/PUBLICATION.md',
    'qa/Kleyos-1.2.0-QA-Report.md', 'qa/Kleyos-1.2.0-Specimen.png',
    'qa/Webfont-OTS.json', 'qa/i31-VALIDATION.json',
    'qa/i31-NATIVE_RENDER.json', 'qa/requirements.txt',
)]
for folder in ('fonts', 'sources', 'qa/googlefonts'):
    payload.extend(p for p in (ROOT / folder).rglob('*')
        if p.is_file() and p.suffix not in ('.log', '.pyc')
        and '__pycache__' not in p.parts)
payload = sorted(set(payload))
for path in payload:
    assert path.is_file(), path
checksums = ROOT / 'SHA256SUMS.txt'
checksums.write_text(''.join(f'{sha(p)}  {p.relative_to(ROOT).as_posix()}\n' for p in payload))
payload.append(checksums)

manifest = json.loads((ROOT / 'manifest.json').read_text())
for role in manifest['fonts']:
    for format in ('ttf', 'woff2'):
        assert sha(ROOT / role[format]['path']) == role[format]['sha256']

archive = ROOT / f'dist/Kleyos-{VERSION}-Public-Release-RFN.zip'
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as out:
    for p in sorted(payload):
        name = f'Kleyos-{VERSION}/' + p.relative_to(ROOT).as_posix()
        info = zipfile.ZipInfo(name, (2026, 10, 28, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        out.writestr(info, p.read_bytes())
with zipfile.ZipFile(archive) as check:
    assert check.testzip() is None
    for role in manifest['fonts']:
        for format in ('ttf', 'woff2'):
            entry = role[format]
            data = check.read(f'Kleyos-{VERSION}/' + entry['path'])
            assert hashlib.sha256(data).hexdigest() == entry['sha256']
archive.with_suffix(archive.suffix + '.sha256').write_text(f'{sha(archive)}  {archive.name}\n')
print(json.dumps({'archive': str(archive), 'file_count': len(payload),
    'size_bytes': archive.stat().st_size, 'sha256': sha(archive),
    'font_hashes_match_manifest': True, 'zip_integrity': True}))

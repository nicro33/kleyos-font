"""Build public Kleyos 1.2.0 metadata from the validated i31 font binaries.

The original editable drawing sources are not reconstructed by this script.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
VERSION = '1.2.0'
EXPECTED = {
    'Display': '6b6b5ffa2a7b5b5f22ae86189be35bbf091fc5ba3e65662a1951f74e60cd016d',
    'Text': '6cc2aacb5555222b59297da16360df3e225fe879a7fb5bada46c8920044d8478',
}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def build():
    records = []
    for role, expected in EXPECTED.items():
        source = ROOT / f'sources/validated-i31/Kleyos-{role}-i31-Assemblages.ttf'
        assert sha(source) == expected, f'Source identity changed: {role}'
        font = TTFont(source, recalcTimestamp=False)
        names = {
            1: f'Kleyos {role}', 2: 'Regular',
            3: f'Kleyos{role}-Regular;1.310;KLYS',
            4: f'Kleyos {role} Regular', 5: 'Version 1.310',
            6: f'Kleyos{role}-Regular', 16: f'Kleyos {role}', 17: 'Regular',
            13: 'This Font Software is licensed under the SIL Open Font License, Version 1.1. This license is available with a FAQ at: https://openfontlicense.org',
        }
        for record in list(font['name'].names):
            if record.nameID in names:
                font['name'].setName(names[record.nameID], record.nameID,
                    record.platformID, record.platEncID, record.langID)
        ttf = ROOT / f'fonts/ttf/Kleyos-{role}.ttf'
        woff = ROOT / f'fonts/woff2/Kleyos-{role}.woff2'
        ttf.parent.mkdir(parents=True, exist_ok=True)
        woff.parent.mkdir(parents=True, exist_ok=True)
        font.save(ttf)
        font.flavor = 'woff2'
        font.save(woff)
        baseline = TTFont(source, recalcTimestamp=False)
        public = TTFont(ttf, recalcTimestamp=False)
        web = TTFont(woff, recalcTimestamp=False)
        checked = []
        for table in baseline.keys():
            if table not in ('GlyphOrder', 'head', 'name'):
                assert baseline.getTableData(table) == public.getTableData(table), table
                assert public.getTableData(table) == web.getTableData(table), table
                checked.append(table)
        assert public['OS/2'].fsType == 0
        assert public.getBestCmap() == baseline.getBestCmap()
        assert web['name'].getDebugName(1) == f'Kleyos {role}'
        records.append({
            'role': role, 'source': source.relative_to(ROOT).as_posix(),
            'source_sha256': expected, 'family': f'Kleyos {role}',
            'public_semver': VERSION, 'opentype_version': '1.310',
            'identical_source_tables_except_head_and_name': checked,
            'woff2_roundtrip_tables_match': True,
            'codepoints': len(public.getBestCmap()),
            'ttf': {'path': ttf.relative_to(ROOT).as_posix(), 'sha256': sha(ttf), 'size_bytes': ttf.stat().st_size},
            'woff2': {'path': woff.relative_to(ROOT).as_posix(), 'sha256': sha(woff), 'size_bytes': woff.stat().st_size},
        })
    manifest = {
        'name': 'Kleyos', 'version': VERSION, 'date': '2026-10-28',
        'source_iteration': 'H2-i31-Assemblages', 'license': 'OFL-1.1',
        'reserved_font_name': 'Kleyos',
        'repository': 'https://github.com/nicro33/kleyos-font',
        'tag': 'v' + VERSION,
        'source_drawings_and_positioning_unchanged': True,
        'fontbakery_googlefonts_acceptance': False,
        'fonts': records,
    }
    (ROOT / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'public_version': VERSION, 'internal_version': '1.310', 'font_variants': len(records), 'all_content_tables_preserved': True}))

if __name__ == '__main__':
    build()

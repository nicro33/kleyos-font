#!/usr/bin/env python3
"""Build Kleyos Regular from the editable i33 master."""
import argparse
import hashlib
import json
import os
from pathlib import Path

from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables._k_e_r_n import KernTable_format_0
from fontTools.ttLib.tables.ttProgram import Program
from ufo2ft import compileTTF
from ufo2ft.filters import DecomposeComponentsFilter
from ufoLib2 import Font

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "sources/KleyosMaster.ufoz"
VERSION = "1.3.0"
OPENTYPE_VERSION = "1.411"
STEM = "Kleyos-Regular"


def file_record(path, relative_to):
    return {
        "path": path.relative_to(relative_to).as_posix(),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "size_bytes": path.stat().st_size,
    }


def build(out):
    os.environ.setdefault("SOURCE_DATE_EPOCH", "1793232000")
    ufo = Font.open(MASTER, lazy=False)
    ufo.info.familyName = "Kleyos"
    ufo.info.styleName = "Regular"
    ufo.info.versionMajor, ufo.info.versionMinor = (1, 411)
    ufo.info.copyright = (ROOT / "OFL.txt").read_text(encoding="utf-8").splitlines()[0]
    for name, width in (("space", 250), ("nbspace", 250), ("uni202F", 125)):
        ufo[name].width = width

    font = compileTTF(
        ufo,
        convertCubics=False,
        reverseDirection=False,
        removeOverlaps=False,
        useProductionNames=False,
        inplace=False,
        filters=[DecomposeComponentsFilter()],
    )

    # Keep the i33 legacy kerning for encoded glyphs alongside full GPOS.
    cmap = font.getBestCmap()
    encoded = set(cmap.values())
    pairs = sorted(
        (pair, value) for pair, value in ufo.kerning.items()
        if pair[0] in encoded and pair[1] in encoded
    )
    kern = newTable("kern")
    kern.version = 0
    kern.kernTables = []
    # Each format-0 subtable has a 16-bit length field.
    for start in range(0, len(pairs), 10_000):
        table = KernTable_format_0()
        table.version = 0
        table.coverage = 1
        table.kernTable = dict(pairs[start:start + 10_000])
        kern.kernTables.append(table)
    font["kern"] = kern

    # Preserve the i33 scan conversion settings for the unhinted outlines.
    font["gasp"] = newTable("gasp")
    font["gasp"].version = 1
    font["gasp"].gaspRange = {65535: 15}
    font["prep"] = newTable("prep")
    font["prep"].program = Program()
    font["prep"].program.fromAssembly(
        ["PUSHW[ ]", "511", "SCANCTRL[ ]", "PUSHB[ ]", "4", "SCANTYPE[ ]"]
    )
    font["maxp"].maxStackElements = max(1, font["maxp"].maxStackElements)
    font.recalcTimestamp = False
    font["head"].created = font["head"].modified = 3876076800

    names = font["name"]
    names.names = [record for record in names.names if record.nameID not in (16, 17)]
    public_names = {
        1: "Kleyos",
        2: "Regular",
        3: f"{OPENTYPE_VERSION};KLYS;{STEM}",
        4: "Kleyos Regular",
        5: f"Version {OPENTYPE_VERSION}",
        6: STEM,
    }
    for name_id, value in public_names.items():
        for record in names.names:
            if record.nameID == name_id:
                record.string = value
        names.setName(value, name_id, 3, 1, 0x409)

    ttf = out / "fonts" / "ttf" / f"{STEM}.ttf"
    woff2 = out / "fonts" / "woff2" / f"{STEM}.woff2"
    ttf.parent.mkdir(parents=True, exist_ok=True)
    woff2.parent.mkdir(parents=True, exist_ok=True)
    font.save(ttf)
    font.flavor = "woff2"
    font.save(woff2)

    with TTFont(ttf) as desktop, TTFont(woff2) as web:
        assert desktop.keys() == web.keys()
        for tag in desktop.keys():
            if tag not in ("GlyphOrder", "head"):
                assert desktop.getTableData(tag) == web.getTableData(tag), tag
        assert desktop["OS/2"].fsType == 0
        glyph_count = len(desktop.getGlyphOrder())

    required = json.loads((ROOT / "sources/gf-latin-core-map.json").read_text())
    glyph_order = set(font.getGlyphOrder())
    missing = [
        entry["name"] for entry in required["glyphs"]
        if (entry["name"] not in glyph_order if entry["unicode"] is None else entry["unicode"] not in cmap)
    ]
    if missing:
        raise ValueError(f"Missing Google Fonts Latin Core glyphs: {missing}")

    manifest = {
        "name": "Kleyos",
        "version": VERSION,
        "source_iteration": "i33",
        "source": file_record(MASTER, ROOT),
        "source_archive_sha256": "fdb9b8394a5c5b4b878606592b78b5d791f73eef13b9b172d1f5a72b7cda9fa7",
        "source_commit": "9066724660e004dc87ba0a10972fd59eaa2ad3eb",
        "license": "OFL-1.1",
        "reserved_font_name": "Kleyos",
        "repository": "https://github.com/nicro33/kleyos-font",
        "tag": f"v{VERSION}",
        "fonts": [{
            "family": "Kleyos",
            "style": "Regular",
            "opentype_version": OPENTYPE_VERSION,
            "codepoints": len(cmap),
            "glyph_count": glyph_count,
            "space_widths": {"U+0020": 250, "U+00A0": 250, "U+202F": 125},
            "ttf": file_record(ttf, out),
            "woff2": file_record(woff2, out),
        }],
        "latin_core": {
            "reference_revision": required["revision"],
            "entries_checked": len(required["glyphs"]),
            "missing": [],
        },
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Built {STEM} {VERSION} from {MASTER.name} ({len(cmap)} code points).")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT / "build/public")
    build(parser.parse_args().out.resolve())

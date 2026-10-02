# Kleyos 1.0.0 — QA Report

**Status:** PASS with known brush-style contour contacts.

## Binary integrity

- 124 glyphs / 123 encoded characters.
- 1000 UPM.
- 83 legacy kern pairs.
- GPOS + kern present.
- `fsType = 0`.
- Vendor ID `KLYS`.
- Required French/project characters present.

## WOFF2

Roundtrip TTF → WOFF2 preserves cmap, glyph order, horizontal metrics,
kern count and outline signatures for both roles.

## 676 lowercase pairs

Nine pairs have contour contact:

`ho, wo, zo, eo, qo, ko, xo, uo, ao`

These are existing brush-style contacts associated with the left overhang
of `o`. The V1.4-F change only modifies capital `Ç`.

## Remaining publication checks

- Run FontBakery before a Google Fonts submission.
- Test Safari / Chrome / Firefox and major OSes.
- Reserved Font Name: **Kleyos**.

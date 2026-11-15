# Source provenance

Kleyos 1.3.0 uses the editable final i33 UFO. It is stored as
`sources/KleyosMaster.ufoz`, a ZIP of the original UFO 3 directory.
The source came from the i33 archive with SHA-256
`fdb9b8394a5c5b4b878606592b78b5d791f73eef13b9b172d1f5a72b7cda9fa7`.
All 558 entries in the archive checksum inventory were verified on
15 November 2026. The archive identifies source commit
`9066724660e004dc87ba0a10972fd59eaa2ad3eb`.

The build produces one public family, Kleyos Regular, with the i33 Display
spacing and OpenType revision 1.411. The compiled drawing, positioning and
metric tables were compared with the archived i33 Display TTF. The two
packages share those tables byte for byte. See
[build verification](../qa/release-1.3.0/BUILD-VERIFICATION.json).

ChatGPT assisted iterative design and refinement, source generation,
engineering, testing, and documentation under Nicolas Gros’s direction.
Nicolas Gros is credited in AUTHORS.txt and the font metadata. The OFL 1.1
license retains Kleyos as a Reserved Font Name. A Google Fonts review and
any written permission for Google are separate from this release.

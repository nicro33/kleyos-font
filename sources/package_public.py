"""Package the current Kleyos release and verify the archive contents."""
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
QA = "qa/release-1.3.0"


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def package():
    manifest = json.loads((ROOT / "manifest.json").read_text())
    version = manifest["version"]
    family, = manifest["fonts"]
    payload = {
        "AUTHORS.txt", "CHANGELOG.md", "DESCRIPTION.en_us.html", "FONTLOG.txt",
        "OFL.txt", "README.md", "manifest.json", "css/kleyos-regular.css",
        "documentation/PUBLICATION.md", "documentation/PROVENANCE.md",
        "documentation/RELEASE-1.3.0.md", "sources/build_public.py",
        "sources/package_public.py", "sources/requirements-build.lock",
        "sources/gf-latin-core-map.json", "sources/test_web.py",
        manifest["source"]["path"],
        *(p.relative_to(ROOT).as_posix() for p in (ROOT / QA).iterdir() if p.is_file()),
    }
    for kind in ("ttf", "woff2"):
        entry = family[kind]
        if sha(ROOT / entry["path"]) != entry["sha256"]:
            raise ValueError(f"Font checksum mismatch: {entry['path']}")
        payload.add(entry["path"])
    checksums = {name: sha(ROOT / name) for name in sorted(payload)}
    checksums_path = ROOT / "SHA256SUMS.txt"
    checksums_path.write_text("".join(f"{digest}  {name}\n" for name, digest in checksums.items()))
    payload.add(checksums_path.name)
    folder = f"Kleyos-{version}"
    archive = ROOT / "dist" / f"{folder}-Public-Release-RFN.zip"
    with zipfile.ZipFile(archive, "w") as zipped:
        for name in sorted(payload):
            info = zipfile.ZipInfo(f"{folder}/{name}", (2026, 11, 15, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            zipped.writestr(info, (ROOT / name).read_bytes(), compresslevel=9)
    with zipfile.ZipFile(archive) as zipped:
        assert zipped.testzip() is None
        for name, digest in checksums.items():
            assert hashlib.sha256(zipped.read(f"{folder}/{name}")).hexdigest() == digest, name
    digest = sha(archive)
    archive.with_suffix(".zip.sha256").write_text(f"{digest}  {archive.name}\n")
    print(f"{archive.name}: {len(payload)} files, SHA-256 {digest}")


if __name__ == "__main__":
    package()

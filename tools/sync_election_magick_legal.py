#!/usr/bin/env python3
"""Copies Election Magick's legal documents from a local ElectionMagica checkout, verbatim, and updates SOURCE.json.

    python3 tools/sync_election_magick_legal.py /path/to/ElectionMagica

The app bundles LEGAL/*.md; the website must show the same text. Change the documents in ElectionMagica first, then sync.
Only the 15 legal Markdown files and the support text are read; nothing else from that repository is copied.
"""
import hashlib, importlib.util, json, os, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEST = os.path.join(ROOT, "content", "apps", "election-magick", "legal")
LANGS = {"en": "EN", "pt-br": "PT-BR", "es": "ES"}
DOCS = {"privacy": "Privacy-Policy", "terms": "Terms-of-Use", "subscription": "Subscription-Terms",
        "disclaimer": "Disclaimer", "data-retention": "Data-Retention-Policy"}


def main(src):
    commit = subprocess.check_output(["git", "-C", src, "rev-parse", "HEAD"], text=True).strip()
    spec = importlib.util.spec_from_file_location("bw", os.path.join(src, "Tools", "legal", "build_website.py"))
    bw = importlib.util.module_from_spec(spec); spec.loader.exec_module(bw)
    manifest = {"source_repository": "huerlemp2-cloud/ElectionMagica (private)", "source_commit": commit,
                "rule": "Copied verbatim. Edit the documents in ElectionMagica LEGAL/ first (the app bundles them), "
                        "then re-sync with tools/sync_election_magick_legal.py.", "files": {}}
    changed = []
    for d, s in LANGS.items():
        os.makedirs(os.path.join(DEST, d), exist_ok=True)
        items = [(f"{k}.md", f"LEGAL/{v}-{s}.md", open(os.path.join(src, "LEGAL", f"{v}-{s}.md"), "rb").read())
                 for k, v in DOCS.items()]
        items.append(("support.md", f"Tools/legal/build_website.py SUPPORT['{d}']", bw.SUPPORT[d].encode("utf-8")))
        for name, origin, data in items:
            path = os.path.join(DEST, d, name)
            old = open(path, "rb").read() if os.path.exists(path) else None
            if old != data:
                open(path, "wb").write(data); changed.append(f"{d}/{name}")
            manifest["files"][f"{d}/{name}"] = {"source": origin, "sha256": hashlib.sha256(data).hexdigest()}
    with open(os.path.join(DEST, "SOURCE.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
    print(f"synced from {commit[:7]}; changed: {', '.join(changed) or 'nothing'}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])

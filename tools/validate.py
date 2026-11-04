#!/usr/bin/env python3
"""Validates the built site in docs/ and the repository contents. Python 3.9+ standard library only.

    python3 tools/validate.py            preview check: broken links, required pages, forbidden files -> exit 1;
                                         open owner details and legal-review notes are listed, not failed
    python3 tools/validate.py --release  also fails while any owner detail, placeholder or legal-review note remains,
                                         while indexing is off, or while the legal copies differ from SOURCE.json

Writes VALIDATION_REPORT.md at the repository root.
"""
import hashlib, html.parser, json, os, re, sys
from urllib.parse import urlparse, unquote

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS = os.path.join(ROOT, "docs")
RELEASE = "--release" in sys.argv
SITE = json.load(open(os.path.join(ROOT, "site.json"), encoding="utf-8"))

FORBIDDEN_EXT = {".swift", ".xcconfig", ".storekit", ".p8", ".p12", ".cer", ".mobileprovision", ".ipa", ".key", ".pem",
                 ".env", ".xcodeproj", ".pbxproj", ".entitlements", ".plist"}
FORBIDDEN_TEXT = [r"BEGIN [A-Z ]*PRIVATE KEY", r"EM_QA_BUILD", r"EM-QA-ENTITLEMENT", r"QA BUILD", r"\.qa\b(?!\w)",
                  r"codemagic", r"x-auth-token", r"api[_-]?key\s*[:=]", r"ghp_[A-Za-z0-9]{20,}", r"QA_DEVICE_UDID"]
PLACEHOLDERS = [(r"\[\[[A-Z_]+\]\]", "unfilled [[TOKEN]]"), (r"example\.(com|org)", "example domain"),
                (r"\[OWNER[^\]]*\]", "[OWNER …] placeholder"), (r'class="todo"', "owner detail still to be provided"),
                (r"LEGAL REVIEW REQUIRED", "legal review note"), (r"(?i)lorem ipsum", "lorem ipsum"),
                (r"\bTODO\b|\bTBD\b|\bFIXME\b", "TODO/TBD marker")]
REQUIRED = [f"election-magick/{l}/{d}/index.html" for l in ("en", "pt-br", "es") for d in ("privacy", "terms", "support")]
REQUIRED += ["index.html", "404.html", "robots.txt", ".nojekyll", "legal/index.html", "support/index.html",
             "election-magick/index.html", "intellishop/index.html", "dream-tales/index.html"]


class Links(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs, self.ids = [], set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        for k in ("href", "src"):
            if k in a and not (tag == "link" and a.get("rel") in ("canonical", "alternate")) and tag != "meta":
                self.refs.append(a[k])


def resolve(page, ref):
    """Map a relative/absolute reference from a page in docs/ to a file path, or None for external links."""
    u = urlparse(ref)
    if u.scheme or ref.startswith("//"):
        return None
    base_path = urlparse(SITE.get("base_url") or "").path.rstrip("/")
    path = unquote(u.path)
    if path.startswith("/"):
        path = path[len(base_path):] if base_path and path.startswith(base_path) else path
        target = os.path.join(DOCS, path.lstrip("/"))
    elif path == "":
        target = page
    else:
        target = os.path.normpath(os.path.join(os.path.dirname(page), path))
    if os.path.isdir(target) or path.endswith("/"):
        target = os.path.join(target, "index.html")
    return target, u.fragment


def main():
    errors, notes, externals = [], [], {}
    found = {}
    if not os.path.isdir(DOCS):
        print("docs/ missing: run tools/build.py first"); return 1

    for rel in REQUIRED:
        if not os.path.exists(os.path.join(DOCS, rel)):
            errors.append(f"required page missing: /{rel}")

    pages = []
    for dp, _, fs in os.walk(DOCS):
        pages += [os.path.join(dp, f) for f in fs if f.endswith(".html")]
    parsed = {}
    for p in pages:
        lp = Links(); lp.feed(open(p, encoding="utf-8").read()); parsed[p] = lp
    checked = 0
    for p, lp in parsed.items():
        relp = os.path.relpath(p, DOCS)
        for ref in lp.refs:
            if ref.startswith("mailto:"):
                continue
            r = resolve(p, ref)
            if r is None:
                externals.setdefault(ref, set()).add(relp); continue
            target, frag = r
            checked += 1
            if not os.path.exists(target):
                errors.append(f"broken link in /{relp}: {ref}")
            elif frag and target in parsed and frag not in parsed[target].ids:
                errors.append(f"missing anchor in /{relp}: {ref}")

    # placeholders and review notes in the built site
    for p in sorted(pages):
        text = open(p, encoding="utf-8").read()
        relp = os.path.relpath(p, DOCS)
        for pat, label in PLACEHOLDERS:
            n = len(re.findall(pat, text))
            if n:
                found.setdefault(label, {})[relp] = n

    # repository hygiene: nothing private, no QA, no keys
    for dp, dirs, fs in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git",)]
        for f in fs:
            full = os.path.join(dp, f); relp = os.path.relpath(full, ROOT)
            if os.path.splitext(f)[1].lower() in FORBIDDEN_EXT:
                errors.append(f"forbidden file type in repository: {relp}")
            if relp in ("tools/validate.py", "VALIDATION_REPORT.md") or f.endswith((".png", ".jpg", ".webp")):
                continue
            text = open(full, encoding="utf-8", errors="ignore").read()
            for pat in FORBIDDEN_TEXT:
                if re.search(pat, text, re.I if pat == "codemagic" else 0):
                    errors.append(f"forbidden content /{pat}/ in {relp}")

    # legal copies must match the app's documents (SOURCE.json)
    src = os.path.join(ROOT, "content/apps/election-magick/legal/SOURCE.json")
    drift = []
    if os.path.exists(src):
        man = json.load(open(src, encoding="utf-8"))
        for relp, info in man["files"].items():
            data = open(os.path.join(os.path.dirname(src), relp), "rb").read()
            if hashlib.sha256(data).hexdigest() != info["sha256"]:
                drift.append(relp)
        (errors if RELEASE else notes).extend(f"legal copy differs from SOURCE.json: {d}" for d in drift)

    owner_missing = [k for k, v in SITE["owner"].items() if not v]
    if RELEASE:
        if found:
            errors.append("placeholders or legal-review notes remain (see table)")
        if owner_missing:
            errors.append("owner details missing in site.json: " + ", ".join(owner_missing))
        if not SITE.get("indexing"):
            errors.append("indexing is off in site.json (preview mode)")
        if not SITE.get("base_url"):
            errors.append("base_url is not set in site.json")

    status = "FAIL" if errors else "PASS"
    mode = "release" if RELEASE else "preview"
    out = [f"# Validation report ({mode} mode): {status}", "",
           f"- Pages: {len(pages)} · internal links and assets checked: {checked} · broken: "
           f"{sum(1 for e in errors if e.startswith(('broken', 'missing anchor')))}",
           f"- Required pages present: {sum(os.path.exists(os.path.join(DOCS, r)) for r in REQUIRED)}/{len(REQUIRED)}",
           f"- Forbidden files or content: {sum(1 for e in errors if e.startswith('forbidden'))}",
           f"- Legal copies identical to the app's documents (SOURCE.json): {'yes' if not drift else 'NO: ' + ', '.join(drift)}",
           f"- Owner details missing in site.json: {', '.join(owner_missing) or 'none'}",
           f"- Indexing: {'on' if SITE.get('indexing') else 'off (preview: noindex + robots Disallow)'}", ""]
    if errors:
        out += ["## Errors", ""] + [f"- {e}" for e in errors] + [""]
    out += ["## Placeholders and legal-review notes in the built pages", ""]
    if found:
        out += ["| Kind | Pages | Occurrences |", "|---|---|---|"]
        for label, pg in found.items():
            out.append(f"| {label} | {len(pg)} | {sum(pg.values())} |")
        out += ["", "<details><summary>Pages</summary>", ""]
        for label, pg in found.items():
            out.append(f"**{label}**: " + ", ".join(f"/{k} ({v})" for k, v in sorted(pg.items())))
            out.append("")
        out += ["</details>", ""]
    else:
        out += ["None.", ""]
    out += ["## External links (not fetched; open each once before publishing)", ""]
    out += [f"- {u} ({len(p)} pages)" for u, p in sorted(externals.items())] + [""]
    if notes:
        out += ["## Notes", ""] + [f"- {n}" for n in notes] + [""]
    open(os.path.join(ROOT, "VALIDATION_REPORT.md"), "w", encoding="utf-8").write("\n".join(out))
    print("\n".join(out[:9]))
    if errors:
        print("\n".join(errors[:20]))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

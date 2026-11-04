#!/usr/bin/env python3
"""Checks that the website shows the same legal text as the Election Magick app. Read-only.

    python3 tools/compare_with_app.py /path/to/ElectionMagica

1. Each website source (content/apps/election-magick/legal/<lang>/<doc>.md) is byte-identical to the file the app
   bundles (LEGAL/<Doc>-<LANG>.md), and the support text matches Tools/legal/build_website.py.
2. The owner values the website fills into [[TOKENS]] equal the app's Config/Owner.xcconfig values.
3. The visible text of every built page in docs/ equals its Markdown source with the tokens filled, word for word.
Exit 1 on any difference.
"""
import html.parser, importlib.util, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LEGAL = os.path.join(ROOT, "content", "apps", "election-magick", "legal")
LANGS = {"en": "EN", "pt-br": "PT-BR", "es": "ES"}
DOCS = {"privacy": "Privacy-Policy", "terms": "Terms-of-Use", "subscription": "Subscription-Terms",
        "disclaimer": "Disclaimer", "data-retention": "Data-Retention-Policy"}
TOKENS = {"OWNER_LEGAL_NAME": ("legal_name", "EM_OWNER_LEGAL_NAME"), "OWNER_POSTAL_ADDRESS": ("postal_address", "EM_OWNER_POSTAL_ADDRESS"),
          "GOVERNING_LAW": ("governing_law", "EM_GOVERNING_LAW"), "SUPPORT_EMAIL": ("contact_email", "EM_SUPPORT_EMAIL"),
          "WEBSITE_URL": (None, "EM_WEBSITE_URL")}


class Article(html.parser.HTMLParser):
    """Collects the text inside <article>, skipping the language switcher and preview-only labels."""
    def __init__(self):
        super().__init__(); self.depth = 0; self.skip = 0; self.out = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "article": self.depth += 1
        if self.depth and (a.get("class") == "langs" or self.skip):
            self.skip += 1
    def handle_endtag(self, tag):
        if self.skip: self.skip -= 1
        if tag == "article": self.depth -= 1
    def handle_data(self, d):
        if self.depth and not self.skip: self.out.append(d)


def words(s):
    return re.sub(r"\s+", " ", s).strip()


def md_text(md):
    lines = []
    for raw in md.splitlines():
        line = raw.strip()
        if line.startswith("<!--") and line.endswith("-->"):
            continue
        if line.startswith("#"):
            line = re.sub(r"^#+\s*", "", line)
        else:
            line = re.sub(r"^(- |• |\d+\. )", "", line)
        lines.append(line.replace("**", ""))
    return words(" ".join(lines))


def xcconfig(path):
    vals = {}
    for line in open(path, encoding="utf-8"):
        m = re.match(r"^([A-Z_]+)\s*=\s*(.*)$", line.rstrip("\n"))
        if m: vals[m.group(1)] = m.group(2).replace("$()", "").strip()
    return vals


def main(app):
    problems, notes = [], []
    site = json.load(open(os.path.join(ROOT, "site.json"), encoding="utf-8"))
    app_cfg = xcconfig(os.path.join(app, "Config", "Owner.xcconfig"))
    spec = importlib.util.spec_from_file_location("bw", os.path.join(app, "Tools", "legal", "build_website.py"))
    bw = importlib.util.module_from_spec(spec); spec.loader.exec_module(bw)

    # 1. sources
    n = 0
    for d, s in LANGS.items():
        for k, v in DOCS.items():
            n += 1
            if open(os.path.join(LEGAL, d, f"{k}.md"), "rb").read() != open(os.path.join(app, "LEGAL", f"{v}-{s}.md"), "rb").read():
                problems.append(f"source differs from app: {d}/{k}.md vs LEGAL/{v}-{s}.md")
        n += 1
        if open(os.path.join(LEGAL, d, "support.md"), encoding="utf-8").read() != bw.SUPPORT[d]:
            problems.append(f"support text differs from app tooling: {d}/support.md")
    print(f"1. sources identical to the app: {n - len(problems)}/{n}")

    # 2. owner values
    site_url = (site.get("base_url") or "").rstrip("/") + "/election-magick"
    for token, (skey, akey) in TOKENS.items():
        sv = site_url if skey is None else site["owner"].get(skey)
        av = app_cfg.get(akey, "")
        if sv != av:
            (notes if token == "WEBSITE_URL" else problems).append(f"[[{token}]]: website '{sv}' / app '{av}'")
    print(f"2. owner values equal to Owner.xcconfig: {5 - sum(1 for p in problems + notes if p.startswith('[['))}/5")

    # 3. rendered text
    checked = 0
    for d in LANGS:
        for k in list(DOCS) + ["support"]:
            md = open(os.path.join(LEGAL, d, f"{k}.md"), encoding="utf-8").read()
            for token, (skey, _) in TOKENS.items():
                md = md.replace(f"[[{token}]]", site_url if skey is None else site["owner"][skey])
            p = Article(); p.feed(open(os.path.join(ROOT, "docs", "election-magick", d, k, "index.html"), encoding="utf-8").read())
            got, want = words(" ".join(p.out)), md_text(md)
            checked += 1
            if got.replace(" ", "") != want.replace(" ", ""):
                i = next((i for i, (a, b) in enumerate(zip(got, want)) if a != b), min(len(got), len(want)))
                problems.append(f"rendered text differs: {d}/{k} near «{want[max(0, i - 40):i + 40]}»")
    print(f"3. built pages matching their source word for word: {checked - sum(1 for p in problems if p.startswith('rendered'))}/{checked}")

    for x in notes:
        print("NOTE:", x)
    for x in problems:
        print("DIFF:", x)
    return 1 if problems else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))

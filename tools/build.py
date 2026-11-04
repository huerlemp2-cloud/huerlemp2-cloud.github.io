#!/usr/bin/env python3
"""Builds the Huerlem Apps static site into docs/ (served by GitHub Pages, "Deploy from a branch", folder /docs).

Python 3.9+ standard library only. Deterministic: the same content always gives the same files.

    python3 tools/build.py

Sources
  site.json                          site name, base URL, indexing switch, owner details (null = still missing)
  content/i18n/<locale>.json         interface strings
  content/apps/<slug>/app.json       one file per app; add a folder to add an app
  content/apps/<slug>/description.md feature text (optional)
  content/apps/<slug>/legal/<lang>/<doc>.md   legal documents and support text (optional)
  assets/                            stylesheet and images, copied as they are

Missing owner details and "LEGAL REVIEW REQUIRED" notes are rendered as visible markers so the preview shows exactly
what is still open; tools/validate.py --release refuses to pass while any marker remains.
"""
import datetime, html, json, os, re, shutil
from urllib.parse import urlparse

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "docs")
DOC_ORDER = ["privacy", "terms", "subscription", "disclaimer", "data-retention"]
LANG_ATTR = {"en": "en-GB", "pt-br": "pt-BR", "es": "es"}
TODO = "\u0000TODO:{}\u0000"
CUR = ' aria-current="page"'
TODO_RE = re.compile("\u0000TODO:([a-z_]+)\u0000")
YEAR = 2026  # fixed so builds are reproducible; update when the year changes


def load(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as fh:
        return json.load(fh)


SITE = load("site.json")
OWNER = SITE["owner"]
BASE_URL = (SITE.get("base_url") or "").rstrip("/")
BASE_PATH = urlparse(BASE_URL).path.rstrip("/") + "/" if BASE_URL else "/"
I18N = {loc: load(f"content/i18n/{loc}.json") for loc in ("en-GB", "pt-BR", "es")}
EN = I18N["en-GB"]


def t(locale, key, **kw):
    s = I18N[locale].get(key) or EN[key]
    return s.format(**kw) if kw else s


def load_apps():
    apps = []
    base = os.path.join(ROOT, "content", "apps")
    for slug in sorted(os.listdir(base)):
        p = os.path.join(base, slug, "app.json")
        if os.path.isfile(p):
            app = load(os.path.relpath(p, ROOT))
            assert app["slug"] == slug, f"{p}: slug must equal the folder name"
            apps.append(app)
    return sorted(apps, key=lambda a: a["order"])


APPS = load_apps()


# ---------------------------------------------------------------- text helpers
def esc(s):
    return html.escape(s, quote=True)


def owner_or_todo(key):
    v = OWNER.get(key)
    return v if v else TODO.format(key)


def app_email(app):
    return app.get("support_email") or owner_or_todo("contact_email")


def app_url(app):
    return f"{BASE_URL}/{app['slug']}" if BASE_URL else TODO.format("base_url")


def fill_tokens(md, app):
    values = {"OWNER_LEGAL_NAME": owner_or_todo("legal_name"), "OWNER_POSTAL_ADDRESS": owner_or_todo("postal_address"),
              "GOVERNING_LAW": owner_or_todo("governing_law"), "SUPPORT_EMAIL": app_email(app), "WEBSITE_URL": app_url(app)}
    for token, value in values.items():
        md = md.replace(f"[[{token}]]", value)
    return md


def render_todos(s, locale):
    def rep(m):
        key = m.group(1)
        label = I18N[locale].get(f"todo_{key}") or EN.get(f"todo_{key}") or key
        return f'<mark class="todo">{esc(label)}</mark>'
    return TODO_RE.sub(rep, s)


def inline(text, locale):
    s = esc(text)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(https?://[^\s<)]+[^\s<).,;:])", r'<a href="\1">\1</a>', s)
    s = re.sub(r"(?<![\w./:-])([A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+)", r'<a href="mailto:\1">\1</a>', s)
    return render_todos(s, locale)


def md_to_html(md, locale, shift=0):
    """Small Markdown subset used by the legal documents: headings, paragraphs, - and 1. lists, **bold**, bare URLs.
    HTML comments (fact anchors) are dropped. Paragraphs carrying LEGAL REVIEW REQUIRED are flagged."""
    out, para, lst = [], [], None

    def flush():
        nonlocal para
        if para:
            text = " ".join(para)
            body = inline(text, locale)
            if "LEGAL REVIEW REQUIRED" in text:
                out.append(f'<p class="review"><strong>{esc(t(locale, "review_label"))}</strong>{body}</p>')
            else:
                out.append(f"<p>{body}</p>")
            para = []

    def close():
        nonlocal lst
        if lst:
            out.append(f"</{lst}>")
            lst = None

    for raw in md.splitlines():
        line = raw.strip()
        if line.startswith("<!--") and line.endswith("-->"):
            continue
        if not line:
            flush(); close(); continue
        if line.startswith("#"):
            flush(); close()
            level = min(6, len(line) - len(line.lstrip("#")) + shift)
            out.append(f"<h{level}>{inline(line.lstrip('#').strip(), locale)}</h{level}>")
            continue
        m = re.match(r"^(- |• |\d+\. )(.*)$", line)
        if m:
            flush()
            kind = "ol" if m.group(1)[0].isdigit() else "ul"
            if lst != kind:
                close(); out.append(f"<{kind}>"); lst = kind
            out.append(f"<li>{inline(m.group(2), locale)}</li>")
            continue
        if lst:
            close()
        para.append(line)
    flush(); close()
    return "\n".join(out)


# ---------------------------------------------------------------- page shell
def rel(path):
    depth = len([p for p in path.split("/") if p and not p.endswith(".html")])
    return "../" * depth


def plate_class(app):
    return f"app-{app['slug']}"


def page(*, path, locale, title, description, body, alternates=None, image=None, jsonld=None, nav_current=None,
         absolute=False):
    up = BASE_PATH if absolute else rel(path)
    preview = not SITE.get("indexing")
    canonical = f"{BASE_URL}/{path}" if BASE_URL else ""
    head = [
        '<!doctype html>',
        f'<html lang="{locale}">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">',
        f"<title>{esc(title)}</title>",
        f'<meta name="description" content="{esc(description)}">',
        "<meta http-equiv=\"Content-Security-Policy\" content=\"default-src 'none'; style-src 'self'; img-src 'self'; "
        "base-uri 'none'; form-action 'none'\">",
        '<meta name="referrer" content="strict-origin-when-cross-origin">',
        '<meta name="color-scheme" content="light dark">',
        '<meta name="robots" content="noindex, nofollow">' if preview else "",
        f'<link rel="canonical" href="{esc(canonical)}">' if canonical else "",
    ]
    for hl, href in (alternates or []):
        head.append(f'<link rel="alternate" hreflang="{hl}" href="{esc(BASE_URL + "/" + href)}">')
    head += [
        f'<meta property="og:site_name" content="{esc(SITE["site_name"])}">',
        f'<meta property="og:title" content="{esc(title)}">',
        f'<meta property="og:description" content="{esc(description)}">',
        '<meta property="og:type" content="website">',
        f'<meta property="og:url" content="{esc(canonical)}">' if canonical else "",
        f'<meta property="og:image" content="{esc(BASE_URL + "/" + image)}">' if (image and BASE_URL) else "",
        f'<link rel="icon" href="{up}assets/img/favicon.svg" type="image/svg+xml">',
        f'<link rel="stylesheet" href="{up}assets/css/site.css">',
    ]
    if jsonld:
        head.append('<script type="application/ld+json">' + json.dumps(jsonld, ensure_ascii=False).replace("</", "<\\/")
                    + "</script>")
    head.append("</head>")

    def nav_link(key, href, name):
        cur = ' aria-current="page"' if nav_current == name else ""
        return f'<li><a href="{up}{href}"{cur}>{esc(EN[key])}</a></li>'

    header = (f'<a class="skip" href="#content">{esc(t(locale, "skip"))}</a>'
              + (f'<div class="preview" role="note"><div class="wrap">{esc(t(locale, "preview_banner"))}</div></div>'
                 if preview else "")
              + '<header class="site-header" lang="en-GB"><div class="wrap">'
              f'<a class="wordmark" href="{up}">{esc(SITE["site_name"])}</a>'
              f'<nav class="site-nav" aria-label="Main"><ul>{nav_link("nav_apps", "#apps", "apps")}'
              f'{nav_link("nav_support", "support/", "support")}{nav_link("nav_legal", "legal/", "legal")}</ul></nav>'
              "</div></header>")
    owner_name = render_todos(esc(owner_or_todo("legal_name")), "en-GB")
    email = owner_or_todo("contact_email")
    email_html = (render_todos(esc(email), "en-GB") if email.startswith("\u0000")
                  else f'<a href="mailto:{esc(email)}">{esc(email)}</a>')
    footer = ('<footer class="site-footer" lang="en-GB"><div class="wrap">'
              f'<p>{esc(SITE["site_name"])}. {EN["footer_rights"].format(year=YEAR, owner=owner_name)}</p>'
              f'<ul><li>{email_html}</li><li><a href="{up}support/">{esc(EN["nav_support"])}</a></li>'
              f'<li><a href="{up}legal/">{esc(EN["nav_legal"])}</a></li></ul></div></footer>')
    html_text = "\n".join(x for x in head if x) + f'\n<body>\n{header}\n<main id="content">\n{body}\n</main>\n{footer}\n</body>\n</html>\n'
    return html_text.replace("{{UP}}", up)


def write(path, text):
    full = os.path.join(OUT, path)
    if path.endswith("/") or path == "":
        full = os.path.join(full, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


# ---------------------------------------------------------------- app data
def legal_docs(app, lang):
    """[(slug, title, markdown)] that exist for this app and language, in a fixed order, support last."""
    if not app.get("legal"):
        return []
    base = os.path.join(ROOT, "content", "apps", app["slug"], "legal", lang)
    docs = []
    names = list(app["legal"]["documents"]) + (["support"] if app["legal"].get("support") else [])
    for slug in names:
        p = os.path.join(base, f"{slug}.md")
        if os.path.isfile(p):
            with open(p, encoding="utf-8") as fh:
                md = fill_tokens(fh.read(), app)
            title = md.splitlines()[0].lstrip("#").strip()
            docs.append((slug, title, md))
    return docs


def legal_langs(app):
    return list(app["legal"]["languages"].keys()) if app.get("legal") else []


def status_html(app, cls="status"):
    st = app["status"]
    if st == "available" and app.get("app_store_url"):
        return f'<a class="{cls}" href="{esc(app["app_store_url"])}">{esc(EN["status_available"])}</a>'
    return f'<span class="{cls}">{esc(EN["status_" + st])}</span>'


def description_sections(app):
    p = os.path.join(ROOT, "content", "apps", app["slug"], "description.md")
    if not os.path.isfile(p):
        return []
    with open(p, encoding="utf-8") as fh:
        md = fh.read()
    sections = []
    for block in re.split(r"(?m)^## ", md)[1:]:
        heading, _, rest = block.partition("\n")
        sections.append((heading.strip(), rest.strip()))
    return sections


# ---------------------------------------------------------------- pages
def home():
    rows = []
    for app in APPS:
        slug = app["slug"]
        if app["status"] in ("upcoming", "available") and app.get("icon"):
            links = [f'<li><a href="{slug}/">{esc(EN["about_app"])}</a></li>']
            if "en" in legal_langs(app):
                docs = dict((d[0], d[1]) for d in legal_docs(app, "en"))
                for key in ("support", "privacy", "terms"):
                    if key in docs:
                        links.append(f'<li><a href="{slug}/en/{key}/">{esc(docs[key])}</a></li>')
            rows.append(
                f'<li class="plate {plate_class(app)}"><img class="icon" src="{esc(app["icon"])}" alt="" width="112" height="112">'
                f'<div class="plate-body"><h3><a href="{slug}/">{esc(app["name"])}</a></h3>'
                f'<p class="subtitle">{esc(app["subtitle"])}</p><p class="summary">{esc(app["summary"])}</p>'
                f'{status_html(app)}<ul class="links">{"".join(links)}</ul></div></li>')
        else:
            rows.append(f'<li class="upcoming-row"><h3><a href="{slug}/">{esc(app["name"])}</a></h3>'
                        f'<span class="state">{esc(EN["status_" + app["status"]])}</span></li>')
    body = (f'<div class="wrap"><section class="intro"><h1>{esc(EN["home_lede"])}</h1><p>{esc(EN["home_sub"])}</p></section>'
            f'<section class="catalogue" id="apps" aria-labelledby="apps-h"><h2 class="section-title" id="apps-h">{esc(EN["apps_heading"])}</h2>'
            f'<ul>{"".join(rows)}</ul></section></div>')
    jsonld = {"@context": "https://schema.org", "@type": "Organization", "name": SITE["site_name"]}
    if BASE_URL:
        jsonld["url"] = BASE_URL + "/"
    write("", page(path="", locale="en-GB", title=EN["home_title"], description=EN["home_description"], body=body,
                   jsonld=jsonld, nav_current="apps"))


def app_page(app):
    slug = app["slug"]
    if app.get("theme"):
        hero_inner = (f'<img class="icon" src="../{esc(app["icon"])}" alt="{esc(app["name"])} app icon" width="168" height="168">'
                      f'<div><h1>{esc(app["name"])}</h1><p class="subtitle">{esc(app["subtitle"])}</p>'
                      f'<p class="summary">{esc(app["summary"])}</p>{status_html(app)}</div>')
        hero = f'<section class="app-hero {plate_class(app)}"><div class="wrap">{hero_inner}</div></section>'
    else:
        hero = (f'<div class="wrap"><section class="page"><h1>{esc(app["name"])}</h1>'
                f'<p class="lede">{esc(EN["status_" + app["status"]])}. {esc(EN["in_development_note"])}</p></section></div>')
    parts = [hero]
    sections = description_sections(app)
    if sections:
        cells = "".join(f'<section><h3>{esc(h)}</h3>{md_to_html(b, "en-GB")}</section>' for h, b in sections)
        parts.append(f'<div class="wrap features"><h2 class="section-title">{esc(EN["features_heading"])}</h2>'
                     f'<div class="features-grid">{cells}</div></div>')
    if app.get("screenshots"):
        items = "".join(f'<li><figure><img src="../{esc(s["src"])}" alt="{esc(s["alt"])}" width="{s["width"]}" height="{s["height"]}" loading="lazy">'
                        f'<figcaption>{esc(s["caption"])}</figcaption></figure></li>' for s in app["screenshots"])
        parts.append(f'<div class="wrap shots"><h2 class="section-title">{esc(EN["screenshots_heading"])}</h2><ul>{items}</ul></div>')
    langs = legal_langs(app)
    if langs:
        per_lang = {l: {d[0]: d[1] for d in legal_docs(app, l)} for l in langs}
        order = [d[0] for d in legal_docs(app, "en")]
        head = "".join(f'<th scope="col" lang="{LANG_ATTR[l]}">{esc(t(LANG_ATTR[l], "lang_name"))}</th>' for l in langs)
        rows = ""
        for key in order:
            cells = "".join(f'<td lang="{LANG_ATTR[l]}"><a href="{l}/{key}/">{esc(per_lang[l][key])}</a></td>'
                            if key in per_lang[l] else "<td></td>" for l in langs)
            rows += f'<tr><th scope="row">{esc(per_lang["en"][key])}</th>{cells}</tr>'
        parts.append(f'<div class="wrap legal-table"><h2 class="section-title" id="legal">{esc(EN["legal_heading"])}</h2>'
                     f'<div class="table-scroll"><table><caption>{esc(EN["legal_table_caption"].format(app=app["name"]))}</caption>'
                     f'<thead><tr><th scope="col">{esc(EN["document"])}</th>{head}</tr></thead><tbody>{rows}</tbody></table></div></div>')
    else:
        parts.append('<div class="spacer"></div>')
    jsonld = None
    if app.get("theme"):
        jsonld = {"@context": "https://schema.org", "@type": "MobileApplication", "name": app["name"],
                  "operatingSystem": "iOS", "description": app["summary"]}
        if BASE_URL:
            jsonld["url"] = f"{BASE_URL}/{slug}/"
    desc = app.get("summary") or f'{app["name"]}: {EN["status_" + app["status"]]}.'
    write(f"{slug}/", page(path=f"{slug}/", locale="en-GB", title=f'{app["name"]} | {SITE["site_name"]}', description=desc,
                           body="\n".join(parts), image=app.get("icon"), jsonld=jsonld))


def crumbs(locale, items):
    lis = "".join(f'<li><a href="{h}">{esc(n)}</a></li>' if h else f'<li aria-current="page">{esc(n)}</li>' for n, h in items)
    return f'<nav class="crumbs wrap" aria-label="{esc(t(locale, "breadcrumb"))}"><ol>{lis}</ol></nav>'


def legal_pages(app):
    slug = app["slug"]
    langs = legal_langs(app)
    for lang in langs:
        locale = LANG_ATTR[lang]
        docs = legal_docs(app, lang)
        for key, title, md in docs:
            path = f"{slug}/{lang}/{key}/"
            lines = md.splitlines()
            rest = "\n".join(lines[1:]).lstrip("\n")
            meta = ""
            first = rest.split("\n\n", 1)
            if re.match(r"^(Version|Versão|Versión) ", first[0]):
                meta = f'<p class="meta">{inline(first[0], locale)}</p>'
                rest = first[1] if len(first) > 1 else ""
            lang_links = "".join(
                f'<li><a href="../../{l}/{key}/" hreflang="{LANG_ATTR[l]}" lang="{LANG_ATTR[l]}"'
                f'{CUR if l == lang else ""}>{esc(t(LANG_ATTR[l], "lang_name"))}</a></li>'
                for l in langs if any(d[0] == key for d in legal_docs(app, l)))
            others = "".join(f'<li><a href="../{k}/"{CUR if k == key else ""}>{esc(tt)}</a></li>' for k, tt, _ in docs)
            body = (crumbs(locale, [(SITE["site_name"], "../../../"), (app["name"], "../../"), (title, None)])
                    + f'<div class="wrap doc-layout"><article class="doc">'
                    f'<ul class="langs" aria-label="{esc(t(locale, "language"))}">{lang_links}</ul>'
                    f'<h1>{esc(title)}</h1>{meta}{md_to_html(rest, locale, shift=0)}</article>'
                    f'<aside class="doc-aside"><nav aria-label="{esc(t(locale, "documents"))}"><h2>{esc(t(locale, "documents"))}</h2><ul>{others}</ul>'
                    f'<ul><li><a href="../../">{esc(t(locale, "back_to_app", app=app["name"]))}</a></li></ul></nav></aside></div>')
            alternates = [(LANG_ATTR[l], f"{slug}/{l}/{key}/") for l in langs] + [("x-default", f"{slug}/en/{key}/")]
            plain = re.sub(r"\s+", " ", TODO_RE.sub("", re.sub(r"[#*]", "", rest)))[:155].rsplit(" ", 1)[0]
            write(path, page(path=path, locale=locale, title=f'{title} | {app["name"]}', description=plain,
                             body=body, alternates=alternates, nav_current="legal"))
        # language hub: /<slug>/<lang>/
        items = "".join(f'<li><a href="{k}/">{esc(tt)}</a></li>' for k, tt, _ in docs)
        lang_links = "".join(f'<li><a href="../{l}/" hreflang="{LANG_ATTR[l]}" lang="{LANG_ATTR[l]}"'
                             f'{CUR if l == lang else ""}>{esc(t(LANG_ATTR[l], "lang_name"))}</a></li>' for l in langs)
        title = t(locale, "legal_hub_title", app=app["name"])
        body = (crumbs(locale, [(SITE["site_name"], "../../"), (app["name"], "../"), (title, None)])
                + f'<div class="wrap"><section class="page"><ul class="langs" aria-label="{esc(t(locale, "language"))}">{lang_links}</ul>'
                f'<h1>{esc(title)}</h1><p class="lede">{esc(t(locale, "legal_hub_lede", app=app["name"]))}</p>'
                f'<ul class="plain-list">{items}</ul></section></div>')
        alternates = [(LANG_ATTR[l], f"{slug}/{l}/") for l in langs] + [("x-default", f"{slug}/en/")]
        write(f"{slug}/{lang}/", page(path=f"{slug}/{lang}/", locale=locale, title=title,
                                      description=t(locale, "legal_hub_lede", app=app["name"]), body=body,
                                      alternates=alternates, nav_current="legal"))


def legal_index():
    blocks = []
    for app in APPS:
        langs = legal_langs(app)
        if not langs:
            blocks.append(f'<h2>{esc(app["name"])}</h2><p>{esc(EN["legal_none_yet"])}</p>')
            continue
        groups = "".join(
            f'<li lang="{LANG_ATTR[l]}"><a href="../{app["slug"]}/{l}/">{esc(t(LANG_ATTR[l], "lang_name"))}</a>: '
            + ", ".join(f'<a href="../{app["slug"]}/{l}/{k}/">{esc(tt)}</a>' for k, tt, _ in legal_docs(app, l)) + "</li>"
            for l in langs)
        blocks.append(f'<h2>{esc(app["name"])}</h2><ul class="plain-list">{groups}</ul>')
    body = (f'<div class="wrap"><section class="page"><h1>{esc(EN["legal_index_title"])}</h1>'
            f'<p class="lede">{esc(EN["legal_index_lede"])}</p>{"".join(blocks)}</section></div>')
    write("legal/", page(path="legal/", locale="en-GB", title=f'{EN["legal_index_title"]} | {SITE["site_name"]}',
                         description=EN["legal_index_lede"], body=body, nav_current="legal"))


def support_index():
    email = owner_or_todo("contact_email")
    email_html = (render_todos(esc(email), "en-GB") if email.startswith("\u0000")
                  else f'<a href="mailto:{esc(email)}">{esc(email)}</a>')
    rows = []
    for app in APPS:
        if "en" in legal_langs(app) and any(d[0] == "support" for d in legal_docs(app, "en")):
            rows.append(f'<li><a href="../{app["slug"]}/en/support/">{esc(app["name"])}</a></li>')
        else:
            rows.append(f'<li>{esc(app["name"])}: {esc(EN["status_" + app["status"]])}</li>')
    body = (f'<div class="wrap"><section class="page"><h1>{esc(EN["support_title"])}</h1>'
            f'<p class="lede">{esc(EN["support_lede"])}</p><ul class="plain-list">{"".join(rows)}</ul>'
            f'<h2>{esc(EN["contact"])}</h2><p>{esc(EN["support_email_label"])}: {email_html}</p></section></div>')
    write("support/", page(path="support/", locale="en-GB", title=f'{EN["support_title"]} | {SITE["site_name"]}',
                           description=EN["support_lede"], body=body, nav_current="support"))


def not_found():
    links = "".join(f'<li><a href="{{{{UP}}}}{a["slug"]}/">{esc(a["name"])}</a></li>' for a in APPS)
    body = (f'<div class="wrap"><section class="page"><h1>{esc(EN["not_found_title"])}</h1><p class="lede">{esc(EN["not_found_body"])}</p>'
            f'<ul class="plain-list"><li><a href="{{{{UP}}}}">{esc(SITE["site_name"])}</a></li>{links}'
            f'<li><a href="{{{{UP}}}}support/">{esc(EN["nav_support"])}</a></li><li><a href="{{{{UP}}}}legal/">{esc(EN["nav_legal"])}</a></li></ul></section></div>')
    write("404.html", page(path="404.html", locale="en-GB", title=f'{EN["not_found_title"]} | {SITE["site_name"]}',
                           description=EN["not_found_body"], body=body, absolute=True)
          .replace('<link rel="canonical" href="' + BASE_URL + '/404.html">', ""))


def assets():
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(OUT, "assets"))
    css = []
    for app in APPS:
        th = app.get("theme")
        if th:
            css.append(f".{plate_class(app)} {{ --plate: {th['plate']}; --plate-ink: {th['ink']}; --plate-muted: {th['muted']}; "
                       f"--plate-accent: {th['accent']}; --plate-line: {th['line']}; }}")
    with open(os.path.join(OUT, "assets", "css", "site.css"), "a", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(css) + "\n")


def sitemap_and_robots():
    paths = []
    for dirpath, _, files in os.walk(OUT):
        if "index.html" in files:
            r = os.path.relpath(dirpath, OUT).replace(os.sep, "/")
            paths.append("" if r == "." else r + "/")
    paths.sort()
    if BASE_URL:
        urls = "".join(f"<url><loc>{esc(BASE_URL + '/' + p)}</loc></url>" for p in paths)
        with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                     + urls + "</urlset>\n")
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8", newline="\n") as fh:
        if SITE.get("indexing"):
            fh.write("User-agent: *\nAllow: /\n" + (f"Sitemap: {BASE_URL}/sitemap.xml\n" if BASE_URL else ""))
        else:
            fh.write("# Preview: indexing is off in site.json\nUser-agent: *\nDisallow: /\n")


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    open(os.path.join(OUT, ".nojekyll"), "w").close()
    if SITE.get("cname"):
        with open(os.path.join(OUT, "CNAME"), "w", encoding="utf-8") as fh:
            fh.write(SITE["cname"].strip() + "\n")
    assets()
    home()
    for app in APPS:
        app_page(app)
        legal_pages(app)
    legal_index()
    support_index()
    not_found()
    sitemap_and_robots()
    n = sum(len(f) for _, _, f in os.walk(OUT))
    print(f"docs/ written: {n} files ({'preview, indexing off' if not SITE.get('indexing') else 'indexing on'})")


if __name__ == "__main__":
    main()

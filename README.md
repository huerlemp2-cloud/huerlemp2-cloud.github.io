# Huerlem Apps website

Static website for the apps published by Huerlem Apps: Election Magick, IntelliShop and Dream Tales.
It is served by GitHub Pages from the `docs/` folder. There is no server, no database, no cookies, no analytics,
no web fonts and no JavaScript.

## Routes

| URL | Page |
|---|---|
| `/` | Home: the app catalogue |
| `/support/` | Support for all apps, with the contact e-mail |
| `/legal/` | Every app's legal documents, by language |
| `/<app>/` | App page: description, features, screenshots (when real ones exist), links to the documents |
| `/<app>/<lang>/` | The app's support and legal documents in one language (`en`, `pt-br`, `es`) |
| `/<app>/<lang>/<document>/` | One document: `privacy`, `terms`, `subscription`, `disclaimer`, `data-retention`, `support` |
| `/404.html`, `/robots.txt`, `/sitemap.xml` | Generated |

The `/<app>/<lang>/<document>/` addresses are **permanent**: apps link to them from inside the app and from App Store
Connect (Election Magick opens `EM_WEBSITE_URL/<lang>/support`, with `EM_WEBSITE_URL = <site>/election-magick`).
Never rename an app slug or a document slug after release.

## Layout

```
site.json                          site name, base URL, indexing switch, owner details
content/i18n/*.json                interface text (en-GB now; pt-BR and es are used by the legal pages)
content/apps/<slug>/app.json       one folder per app; status: in-development | upcoming | available
content/apps/<slug>/description.md feature text taken from the App Store metadata
content/apps/<slug>/legal/<lang>/  legal documents and support text (Markdown)
assets/                            stylesheet, icons, screenshots
tools/build.py                     builds docs/ (Python 3.9+, standard library only)
tools/validate.py                  link check, required pages, forbidden content, placeholders (--release)
tools/sync_election_magick_legal.py  copies Election Magick's documents verbatim from the app repository
docs/                              generated site (committed; GitHub Pages serves this folder)
```

## Adding an app

1. Create `content/apps/<slug>/app.json` (copy an existing one). Start with `"status": "in-development"` and only
   facts the owner has approved.
2. When its documents exist, add `content/apps/<slug>/legal/<lang>/*.md` and the `"legal"` block in `app.json`.
3. Add real screenshots under `assets/img/<slug>/` and list them in `"screenshots"` (`src`, `alt`, `caption`, `width`,
   `height`). The page shows no screenshot section while the list is empty.
4. `python3 tools/build.py && python3 tools/validate.py`, review, commit.

## Adding a language for the site pages

The site pages are in British English. To add Portuguese (Brazil) or Spanish later, complete the matching file in
`content/i18n/` and set `"enabled": true` for that locale in `site.json`; the paths `/pt-br/` and `/es/` are reserved
for it. App documents already exist in all three languages.

## Rules

- Legal documents for Election Magick are copies of the app's own documents. Change them in the app repository first,
  then run the sync tool. `validate.py --release` fails if a copy differs from `SOURCE.json`.
- Nothing from the app repositories other than those documents, the App Store description and the app icon is
  published here: no source code, keys, build or test files.
- Never invent features, prices, dates or policies for an app.

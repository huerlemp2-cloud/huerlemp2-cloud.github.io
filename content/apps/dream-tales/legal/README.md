# Dream Tales — legal documents (not yet written)

No policy exists for Dream Tales yet, and none may be invented. When the owner approves its documents:

1. Add `<lang>/privacy.md`, `<lang>/terms.md`, `<lang>/support.md` (and any other document) in this folder, with `<lang>` = `en`, `pt-br` or `es`.
2. In `../app.json` set `"legal"` like Election Magick's (languages + documents) and fill `subtitle`, `summary`, `icon`.
3. Run `python3 tools/build.py` and `python3 tools/validate.py`.

The pages then appear at `/dream-tales/<lang>/privacy/`, `/dream-tales/<lang>/support/`, `/dream-tales/<lang>/terms/`.

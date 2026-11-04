# Election Magick V1 — source documents synchronised; HTML rebuild still required

Date: 4 November 2026. **DO NOT PUBLISH.**

Fifteen legal Markdown sources under `content/apps/election-magick/legal/{en,pt-br,es}/` were copied from ElectionMagica `fix/qa-stabilisation` at the legal-draft checkpoint. These match the current substantive terms and have no outstanding `LEGAL REVIEW REQUIRED` labels in the app source.

**Release blocker:** the existing `content/apps/election-magick/legal/SOURCE.json` hash manifest and generated `docs/` HTML still reference older revisions. Rebuild must be done together: from a current checkout run `python3 tools/sync_election_magick_legal.py <ElectionMagica-checkout>`, then `python3 tools/build.py` and `python3 tools/validate.py`. Commit the regenerated `SOURCE.json`, `docs/` and `VALIDATION_REPORT.md`. Make sure hashes match, and old HTML has no legal-review labels.

Keep `site.json.indexing = false` until the owner authorises public deployment. The repository remains private. Do not enable GitHub Pages or start Codemagic builds.

Remaining administrative assessments: conditional ICO result (based on `Not started trading`, must be revisited at commercial activity), EU GDPR Article 27 where applicable, App Privacy disclosures, IAP configuration and TestFlight commercial purchase tests.

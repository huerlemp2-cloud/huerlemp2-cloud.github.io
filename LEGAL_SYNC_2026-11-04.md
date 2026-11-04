# Election Magick V1 — legal synchronisation completed

Date: 4 November 2026. **Preview only: do not publish.**

## Done

- Source: ElectionMagica `fix/qa-stabilisation` @ `3f406eb`, the revised legal documents with no "LEGAL REVIEW REQUIRED" note and the 18+ minimum age.
- `tools/sync_election_magick_legal.py` was run. The 15 legal documents and the 3 support texts were already identical. `SOURCE.json` now records `3f406eb` and the SHA-256 of all 18 files.
- `tools/build.py` regenerated `docs/` (28 HTML pages). `tools/validate.py`: PASS in preview mode. There are no placeholders and no legal-review notes left in the built pages.
- `tools/compare_with_app.py` checked the site against the app:
  - 18/18 sources are byte-identical;
  - 18/18 built pages match their source word for word;
  - 4/5 owner values are equal.

## Still open before public deployment

- **`EM_WEBSITE_URL`.** The app's `Config/Owner.xcconfig` is still `https://example.com`. The website uses `https://huerlemp2-cloud.github.io/election-magick`. That URL appears in the Terms contact line and in the app's Settings → Support link. The two must be equal before release.
- **Indexing.** `site.json.indexing` stays `false` until the owner authorises public deployment. The repository stays private, and GitHub Pages stays off.
- **ICO.** The self-assessment on 4 November 2026 returned "You don't need to pay a fee yet". That result depends on the answer "Not started trading". It is **not** a permanent exemption: repeat the assessment when commercial activity starts (first paid subscription or App Store sale) and pay the fee if it applies from then.
- **Other assessments:**
  - EU GDPR Article 27 representative, where applicable;
  - App Privacy disclosures in App Store Connect;
  - in-app purchase configuration;
  - TestFlight sandbox purchase tests.

# Data Retention Policy

Version 1.0 · Effective 2026-11-01

Election Magick stores the app data described below on your device; we (the developer) keep no copy of that on-device app data. Support correspondence that you send us is handled separately, as described below. This policy explains where each item lives, how long it stays and how to delete it.

## On your device until you delete it

- Saved elections (ritual description, entity, place with coordinates and time zone, date, classification at the time of saving): until you delete them in Saved, use Settings → Delete local data, or delete the app.
- Calculation history (the same kind of inputs and the ranked dates): as above.
- Saved places (name, country, coordinates, time zone): as above.
- Favourite entities and ritual profiles (no location): as above.
- Chosen location for the next calculation (manual choice only; current-location fixes are not stored): until you choose another place, use Delete local data, or delete the app.
- Preferences (language, house system, lunar node, AI explanations switch): until changed or the app is deleted.
- Record of your legal acceptance (document versions, time, app version): until Delete local data or deletion of the app; a material change to a document asks you again.
- Private Cloud Compute consent (disclosure version and time): until you turn Private Cloud Compute off, use Delete local data, or delete the app.

## In the device Keychain

- Consultation allowance record: one-way SHA-256 digests used to prevent resetting the included consultation allowance, stored in the device Keychain for the subscription periods recorded there. The digests do not display ritual text, place or dates in readable form, but may still count as personal data when linked to a device or subscriber. These entries are not removed by the in-app Delete local data command and may persist when the app is deleted because of iOS Keychain behaviour. We do not receive these entries. This is a functional limitation of the current version; if you require assistance with retained records, contact [[SUPPORT_EMAIL]].

## Temporary files

- Exported reports (PDF, text, data file) are written to the app's temporary folder for sharing and deleted after one hour; iOS may remove them earlier. Copies you share or save elsewhere are under your control.

## Held by Apple, not by us

- Purchases and subscription history: Apple (App Store), under Apple's privacy policy. Manage them in your Apple account.
- Apple Maps search and geocoding requests, and Private Cloud Compute requests if you enabled it: processed by Apple as described in the Privacy Policy.
- Crash reports and usage statistics, only if you enabled "Share with App Developers" in iOS Settings: provided by Apple.

## Deleting everything

1. Settings → Delete local data (removes everything in the first section).
2. Delete the app from your device.
3. Optionally cancel the subscription in your Apple account.

## Support messages we receive

Unlike the app's on-device data, messages you send to [[SUPPORT_EMAIL]] are received through our e-mail provider. We retain your contact details, message and any attachments only as long as reasonably needed to handle the request, follow up and meet applicable legal obligations. You may ask us to access or delete this correspondence, subject to legal exceptions. This information is **not** removed by the in-app Delete local data control.

## Contact

[[SUPPORT_EMAIL]]

# model-viewer AR Notes

Google's [`<model-viewer>`](https://modelviewer.dev/) is a web component that renders glTF/GLB models and,
with the `ar` attribute, hands off to the device's native AR:

- **Android** → Google **Scene Viewer** (reads the `.glb` via `src`). Works over http or https.
- **iOS** → **AR Quick Look** (reads the `.usdz` via `ios-src`). Requires a USDZ file; without it the AR
  button still shows but will not launch Quick Look on iPhone/iPad.

## Key attributes used in the template

| Attribute | Purpose |
|-----------|---------|
| `src` | The GLB/GLTF model URL (required). |
| `ios-src` | USDZ model URL for iOS AR Quick Look (required for iOS AR). |
| `ar` | Enables the AR button / native AR handoff. |
| `ar-modes="webxr scene-viewer quick-look"` | Tries WebXR first, then Android Scene Viewer, then iOS Quick Look. |
| `ar-placement="floor"` | Places the model on the floor in AR (`"wall"` also available). |
| `camera-controls` | Lets users orbit/zoom on the preview. |
| `auto-rotate` / `rotation-per-second` | Gentle idle spin on the preview. |
| `shadow-intensity` / `exposure` / `environment-image="neutral"` | Lighting/reflections. |
| `poster` | Image shown while the model loads. |

## Sizing & placement tips

- If the model looks too big/small in AR, add `scale="0.5 0.5 0.5"` (or a single scalar) to `<model-viewer>`
  to pre-scale, or fix the model's units in the export step (see `convert.md`).
- Keep models **under ~25 MB** for fast mobile loading.
- To change the button label, edit the `<button slot="ar-button">` text in `assets/ar-template.html`.
- For offline / no-CDN use, download `model-viewer.min.js` next to the page and change the `<script src>`
  to a relative path, then re-run `launch_ar.py`.

## Platform gotchas

- **iOS + http**: AR Quick Look can be finicky over plain http on some iOS versions; for public sharing use
  the GitHub Pages (https) URL. Local LAN http testing usually works but prefer https (ngrok) if it doesn't.
- **Android + Scene Viewer** requires the **Google Play Services for AR (ARCore)** app installed; most modern
  phones have it. If missing, the page falls back to the in-page 3D preview (still useful).

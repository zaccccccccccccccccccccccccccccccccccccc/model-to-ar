---
name: model-to-ar
description: This skill should be used when the user wants to turn a 3D model (.glb/.gltf/.stl/.3mf) into a scannable QR-code AR experience. It builds a Google model-viewer one-tap AR web page (Android Scene Viewer / iOS AR Quick Look), supports local LAN/ngrok testing without hosting, and can deploy the page to GitHub Pages for public scanning. Trigger phrases include "把3D模型变成AR", "二维码+AR", "扫码看3D模型", "GLB/GLTF 转 AR 二维码", "model to AR QR".
---

# Model To AR

## Overview

Turn any 3D model into a QR-code-triggered AR experience using Google's `<model-viewer>` one-tap AR.
End users scan a QR code that opens a web page; tapping **在 AR 中查看** drops the model into their real space
(Android via Scene Viewer, iOS via AR Quick Look). No app install required. The page can be tested on the local
LAN / via ngrok without any hosting, and published publicly through GitHub Pages (free HTTPS).

## When To Use

- The user has a 3D model and wants people to "scan a QR code to see it in AR on their phone".
- Typical requests: "把3D模型变成AR", "二维码加AR", "扫码看3D模型", "GLB/GLTF 转 AR 二维码".
- Default mechanism is **model-viewer one-tap AR** (chosen for simplicity and cross-platform support).
  A marker-based alternative (model anchored on the QR image itself) is sketched under **Advanced**.

## Prerequisites

- Python 3.10+ (scripts use the standard library plus `segno`). Install segno with `pip install segno`.
- For public sharing: a GitHub account with the `gh` CLI authenticated (`gh auth login`). GitHub Pages
  serves the page over HTTPS at no cost.

## Workflow

1. **Normalize the model** (skip if already `.glb`/`.gltf`):
   - `.stl` / `.3mf` / `.obj` → convert to `.glb` following `references/convert.md`.
   - For iOS AR, also produce a `.usdz` from the `.glb` (see `references/convert.md`). Without a USDZ file the
     AR button still works on Android, but iOS Quick Look will not launch.
2. **Build & test locally** with `scripts/launch_ar.py`: it copies `assets/ar-template.html` into `site/`,
   injects the model path, copies the model (and optional usdz/poster) into `site/`, starts a local server,
   and writes a LAN QR to `site/qr.png`.
   ```
   python scripts/launch_ar.py path/to/model.glb --usdz path/to/model.usdz --poster poster.jpg --port 8000
   ```
   Keep the server running, then on the phone (same Wi-Fi) open the printed `http://<LAN-IP>:<port>/` URL,
   or just scan `site/qr.png`. Verify the model loads and the AR button works.
3. **Deploy publicly (optional)** with `scripts/deploy_pages.py`: it commits & pushes `site/` to the current
   git repo, then prints the public URL.
   ```
   python scripts/deploy_pages.py "add historical king model"
   ```
   Enable Pages (repo **Settings → Pages → Branch: main, Folder: /site**). The public QR URL becomes
   `https://<user>.github.io/<repo>/`. Regenerate the QR with
   `python scripts/qr_generate.py "https://<user>.github.io/<repo>/"`.
   Full GitHub Pages + ngrok walkthrough lives in `references/serving-local.md`.
4. **Share** the QR (printed or on-screen). Recipients scan → web page → tap **在 AR 中查看** → model drops in.

## Scripts

- `scripts/launch_ar.py` — build `site/`, inject the template, copy assets, start a local server, generate a LAN QR.
  Args: `MODEL [--usdz X] [--poster P] [--port N] [--out DIR] [--no-serve]`.
- `scripts/deploy_pages.py` — `git add site/ && commit && push`; prints the resulting Pages URL. Arg: commit message.
- `scripts/qr_generate.py` — standalone QR for any URL. Args: `URL [OUT.png]`.

## Assets

- `assets/ar-template.html` — the `<model-viewer>` page template. Placeholders replaced at build time:
  `__MODEL_GLB__`, `__MODEL_USDZ__`, `__POSTER__`. The `<model-viewer>` library is loaded from a CDN; for fully
  offline use, vendor `model-viewer.min.js` locally and update the `<script src>`.

## References

- `references/model-viewer-notes.md` — `<model-viewer>` AR attributes, the iOS USDZ requirement, Android Scene
  Viewer behavior, and sizing/placement tips.
- `references/convert.md` — STL / 3MF / OBJ → GLB and GLB → USDZ conversion (with Windows notes).
- `references/serving-local.md` — LAN testing, ngrok HTTPS tunnel, GitHub Pages setup, and GitHub file-size limits.

## Advanced (future 同类方案)

To anchor the model **on top of the QR image itself** (marker-based: the model appears beside the scanned code
rather than in free space), replace the template with a MindAR / AR.js image-tracking page and compile the QR
image as a tracking target. The `launch_ar.py` / `deploy_pages.py` transport scripts stay the same. This extension
is left as a future recipe and is intentionally out of scope for the default one-tap flow.

## Notes / Limits

- GitHub enforces a 100 MB/file hard limit; keep models under ~25 MB for fast mobile loading. For larger models
  use Git LFS or an external CDN and point `src`/`ios-src` at the absolute URL.
- iOS requires a USDZ for AR; Android works with GLB via Scene Viewer. Always ship both when targeting all phones.

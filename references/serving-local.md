# Serving & Hosting Notes

WebAR needs the page reachable by the phone. Three options, from quickest to most public.

## 1. Local LAN (fastest iteration, no internet sharing)

`scripts/launch_ar.py` starts Python's `http.server` and prints `http://<LAN-IP>:<port>/`.

- Phone must be on the **same Wi-Fi** as the PC.
- Find the LAN IP: Windows → `ipconfig` → the `IPv4` under your Wi-Fi/Ethernet adapter
  (usually `192.168.x.x`). `launch_ar.py` auto-detects it.
- **Firewall:** when Windows prompts, allow `python` through **Private** networks. If blocked, run once as
  admin or add a rule: `netsh advfirewall firewall add rule name="AR" dir=in action=allow protocol=TCP localport=8000`.
- Open the URL in the phone browser, or scan the generated `docs/qr.png`.
- AR over plain http works on Android Scene Viewer; iOS Quick Look prefers https (use option 2 if it fails).

## 2. ngrok HTTPS tunnel (public link, no hosting account)

Install [ngrok](https://ngrok.com), authenticate once, then in a second terminal:

```bat
ngrok http 8000
```

Copy the `https://xxxx.ngrok-free.app` URL, then regenerate the QR:

```bat
python scripts/qr_generate.py "https://xxxx.ngrok-free.app"
```

Anyone with the QR can open it (the tunnel forwards to your local server). Free tier URLs change on restart.

## 3. GitHub Pages (permanent public URL, free HTTPS)

Best for sharing the final QR broadly. The skill's `docs/` folder is the Pages source.

1. Create the repo and push (see `SKILL.md` workflow / `deploy_pages.py`).
2. In the repo: **Settings → Pages → Build and deployment → Branch: master, Folder: /docs** → Save.
3. Wait ~1 minute. The page is live at `https://<user>.github.io/<repo>/`.
4. Regenerate the public QR:
   ```bat
   python scripts/qr_generate.py "https://<user>.github.io/<repo>/"
   ```

### GitHub file-size limits

- Hard limit **100 MB per file**; recommended **< 25 MB** for snappy mobile loading.
- For larger models: use **Git LFS**, or host the `.glb`/`.usdz` on a CDN / object storage and set `src` /
  `ios-src` in `assets/ar-template.html` to the **absolute https URL** (works because model-viewer fetches
  cross-origin with CORS; most CDNs send permissive CORS headers).

## When to use which

| Goal | Use |
|------|-----|
| Test quickly on your own phone | Local LAN (option 1) |
| Demo to someone remote, temporarily | ngrok (option 2) |
| Ship a QR for everyone, permanently | GitHub Pages (option 3) |

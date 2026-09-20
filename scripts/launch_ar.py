#!/usr/bin/env python3
"""Build a model-viewer AR page into ./site, start a local server, and generate a LAN QR.

Usage:
  python launch_ar.py MODEL.glb [--usdz MODEL.usdz] [--poster poster.jpg]
                              [--port 8000] [--out DIR] [--no-serve]

Behavior:
  1. Copy assets/ar-template.html into <out>/, replacing __MODEL_GLB__ / __MODEL_USDZ__ / __POSTER__.
  2. Copy the model (and optional usdz/poster) into <out>/.
  3. Start `http.server` in <out> (unless --no-serve).
  4. Detect the LAN IP, print the URL, and save a QR (segno) to <out>/qr.png.
"""
import argparse
import os
import shutil
import socket
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "assets", "ar-template.html")


def lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()


def build(model, usdz, poster, out):
    os.makedirs(out, exist_ok=True)
    # Clear previous build artifacts (keep .gitkeep) so stale files don't accumulate.
    for entry in os.listdir(out):
        if entry == ".gitkeep":
            continue
        p = os.path.join(out, entry)
        if os.path.isdir(p):
            shutil.rmtree(p)
        else:
            os.remove(p)
    if not os.path.exists(TEMPLATE):
        sys.exit(f"Template not found: {TEMPLATE}")
    with open(TEMPLATE, encoding="utf-8") as f:
        html = f.read()

    # Copy assets under clean, space-free names so they work on every host (incl. GitHub Pages).
    model_ext = os.path.splitext(model)[1].lower() or ".glb"
    model_name = "model" + model_ext
    usdz_name = "model.usdz" if usdz else ""
    poster_name = ("poster" + (os.path.splitext(poster)[1].lower() or ".jpg")) if poster else ""

    html = html.replace("__MODEL_GLB__", model_name)
    if usdz_name:
        html = html.replace("__MODEL_USDZ__", usdz_name)
    else:
        html = html.replace('    ios-src="__MODEL_USDZ__"\n', "")
    if poster_name:
        html = html.replace("__POSTER__", poster_name)
    else:
        html = html.replace('    poster="__POSTER__"\n', "")

    with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)

    shutil.copy(model, os.path.join(out, model_name))
    if usdz:
        shutil.copy(usdz, os.path.join(out, usdz_name))
    if poster:
        shutil.copy(poster, os.path.join(out, poster_name))
    return {"model": model_name, "usdz": usdz_name, "poster": poster_name}


def make_qr(url, out):
    try:
        import segno
    except ImportError:
        print("NOTE: `segno` not installed -> skip QR. Run `pip install segno`.")
        return
    segno.make(url, error="h").save(os.path.join(out, "qr.png"), scale=10, border=2)
    print(f"QR saved -> {os.path.join(out, 'qr.png')}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("model", help="Path to the .glb/.gltf model")
    ap.add_argument("--usdz", default="", help="Optional .usdz for iOS AR")
    ap.add_argument("--poster", default="", help="Optional poster image")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--out", default="site")
    ap.add_argument("--no-serve", action="store_true")
    a = ap.parse_args()

    out = os.path.abspath(a.out)
    names = build(a.model, a.usdz, a.poster, out)
    print("Built AR page in:", out)
    print("  model :", names["model"])
    if names["usdz"]:
        print("  usdz  :", names["usdz"])

    ip = lan_ip()
    url = f"http://{ip}:{a.port}/"
    print("\nLocal URL (phone on same Wi-Fi):", url)
    make_qr(url, out)

    if a.no_serve:
        return
    print("\nServing... press Ctrl+C to stop.")
    try:
        subprocess.run(
            [sys.executable, "-m", "http.server", str(a.port), "--directory", out],
            check=True,
        )
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()

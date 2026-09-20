#!/usr/bin/env python3
"""Generate a QR code PNG for any URL (pure Python, depends on `segno`).

Usage:
  python qr_generate.py "https://example.com" [output.png]
"""
import sys


def main():
    if len(sys.argv) < 2:
        url = input("Enter the URL to encode: ").strip()
    else:
        url = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "qr.png"
    try:
        import segno
    except ImportError:
        sys.exit("Missing dependency: run `pip install segno` first.")
    qr = segno.make(url, error="h")
    qr.save(out, scale=10, border=2)
    print(f"QR code saved -> {out}")
    print(f"Encoded URL   -> {url}")


if __name__ == "__main__":
    main()

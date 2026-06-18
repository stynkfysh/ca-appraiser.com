#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Process a downloaded Gemini image into a web-ready area/hero image.
Usage: python3 process_city_image.py <slug-or-target> [source_png]
If source omitted, uses the newest Gemini_Generated_Image_*.png in Reports.
Crops the bottom 7% (removes the Gemini sparkle watermark), resizes to 1600px
wide, saves optimized JPEG to images/areas/<slug>.jpg (or images/<target>.jpg
if target starts with 'hero-' or 'og-')."""
import os, sys, glob
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPORTS = "/sessions/optimistic-festive-darwin/mnt/Reports"

def newest_gemini():
    files = glob.glob(os.path.join(REPORTS, "Gemini_Generated_Image_*.png"))
    if not files:
        return None
    return max(files, key=os.path.getmtime)

def process(target, source=None):
    source = source or newest_gemini()
    if not source or not os.path.exists(source):
        print("NO_SOURCE")
        return False
    img = Image.open(source).convert("RGB")
    w, h = img.size
    # crop bottom 7% to remove Gemini sparkle/watermark in corner
    img = img.crop((0, 0, w, int(h * 0.93)))
    # resize to 1600 wide
    tw = 1600
    th = int(img.height * tw / img.width)
    img = img.resize((tw, th), Image.LANCZOS)
    if target.startswith("hero-") or target.startswith("og-"):
        out = os.path.join(ROOT, "images", target + ".jpg")
    else:
        out = os.path.join(ROOT, "images", "areas", target + ".jpg")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.save(out, "JPEG", quality=85, optimize=True)
    print(f"OK {out} ({os.path.getsize(out)//1024} KB, {img.size[0]}x{img.size[1]}) <- {os.path.basename(source)}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: process_city_image.py <slug> [source]")
        sys.exit(1)
    src = sys.argv[2] if len(sys.argv) > 2 else None
    process(sys.argv[1], src)

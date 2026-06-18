#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate branded placeholder images + favicon for CA-Appraiser.com.
Tasteful slate-green/gold gradients with a label; replaced later by Gemini photos."""
import os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import importlib.util

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IMG = os.path.join(ROOT, "images")
AREAS = os.path.join(IMG, "areas")
os.makedirs(AREAS, exist_ok=True)

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
if not os.path.exists(FONT):
    FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

SLATE = (31, 58, 52)
SLATE_DEEP = (21, 43, 39)
SLATE_2 = (45, 79, 71)
GOLD = (200, 150, 42)
SAND = (244, 238, 222)

def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def gradient(w, h, top, bottom):
    base = Image.new("RGB", (w, h), top)
    px = base.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        # ease
        t = t * t * (3 - 2 * t)
        r = int(top[0] + (bottom[0]-top[0])*t)
        g = int(top[1] + (bottom[1]-top[1])*t)
        b = int(top[2] + (bottom[2]-top[2])*t)
        for x in range(w):
            px[x, y] = (r, g, b)
    return base

def add_texture(img, seed):
    # subtle diagonal "ridge" bands for visual interest, varied by seed
    w, h = img.size
    overlay = Image.new("RGB", (w, h), (0,0,0))
    od = ImageDraw.Draw(overlay)
    import random
    rnd = random.Random(seed)
    n = 5
    for i in range(n):
        x0 = rnd.randint(-w//3, w)
        col = (rnd.randint(40,70), rnd.randint(70,100), rnd.randint(60,90))
        od.polygon([(x0,0),(x0+w//2,0),(x0+w//2-h, h),(x0-h, h)], fill=col)
    overlay = overlay.filter(ImageFilter.GaussianBlur(40))
    return Image.blend(img, Image.composite(overlay, img, Image.new("L",(w,h),28)), 0.5)

def wrap(draw, text, fnt, maxw):
    words = text.split()
    lines, cur = [], ""
    for wd in words:
        test = (cur + " " + wd).strip()
        if draw.textlength(test, font=fnt) <= maxw:
            cur = test
        else:
            if cur: lines.append(cur)
            cur = wd
    if cur: lines.append(cur)
    return lines

def make(path, w, h, title, subtitle, seed):
    img = gradient(w, h, SLATE_2, SLATE_DEEP)
    img = add_texture(img, seed)
    d = ImageDraw.Draw(img)
    # gold accent bar
    d.rectangle([0, h-14, w, h], fill=GOLD)
    # monogram top-left
    mf = font(FONT, int(h*0.05))
    d.text((int(w*0.06), int(h*0.10)), "CA-APPRAISER.COM", font=font(FONT_SANS, int(h*0.035)), fill=(230,222,200))
    # title
    tf = font(FONT, int(h*0.11))
    lines = wrap(d, title, tf, int(w*0.84))
    total_h = len(lines)*int(h*0.13)
    y = (h - total_h)//2 + int(h*0.04)
    for ln in lines:
        tw = d.textlength(ln, font=tf)
        d.text(((w-tw)//2, y), ln, font=tf, fill=SAND)
        y += int(h*0.13)
    if subtitle:
        sf = font(FONT_SANS, int(h*0.042))
        sw = d.textlength(subtitle, font=sf)
        d.text(((w-sw)//2, y+int(h*0.01)), subtitle, font=sf, fill=GOLD)
    img.save(path, "JPEG", quality=86, optimize=True)

# ---- shared heroes ----
shared = [
    ("hero-home.jpg", "California Home Appraisals", "Certified · Independent · Clear"),
    ("hero-estate.jpg", "Estate & Date-of-Death Valuations", "Step-up in basis · Probate · Trusts"),
    ("hero-keys.jpg", "Divorce & Transfer Appraisals", "Neutral · Defensible · Court-ready"),
    ("hero-documents.jpg", "Litigation & Bankruptcy Reports", "USPAP & IRS compliant"),
    ("hero-contact.jpg", "Request an Appraisal", "Free, no-pressure consultation"),
    ("hero-aerial.jpg", "Serving 130+ California Communities", "San Diego · Riverside · Statewide"),
]
for i,(fn,t,s) in enumerate(shared):
    make(os.path.join(IMG, fn), 1600, 760, t, s, seed=i+1)
make(os.path.join(IMG, "og-default.jpg"), 1200, 630, "CA-Appraiser.com", "Certified California Real Estate Appraiser", seed=99)

# ---- area images ----
spec = importlib.util.spec_from_file_location("content_data", os.path.join(ROOT, "build", "content_data.py"))
cd = importlib.util.module_from_spec(spec); spec.loader.exec_module(cd)
from content_area import SLUGS  # type: ignore
import sys; sys.path.insert(0, os.path.join(ROOT, "build"))
from content_area import SLUGS

count = 0
for idx, slug in enumerate(SLUGS):
    c = cd.CITIES[slug]
    make(os.path.join(AREAS, slug + ".jpg"), 1600, 760, c["name"], c["county"], seed=idx+100)
    count += 1
print(f"shared images: {len(shared)+1}, area images: {count}")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate all city + hero images via the Google Gemini image API.
Reads the API key from env GEMINI_API_KEY (or first CLI arg).
Auto-detects an image-capable model, builds a scene-aware prompt per city,
saves + processes each into images/areas/<slug>.jpg (1600px, optimized JPEG).

Usage:
  GEMINI_API_KEY=... python3 gen_images_api.py            # all cities + heroes
  GEMINI_API_KEY=... python3 gen_images_api.py probe      # just list models
  GEMINI_API_KEY=... python3 gen_images_api.py san-marcos vista   # specific slugs
"""
import os, sys, json, time, base64, io, urllib.request, urllib.error
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "build"))
import content_data
from content_area import SLUGS

API = "https://generativelanguage.googleapis.com/v1beta"
KEY = os.environ.get("GEMINI_API_KEY") or (sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].startswith("AIza") else "")

HEROES = {
    "hero-estate": "a warm, established California family home exterior at golden hour, welcoming covered front porch, mature oak and magnolia trees, soft morning light, evoking family legacy and estate",
    "hero-keys": "a tasteful California suburban two-story home with a manicured front yard and a for-sale-style setting, bright clear daylight, calm and neutral",
    "hero-documents": "a clean, professional residential streetscape of well-kept California homes under a blue sky, orderly and trustworthy, late-morning light",
    "hero-contact": "an inviting California home exterior with an open front walkway and bright friendly daylight, approachable and warm",
    "hero-aerial": "a high aerial drone view over sprawling California residential neighborhoods stretching to distant hills, rooftops and tree-lined streets, clear day",
    "og-default": "an upscale California residential neighborhood with palm trees and Spanish-tile homes at golden hour, wide establishing shot",
}

def scene_for(c):
    t = (c["blurb"] + " " + c["homes"]).lower()
    if any(k in t for k in ["beach", "coastal", "ocean", "surf", "harbor", "waterfront", "bluff", "seaside"]):
        return "a sunny coastal California neighborhood near the ocean, single-family homes, palm trees, blue sky"
    if any(k in t for k in ["desert", "coachella", "palm springs", "mid-century modern"]):
        return "a desert-resort California neighborhood, palm trees, mountains in the background, clear sky, warm light"
    if any(k in t for k in ["rural", "ranch", "grove", "acreage", "equestrian", "country", "agricultural", "mountain", "backcountry", "vineyard", "wine"]):
        return "a rural California residential property with a custom home on acreage, rolling hills, mature trees, golden light"
    if any(k in t for k in ["downtown", "urban", "high-rise", "dense", "victorian", "craftsman", "bungalow", "historic"]):
        return "a charming established California neighborhood with character homes and tree-lined streets, warm afternoon light"
    return "a pleasant suburban California neighborhood of single-family homes, green lawns, blue sky, warm light"

def prompt_for(slug):
    if slug in HEROES:
        scene = HEROES[slug]
    else:
        c = content_data.CITIES[slug]
        scene = scene_for(c) + f", representative of {c['name']}, {c['county']}, California"
    return ("Photorealistic 16:9 landscape photograph, professional real-estate / architectural style: "
            + scene + ". Natural lighting, high detail, no text, no watermark, no logos, no people, no cars in focus.")

def http_post(url, payload):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode())

def http_get(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.loads(r.read().decode())

def list_models():
    d = http_get(f"{API}/models?key={KEY}&pageSize=200")
    return d.get("models", [])

def pick_models():
    """Return (imagen_models, gemini_image_models) by capability."""
    imagen, gem = [], []
    try:
        for m in list_models():
            name = m.get("name", "").replace("models/", "")
            methods = m.get("supportedGenerationMethods", [])
            low = name.lower()
            if "imagen" in low and "predict" in methods:
                imagen.append(name)
            elif "image" in low and "generateContent" in methods:
                gem.append(name)
    except Exception as e:
        print("model-list error:", e)
    # sensible ordering: newest first heuristics
    imagen.sort(reverse=True); gem.sort(reverse=True)
    return imagen, gem

def gen_imagen(model, prompt):
    url = f"{API}/models/{model}:predict?key={KEY}"
    payload = {"instances": [{"prompt": prompt}],
               "parameters": {"sampleCount": 1, "aspectRatio": "16:9"}}
    d = http_post(url, payload)
    preds = d.get("predictions", [])
    if preds and "bytesBase64Encoded" in preds[0]:
        return base64.b64decode(preds[0]["bytesBase64Encoded"])
    raise RuntimeError("no image in imagen response: " + json.dumps(d)[:200])

def gen_gemini(model, prompt):
    url = f"{API}/models/{model}:generateContent?key={KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}],
               "generationConfig": {"responseModalities": ["IMAGE"]}}
    d = http_post(url, payload)
    for cand in d.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            inline = part.get("inlineData") or part.get("inline_data")
            if inline and inline.get("data"):
                return base64.b64decode(inline["data"])
    raise RuntimeError("no image in gemini response: " + json.dumps(d)[:200])

def save_processed(raw, slug):
    img = Image.open(io.BytesIO(raw)).convert("RGB")
    w, h = img.size
    tw = 1600
    th = int(h * tw / w)
    img = img.resize((tw, th), Image.LANCZOS)
    if slug.startswith("hero-") or slug.startswith("og-"):
        out = os.path.join(ROOT, "images", slug + ".jpg")
    else:
        out = os.path.join(ROOT, "images", "areas", slug + ".jpg")
    img.save(out, "JPEG", quality=85, optimize=True)
    return out, os.path.getsize(out)

def main():
    if not KEY:
        print("ERROR: no GEMINI_API_KEY"); sys.exit(2)
    imagen, gem = pick_models()
    print("Imagen models:", imagen[:5])
    print("Gemini image models:", gem[:5])
    if len(sys.argv) > 1 and sys.argv[1] == "probe":
        return
    # prefer standard Imagen 4 (quality/cost balance) over ultra/fast
    preferred = ["imagen-4.0-generate-001", "imagen-4.0-fast-generate-001", "imagen-4.0-ultra-generate-001"]
    for pm in preferred:
        if pm in imagen:
            imagen = [pm] + [m for m in imagen if m != pm]
            break
    override = os.environ.get("GEN_MODEL")
    if override:
        imagen = [override]
    use_imagen = bool(imagen)
    model = imagen[0] if use_imagen else (gem[0] if gem else None)
    if not model:
        print("ERROR: no image-capable model available for this key"); sys.exit(3)
    print("Using model:", model, "(imagen)" if use_imagen else "(gemini)")

    import threading
    from concurrent.futures import ThreadPoolExecutor
    DONE = "/tmp/caa_done.txt"
    done = set()
    if os.path.exists(DONE):
        done = set(open(DONE).read().split())

    args = [a for a in sys.argv[1:] if not a.startswith("AIza") and a != "probe" and not a.isdigit()]
    batch = next((int(a) for a in sys.argv[1:] if a.isdigit()), 0)
    all_targets = args if args else (list(HEROES.keys()) + [s for s in SLUGS if s != "san-diego"])
    targets = [t for t in all_targets if t not in done]
    if batch:
        targets = targets[:batch]
    print(f"to do this run: {len(targets)} (remaining overall: {len([t for t in all_targets if t not in done])})")

    lock = threading.Lock()
    counts = {"ok": 0, "fail": 0}

    def work(slug):
        p = prompt_for(slug)
        for attempt in range(4):
            try:
                raw = gen_imagen(model, p) if use_imagen else gen_gemini(model, p)
                out, sz = save_processed(raw, slug)
                with lock:
                    counts["ok"] += 1
                    with open(DONE, "a") as f:
                        f.write(slug + "\n")
                    print(f"OK {slug} ({sz//1024}KB)")
                return
            except urllib.error.HTTPError as e:
                try: body = e.read().decode()[:140]
                except Exception: body = ""
                if e.code == 429:
                    time.sleep(4 + attempt * 4)
                else:
                    print(f"HTTP {e.code} {slug}: {body}")
                    if attempt == 3:
                        with lock: counts["fail"] += 1
            except Exception as e:
                if attempt == 3:
                    print(f"ERR {slug}: {e}")
                    with lock: counts["fail"] += 1
                time.sleep(2)

    workers = int(os.environ.get("WORKERS", "5"))
    with ThreadPoolExecutor(max_workers=workers) as ex:
        list(ex.map(work, targets))
    print(f"DONE ok={counts['ok']} fail={counts['fail']}")

if __name__ == "__main__":
    main()

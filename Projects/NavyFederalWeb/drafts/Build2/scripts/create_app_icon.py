#!/usr/bin/env python3
"""Fetch artwork of verified official App Store listing 370811491 and create iOS icon catalog.
Fails closed if the listing or official image cannot be verified. Never calls banking services.
"""
import hashlib
import json
import pathlib
import re
import subprocess
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "BankWebAccess/Assets.xcassets/AppIcon.appiconset"
OUT.mkdir(parents=True, exist_ok=True)
agent = {"User-Agent": "Mozilla/5.0 BankWebAccess personal source build"}

def get(url):
    req = urllib.request.Request(url, headers=agent)
    with urllib.request.urlopen(req, timeout=35) as response:
        return response.read()

listing = json.loads(get("https://itunes.apple.com/lookup?id=370811491&country=us").decode("utf-8"))
matches = [v for v in listing.get("results", []) if v.get("trackId") == 370811491]
if len(matches) != 1:
    raise RuntimeError("Cannot verify Navy Federal official App Store listing")
app = matches[0]
if app.get("trackName") != "Navy Federal Credit Union" or "Navy Federal" not in app.get("sellerName", ""):
    raise RuntimeError("App Store identity mismatch; refusing nonofficial artwork")
original_url = app.get("artworkUrl512", "")
if not original_url:
    raise RuntimeError("Verified official app did not supply artwork URL")
parts = urllib.parse.urlsplit(original_url)
if parts.scheme != "https" or not (parts.hostname or "").endswith(".mzstatic.com"):
    raise RuntimeError("Artwork host is not Apple's mzstatic CDN")
url = re.sub(r"/\\d+x\\d+bb\\.[A-Za-z0-9]+(?:\\?.*)?$", "/1024x1024bb.png", original_url)
try:
    data = get(url)
except Exception:
    url = original_url
    data = get(url)
if len(data) < 5000:
    raise RuntimeError("Official icon image is unexpectedly small")
raw = OUT / "_original_artwork"
raw.write_bytes(data)
subprocess.run(["sips", "-s", "format", "png", "-z", "1024", "1024", str(raw), "--out", str(OUT / "icon-1024.png")], check=True, stdout=subprocess.DEVNULL)
raw.unlink()
dims = subprocess.check_output(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(OUT / "icon-1024.png")], text=True)
if "pixelWidth: 1024" not in dims or "pixelHeight: 1024" not in dims:
    raise RuntimeError("Icon decode/dimensions verification failed")
entries = [
    ("20x20","iphone",2,"icon-40.png"),
    ("20x20","iphone",3,"icon-60.png"),
    ("29x29","iphone",2,"icon-58.png"),
    ("29x29","iphone",3,"icon-87.png"),
    ("40x40","iphone",2,"icon-80.png"),
    ("40x40","iphone",3,"icon-120.png"),
    ("60x60","iphone",2,"icon-120.png"),
    ("60x60","iphone",3,"icon-180.png"),
    ("1024x1024","ios-marketing",1,"icon-1024.png"),
]
for size, idiom, scale, name in entries:
    if name == "icon-1024.png": continue
    px = int(size.split("x")[0]) * scale
    subprocess.run(["sips", "-z", str(px), str(px), str(OUT / "icon-1024.png"), "--out", str(OUT / name)], check=True, stdout=subprocess.DEVNULL)
catalog = {"images": [{"size": size, "idiom": idiom, "filename": name, "scale": str(scale) + "x"} for size,idiom,scale,name in entries],
           "info": {"author":"xcode","version":1}}
(OUT / "Contents.json").write_text(json.dumps(catalog, indent=2) + "\n")
metadata = {"trackId":370811491, "trackName":app["trackName"], "sellerName":app["sellerName"], "officialArtworkURL":url,
            "officialArtworkSHA256":hashlib.sha256(data).hexdigest(), "icon1024SHA256":hashlib.sha256((OUT / "icon-1024.png").read_bytes()).hexdigest()}
(OUT / "official_icon_provenance.json").write_text(json.dumps(metadata, indent=2)+"\n")
print(json.dumps(metadata, indent=2))

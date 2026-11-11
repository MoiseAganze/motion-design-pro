"""Rebuild the scrollable right-hand drawers of the legality screen from two captures (scroll 0 and max).

Usage: python drawers.py <captures_dir> <project_dir>
"""
import json
import sys

from PIL import Image

D, PROJ = sys.argv[1], sys.argv[2]
bx = json.load(open(D + "/boxes.json"))
for sig in ["0163", "0186"]:
    a, b = Image.open(f"{D}/m_sig{sig}_a.png"), Image.open(f"{D}/m_sig{sig}_b.png")
    m = bx[f"m_sig{sig}_scroll"]["max"]
    x0 = 880 * 2
    # header (page y 255..344) + body window (344..900, 556 px) at scroll 0, then the rest of the body at max scroll
    out = Image.new("RGB", (560 * 2, (89 + 556 + m) * 2), "white")
    out.paste(a.crop((x0, 255 * 2, 1440 * 2, 900 * 2)), (0, 0))
    out.paste(b.crop((x0, (344 + 556 - m) * 2, 1440 * 2, 900 * 2)), (0, (89 + 556) * 2))
    out.save(f"{PROJ}/assets/ui/drawer_{sig}.webp", "WEBP", quality=90, method=6)

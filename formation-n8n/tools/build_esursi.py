"""Writes the n8n canvas markup for scene 3 from the node positions measured on the
person's screenshot "Agent Courriers ESURSI" (assets/img/workflow-courriers-esursi.png).
World coordinates = (screenshot - (92.5, 200)) * K + (200, 400). Prints HTML to stdout."""
K = 4.0
OX, OY = 200, 400


def W(x, y):
    return ((x - 92.5) * K + OX, (y - 200) * K + OY)


# id, label, kind, screenshot centre
NODES = [
    ("trig", "Email Trigger (IMAP)", "trigger", (92.5, 235)),
    ("prep", "Préparer le mail", "code", (156, 235)),
    ("auto", "Mail automatique ?", "if", (225, 235)),
    ("pj", "Pièce jointe valide ?", "if", (292.5, 235)),
    ("ocrq", "Préparer requête OCR", "code", (361, 201)),
    ("ocr", "Extraction OCR (OpenRouter)", "http", (429.5, 201)),
    ("txt", "Texte du document", "code", (498, 201)),
    ("lis", "Document lisible ?", "if", (600, 201)),
    ("agent", "AI Agent", "agent", (687.5, 200)),
    ("dec", "Décider", "code", (761.5, 200)),
    ("sw", "Décision", "switch", (830, 210)),
    ("gec", "Enregistrer dans le GEC", "http", (899, 152)),
    ("jr", "Journal enregistré", "table", (966.5, 152)),
    ("ar", "Accusé de réception", "mail", (1035, 152)),
]
SIZE = {"agent": (268, 116), "switch": (120, 192)}

ICON = {
    "trigger": '<svg viewBox="0 0 48 48" fill="none" stroke="#2FBF71" stroke-width="3.6" stroke-linejoin="round" stroke-linecap="round"><path d="M6 26 L12 10 H36 L42 26 V38 H6 Z"/><path d="M6 26 H16 L19 31 H29 L32 26 H42"/></svg>',
    "code": '<div class="s3-braces">{ }</div>',
    "if": '<svg viewBox="0 0 48 48" fill="none" stroke="#00C950" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><path d="M6 14 H16 C22 14 24 34 32 34 H40"/><path d="M6 14 H40"/><path d="M34 8 L40 14 L34 20"/><path d="M34 28 L40 34 L34 40"/></svg>',
    "http": '<svg viewBox="0 0 48 48" fill="none" stroke="#898FFF" stroke-width="3.4"><circle cx="24" cy="24" r="17"/><ellipse cx="24" cy="24" rx="7.5" ry="17"/><path d="M7 24 H41 M10 15 H38 M10 33 H38"/></svg>',
    "agent": '<svg viewBox="0 0 48 48" fill="none" stroke="#FFFFFF" stroke-width="3.2" stroke-linejoin="round" stroke-linecap="round"><rect x="9" y="15" width="30" height="22" rx="8"/><circle cx="18.5" cy="26" r="2.6" fill="#FFFFFF"/><circle cx="29.5" cy="26" r="2.6" fill="#FFFFFF"/><path d="M24 15 V9"/><circle cx="24" cy="7.5" r="2.2"/><path d="M5 24 V30 M43 24 V30"/></svg>',
    "switch": '<svg viewBox="0 0 48 48" fill="none" stroke="#3B9CF0" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"><path d="M6 24 H18"/><path d="M18 24 C24 24 24 10 32 10 H40"/><path d="M18 24 H40"/><path d="M18 24 C24 24 24 38 32 38 H40"/><path d="M35 6 L40 10 L35 14"/><path d="M35 34 L40 38 L35 42"/></svg>',
    "table": '<svg viewBox="0 0 48 48" fill="none" stroke="#FF6D00" stroke-width="3.6" stroke-linejoin="round"><rect x="8" y="9" width="32" height="30" rx="3"/><path d="M8 19 H40 M8 29 H40 M19 9 V39 M29 9 V39"/></svg>',
    "mail": '<svg viewBox="0 0 48 48" fill="none" stroke="#FFFFFF" stroke-width="3.4" stroke-linejoin="round"><rect x="7" y="11" width="34" height="26" rx="3"/><path d="M7 13 L24 26 L41 13"/></svg>',
}


def node_html(nid, label, kind, c):
    x, y = W(*c)
    w, h = SIZE.get(kind, (120, 120))
    cls = "s3-node" + (" s3-trigger" if kind == "trigger" else "") + (" s3-agent" if kind == "agent" else "")
    inner = f'<div class="s3-ico">{ICON[kind]}</div>'
    if kind == "agent":
        inner = f'<div class="s3-ico s3-ico-agent">{ICON[kind]}</div><div class="s3-agent-name">AI Agent</div>'
    lab = "" if kind == "agent" else f'<div class="s3-label" style="top: {h + 14}px">{label}</div>'
    bolt = '<svg class="s3-bolt" viewBox="0 0 20 28"><path d="M12 0 L2 16 H9 L7 28 L18 10 H11 Z" fill="#FF6D5A"/></svg>' if kind == "trigger" else ""
    return (f'<div class="{cls}" id="s3-n-{nid}" style="left: {x - w / 2:.0f}px; top: {y - h / 2:.0f}px; width: {w}px; height: {h}px">'
            f'{bolt}{inner}<div class="s3-ok"><svg viewBox="0 0 24 24"><path d="M6 12.5 L10.5 17 L18.5 8" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg></div>{lab}</div>')


def port_out(n):
    nid, _, kind, c = n
    x, y = W(*c)
    w, h = SIZE.get(kind, (120, 120))
    if kind == "if":
        return (x + w / 2, y - 22)  # "true" output
    if kind == "switch":
        return (x + w / 2, y - 66)  # first rule output
    return (x + w / 2, y)


def port_in(n):
    nid, _, kind, c = n
    x, y = W(*c)
    w, h = SIZE.get(kind, (120, 120))
    return (x - w / 2, y)


out = []
paths = []
for a, b in zip(NODES, NODES[1:]):
    (x1, y1), (x2, y2) = port_out(a), port_in(b)
    # "Mail automatique ?" leaves by its false output toward "Pièce jointe valide ?"
    if a[0] == "auto":
        x1, y1 = port_out(a)[0], W(*a[3])[1] + 22
    dx = max(60, (x2 - x1) * 0.5)
    paths.append((a[0], b[0], f"M{x1:.0f} {y1:.0f} C {x1 + dx:.0f} {y1:.0f} {x2 - dx:.0f} {y2:.0f} {x2:.0f} {y2:.0f}"))

# faint branches that hint at the rest of the real workflow
stubs = []
def stub(n, dy_out, d):
    x, y = port_out(n)
    return d
ax, ay = W(225, 235)
stubs.append(f"M{ax + 60:.0f} {ay - 22:.0f} H {ax + 150:.0f}")                     # Mail automatique ? -> true (end)
px, py = W(292.5, 235)
stubs.append(f"M{px + 60:.0f} {py + 22:.0f} C {px + 170:.0f} {py + 22:.0f} {px + 120:.0f} {py + 420:.0f} {px + 260:.0f} {py + 420:.0f}")  # -> Historique des refus
gx, gy = W(687.5, 200)
stubs.append(f"M{gx + 134:.0f} {gy + 22:.0f} C {gx + 330:.0f} {gy + 22:.0f} {gx + 360:.0f} {gy + 700:.0f} {gx + 560:.0f} {gy + 760:.0f}")  # AI Agent error -> Préparer échec
sx, sy = W(830, 210)
for k, dy in enumerate((-22, 22, 66)):
    stubs.append(f"M{sx + 60:.0f} {sy + dy:.0f} C {sx + 170:.0f} {sy + dy:.0f} {sx + 150:.0f} {sy + dy + 40 + k * 60:.0f} {sx + 300:.0f} {sy + dy + 40 + k * 60:.0f}")
ex, ey = W(1035, 152)
stubs.append(f"M{ex + 60:.0f} {ey:.0f} H {ex + 150:.0f}")

# sub-nodes of the AI Agent: OpenRouter Chat Model, Structured Output Parser
subs = [("model", "OpenRouter Chat Model", (642.5, 276), "openrouter"), ("parser", "Structured Output Parser", (701, 276), "parser")]
sub_html = []
for sid, label, c, icon in subs:
    x, y = W(*c)
    ico = '<img src="assets/icons/openrouter-blanc.svg" alt="" />' if icon == "openrouter" else '<div class="s3-braces s3-braces-sm">{⋯}</div>'
    sub_html.append(f'<div class="s3-sub" id="s3-s-{sid}" style="left: {x - 46:.0f}px; top: {y - 46:.0f}px">{ico}<div class="s3-label" style="top: 106px">{label}</div></div>')
gx, gy = W(687.5, 200)
dashed = [f"M{gx - 90:.0f} {gy + 58:.0f} C {gx - 90:.0f} {gy + 130:.0f} {W(642.5, 276)[0]:.0f} {W(642.5, 276)[1] - 120:.0f} {W(642.5, 276)[0]:.0f} {W(642.5, 276)[1] - 46:.0f}",
          f"M{gx + 90:.0f} {gy + 58:.0f} C {gx + 90:.0f} {gy + 130:.0f} {W(701, 276)[0]:.0f} {W(701, 276)[1] - 120:.0f} {W(701, 276)[0]:.0f} {W(701, 276)[1] - 46:.0f}"]

print('<svg id="s3-wires" viewBox="0 0 4200 1000" width="4200" height="1000" fill="none" stroke-linecap="round">')
print('  <g stroke="#5E5E5E" stroke-width="3" stroke-opacity="0.55">' + "".join(f'<path d="{d}"/>' for d in stubs) + "</g>")
print('  <g stroke="#6B6B6B" stroke-width="3" stroke-dasharray="7 9">' + "".join(f'<path d="{d}"/>' for d in dashed) + "</g>")
for a, b, d in paths:
    print(f'  <path class="s3-wire" id="s3-w-{a}-{b}" d="{d}" stroke="#6B6B6B" stroke-width="4"/>')
print("</svg>")
for a, b, d in paths:
    print(f'<div class="s3-pkt" id="s3-p-{b}"></div>')
for n in NODES:
    print(node_html(*n))
for h in sub_html:
    print(h)

import json, sys
meta = {n[0]: [round(v, 1) for v in W(*n[3])] for n in NODES}
meta["wires"] = [f"s3-w-{a}-{b}" for a, b, _ in paths]
print("<!-- META " + json.dumps(meta) + " -->")

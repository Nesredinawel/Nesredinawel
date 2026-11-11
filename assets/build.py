"""Generate light/dark SVG assets for the GitHub profile README."""
import math
from pathlib import Path

OUT = Path(__file__).parent
OUT.mkdir(parents=True, exist_ok=True)

SANS = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'SF Mono', ui-monospace, Menlo, Consolas, monospace"

THEMES = {
    "light": dict(fg="#0a0a0a", muted="#6b7280", faint="#a1a1aa", line="#e4e4e7",
                  card="#fafafa", dot="#d4d4d8", accent="#16a34a"),
    "dark": dict(fg="#f4f4f5", muted="#9ca3af", faint="#52525b", line="#27272a",
                 card="#111113", dot="#3f3f46", accent="#4ade80"),
}

W = 840


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" fill="none">{body}</svg>')


def text(x, y, s, size, color, family=SANS, weight=400, ls=0, anchor="start"):
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" letter-spacing="{ls}" fill="{color}" '
            f'text-anchor="{anchor}">{s}</text>')


# ---------- header ----------
def header(t):
    h = 300
    b = []
    # dot grid on the right, fading left
    for i in range(14):
        for j in range(9):
            x, y = 560 + i * 20, 40 + j * 22
            op = round(0.15 + 0.85 * (i / 13) ** 1.6, 2)
            b.append(f'<circle cx="{x}" cy="{y}" r="1.2" fill="{t["dot"]}" opacity="{op}"/>')
    # top row
    b.append(text(0, 22, "NESREDINAWEL", 11, t["faint"], MONO, 500, 2))
    b.append(f'<circle cx="{W-250}" cy="18" r="3.5" fill="{t["accent"]}">'
             f'<animate attributeName="opacity" values="1;0.25;1" dur="2.4s" repeatCount="indefinite"/></circle>')
    b.append(text(W, 22, "LEAD, CUSTOM SOFTWARE · PITRON", 11, t["muted"], MONO, 500, 1.2, "end"))
    # name
    b.append(text(-3, 150, "Nesredin Awel", 68, t["fg"], SANS, 600, -2.8))
    # tagline
    b.append(text(0, 192, "Designer and software engineer crafting calm, precise", 19, t["muted"], SANS, 400, -0.2))
    b.append(text(0, 218, "interfaces and the systems behind them.", 19, t["muted"], SANS, 400, -0.2))
    # rule + disciplines
    b.append(f'<line x1="0" y1="258" x2="{W}" y2="258" stroke="{t["line"]}"/>')
    tags = ["PRODUCT DESIGN", "INTERFACE ENGINEERING", "3D / WEBGL", "PLATFORM SYSTEMS"]
    x = 0
    for tg in tags:
        b.append(text(x, 286, tg, 11, t["faint"], MONO, 500, 1.6))
        x += len(tg) * 8.6 + 34
    return svg(W, h, "".join(b))


# ---------- section label ----------
def section(t, idx, title):
    h = 64
    b = [text(0, 40, idx, 11, t["faint"], MONO, 500, 1.6),
         text(36, 40, title, 15, t["fg"], SANS, 500, -0.2),
         f'<line x1="{40 + len(title) * 8.4 + 16}" y1="35.5" x2="{W}" y2="35.5" stroke="{t["line"]}"/>']
    return svg(W, h, "".join(b))


# ---------- card motifs ----------
def motif_globe(t, cx, cy):
    out = [f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 -2;0 0" dur="6s" repeatCount="indefinite"/>']
    r = 46
    for lat in range(-72, 90, 12):
        rr = r * math.cos(math.radians(lat))
        y = cy + r * math.sin(math.radians(lat))
        n = max(1, int(rr / 3.6))
        for k in range(n):
            a = 2 * math.pi * k / n
            x = cx + rr * math.cos(a)
            depth = (math.sin(a) + 1) / 2
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.1" fill="{t["fg"]}" opacity="{0.08 + 0.7 * depth:.2f}"/>')
    out.append("</g>")
    return "".join(out)


def motif_ring(t, cx, cy):
    out = [f'<g><animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="40s" repeatCount="indefinite"/>']
    for k in range(72):
        a = 2 * math.pi * k / 72
        for rr, op in ((44, 0.7), (36, 0.35), (28, 0.15)):
            if (k + int(rr)) % 2:
                continue
            out.append(f'<circle cx="{cx + rr * math.cos(a):.1f}" cy="{cy + rr * math.sin(a):.1f}" r="1.2" fill="{t["fg"]}" opacity="{op}"/>')
    out.append("</g>")
    return "".join(out)


def motif_capsule(t, cx, cy):
    return (f'<rect x="{cx-22}" y="{cy-46}" width="44" height="92" rx="22" stroke="{t["fg"]}" stroke-opacity="0.55"/>'
            f'<rect x="{cx-12}" y="{cy-36}" width="10" height="40" rx="5" fill="{t["fg"]}" opacity="0.08"/>'
            f'<line x1="{cx-22}" y1="{cy}" x2="{cx+22}" y2="{cy}" stroke="{t["fg"]}" stroke-opacity="0.25"/>'
            f'<path d="M{cx+40} {cy-14} l14 14 l-14 14 l-14 -14 z" stroke="{t["fg"]}" stroke-opacity="0.35"/>')


def motif_pay(t, cx, cy):
    return (f'<rect x="{cx-50}" y="{cy-32}" width="100" height="64" rx="9" stroke="{t["fg"]}" stroke-opacity="0.55"/>'
            f'<rect x="{cx-38}" y="{cy-18}" width="16" height="12" rx="2.5" stroke="{t["fg"]}" stroke-opacity="0.4"/>'
            f'<line x1="{cx-38}" y1="{cy+14}" x2="{cx+10}" y2="{cy+14}" stroke="{t["fg"]}" stroke-opacity="0.3" stroke-width="2" stroke-linecap="round"/>'
            f'<circle cx="{cx+36}" cy="{cy+14}" r="5" fill="{t["accent"]}"/>')


def card(t, idx, title, desc, tags, motif):
    w, h = 412, 216
    b = [f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="14" fill="{t["card"]}" stroke="{t["line"]}"/>',
         text(24, 38, idx, 11, t["faint"], MONO, 500, 1.6),
         motif(t, w - 96, 92),
         text(24, 146, title, 20, t["fg"], SANS, 600, -0.4),
         f'<path d="M{w-34} 38 l10 -10 m-7 0 h7 v7" stroke="{t["muted"]}" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>',
         text(24, 170, desc, 13.5, t["muted"], SANS, 400, -0.1),
         text(24, 198, "  ·  ".join(tags), 10.5, t["faint"], MONO, 500, 1.2)]
    return svg(w, h, "".join(b))


# ---------- stack ----------
def stack(t):
    items = ["Figma", "TypeScript", "React", "Next.js", "Three.js", "Tailwind", "NestJS", "PostgreSQL"]
    b, x, y = [], 0, 8
    for it in items:
        w = len(it) * 7.9 + 28
        if x + w > W:
            x, y = 0, y + 44
        b.append(f'<rect x="{x+0.5}" y="{y+0.5}" width="{w}" height="32" rx="16" stroke="{t["line"]}"/>')
        b.append(text(x + w / 2, y + 21, it, 13, t["fg"], SANS, 500, -0.1, "middle"))
        x += w + 10
    return svg(W, y + 44, "".join(b))


# ---------- footer ----------
def footer(t):
    b = [f'<line x1="0" y1="20" x2="{W}" y2="20" stroke="{t["line"]}"/>',
         text(0, 52, "Designing and building at Pitron Tech Solutions.", 13, t["muted"], SANS, 400, -0.1),
         text(W, 52, "© 2026", 11, t["faint"], MONO, 500, 1.4, "end")]
    return svg(W, 64, "".join(b))


CARDS = [
    ("01", "globe-app", "Dotted 3D globe hero for the web", ["NEXT.JS", "THREE.JS", "R3F"], motif_globe),
    ("02", "particle-ring", "Particle ring and glass cube scene", ["NEXT.JS", "THREE.JS", "R3F"], motif_ring),
    ("03", "glass-capsule", "Refractive glass capsule study", ["NEXT.JS", "THREE.JS", "R3F"], motif_capsule),
    ("04", "mereb_demo", "Payment gateway checkout interface", ["REACT", "RADIX", "MUI"], motif_pay),
]

for name, t in THEMES.items():
    (OUT / f"header-{name}.svg").write_text(header(t))
    (OUT / f"work-{name}.svg").write_text(section(t, "01", "Selected work"))
    (OUT / f"stack-{name}.svg").write_text(section(t, "02", "Toolkit"))
    (OUT / f"tools-{name}.svg").write_text(stack(t))
    (OUT / f"footer-{name}.svg").write_text(footer(t))
    for idx, title, desc, tags, m in CARDS:
        (OUT / f"card-{title}-{name}.svg").write_text(card(t, idx, title, desc, tags, m))

print(sorted(p.name for p in OUT.iterdir()))

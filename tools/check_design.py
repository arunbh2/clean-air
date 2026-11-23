"""Design guardrail checks for Clean Air (docs/design-guardrails.md explains every rule).

Run all:   python3 tools/check_design.py [--css site/static/css/site.css] [--dist site/dist]
One check: python3 tools/check_design.py stripes|cards|type|colours|contrast|budget
Self-test: python3 tools/check_design.py --self-test   (each check must FAIL on its bad fixture)

Mapping to the brief's suggested names (docs/three-audiences-governance-brief.md, section 3):
  tools/check-stripes.js  -> check_design.py stripes   no left accent stripes on containers; no gradients, glows, grain
  tools/check-cards.js    -> check_design.py cards     containers belong to one of four registered families, use radius
                                                       tokens, carry no shadow
  tools/check-type.js     -> check_design.py type      only the serif/sans families; no public text under 12px
  tools/check-colours.js  -> check_design.py colours   colour literals only as :root tokens (or in print CSS); tokens match
                                                       design-tokens.json; no green; AQI colours only under --aqi-*
  tools/check-contrast.js -> check_design.py contrast  WCAG ratios for every documented foreground/background pair
  (budget)                -> check_design.py budget    byte budgets for CSS, JS, HTML pages, Markdown mirrors, llms-full
The rendered-DOM checks (computed font sizes, axe colour contrast, overflow at 320px and 200% zoom) run in site/qa/qa.js.
"""
import glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TOK = json.load(open(os.path.join(HERE, "design-tokens.json")))


def parse_css(text):
    """Return list of (selector, declarations dict, media) with @media nesting flattened."""
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    out, i, media_stack = [], 0, []
    buf, depth = "", 0
    tokens = re.finditer(r"[{}]", text)
    start = 0; stack = []
    for m in tokens:
        if m.group() == "{":
            head = text[start:m.start()].strip()
            stack.append(head); start = m.end()
        else:
            head = stack.pop() if stack else ""
            body = text[start:m.start()]
            start = m.end()
            if head.startswith("@"):
                continue
            decls = {}
            for d in body.split(";"):
                if ":" in d:
                    k, v = d.split(":", 1); decls.setdefault(k.strip().lower(), []).append(v.strip())
            media = " ".join(h for h in stack if h.startswith("@"))
            for sel in head.split(","):
                out.append((sel.strip(), decls, media))
    return out


def css_files(css):
    return [css] if css else sorted(glob.glob(os.path.join(ROOT, "site", "static", "css", "*.css")))


def is_container(decls):
    bg = " ".join(decls.get("background", []) + decls.get("background-color", []))
    has_border = any(v and not v.startswith("0") and v != "none" for v in decls.get("border", []))
    return ("--ca-surface" in bg or "--ca-tint" in bg or "#fff" in bg.lower()) and has_border


def check_stripes(rules, errs):
    allowed = set(TOK["left_rule_allowed"])
    for sel, d, media in rules:
        if "print" in media: continue
        for k in ("border-left", "border-inline-start"):
            for v in d.get(k, []):
                if v and not v.startswith("0") and v != "none" and sel not in allowed:
                    errs.append(f"stripes: {sel} sets {k}:{v} (left accent stripes are reserved for {sorted(allowed)})")
        for v in d.get("box-shadow", []):
            if re.search(r"inset\s+\d+px\s+0", v):
                errs.append(f"stripes: {sel} draws a left stripe with box-shadow:{v}")
        for k, vs in d.items():
            for v in vs:
                if re.search(r"(linear|radial|conic)-gradient", v): errs.append(f"stripes: {sel} uses a decorative gradient ({k})")
                if k in ("filter", "backdrop-filter") and "blur" in v: errs.append(f"stripes: {sel} uses blur/glow ({k}:{v})")
                if k == "text-shadow" and v != "none": errs.append(f"stripes: {sel} uses text-shadow glow")
                if "noise" in v or "grain" in v: errs.append(f"stripes: {sel} references grain/noise texture")


def check_cards(rules, errs):
    fam = {s for v in TOK["container_families"].values() for s in v}
    fam |= {s for k, v in TOK.get("inline_components", {}).items() if not k.startswith("_") for s in v}
    radii = set(TOK["radius_tokens"])
    for sel, d, media in rules:
        if "print" in media: continue
        for v in d.get("box-shadow", []):
            if v != "none" and sel not in TOK["shadow_allowed"]:
                errs.append(f"cards: {sel} has box-shadow:{v} (shadows only for floating surfaces: {TOK['shadow_allowed']})")
        if is_container(d):
            base = re.sub(r":(hover|focus|focus-visible|focus-within|active)\b", "", sel)
            if base not in fam and not any(base.startswith(f + " ") or base.startswith(f + ".") or base.startswith(f + "[") for f in fam):
                errs.append(f"cards: {sel} is a bordered surface container but is not registered in a container family "
                            f"(card/note/row/panel) in tools/design-tokens.json")
        for v in d.get("border-radius", []):
            if v not in radii: errs.append(f"cards: {sel} uses border-radius:{v}; use {sorted(radii)}")


def to_px(v):
    v = v.strip()
    m = re.match(r"^max\((.*)\)$", v)
    if m: return max(to_px(x) for x in m.group(1).split(","))
    m = re.match(r"^clamp\(([^,]+),", v)
    if m: return to_px(m.group(1))
    m = re.match(r"^([\d.]+)(rem|px|em|pt)$", v)
    if not m: return None
    n, u = float(m.group(1)), m.group(2)
    return {"rem": n * TOK["root_px"], "px": n, "em": n * TOK["em_context_px"], "pt": n * 4 / 3}[u]


def check_type(rules, errs):
    fams = set(TOK["font_families_allowed"])
    for sel, d, media in rules:
        for v in d.get("font-family", []):
            if v not in fams and not (sel == ":root"):
                errs.append(f"type: {sel} sets font-family:{v}; allowed {sorted(fams)}")
        if "print" in media: continue
        for v in d.get("font-size", []):
            px = to_px(v)
            if px is not None and px < TOK["min_font_px"] - 0.01:
                errs.append(f"type: {sel} font-size:{v} is about {px:.1f}px, below {TOK['min_font_px']}px")
        for v in d.get("font", []):
            if v not in ("inherit",) and re.search(r"\d", v) and not v.startswith("inherit"):
                errs.append(f"type: {sel} uses font shorthand '{v}'; set family and size from tokens")


HEX = re.compile(r"#[0-9a-fA-F]{3,8}\b")
FUNC = re.compile(r"\b(rgb|rgba|hsl|hsla)\(")
GREENISH = re.compile(r"\b(green|lime|forestgreen|seagreen)\b", re.I)


def hex_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3: h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def is_green(h):
    r, g, b = hex_rgb(h); return g > 100 and g > r * 1.3 and g > b * 1.15


def check_colours(rules, errs, raw_text):
    root = {}
    for sel, d, media in rules:
        for k, vs in d.items():
            for v in vs:
                if sel == ":root" and k.startswith("--"):
                    root[k] = v
                    if HEX.search(v) and is_green(HEX.search(v).group()) and not k.startswith("--aqi-"):
                        errs.append(f"colours: token {k}:{v} is green; green may not signal proof or safety")
                    continue
                if "print" in media: continue
                if HEX.search(v) or FUNC.search(v):
                    errs.append(f"colours: {sel} {k}:{v} uses a literal colour; use a --ca-* token")
                if GREENISH.search(v): errs.append(f"colours: {sel} {k}:{v} uses a green keyword")
                if "--aqi-" in v and not re.search(r"aqi", sel):
                    errs.append(f"colours: {sel} uses an AQI colour outside an AQI legend")
    for k, v in TOK["colour_tokens"].items():
        if k not in root: errs.append(f"colours: token {k} missing from :root")
        elif root[k].upper() != v.upper(): errs.append(f"colours: token {k} is {root[k]} in CSS but {v} in design-tokens.json")
    for k in root:
        if k.startswith("--ca-") and HEX.search(root[k]) and k not in TOK["colour_tokens"]:
            errs.append(f"colours: CSS defines undocumented colour token {k}; add it to design-tokens.json with a role")


def lum(h):
    def ch(c):
        c = c / 255; return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = hex_rgb(h); return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def ratio(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True); return (la + 0.05) / (lb + 0.05)


def check_contrast(tok, errs, report=None):
    for p in tok["contrast_pairs"]:
        r = ratio(tok["colour_tokens"][p["fg"]], tok["colour_tokens"][p["bg"]])
        if report is not None: report.append(f"  {r:5.2f}:1  (min {p['min']})  {p['name']}")
        if r < p["min"]: errs.append(f"contrast: {p['name']} is {r:.2f}:1, below {p['min']}:1")


def check_budget(dist, errs, report=None):
    b = TOK["budgets_bytes"]
    def size(globpat): return sum(os.path.getsize(p) for p in glob.glob(os.path.join(dist, globpat), recursive=True))
    css, js = size("css/*.css"), size("js/*.js")
    if report is not None: report.append(f"  css {css} B (budget {b['css_total']}), js {js} B (budget {b['js_total']})")
    if css > b["css_total"]: errs.append(f"budget: CSS {css} B over {b['css_total']} B")
    if js > b["js_total"]: errs.append(f"budget: JS {js} B over {b['js_total']} B")
    big = []
    for p in glob.glob(os.path.join(dist, "**", "*.html"), recursive=True):
        rel = os.path.relpath(p, dist); n = os.path.getsize(p)
        lim = b["html_page_exceptions"].get(rel, b["html_page_default"])
        if n > lim: errs.append(f"budget: {rel} is {n} B, over {lim} B")
        big.append((n, rel))
    for p in glob.glob(os.path.join(dist, "**", "*.md"), recursive=True):
        rel = os.path.relpath(p, dist)
        if rel.startswith("downloads/"): continue
        n = os.path.getsize(p); lim = b["html_page_exceptions"].get(rel.replace(".md", ".html"), b["markdown_page_default"])
        if n > lim: errs.append(f"budget: {rel} is {n} B, over {lim} B")
    full = os.path.join(dist, "llms-full.txt")
    if os.path.exists(full) and os.path.getsize(full) > b["llms_full_txt"]:
        errs.append(f"budget: llms-full.txt is {os.path.getsize(full)} B, over {b['llms_full_txt']} B")
    if report is not None and big:
        big.sort(reverse=True); report.append("  largest pages: " + ", ".join(f"{r} {n // 1000} kB" for n, r in big[:5]))


def run(which, css=None, dist=None, tok=None, quiet=False):
    errs, rep = [], []
    text = "\n".join(open(f).read() for f in css_files(css))
    rules = parse_css(text)
    if "stripes" in which: check_stripes(rules, errs)
    if "cards" in which: check_cards(rules, errs)
    if "type" in which: check_type(rules, errs)
    if "colours" in which: check_colours(rules, errs, text)
    if "contrast" in which: check_contrast(tok or TOK, errs, rep)
    if "budget" in which and dist: check_budget(dist, errs, rep)
    if not quiet:
        for e in errs: print("ERROR", e)
        for r in rep: print(r)
    return errs


ALL = ["stripes", "cards", "type", "colours", "contrast", "budget"]


def self_test():
    fx = os.path.join(HERE, "fixtures", "design")
    bad_css = os.path.join(fx, "bad.css")
    fails = 0
    for check in ["stripes", "cards", "type", "colours"]:
        e = run([check], css=bad_css, quiet=True)
        print(f"design self-test {check}: bad fixture -> {len(e)} errors"); fails += (len(e) == 0)
    bad_tok = json.loads(json.dumps(TOK)); bad_tok["contrast_pairs"].append({"name": "fixture: light grey on white", "fg": "--ca-rule", "bg": "--ca-surface", "min": 4.5})
    e = run(["contrast"], tok=bad_tok, quiet=True); print(f"design self-test contrast: bad fixture -> {len(e)} errors"); fails += (len(e) == 0)
    e = run(["budget"], dist=os.path.join(fx, "bigdist"), quiet=True); print(f"design self-test budget: bad fixture -> {len(e)} errors"); fails += (len(e) == 0)
    return 1 if fails else 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--self-test" in args: sys.exit(self_test())
    css = args[args.index("--css") + 1] if "--css" in args else None
    dist = args[args.index("--dist") + 1] if "--dist" in args else os.path.join(ROOT, "site", "dist")
    which = [a for a in args if a in ALL] or ALL
    errs = run(which, css=css, dist=dist)
    print(f"design ({', '.join(which)}): {len(errs)} errors")
    sys.exit(1 if errs else 0)

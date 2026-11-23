"""Turn a generated Clean Air HTML page into its Markdown mirror.

The mirror is produced from the *rendered* <main> element of the same page, so the wording, caveats,
citations, tables and links cannot drift from what a human reader sees. Interactive controls (filter
forms, buttons) are dropped because they do nothing in plain text; their static results (the full lists)
are kept. Relative links become absolute, base-aware URLs so an agent can follow them.
"""
import posixpath, re
from bs4 import BeautifulSoup, NavigableString, Tag

DROP = {"script", "style", "form", "button", "noscript", "svg", "template", "input", "select", "label"}
BLOCK = {"p", "ul", "ol", "table", "h1", "h2", "h3", "h4", "h5", "h6", "details", "section", "div", "dl", "blockquote", "nav", "figure", "article", "header", "aside"}


def absolute(href, page_path, base):
    if not href or href.startswith(("http://", "https://", "mailto:")): return href
    if href.startswith("#"): return base + page_path + href
    path, _, frag = href.partition("#")
    joined = posixpath.normpath(posixpath.join(posixpath.dirname(page_path), path))
    return base + joined + ("#" + frag if frag else "")


def esc(t):
    return re.sub(r"([\\`*_])", r"\\\1", t)


class Conv:
    def __init__(self, page_path, base):
        self.page, self.base = page_path, base

    def inline(self, node):
        if isinstance(node, NavigableString):
            return esc(re.sub(r"\s+", " ", str(node)))
        if not isinstance(node, Tag) or node.name in DROP: return ""
        if node.get("aria-hidden") == "true" or node.has_attr("hidden"): return ""
        inner = "".join(self.inline(c) for c in node.children)
        n = node.name
        if n == "a":
            href = absolute(node.get("href", ""), self.page, self.base)
            txt = inner.strip() or href
            return f"[{txt}]({href})" if href else txt
        if n in ("strong", "b"): return f"**{inner.strip()}**" if inner.strip() else ""
        if n == "cite": return f"_{inner.strip()}_" if inner.strip() else ""   # underscore = external title (voice check skips it)
        if n in ("em", "i"): return f"*{inner.strip()}*" if inner.strip() else ""
        if n == "code": return f"`{node.get_text()}`"
        if n == "br": return "  \n"
        if n == "img": return node.get("alt", "")
        if n in BLOCK or n in ("li", "tr", "td", "th"): return " " + inner + " "
        return inner

    def text(self, node):
        return re.sub(r"[ \t]+", " ", self.inline(node)).strip()

    def table(self, t):
        rows = []
        cap = t.find("caption")
        out = []
        if cap and cap.get_text(strip=True): out.append(f"*{self.text(cap)}*\n")
        for tr in t.find_all("tr"):
            if tr.has_attr("hidden"): continue
            cells = [self.text(c).replace("|", "\\|").replace("\n", " ") or " " for c in tr.find_all(["th", "td"]) if not c.has_attr("hidden")]
            if cells: rows.append(cells)
        if not rows: return ""
        width = max(len(r) for r in rows)
        rows = [r + [" "] * (width - len(r)) for r in rows]
        out.append("| " + " | ".join(rows[0]) + " |")
        out.append("|" + "---|" * width)
        out += ["| " + " | ".join(r) + " |" for r in rows[1:]]
        return "\n".join(out)

    def lst(self, node, depth=0):
        out, i = [], 1
        for li in node.find_all("li", recursive=False):
            if li.has_attr("hidden"): continue
            bullet = f"{i}." if node.name == "ol" else "-"
            parts, subs = [], []
            for c in li.children:
                if isinstance(c, Tag) and c.name in ("ul", "ol"): subs.append(self.lst(c, depth + 1))
                elif isinstance(c, Tag) and c.name in ("p", "div", "h3", "h4"): parts.append(" " + self.text(c) + " ")
                else: parts.append(self.inline(c))
            line = re.sub(r"\s+", " ", "".join(parts)).strip()
            if line or subs:
                out.append("  " * depth + f"{bullet} {line}")
                out += [s for s in subs if s]
            i += 1
        return "\n".join(out)

    def blocks(self, node):
        out = []
        for c in node.children:
            if isinstance(c, NavigableString):
                t = esc(str(c)).strip()
                if t: out.append(t)
                continue
            if not isinstance(c, Tag) or c.name in DROP: continue
            if c.get("aria-hidden") == "true" or c.has_attr("hidden"): continue
            n = c.name
            if re.fullmatch(r"h[1-6]", n):
                out.append("#" * int(n[1]) + " " + self.text(c))
            elif n == "p":
                t = self.text(c)
                if t: out.append(t)
            elif n in ("ul", "ol"):
                t = self.lst(c)
                if t: out.append(t)
            elif n == "table":
                t = self.table(c)
                if t: out.append(t)
            elif n == "details":
                s = c.find("summary")
                if s: out.append(f"**{self.text(s)}**"); s.extract()
                out += self.blocks(c)
            elif n == "dl":
                for el in c.find_all(["dt", "dd"]):
                    out.append(f"**{self.text(el)}**" if el.name == "dt" else self.text(el))
            elif n == "blockquote":
                out.append("\n".join("> " + l for l in self.text(c).splitlines()))
            elif n in ("div", "section", "article", "nav", "header", "aside", "figure", "main", "dd", "summary", "figcaption", "span"):
                inner = self.blocks(c)
                if any(isinstance(x, Tag) and x.name in BLOCK for x in c.children): out += inner
                else:
                    t = self.text(c)
                    if t: out.append(t)
            elif n == "hr": out.append("---")
            else:
                t = self.text(c)
                if t: out.append(t)
        return out


def html_to_markdown(html_text, page_path, base, meta):
    """meta: dict with title, description, html_url, cutoff, built. Returns Markdown string."""
    soup = BeautifulSoup(html_text, "html.parser")
    main = soup.find("main") or soup.body
    for crumbs in main.select("p.crumbs"): crumbs.decompose()
    body = "\n\n".join(b for b in Conv(page_path, base).blocks(main) if b.strip())
    body = re.sub(r"\n{3,}", "\n\n", body)
    head = ["---", f"title: \"{meta['title']}\"", f"canonical_html: {meta['html_url']}", f"research_cutoff: {meta['cutoff']}",
            f"generated: {meta['built']}", "generated_from: the same research records as the HTML page (research/ in the repository)",
            "---", ""]
    if not re.search(r"^# ", body, re.M):
        head.append(f"# {meta['title']}\n")
    foot = ["", "---", f"Markdown mirror of {meta['html_url']}. Research cutoff: {meta['cutoff']}. "
            "Inclusion of an organisation does not imply endorsement. Not medical or investment advice. "
            f"Corrections: {base}about/corrections.html"]
    return "\n".join(head) + body + "\n" + "\n".join(foot) + "\n"

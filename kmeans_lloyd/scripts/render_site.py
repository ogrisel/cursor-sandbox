"""Render the experiment journal as a small static site."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JOURNAL = ROOT / "journal"
SITE = ROOT / "site"

CSS = """
:root { color-scheme: light; --ink: #1c1915; --muted: #5c564c; --line: #e4ddd0; --paper: #faf7f2; --accent: #8c3a2f; }
body { margin: 0; font: 18px/1.55 "Iowan Old Style", Palatino, Georgia, serif; color: var(--ink); background: var(--paper); }
header, main { max-width: 920px; margin: 0 auto; padding: 1.25rem 1.25rem 2.5rem; }
header { border-bottom: 1px solid var(--line); }
a { color: var(--accent); }
nav a { margin-right: 1rem; }
h1, h2, h3 { line-height: 1.2; }
table { border-collapse: collapse; width: 100%; font-size: 0.92rem; display: block; overflow-x: auto; }
th, td { border-bottom: 1px solid var(--line); text-align: left; padding: 0.35rem 0.5rem; vertical-align: top; }
code { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 0.86em; }
pre { overflow-x: auto; padding: 0.8rem 1rem; background: #fff; border: 1px solid var(--line); }
img { max-width: 100%; height: auto; }
.meta { color: var(--muted); }
"""


def _href(url):
    if url.endswith("report.md"):
        url = url[: -len("report.md")] + "index.html"
    elif url.endswith("index.md"):
        url = url[: -len("index.md")] + "index.html"
    return url


def _inline(text):
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", lambda match: f"<code>{match.group(1)}</code>", escaped)

    def link(match):
        label = match.group(1)
        href = _href(html.unescape(match.group(2)))
        return f'<a href="{html.escape(href, quote=True)}">{label}</a>'

    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, escaped)
    return escaped


def _slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def markdown_to_html(source):
    lines = source.splitlines()
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            block = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                block.append(html.escape(lines[i]))
                i += 1
            out.append("<pre><code>" + "\n".join(block) + "</code></pre>")
            i += 1
            continue
        if line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|\s*-+", lines[i + 1]):
            headers = [cell.strip() for cell in line.strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([cell.strip() for cell in lines[i].strip("|").split("|")])
                i += 1
            head = "".join(f"<th>{_inline(cell)}</th>" for cell in headers)
            body = "".join(
                "<tr>" + "".join(f"<td>{_inline(cell)}</td>" for cell in row) + "</tr>" for row in rows
            )
            out.append(f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>")
            continue
        if line.startswith("### "):
            title = line[4:]
            out.append(f'<h3 id="{_slug(title)}">{_inline(title)}</h3>')
        elif line.startswith("## "):
            title = line[3:]
            out.append(f'<h2 id="{_slug(title)}">{_inline(title)}</h2>')
        elif line.startswith("# "):
            title = line[2:]
            out.append(f'<h1 id="{_slug(title)}">{_inline(title)}</h1>')
        elif line.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append(f"<li>{_inline(lines[i][2:])}</li>")
                i += 1
            out.append("<ul>" + "".join(items) + "</ul>")
            continue
        elif line.startswith("!["):
            match = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", line.strip())
            if match:
                alt, src = match.groups()
                out.append(f'<img alt="{html.escape(alt)}" src="{html.escape(src, quote=True)}" />')
            else:
                out.append(f"<p>{_inline(line)}</p>")
        elif not line.strip():
            pass
        else:
            paragraph = [line]
            i += 1
            while i < len(lines) and lines[i].strip() and not lines[i].startswith(("#", "-", "|", "!", "```")):
                paragraph.append(lines[i])
                i += 1
            out.append(f"<p>{_inline(' '.join(paragraph))}</p>")
            continue
        i += 1
    return "\n".join(out)


def _page(title, body, depth):
    prefix = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="{prefix}style.css" />
</head>
<body>
<header>
<nav>
<a href="{prefix}index.html">Journal</a>
<a href="{prefix}index.html#cases">Cases</a>
</nav>
</header>
<main>
{body}
</main>
</body>
</html>
"""


def render():
    if SITE.exists():
        for path in SITE.rglob("*"):
            if path.is_file():
                path.unlink()
    SITE.mkdir(parents=True, exist_ok=True)
    (SITE / "style.css").write_text(CSS)
    entries = []
    if JOURNAL.exists():
        for report in sorted(JOURNAL.glob("*/report.md")):
            entries.append(report)
    index_md = JOURNAL / "index.md"
    index_body = markdown_to_html(index_md.read_text()) if index_md.exists() else "<p>No journal yet.</p>"
    (SITE / "index.html").write_text(_page("Lloyd k-means fusion journal", index_body, 0))
    for report in entries:
        folder = SITE / report.parent.name
        folder.mkdir(parents=True, exist_ok=True)
        # Rewrite relative image links so they still resolve next to the HTML copy,
        # and copy sibling assets (svg, png, json).
        for asset in report.parent.iterdir():
            if asset.suffix.lower() in {".svg", ".png", ".json", ".md"} and asset.name != "report.md":
                target = folder / asset.name
                target.write_bytes(asset.read_bytes())
        body = markdown_to_html(report.read_text())
        (folder / "index.html").write_text(_page(report.parent.name, body, 1))
    print(f"rendered {SITE}")


def main():
    parser = argparse.ArgumentParser()
    parser.parse_args()
    render()


if __name__ == "__main__":
    main()

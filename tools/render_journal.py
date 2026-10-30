"""Render a chronological experiment journal as a small static site.

Markdown is converted with pandoc using GitHub-flavored Markdown and MathML.
Relative links whose path ends in ``report.md`` or ``index.md`` are rewritten
to ``index.html`` (query strings and fragments are kept).

The journal layout is:

    journal/index.md
    journal/<iteration>/report.md
    journal/<iteration>/*.{svg,png,json,...}
"""

from __future__ import annotations

import argparse
import html
import re
import shutil
import subprocess
from pathlib import Path

ASSET_SUFFIXES = {".svg", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".json", ".md"}

# Bound a single page so a pathological document cannot hang the publisher.
PANDOC_TIMEOUT_SECONDS = 60

CSS = """
:root { color-scheme: light; --ink: #1c1915; --muted: #5c564c; --line: #e4ddd0; --paper: #faf7f2; --accent: #8c3a2f; }
body { margin: 0; font: 18px/1.55 "Iowan Old Style", Palatino, Georgia, serif; color: var(--ink); background: var(--paper); }
header, main { max-width: 920px; margin: 0 auto; padding: 1.25rem 1.25rem 2.5rem; }
header { border-bottom: 1px solid var(--line); }
a { color: var(--accent); }
nav a { margin-right: 1rem; }
h1, h2, h3, h4, h5, h6 { line-height: 1.2; }
p, ul, ol, blockquote, pre, div.sourceCode, table, hr, .footnotes { margin: 1rem 0; }
ul, ol { padding-left: 1.3rem; }
li { margin: 0.15rem 0; }
li > ul, li > ol { margin: 0.15rem 0; }
ul.task-list { list-style: none; padding-left: 0.2rem; }
ul.task-list input { margin-right: 0.4rem; }
blockquote { padding: 0.2rem 1rem; border-left: 3px solid var(--accent); color: var(--muted); }
table { border-collapse: collapse; width: 100%; font-size: 0.92rem; display: block; overflow-x: auto; }
th, td { border-bottom: 1px solid var(--line); text-align: left; padding: 0.35rem 0.5rem; vertical-align: top; }
tbody tr.even { background: #f3eee4; }
code { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 0.86em; }
:not(pre) > code { background: #fff; border: 1px solid var(--line); padding: 0.05em 0.3em; border-radius: 0.2rem; }
pre { overflow-x: auto; padding: 0.8rem 1rem; background: #fff; border: 1px solid var(--line); }
div.sourceCode { overflow-x: auto; background: #fff; border: 1px solid var(--line); }
div.sourceCode pre { margin: 0; border: 0; background: transparent; }
div.sourceCode a { color: inherit; text-decoration: none; }
hr { border: 0; border-top: 1px solid var(--line); }
img { max-width: 100%; height: auto; }
figure { margin: 1rem 0; }
figcaption { color: var(--muted); font-size: 0.9rem; }
math[display="block"] { display: block; overflow-x: auto; margin: 1rem 0; }
sup { line-height: 0; }
.footnotes { color: var(--muted); font-size: 0.92rem; }
.footnote-back { text-decoration: none; }
.meta { color: var(--muted); }
dt { font-weight: 600; }
dd { margin: 0 0 0.6rem; }
del { color: var(--muted); }
code span.al { color: #ff0000; font-weight: bold; }
code span.an { color: #60a0b0; font-weight: bold; font-style: italic; }
code span.at { color: #7d9029; }
code span.bn { color: #40a070; }
code span.bu { color: #008000; }
code span.cf { color: #007020; font-weight: bold; }
code span.ch { color: #4070a0; }
code span.cn { color: #880000; }
code span.co { color: #60a0b0; font-style: italic; }
code span.cv { color: #60a0b0; font-weight: bold; font-style: italic; }
code span.do { color: #ba2121; font-style: italic; }
code span.dt { color: #902000; }
code span.dv { color: #40a070; }
code span.er { color: #ff0000; font-weight: bold; }
code span.fl { color: #40a070; }
code span.fu { color: #06287e; }
code span.im { color: #008000; font-weight: bold; }
code span.in { color: #60a0b0; font-weight: bold; font-style: italic; }
code span.kw { color: #007020; font-weight: bold; }
code span.op { color: #666666; }
code span.ot { color: #007020; }
code span.pp { color: #bc7a00; }
code span.sc { color: #4070a0; }
code span.ss { color: #bb6688; }
code span.st { color: #4070a0; }
code span.va { color: #19177c; }
code span.vs { color: #4070a0; }
code span.wa { color: #60a0b0; font-weight: bold; font-style: italic; }
"""

_HREF = re.compile(
    r"""(?<![A-Za-z0-9_:-])(?P<attr>href)=(?P<quote>["'])(?P<url>.*?)(?P=quote)""",
    re.IGNORECASE | re.DOTALL,
)
_SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
_JOURNAL_PAGES = ("report.md", "index.md")


class RenderError(RuntimeError):
    """The journal could not be rendered."""


def _rewrite_href(url: str) -> str:
    """Rewrite a relative journal link to the generated HTML page."""
    if _SCHEME.match(url) or url.startswith("//"):
        return url
    split_at = len(url)
    for marker in ("?", "#"):
        index = url.find(marker)
        if index != -1:
            split_at = min(split_at, index)
    path, suffix = url[:split_at], url[split_at:]
    for name in _JOURNAL_PAGES:
        if path.endswith(name):
            path = path[: -len(name)] + "index.html"
            break
    return path + suffix


def _rewrite_markdown_hrefs(fragment: str) -> str:
    def replace(match: re.Match[str]) -> str:
        quote = match.group("quote")
        url = _rewrite_href(match.group("url"))
        return f"{match.group('attr')}={quote}{url}{quote}"

    return _HREF.sub(replace, fragment)


def markdown_to_html(source: str) -> str:
    """Convert Markdown to an HTML fragment with pandoc."""
    pandoc = shutil.which("pandoc")
    if pandoc is None:
        raise RenderError(
            "pandoc was not found on PATH. Install pandoc to render the journal."
        )
    command = [
        pandoc,
        "--from=gfm+tex_math_dollars",
        "--to=html",
        "--mathml",
        "--wrap=none",
        "--highlight-style=pygments",
    ]
    try:
        result = subprocess.run(
            command,
            input=source,
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
            timeout=PANDOC_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as exc:
        raise RenderError("pandoc timed out while rendering markdown") from exc
    if result.returncode != 0:
        detail = result.stderr.strip() or f"exit code {result.returncode}"
        raise RenderError(f"pandoc failed: {detail}")
    return _rewrite_markdown_hrefs(result.stdout)


def _page(title, body, depth, cases):
    prefix = "../" * depth
    cases_link = f'<a href="{prefix}index.html#cases">Cases</a>' if cases else ""
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
{cases_link}
</nav>
</header>
<main>
{body}
</main>
</body>
</html>
"""


def render(journal: Path, site: Path, title: str) -> None:
    """Write ``site`` from the markdown journal in ``journal``."""
    journal = Path(journal)
    site = Path(site)
    if site.exists():
        shutil.rmtree(site)
    site.mkdir(parents=True)
    (site / "style.css").write_text(CSS)
    index_md = journal / "index.md"
    index_source = index_md.read_text() if index_md.exists() else ""
    index_body = markdown_to_html(index_source) if index_source else "<p>No journal yet.</p>"
    cases = 'id="cases"' in index_body
    (site / "index.html").write_text(_page(title, index_body, 0, cases))
    if not journal.exists():
        print(f"rendered {site}")
        return
    for report in sorted(journal.glob("*/report.md")):
        folder = site / report.parent.name
        folder.mkdir(parents=True, exist_ok=True)
        for asset in report.parent.iterdir():
            if asset.suffix.lower() in ASSET_SUFFIXES and asset.name != "report.md":
                shutil.copyfile(asset, folder / asset.name)
        body = markdown_to_html(report.read_text())
        (folder / "index.html").write_text(_page(report.parent.name, body, 1, cases))
    print(f"rendered {site}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--journal", type=Path, required=True)
    parser.add_argument("--site", type=Path, required=True)
    parser.add_argument("--title", default="Experiment journal")
    args = parser.parse_args()
    try:
        render(args.journal, args.site, args.title)
    except RenderError as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()

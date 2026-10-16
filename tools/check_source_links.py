"""Check GitHub source links in journal markdown against the git history.

A link with a line anchor must name a full commit SHA: branch names move and
their line numbers drift. The pinned file must exist at that commit. For a
Python file, a link whose text is a backticked identifier must cover exactly
that function or class; any other line-anchored link must start at a
definition.

Usage: python tools/check_source_links.py --repo owner/name journal [...]
"""

from __future__ import annotations

import argparse
import ast
import re
import subprocess
import sys
from pathlib import Path

SHA = re.compile(r"[0-9a-f]{40}")


def _link_pattern(repo):
    return re.compile(
        r"\[([^\]]+)\]\(https://github\.com/" + re.escape(repo)
        + r"/blob/([^/]+)/([^#)\s]+)(?:#L(\d+)(?:-L(\d+))?)?\)"
    )


def _definitions(source):
    ranges = {}
    starts = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            start = min([node.lineno] + [d.lineno for d in node.decorator_list])
            ranges.setdefault(node.name, (start, node.end_lineno))
            starts.add(start)
    return ranges, starts


def check(paths, repo, git_dir="."):
    pattern = _link_pattern(repo)
    problems = []
    checked = 0
    for root in paths:
        files = [Path(root)] if Path(root).is_file() else sorted(Path(root).rglob("*.md"))
        for markdown in files:
            for match in pattern.finditer(markdown.read_text()):
                text, ref, path, first, last = match.groups()
                checked += 1
                where = f"{markdown}: [{text}]"
                if not SHA.fullmatch(ref):
                    # Branch names may contain slashes, so the path cannot be
                    # resolved reliably; only line anchors are worth failing on.
                    if first:
                        problems.append(f"{where} anchors lines on a branch, not a commit SHA")
                    continue
                shown = subprocess.run(
                    ["git", "-C", str(git_dir), "show", f"{ref}:{path}"],
                    capture_output=True,
                    text=True,
                )
                if shown.returncode:
                    problems.append(f"{where} {path} does not exist at {ref}")
                    continue
                if not first:
                    continue
                first, last = int(first), int(last or first)
                n_lines = len(shown.stdout.splitlines())
                if last > n_lines or first > last:
                    problems.append(f"{where} L{first}-L{last} is outside 1..{n_lines}")
                    continue
                if not path.endswith(".py"):
                    continue
                ranges, starts = _definitions(shown.stdout)
                name = text.strip("`")
                if text.startswith("`") and re.fullmatch(r"\w+", name):
                    expected = ranges.get(name)
                    if expected != (first, last):
                        problems.append(
                            f"{where} L{first}-L{last} does not match {name} at {expected}"
                        )
                elif first not in starts:
                    problems.append(f"{where} L{first} is not the start of a definition")
    return checked, problems


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, help="GitHub owner/name")
    parser.add_argument("paths", nargs="+")
    args = parser.parse_args()
    checked, problems = check(args.paths, args.repo)
    for problem in problems:
        print(problem)
    print(f"checked {checked} source links, {len(problems)} problems")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()

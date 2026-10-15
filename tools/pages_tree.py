"""Keep one GitHub Pages directory per pull request.

``actions/deploy-pages`` replaces the whole site. This module copies a newly
rendered journal into ``pr-<number>/`` and keeps the directories of other
pull requests, either from the ``report-site`` branch or from the live site.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path


class _Refs(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {"a", "link"} and attrs.get("href"):
            self.refs.append(attrs["href"])
        elif tag in {"img", "script"} and attrs.get("src"):
            self.refs.append(attrs["src"])


def path_under(base_url, page_url, ref):
    """Return ``ref`` resolved under ``base_url``, or None when it leaves the site."""
    if not ref or ref.startswith(("#", "mailto:", "javascript:")):
        return None
    base = base_url if base_url.endswith("/") else base_url + "/"
    absolute = urllib.request.urljoin(page_url, ref)
    absolute = absolute.split("#", 1)[0].split("?", 1)[0]
    if not absolute.startswith(base):
        return None
    return absolute[len(base) :]


def stage(site: Path, pages: Path, pr_number: int) -> Path:
    """Copy ``site`` to ``pages/pr-<pr_number>``, replacing that directory only."""
    if pr_number < 1:
        raise ValueError(f"pull request number must be positive, got {pr_number}")
    destination = Path(pages) / f"pr-{pr_number}"
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(site, destination)
    return destination


def copy_seed(seed: Path, pages: Path) -> None:
    """Copy previously published ``pr-*`` directories from ``seed``."""
    pages.mkdir(parents=True, exist_ok=True)
    if not seed.exists():
        return
    for child in seed.iterdir():
        if child.name.startswith("pr-") and child.is_dir():
            target = pages / child.name
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(child, target)


def _request(url, token=None):
    headers = {"User-Agent": "cursor-sandbox-report"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read(), response.headers.get_content_type()


def pull_request_numbers(repository, token=None):
    owner, repo = repository.split("/", 1)
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls?state=all&per_page=100"
    payload, _ = _request(url, token)
    return [int(item["number"]) for item in json.loads(payload)]


def download_prefix(base_url, prefix, destination, token=None, max_files=500):
    """Download the pages under ``base_url + prefix`` into ``destination``."""
    base = base_url if base_url.endswith("/") else base_url + "/"
    start = prefix if prefix.endswith("/") else prefix + "/"
    queue = [urllib.request.urljoin(base, start)]
    seen = set()
    saved = 0
    while queue and saved < max_files:
        url = queue.pop()
        relative = path_under(base, base, url)
        if url in seen or relative is None or not relative.startswith(start):
            continue
        seen.add(url)
        try:
            body, content_type = _request(url, token)
        except urllib.error.HTTPError:
            continue
        if relative.endswith("/"):
            relative += "index.html"
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(body)
        saved += 1
        if "html" in content_type:
            parser = _Refs()
            parser.feed(body.decode("utf-8", errors="replace"))
            for ref in parser.refs:
                child = path_under(base, url, ref)
                if child and child.startswith(start):
                    queue.append(urllib.request.urljoin(base, child))
    return saved


def recover_live(pages: Path, repository: str, base_url: str, token=None) -> int:
    """Copy live ``pr-*`` directories that still respond into ``pages``."""
    pages.mkdir(parents=True, exist_ok=True)
    saved = 0
    for number in pull_request_numbers(repository, token):
        prefix = f"pr-{number}/"
        try:
            _request(urllib.request.urljoin(base_url, prefix), token)
        except urllib.error.HTTPError:
            continue
        saved += download_prefix(base_url, prefix, pages, token)
    return saved


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    stage_parser = subparsers.add_parser("stage")
    stage_parser.add_argument("--site", type=Path, required=True)
    stage_parser.add_argument("--pages", type=Path, required=True)
    stage_parser.add_argument("--pr", type=int, required=True)

    seed_parser = subparsers.add_parser("seed")
    seed_parser.add_argument("--seed", type=Path, required=True)
    seed_parser.add_argument("--pages", type=Path, required=True)

    recover_parser = subparsers.add_parser("recover-live")
    recover_parser.add_argument("--pages", type=Path, required=True)
    recover_parser.add_argument("--repository", default=os.environ.get("GITHUB_REPOSITORY", ""))
    recover_parser.add_argument("--base-url", required=True)
    args = parser.parse_args()
    if args.command == "stage":
        print(stage(args.site, args.pages, args.pr))
    elif args.command == "seed":
        copy_seed(args.seed, args.pages)
        print(args.pages)
    else:
        if not args.repository:
            raise SystemExit("repository is required")
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        print(recover_live(args.pages, args.repository, args.base_url, token))


if __name__ == "__main__":
    main()

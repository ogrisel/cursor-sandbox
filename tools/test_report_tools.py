"""Tests for the shared journal renderer and Pages tree."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pages_tree
import render_journal


class RenderJournalTest(unittest.TestCase):
    def test_journal_links_assets_and_heading_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            journal = root / "journal"
            iteration = journal / "001-first"
            iteration.mkdir(parents=True)
            (journal / "index.md").write_text(
                "# Trial\n\n## Cases\n\n- [first](001-first/report.md)\n"
            )
            (iteration / "report.md").write_text(
                "# First\n\n| a | b |\n| --- | --- |\n| 1 | `two` |\n\n![plot](plot.svg)\n\nPrevious: [journal](../index.md).\n"
            )
            (iteration / "plot.svg").write_text("<svg></svg>")
            site = root / "site"
            render_journal.render(journal, site, "Trial journal")
            index = (site / "index.html").read_text()
            report = (site / "001-first" / "index.html").read_text()
            self.assertIn('id="cases"', index)
            self.assertIn('href="001-first/index.html"', index)
            self.assertIn('href="../index.html#cases"', report)
            self.assertIn("<code>two</code>", report)
            self.assertIn('src="plot.svg"', report)
            self.assertTrue((site / "001-first" / "plot.svg").is_file())
            self.assertIn("<title>Trial journal</title>", index)


class PagesTreeTest(unittest.TestCase):
    def test_stage_replaces_one_pull_request_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            site = root / "site"
            site.mkdir()
            (site / "index.html").write_text("new")
            pages = root / "pages"
            (pages / "pr-3").mkdir(parents=True)
            (pages / "pr-3" / "index.html").write_text("old")
            (pages / "pr-9").mkdir()
            (pages / "pr-9" / "index.html").write_text("keep")
            pages_tree.stage(site, pages, 3)
            self.assertEqual((pages / "pr-3" / "index.html").read_text(), "new")
            self.assertEqual((pages / "pr-9" / "index.html").read_text(), "keep")

    def test_seed_copies_only_pr_directories(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            seed = root / "seed"
            (seed / "pr-2").mkdir(parents=True)
            (seed / "pr-2" / "index.html").write_text("two")
            (seed / "README.md").write_text("ignore")
            pages = root / "pages"
            pages_tree.copy_seed(seed, pages)
            self.assertTrue((pages / "pr-2" / "index.html").is_file())
            self.assertFalse((pages / "README.md").exists())

    def test_save_step_passes_github_token(self):
        workflow = (
            Path(__file__).resolve().parents[1] / ".github" / "workflows" / "publish-report.yml"
        )
        step = workflow.read_text().split("name: Save the published tree", 1)[1]
        self.assertIn("GITHUB_TOKEN: ${{ github.token }}", step)
        self.assertIn("${GITHUB_TOKEN}", step)

    def test_relative_link_stays_inside_the_pull_request_prefix(self):
        page = "https://example.github.io/repo/pr-4/index.html"
        base = "https://example.github.io/repo/"
        self.assertEqual(pages_tree.path_under(base, page, "001/plot.svg"), "pr-4/001/plot.svg")
        self.assertIsNone(pages_tree.path_under(base, page, "https://example.com/elsewhere"))


if __name__ == "__main__":
    unittest.main()

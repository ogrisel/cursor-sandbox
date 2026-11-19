"""Tests for the shared journal renderer and Pages tree."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

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
            self.assertNotIn("report.md", index)
            self.assertNotIn("index.md", report)
            self.assertTrue((site / "001-first" / "plot.svg").is_file())
            self.assertIn("<title>Trial journal</title>", index)

    def test_pandoc_renders_markdown_the_hand_parser_missed(self):
        source = "\n".join(
            [
                "# Result",
                "",
                "A **bold** claim and a *term*.",
                "",
                "> quoted",
                "",
                "~~drop~~",
                "",
                "See [part](001-first/report.md#score) and [web](https://example.com/index.md).",
                "",
                '<a HREF="001-first/report.md?raw=1">raw</a>',
                "",
                "Inline $x^2$.",
                "",
                "- [x] checked item",
                "",
                "A note.[^n]",
                "",
                "[^n]: Foot text.",
                "",
                "```python",
                "# Not a heading",
                "| a | b |",
                'href="keep/report.md"',
                "```",
                "",
                "- outer",
                "  - inner",
                "",
                "| name | value |",
                "| --- | ---: |",
                "| **n** | 1 |",
                "",
            ]
        )
        body = render_journal.markdown_to_html(source)
        self.assertIn("<strong>bold</strong>", body)
        self.assertIn("<em>term</em>", body)
        self.assertIn("<blockquote>", body)
        self.assertIn("<del>drop</del>", body)
        self.assertIn('href="001-first/index.html#score"', body)
        self.assertIn('href="https://example.com/index.md"', body)
        self.assertIn('HREF="001-first/index.html?raw=1"', body)
        self.assertIn("<math", body)
        self.assertIn('type="checkbox"', body)
        self.assertIn("Foot text.", body)
        self.assertIn("keep/report.md", body)
        self.assertNotIn('href="keep/report.md"', body)
        self.assertEqual(body.count("<h1"), 1)
        self.assertEqual(body.count("<table>"), 1)
        self.assertRegex(body, r"outer\s*<ul>\s*<li>inner</li>")
        self.assertIn("<strong>n</strong>", body)
        self.assertIn("text-align: right", body)
        self.assertIn("code span.kw", render_journal.CSS)

    def test_relative_journal_links_keep_query_and_fragment(self):
        fragment = '<a href="dir/report.md?raw=1#s">x</a> <a href="//cdn.example/report.md">y</a>'
        rewritten = render_journal._rewrite_markdown_hrefs(fragment)
        self.assertIn('href="dir/index.html?raw=1#s"', rewritten)
        self.assertIn('href="//cdn.example/report.md"', rewritten)

    def test_missing_pandoc_explains_how_to_fix(self):
        with mock.patch.object(render_journal.shutil, "which", return_value=None):
            with self.assertRaises(render_journal.RenderError) as caught:
                render_journal.markdown_to_html("# Hi")
        self.assertIn("pandoc", str(caught.exception))

    def test_pandoc_error_is_reported(self):
        completed = subprocess.CompletedProcess(
            args=["pandoc"], returncode=64, stdout="", stderr="unknown extension"
        )
        with (
            mock.patch.object(render_journal.shutil, "which", return_value="pandoc"),
            mock.patch.object(render_journal.subprocess, "run", return_value=completed),
        ):
            with self.assertRaises(render_journal.RenderError) as caught:
                render_journal.markdown_to_html("# Hi")
        self.assertIn("unknown extension", str(caught.exception))


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

    def test_workflows_install_pandoc_before_using_it(self):
        root = Path(__file__).resolve().parents[1] / ".github" / "workflows"
        publish = (root / "publish-report.yml").read_text()
        self.assertLess(publish.index("apt-get install -y pandoc"), publish.index("render_journal.py"))
        tests = (root / "report-tool.yml").read_text()
        self.assertLess(tests.index("apt-get install -y pandoc"), tests.index("test_report_tools.py"))

    def test_relative_link_stays_inside_the_pull_request_prefix(self):
        page = "https://example.github.io/repo/pr-4/index.html"
        base = "https://example.github.io/repo/"
        self.assertEqual(pages_tree.path_under(base, page, "001/plot.svg"), "pr-4/001/plot.svg")
        self.assertIsNone(pages_tree.path_under(base, page, "https://example.com/elsewhere"))


if __name__ == "__main__":
    unittest.main()

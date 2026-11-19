# AGENTS.md

## Repository overview

This is a sandbox repo used by @ogrisel to conduct agent driven experimental work.

The main branch holds these instructions and the shared report publisher in `tools/` and `.github/workflows/publish-report.yml`.

Experiment code stays on dedicated branches, possibly with accompanying pull requests. Those experiment pull requests are not meant to be merged.

## Environment setup

Configure pixi based environment to manage per-experiment dedicated environments with recent enough versions of Python and feel free to choose between conda-forge and pypi.org distribution channel based on the nature of the experiment.

## Cursor Cloud specific instructions

- Use the ssh key information provided as Cursor Agent Secret to connect to remote machines if needed to conduct your experiments.
- The ssh key is passphrase protected but the passphrase is also stored as a secret.
- You can find lists of username and ip addresses to connect to hosts with CUDA GPUs on AWS also stored as secrets.
- AWS machines are specified by private IP address. You need to set a proxyjump rule to reach them. Details provided as secret.
- Those machines might not be reachable because they automatically shutdown when idling. Ask your human operator to put one back online when needed.

## Running experiments

Try to be mindful of resource usage:

- start with short running experiments that are likely to yield the most informative signal per amount of spent resources;
- when benchmarking user facing API, focus on calls that individually last more than 1s to focus on case that actually matter for humans interacting with the software instead of only reporting microbenchmark results;
- if possible run experiments that individually last for less than 10s so as to iterate faster;
- progressively run longer experiments if needed but only if this justified;
- be mindful of host and GPU memory usage (when applicable) and make sure the experiments do not fail or their results are not invalidated because of memory exhaustion. Plan experiment to always keep at least 20% of free headroom.

## Reporting

Summarize experimental results with tables in markdown files.

Keep a chronological journal inside the experiment:

- `journal/index.md` is the entry page.
- `journal/<iteration>/report.md` is one iteration. Put plots and data (`svg`, `png`, `json`) next to that report.
- Link earlier iterations from the index. The renderer rewrites links that end in `report.md` or `index.md` to `index.html`.

Render it locally with the shared tool. Pandoc must be on `PATH` (`apt install pandoc` or the equivalent). The renderer reads GitHub-flavored Markdown, including tables, fenced code, and `$...$` math, and writes MathML.

```bash
python tools/render_journal.py --journal path/to/journal --site path/to/site --title "Experiment name"
```

Publish the journal from a pull request by calling `.github/workflows/publish-report.yml`. The repository Pages setting is GitHub Actions, and the `github-pages` environment must allow pull-request refs (`refs/pull/*/merge`, or no deployment-branch restriction). The workflow renders the journal, publishes it at `https://<owner>.github.io/<repo>/pr-<number>/`, prints that URL in the job summary, and creates or updates a pull request comment with the same URL. A later deployment keeps the `pr-*` directories of other pull requests.

```yaml
name: Publish experiment report

on:
  pull_request:
    paths:
      - "my_experiment/**"

permissions:
  contents: write
  pages: write
  id-token: write
  pull-requests: write

jobs:
  report:
    uses: ogrisel/cursor-sandbox/.github/workflows/publish-report.yml@main
    with:
      journal-path: my_experiment/journal
      site-title: My experiment
```

Use `@main` after this workflow is on the default branch. Until then, call it with the ref that contains `.github/workflows/publish-report.yml`.



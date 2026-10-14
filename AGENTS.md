# AGENTS.md

## Repository overview

This is a sandbox repo used by @ogrisel to conduct agent driven experimental work.

The main branch is expected to remain empty.

Experiments are expected to happen in dedicated branches, possibly with accompanying PRs
but those PRs are never meant to be merged.

## Environment setup

Configure pixi based environment to manage per-experiment dedicated environments with recent enough versions of Python and feel free to choose between conda-forge and pypi.org distribution channel based on the nature of the experiment.

## Cursor Cloud specific instructions

- Use the ssh key information provided as Cursor Agent Secret to connect to remote machines if needed to conduct your experiments.
- You can find lists of username and ip addresses to connect to hosts with CUDA GPUs on AWS also stored as secrets.
- AWS machines are specified by private IP address. You need to set a proxyjump rule to reach them. Details provided as secret.
- Those machines might not be reachable because they automatically shutdown when idling. Ask human operator to one back on if needed.

## Running experiments

Try to be mindful of resource usage:

- start with short running experiments that are likely to yield the most informative signal per amount of spent resources;
- when benchmarking user facing API, focus on calls that individually last more than 1s to focus on case that actually matter for humans interacting with the software instead of only reporting microbenchmark results;
- if possible run experiments that individually last for less than 10s so as to iterate faster;
- progressively run longer experiments if needed but only if this justified;
- be mindful of host and GPU memory usage (when applicable) and make sure the experiments do not fail or their results are not invalidated because of memory exhaustion. Plan experiment to always keep at least 20% of free headroom.

## Reporting 

Summarize experimental results with tables in markdown files.

If those markdown files include plots, configure a CI to render the report as a small HTML website.

Render those reports as a small browsable HTML websites hosted on cloudflare' pages.dev and post a link that includes the PR number as comment to the PR once renderedC by the CI.

When iterating, keep a chronologically structured journal. Create subfolders to archive results from previous iterations and cross-links to individual subreports and make sure that the rendered website makes it easy to navigate to previous experiment reports from the rendered journal page.



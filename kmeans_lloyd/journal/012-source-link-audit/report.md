# 012 — source link audit

After [011](../011-consolidated-benchmark/report.md) was published, every
GitHub source link on the rendered PR site was checked against the code it
points to. Reports 001 to 009 linked line ranges on the
`cursor/kmeans-lloyd-fusion-8896` branch. A branch moves, so its line
numbers drift as `iteration.py` grows.

## Live site before the fix

The audit crawled all 12 pages of the published site, found 36 links to this
repository's source files, and read the line each anchor opens at. The 011
link names a whole file and has no anchor.

| report | anchored links | first line is the named definition | misaligned |
| --- | --- | --- | --- |
| 001 fusion probe | 15 | 15 | 0 |
| 003 resized shapes | 7 | 7 | 0 |
| 004 tile trade-offs | 6 | 3 | 3 |
| 005 full k-means | 6 | 1 | 5 |
| 009 k-means++ only | 1 | 1 | 0 |

The eight misaligned links opened inside other functions. For example,
004's `lloyd_step` link opened at line 311, a docstring inside
`update_centroids_tiled`, while `lloyd_step` now spans lines 406 to 454.
005's `fit_kmeans` link opened at a closing parenthesis. The aligned links
were correct only because the code above them had not moved yet. Several of
them already ended at the wrong line: `update_centroids_tiled` grew from 21
to 72 lines after empty-center relocation.

## Fix

Each link now names the full SHA of the commit that published its report,
so it shows the code that the report measured:

| report | pinned commit |
| --- | --- |
| 001 and 003 | `c476847` |
| 004 | `16cfa4d` |
| 005 | `1d641b2` |
| 009 | `9f1ab99` |
| 011 | `82e5aaa` |

Line ranges come from Python's `ast` at that commit, so each covers exactly
one function from its first line to its last. The old ranges for 004 and
005 also included one trailing blank line; the exact ranges drop it.

`tools/check_source_links.py` now runs in the report CI with full git
history. It fails when a line-anchored link names a branch instead of a
commit, when the file is missing at that commit, when a backticked function
name does not match its exact range, or when a descriptive link does not
start at a definition. It checks the 36 current links with no problems.

Previous: [consolidated benchmark](../011-consolidated-benchmark/report.md).
Index: [journal](../index.md).

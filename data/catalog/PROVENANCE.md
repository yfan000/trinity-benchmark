# Vendored: zhenghh04/application_catalog

| | |
|---|---|
| Upstream | https://github.com/zhenghh04/application_catalog |
| Pinned commit | `4c6a192242452d798afb6b7f1e44362f263a1c7d` |
| Commit date | 2026-05-13T18:56:08Z |
| Vendored | 2026-09-20 |
| Contents | 144 software entries, 9 systems (+1 template), 114 performance records |
| Licence | **none** — see below |

## This copy is unmodified

Every file is byte-identical to upstream at the pinned commit. Verify with:

```bash
python -m benchmark.catalog --verify-upstream    # all 273 files, by git blob hash
python -m benchmark.catalog --parity             # nothing our reader returns has changed
```

Two upstream files have YAML syntax errors and do not parse. **They are not fixed here.** The
repairs live outside this tree in `benchmark/catalog_repairs/`, applied at load time and guarded
by the upstream file's SHA-256: if upstream changes, the repair is refused rather than silently
shadowing new content. That keeps this directory a clean mirror, makes a refresh a plain
replace, and keeps the fixes readable as a patch to send upstream.

```
software/polaris/qe.yaml   line 7   unterminated double-quoted scalar
software/sunspot/qe.yaml   line 20  unquoted value containing ': '
```

Both are one-character fixes. `python -m benchmark.catalog --repairs` prints them as a diff.

## Licence status

Upstream has **no licence file** — the GitHub API reports `license: null` and `LICENSE` returns
404. A public repository without a licence is under default copyright: readable, but not
licensed for redistribution.

This repository is **private and internal**, so the copy is internal use. That position changes
if this repository is made public or shared outside the group, and the copy would then need
either a licence from the author or replacement by a fetch-on-demand step.

## Why vendored rather than a submodule

Upstream is a two-commit personal repository. If it is force-pushed, renamed or deleted, a
submodule would take every published number here down with it. A pinned copy keeps the benchmark
reproducible on its own, which for a result artifact is worth more than the tidier reference.

## Refreshing

```bash
bash tools/refresh_catalog.sh <commit-sha>
```

Re-clones at that commit, replaces this directory, and re-runs `--parity` and the regression
oracle so the refresh has to prove it changed nothing unexpected.

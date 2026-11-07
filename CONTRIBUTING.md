# Contributing to divelet-ml

## Setup

You need [uv][uv]. Building the site also needs [micromamba][micromamba], and the browser smoke test needs Google Chrome.

```bash
git clone https://github.com/decitre/divelet-ml.git
cd divelet-ml
uv sync
```

`uv sync` creates `.venv` with the `divelet_ml` package (editable) and the `dev` group, which provides bumpver.

## Test

These are the same checks [CI][build-yml] runs on every push and pull request:

```bash
# divelet_ml package tests, and every notebook in content/ run in CPython
uv run --group test pytest tests/test_divelet_ml.py tests/test_notebooks.py -v

# build the xeus-python and Pyodide sites into workspace/public/
./build.sh

# run every notebook in both sites in headless Chrome (after build.sh)
uv run --group browser pytest tests/smoke_test.py -v
```

The CPython run is a fast first check. Only the smoke test shows that a notebook runs in JupyterLite.

To browse the built sites, serve `workspace/public/` over HTTP, for example with `python -m http.server -d workspace/public`, and open `/xeus/` or `/pyodide/`.

## Changes

Work on a branch and open a pull request against `main`. A pull request must pass the "Build site" workflow. A push to `main` deploys the site to GitHub Pages.

## Version bump

The version lives in `src/divelet_ml/__init__.py` (`__version__`). Hatch reads it from there, and `[tool.bumpver]` in `pyproject.toml` keeps `current_version` in sync. Don't edit either one by hand. From an up-to-date `main` with a clean working tree:

```bash
uv run bumpver update --patch   # 0.1.0 -> 0.1.1; or --minor, --major
uv run bumpver update --patch --dry   # preview the change first
```

bumpver commits `bump version X -> Y`, tags it `Y` (bare version, no `v`), and pushes both to `origin`.

## Release

Publishing a GitHub release uploads the package to PyPI through [release.yml][release-yml], using trusted publishing (no token). A version on PyPI can never be replaced, so check the build first:

1. **Bump the version** as above.
2. **Test the release build without publishing:**

   ```bash
   gh workflow run release.yml --ref main -f publish=false
   ```

   It builds the sdist and wheel, runs `twine check --strict`, and checks that the installed `__version__` matches the package version.
3. **Write the release notes** in `release-notes.md`, an untracked local file. Use `### Breaking`, `### Added` and `### Fixed` sections as needed, with no version heading (the release title shows it), and refer to issues as `(#N)`.
4. **Publish the release** on the tag bumpver created:

   ```bash
   gh release create X.Y.Z --title vX.Y.Z --notes-file release-notes.md
   ```

   This triggers the publish job. Check the run under Actions → Release, then the page at [pypi.org/project/divelet-ml][pypi].

A draft release doesn't trigger the workflow. A manual run with `publish=true` on `main` also publishes, but use a release so each PyPI version has a tag and notes.

[uv]: https://docs.astral.sh/uv/
[micromamba]: https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html
[build-yml]: .github/workflows/build.yml
[release-yml]: .github/workflows/release.yml
[pypi]: https://pypi.org/project/divelet-ml/

<img src="https://raw.githubusercontent.com/decitre/divelet-ml/main/divelet-ml.svg"
     alt="Divelet ML — Deep learning, in your browser"
     width="600">

[![Build site][ci-badge]][ci-url]
[![Coverage][codecov-badge]][codecov-url]
[![Try xeus-python][xeus-badge]][xeus-url]
[![Try Pyodide][pyodide-badge]][pyodide-url]
[![Content: CC BY-SA 4.0][license-badge]][license-url]
[![Code: Apache 2.0][apache-badge]][apache]

# divelet-ml

**divelet for ML: Dive into Deep Learning, adapted for JupyterLite.**

divelet-ml is an experimental, browser-native adaptation of the Jupyter notebooks that accompany the book [*Dive into Deep Learning*][d2l-site] ("D2L" in the text below), designed to make its educational content and interactive examples accessible through [JupyterLite][jupyterlite] without requiring a local Python installation or a remote computation server.

The project aims to preserve D2L's chapter structure, mathematical explanations, learning objectives, and exercises while adapting its framework-dependent Python implementations for execution directly in the browser.

**Project status:** Early development. Compatibility assessment is underway. Adapted sections run in the browser with no installation ([all notebooks][site]):

| Section | Run with | | Source | D2L original |
|---|---|---|---|---|
| 1 Introduction | — | — | no code, read the original | [d2l.ai][d2l-1] |
| 2.1 Data Manipulation | [xeus-python][xeus-url] | [Pyodide][pyodide-url] | [notebook][nb-2.1] | [d2l.ai][d2l-2.1] |
| 3.3 Synthetic Regression Data | [xeus-python][xeus-3.3] | [Pyodide][pyodide-3.3] | [notebook][nb-3.3] | [d2l.ai][d2l-3.3] |

Build the site locally with `./build.sh` (needs uv and micromamba).

## Python package

The notebooks use `divelet_ml`, a small NumPy counterpart of D2L's `d2l` library. The site's browser kernels already include it. To use it elsewhere:

```bash
pip install divelet-ml
```

```python
import divelet_ml as d2l
```

It provides `add_to_class`, `HyperParameters` and `DataModule`, adapted from D2L's `d2l/torch.py`, and `ArrayLoader`, which yields minibatches of NumPy arrays in place of PyTorch's `DataLoader`. The package grows only as adapted chapters need more of it. Its code is licensed under the Apache License 2.0; the notebooks are not part of the package.

## Motivation

Dive into Deep Learning is an open-source, interactive textbook combining mathematical explanations with executable code.

Its implementations rely primarily on deep learning frameworks such as PyTorch, TensorFlow, JAX, and MXNet. These environments can be difficult to reproduce in a browser-only Python runtime.

divelet-ml explores whether the same educational progression can be maintained using lightweight, browser-compatible implementations.

The objective is not to reproduce the entire deep learning framework ecosystem in the browser, but to make the underlying concepts accessible through executable, pedagogically faithful examples.

## Design Principles

- **Educational fidelity:** Preserve D2L's explanations, mathematical formulations, learning objectives, and exercises wherever possible.
- **Browser-native execution:** Run examples entirely in the browser without requiring a remote Python kernel.
- **NumPy first:** Prefer NumPy implementations when they adequately illustrate the underlying concepts.
- **Framework independence:** Avoid unnecessary dependencies on full deep learning frameworks.
- **Progressive adaptation:** Adapt chapters individually, prioritizing educational value and technical feasibility.
- **Reproducibility:** Document runtime requirements, implementation differences, and compatibility limitations.

## Technical Approach

### JupyterLite

divelet-ml targets JupyterLite with two Python execution environments:

- **Pyodide:** Python compiled to WebAssembly, with access to a browser-compatible scientific Python ecosystem.
- **xeus-python:** A browser-native Python kernel built using WebAssembly.

Compatibility will be evaluated independently for each environment.

### NumPy and Deep Learning

Where practical, framework-specific operations will be replaced with NumPy equivalents.

This includes tensor manipulation, linear algebra, probability, optimization, and selected neural network implementations.

Some chapters may require more substantial adaptation, particularly those involving automatic differentiation, GPU acceleration, large datasets, or computationally expensive training.

The goal is to preserve the concepts being taught rather than provide identical framework APIs.

### Transformers.js and lmLite

For selected chapters involving modern language models or inference, divelet-ml may explore integration with [Transformers.js][transformers-js] through [lmLite][lmlite].

lmLite provides Python access to browser-native machine learning inference.

This integration is optional and is not intended to replace the mathematical and algorithmic foundations of D2L.

## Compatibility Assessment

An initial static audit of the D2L source repository has been developed to identify:

- Framework-specific implementations and dependencies.
- Candidate chapters for direct adaptation.
- Potential incompatibilities with browser-native Python runtimes.
- Estimated adaptation effort.
- Opportunities for alternative browser-native implementations.

The audit distinguishes static compatibility estimates from actual execution results.

**Static analysis does not establish that a chapter runs successfully in JupyterLite.** Browser execution and educational fidelity must be validated separately.

The initial audit references D2L commit:

`23d7a5aecceee57d1292c56e90cce307f183bb0a`

## Initial Development Plan

The first phase focuses on three representative D2L sections:

| Section | Focus | Status |
|---|---|---|
| 2.1 `chapter_preliminaries/ndarray.md` | Array operations and tensor fundamentals | Adapted |
| 3.3 `chapter_linear-regression/synthetic-regression-data.md` | Synthetic datasets and numerical computation | Adapted |
| 11.3 `chapter_attention-mechanisms-and-transformers/attention-scoring-functions.md` | Attention mechanisms and scoring functions | Planned |

The PyTorch implementations serve as the primary reference.

Each adaptation will be reviewed for educational fidelity, browser compatibility, dependencies, and reproducibility.

The project will progressively expand to additional chapters based on the results of these initial experiments.

See [ROADMAP.md][roadmap] for further details.

## Relationship to Dive into Deep Learning

divelet-ml is an independent adaptation of the original [Dive into Deep Learning][d2l-repo] project.

It is not an official D2L edition and is not affiliated with or endorsed by the original authors.

The project intends to preserve the educational contributions of D2L while adapting selected implementations for browser-native execution.

Adapted chapters will identify their original sources and document substantive modifications.

## License and Attribution

The original Dive into Deep Learning book content is distributed under the [Creative Commons Attribution-ShareAlike 4.0 International License][cc-by-sa].

Adapted educational content derived from D2L will retain the applicable attribution and ShareAlike requirements.

divelet-ml's own source code (the `divelet_ml` package, build scripts and tests) is licensed under the [Apache License 2.0][apache]. Third-party materials may be subject to separate licenses; these will be reviewed and their required notices preserved before redistribution.

The divelet-ml name and logo (`divelet-ml.svg`) are not covered by the Apache License 2.0 or CC BY-SA 4.0. © 2026 Emmanuel Decitre. All rights reserved. You may use the unmodified logo to refer to the divelet-ml project.

See [CONTENT-LICENSE.md][license-url] and [NOTICE.md][notice] for licensing and attribution details.

## Feedback and Contributions

divelet-ml is an experimental project exploring browser-native deep learning education.

Feedback is particularly welcome on:

- The educational usefulness of framework-independent implementations.
- The fidelity of NumPy adaptations to the original D2L examples.
- JupyterLite compatibility, performance, and runtime limitations.
- Opportunities for browser-native machine learning beyond traditional Python frameworks.

Please share suggestions, bug reports, and use cases through [GitHub Issues][issues]. To set up a development environment, run the tests or make a release, see [CONTRIBUTING.md][contributing].

[ci-badge]: https://github.com/decitre/divelet-ml/actions/workflows/build.yml/badge.svg
[ci-url]: https://github.com/decitre/divelet-ml/actions/workflows/build.yml
[codecov-badge]: https://img.shields.io/codecov/c/github/decitre/divelet-ml/main?flag=python&label=Coverage&logo=codecov
[codecov-url]: https://codecov.io/gh/decitre/divelet-ml
[xeus-url]: https://decitre.github.io/divelet-ml/xeus/lab/index.html?path=02_preliminaries/02.01_ndarray.ipynb
[pyodide-url]: https://decitre.github.io/divelet-ml/pyodide/lab/index.html?path=02_preliminaries/02.01_ndarray.ipynb
[xeus-badge]: https://img.shields.io/badge/try-xeus--python-f7dc1e.svg?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA0Ni43IDQ2LjciPgogIDxwYXRoCiAgICBmaWxsPSIjNDBCM0MzIgogICAgZD0iTTUgMGMyLjUuOCA0LjUgMiA0LjYgMi4xIDEuOSAxLjMgMy42IDMuMSA0LjggNS4xLjQuNiA1LjIgNy44IDguNiAxMi45LS44IDEuMi0xLjUgMi4zLTIuMSAzLjEgMC0uMS0uMS0uMS0uMS0uMkMxNy42IDE3LjkgMTEuNCA4LjYgMTEgNy45Yy0uOS0xLjMtMi0yLjUtMy41LTMuNCAwIDAtMS41LTEtMy41LTEuNkMzLjIgMi42IDEuOCAyLjQgMCAyLjJ2NDIuNGMxLjgtLjIgMy4yLS40IDQtLjcgMi0uNiAzLjUtMS42IDMuNS0xLjYgMS41LTEgMi43LTIuMiAzLjUtMy40LjQtLjcgNi42LTkuOSAxMC4xLTE1LjJDMjQgMTkuMSAzMS40IDguMSAzMS45IDcuM2MxLjItMiAyLjktMy44IDQuOC01LjEgMC0uMSAyLjEtMS4zIDQuNi0yLjFMNDEuOCAwSDV6CiAgICAgICBNNDYuNyAyLjJjLTEuOC4yLTMuMi40LTQgLjctMi4xLjYtMy42IDEuNi0zLjYgMS42LTEuNS45LTIuNiAyLjEtMy41IDMuNC0uNC43LTYuNiA5LjktMTAuMSAxNS4yLTIuOSA0LjQtMTAuMyAxNS41LTEwLjggMTYuMi0xLjIgMi0yLjkgMy44LTQuOCA1LjEgMCAuMS0yLjEgMS4zLTQuNiAyLjFsLS41LjFoMzYuOGwtLjQtLjFjLTIuNS0uOC00LjUtMi00LjYtMi4xLTEuOS0xLjMtMy42LTMuMS00LjgtNS4xLS40LS42LTUuMi03LjgtOC42LTEyLjkuOC0xLjIgMS41LTIuMyAyLjEtMy4xIDAgLjEuMS4xLjEuMiAzLjUgNS4zIDkuNyAxNC41IDEwLjEgMTUuMi45IDEuMyAyIDIuNSAzLjUgMy40IDAgMCAxLjUgMSAzLjUgMS42LjguMyAyLjIuNSA0IC43VjIuMnoiCiAgLz4KPC9zdmc+Cgo=
[pyodide-badge]: https://img.shields.io/badge/try-Pyodide-f7dc1e.svg?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI2OCIgaGVpZ2h0PSI2OCIgdmlld0JveD0iMCAwIDE3Ljk5MiAxNy45OTIiPjxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKC40NiAuNDQ4KSI+PGNpcmNsZSBjeD0iODMuNzI3IiBjeT0iODUuNjMzIiByPSI2LjU5OCIgc3R5bGU9ImZpbGw6I2Y3ZGMxZTtzdHJva2U6bm9uZTtzdHJva2Utd2lkdGg6LjI2NDU4MzMyIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtNzUuMTkxIC03OS4wMjUpIi8+PHJlY3Qgd2lkdGg9IjUuNjUzIiBoZWlnaHQ9IjEuMDEiIHg9IjgwLjgzMSIgeT0iOTIuMzQ0IiByeD0iLjQxMyIgcnk9Ii40MTMiIHN0eWxlPSJmaWxsOiNmOWY5Zjk7c3Ryb2tlOm5vbmU7c3Ryb2tlLXdpZHRoOjEuOTk5OTk5ODgiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC03NS4xOTEgLTc5LjAyNSkiLz48cmVjdCB3aWR0aD0iNS42NDEiIGhlaWdodD0iMS4wMzEiIHg9IjgwLjgzNyIgeT0iOTMuNjcxIiByeD0iLjQyMSIgcnk9Ii40MjEiIHN0eWxlPSJmaWxsOiNmOWY5Zjk7c3Ryb2tlOm5vbmU7c3Ryb2tlLXdpZHRoOjEuOTk5OTk5NzYiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC03NS4xOTEgLTc5LjAyNSkiLz48cmVjdCB3aWR0aD0iMy4yNCIgaGVpZ2h0PSIxLjAyIiB4PSI4Mi4wMzgiIHk9Ijk1LjAxOSIgcng9Ii40MTciIHJ5PSIuNDE3IiBzdHlsZT0iZmlsbDojZjlmOWY5O3N0cm9rZTpub25lO3N0cm9rZS13aWR0aDoxLjk5OTk5OTg4IiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtNzUuMTkxIC03OS4wMjUpIi8+PGcgc3R5bGU9ImZpbGw6IzFhMWExYSI+PGcgc3R5bGU9ImZpbGw6IzFhMWExYTtzdHJva2Utd2lkdGg6LjI2NDU4MzM1Ij48cGF0aCBkPSJNODcuMDY1IDkwLjI4OXEtLjk5Ni0uMDQxLTEuNDc1LTEuMjE2LS4zNTYtLjg4NC0uMzU2LTIuMTY2IDAtLjA2Ni4wMDgtLjE3LjA1OC0uODcyLjMyMy0xLjYuNDMtMS4xNzMgMS4yMTUtMS4xNzMuMDQyIDAgLjA4Ny4wMDQuNzE1LjA0NS43MTUuODMgMCAuODU3LS43MzYgMS45MDItLjQ2Ny42NjYtLjk4IDEuMDguMTQxLjc4NS4zMSAxLjE3OC4zMTUuNzI3LjkzNS43MjcuMDQxIDAgLjA4Ny0uMDA4LjEzNi0uMDI1LjM4LS4xOTguMjM2LS4xNjIuMzY4LS4xNjIuMDU4IDAgLjExMi4wMzguMTIuMDgyLjEyLjIyMy0uMDA5LjIxNS0uMzA2LjQ0Mi0uMzcyLjI2OS0uODA3LjI2OXptLS4yOC01LjcwMXEtLjI0NS4wMDQtLjQzLjIxLS40NzIuNTM0LS41MTcgMi4yMy4yNDgtLjI1My40OTYtLjU5Ni42ODYtLjkzOS42ODYtMS41ODQgMC0uMDMzLS4wMTctLjA3OC0uMDY2LS4xODItLjIxOS0uMTgyeiIgYXJpYS1sYWJlbD0ibCIgc3R5bGU9ImZpbGw6IzFhMWExYTtzdHJva2Utd2lkdGg6LjI2NDU4MzM1IiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtNzYuNDA5IC03OS40NzMpIi8+PC9nPjxwYXRoIGQ9Ik04NC45OTggODMuNjYzYS42OTQuNjk0IDAgMCAxLS42OTQuNjk1LjY5NC42OTQgMCAwIDEtLjY5NC0uNjk1LjY5NC42OTQgMCAwIDEgLjY5NC0uNjk0LjY5NC42OTQgMCAwIDEgLjY5NC42OTR6IiBzdHlsZT0iZmlsbDojMWExYTFhO3N0cm9rZTpub25lO3N0cm9rZS13aWR0aDouMjY0NTgzMzIiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC03Ni40MDkgLTc5LjQ3MykiLz48ZyBzdHlsZT0iZmlsbDojMWExYTFhO3N0cm9rZS13aWR0aDouMjY0NTgzMzUiPjxwYXRoIGQ9Ik04NC4xNTUgODQuNjY3cS4yNjkuMDA0LjI3Ny4zNWwtLjQ1OSAzLjI4M3ExLjAzNC0uNzkgMS4xNjItLjg5My4xNTMtLjEzMi4zMTQtLjEzNi4wNTggMCAuMTEyLjAzNy4xMi4wODMuMTIuMjExLS4wMDUuMTk5LS4yMjQuMzg1LS42MDcuNTEyLTEuNjA4IDEuMjZsLS4xOSAxLjM2OXEtLjAxMi4wOTUtLjAzNy4xODYtLjE5LjcyNy0uOTU1LjcyNy0uMzggMC0uNjctLjI4NS0uMjg1LS4yODUtLjI4NS0uNjQgMC0uMzczLjE3OC0uNjEyLjA5OS0uMTI0LjM4OC0uMzRsLjk5Mi0uNzQ0cS41MjUtMy40NjguNTM4LTMuNjQ2IDAtLjAyNS4wMDQtLjA0NS4wNDUtLjQ2Ny4zNDMtLjQ2N3ptLTEuMDg3IDUuNTM1LjA3LS41MDQtLjQ1OS4zNTFxLS4yOTguMjIzLS4zMDIuNDIyIDAgLjA3LjAyNS4xMzIuMDcuMTgyLjI2NS4xODIuMDc4IDAgLjE0LS4wMjUuMTk5LS4wODcuMjYtLjU1OHptLjg5Ny02LjMyNXEwLS4wNzQuMDM3LS4xNC4wODctLjE2Mi4yNjktLjE2Mi4wNzQgMCAuMTQ0LjAzNy4xNTguMDg3LjE1OC4yNjUgMCAuMDc0LS4wMzguMTQ1LS4wODYuMTU3LS4yNjQuMTU3LS4wNzUgMC0uMTQ1LS4wMzgtLjE2MS0uMDgyLS4xNjEtLjI2NHoiIGFyaWEtbGFiZWw9ImoiIHN0eWxlPSJmaWxsOiMxYTFhMWE7c3Ryb2tlLXdpZHRoOi4yNjQ1ODMzNSIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTc2LjQwOSAtNzkuNDczKSIvPjwvZz48L2c+PC9nPjwvc3ZnPiA=
[license-badge]: https://img.shields.io/badge/Content-CC%20BY--SA%204.0-lightgrey.svg
[apache-badge]: https://img.shields.io/badge/Code-Apache%202.0-blue.svg
[license-url]: https://github.com/decitre/divelet-ml/blob/main/CONTENT-LICENSE.md
[d2l-site]: https://d2l.ai/
[jupyterlite]: https://jupyterlite.readthedocs.io/
[site]: https://decitre.github.io/divelet-ml/
[d2l-1]: https://d2l.ai/chapter_introduction/index.html
[nb-2.1]: https://github.com/decitre/divelet-ml/blob/main/content/02_preliminaries/02.01_ndarray.ipynb
[d2l-2.1]: https://d2l.ai/chapter_preliminaries/ndarray.html
[xeus-3.3]: https://decitre.github.io/divelet-ml/xeus/lab/index.html?path=03_linear-regression/03.03_synthetic-regression-data.ipynb
[pyodide-3.3]: https://decitre.github.io/divelet-ml/pyodide/lab/index.html?path=03_linear-regression/03.03_synthetic-regression-data.ipynb
[nb-3.3]: https://github.com/decitre/divelet-ml/blob/main/content/03_linear-regression/03.03_synthetic-regression-data.ipynb
[d2l-3.3]: https://d2l.ai/chapter_linear-regression/synthetic-regression-data.html
[transformers-js]: https://huggingface.co/docs/transformers.js/
[lmlite]: https://github.com/decitre/lmlite
[roadmap]: https://github.com/decitre/divelet-ml/blob/main/ROADMAP.md
[d2l-repo]: https://github.com/d2l-ai/d2l-en
[cc-by-sa]: https://creativecommons.org/licenses/by-sa/4.0/
[notice]: https://github.com/decitre/divelet-ml/blob/main/NOTICE.md
[issues]: https://github.com/decitre/divelet-ml/issues
[contributing]: https://github.com/decitre/divelet-ml/blob/main/CONTRIBUTING.md
[apache]: https://github.com/decitre/divelet-ml/blob/main/LICENSE

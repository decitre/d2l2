# Attribution and Modification Notices

divelet-ml
Copyright 2026 Emmanuel Decitre

## Original Work

**Dive into Deep Learning** is an open-source interactive textbook developed by its original authors and contributors.

- **Website:** https://d2l.ai/
- **Source repository:** https://github.com/d2l-ai/d2l-en
- **Authors and contributors:** As credited in the original project
- **Book content license:** Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
- **License:** https://creativecommons.org/licenses/by-sa/4.0/

The initial divelet-ml compatibility assessment used the following upstream revision:

`23d7a5aecceee57d1292c56e90cce307f183bb0a`

https://github.com/d2l-ai/d2l-en/commit/23d7a5aecceee57d1292c56e90cce307f183bb0a

## Nature of the Adaptation

**divelet-ml** is an independent, browser-native adaptation of Dive into Deep Learning for JupyterLite.

The project aims to preserve the original book's educational structure, mathematical explanations, learning objectives, and exercises while adapting framework-dependent implementations for execution in browser-native Python environments.

Modifications, which vary between chapters, include:

- Replacing selected framework-specific implementations with NumPy or other browser-compatible alternatives.
- Adapting code examples for JupyterLite using Pyodide and xeus-python.
- Modifying dependency installation, dataset loading, and execution instructions where necessary.
- Introducing alternative browser-native implementations for selected machine learning tasks.
- Documenting differences in functionality, performance, and compatibility.

The adapted sections are listed in the README and published at https://decitre.github.io/divelet-ml/. Each one's notebook lists the specific changes made to it.

## Attribution of Adapted Chapters

The notebook of each adapted section opens with a one-line credit and ends with an "Attribution and changes" section that provides:

1. A reference to the corresponding chapter of the original book.
2. Identification of the upstream source revision.
3. Attribution to the original authors and contributors.
4. A description of substantive modifications.
5. Applicable license information.

Adapted educational content derived from the book is distributed under the terms of CC BY-SA 4.0.

## Source Code and Third-Party Materials

The licensing of executable code, illustrations, datasets, and other third-party materials may differ from that of the book's educational content.

Before incorporating such materials, divelet-ml will review their applicable licenses and preserve required copyright notices, attribution, and license terms.

The CC BY-SA 4.0 designation for adapted book content does not automatically apply to independently developed software or separately licensed third-party materials.

Code adapted from the book's sample code is used under its MIT-0 license. divelet-ml's own source code (the `divelet_ml` package, build scripts and tests) is licensed under the Apache License 2.0; see `LICENSE`.

## Name and Logo

The divelet-ml name and logo (`divelet-ml.svg`) are not covered by the Apache License 2.0 or CC BY-SA 4.0. © 2026 Emmanuel Decitre. All rights reserved. You may use the unmodified logo to refer to the divelet-ml project.

## Independence

divelet-ml is not an official edition of Dive into Deep Learning.

It is not affiliated with, sponsored by, or endorsed by the book's original authors or maintainers.

divelet-ml is not affiliated with D2L Corporation or its products.

The original work and its associated rights remain with their respective authors and copyright holders.

## Project Repository

https://github.com/decitre/divelet-ml
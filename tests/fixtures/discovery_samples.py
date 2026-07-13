"""Sample data for discovery testing."""

SAMPLE_MARKDOWN_WITH_FM = """---
title: Chapter One
author: Test Author
date: 2026-07-13
---

# Introduction

This is the introduction.

# Background

This is background information.
"""

SAMPLE_MARKDOWN_NO_FM = """# Overview

Content without front matter.

# Details

More details here.
"""

SAMPLE_ORDER_YAML = """order:
  - chapter1.md
  - chapter2.md
  - chapter3.md
"""

SAMPLE_NESTED_CHAPTERS = """---
title: Nested Chapter
---

# Main Section

Content here.

## Subsection

Nested content.

# Another Section

More content.
"""

SAMPLE_INVALID_YAML_FM = """---
title: Test
  invalid: yaml: structure:
---

# Content

Body
"""

EMPTY_MARKDOWN = """# Empty

"""

MARKDOWN_WITH_MULTIPLE_HEADINGS = """---
title: Multi Heading
---

# Level One

Content.

## Level Two

Sub content.

### Level Three

Deep content.

# Another Level One

Back to top.
"""

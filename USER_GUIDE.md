# Markdown Book Builder - User Guide

Welcome to the **Markdown Book Builder**! This guide will help you convert your Markdown documents into professional, publication-quality books in multiple formats.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Installation](#installation)
3. [Project Structure](#project-structure)
4. [Configuration](#configuration)
5. [Building Your Book](#building-your-book)
6. [Working with Images](#working-with-images)
7. [Themes and Customization](#themes-and-customization)
8. [CLI Commands Reference](#cli-commands-reference)
9. [Examples](#examples)
10. [Troubleshooting](#troubleshooting)

---

## Quick Start

### 1. Create a new book project

```bash
markdown-book-builder init my-book
cd my-book
```

### 2. Add your Markdown content

Place your `.md` files in the `content/` directory:

```
my-book/
├── book.toml
├── content/
│   ├── chapter1.md
│   ├── chapter2.md
│   └── chapter3.md
└── output/
```

### 3. Build your book

```bash
markdown-book-builder build .
```

Your PDF is now in `output/book.pdf`!

---

## Installation

### Prerequisites

- Python 3.13+
- Pandoc 3.8+ ([install here](https://pandoc.org/installing.html))
- LaTeX (for PDF support): `xelatex`, `pdflatex`, or `wkhtmltopdf`

### Install via pip

```bash
pip install markdown-book-builder
```

### Install with image generation support

```bash
pip install markdown-book-builder[images]
```

This adds OpenAI API integration for automatic image generation.

### Verify Installation

```bash
markdown-book-builder --help
```

You should see the help menu with available commands.

---

## Project Structure

### Anatomy of a Book Project

```
my-book/
├── book.toml                 # Project configuration
├── content/                  # Markdown source files
│   ├── chapter1.md
│   ├── chapter2.md
│   └── chapter3.md
├── order.yaml                # (Optional) Custom chapter ordering
├── themes/                   # (Optional) Custom CSS themes
│   └── custom-theme.css
├── output/                   # Generated books (created on build)
│   ├── book.pdf
│   ├── book.html
│   └── book.epub
└── .mbb-cache/               # (Auto-created) Image cache
    └── abc123def456.png
```

### Minimal `book.toml`

```toml
title = "My Awesome Book"
author = "Your Name"
version = "1.0.0"
source_dir = "content"

[output]
format = "pdf"
path = "output/book.pdf"
```

---

## Configuration

### book.toml Reference

#### Required Fields

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `title` | string | `"My Book"` | Book title (appears in TOC and metadata) |
| `author` | string | `"Jane Doe"` | Book author |

#### Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `version` | string | `"1.0.0"` | Book version |
| `source_dir` | string | `"."` | Directory containing Markdown files |

#### Output Configuration

```toml
[output]
format = "pdf"                    # pdf, html, epub, docx
path = "output/book.pdf"          # Output file path
pdf_engine = "xelatex"            # xelatex, pdflatex, wkhtmltopdf (PDF only)
```

#### Theme Configuration

```toml
[theme]
name = "default"                  # default, dark, minimal, or path to custom CSS
```

#### OpenAI Configuration (for image generation)

```toml
[openai]
api_key = "${OPENAI_API_KEY}"     # From environment variable
model = "gpt-4o"                  # Text model (unused currently)
image_model = "dall-e-3"          # Image generation model
```

**Important**: Set the `OPENAI_API_KEY` environment variable:

```bash
export OPENAI_API_KEY="sk-..."
markdown-book-builder build .
```

#### Plugin Configuration

```toml
[plugins]
extra_plugins = ["my_plugin.module"]  # Additional plugin modules to load
disabled = ["mermaid"]                 # Disable built-in plugins
```

---

## Building Your Book

### Build Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                    Build Process Flow                        │
└─────────────────────────────────────────────────────────────┘

  1. Load Configuration
     └─ Parse book.toml
     └─ Set output format

  2. Discover Documents
     └─ Scan content directory
     └─ Extract metadata (YAML front matter)
     └─ Order chapters (alphabetically or via order.yaml)

  3. Build AST (Abstract Syntax Tree)
     └─ Parse Markdown to internal representation
     └─ Validate structure

  4. Process Images
     └─ Detect image placeholders
     └─ Check image cache
     └─ Generate missing images (if OPENAI_API_KEY set)
     └─ Update AST with cached paths

  5. Render to Output Format
     └─ PDF: Pandoc + LaTeX engine
     └─ HTML: Pandoc + CSS theme
     └─ EPUB: Pandoc with table of contents
     └─ DOCX: Pandoc with formatting

  6. Output Complete
     └─ Written to [output.path]
```

### Single Command

```bash
markdown-book-builder build .
```

Output:

```
📚 Loading configuration...
🔍 Discovering documents in content/...
🖼️  Processing images...
📝 Rendering to PDF...
✓ Build complete: My Book (3 chapters)
✓ PDF written to output/book.pdf
```

### Output Formats

#### PDF
```bash
# Default
[output]
format = "pdf"
path = "output/book.pdf"
```

#### HTML (Standalone)
```toml
[output]
format = "html"
path = "output/book.html"
```

#### EPUB (E-book)
```toml
[output]
format = "epub"
path = "output/book.epub"
```

#### DOCX (Microsoft Word)
```toml
[output]
format = "docx"
path = "output/book.docx"
```

---

## Working with Images

### Two Ways to Include Images

#### 1. Static Images (Recommended for simple cases)

```markdown
# Chapter 1

Here is a diagram:

![Architecture Diagram](images/arch.png)
```

Place your image files in the `images/` directory. They'll be copied to the output.

#### 2. Generated Images (AI-powered)

Use an alt-text-only image and Markdown Book Builder will generate it for you:

```markdown
# Chapter 2

Here's a generated diagram:

![Generate a flowchart showing user authentication flow with login, password verification, and session creation]
```

**To enable image generation:**

1. Install with image support:
   ```bash
   pip install markdown-book-builder[images]
   ```

2. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```

3. Configure in `book.toml`:
   ```toml
   [openai]
   api_key = "${OPENAI_API_KEY}"
   image_model = "dall-e-3"
   ```

4. Build normally:
   ```bash
   markdown-book-builder build .
   ```

### Image Caching

Generated images are cached automatically using SHA256 hashing:

- **First build**: Images are generated via OpenAI API
- **Subsequent builds**: Cached images are reused (fast!)
- **Clear cache**: `markdown-book-builder images clean`

### Image Placeholder Format

```markdown
![Detailed description of what you want to see]

# Alt text is the prompt:
# - Be specific and detailed
# - Describe the layout and arrangement
# - Mention colors, style, and mood
# - Example: "A flowchart with 3 boxes connected by arrows, 
#   showing data flow from input to processing to output"
```

---

## Themes and Customization

### Built-in Themes

#### Default Theme
Clean, readable design with blue accents.

```toml
[theme]
name = "default"
```

#### Dark Theme
Dark background with light text, easy on the eyes.

```toml
[theme]
name = "dark"
```

#### Minimal Theme
Bare-bones, semantic HTML styling.

```toml
[theme]
name = "minimal"
```

### Custom Themes

Create your own theme by providing a CSS file:

```toml
[theme]
name = "./themes/custom.css"
```

Example `themes/custom.css`:

```css
:root {
  --primary-color: #2c3e50;
  --secondary-color: #3498db;
  --background: #ecf0f1;
  --text-color: #2c3e50;
}

body {
  font-family: 'Georgia', serif;
  line-height: 1.6;
  color: var(--text-color);
  background: var(--background);
}

h1, h2, h3 {
  color: var(--primary-color);
  margin-top: 1.5em;
  margin-bottom: 0.5em;
}

a {
  color: var(--secondary-color);
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
```

**Supported on**: HTML, EPUB (PDF themes not supported by Pandoc)

---

## CLI Commands Reference

### init

Create a new book project scaffold.

```bash
markdown-book-builder init <path>
```

**Output:**
- `book.toml` - Configuration file
- `content/` - Directory for Markdown files
- Sample chapter

### build

Build your book in the configured output format.

```bash
markdown-book-builder build <path>
```

**Supports:**
- Directory: `markdown-book-builder build .`
- TOML file: `markdown-book-builder build ./book.toml`

**Output:** Book in the format specified in `book.toml`

### validate

Check your project structure and configuration.

```bash
markdown-book-builder validate <path>
```

**Checks:**
- Configuration validity
- Markdown file syntax
- Missing referenced images
- Broken links (future)

### config

Display the loaded configuration.

```bash
markdown-book-builder config <path>
```

**Shows:**
- All settings (merged from environment variables)
- Output format and path
- Theme configuration

### images clean

Clear the image cache.

```bash
markdown-book-builder images clean
```

**Clears:**
- All cached generated images
- Frees up disk space

---

## Examples

### Example 1: Simple Technical Book

**Project structure:**

```
my-book/
├── book.toml
└── content/
    ├── 01-introduction.md
    ├── 02-getting-started.md
    ├── 03-advanced-topics.md
    └── 04-api-reference.md
```

**book.toml:**

```toml
title = "The Technical Guide"
author = "Alice Engineer"
version = "1.0.0"
source_dir = "content"

[output]
format = "pdf"
path = "output/technical-guide.pdf"

[theme]
name = "default"
```

**Build:**

```bash
markdown-book-builder build .
```

---

### Example 2: Multi-format Book with Custom Theme

**book.toml:**

```toml
title = "Illustrated Guide to Kubernetes"
author = "Bob DevOps"
version = "2.1.0"
source_dir = "content"

[output]
format = "html"
path = "output/k8s-guide.html"
pdf_engine = "xelatex"

[theme]
name = "./themes/modern.css"

[openai]
api_key = "${OPENAI_API_KEY}"
image_model = "dall-e-3"

[plugins]
disabled = []
```

**Build:**

```bash
markdown-book-builder build .
```

---

### Example 3: Book with Generated Diagrams

**content/chapter-architecture.md:**

```markdown
# System Architecture

## Overview

Here's our microservices architecture:

![A detailed system architecture diagram showing 5 microservices 
(Auth, API, Database, Cache, Queue) connected with arrows indicating 
communication flow. Use a professional style with boxes and connecting lines.]

## Data Flow

The system processes requests through these stages:

![A flowchart showing the request flow: Client → Load Balancer → 
Authentication Service → API Gateway → Business Logic → Database. 
Include stage labels and decision points.]
```

**book.toml:**

```toml
title = "Microservices Handbook"
author = "Carol Cloud"

[openai]
api_key = "${OPENAI_API_KEY}"
image_model = "dall-e-3"
```

**Build:**

```bash
export OPENAI_API_KEY="sk-..."
markdown-book-builder build .
```

First build generates images via OpenAI. Subsequent builds reuse cached images.

---

### Example 4: EPUB Book for Distribution

**book.toml:**

```toml
title = "Journey Through Code"
author = "David Developer"

[output]
format = "epub"
path = "output/book.epub"

[theme]
name = "default"
```

**Build:**

```bash
markdown-book-builder build .
# Output: output/book.epub (ready for Amazon Kindle, Apple Books, etc.)
```

---

## Troubleshooting

### "pandoc not found on PATH"

**Problem**: Pandoc is not installed or not in PATH.

**Solution**:
```bash
# macOS
brew install pandoc

# Ubuntu/Debian
sudo apt-get install pandoc

# Or download from https://pandoc.org/installing.html
```

### "PDF renderer not available"

**Problem**: LaTeX engine (xelatex, pdflatex) not installed.

**Solution** (macOS):
```bash
# Full LaTeX
brew install mactex

# Minimal LaTeX
brew install basictex
```

**Solution** (Ubuntu/Debian):
```bash
sudo apt-get install texlive-xetex texlive-fonts-recommended
```

### "OpenAI API key not configured"

**Problem**: Image generation attempted without OPENAI_API_KEY.

**Solution**:
```bash
export OPENAI_API_KEY="sk-..."
markdown-book-builder build .
```

Or set in `book.toml`:
```toml
[openai]
api_key = "sk-..."  # Not recommended; use environment variable instead
```

### "No Markdown files found"

**Problem**: No `.md` files in the source directory.

**Solution**:
- Add `.md` files to the directory specified in `book.toml` (`source_dir`)
- Verify the directory exists: `ls content/`
- Check file extensions are `.md` (not `.markdown` or `.txt`)

### Image generation too slow

**Problem**: First build with many images takes a long time.

**Reason**: OpenAI API generates each image individually (~30s each).

**Solution**:
- First build is slow (image generation happens once)
- Subsequent builds are fast (cached images reused)
- Batch images across multiple chapters for efficiency

### PDF rendering looks wrong

**Problem**: Formatting, fonts, or layout issues in PDF output.

**Solution**:
- Verify you're using a PDF engine: `pdf_engine = "xelatex"` in `book.toml`
- Check LaTeX is installed: `xelatex --version`
- Try a different PDF engine: `pdflatex` or `wkhtmltopdf`
- Use HTML or EPUB format as a fallback

---

## Advanced Usage

### Custom Chapter Ordering

By default, chapters are ordered alphabetically. To customize:

**order.yaml:**

```yaml
order:
  - preface.md
  - chapter-01-intro.md
  - chapter-02-basics.md
  - chapter-03-advanced.md
  - appendix.md
```

The build will respect this order.

### Document Front Matter

Add metadata to each Markdown file:

```markdown
---
title: Advanced Topics
author: Override Author
date: 2024-01-15
---

# Advanced Topics

Content here...
```

---

## Next Steps

- 📚 **Read**: [CONTRIBUTING.md](CONTRIBUTING.md) to contribute plugins
- 🔌 **Extend**: Create custom plugins via [PLUGIN_DEVELOPMENT.md](PLUGIN_DEVELOPMENT.md)
- 🐛 **Report Issues**: [GitHub Issues](https://github.com/your-org/markdown-book-builder/issues)
- 💬 **Get Help**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more solutions

---

## FAQ

**Q: Can I use Markdown features like tables and code blocks?**
A: Yes! All CommonMark features are supported: tables, code blocks, blockquotes, lists, etc.

**Q: Can I build multiple formats in one command?**
A: Currently, one format per build. Workaround: create separate `book-pdf.toml`, `book-html.toml`, etc.

**Q: Do I need to write HTML/CSS?**
A: No, use the built-in themes. For customization, basic CSS knowledge helps.

**Q: Is my book truly reproducible/deterministic?**
A: Yes! Same input → identical output. Configuration is versioned, images are cached by hash.

**Q: What if I don't have an OpenAI account?**
A: You can still build books with static images. The image generation is optional.

---

**Happy writing! 📖✨**

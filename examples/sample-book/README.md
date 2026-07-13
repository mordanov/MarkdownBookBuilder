# Sample Book: The Complete Guide to Markdown Book Builder

This is a complete sample project with **12 chapters** demonstrating all features of the Markdown Book Builder system.

## Project Structure

```
sample-book/
├── book.toml              # Project configuration (title, author, format)
├── order.yaml             # Custom chapter ordering
├── README.md              # This file
└── content/               # Chapter files (12 chapters)
    ├── 01-introduction.md
    ├── 02-getting-started.md
    ├── 03-chapter3.md
    └── ... (through chapter 12)
```

## Quick Start

### 1. Build the Sample Book

```bash
cd examples/sample-book
markdown-book-builder build .
```

This creates `output/book.pdf` with all 12 chapters.

### 2. Validate Structure

```bash
markdown-book-builder validate .
```

### 3. View Configuration

```bash
markdown-book-builder config .
```

## Sample Chapters

The book includes:

- **Chapter 1**: Introduction to the system
- **Chapter 2**: Getting started guide
- **Chapters 3-12**: Detailed topics with examples

Each chapter demonstrates standard Markdown formatting, front matter metadata, and structure.

## Customization

### Add a New Chapter

1. Create `content/13-new-chapter.md`
2. Update `order.yaml` to include the new chapter
3. Rebuild: `markdown-book-builder build .`

### Change Chapter Order

Edit `order.yaml` to reorder chapters:

```yaml
order:
  - 02-getting-started.md
  - 01-introduction.md
  - 03-chapter3.md
```

### Update Metadata

Edit `book.toml`:

```toml
title = "Your Title"
author = "Your Name"
version = "2.0.0"
```

## Features Demonstrated

- ✅ Multi-chapter book structure
- ✅ YAML front matter for chapter metadata
- ✅ Custom chapter ordering via order.yaml
- ✅ Standard Markdown formatting
- ✅ Configuration via book.toml
- ✅ Deterministic builds (same output each time)
- ✅ Project initialization and validation

## Tips

- Use sequential numbering for chapters (01-, 02-, etc.) for easy sorting
- Keep chapter titles descriptive and unique
- Use front matter for chapter-specific metadata
- Run `validate` after making changes
- Use `build .` to rebuild the final output

## Next Steps

- Modify existing chapters
- Add more chapters (13+, 20+, etc.)
- Generate images with OpenAI API (set `OPENAI_API_KEY`)
- Customize colors and styling via themes (future feature)

Happy writing! 📚

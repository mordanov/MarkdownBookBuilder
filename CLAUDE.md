# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Markdown Book Builder** is a developer-focused book processing pipeline that converts a collection of Markdown documents into professionally typeset books (PDFs). The system is designed for technical authors who need deterministic, reproducible, automated book generation with AI-assisted image generation.

See `Markdown_Book_Builder_PRD.md` for the full product requirements.

## Architecture

The system is organized around a **pipeline-based architecture** with a central AST (Abstract Syntax Tree) that all transformations operate on. Key architectural layers:

1. **Document Discovery**: Recursively scans and orders Markdown files, extracts metadata
2. **AST Transformation**: All processing stages (diagrams, images, validation) operate on an internal AST representation
3. **Plugins**: Extensible system for diagram renderers, image providers, exporters, themes, and validation rules
4. **Rendering**: Final export to PDF via Pandoc + Typst (LaTeX optional)

### Technology Stack

- **Language**: Python 3.13
- **Package Manager**: `uv`
- **CLI Framework**: Typer
- **Validation**: Pydantic
- **Linting**: Ruff
- **Type Checking**: mypy
- **Testing**: pytest
- **Configuration**: TOML
- **Image Generation**: OpenAI API (via official SDK)

### Key Extension Points

Future implementations will plugin into:
- Diagram renderers (Mermaid, PlantUML, Graphviz, D2, Draw.io)
- Image providers (cache system, OpenAI generation)
- Exporters (Typst, LaTeX, EPUB, DOCX, HTML)
- Themes (customizable styling)
- Validation rules (custom checks)

## Development Commands

### Setup

```bash
# Initialize virtual environment and install dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate
```

### Build & Run

```bash
# Run the CLI (adjust command based on final entry point)
python -m markdown_book_builder --help

# Build a book from a directory
python -m markdown_book_builder build <path-to-markdown-dir>

# Validate book structure
python -m markdown_book_builder validate <path-to-markdown-dir>

# Initialize a new book project
python -m markdown_book_builder init <path>

# Manage image cache
python -m markdown_book_builder images clean
```

### Code Quality

```bash
# Format code
ruff format .

# Lint code
ruff check . --fix

# Type checking
mypy .

# Run all checks (format, lint, type-check)
ruff check . && mypy . && ruff format --check .
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov

# Run a specific test file
pytest tests/test_<module>.py

# Run a specific test
pytest tests/test_<module>.py::test_<function>

# Run tests with verbose output
pytest -v

# Watch mode (requires pytest-watch)
ptw
```

## Project Structure (Phase 1)

During Phase 1 (SpecKit, ADRs, Core AST, CLI), expect:
- Core AST definitions and transformations
- CLI command structure using Typer
- Basic document discovery
- Project and build configuration

Configuration is TOML-based with environment variables for secrets (OpenAI API key, etc.).

## Testing Strategy

- **Unit tests**: Core transformations, AST operations
- **Integration tests**: Full pipeline stages
- **Snapshot tests**: Document output consistency
- **Golden files**: Expected CLI outputs
- **CLI tests**: Command parsing and error handling

Use pytest fixtures for reusable test data and mock OpenAI responses.

## Key Principles

1. **Deterministic Builds**: Same input → identical output (enables caching and reproducibility)
2. **Incremental Processing**: Cache stages to skip re-processing unchanged content
3. **Error Reporting**: Non-zero exit codes, machine-readable reports for CI
4. **Modular Design**: Plugin architecture allows extending without core changes
5. **Performance**: Support 1000+ page books with reasonable build times

## Important Notes

- All transformations work on the internal AST — this is the central abstraction
- Configuration is versioned (part of reproducibility guarantee)
- Idempotent pipeline design enables safe retry policies
- Caching strategy critical for large books and costly operations (OpenAI API)
- Cross-platform rendering is a known risk (test on macOS, Linux, Windows)

## References

- PRD: `Markdown_Book_Builder_PRD.md`
- Configuration: TOML files (schema to be defined)
- Plugin contract: (to be documented in ADRs)

<!-- SPECKIT START -->
For additional context about technologies to be used, project structure,
shell commands, and other important information, read the current plan at
`specs/005-pdf-formatting/plan.md`
<!-- SPECKIT END -->

# Markdown Book Builder

**Developer-focused book processing pipeline** that converts collections of Markdown documents into professionally typeset books (PDFs) with deterministic, reproducible builds.

## Features

- 📄 **Markdown-first**: Organize your book as a collection of Markdown files
- 🎯 **Deterministic builds**: Same input → identical output, every time
- 🔌 **Extensible**: Plugin architecture for renderers, themes, and validators
- 🤖 **AI-assisted**: OpenAI integration for image generation
- ⚡ **Fast**: Document discovery <1s for 100+ files; CLI <100ms
- 🔒 **Reproducible**: Configuration-driven builds with version-pinned dependencies

## Quick Start

### Prerequisites

- Python 3.13+
- `uv` package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/markdown-book-builder.git
cd markdown-book-builder

# Install dependencies with uv
uv sync

# Activate virtual environment
source .venv/bin/activate

# Verify installation
python -m markdown_book_builder --help
```

### Creating Your First Book

```bash
# Initialize a new book project
python -m markdown_book_builder init my-book

# Navigate to project
cd my-book

# Edit Markdown files in the content/ directory
# Edit book.toml to configure title, author, etc.

# Build the book
python -m markdown_book_builder build .
```

## Project Structure

```
markdown-book-builder/
├── src/
│   └── markdown_book_builder/          # Main package
│       ├── __init__.py                 # Version and public API
│       ├── __main__.py                 # CLI entry point
│       ├── ast_/                       # Abstract Syntax Tree definitions
│       │   ├── models.py               # Pydantic AST node types
│       │   └── transform.py            # Tree transformations
│       ├── cli/                        # CLI commands (Typer)
│       │   ├── main.py                 # Root app and commands
│       │   ├── build.py                # Build command
│       │   ├── validate.py             # Validate command
│       │   ├── init.py                 # Init command
│       │   ├── config.py               # Config command
│       │   └── images.py               # Image management
│       ├── config/                     # Configuration system
│       │   ├── models.py               # Pydantic config schema
│       │   └── loader.py               # TOML + env var loading
│       ├── discovery/                  # Document discovery
│       │   ├── scanner.py              # File scanning
│       │   └── metadata.py             # Front matter parsing
│       └── core/                       # Shared utilities
│           ├── errors.py               # Custom exceptions
│           ├── logging.py              # Logging setup
│           └── types.py                # Type aliases and constants
├── tests/
│   ├── unit/                           # Unit tests
│   ├── integration/                    # Integration tests
│   ├── contract/                       # CLI/API contract tests
│   ├── fixtures/                       # Test fixtures
│   │   ├── ast_samples.py              # Sample AST instances
│   │   ├── markdown_samples.py         # Sample Markdown
│   │   ├── config_samples.py           # Sample configs
│   │   └── golden/                     # Golden file outputs
│   └── conftest.py                     # Pytest configuration
├── docs/
│   ├── adr/                            # Architecture Decision Records
│   ├── testing.md                      # Testing guide
│   └── quickstart.md                   # Developer onboarding
├── pyproject.toml                      # Project metadata and tools config
├── .pre-commit-config.yaml             # Pre-commit hooks
├── .gitignore                          # Git ignore rules
└── README.md                           # This file
```

## Development

### Setup

```bash
# Install with development dependencies
uv sync

# Install pre-commit hooks
pre-commit install

# Verify setup
python -m markdown_book_builder --help
```

### Code Quality

```bash
# Format code with Ruff
ruff format src/ tests/

# Lint with Ruff
ruff check src/ tests/ --fix

# Type check with mypy
mypy src/

# Run all checks
ruff check . && ruff format --check . && mypy .
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov

# Run specific test file
pytest tests/unit/test_ast_models.py

# Watch mode (requires pytest-watch)
ptw

# Run tests by marker
pytest -m unit
pytest -m integration
```

### Test Markers

- `@pytest.mark.unit` - Unit tests for core modules
- `@pytest.mark.integration` - Integration tests for pipeline stages
- `@pytest.mark.contract` - CLI and API contract tests
- `@pytest.mark.slow` - Slow-running tests (skipped by default)

## CLI Commands

```bash
# Build a book
python -m markdown_book_builder build path/to/markdown

# Validate book structure
python -m markdown_book_builder validate path/to/markdown

# Initialize new book project
python -m markdown_book_builder init my-book

# Show configuration
python -m markdown_book_builder config

# Manage images
python -m markdown_book_builder images clean

# Enable verbose output
python -m markdown_book_builder --verbose build path/to/markdown
```

## Configuration

Create a `book.toml` file in your project root:

```toml
title = "My Awesome Book"
author = "Your Name"
version = "1.0.0"

[output]
format = "pdf"
path = "output/my-book.pdf"

# Set API keys via environment variables
# export OPENAI_API_KEY="sk-..."
```

## Architecture

### Core Concepts

1. **AST-Centric Design**: All processing stages operate on an Abstract Syntax Tree representation defined with Pydantic
2. **Deterministic Builds**: Same input configuration + Markdown files → identical output (enables caching and CI/CD)
3. **Plugin Architecture**: Extensible via plugins for renderers, themes, validators, and image providers
4. **Reproducibility**: Configuration versioning and dependency pinning ensure reproducible builds across environments

### Data Flow

```
Markdown Files → Discovery → Parser → AST → Transformations → Renderer → PDF
                                ↓
                          Config System
                          (TOML + Env)
```

## Performance Targets

- Document discovery: <1s for 100+ files
- CLI help response: <100ms
- Configuration loading: <50ms (valid TOML); <100ms (error reporting)
- Builds: Scale to 1000+ page books

## Success Criteria

- ✅ All tests pass with >80% coverage on core modules
- ✅ CLI responds to `--help` within <100ms
- ✅ Document discovery completes for 100+ files in <1 second
- ✅ AST serialization/deserialization is lossless (100% round-trip fidelity)
- ✅ Developers can set up project with `uv sync` in <2 minutes

## Contributing

1. Read [CONTRIBUTING.md](./docs/CONTRIBUTING.md) for development workflow
2. Follow the testing strategy: unit tests → integration tests → contract tests
3. Write tests before implementation (TDD approach)
4. Ensure all checks pass: `ruff check .`, `ruff format --check .`, `mypy .`, `pytest --cov`

## License

MIT License - see LICENSE file for details

## References

- [Product Requirements Document](./Markdown_Book_Builder_PRD.md)
- [Implementation Plan](./specs/001-project-foundation/plan.md)
- [Architecture Decision Records](./docs/adr/)
- [Testing Guide](./docs/testing.md)

---

**Phase 1 Status**: ✅ Foundation complete (CLI scaffolding, config system, AST models, discovery framework)

Next phases: Phase 2 (Diagram rendering), Phase 3 (Image generation), Phase 4 (Multiple exporters)

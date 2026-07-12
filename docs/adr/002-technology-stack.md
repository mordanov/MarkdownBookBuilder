# ADR-002: Technology Stack Selection

**Status**: Accepted

## Context

We need to select a technology stack that enables:
- Fast CLI performance (<100ms for help)
- Type safety and validation
- Easy dependency management
- Modern Python ecosystem
- Minimal external dependencies

## Decision

**Core Stack**:
- **Language**: Python 3.13 (latest stable)
- **Package Manager**: `uv` (fast, deterministic)
- **CLI Framework**: Typer (modern, minimal syntax)
- **Validation**: Pydantic (comprehensive, performant)
- **Linting**: Ruff (fast Rust-based)
- **Type Checking**: mypy (mature, standards-based)
- **Testing**: pytest (flexible, rich ecosystem)
- **Rendering**: Pandoc + Typst (mature, high-quality output)
- **Image Generation**: OpenAI API (via official SDK)

## Consequences

**Advantages**:
- Python 3.13 supports latest language features (match expressions, type unions)
- `uv` provides deterministic, reproducible builds
- Typer reduces CLI boilerplate compared to Click/argparse
- Pydantic's validation handles configuration edge cases
- Ruff is 10-100x faster than pylint/flake8
- Pandoc + Typst pipeline produces professional-quality PDFs

**Disadvantages**:
- Python is slower than compiled languages (mitigated by targeting <100ms CLI help)
- uv is newer (mitigated by wide adoption in Python community)
- Typer is opinionated (minimal downside; well-designed opinions)
- Pandoc adds external dependency (acceptable; it's the industry standard)

**Trade-offs**:
- Chose uv over pip/poetry for speed and reproducibility
- Chose Typer over Click for cleaner API (fewer decorator layers)
- Chose Ruff over pylint for speed (linting must be fast for pre-commit)

## Alternatives Considered

1. **Go**: Faster CLI, better cross-platform support
   - Rejected: Authors prefer Python; Typst integration easier in Python

2. **Rust**: Maximum performance and safety
   - Rejected: Longer development cycle, smaller team familiarity

3. **pip + Poetry**: Traditional Python packaging
   - Rejected: uv is faster and has deterministic lock files

4. **Click**: Established CLI framework
   - Rejected: Typer has less boilerplate and better type hints

## Migration Path

Technology can be substituted if requirements change:
- Rendering engine: Pandoc → Weasyprint/wkhtmltopdf (for HTML pipelines)
- API client: OpenAI SDK → LangChain/LiteLLM (if multi-LLM support needed)
- Package manager: uv → pip/poetry (if uv adoption is blocked)

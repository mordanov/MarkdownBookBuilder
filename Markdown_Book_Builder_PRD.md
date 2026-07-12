
# Product Requirements Document (PRD)
# Markdown Book Builder

Version: 1.0

## 1. Executive Summary
Markdown Book Builder is a developer-focused Book Processing Pipeline that converts a collection of Markdown documents into a professionally typeset book. The system targets technical authors who want deterministic, reproducible, automated book generation with AI-assisted illustration generation.

## 2. Goals
- Produce publication-quality PDFs.
- Minimize manual editing.
- Incremental, reproducible builds.
- Extensible plugin architecture.
- AI-assisted image generation.

## 3. Non-Goals
- Rich WYSIWYG editing.
- Cloud SaaS.
- Collaborative editing.

## 4. Target Users
Primary:
- Software engineers
- Technical writers
- Documentation teams
- Authors of programming books

Secondary:
- Trainers
- Researchers

## 5. User Stories

### Book Author
As an author, I want to point the CLI at a directory so that I receive a complete PDF book.

Acceptance Criteria:
- One command builds the book.
- TOC generated automatically.
- Figures numbered.
- Broken links reported.

### Technical Writer
As a writer, I want image placeholders converted into illustrations.

Acceptance Criteria:
- Missing images generated via OpenAI.
- Existing images reused.
- Cache prevents duplicate generation.

### Engineer
As an engineer, I want deterministic builds.

Acceptance Criteria:
- Same input -> identical output.
- Cached stages skipped.
- Configuration versioned.

### Documentation Team
As a team, we want CI builds.

Acceptance Criteria:
- Headless CLI.
- Non-zero exit code on errors.
- Machine-readable reports.

## 6. Functional Requirements

### Document Discovery
- Recursive scan
- Ordering
- Metadata

### Book AST
All transformations operate on an internal AST.

### Diagram Pipeline
Support Mermaid initially.
Render to SVG preferred.
Future plugins:
- PlantUML
- Graphviz
- D2
- Draw.io

### Image Pipeline
Detect placeholders.
Generate via OpenAI Images API.
Cache by prompt hash.

### Rendering
Pandoc + Typst primary.
LaTeX optional.

### CLI
Commands:
- build
- validate
- init
- images
- clean
- config

## 7. Non-functional Requirements
Performance:
- 1000+ page books.

Reliability:
- Idempotent pipeline.
- Incremental builds.

Maintainability:
- Modular architecture.
- Dependency injection where appropriate.

## 8. Architecture Constraints
- Python 3.13
- uv
- Typer
- Pydantic
- Ruff
- mypy
- pytest
- Official OpenAI SDK
- TOML configuration

Mandatory planning:
- GitHub SpecKit
- Brainstorm MCP
- ADRs

## 9. Plugin Architecture

Extension points:
- Diagram renderers
- Image providers
- Exporters
- Themes
- Validation rules

## 10. Configuration
TOML-based configuration.
Environment variables for secrets.

## 11. Testing Strategy
- Unit tests
- Integration tests
- Snapshot tests
- Golden files
- CLI tests

## 12. Risks
- OpenAI API cost
- PDF reproducibility
- Large images
- Cross-platform rendering

Mitigation:
- Cache
- Hashing
- Retry policies
- Incremental builds

## 13. Roadmap

Phase 1
- SpecKit
- ADRs
- Core AST
- CLI

Phase 2
- Markdown merge
- Typst export
- TOC

Phase 3
- Mermaid rendering
- Image cache

Phase 4
- OpenAI image generation

Phase 5
- Plugin system
- Themes

Phase 6
- EPUB
- DOCX
- HTML

## 14. Definition of Done
- All tests pass.
- CI green.
- Documentation complete.
- Reproducible builds.
- Example book included.

## 15. Success Metrics
- One-command build.
- <10% rebuild after small change.
- Deterministic output.
- 90%+ test coverage of core pipeline.

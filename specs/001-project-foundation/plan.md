# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit-plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Establish the Markdown Book Builder project foundation with core AST data model, CLI scaffolding, document discovery, and configuration system. This phase creates the pipeline architecture and core abstractions that all downstream features depend on—diagram rendering, image generation, and exporters will plugin into the defined AST and configuration system.

## Technical Context

**Language/Version**: Python 3.13  
**Primary Dependencies**: Typer (CLI), Pydantic (validation/AST), Ruff (linting), mypy (type checking), pytest (testing)  
**Storage**: File-based (Markdown input); configuration via TOML; no database  
**Testing**: pytest with fixtures, snapshot tests, golden files  
**Target Platform**: macOS, Linux, Windows (via `uv` for cross-platform support)  
**Project Type**: CLI application + pluggable library  
**Performance Goals**: Document discovery <1s for 100+ files; CLI --help <100ms; config load <50ms  
**Constraints**: Deterministic builds (same input → identical output); reproducible caching strategy; Python 3.13 only  
**Scale/Scope**: Support 10+ chapter books initially; extensible for 1000+ page books in future phases

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Status**: Constitution file is a template (placeholder). No constitutional principles have been ratified yet. This project foundation phase should establish the core principles (e.g., AST-centric design, deterministic builds, plugin architecture, test-first discipline). Constitution to be finalized after Phase 0 research is complete.

**Action**: After Phase 0, use `/speckit-constitution` to ratify project principles.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output (/speckit-plan command)
├── data-model.md        # Phase 1 output (/speckit-plan command)
├── quickstart.md        # Phase 1 output (/speckit-plan command)
├── contracts/           # Phase 1 output (/speckit-plan command)
└── tasks.md             # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)

```text
src/
└── markdown_book_builder/      # Main package (src-layout convention)
    ├── __init__.py
    ├── __main__.py             # Entry point: python -m markdown_book_builder
    ├── ast_/                   # Core AST definitions
    │   ├── __init__.py
    │   ├── models.py           # Pydantic models (Book, Chapter, Section, Image, CodeBlock, etc.)
    │   └── transform.py        # AST transformation utilities
    ├── discovery/              # Document discovery
    │   ├── __init__.py
    │   ├── scanner.py          # Recursive file scanning + ordering
    │   └── metadata.py         # Front matter parsing
    ├── cli/                    # CLI commands (Typer-based)
    │   ├── __init__.py
    │   ├── main.py             # Main CLI app and root commands
    │   ├── build.py            # `build` command
    │   ├── validate.py         # `validate` command
    │   ├── init.py             # `init` command
    │   ├── images.py           # `images` subcommand group
    │   └── config.py           # `config` command
    ├── config/                 # Configuration system
    │   ├── __init__.py
    │   ├── models.py           # Pydantic config schema
    │   └── loader.py           # TOML loading + env var overrides
    └── core/                   # Shared utilities
        ├── __init__.py
        ├── errors.py           # Custom exceptions
        ├── logging.py          # Logging setup
        └── types.py            # Type aliases

tests/                          # Tests at repository root
├── __init__.py
├── fixtures/                   # Reusable test fixtures
│   ├── __init__.py
│   ├── ast_samples.py          # Sample AST instances
│   ├── markdown_samples.py     # Sample markdown content
│   ├── config_samples.py       # Sample TOML configs
│   └── golden/                 # Golden file outputs
│       └── README.md
├── unit/                       # Unit tests
│   ├── test_ast_models.py
│   ├── test_discovery.py
│   ├── test_config.py
│   └── test_cli.py
├── integration/                # Integration tests
│   ├── test_pipeline.py        # End-to-end build pipeline
│   └── test_golden_files.py    # Golden file comparison
└── contract/                   # Contract tests (CLI interface, output formats)
    └── test_cli_interface.py

pyproject.toml                  # Project metadata, dependencies, tool config
uv.lock                         # Locked dependency versions
.pre-commit-config.yaml         # Pre-commit hooks (ruff, mypy)
```

**Structure Decision**: Single monolithic package (Option 1) with clear separation of concerns (AST, discovery, CLI, config). All modules operate on the central AST abstraction. Tests organized by type (unit, integration, contract) with shared fixtures for deterministic testing.

## Complexity Tracking

**Status**: No violations. Architecture is straightforward:
- Single monolithic Python package (no multi-project complexity)
- Clear separation: AST layer, discovery, CLI, config (no cross-cutting concerns)
- Plugin pattern is extensibility mechanism (deferred to Phase 3+)
- No repository pattern needed (stateless transformations)

Complexity is appropriate to requirements and manageable within Phase 1 scope.

---

## Phase 0 Outputs

**Generated**:
- `research.md` — All technical decisions documented with rationale and alternatives considered
- Updated `plan.md` (this file) — Technical context filled, complexity assessment complete

**Key Decisions Finalized**:
1. AST: Pydantic discriminated unions with visitor pattern for transformations
2. Parsing: `python-frontmatter` + `markdown-it-py` with line-number tracking
3. CLI: Typer hierarchical command groups with modular file structure
4. Config: Pydantic Settings + tomllib with environment override precedence
5. Testing: Syrupy snapshots + golden files + 80%+ coverage threshold

**Unknowns Resolved**: 0 — All technical areas researched and decisions documented

---

## Phase 1: Design & Contracts (Weeks 1–2)

### Deliverables

This phase generates three key artifacts:

#### 1. `data-model.md` — Entity Definitions

Documents the core AST node types with Pydantic schemas:

```
Book (root)
├── chapters: List[Chapter]
├── metadata: dict

Chapter
├── title: str (required)
├── sections: List[Section | Paragraph | CodeBlock | Image]
├── metadata: dict (from front matter)

Section
├── title: str
├── level: int (1–6, heading level)
├── children: List[Section | Paragraph | CodeBlock | Image]

Paragraph
├── children: List[Text | CodeBlock | Image]

Text
├── content: str (non-empty)

CodeBlock
├── language: str (constrained to known syntaxes)
├── content: str
├── line_numbers: bool

Image
├── path: str (relative, no absolute paths)
├── alt_text: str (required, describes image)
├── caption: Optional[str]
├── width/height: Optional[str] (standard units)
```

**Validation rules**: See `research.md` Section 1 for all constraint definitions.

#### 2. `contracts/` — Public Interface Specifications

Since this is a CLI application + pluggable library:

**CLI Contract** (`contracts/cli.md`):
- Command structure and argument specifications
- Exit codes (0=success, 1=runtime error, 2=usage error)
- Help text format
- Output format (human-readable + JSON)
- Configuration file schema (book.toml)

**Plugin Contract** (`contracts/plugin.md`):
- Transformation plugin interface (`visit(node, context) -> node`)
- Node registry API (registration, lookup)
- Validator plugin interface
- Error reporting format

**Configuration Contract** (`contracts/config.md`):
- TOML schema (required fields, types, defaults)
- Environment variable naming convention (`BOOK_*`, `OPENAI_*`)
- Validation error messages

#### 3. `quickstart.md` — Developer Onboarding

Quick reference for developers implementing Phase 1:

```
## Quick Start: Phase 1 Implementation

### 1. AST Nodes
Create `src/markdown_book_builder/ast/nodes.py`:
- Define Pydantic models for all node types
- Enable self-references with model_rebuild()
- Write snapshot tests for round-trip serialization

### 2. CLI Structure
Create `src/markdown_book_builder/cli/` hierarchy:
- main.py: Root Typer app + callback
- build.py, validate.py, init.py: Core commands
- config/, images/: Command groups
- error_handlers.py: Exit codes + exceptions

### 3. Configuration
Create `src/markdown_book_builder/config/`:
- settings.py: Pydantic Settings schema
- loader.py: TOML file loader

### 4. Discovery
Create `src/markdown_book_builder/discovery/`:
- scanner.py: Recursive Markdown file discovery + ordering
- metadata.py: Front matter parsing (python-frontmatter)

### 5. Testing
Setup `tests/`:
- fixtures/ for sample data
- conftest.py for shared fixtures
- unit/, integration/, contract/ directories
```

---

### Milestones

- **Week 1 End**: AST nodes defined and tested; CLI scaffolding complete; config system loads and validates
- **Week 2 End**: Discovery scans files and orders them; document parsing extracts front matter; all unit tests passing with >80% coverage
- **Day 10 (EOD Friday)**: Integration tests verify end-to-end pipeline (load docs → parse → build AST); branch ready for review

---

## Constitution Check (Re-evaluated Post-Phase 1)

After Phase 1 design is complete, will reconvene to:
1. Ratify project constitution principles (e.g., "AST-centric", "deterministic builds", "plugin architecture")
2. Verify design complies with emerging principles
3. Document any deviations with justification

**Placeholder for Phase 1 gate approval**: Constitution principles to be established via `/speckit-constitution` command.

# Feature Specification: Project Foundation

**Feature Branch**: `001-project-foundation`  
**Created**: 2026-07-12  
**Status**: Draft  
**Input**: Initialize Markdown Book Builder project with core architecture, AST, and CLI foundation

## User Scenarios & Testing

### User Story 1 - Project Setup & Repository Initialization (Priority: P1)

As a developer, I want to initialize a new Markdown Book Builder project with all necessary tooling, configuration, and directory structure so that I can start building books immediately.

**Why this priority**: This is the foundation—without project setup, no other features can be tested or developed. Every developer starts here.

**Independent Test**: Can be fully tested by cloning the repo, running setup commands, and verifying the dev environment is functional with all tools available and passing.

**Acceptance Scenarios**:

1. **Given** a fresh clone of the repository, **When** I run `uv sync`, **Then** the virtual environment is created and all dependencies are installed
2. **Given** the installed environment, **When** I run `python -m markdown_book_builder --help`, **Then** the CLI is available and displays help
3. **Given** the installed environment, **When** I run linting/type-checking commands, **Then** the codebase passes all checks with no errors
4. **Given** the installed environment, **When** I run `pytest`, **Then** the test suite runs and reports coverage

---

### User Story 2 - Core AST Definition & Transformation (Priority: P1)

As a developer, I want to define the internal AST (Abstract Syntax Tree) representation that all processing stages operate on so that I have a stable, extensible data model for book transformations.

**Why this priority**: The AST is the central abstraction per the architecture. All plugins, validators, and exporters depend on it. Must be defined early to unblock downstream development.

**Independent Test**: Can be fully tested by creating AST instances, serializing/deserializing them, and verifying transformations apply correctly to the tree structure.

**Acceptance Scenarios**:

1. **Given** a Markdown document with headings, code blocks, and images, **When** I parse it into the AST, **Then** all content types are represented with correct hierarchy and metadata
2. **Given** an AST instance, **When** I serialize and deserialize it, **Then** the structure is preserved exactly (round-trip fidelity)
3. **Given** an AST with placeholder images, **When** I apply a transformation, **Then** the transformation correctly modifies nodes without corrupting the tree

---

### User Story 3 - Document Discovery & Ordering (Priority: P1)

As a user, I want the system to automatically discover and order Markdown files from a directory so that I can organize my book content naturally without manual configuration.

**Why this priority**: Document discovery is a mandatory first step in the pipeline. Without it, there's no input to process.

**Independent Test**: Can be fully tested by providing a sample directory structure, running discovery, and verifying the output is correctly ordered and includes all files.

**Acceptance Scenarios**:

1. **Given** a directory with Markdown files named `01-intro.md`, `02-chapter1.md`, `03-chapter2.md`, **When** discovery runs, **Then** files are returned in order and metadata is extracted
2. **Given** nested directories, **When** discovery runs, **Then** all Markdown files at any depth are found
3. **Given** files with front matter (YAML), **When** discovery runs, **Then** metadata is parsed and available for routing

---

### User Story 4 - CLI Command Structure (Priority: P1)

As a developer, I want a clean, extensible CLI with core commands (`build`, `validate`, `init`, `images`, `clean`, `config`) so that users have a consistent interface for all operations.

**Why this priority**: The CLI is the primary user interface. It must be usable and follow the Typer conventions established in the codebase from the start.

**Independent Test**: Can be fully tested by invoking each command with various arguments and verifying the output, exit codes, and behavior.

**Acceptance Scenarios**:

1. **Given** a valid markdown directory, **When** I run `build <path>`, **Then** the command executes and reports progress or errors clearly
2. **Given** an invalid or empty path, **When** I run any command with bad arguments, **Then** the CLI displays a helpful error message and returns non-zero exit code
3. **Given** the CLI, **When** I run `<command> --help`, **Then** clear documentation is shown for each command

---

### User Story 5 - Configuration System (Priority: P2)

As a user, I want to configure book builds via a TOML file so that I can specify output options, themes, and API keys without passing CLI flags every time.

**Why this priority**: Configuration enables reproducible builds and is required for Phase 1 but secondary to core AST and CLI scaffolding.

**Independent Test**: Can be fully tested by creating a `book.toml` config file, loading it, and verifying all settings are applied correctly to the build pipeline.

**Acceptance Scenarios**:

1. **Given** a `book.toml` file with valid settings, **When** I run build, **Then** settings from the config are applied
2. **Given** environment variables for secrets (e.g., `OPENAI_API_KEY`), **When** config loads, **Then** secrets are read from environment correctly
3. **Given** missing or invalid TOML, **When** config loads, **Then** a clear error is reported with line number

---

### User Story 6 - Testing Infrastructure & Golden Files (Priority: P2)

As a developer, I want a testing framework with fixtures, snapshot tests, and golden files in place so that I can write reliable tests for deterministic outputs.

**Why this priority**: Testing infrastructure is essential for reproducibility but can be built alongside early features.

**Independent Test**: Can be fully tested by creating sample tests, running the test suite, and verifying coverage reports and snapshot capture/comparison.

**Acceptance Scenarios**:

1. **Given** test fixtures for sample documents, **When** I run pytest, **Then** fixtures are available and reusable
2. **Given** a transformation, **When** I run a snapshot test, **Then** the output is captured on first run and compared on subsequent runs
3. **Given** golden files in `tests/fixtures/golden/`, **When** tests run, **Then** outputs are compared against golden files correctly

---

### Edge Cases

- What happens when a Markdown file is empty or contains only front matter?
- How does the AST handle deeply nested content (10+ levels of headers)?
- What happens when the TOML config is missing required fields?
- How does the CLI behave when input directory doesn't exist?
- Can the system handle filenames with special characters or unicode?

## Requirements

### Functional Requirements

- **FR-001**: System MUST initialize a valid Python project with `uv` virtual environment and dependencies installed correctly
- **FR-002**: System MUST define an AST data model using Pydantic that represents book structure (chapters, sections, images, code blocks, metadata)
- **FR-003**: System MUST discover all Markdown files recursively from a given directory and extract front matter metadata
- **FR-004**: System MUST support ordering files by filename (lexicographic) or explicit ordering metadata
- **FR-005**: System MUST provide a CLI built with Typer supporting `build`, `validate`, `init`, `images`, `clean`, `config` commands
- **FR-006**: System MUST load configuration from a `book.toml` file with environment variable overrides for secrets
- **FR-007**: System MUST return non-zero exit codes on errors and display machine-readable error reports
- **FR-008**: System MUST provide comprehensive test fixtures and golden file infrastructure for deterministic testing
- **FR-009**: System MUST enforce code quality standards via Ruff linting and mypy type checking with pre-commit hooks
- **FR-010**: System MUST support Python 3.13 only; all code must be compatible with this version

### Key Entities

- **Book**: Top-level entity representing the complete book; contains metadata (title, author, version) and chapters
- **Chapter**: Container for sections and content; has metadata like chapter number and title
- **Section**: Subsection of a chapter; contains paragraphs, code blocks, and images
- **Image**: Placeholder or embedded image with metadata (caption, alt text, size)
- **CodeBlock**: Syntax-highlighted code with language, caption, and line numbers
- **Front Matter**: YAML metadata at the start of Markdown files

## Success Criteria

### Measurable Outcomes

- **SC-001**: All test suite passes with >80% code coverage on core modules (AST, discovery, CLI)
- **SC-002**: CLI responds to `--help` within <100ms and displays accurate documentation
- **SC-003**: Document discovery completes for 100+ files within <1 second
- **SC-004**: A sample book with 10+ chapters can be initialized, validated, and all checks pass
- **SC-005**: Configuration loading succeeds with valid TOML in <50ms; invalid configs fail with clear error messages within <100ms
- **SC-006**: Developers can set up the project with `uv sync` and have all linting/typing tools ready in <2 minutes
- **SC-007**: AST serialization/deserialization is lossless (round-trip fidelity 100%)

## Assumptions

- **Target Python**: Python 3.13 (specified in CLAUDE.md and PRD)
- **Development Environment**: macOS, Linux, and Windows support via `uv` and platform-agnostic Python
- **Dependency Management**: `uv` is the primary package manager; no Poetry/pip workflows
- **CLI Framework**: Typer is used for all CLI commands (standard in this project)
- **Configuration Format**: TOML is the primary format; environment variables override config for secrets
- **Testing**: pytest is the test framework; pytest-watch for local development
- **Code Quality**: Ruff for linting/formatting, mypy for static type checking with strict mode
- **Git & Version Control**: Feature branches follow SpecKit conventions; ADRs document architectural decisions
- **Reproducibility**: All builds are deterministic; caching strategy TBD in Phase 3
- **Scope Boundaries**: Phase 1 does NOT include Mermaid rendering, image generation, or Typst export (these are Phase 3–4)
- **No External Build System**: Builds are pure Python; Pandoc + Typst optional in later phases
- **Documentation**: ADRs live in `docs/adr/` and are referenced in CLAUDE.md
- **Project Layout**: Package lives under `src/` directory following src-layout convention: `src/markdown_book_builder/` with separate `tests/` at repo root

---

## Clarifications

### Session 2026-07-13

- Q: Package location (root-level vs src-layout)? → A: Package lives under `src/markdown_book_builder/` (src-layout convention)
- Q: Pre-commit hook validation? → A: Add explicit task to validate pre-commit hooks execute correctly
- Q: Coverage scope specificity? → A: T028 validates core modules only (`markdown_book_builder/{ast_,cli,discovery}`); T077 validates entire codebase
- Q: Edge case coverage? → A: Add tests for deeply nested content (10+ heading levels) and invalid TOML error scenarios
- Q: Sample book validation? → A: Final validation task (T078) includes end-to-end pipeline with 10+ chapter sample book

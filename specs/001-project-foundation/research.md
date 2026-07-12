# Phase 0 Research: Project Foundation Technical Decisions

**Date**: 2026-07-12  
**Status**: Complete  
**Branch**: `001-project-foundation`

---

## Research Summary

Phase 0 investigated 5 key technical areas to establish the foundation for all downstream development:
1. Core AST (Abstract Syntax Tree) data model design
2. Markdown parsing + front matter extraction
3. CLI command structure and patterns
4. Configuration loading system
5. Testing infrastructure and patterns

All unknowns from the technical context have been resolved through research into industry best practices and established Python ecosystem patterns.

---

## 1. Core AST Design: Discriminated Union Pattern

### Decision
Use **Pydantic BaseModel with discriminated unions** for the AST. Each node type (Text, CodeBlock, Image, Paragraph, Section, Chapter, Book) is a Pydantic model with a `type` field acting as a discriminator.

### Rationale
- **Type Safety**: Pydantic validates at construction; invalid trees never exist
- **Self-Reference**: Forward annotations + `model_rebuild()` enable recursive hierarchies
- **Round-Trip Fidelity**: Native JSON serialization with 100% structure preservation
- **Extensibility**: Plugin registry pattern allows dynamic node type registration (future diagram renderers, exporters)
- **Visitor Pattern**: Transformations (image generation, diagram rendering, validation) use visitor pattern—clean separation of concerns
- **Performance**: Pydantic v2 uses Rust-backed validation (~100x faster than v1); supports 1000+ node trees

### Key Entities
```
Book (root)
├── Chapter[]
    ├── Section[] | Paragraph | CodeBlock | Image
        ├── Section[] (nested)
        ├── Paragraph[]
        │   └── Text | CodeBlock | Image
        └── CodeBlock | Image
```

### Validation Rules Per Node Type
- **Text**: Non-empty content
- **CodeBlock**: Language field constrained to known syntaxes (extensible via plugin registry)
- **Image**: Relative paths only (no absolute paths); alt_text required; dimensions use standard units (%, px, em, cm, in)
- **Section**: Heading levels 1–6; nested sections must have higher level than parent
- **Chapter**: Optional metadata dict (for front matter data)

### Serialization Strategy
- Dump with `exclude_none=False` to preserve all field values
- Discriminator field (`type`) always present for re-parsing
- Custom serializers for platform normalization (line endings, path separators)
- Streaming deserialization for large books (100+ chapters)

### Alternatives Considered & Rejected
- **Flat node list + parent refs**: Slower traversal, harder to validate, cyclic reference complexity
- **Abstract base class hierarchy**: Verbose, harder to extend, discriminator manual
- **TypedDict unions**: No validation, not extensible
- **SQLAlchemy ORM**: Overkill without persistence requirement

### Estimated Performance
- Parse 1000-node tree: 50–100ms
- Serialize to JSON: 20–50ms
- Full round-trip: 100–150ms
- Caching strategy: Deterministic tree hashing for incremental builds

---

## 2. Markdown Parsing: `python-frontmatter` + `markdown-it-py`

### Decision
Use **`python-frontmatter`** for reliable YAML front matter extraction combined with **`markdown-it-py`** (CommonMark-compliant) for AST generation with preserved line numbers.

### Rationale
- **Front Matter**: `python-frontmatter` is spec-compliant (Jekyll convention), handles all edge cases (missing frontmatter, empty YAML, unicode, special characters)
- **Markdown Parsing**: `markdown-it-py` provides CommonMark-compliant AST; tokens include line number mapping (`token.map[start_line, end_line]`)
- **Error Reporting**: Line numbers enable precise error messages ("metadata error on line 5")
- **Extensibility**: `mdit-py-plugins` adds extended syntax (tables, footnotes, task lists)
- **Regex Pitfalls Avoided**: Naive regex fails on triple-dash delimiters in code blocks, multiline YAML values, unicode detection

### Edge Cases Handled
1. **No front matter**: Returns empty metadata dict (safe, no crash)
2. **Empty files**: Graceful handling
3. **Unicode & special characters**: UTF-8 fully supported via PyYAML's safe loading
4. **Triple-dash in code block**: `python-frontmatter` correctly distinguishes front matter delimiters from content
5. **Custom metadata**: Ordering via explicit `order` field, sorted by filename as fallback
6. **Line number tracking**: Custom mapping layer attaches source line numbers to AST tokens

### Dependencies
- `python-frontmatter>=1.0.0`
- `markdown-it-py>=3.0.0`
- `mdit-py-plugins>=0.4.0`
- `pyyaml>=6.0` (via frontmatter)

### Alternatives Considered & Rejected
- **Regex-only**: Fragile edge cases, no YAML validation, unicode bugs
- **Raw PyYAML + regex**: Still fragile delimiter detection
- **TOML front matter**: Non-standard (Markdown convention is YAML)
- **Pandoc subprocess**: External dependency, subprocess overhead, harder to integrate

### Discovery & Ordering
- Recursive scan of directory for `*.md` files
- Parse front matter to extract `order` metadata
- Sort by `(order, filename)` tuple for deterministic ordering
- Fast (<1s for 100+ files)

---

## 3. CLI Design: Hierarchical Command Groups

### Decision
Use **Typer with modular command structure**: separate file per command, command groups in subdirectories. Root callback initializes shared state (config, logging). Context object carries state between root and commands.

### Rationale
- **Modularity**: Each command has single responsibility; easy to test independently
- **Scalability**: Nested `add_typer()` composition allows unlimited command groups without modifying root
- **Context Sharing**: Root callback runs before any command; stores config/logger in `ctx.obj` (type-safe dict)
- **Error Handling**: Custom `Exit` subclasses with explicit exit codes (0=success, 1=runtime error, 2=usage error)
- **Extensibility**: Plugin architecture can register new command groups dynamically

### Command Structure
```
markdown-book-builder [OPTIONS] COMMAND [ARGS]
├── build <path>                    # Build book from markdown
├── validate <path>                 # Validate book structure
├── init <path>                     # Initialize new book
├── config COMMAND [ARGS]           # Configuration management
│   ├── show                        # Display current config
│   └── set <key> <value>           # Set config value
├── images COMMAND [ARGS]           # Image & diagram management
│   ├── clean                       # Clear image cache
│   ├── generate <prompts>...       # Generate images from prompts
│   └── list                        # List cached images
```

### Error Handling Strategy
- **Exit codes**: 0 (success), 1 (runtime errors), 2 (usage errors), 130 (Ctrl+C)
- **Machine-readable errors**: JSON output via `--output-format json` (future)
- **Help text**: Auto-generated from docstrings and type hints; `show_envvar=False` hides secrets

### Environment Variables
- Root-level options (e.g., `--config`) support env var fallback (`envvar="MBB_CONFIG"`)
- Secrets like `OPENAI_API_KEY` never displayed in `--help` (flagged with `show_envvar=False`)
- CLI args override env vars (user intent first)

### File Structure
```
markdown_book_builder/cli/
├── main.py              # Root app + root callback
├── build.py             # `build` command
├── validate.py          # `validate` command
├── init.py              # `init` command
├── config/
│   ├── __init__.py      # `config` command group + `config show`
│   └── set.py           # `config set` command
├── images/
│   ├── __init__.py      # `images` command group
│   ├── clean.py         # `images clean` command
│   ├── generate.py      # `images generate` command
│   └── list.py          # `images list` command
└── error_handlers.py    # Custom Exit subclasses
```

### Alternatives Considered & Rejected
- **Flat structure (all commands at root)**: Namespace pollution (`images_clean` vs `images clean`), doesn't scale beyond 10 commands
- **Click directly**: More verbose, less Pythonic; Typer is superior for type-hint integration
- **Monolithic CLI object**: Single file grows to 500+ lines; violates separation of concerns

---

## 4. Configuration System: Pydantic Settings + tomllib

### Decision
Use **Pydantic Settings with tomllib** (native Python 3.13). Schema defined via Pydantic models; TOML parsed with built-in `tomllib`; environment variables override TOML values.

### Rationale
- **No External Dependencies**: `tomllib` is built-in (Python 3.13); no `tomli` backport needed
- **Validation**: Pydantic validates required fields, types, and constraints
- **Error Reporting**: TOML syntax errors include line:column info; validation errors list all field failures
- **Environment Overrides**: Pydantic Settings `env_prefix` + `env_nested_delimiter` handles precedence automatically
- **Extensibility**: Nested Pydantic models (`OpenAIConfig`) make adding new sections trivial

### Configuration Precedence (Highest → Lowest)
1. Environment variables (`OPENAI_API_KEY`, `BOOK__SOURCE_DIR`)
2. TOML file (`book.toml`)
3. Field defaults (Pydantic model)

### Config Schema
```python
class BookConfig(BaseSettings):
    title: str              # Required
    author: str             # Required
    version: str = "1.0.0"
    source_dir: Path = Path("./chapters")
    output_dir: Path = Path("./dist")
    openai: OpenAIConfig    # Nested section
```

### Example `book.toml`
```toml
[book]
title = "Building with Python"
author = "Jane Doe"
version = "1.0.0"
source_dir = "~/books/my-book/chapters"
output_dir = "./dist"

[openai]
model = "gpt-4-turbo"
```

### Error Messages
- **Missing required field**: `validation failed: title: Field required`
- **Invalid TOML syntax**: `book.toml:2 - Invalid TOML syntax: Unterminated string`
- **Invalid type**: `version: Input should be a valid string`

### File Discovery
- Explicit `--config` flag or `$MBB_CONFIG` env var
- Auto-discovery: Search current directory up parent directories (stop at 5 levels or filesystem root)
- Clear error if `book.toml` not found

### Secrets Management
- Sensitive values (API keys) loaded from environment variables only
- Never committed to version control
- `.env` file support for development (via `env_file` in Pydantic Settings)

### Dependencies
- `pydantic>=2.0` (already required)
- `pydantic-settings>=2.0` (separate package)
- `tomli>=2.0` for Python <3.11 (via conditional in pyproject.toml)

### Alternatives Considered & Rejected
- **YAML + python-dotenv**: YAML is ambiguous (yes/no → bool); less explicit than TOML
- **Pydantic BaseSettings without TOML**: No file support; harder to distribute config templates
- **tomlkit (style-preserving)**: Overkill—used for editing; unnecessary 20x slowdown
- **toml (pure Python)**: Outdated (2020); replaced by tomllib

---

## 5. Testing Infrastructure: Pytest Patterns

### Decision
Use **Syrupy for snapshots**, **golden files with checksums** for integration tests, **parametrized tests** for edge cases, **80%+ code coverage threshold** enforced in CI.

### Rationale
- **Snapshots (Syrupy)**: Zero-dependency, human-readable `.ambr` format, diff-friendly, perfect for AST validation
- **Golden Files**: Prove deterministic builds (same input → identical output, verified via SHA256)
- **Parametrization**: DRY test code; stacked parametrization covers combinatorial variants
- **Coverage Threshold**: 80%+ prevents regression; `pytest-cov` with `--fail-under=80` in CI
- **Determinism**: No flaky tests—mock external APIs, use temporary directories, seed randomness

### Test Organization
```
tests/
├── conftest.py              # Shared fixtures
├── unit/
│   ├── test_ast_models.py
│   ├── test_discovery.py
│   ├── test_config.py
│   └── test_cli.py
├── integration/
│   ├── test_book_build_pipeline.py
│   └── test_golden_files.py  # Determinism validation
├── contract/
│   └── test_cli_interface.py  # CLI contract tests
└── fixtures/
    ├── sample_markdown/
    ├── sample_configs/
    └── golden/                # Expected outputs
```

### Fixture Patterns
- **Factory fixtures**: Return callables for fresh data on demand (prevents cross-test pollution)
- **Yield fixtures**: Always use `yield` over `return` for guaranteed cleanup
- **Parametrized fixtures**: Test multiple configurations without duplication

### Snapshot Testing (Syrupy)
```python
def test_ast_generation(snapshot):
    doc = parse_markdown("# Title\nBody")
    assert doc.ast == snapshot
```
- Snapshots stored in `__snapshots__/` adjacent to test files
- Human-readable YAML-like `.ambr` format
- Update via `pytest --snapshot-update` (review diff before commit)
- Exclude dynamic content (timestamps, hashes) via `exclude` parameter

### Golden File Testing
- Store expected outputs (TOC, metadata) in `tests/fixtures/golden/`
- Compare via checksums (SHA256) for PDFs (binaries not version-controlled)
- Prove determinism: build twice, verify checksums match
- Update workflow documented in CONTRIBUTING.md

### Coverage Configuration
- Target: **80%+ branch coverage** on core modules (AST, discovery, CLI, config)
- Enforce via `pytest-cov --fail-under=80` in CI
- Higher targets (90%+) for high-risk modules; lower (70%+) acceptable for scripts
- `coverage html` generates detailed reports per file

### Markers for Test Selection
```ini
[pytest]
markers =
    unit: Unit tests (fast, <100ms)
    integration: Integration tests (may call mocked APIs)
    contract: Contract/interface tests
    slow: Slow tests (>1s)
    flaky: Known-flaky tests (skip by default)
```

### Avoiding Flaky Tests
1. **No timestamps in assertions**: Use `is not None` checks instead
2. **Mock external APIs**: No real OpenAI calls in tests
3. **Use temporary directories**: Via `tmp_path` fixture; auto-cleanup
4. **Seed randomness**: `random.seed(42)` in fixtures
5. **Deterministic ordering**: Sort collections before comparison

### Dependencies
- `pytest>=7.0`
- `pytest-cov>=4.0`
- `syrupy>=4.0` (snapshot testing)
- `pytest-watch` (optional, for local watch mode)

### Alternatives Considered & Rejected
- **pytest-snapshot**: Heavier than Syrupy; one file per snapshot
- **Manual golden files**: Verbose, no diff generation
- **No snapshots/golden files**: Brittle, hard to detect regressions

---

## Implementation Sequence (Phases 1–2)

### Phase 1: Core Foundation (Weeks 1–3)
1. **AST Nodes & Validation** (Week 1)
   - Implement all Pydantic models (Text, CodeBlock, Image, Paragraph, Section, Chapter, Book)
   - Test round-trip serialization
   - Validate edge cases (empty files, unicode, deeply nested content)

2. **CLI Scaffolding** (Week 1–2)
   - Create Typer app structure (main.py, command modules)
   - Implement `--help`, `--version`, error handling
   - Root callback for config/logging initialization
   - Test command parsing and error messages

3. **Configuration System** (Week 2)
   - Pydantic Settings schema
   - TOML loader with error reporting
   - Environment variable precedence
   - Test invalid TOML, missing fields, type errors

4. **Document Discovery & Parsing** (Week 2–3)
   - Markdown parser (python-frontmatter + markdown-it-py)
   - Front matter extraction
   - File ordering (explicit + filename-based)
   - Test edge cases (no frontmatter, unicode, special characters)

5. **Testing Infrastructure** (Week 3)
   - Test fixtures (sample docs, configs, AST instances)
   - pytest configuration (markers, coverage thresholds)
   - Snapshot testing setup (Syrupy)
   - Golden file strategy

### Phase 2: Plugin & Transformation System (Weeks 4–5)
1. **Visitor Pattern & Transformations**
   - Implement `ASTTransformer` base class
   - Visitor pattern for plugins
   - Test on 100+ chapter books

2. **First Plugin: Document Discovery**
   - Scan directory, order files
   - Return fully-formed `Book` AST

3. **Integration Testing**
   - End-to-end pipeline tests
   - Determinism validation (golden files)
   - Performance benchmarks

---

## Resolved Unknowns

| Unknown | Resolution |
|---------|------------|
| AST design pattern | Discriminated union with Pydantic |
| Round-trip fidelity | JSON serialization with Pydantic (100% preservation) |
| Markdown parsing library | `python-frontmatter` + `markdown-it-py` |
| CLI framework | Typer with modular command groups |
| Config file format | TOML with Pydantic Settings |
| Environment overrides | Pydantic Settings `env_prefix` |
| Testing strategy | Syrupy snapshots + golden files + 80%+ coverage |
| Plugin extensibility | Visitor pattern + dynamic registry |
| Performance targets | 50–100ms for 1000-node tree parse/serialize |

---

## Next Steps: Phase 1 Design

See `/specs/001-project-foundation/plan.md` (Phase 1 section) for detailed:
- Data model definitions
- CLI command specifications
- Configuration schema
- Testing checklist
- Repository structure

All technical decisions are now finalized and ready for implementation.

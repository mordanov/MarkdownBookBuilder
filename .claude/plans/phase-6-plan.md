# Phase 6 Implementation Plan: Full CLI Commands Integration (T045-T054)

## Overview
Phase 6 integrates the document discovery, AST building, and configuration systems into fully functional CLI commands that users can run end-to-end.

## Tasks (T045-T054)

### T045: Enhance build command
**File**: `src/markdown_book_builder/cli/build.py`
**Goal**: Implement full build pipeline

```python
def build(path: str) -> None:
    """Build a book from Markdown source directory."""
    # 1. Load config
    # 2. Discover documents
    # 3. Build AST
    # 4. Export (stub for now)
    # 5. Report results
```

### T046: Enhance validate command
**File**: `src/markdown_book_builder/cli/validate.py`
**Goal**: Validate book structure and configuration

```python
def validate(path: str) -> None:
    """Validate book structure and configuration."""
    # 1. Load config
    # 2. Discover documents
    # 3. Build AST
    # 4. Validate schema
    # 5. Report issues
```

### T047: Enhance init command
**File**: `src/markdown_book_builder/cli/init.py`
**Goal**: Initialize new book project with samples

```python
def init(path: str) -> None:
    """Initialize new book project."""
    # 1. Create directory
    # 2. Create book.toml
    # 3. Create content/ with sample files
    # 4. Create order.yaml template
    # 5. Create README
```

### T048: Config command with export
**File**: `src/markdown_book_builder/cli/config.py`
**Goal**: Show and export configuration

```python
def config(path: str) -> None:
    """Display configuration."""
    # Load and pretty-print config
```

### T049: Images command subcommands
**File**: `src/markdown_book_builder/cli/images.py`
**Goal**: Image cache management

```python
def clean() -> None:
    """Clear image cache."""
```

### T050: Error handling & reporting
**Goal**: Consistent error messages and exit codes

- Use ConfigurationError, DiscoveryError, ValidationError
- Non-zero exit codes on failure
- Clear error messages to user

### T051-T052: Integration tests
**File**: `tests/integration/test_cli_*.py`
**Goal**: End-to-end CLI tests

- Build command integration tests
- Validate command integration tests
- Init command with sample generation
- Error scenarios

### T053: CLI help text
**Goal**: Comprehensive help documentation

- Docstrings for all commands
- Examples in help text
- Error message guidance

### T054: CLI polish
**Goal**: User experience refinement

- Progress messages
- Consistent formatting
- Clear success/failure reporting

## Implementation Order

1. **T045**: Update build command with discovery
2. **T046**: Update validate command
3. **T047**: Update init command with samples
4. **T048**: Config command polish
5. **T049**: Images subcommand
6. **T050**: Error handling standardization
7. **T051-T052**: Integration tests
8. **T053-T054**: Polish and documentation

## Key Integration Points

- Config loader → CLI entry point
- Document discovery → build pipeline
- AST builder → validation
- Error handling → consistent UX

## Success Criteria

- ✅ All CLI commands functional end-to-end
- ✅ Build command runs complete pipeline
- ✅ Validate command reports structure issues
- ✅ Init creates sample projects
- ✅ 15+ integration tests pass
- ✅ All error cases handled gracefully
- ✅ Ruff/mypy checks clean
- ✅ Help text comprehensive
# Phase 5 Implementation Plan: Document Discovery (T038-T044)

## Overview
Phase 5 implements document discovery: scanning Markdown files, extracting metadata, ordering chapters, and building the AST from file system sources.

## Tasks (T038-T044)

### T038: Document Scanner
**File**: `src/markdown_book_builder/discovery/scanner.py`
**Goal**: Recursively scan directories for Markdown files

```python
def scan_directory(path: Path) -> list[Path]:
    """Recursively find all .md files in order."""
    # Sorted by filename for determinism
    # Returns absolute paths

def get_files_in_order(source_dir: Path, order_file: Path | None = None) -> list[Path]:
    """Get Markdown files in correct order (from order.yaml or alphabetical)."""
```

### T039: Metadata Extraction
**File**: `src/markdown_book_builder/discovery/metadata.py`
**Goal**: Extract YAML front matter from Markdown files

```python
def extract_front_matter(content: str) -> tuple[dict[str, Any], str]:
    """Extract YAML front matter block and remaining content."""

def parse_markdown_metadata(path: Path) -> FrontMatter:
    """Read file and extract metadata."""
```

### T040: Chapter Ordering
**File**: `src/markdown_book_builder/discovery/ordering.py`
**Goal**: Determine chapter order from files or order.yaml

```python
def load_order_config(path: Path) -> list[str]:
    """Load chapter ordering from order.yaml."""

def sort_chapters(files: list[Path], order: list[str] | None = None) -> list[Path]:
    """Sort files according to order config or alphabetically."""
```

### T041: AST Builder
**File**: `src/markdown_book_builder/discovery/builder.py`
**Goal**: Convert discovered documents into AST

```python
def build_ast_from_files(files: list[Path], config: BookConfig) -> Book:
    """Convert Markdown files to Book AST."""

def parse_markdown_file(path: Path) -> Chapter:
    """Parse single Markdown file into Chapter AST."""
```

### T042: Discovery Service
**File**: `src/markdown_book_builder/discovery/__init__.py`
**Goal**: High-level API coordinating discovery

```python
def discover_book(source_dir: Path, config: BookConfig) -> Book:
    """Complete document discovery pipeline."""
```

### T043-T044: Tests
**File**: `tests/unit/test_discovery_*.py`
**Goal**: Comprehensive tests for all discovery components

- Scanner tests (nested dirs, sorting)
- Metadata extraction tests (front matter parsing)
- Ordering tests (order.yaml, alphabetical)
- AST builder tests (full pipeline)
- Integration tests (end-to-end discovery)

## Implementation Order

1. **T038**: Scanner - core file discovery
2. **T039**: Metadata - front matter extraction
3. **T040**: Ordering - chapter sequencing
4. **T041**: Builder - AST conversion
5. **T042**: Service - high-level API
6. **T043-T044**: Tests - validate all components

## Key Decisions

- **Deterministic**: Alphabetical sorting as default, order.yaml for custom
- **Front matter**: Standard YAML block (--- delimiters)
- **Chapter structure**: One file = one chapter, sections from headings
- **Error handling**: Validate file structure, report missing metadata

## Success Criteria

- ✅ Scan nested directory structures
- ✅ Extract YAML front matter correctly
- ✅ Support custom ordering via order.yaml
- ✅ Build complete AST from files
- ✅ All tests pass (20+ test cases)
- ✅ Ruff/mypy checks clean
# Testing Guide

This guide documents the testing strategy and practices for the Markdown Book Builder project.

## Testing Strategy

We use a **pyramid approach** with four layers of tests:

```
         🧪 Contract/CLI Tests (5%)
        ┌─────────────────────────┐
       ╱ Integration Tests (20%)  ╲
      ┌────────────────────────────┐
     ╱ Unit Tests (75%)            ╲
    └──────────────────────────────┘
```

### 1. Unit Tests (75% of tests)

**Purpose**: Test individual functions and classes in isolation

**Location**: `tests/unit/`

**What to test**:
- AST model validation
- Configuration parsing
- Document discovery
- Individual transformation functions
- Error handling

**Example**:
```python
# tests/unit/test_ast_models.py
import pytest
from markdown_book_builder.ast_.models import Document, Heading

def test_heading_model_validation():
    """Headings must have level 1-6."""
    valid = Heading(level=1, text="Title")
    assert valid.level == 1
    
    with pytest.raises(ValidationError):
        Heading(level=0, text="Invalid")

def test_document_title_required():
    """Documents must have a title."""
    with pytest.raises(ValidationError):
        Document(content=[])
```

**Markers**: `@pytest.mark.unit`

### 2. Integration Tests (20% of tests)

**Purpose**: Test interactions between modules and complete pipeline stages

**Location**: `tests/integration/`

**What to test**:
- Full discovery → parsing → AST transformation flow
- Configuration loading with multiple sources
- Plugin loading and execution
- End-to-end CLI commands (without actual file output)

**Example**:
```python
# tests/integration/test_discovery_to_ast.py
import pytest
from markdown_book_builder.discovery import scan_documents
from markdown_book_builder.parser import parse_to_ast

def test_discovery_parse_roundtrip(tmp_path):
    """Documents discovered can be parsed into valid AST."""
    # Create test markdown files
    (tmp_path / "01-intro.md").write_text("# Introduction\nContent here")
    (tmp_path / "02-main.md").write_text("# Main\nMore content")
    
    discovered = scan_documents(tmp_path)
    ast = parse_to_ast(discovered)
    
    assert len(ast.chapters) == 2
    assert ast.chapters[0].title == "Introduction"
```

**Markers**: `@pytest.mark.integration`

**Fixtures**: Use `tests/fixtures/` for test data (markdown samples, configs, etc.)

### 3. Contract Tests (5% of tests)

**Purpose**: Test CLI API and output format contracts

**Location**: `tests/contract/`

**What to test**:
- CLI command parsing and exit codes
- Output format (JSON structure, golden files)
- API stability across versions
- Error messages and logging

**Example**:
```python
# tests/contract/test_cli_commands.py
import pytest
from typer.testing import CliRunner
from markdown_book_builder.cli.main import app

runner = CliRunner()

def test_build_command_help():
    """Build command shows help."""
    result = runner.invoke(app, ["build", "--help"])
    assert result.exit_code == 0
    assert "Build a book from Markdown" in result.stdout

def test_validate_nonexistent_path():
    """Validate reports error for missing path."""
    result = runner.invoke(app, ["validate", "/nonexistent"])
    assert result.exit_code == 1
    assert "not found" in result.stdout.lower()
```

**Markers**: `@pytest.mark.contract`

### 4. Slow Tests (Optional)

**Purpose**: End-to-end tests with real file I/O, API calls, or rendering

**Location**: `tests/slow/`

**What to test**:
- Full build pipeline with real Pandoc/Typst
- Image generation with real OpenAI API (uses mocked responses)
- Large document performance

**Skip by default**: `pytest --ignore=tests/slow/`

**Markers**: `@pytest.mark.slow`

## Test File Organization

```
tests/
├── unit/
│   ├── test_ast_models.py         # AST node validation
│   ├── test_config_loader.py      # Configuration parsing
│   ├── test_discovery_scanner.py  # File discovery
│   └── test_transformations.py    # AST transformations
├── integration/
│   ├── test_discovery_to_ast.py   # Discovery → AST flow
│   ├── test_config_loading.py     # Config layer merging
│   ├── test_plugin_loading.py     # Plugin registration
│   └── test_build_pipeline.py     # Full pipeline stages
├── contract/
│   ├── test_cli_commands.py       # CLI parsing
│   ├── test_cli_outputs.py        # Output formats
│   └── test_api_stability.py      # API contracts
├── slow/
│   ├── test_full_build.py         # End-to-end builds
│   └── test_performance.py        # Timing benchmarks
├── fixtures/
│   ├── ast_samples.py             # Pre-built AST nodes
│   ├── markdown_samples.py        # Sample Markdown content
│   ├── config_samples.py          # Sample configurations
│   └── golden/
│       ├── book-simple.pdf        # Expected output
│       └── book-complex.pdf
└── conftest.py                    # Pytest configuration
```

## Fixtures and Test Data

### Built-in Fixtures

**conftest.py** provides reusable fixtures:

```python
@pytest.fixture
def sample_markdown_dir(tmp_path):
    """Create a temporary directory with sample markdown."""
    (tmp_path / "01-intro.md").write_text("# Introduction\nContent")
    (tmp_path / "02-main.md").write_text("# Main\nMore content")
    return tmp_path

@pytest.fixture
def sample_config():
    """Return a valid configuration."""
    return {
        "title": "Test Book",
        "author": "Test Author",
        "version": "1.0.0"
    }

@pytest.fixture
def sample_ast_document():
    """Return a valid AST document."""
    from markdown_book_builder.ast_.models import Document, Paragraph
    return Document(
        title="Test",
        content=[Paragraph(text="Hello world")]
    )
```

### Golden Files

For output validation, store expected outputs in `tests/fixtures/golden/`:

```python
def test_html_export_matches_golden(tmp_path):
    """HTML export matches golden file."""
    result = build_html("tests/fixtures/markdown_samples/simple", tmp_path)
    
    with open("tests/fixtures/golden/simple.html") as f:
        expected = f.read()
    
    assert result == expected
```

Update golden files with: `pytest --golden-update`

## Running Tests

### Basic Commands

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/unit/test_ast_models.py

# Run specific test
pytest tests/unit/test_ast_models.py::test_heading_model_validation

# Run by marker
pytest -m unit          # Only unit tests
pytest -m integration   # Only integration tests
pytest -m "not slow"    # Skip slow tests (default)
```

### Coverage

```bash
# Run tests with coverage report
pytest --cov=src --cov-report=html

# Coverage for specific module
pytest --cov=src/markdown_book_builder/ast_ tests/unit/

# Fail if coverage drops below 80%
pytest --cov=src --cov-fail-under=80
```

### Watch Mode

```bash
# Auto-run tests on file changes (requires pytest-watch)
ptw

# Watch with specific marker
ptw -- -m unit
```

## Test Best Practices

### 1. Use Clear Naming

```python
# ✅ Good: test name describes what is tested and expected outcome
def test_document_with_empty_content_raises_validation_error():
    pass

# ❌ Bad: vague name
def test_document():
    pass
```

### 2. Arrange-Act-Assert Pattern

```python
def test_config_merges_layers():
    # Arrange: Set up test data
    project_config = {"title": "Project"}
    env_config = {"output_path": "/tmp"}
    
    # Act: Perform the operation
    result = merge_configs(project_config, env_config)
    
    # Assert: Verify the result
    assert result["title"] == "Project"
    assert result["output_path"] == "/tmp"
```

### 3. One Assertion Per Test (Usually)

```python
# ✅ Good: Single assertion per test
def test_heading_level_validation():
    with pytest.raises(ValidationError):
        Heading(level=0)

def test_heading_accepts_level_1_to_6():
    for level in range(1, 7):
        h = Heading(level=level)
        assert h.level == level

# ❌ Avoid: Multiple unrelated assertions
def test_heading_model():
    h = Heading(level=1, text="Title")
    assert h.level == 1
    assert h.text == "Title"
    assert str(h) == "# Title"
    # ... more assertions
```

### 4. Mock External Dependencies

```python
import pytest
from unittest.mock import patch

def test_image_generation_api_call():
    """Image generation calls OpenAI API correctly."""
    with patch("openai.Image.create") as mock_create:
        mock_create.return_value = {"url": "http://..."}
        
        result = generate_image("A diagram")
        
        assert result == "http://..."
        mock_create.assert_called_once()
```

### 5. Use Parametrize for Multiple Cases

```python
@pytest.mark.parametrize("level,valid", [
    (0, False),
    (1, True),
    (6, True),
    (7, False),
])
def test_heading_level_bounds(level, valid):
    if valid:
        assert Heading(level=level)
    else:
        with pytest.raises(ValidationError):
            Heading(level=level)
```

### 6. Test Error Paths

```python
def test_config_loader_invalid_toml():
    """Config loader reports error for invalid TOML."""
    with pytest.raises(ConfigError) as exc_info:
        load_config("invalid: [toml")
    
    assert "TOML" in str(exc_info.value)
    assert "syntax" in str(exc_info.value).lower()
```

### 7. Use Fixtures for Setup

```python
@pytest.fixture
def markdown_book(tmp_path):
    """Create a test book with standard structure."""
    book_path = tmp_path / "book"
    book_path.mkdir()
    (book_path / "01-chapter.md").write_text("# Chapter 1\nContent")
    return book_path

def test_build_simple_book(markdown_book):
    """Build processes simple book correctly."""
    result = build(markdown_book)
    assert result.chapter_count == 1
```

## Performance Testing

For performance-sensitive code, use timers:

```python
def test_discovery_performance(benchmark):
    """Document discovery completes in <1 second."""
    def run():
        scan_documents("tests/fixtures/markdown_samples/")
    
    result = benchmark(run)
    assert result < 1.0  # seconds
```

## Continuous Integration

Tests run automatically on:
- Every commit (pre-commit hooks)
- Every pull request (GitHub Actions)
- Before releases

**Required** before merge:
- ✅ All tests pass: `pytest`
- ✅ Coverage above 80%: `pytest --cov`
- ✅ No lint issues: `ruff check .`
- ✅ Types pass: `mypy .`

## Debugging Tests

```bash
# Show print statements
pytest -s

# Drop into debugger on failure
pytest --pdb

# Stop after first failure
pytest -x

# Run last failed tests
pytest --lf

# Run failed tests first
pytest --ff
```

## Related Documentation

- [Architecture Decision Records](./adr/) - Design decisions
- [CONTRIBUTING.md](./CONTRIBUTING.md) - Development workflow
- [README.md](../README.md) - Quick start guide

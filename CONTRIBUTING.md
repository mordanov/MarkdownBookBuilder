# Contributing to Markdown Book Builder

Thank you for your interest in contributing! This guide will help you get started with development.

## Getting Started

### Prerequisites
- Python 3.13+
- Git
- Basic familiarity with the command line

### Development Setup

1. **Clone the repository**
```bash
git clone https://github.com/mordanov/MarkdownBookBuilder.git
cd MarkdownBookBuilder
```

2. **Install dependencies with uv**
```bash
uv sync
```

This installs all dependencies and creates a virtual environment in `.venv/`.

3. **Activate the virtual environment**
```bash
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows
```

4. **Verify setup**
```bash
python -m markdown_book_builder --help
pytest --version
ruff --version
mypy --version
```

All commands should work without errors.

## Development Workflow

### 1. Branch Naming Conventions

Use descriptive branch names following these patterns:

- **Features**: `feat/feature-name` (e.g., `feat/image-caching`)
- **Bug Fixes**: `fix/bug-description` (e.g., `fix/config-loading-error`)
- **Documentation**: `docs/documentation-topic` (e.g., `docs/cli-reference`)
- **Tests**: `test/test-description` (e.g., `test/performance-benchmarks`)
- **Refactoring**: `refactor/component-name` (e.g., `refactor/ast-traversal`)
- **Chores**: `chore/maintenance-task` (e.g., `chore/dependency-update`)

### 2. Working on Code

Create a new branch and make your changes:

```bash
# Create and switch to new branch
git checkout -b feat/your-feature-name

# Make your changes
# ... edit files ...

# Verify quality checks pass locally (see Quality Assurance below)
```

### 3. Committing Changes

Write clear, descriptive commit messages:

```bash
git add <files>
git commit -m "Brief description of what changed and why"
```

**Commit message guidelines:**
- Start with a verb: Add, Fix, Update, Refactor, Remove, etc.
- First line should be under 70 characters
- Add detailed explanation in body if needed
- Reference issue numbers if applicable (e.g., "Fixes #123")

**Example:**
```
Add image caching with SHA256 hash keys

Implement file-based image cache in .cache/images/ directory
to avoid regenerating identical images via OpenAI API.

- Use SHA256(prompt) as cache key
- Cache lookup is O(1)
- Graceful degradation without API key

Fixes #42
```

### 4. Push and Create Pull Request

```bash
# Push your branch to remote
git push -u origin feat/your-feature-name

# Create a pull request via GitHub CLI
gh pr create --title "Brief title" --body "Description of changes"

# Or use the GitHub web interface
```

## Code Quality Requirements

### All Contributions Must Pass

1. **Ruff Formatting** - Code must be auto-formatted
```bash
ruff format .
```

2. **Ruff Linting** - No linting errors
```bash
ruff check .
```

3. **mypy Type Checking** - Full type coverage with strict mode
```bash
mypy .
```

4. **pytest Testing** - All tests must pass
```bash
pytest
```

5. **Test Coverage** - Maintain >80% coverage on core modules
```bash
pytest --cov=src/ --cov-report=html
```

### Quick Verification Script

Run this before committing:

```bash
#!/bin/bash
set -e
echo "Formatting..."
ruff format .
echo "Linting..."
ruff check .
echo "Type checking..."
mypy .
echo "Running tests..."
pytest
echo "✅ All checks passed!"
```

## Testing Standards

### When to Write Tests

- **New features**: Unit tests are required before implementation
- **Bug fixes**: Add regression test that fails before fix, passes after
- **Refactoring**: Existing tests should continue to pass
- **Performance work**: Add benchmark tests to `tests/benchmarks/`

### Test Organization

```
tests/
├── unit/              # Unit tests for isolated components
├── integration/       # End-to-end CLI and workflow tests
├── benchmarks/        # Performance tests
└── fixtures/          # Reusable test data
```

### Writing Tests

Follow pytest conventions:

```python
def test_feature_description():
    """One-line description of what is being tested."""
    # Setup
    input_data = create_sample_data()
    
    # Execute
    result = function_under_test(input_data)
    
    # Assert
    assert result.expected_field == "expected_value"
```

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/unit/test_module.py

# Specific test function
pytest tests/unit/test_module.py::test_function_name

# With coverage
pytest --cov=src/ --cov-report=html

# With verbose output
pytest -v

# Watch mode (requires pytest-watch)
ptw
```

## Documentation Standards

### When to Document

- **Public APIs**: Docstrings required for all public functions
- **Complex logic**: Explain non-obvious design decisions
- **Configuration**: Update docs when adding new config options
- **CLI commands**: Help text should be clear and concise

### Docstring Format

Use NumPy-style docstrings:

```python
def traverse_ast(node: Any) -> Generator[Any]:
    """Traverse all nodes in an AST depth-first.
    
    Args:
        node: AST node to traverse (can be Book, Chapter, Section, etc.)
    
    Yields:
        Each node in the tree
    
    Raises:
        ValueError: If node is invalid
    """
```

### Documentation Files

- Update `docs/CLI.md` for CLI command changes
- Update `docs/TESTING.md` for testing changes
- Create ADRs in `docs/adr/` for architectural decisions
- Update README.md for major features

## Architecture & Design Decisions

### Core Principles

1. **AST-Based Pipeline** - All transformations operate on the central AST (see `docs/adr/001-ast-based-architecture.md`)
2. **Deterministic Builds** - Same input always produces identical output (see `docs/adr/003-deterministic-builds.md`)
3. **Layered Configuration** - Environment variables override TOML which overrides defaults (see `docs/adr/002-layered-configuration.md`)
4. **Image Caching** - Use hash-based file cache to avoid duplicate API calls (see `docs/adr/004-image-caching.md`)

### Before Making Architectural Changes

If your change affects the overall architecture:

1. Read the relevant ADRs in `docs/adr/`
2. Check if your change aligns with the current design
3. If you're proposing a major change, create an ADR first (see below)
4. Discuss in a GitHub issue before implementing

### Creating an ADR

If you're making a significant architectural decision:

1. Create `docs/adr/NNN-decision-title.md` (increment the number)
2. Use this template:

```markdown
# ADR NNN: Decision Title

## Status
Proposed/Accepted/Deprecated

## Context
Why this decision matters.

## Decision
What we decided to do.

## Rationale
Why this approach is better than alternatives.

## Consequences
Positive and negative effects of this decision.

## Alternatives Considered
Other options we looked at.
```

3. Link it from `docs/adr/README.md`
4. Get review before implementing

## Troubleshooting

If you run into issues during development:

### Environment Issues

**"Command not found: uv"**
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Virtual environment not activating**
```bash
# Recreate it
uv sync
source .venv/bin/activate
```

### Test Failures

**Tests pass locally but fail in CI**
- Check Python version: `python --version` (should be 3.13+)
- Check if tests require specific environment variables
- Run `pytest -v` for detailed output
- Check `pytest --cov` for coverage gaps

**Specific test failing**
```bash
# Run with verbose output
pytest tests/path/to/test.py::test_name -v

# Run with print statements visible
pytest tests/path/to/test.py::test_name -s

# Run with pdb debugger
pytest tests/path/to/test.py::test_name --pdb
```

### Code Quality Failures

**"ruff check" fails**
```bash
# Auto-fix most issues
ruff check . --fix

# Format code
ruff format .
```

**"mypy" type errors**
- Add type hints to your code
- Use `# type: ignore` as last resort (with a comment explaining why)
- Check `mypy --help` for strict mode options

### Documentation Issues

See `docs/TROUBLESHOOTING.md` for detailed troubleshooting guide.

## Review Process

### What to Expect

1. **Automated checks**: GitHub Actions runs tests, linting, type checking
2. **Code review**: A maintainer will review your code for:
   - Correctness and design
   - Test coverage and quality
   - Documentation completeness
   - Adherence to project conventions
3. **Changes requested**: Make updates and push new commits
4. **Approval & merge**: Once approved, your PR will be merged

### Getting Changes Approved Faster

- Follow the guidelines in this document
- Include tests with your changes
- Write clear commit messages
- Update relevant documentation
- Be responsive to review feedback

## Release Process

(For maintainers)

1. Update version in `src/markdown_book_builder/__init__.py`
2. Update CHANGELOG.md
3. Create git tag: `git tag v1.2.3`
4. Push tag: `git push origin v1.2.3`
5. GitHub Actions builds and publishes to PyPI

## Getting Help

- **Questions?** Check `docs/TROUBLESHOOTING.md` or existing issues
- **Bug found?** Create a GitHub issue with reproduction steps
- **Feature request?** Open an issue with use case and examples
- **Questions about architecture?** Read the ADRs in `docs/adr/`

## Thank You!

Your contributions help make Markdown Book Builder better for everyone. We appreciate your time and effort!

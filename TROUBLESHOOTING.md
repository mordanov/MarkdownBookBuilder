# Troubleshooting Guide

This guide addresses common issues when using Markdown Book Builder. If you don't find your issue here, check the [GitHub Issues](https://github.com/mordanov/MarkdownBookBuilder/issues) or create a new issue with details about your problem.

## Installation & Setup

### "Command not found: uv"

**Problem**: The `uv` package manager isn't installed or not in your PATH.

**Solution**:
```bash
# Install uv using the official installer
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH if needed
export PATH="$HOME/.local/bin:$PATH"

# Verify installation
uv --version
```

### "ModuleNotFoundError: No module named 'markdown_book_builder'"

**Problem**: The package isn't installed or the virtual environment isn't activated.

**Solution**:
```bash
# Ensure dependencies are installed
uv sync

# Activate the virtual environment
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows

# Verify the module can be imported
python -c "import markdown_book_builder; print(markdown_book_builder.__version__)"
```

### Virtual environment not activating

**Problem**: `source .venv/bin/activate` doesn't work or environment variables aren't set.

**Solution**:
```bash
# Recreate the virtual environment
rm -rf .venv

# Reinstall with uv
uv sync

# Activate it
source .venv/bin/activate

# Verify it's active (your prompt should show (.venv))
which python
```

### "Python 3.13 not found"

**Problem**: The installed Python version is older than 3.13.

**Solution**:
```bash
# Check your Python version
python --version

# If you need Python 3.13, install it
# macOS with Homebrew:
brew install python@3.13

# Or use pyenv for multiple Python versions:
pyenv install 3.13.0
pyenv local 3.13.0

# Verify it worked
python --version
```

## Configuration Issues

### "Cannot find config file: book.toml"

**Problem**: The `book.toml` configuration file is missing or in the wrong location.

**Solution**:
```bash
# The book.toml should be in your book's root directory
ls -la book.toml

# If it's missing, create a basic one:
python -m markdown_book_builder init /path/to/book
```

**Configuration file structure:**
```toml
[book]
title = "My Book Title"
author = "Your Name"
description = "Brief description"
language = "en"

[build]
output_dir = "output"
theme = "default"
```

### "Invalid configuration: missing required field 'title'"

**Problem**: The `book.toml` is missing required fields.

**Solution**: Ensure your `book.toml` has all required fields:
```toml
[book]
title = "Book Title"
author = "Author Name"
description = "Description"
```

### Environment variable not being read

**Problem**: Environment variables like `OPENAI_API_KEY` aren't being recognized.

**Solution**:
```bash
# Set environment variables before running the command
export OPENAI_API_KEY="sk-..."
export MARKDOWN_BOOK_BUILDER_CONFIG="/path/to/book.toml"

# Or set them inline
OPENAI_API_KEY="sk-..." python -m markdown_book_builder build .

# Verify the variable is set
echo $OPENAI_API_KEY
```

## API & Image Generation

### "Error: OpenAI API key not found"

**Problem**: The OpenAI API key isn't configured.

**Solution**:
```bash
# Set your API key
export OPENAI_API_KEY="sk-..."

# Or create a .env file (not committed to git):
echo "OPENAI_API_KEY=sk-..." > .env

# Load from .env (if your app supports it)
source .env
python -m markdown_book_builder build .
```

### "Error: 401 Unauthorized from OpenAI API"

**Problem**: The API key is invalid, expired, or doesn't have the right permissions.

**Solution**:
```bash
# Verify your API key
# 1. Go to https://platform.openai.com/account/api-keys
# 2. Confirm the key hasn't expired
# 3. Check that your account has credits/billing set up
# 4. Try a simple test:

curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer sk-..."

# If that fails, your key is invalid
# Generate a new one at the link above
```

### "Error: Rate limit exceeded"

**Problem**: Too many API requests to OpenAI in a short time.

**Solution**:
```bash
# Wait before retrying (rate limits reset after ~1 minute)
sleep 60

# For batch processing, add delays between requests
# Or use the image cache to avoid re-generating images

# Check your usage at https://platform.openai.com/account/usage
```

### "Image generation timeout"

**Problem**: OpenAI image generation is taking too long or timing out.

**Solution**:
```bash
# The default timeout is 30 seconds. For slower connections:
# Set a longer timeout (if configurable)
OPENAI_TIMEOUT=60 python -m markdown_book_builder build .

# Or try again - temporary API delays are common
# If consistently timing out, check OpenAI status
```

### "Image cache not being used"

**Problem**: Images are regenerated every build instead of using cached versions.

**Solution**:
```bash
# Verify the cache directory exists and is readable
ls -la .cache/images/

# Check if images are actually in the cache
find .cache/images -type f

# Clear cache if it's corrupted
rm -rf .cache/images/*

# Rebuild - new images will be cached
python -m markdown_book_builder build .
```

## Document Processing

### "Error: No markdown files found"

**Problem**: The builder can't find any `.md` files in the specified directory.

**Solution**:
```bash
# Verify markdown files exist
find . -name "*.md" -type f

# Check the directory structure
ls -la content/

# Ensure files have .md extension (not .markdown or .txt)
# If needed, rename files:
find . -name "*.markdown" -exec rename 's/.markdown$/.md/' {} \;
```

### "Error: Invalid markdown syntax in chapter X"

**Problem**: A markdown file has syntax that can't be parsed.

**Solution**:
```bash
# Run validation to find the exact issue
python -m markdown_book_builder validate .

# The output should show which file and line has the problem
# Common issues:
# - Unclosed code blocks (``` without closing `)
# - Invalid links: [text](url without quotes)
# - Malformed tables or lists
# - Invalid YAML frontmatter

# Fix the file and validate again
```

### "Markdown file is ignored or not processed"

**Problem**: A `.md` file exists but isn't included in the book.

**Solution**:
```bash
# Check the ordering file (if one exists)
cat order.yaml

# Verify the file is listed in order.yaml or the discovery system
# If not, add it:
python -m markdown_book_builder discover .

# Check if the file has proper metadata
head -20 content/chapter.md

# Required: filename should follow numbering pattern or be in order.yaml
```

### "Images in markdown not rendering in PDF"

**Problem**: Images display in markdown but not in the final PDF.

**Solution**:
```bash
# Verify image paths are relative to the markdown file
# ✅ Correct: ![alt](../images/diagram.png)
# ❌ Wrong: ![alt](/absolute/path/image.png)

# Check that image files exist
ls -la images/

# Ensure images are in supported format (PNG, JPG, SVG)
file images/*.png

# If using generated images, verify they were created
ls -la .cache/images/
```

## PDF Output Issues

### "Error: Pandoc not found"

**Problem**: Pandoc isn't installed or not in PATH.

**Solution**:
```bash
# Install Pandoc
# macOS with Homebrew:
brew install pandoc

# Linux (Ubuntu/Debian):
sudo apt-get install pandoc

# Or download from https://pandoc.org/installing.html

# Verify installation
pandoc --version
```

### "Error: Typst compilation failed"

**Problem**: The Typst template or syntax is invalid.

**Solution**:
```bash
# Check the Typst template for syntax errors
# Common issues:
# - Missing colons in key-value pairs
# - Unmatched braces or parentheses
# - Invalid unicode characters

# Test with a simpler template first
# Run validation to get detailed error:
python -m markdown_book_builder validate . --detailed

# Check Typst documentation: https://typst.app/docs/
```

### "PDF output is empty or has missing pages"

**Problem**: The generated PDF is incomplete or blank.

**Solution**:
```bash
# Check the build log for warnings
python -m markdown_book_builder build . --verbose

# Verify content files exist and have content
wc -l content/*.md

# Try building with a simpler configuration
# Start with just one chapter to isolate the issue

# If it's a specific chapter, check for unsupported markdown syntax
# or broken images in that chapter
```

### "PDF has incorrect styling or fonts"

**Problem**: The theme isn't applying correctly or fonts are wrong.

**Solution**:
```bash
# Verify the theme exists and is configured correctly
ls -la themes/

# Check book.toml for theme setting
grep -A5 "^\[build\]" book.toml

# Ensure theme files are valid
# Themes typically contain: template.typst or main.tex

# Test with default theme first
# Update book.toml:
# [build]
# theme = "default"

# Then rebuild
python -m markdown_book_builder build .
```

## Testing Issues

### "Tests fail locally but pass in CI"

**Problem**: Environment differences between local and CI.

**Solution**:
```bash
# Check Python version matches CI (should be 3.13+)
python --version

# Verify all dependencies are installed
uv sync

# Run tests with verbose output
pytest -v

# Check for environment-specific code or paths
grep -r "os.path.expanduser\|~/" src/tests/

# Ensure no hardcoded paths for macOS/Windows
# Use pathlib instead: Path.home() / "path"
```

### "pytest: command not found"

**Problem**: pytest isn't installed or the virtual environment isn't active.

**Solution**:
```bash
# Activate the virtual environment
source .venv/bin/activate

# Install test dependencies if needed
uv sync

# Try pytest again
pytest --version

# If still not found, install explicitly
pip install pytest
```

### "Test timeout or hangs indefinitely"

**Problem**: A test is stuck or takes too long.

**Solution**:
```bash
# Run tests with a timeout
pytest --timeout=10

# Find which test is slow
pytest -v --tb=short

# If a specific test hangs, run it alone
pytest tests/unit/test_module.py::test_hanging_test -v

# Add timeout decorator to the test:
import pytest

@pytest.mark.timeout(5)
def test_something():
    ...
```

## Code Quality Issues

### "ruff format fails with SyntaxError"

**Problem**: There's a syntax error in your Python code.

**Solution**:
```bash
# The error message should point to the file
# Fix the syntax error first

# Common issues:
# - Unclosed string or bracket
# - Invalid characters in variable names
# - Mismatched indentation

# Try running mypy to find the error
mypy .

# Once fixed, try ruff again
ruff format .
```

### "mypy reports type errors that seem wrong"

**Problem**: Type checking is too strict or missing type hints.

**Solution**:
```bash
# Add type hints to your code
def process_data(data: dict[str, Any]) -> str:
    return str(data)

# For third-party libraries without types:
pip install types-requests  # example for requests library

# Or use type: ignore (sparingly, with comment)
result = untyped_function()  # type: ignore[attr-defined]

# Check mypy configuration in pyproject.toml
cat pyproject.toml | grep -A10 "\[tool.mypy\]"
```

### "ruff check fails with import errors"

**Problem**: Ruff can't find imports or modules.

**Solution**:
```bash
# Ensure all dependencies are installed
uv sync
pip install -e .

# Check that the Python path includes the source directory
export PYTHONPATH="./src:$PYTHONPATH"

# Try ruff again
ruff check .

# If it's a third-party package, ensure it's installed
pip list | grep package-name
```

## Performance Issues

### "Build is very slow"

**Problem**: The build process takes a long time.

**Solution**:
```bash
# Profile the build to find the bottleneck
python -m markdown_book_builder build . --profile

# Common slow operations:
# 1. Image generation (use cache or pre-generate)
# 2. Large files (split into multiple files)
# 3. Pandoc/Typst rendering (reduce complexity)

# To speed up:
# - Check image cache is being used
# - Reduce markdown complexity temporarily for testing
# - Use a simpler theme or template
```

### "Memory usage is high during build"

**Problem**: The process uses too much RAM and may crash.

**Solution**:
```bash
# Check memory usage
python -m markdown_book_builder build . --memory-efficient

# Split large books into sections
# Process one chapter at a time if needed

# Clear cache to recover disk space
rm -rf .cache/

# Increase available memory (if on a system with constraints)
# Or use a system with more RAM for CI/CD builds
```

## Git & Version Control Issues

### "Accidentally committed sensitive data (API keys, passwords)"

**Problem**: Secrets were committed to git history.

**Solution**:
```bash
# Never push commits with secrets!
# If already pushed, revoke the secrets immediately

# To remove from local history (before pushing):
git reset HEAD~1  # Undo the commit
rm .env  # Remove the file
echo ".env" >> .gitignore  # Ignore it going forward
git add .gitignore
git commit -m "Remove secrets and add .env to gitignore"

# If accidentally pushed, the history is compromised
# Contact the maintainers immediately
```

### "Large files causing git issues"

**Problem**: Binary files or large artifacts are slowing down git.

**Solution**:
```bash
# Don't commit build artifacts, cache, or venv
# Ensure .gitignore includes:
.venv/
.cache/
output/
*.pyc
__pycache__/
dist/
build/
*.egg-info/

# If already committed, remove them:
git rm --cached large_file
git rm --cached -r .cache/
echo ".cache/" >> .gitignore
git commit -m "Remove cached files"
```

## Platform-Specific Issues

### macOS: "Code cannot be opened because it is from an unidentified developer"

**Problem**: Gatekeeper is blocking execution of compiled binaries.

**Solution**:
```bash
# Allow the file
sudo xattr -d com.apple.quarantine /path/to/binary

# Or use System Preferences → Security & Privacy
# Click "Open Anyway" when prompted
```

### Windows: "Command not recognized in PowerShell"

**Problem**: Scripts or commands don't work in PowerShell.

**Solution**:
```powershell
# Use Python directly instead of python-scripts
python -m markdown_book_builder build .

# Or use Command Prompt (cmd.exe) instead of PowerShell
# Activate venv:
.venv\Scripts\activate.bat

# Then run commands
python -m markdown_book_builder build .
```

### Linux: "Permission denied" when running scripts

**Problem**: Script files don't have execute permission.

**Solution**:
```bash
# Add execute permission
chmod +x script.sh

# Or run with python directly
python script.py
```

## Getting Help

If your issue isn't covered here:

1. **Check the [GitHub Issues](https://github.com/mordanov/MarkdownBookBuilder/issues)** - search for similar problems
2. **Read the [CONTRIBUTING.md](CONTRIBUTING.md)** - development guidelines
3. **Check the [README.md](README.md)** - quick start guide
4. **Create a new GitHub issue** with:
   - Your operating system and Python version
   - Exact command you ran
   - Full error message (if any)
   - Your `book.toml` configuration (sanitize secrets)
   - A minimal reproduction example

The maintainers are happy to help!

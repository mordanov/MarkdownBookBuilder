# Plugin Development Guide

This guide explains how to develop and integrate plugins into Markdown Book Builder. The plugin system provides extension points for diagram renderers, image providers, exporters, themes, and validation rules.

## Architecture Overview

The plugin system is built on top of the central AST (Abstract Syntax Tree) that all transformations operate on. Plugins hook into specific stages of the pipeline:

```
Document Discovery
       ↓
    AST Building
       ↓
  Plugin Transformations ← Your plugins hook here
       ↓
    Rendering
       ↓
    PDF Export
```

Each plugin operates on the AST and can:
- **Inspect** nodes to gather information
- **Transform** nodes to modify content
- **Generate** new nodes (e.g., images, diagrams)
- **Validate** nodes against custom rules

## Plugin Types

### 1. Diagram Renderers

Convert diagram syntax in markdown to images.

**Supported formats**:
- Mermaid (default)
- PlantUML
- Graphviz
- D2
- Draw.io

**Example**: A diagram plugin processes `mermaid` code blocks and generates PNG images.

### 2. Image Providers

Generate or fetch images on demand.

**Supported sources**:
- OpenAI DALL-E (default)
- Local image library
- External APIs (Unsplash, Pexels, etc.)

**Example**: An image plugin generates images from natural language descriptions in markdown.

### 3. Exporters

Convert the processed AST to different output formats.

**Supported formats**:
- PDF via Pandoc + Typst (default)
- LaTeX
- EPUB
- HTML
- DOCX

**Example**: An exporter plugin generates an EPUB version of the book.

### 4. Themes

Customize styling and visual appearance of the final output.

**Components**:
- Template files (Typst, LaTeX, HTML, etc.)
- CSS/styling definitions
- Font configuration
- Color schemes

**Example**: A theme plugin provides a custom design system for PDF rendering.

### 5. Validation Rules

Custom checks on document structure and content.

**Examples**:
- Enforce heading hierarchy (no h3 without h2)
- Check image alt text exists
- Validate code block language tags
- Require YAML frontmatter in chapters

## Creating a Plugin

### Step 1: Define the Plugin Interface

All plugins inherit from a base class and implement specific methods:

```python
from abc import ABC, abstractmethod
from typing import Any, Optional
from dataclasses import dataclass

@dataclass
class PluginConfig:
    """Base configuration for all plugins."""
    enabled: bool = True
    priority: int = 100  # Higher = executes later
    options: dict[str, Any] = None

class BasePlugin(ABC):
    """Base class for all plugins."""
    
    def __init__(self, config: PluginConfig):
        self.config = config
        self.options = config.options or {}
        self.enabled = config.enabled
    
    @abstractmethod
    def validate(self) -> bool:
        """Validate plugin configuration and dependencies."""
        pass
    
    @abstractmethod
    def initialize(self) -> None:
        """Initialize the plugin before processing starts."""
        pass
    
    @abstractmethod
    def process(self, ast_node: Any) -> Any:
        """Process an AST node and return modified node."""
        pass
    
    def cleanup(self) -> None:
        """Clean up resources after processing (optional)."""
        pass
```

### Step 2: Create Your Plugin Class

Implement one of the specific plugin types:

#### Diagram Renderer Plugin

```python
from pathlib import Path
from markdown_book_builder.plugins import DiagramRendererPlugin, PluginConfig

class CustomDiagramPlugin(DiagramRendererPlugin):
    """Example diagram renderer for custom diagram syntax."""
    
    DIAGRAM_TYPE = "custom"
    
    def __init__(self, config: PluginConfig):
        super().__init__(config)
        self.output_dir = Path(config.options.get("output_dir", ".cache/diagrams"))
    
    def validate(self) -> bool:
        """Check that required tools are available."""
        # Check if custom-diagram-tool is installed
        import subprocess
        try:
            subprocess.run(
                ["custom-diagram-tool", "--version"],
                capture_output=True,
                check=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def initialize(self) -> None:
        """Create output directory."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def process(self, ast_node: Any) -> Any:
        """Convert diagram node to image."""
        if ast_node.type != "code_block" or ast_node.language != self.DIAGRAM_TYPE:
            return ast_node
        
        # Generate diagram from source
        diagram_source = ast_node.content
        output_path = self.output_dir / f"{hash(diagram_source)}.png"
        
        if not output_path.exists():
            self._render_diagram(diagram_source, output_path)
        
        # Replace code block with image node
        return self._create_image_node(output_path, ast_node.metadata)
    
    def _render_diagram(self, source: str, output_path: Path) -> None:
        """Render diagram to image file."""
        import subprocess
        subprocess.run(
            ["custom-diagram-tool", source, "-o", str(output_path)],
            check=True
        )
    
    def _create_image_node(self, path: Path, metadata: dict) -> Any:
        """Create an image AST node."""
        from markdown_book_builder.ast import ImageNode
        return ImageNode(
            src=str(path),
            alt=metadata.get("caption", ""),
            title=metadata.get("title", "")
        )
```

#### Image Provider Plugin

```python
from markdown_book_builder.plugins import ImageProviderPlugin, PluginConfig
import hashlib
from pathlib import Path

class CustomImagePlugin(ImageProviderPlugin):
    """Example image provider for fetching images from external API."""
    
    def __init__(self, config: PluginConfig):
        super().__init__(config)
        self.api_key = config.options.get("api_key", "")
        self.cache_dir = Path(config.options.get("cache_dir", ".cache/images"))
    
    def validate(self) -> bool:
        """Check that API key is configured."""
        return bool(self.api_key)
    
    def initialize(self) -> None:
        """Create cache directory."""
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def process(self, ast_node: Any) -> Any:
        """Generate or fetch image based on node metadata."""
        if ast_node.type != "image_request":
            return ast_node
        
        description = ast_node.description
        cached_path = self._get_cache_path(description)
        
        if cached_path.exists():
            return self._create_image_node(cached_path, description)
        
        # Generate new image
        image_path = self._generate_image(description)
        return self._create_image_node(image_path, description)
    
    def _get_cache_path(self, description: str) -> Path:
        """Generate cache path based on description hash."""
        hash_key = hashlib.sha256(description.encode()).hexdigest()
        return self.cache_dir / f"{hash_key}.png"
    
    def _generate_image(self, description: str) -> Path:
        """Call external API to generate image."""
        import requests
        
        response = requests.post(
            "https://api.example.com/generate",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"description": description}
        )
        response.raise_for_status()
        
        image_url = response.json()["image_url"]
        cached_path = self._get_cache_path(description)
        
        # Download and cache
        image_response = requests.get(image_url)
        cached_path.write_bytes(image_response.content)
        
        return cached_path
    
    def _create_image_node(self, path: Path, description: str) -> Any:
        """Create an image AST node."""
        from markdown_book_builder.ast import ImageNode
        return ImageNode(
            src=str(path),
            alt=description,
            title=""
        )
```

#### Validation Rule Plugin

```python
from markdown_book_builder.plugins import ValidationPlugin, PluginConfig

class HeadingHierarchyPlugin(ValidationPlugin):
    """Validate proper heading hierarchy in chapters."""
    
    def __init__(self, config: PluginConfig):
        super().__init__(config)
        self.errors = []
    
    def validate(self) -> bool:
        """This validation plugin always initializes."""
        return True
    
    def initialize(self) -> None:
        """Reset error list."""
        self.errors = []
    
    def process(self, ast_node: Any) -> Any:
        """Check heading hierarchy."""
        if ast_node.type == "chapter":
            self._validate_chapter(ast_node)
        return ast_node
    
    def _validate_chapter(self, chapter: Any) -> None:
        """Ensure headings follow proper hierarchy."""
        headings = self._extract_headings(chapter)
        
        for i, heading in enumerate(headings):
            if i == 0:
                # First heading should be h1 or h2
                if heading["level"] not in [1, 2]:
                    self.errors.append(
                        f"First heading in {chapter.metadata['source']} is h{heading['level']}, "
                        f"should be h1 or h2"
                    )
            else:
                prev_level = headings[i-1]["level"]
                curr_level = heading["level"]
                
                # Can't skip heading levels
                if curr_level > prev_level + 1:
                    self.errors.append(
                        f"Heading hierarchy skip in {chapter.metadata['source']}: "
                        f"h{prev_level} followed by h{curr_level}"
                    )
    
    def _extract_headings(self, node: Any) -> list[dict]:
        """Extract all headings from node."""
        headings = []
        
        def traverse(n):
            if n.type == "heading":
                headings.append({
                    "level": n.level,
                    "content": n.content
                })
            for child in getattr(n, "children", []):
                traverse(child)
        
        traverse(node)
        return headings
    
    def get_errors(self) -> list[str]:
        """Return validation errors."""
        return self.errors
```

### Step 3: Register Your Plugin

Create a plugin manifest file that tells the system about your plugin:

**`my_plugin/plugin.toml`:**
```toml
[plugin]
name = "My Custom Plugin"
version = "1.0.0"
author = "Your Name"
description = "Description of what this plugin does"
type = "diagram_renderer"  # or image_provider, exporter, theme, validator
python_module = "my_plugin.main"
python_class = "CustomDiagramPlugin"

[plugin.requirements]
# External dependencies
custom-diagram-tool = ">=2.0.0"

[plugin.configuration]
# Default configuration
output_dir = ".cache/diagrams"
quality = "high"

[plugin.metadata]
# Plugin-specific metadata
supported_formats = ["png", "svg"]
dependencies = []
```

### Step 4: Install Your Plugin

Place your plugin in one of these locations:

```
Option 1: User plugins (system-wide)
~/.markdown_book_builder/plugins/my_plugin/

Option 2: Project plugins (per book)
./plugins/my_plugin/

Option 3: Via pip package
pip install my-markdown-book-plugin
```

### Step 5: Enable in Configuration

Add to your `book.toml`:

```toml
[plugins]
# Enable built-in plugins
diagram_renderer = { enabled = true, type = "mermaid" }
image_provider = { enabled = true, type = "openai" }

# Enable custom plugin
[plugins.my_custom_plugin]
enabled = true
type = "diagram_renderer"
output_dir = ".cache/custom_diagrams"
quality = "high"
```

Or configure via environment variables:

```bash
export MARKDOWN_BOOK_BUILDER_PLUGINS_MY_CUSTOM_PLUGIN_ENABLED=true
export MARKDOWN_BOOK_BUILDER_PLUGINS_MY_CUSTOM_PLUGIN_OUTPUT_DIR=".cache/diagrams"
```

## Plugin Development Checklist

- [ ] Create plugin class inheriting from appropriate base class
- [ ] Implement all required abstract methods
- [ ] Add comprehensive docstrings
- [ ] Create `plugin.toml` manifest
- [ ] Write unit tests in `tests/plugins/test_my_plugin.py`
- [ ] Add integration test in `tests/integration/test_plugin_integration.py`
- [ ] Handle errors gracefully with informative messages
- [ ] Add logging for debugging
- [ ] Document configuration options
- [ ] Test with real book project
- [ ] Update README.md with plugin info
- [ ] Create pull request with plugin

## Testing Your Plugin

### Unit Tests

```python
import pytest
from my_plugin import CustomDiagramPlugin, PluginConfig

def test_custom_diagram_plugin_validates():
    config = PluginConfig(enabled=True, options={"output_dir": "/tmp"})
    plugin = CustomDiagramPlugin(config)
    assert plugin.validate()

def test_custom_diagram_plugin_processes_code_block():
    config = PluginConfig(enabled=True, options={"output_dir": "/tmp"})
    plugin = CustomDiagramPlugin(config)
    plugin.initialize()
    
    # Create mock AST node
    from unittest.mock import MagicMock
    node = MagicMock()
    node.type = "code_block"
    node.language = "custom"
    node.content = "diagram source"
    
    result = plugin.process(node)
    assert result.type == "image"
```

### Integration Tests

```python
import tempfile
from pathlib import Path
from markdown_book_builder.pipeline import Pipeline

def test_plugin_in_pipeline():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create sample markdown with diagram
        md_file = Path(tmpdir) / "test.md"
        md_file.write_text("```custom\ndiagram source\n```")
        
        # Create book config with plugin
        config = {
            "book": {"title": "Test"},
            "plugins": {
                "my_plugin": {"enabled": True}
            }
        }
        
        # Run pipeline
        pipeline = Pipeline(config)
        ast = pipeline.process(tmpdir)
        
        # Verify diagram was processed
        assert any(n.type == "image" for n in ast.walk())
```

## Best Practices

### 1. Error Handling

Always provide clear error messages:

```python
def process(self, node: Any) -> Any:
    try:
        result = self._process_internal(node)
    except Exception as e:
        logger.error(
            f"Plugin {self.__class__.__name__} failed to process {node.type}: {e}",
            exc_info=True
        )
        if self.config.options.get("strict", False):
            raise
        # Return unmodified node if error
        return node
    return result
```

### 2. Caching

Use content-based hashing to enable caching:

```python
import hashlib

def _get_cache_key(self, content: str) -> str:
    """Generate cache key from content."""
    return hashlib.sha256(content.encode()).hexdigest()
```

### 3. Logging

Add debug logging for troubleshooting:

```python
import logging

logger = logging.getLogger(__name__)

class MyPlugin(BasePlugin):
    def process(self, node: Any) -> Any:
        logger.debug(f"Processing {node.type} with {self.__class__.__name__}")
        # ... implementation ...
        logger.debug(f"Successfully processed {node.type}")
        return node
```

### 4. Configuration Validation

Validate all configuration on initialization:

```python
def __init__(self, config: PluginConfig):
    super().__init__(config)
    
    # Validate required options
    required = ["api_key", "output_dir"]
    missing = [k for k in required if k not in self.options]
    if missing:
        raise ValueError(f"Missing required options: {missing}")
```

### 5. Cleanup

Always implement cleanup for resources:

```python
def cleanup(self) -> None:
    """Close any open connections or files."""
    if hasattr(self, 'connection') and self.connection:
        self.connection.close()
        logger.info(f"{self.__class__.__name__} cleaned up")
```

## Plugin Performance Considerations

### Caching Strategy

Cache expensive operations using content hashes:

```python
# Good: Fast for duplicate content
cache_key = hashlib.sha256(content.encode()).hexdigest()
cached = self.cache.get(cache_key)
if cached:
    return cached
```

### Parallel Processing

Mark your plugin as thread-safe for parallel processing:

```python
class MyPlugin(BasePlugin):
    THREAD_SAFE = True  # Can be called from multiple threads
    
    def process(self, node: Any) -> Any:
        # Use thread-safe operations only
        ...
```

### Resource Limits

Respect memory and time budgets:

```python
import resource
import signal

def _set_timeout(self, seconds: int):
    """Set timeout for long-running operations."""
    signal.signal(signal.SIGALRM, self._timeout_handler)
    signal.alarm(seconds)
```

## Debugging Plugins

### Enable Debug Logging

```bash
export MARKDOWN_BOOK_BUILDER_LOG_LEVEL=DEBUG
python -m markdown_book_builder build . --verbose
```

### Use pdb for Interactive Debugging

```python
def process(self, node: Any) -> Any:
    import pdb; pdb.set_trace()
    # ... debugging code ...
    return node
```

### Plugin Execution Order

Control plugin execution order with priority:

```toml
[plugins.my_plugin]
enabled = true
priority = 200  # Higher = executes later
```

## Publishing Your Plugin

To share your plugin with the community:

1. **Create a GitHub repository**
   ```
   markdown-book-plugin-<name>
   ```

2. **Add to Plugin Registry** (coming soon)
   - Submit pull request to main registry
   - Include documentation and examples

3. **Publish to PyPI** (optional)
   ```bash
   python -m build
   twine upload dist/*
   ```

4. **Document on Plugin Registry**
   - Name and version
   - Description
   - Installation instructions
   - Configuration options
   - Examples

## Examples

See the `examples/plugins/` directory for complete plugin examples:
- `diagram_renderer_mermaid/` - Mermaid diagram rendering
- `image_provider_openai/` - OpenAI image generation
- `theme_minimal/` - Minimal PDF theme
- `validator_structure/` - Document structure validation

## Getting Help

- **Questions?** Check existing plugin examples or create a GitHub issue
- **Issues?** Report bugs with reproduction steps
- **Ideas?** Propose new plugins in discussions
- **Contributing?** See [CONTRIBUTING.md](CONTRIBUTING.md)

Happy plugin development! 🎉

# ADR-003: Plugin-Based Extensibility

**Status**: Accepted

## Context

The Markdown Book Builder must support multiple diagram renderers (Mermaid, PlantUML, Graphviz, D2), image providers, exporters, themes, and validation rules. Hard-coding these would create maintenance burden and prevent community contributions. We need a plugin system that is easy to understand and extend.

## Decision

We will implement a plugin architecture with the following principles:

1. **Plugin Types**:
   - Diagram Renderers: Convert diagram AST nodes to images
   - Image Providers: Generate or fetch images
   - Exporters: Convert AST to output format (PDF, LaTeX, EPUB, HTML)
   - Themes: Define styling and layout
   - Validators: Custom validation rules

2. **Plugin Registration**: Plugins register via entry points in `pyproject.toml` or explicit registration in code

3. **Plugin Interface**: Each plugin type has a well-defined base class with standard methods

4. **Plugin Isolation**: Plugins operate on immutable AST copies; failures don't affect the core pipeline

5. **Configuration**: Plugins are configured via TOML, with schema validation

## Consequences

**Advantages**:
- Easy to add new renderers/exporters without modifying core
- Community can contribute plugins
- Optional plugins don't bloat the core
- Clear contract for plugin developers
- Version-independent plugin upgrades

**Disadvantages**:
- Plugin system adds complexity to core codebase
- Plugins can have performance impact if poorly written
- Plugin discovery/debugging can be harder than direct code

**Trade-offs**:
- Chose plugin registration over hardcoding to enable extensibility
- Chose AST-based plugins to maintain pipeline abstraction
- Plugin isolation (immutable copies) over mutation to prevent side effects

## Alternatives Considered

1. **Hardcoded Renderers**: Direct implementation of all renderers in core
   - Rejected: Maintenance burden, blocks community contributions

2. **Standalone Tools**: Each renderer as separate CLI tool
   - Rejected: Complex orchestration, no unified build system

3. **Dynamic Code Loading**: Load plugin code at runtime from files
   - Rejected: Security risk; harder to debug; prefer explicit registration

## Plugin Contract Example

```python
from abc import ABC, abstractmethod
from markdown_book_builder.ast_.models import AST

class DiagramRenderer(ABC):
    """Base class for diagram renderers."""
    
    name: str  # e.g., "mermaid", "plantuml"
    
    @abstractmethod
    def render(self, diagram_node, config) -> bytes:
        """Convert diagram to image bytes."""
        pass
    
    @abstractmethod
    def supports(self, diagram_type: str) -> bool:
        """Check if renderer supports diagram type."""
        pass
```

## Related Decisions

- [ADR-001: AST-Centric Pipeline Architecture](./001-ast-centric-pipeline.md) - Plugins operate on AST
- [ADR-004: Deterministic Builds](./004-deterministic-builds.md) - Plugins must be deterministic

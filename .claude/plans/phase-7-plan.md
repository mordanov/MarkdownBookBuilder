# Phase 7 Implementation Plan: Image & Diagram Processing (T055-T061)

## Overview
Phase 7 implements image placeholder detection, diagram support (Mermaid), and OpenAI image generation with caching.

## Tasks (T055-T061)

### T055: Image Pipeline Detection
**File**: `src/markdown_book_builder/images/detector.py`
**Goal**: Detect image placeholders in AST

```python
def detect_image_placeholders(book: Book) -> list[ImagePlaceholder]:
    """Find all image placeholders that need generation."""

def find_diagrams(book: Book) -> list[DiagramBlock]:
    """Find all diagram blocks (mermaid, etc)."""
```

### T056: Mermaid Diagram Renderer
**File**: `src/markdown_book_builder/diagrams/mermaid.py`
**Goal**: Render Mermaid diagrams to SVG

```python
def render_mermaid(diagram_code: str) -> str:
    """Render Mermaid to SVG."""
```

### T057: Image Cache System
**File**: `src/markdown_book_builder/images/cache.py`
**Goal**: Cache generated images by hash

```python
def cache_image(prompt: str, image_path: Path) -> None:
    """Cache image by prompt hash."""

def get_cached_image(prompt: str) -> Path | None:
    """Retrieve cached image."""
```

### T058: OpenAI Image Generation
**File**: `src/markdown_book_builder/images/generator.py`
**Goal**: Generate images via OpenAI API

```python
def generate_image(prompt: str, config: OpenAIConfig) -> bytes:
    """Generate image via OpenAI."""
```

### T059: Image Processing Service
**File**: `src/markdown_book_builder/images/service.py`
**Goal**: Coordinate generation and caching

```python
def process_images(book: Book, config: BookConfig) -> Book:
    """Detect and generate all images."""
```

### T060: Tests
**File**: `tests/unit/test_images_*.py`
**Goal**: Unit tests for image components

### T061: Integration Tests
**File**: `tests/integration/test_image_generation.py`
**Goal**: End-to-end image pipeline tests

## Implementation Strategy

1. **T055**: AST traversal to find image placeholders
2. **T056**: Mermaid rendering (via mermaid-cli or API)
3. **T057**: File-based cache with hash keys
4. **T058**: OpenAI API integration (with error handling)
5. **T059**: Coordinate detection, generation, caching
6. **T060**: Unit tests for each component
7. **T061**: Integration tests for full pipeline

## Key Decisions

- **Mermaid Rendering**: Use mermaid-cli CLI tool (safe, deterministic)
- **Cache Location**: `.cache/images/` in project directory
- **Image Format**: PNG for web, SVG for Mermaid
- **Error Handling**: Graceful degradation (skip missing images)
- **API Calls**: Memoize within build to avoid duplicates

## Success Criteria

- ✅ Detect image placeholders in AST
- ✅ Render Mermaid diagrams to SVG
- ✅ Cache images by prompt hash
- ✅ Generate images via OpenAI API
- ✅ Full integration with build pipeline
- ✅ 20+ tests covering all scenarios
- ✅ Ruff/mypy clean
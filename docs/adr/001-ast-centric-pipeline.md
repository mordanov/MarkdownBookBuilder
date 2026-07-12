# ADR-001: AST-Centric Pipeline Architecture

**Status**: Accepted

## Context

The Markdown Book Builder needs to support multiple transformations (diagram rendering, image generation, validation, etc.) and export formats (PDF, LaTeX, EPUB, HTML) without creating tight coupling between stages. Different features may need to operate on the same document in different orders, and we need a way to ensure all transformations work consistently.

## Decision

We will use an **Abstract Syntax Tree (AST)** as the central abstraction. All processing stages will:
1. Read from AST nodes (Pydantic models)
2. Perform their transformation
3. Write back to AST nodes
4. Pass the modified AST to the next stage

The AST representation will be defined in `src/markdown_book_builder/ast_/models.py` using Pydantic for validation and serialization.

## Consequences

**Advantages**:
- Clear, well-defined contract between stages
- Easy to add new transformations (just implement a function that transforms AST → AST)
- Enables composition: stages can run in any order
- Serialization/deserialization for caching and inspection
- Type-safe with Pydantic validation

**Disadvantages**:
- Extra memory overhead compared to streaming approaches
- All content must fit in memory (not suitable for very large documents, but acceptable given 1000+ page target)
- Development requires understanding AST structure

**Trade-offs**:
- Chose AST over streaming pipeline to enable flexible, composable transformations
- Chose AST over direct Markdown manipulation to enable format-agnostic processing

## Alternatives Considered

1. **Direct Markdown Manipulation**: Process Markdown strings directly with regex/parsing
   - Rejected: Fragile, hard to maintain consistency across formats

2. **Streaming Pipeline**: Process documents line-by-line without full AST
   - Rejected: Prevents reordering transformations and makes some operations impossible (e.g., diagram -> image conversion needs full document context)

3. **Custom AST Format**: Build our own AST from scratch
   - Rejected: Use Pydantic to leverage existing validation and serialization

## Related Decisions

- [ADR-003: Plugin-Based Extensibility](./003-plugin-architecture.md) - Plugins operate on AST nodes
- [ADR-004: Deterministic Builds](./004-deterministic-builds.md) - AST is serialized for caching

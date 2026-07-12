# Architecture Decision Records (ADRs)

This directory documents significant architectural decisions made in the Markdown Book Builder project.

## Format

Each ADR follows the standard template:
- **Status**: Proposed, Accepted, Deprecated, Superseded
- **Context**: Why this decision was needed
- **Decision**: What we decided to do
- **Consequences**: Trade-offs and implications
- **Alternatives**: Other approaches considered

## Decisions

1. [ADR-001: AST-Centric Pipeline Architecture](./001-ast-centric-pipeline.md) - Using an internal AST representation for all transformations
2. [ADR-002: Technology Stack Selection](./002-technology-stack.md) - Python 3.13, Typer, Pydantic, uv
3. [ADR-003: Plugin-Based Extensibility](./003-plugin-architecture.md) - Extensible system for renderers, themes, and validators
4. [ADR-004: Deterministic Builds](./004-deterministic-builds.md) - Configuration-driven reproducibility strategy
5. [ADR-005: Configuration Strategy](./005-configuration-strategy.md) - TOML + environment variables approach

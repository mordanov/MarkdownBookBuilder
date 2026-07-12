# ADR-004: Deterministic Builds

**Status**: Accepted

## Context

For a book processing pipeline to be reliable and trustworthy, authors need to know that the same Markdown + configuration will always produce the same output. This enables:
- Caching (skip re-processing unchanged content)
- CI/CD reproducibility (verify builds are identical)
- Debugging (diff builds to find what changed)
- Archive/reproducibility (builds remain valid years later)

## Decision

We will ensure all builds are deterministic by:

1. **Dependency Pinning**: All dependencies are pinned to exact versions in `uv.lock`
2. **Configuration Versioning**: Configuration schema includes version field; incompatible changes require migration
3. **Stable Sorting**: All file discovery and processing preserves order (no reliance on filesystem ordering)
4. **Seed Values**: Any randomness (e.g., UUIDs, timestamps) is deterministic or excluded
5. **Plugin Stability**: Plugins must be deterministic; non-deterministic operations flag as "experimental"
6. **Build Caching**: AST checkpoints enable incremental builds without content re-processing

## Consequences

**Advantages**:
- Same input always produces identical output
- Build caching becomes reliable
- Enables testing via golden file comparison
- Authors can reproduce old builds years later
- CI/CD can verify build integrity

**Disadvantages**:
- Requires careful handling of randomness (affects image generation, numbering)
- Plugin authors must ensure determinism
- Version migrations needed when schema changes
- Some operations may need explicit seeding

**Trade-offs**:
- Chose strict determinism over flexibility to enable reproducibility
- Use checksums for verification rather than heuristic freshness checks
- Require plugin authors to opt into experimental non-deterministic mode

## Implementation Guidelines

1. **File Ordering**: Use `sorted()` consistently; document ordering strategy in code
2. **Configuration**: Always include schema version in config files
3. **Random Data**: Use deterministic seeding (e.g., based on input hash)
4. **External APIs**: Cache API responses with checksums; document cache strategy
5. **Timestamps**: Use metadata timestamps, not current time
6. **Testing**: Compare outputs via checksums; golden files for visual validation

## Related Decisions

- [ADR-001: AST-Centric Pipeline Architecture](./001-ast-centric-pipeline.md) - AST enables checkpointing
- [ADR-005: Configuration Strategy](./005-configuration-strategy.md) - Configuration is part of input hash

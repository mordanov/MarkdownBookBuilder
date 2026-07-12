# ADR-005: Configuration Strategy

**Status**: Accepted

## Context

The Markdown Book Builder needs to support:
- Project-specific configuration (book title, author, output format)
- Environment-specific secrets (API keys)
- User preferences (default theme, cache location)
- Build-time overrides (command-line flags)

Configuration sources must have clear precedence, and secrets must never be stored in version control.

## Decision

We will use a **layered configuration strategy**:

1. **Layer 1: Defaults** (lowest priority)
   - Built-in defaults in code
   - Fallback for all settings

2. **Layer 2: User Config**
   - `~/.config/markdown-book-builder/config.toml` (or platform-specific)
   - Global preferences for this user

3. **Layer 3: Project Config**
   - `book.toml` in project root
   - Checked into version control
   - Most important for reproducibility

4. **Layer 4: Environment Variables**
   - `MBB_*` prefix (e.g., `MBB_OPENAI_API_KEY`)
   - Secrets and machine-specific values
   - Never checked into version control

5. **Layer 5: Command-line Flags** (highest priority)
   - `--title`, `--author`, etc.
   - Override everything for one-off builds

## Configuration Format

- **TOML** for static config (book.toml, user config)
- **Environment variables** for secrets and dynamic values
- **CLI flags** for build-time overrides

## Consequences

**Advantages**:
- Clear precedence prevents ambiguity
- Secrets can be managed via environment
- Reproducible builds: `book.toml` contains all project-specific config
- Flexible: developers can use either environment variables or TOML
- Portable: TOML is human-readable and version-control friendly

**Disadvantages**:
- Multiple configuration files can be confusing
- Secrets in environment variables require discipline (easy to leak in logs)
- TOML schema validation needed for error messages

**Trade-offs**:
- Chose TOML over JSON for human-readability
- Chose environment variables over `.env` file to match 12-factor app principles
- Chose layered approach over single config to support global + project configs

## Example Configuration

**book.toml** (project root, checked in):
```toml
title = "My Technical Book"
author = "Jane Doe"
version = "1.0.0"

[output]
format = "pdf"
path = "dist/book.pdf"
theme = "default"

[build]
cache_dir = ".cache"
```

**~/.config/markdown-book-builder/config.toml** (user home, not checked in):
```toml
[cache]
dir = "~/.cache/mbb"

[openai]
# Will be overridden by environment variable if set
model = "gpt-4o"
```

**Environment** (never checked in):
```bash
export MBB_OPENAI_API_KEY="sk-..."
export MBB_OUTPUT_PATH="/tmp/book.pdf"  # Override project config
```

**Command line** (one-off override):
```bash
python -m markdown_book_builder build \
  --title "Quick Preview" \
  --output-format html \
  .
```

## Security Considerations

1. Never log configuration values (secrets may be included)
2. Validate TOML strictly; reject unknown keys
3. Use distinct prefixes for secrets vs. configuration
4. Document which settings should be secrets
5. Provide clear error messages when required secrets are missing

## Related Decisions

- [ADR-004: Deterministic Builds](./004-deterministic-builds.md) - Configuration is part of build identity

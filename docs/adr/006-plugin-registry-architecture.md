# ADR 006: Plugin Registry Architecture

## Status
Proposed

## Context

The Markdown Book Builder supports extensibility through plugins (diagram renderers, image providers, exporters, themes, validation rules). As the plugin ecosystem grows, users need a standardized way to:

1. **Discover** available plugins
2. **Install** plugins with dependency management
3. **Update** plugins to new versions
4. **Verify** plugin integrity and compatibility

Without a registry system, plugin discovery is ad-hoc, installation requires manual steps, and version management is error-prone.

## Decision

We will implement a centralized **Plugin Registry System** with these components:

### 1. Registry Architecture

```
User → CLI Client → Registry API → Plugin Packages
         ↓
    Local Cache
```

- **Central Registry**: GitHub-hosted JSON index or dedicated service
- **CLI Client**: Commands for search, install, update, verify
- **Local Cache**: User's `~/.markdown_book_builder/` directory
- **Plugin Packages**: Tarball or pip distributions

### 2. Plugin Metadata (plugin.toml)

Each plugin includes a manifest with:
- **Identification**: id, name, version, author
- **Classification**: category, tags, type
- **Compatibility**: min/max MBB version, Python version
- **Dependencies**: External tools and libraries
- **Features**: Caching, parallelization, config options
- **Installation**: Method (pip, git, url, local) and source

### 3. Registry Index (registry.json)

Central index maintained on registry server containing:
- All available plugins with metadata
- Version history and download URLs
- Checksums for verification
- Statistics (downloads, ratings, etc.)
- Verification status and signatures

### 4. CLI Commands

Primary commands for users:

```bash
# Discovery
mbb plugin list
mbb plugin search diagram
mbb plugin info diagram-mermaid

# Installation
mbb plugin install diagram-mermaid
mbb plugin install diagram-mermaid@1.0.0
mbb plugin install ./local-plugin.tar.gz

# Management
mbb plugin update
mbb plugin uninstall diagram-mermaid
mbb plugin status
```

### 5. Installation Methods

Support multiple installation sources:
- **Registry**: Recommended, verified plugins
- **GitHub**: Direct from repository releases
- **URL**: Any HTTPS URL hosting plugin package
- **Local**: File paths for development

### 6. Dependency Resolution

Handle transitive dependencies:
- Parse requirements from plugin.toml
- Check compatibility with current MBB version
- Install missing dependencies (external tools)
- Manage version conflicts

### 7. Verification Strategy

Ensure plugin integrity:
- **Checksums**: SHA256 verification of all files
- **Signatures**: Optional GPG signing for trusted maintainers
- **Version Constraints**: Enforce compatibility
- **Security Scanning**: Check for known vulnerabilities (future)

## Rationale

### Why a Centralized Registry?

**Alternatives Considered:**

1. **No registry** (manual installation only)
   - ❌ Poor discoverability
   - ❌ Complex dependency management
   - ❌ Version conflicts and compatibility issues

2. **PyPI only** (distribute via pip)
   - ⚠️ Works for some plugins but not all
   - ⚠️ Doesn't capture non-Python dependencies
   - ⚠️ Less curated and verified

3. **Multiple registries** (fragmented)
   - ❌ Confusing for users
   - ❌ Hard to search across sources
   - ❌ Duplicate effort for maintainers

4. **Centralized registry** (chosen)
   - ✅ Single source of truth
   - ✅ Unified discovery and installation
   - ✅ Version and dependency management
   - ✅ Verification and security
   - ✅ Usage statistics and analytics

### Why Metadata in plugin.toml?

- **Declarative**: Clear specification of plugin properties
- **Portable**: Plugins carry metadata with them
- **Standard**: Similar to Cargo.toml, pyproject.toml
- **Verifiable**: Registry can validate against schema

### Why Layered Installation?

Support multiple sources because:
- **Registry**: Best for production use (stable, verified)
- **GitHub**: For latest development versions
- **URL**: For custom/internal plugins
- **Local**: Essential for plugin development

### Why Checksum Verification?

- Prevents corruption during download
- Detects tampering or man-in-the-middle attacks
- Essential for reproducible builds
- Aligns with other package managers

## Consequences

### Positive

1. **Improved UX**: Simple one-command plugin installation
2. **Better Discovery**: Users can easily find available plugins
3. **Dependency Management**: Automatic resolution of transitive deps
4. **Version Control**: Easy upgrades and downgrades
5. **Security**: Verification and integrity checks
6. **Analytics**: Track plugin usage and popularity
7. **Community**: Ecosystem grows around registry

### Negative

1. **Maintenance Burden**: Registry server needs upkeep
2. **Approval Process**: Plugin submissions need review
3. **Single Point of Failure**: Registry downtime affects installations
4. **Network Dependency**: Offline users limited to cached plugins
5. **Trust Model**: Users must trust registry operators

### Mitigations

- **Maintenance**: Automate via GitHub Actions and workflows
- **Approval**: Clear guidelines and automated checks
- **Reliability**: Use GitHub Pages for registry (high uptime)
- **Offline**: Cache registry locally, support local registries
- **Trust**: Transparent submission process, signed releases, code reviews

## Implementation Roadmap

### Phase 1 (Weeks 1-2): Core Registry
- Plugin metadata schema
- Local cache system
- CLI: list, search, info commands

### Phase 2 (Weeks 3-4): Installation
- Plugin installer with download/setup
- Dependency resolver
- CLI: install, uninstall, update commands

### Phase 3 (Weeks 5-6): Registry Server
- Central registry index
- Registry API endpoints
- Plugin submission process

### Phase 4 (Weeks 7-8): Advanced Features
- Verification and security scanning
- Custom registries
- Plugin recommendations

## Open Questions

1. **Self-hosted vs. Cloud**: Should registry be GitHub-hosted or dedicated server?
   - **Preferred**: GitHub Pages (low maintenance, high reliability)

2. **Sandbox Execution**: Should plugins run sandboxed?
   - **Answer**: Future enhancement after MVP

3. **Monetization**: Should paid plugins be supported?
   - **Answer**: Out of scope for MVP, can be added later

4. **Plugin Reviews**: Should plugins be reviewed before registry inclusion?
   - **Answer**: Yes, light review for security and metadata quality

## Alternatives Considered

### No Registry (Status Quo)
- Manual plugin installation and discovery
- Users discover via docs, examples, GitHub
- ❌ Doesn't scale as plugin ecosystem grows

### Plugin Package (pip only)
- Leverage PyPI for distribution
- ⚠️ Doesn't capture all plugin types
- ⚠️ Doesn't handle external tool dependencies
- ⚠️ Less integrated with MBB workflow

### Ansible/Chef Model (Roles/Cookbooks)
- Plugins as self-contained packages in registry
- ✅ Proven model from other ecosystems
- ✅ Good for complex plugins
- ❌ More overhead than needed for MVP

## References

### Similar Systems
- [npm Registry](https://www.npmjs.com/) - JavaScript packages
- [Cargo Crates Registry](https://crates.io/) - Rust packages
- [Ansible Galaxy](https://galaxy.ansible.com/) - Ansible roles
- [VS Code Extensions Marketplace](https://marketplace.visualstudio.com/) - Code plugins

### Related ADRs
- [ADR 001: AST-Based Architecture](001-ast-based-architecture.md)
- [ADR 002: Layered Configuration](002-layered-configuration.md)
- [ADR 005: Plugin System Design](005-plugin-system-design.md)

## Decision Log

- **2024-03-20**: Initial proposal for plugin registry
- **2024-03-25**: Design review with team
- **2024-04-01**: Approved for implementation

---

**Decision Maker**: Aleksandr Mordanov
**Date**: 2024-04-01

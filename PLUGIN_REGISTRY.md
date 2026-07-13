# Plugin Registry

The Plugin Registry is the centralized system for discovering, registering, and managing extensions for Markdown Book Builder. This document outlines the architecture, data model, and implementation plan.

## Overview

The plugin registry enables:
- **Discovery**: Users can find and browse available plugins
- **Installation**: One-command plugin setup with dependencies
- **Version Management**: Track and upgrade plugin versions
- **Verification**: Check plugin compatibility and metadata
- **Caching**: Local cache of registry data for offline access

## Registry Architecture

### Components

```
┌─────────────────────────────────────────────────────┐
│         Plugin Registry System                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │     Registry Server (metadata & index)       │  │
│  │  - Central repository of plugin definitions  │  │
│  │  - Version management and history            │  │
│  │  - Compatibility matrix                      │  │
│  │  - Rating and statistics                     │  │
│  └──────────────────────────────────────────────┘  │
│                    ↕ API                            │
│  ┌──────────────────────────────────────────────┐  │
│  │        CLI Registry Client                   │  │
│  │  - Search and browse plugins                 │  │
│  │  - Install and update plugins                │  │
│  │  - Manage local plugin cache                 │  │
│  │  - Verify installations                      │  │
│  └──────────────────────────────────────────────┘  │
│                    ↓                                │
│  ┌──────────────────────────────────────────────┐  │
│  │      Local Plugin Cache (~/.mbb/cache)       │  │
│  │  - Downloaded plugin metadata                │  │
│  │  - Installed plugin tracking                 │  │
│  │  - Compatibility cache                       │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Data Flow

```
User runs: mbb plugin search diagram
           ↓
    CLI Client
           ↓
    Query Registry API
           ↓
Registry returns matching plugins
           ↓
    CLI displays results
           ↓
User runs: mbb plugin install my-diagram-plugin
           ↓
    CLI resolves dependencies
           ↓
    Downloads plugin source
           ↓
    Verifies checksum
           ↓
    Runs plugin installer
           ↓
    Updates local cache
           ↓
    Plugin ready to use
```

## Plugin Metadata

Each plugin is described by a manifest file defining its properties, requirements, and capabilities.

### Plugin Manifest (plugin.toml)

```toml
[plugin]
id = "my-plugin"                    # Unique plugin identifier
name = "My Custom Plugin"           # Human-readable name
version = "1.0.0"                   # Semantic version
author = "Your Name"
email = "author@example.com"
license = "MIT"
description = "Short description of what this plugin does"
homepage = "https://github.com/author/plugin"
repository = "https://github.com/author/plugin"
documentation = "https://github.com/author/plugin/blob/main/README.md"

[plugin.type]
category = "diagram_renderer"       # diagram_renderer, image_provider, exporter, theme, validator
supported_formats = ["mermaid", "plantuml"]

[plugin.compatibility]
min_version = "0.1.0"               # Minimum MBB version
max_version = "1.0.0"               # Maximum MBB version (optional)
python = ">=3.13"                   # Python version requirement

[plugin.features]
caching = true                      # Supports caching
parallelizable = true               # Thread-safe for parallel processing
network_capable = false             # Requires network access
configurable = true                 # Supports configuration options

[plugin.requirements]
# External dependencies (tools, libraries)
# Format: package = "version_spec"
mermaid_cli = ">=10.0"
requests = ">=2.31.0"

[plugin.defaults]
# Default configuration values
output_format = "png"
quality = "high"
timeout = 30
cache_enabled = true

[plugin.installation]
method = "pip"                      # pip, git, url, local
source = "https://pypi.org/project/my-plugin"
checksum = "sha256:abc123def456..."

[plugin.metadata]
tags = ["diagram", "visualization", "mermaid"]
downloads = 15420
rating = 4.8
verified = true
maintainer_verified = true
```

### Plugin Registry Entry (registry.json)

The registry server maintains an index of all plugins:

```json
{
  "plugins": [
    {
      "id": "diagram-mermaid",
      "name": "Mermaid Diagram Renderer",
      "version": "1.0.0",
      "author": "Markdown Book Builder Team",
      "category": "diagram_renderer",
      "description": "Render Mermaid diagrams to PNG/SVG",
      "homepage": "https://github.com/mordanov/mbb-plugin-mermaid",
      "license": "MIT",
      "downloads": 45123,
      "rating": 4.9,
      "verified": true,
      "python_versions": ["3.13"],
      "mbb_versions": {
        "min": "0.1.0",
        "max": "1.0.0"
      },
      "dependencies": {
        "mermaid_cli": ">=10.0",
        "puppeteer": ">=20.0"
      },
      "releases": [
        {
          "version": "1.0.0",
          "released_at": "2024-01-15",
          "checksum": "sha256:abc123...",
          "download_url": "https://registry.mbb.dev/plugins/diagram-mermaid-1.0.0.tar.gz"
        },
        {
          "version": "0.9.0",
          "released_at": "2024-01-01",
          "checksum": "sha256:def456...",
          "download_url": "https://registry.mbb.dev/plugins/diagram-mermaid-0.9.0.tar.gz"
        }
      ]
    }
  ],
  "metadata": {
    "total_plugins": 127,
    "last_updated": "2024-03-20T10:30:00Z",
    "version": "1.0"
  }
}
```

## CLI Commands

### Plugin Discovery

```bash
# List all plugins
mbb plugin list

# List plugins by category
mbb plugin list --category diagram_renderer
mbb plugin list --category image_provider

# Search for plugins
mbb plugin search diagram
mbb plugin search --tag mermaid
mbb plugin search --author "author-name"

# Show plugin details
mbb plugin info diagram-mermaid
mbb plugin info diagram-mermaid --version 1.0.0
```

### Plugin Management

```bash
# Install a plugin
mbb plugin install diagram-mermaid
mbb plugin install diagram-mermaid@1.0.0  # Specific version

# Install from URL or local file
mbb plugin install https://github.com/author/plugin/releases/download/v1.0.0/plugin.tar.gz
mbb plugin install ./my-plugin-1.0.0.tar.gz

# Update plugins
mbb plugin update diagram-mermaid
mbb plugin update --all

# Uninstall a plugin
mbb plugin uninstall diagram-mermaid

# List installed plugins
mbb plugin list --installed
mbb plugin list --installed --verbose

# Show plugin status
mbb plugin status diagram-mermaid
```

### Registry Management

```bash
# Refresh registry cache
mbb plugin registry refresh

# Add custom registry
mbb plugin registry add --name custom https://registry.example.com
mbb plugin registry list
mbb plugin registry remove custom

# Verify plugin integrity
mbb plugin verify diagram-mermaid

# Check for updates
mbb plugin check-updates
```

## Registry API

### REST Endpoints

#### Search Plugins

```
GET /api/v1/plugins/search?q=diagram&category=diagram_renderer&limit=50

Response:
{
  "results": [
    {
      "id": "diagram-mermaid",
      "name": "Mermaid Diagram Renderer",
      "version": "1.0.0",
      "category": "diagram_renderer",
      "rating": 4.9,
      "downloads": 45123
    }
  ],
  "total": 127,
  "limit": 50,
  "offset": 0
}
```

#### Get Plugin Details

```
GET /api/v1/plugins/{plugin_id}

Response:
{
  "id": "diagram-mermaid",
  "name": "Mermaid Diagram Renderer",
  "version": "1.0.0",
  "author": "...",
  "description": "...",
  "manifest": { ... },
  "releases": [ ... ],
  "stats": {
    "downloads": 45123,
    "rating": 4.9,
    "installs": 12345
  }
}
```

#### Get Specific Plugin Version

```
GET /api/v1/plugins/{plugin_id}/releases/{version}

Response:
{
  "version": "1.0.0",
  "released_at": "2024-01-15",
  "checksum": "sha256:abc123...",
  "download_url": "https://registry.mbb.dev/plugins/diagram-mermaid-1.0.0.tar.gz",
  "size_bytes": 524288,
  "manifest": { ... }
}
```

#### Download Plugin

```
GET /api/v1/plugins/{plugin_id}/releases/{version}/download

Redirects to plugin package file or streams directly
```

#### Verify Plugin

```
POST /api/v1/plugins/{plugin_id}/verify

Request:
{
  "checksum": "sha256:abc123...",
  "version": "1.0.0"
}

Response:
{
  "valid": true,
  "verified_at": "2024-03-20T10:30:00Z",
  "warnings": []
}
```

## Implementation Plan

### Phase 1: Core Registry (Weeks 1-2)

**Deliverables**:
- Plugin metadata schema (plugin.toml)
- Local plugin cache system
- CLI commands: list, search, info

**Tasks**:
1. Define plugin.toml schema with JSONSchema validation
2. Implement PluginManifest data class
3. Create LocalPluginCache for tracking installed plugins
4. Build PluginRegistry client for querying
5. Implement CLI subcommands in typer

**Success Criteria**:
- ✓ Users can list available plugins via `mbb plugin list`
- ✓ Plugin metadata is correctly parsed from plugin.toml
- ✓ Registry cache syncs correctly

### Phase 2: Installation & Dependency Management (Weeks 3-4)

**Deliverables**:
- Plugin installation from registry or file
- Dependency resolution
- Version constraint handling

**Tasks**:
1. Create PluginInstaller class with download and setup logic
2. Implement dependency resolver (handle transitive deps)
3. Add version constraint parsing (semver, ranges)
4. CLI: install, uninstall, update commands
5. Add plugin verification (checksum validation)

**Success Criteria**:
- ✓ Users can install plugins: `mbb plugin install diagram-mermaid`
- ✓ Dependencies are automatically installed
- ✓ Version constraints are respected
- ✓ Checksum verification prevents corrupted installs

### Phase 3: Registry Server (Weeks 5-6)

**Deliverables**:
- Central registry server (GitHub-hosted JSON or dedicated service)
- Plugin submission process
- Automated registry updates

**Tasks**:
1. Create registry index structure (registry.json)
2. Set up GitHub workflow to publish registry
3. Implement registry API endpoints
4. Add plugin submission guidelines and checklist
5. Create plugin maintainer documentation

**Success Criteria**:
- ✓ Central registry accessible at registry.mbb.dev
- ✓ CLI can query registry API
- ✓ Plugin authors can submit plugins
- ✓ Registry auto-updates on new releases

### Phase 4: Advanced Features (Weeks 7-8)

**Deliverables**:
- Plugin verification and security scanning
- Custom registry support
- Plugin rating and recommendation system

**Tasks**:
1. Add checksum and signature verification
2. Implement basic security scanning (malware, suspicious code)
3. Support multiple registries (primary + custom)
4. Add rating/review system (future enhancement)
5. Implement plugin analytics dashboard

**Success Criteria**:
- ✓ Users can add custom registries
- ✓ Plugins are verified and signed
- ✓ Security warnings shown for unverified plugins
- ✓ Registry provides usage statistics

## Local Plugin Locations

### System-Wide Plugins

```
~/.markdown_book_builder/
├── plugins/
│   ├── diagram-mermaid/
│   │   ├── plugin.toml
│   │   ├── my_plugin/
│   │   │   ├── __init__.py
│   │   │   └── main.py
│   │   └── README.md
│   └── image-openai/
├── config/
│   ├── plugins.toml
│   └── registry-cache.json
└── cache/
    ├── plugins/
    └── downloads/
```

### Project-Level Plugins

```
./plugins/
├── my-custom-plugin/
│   ├── plugin.toml
│   ├── my_plugin/
│   │   ├── __init__.py
│   │   └── main.py
│   └── README.md
└── plugins.toml
```

## Security Considerations

### Plugin Verification

1. **Checksum Validation**: SHA256 of all plugin files
2. **Signature Verification**: Optional GPG signing for trusted maintainers
3. **Sandboxing**: Plugins run in restricted execution context (future)
4. **Dependency Scanning**: Check dependencies for known vulnerabilities

### Registry Security

1. **HTTPS Only**: All registry communication encrypted
2. **Rate Limiting**: Prevent abuse and DDoS
3. **API Keys**: Optional authentication for submissions
4. **Audit Logging**: Track all registry changes

### User Safety

1. **Verified Badge**: Mark plugins from verified authors
2. **Warnings**: Alert users about unverified or risky plugins
3. **Sandboxing Roadmap**: Plan to sandbox plugin execution
4. **Rollback**: Easy uninstall of problematic plugins

## Plugin Submission Process

### For Plugin Authors

1. **Create plugin** following [PLUGIN_DEVELOPMENT.md](PLUGIN_DEVELOPMENT.md)
2. **Write comprehensive documentation** (README, examples)
3. **Add tests** with >80% coverage
4. **Create `plugin.toml`** with complete metadata
5. **Publish** to GitHub (or other public repo)
6. **Submit** to registry via GitHub PR:
   - Add entry to `plugins.json`
   - Include author contact info
   - Link to plugin repository
7. **Maintainers review** for:
   - Code quality and security
   - Metadata completeness
   - Documentation clarity
   - Version compatibility
8. **Merge** and plugin appears in registry

### Registry Entry Template

```json
{
  "id": "my-plugin-name",
  "name": "My Plugin Name",
  "author": "Your Name",
  "email": "you@example.com",
  "repository": "https://github.com/you/my-plugin-name",
  "documentation": "https://github.com/you/my-plugin-name/blob/main/README.md",
  "category": "diagram_renderer",
  "first_released": "2024-01-15",
  "verified": false
}
```

## Migration for Existing Plugins

For teams with custom plugins before the registry existed:

```bash
# 1. Create plugin.toml in your plugin directory
# 2. Package plugin as tarball
tar czf my-plugin-1.0.0.tar.gz my-plugin/

# 3. Install locally or from file
mbb plugin install ./my-plugin-1.0.0.tar.gz

# 4. Submit to registry (optional)
# Create GitHub repo and submit PR to registry
```

## Future Enhancements

### Short Term (Next 1-2 releases)

- [ ] Plugin configuration UI
- [ ] Plugin marketplace website
- [ ] Rating and review system
- [ ] Plugin templates and scaffolding

### Medium Term (Next 2-4 releases)

- [ ] Plugin sandboxing for security
- [ ] Automatic security scanning
- [ ] Plugin compatibility testing matrix
- [ ] CDN distribution for faster downloads

### Long Term (Future)

- [ ] Plugin monetization (paid plugins)
- [ ] Plugin dependency graph visualization
- [ ] A/B testing framework for plugins
- [ ] Community voting on plugin quality

## Related Documentation

- [PLUGIN_DEVELOPMENT.md](PLUGIN_DEVELOPMENT.md) - How to create plugins
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contributing guidelines
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues

## Questions & Support

- **Registry Issues?** Open GitHub issue at [mordanov/MarkdownBookBuilder](https://github.com/mordanov/MarkdownBookBuilder)
- **Plugin Problems?** Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Plugin Development?** See [PLUGIN_DEVELOPMENT.md](PLUGIN_DEVELOPMENT.md)
- **Contributing?** Review [CONTRIBUTING.md](CONTRIBUTING.md)

---

**Registry Status**: Planning & Documentation Phase

The plugin registry is currently in the documentation and planning phase. Implementation will begin in Phase 2 of the Markdown Book Builder roadmap.

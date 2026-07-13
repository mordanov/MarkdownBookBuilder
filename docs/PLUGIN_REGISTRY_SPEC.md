# Plugin Registry Implementation Specification

## Overview

This document provides detailed technical specifications for implementing the Plugin Registry system for Markdown Book Builder.

## Table of Contents

1. [Data Models](#data-models)
2. [API Specifications](#api-specifications)
3. [CLI Commands](#cli-commands)
4. [Database Schema](#database-schema)
5. [Configuration](#configuration)
6. [Error Handling](#error-handling)
7. [Testing Strategy](#testing-strategy)

---

## Data Models

### PluginManifest

Represents a single plugin's metadata from `plugin.toml`.

```python
@dataclass
class PluginManifest:
    # Identification
    id: str                           # Unique identifier (slug format)
    name: str                         # Display name
    version: str                      # Semantic version
    author: str                       # Author name
    email: Optional[str]              # Contact email
    license: str                      # License type (MIT, Apache-2.0, etc.)
    description: str                  # Short description (<200 chars)
    long_description: Optional[str]   # Extended description
    
    # URLs
    homepage: Optional[str]           # Project homepage
    repository: Optional[str]         # Source code repository
    documentation: Optional[str]      # Documentation URL
    bug_tracker: Optional[str]        # Issue tracker URL
    
    # Classification
    category: PluginCategory          # Category enum
    type: str                         # Specific type (e.g., "mermaid" for diagram)
    tags: list[str]                   # Tags for discovery
    
    # Compatibility
    min_mbb_version: str              # Minimum MBB version
    max_mbb_version: Optional[str]    # Maximum MBB version
    python_version: str               # Python version requirement
    
    # Features
    features: PluginFeatures          # Supported features
    
    # Dependencies
    dependencies: dict[str, str]      # External dependencies
    python_dependencies: dict[str, str]  # Python package requirements
    
    # Configuration
    defaults: dict[str, Any]          # Default configuration
    schema: Optional[dict]            # JSON schema for validation
    
    # Installation
    installation_method: str          # Installation method
    installation_source: str          # Where to install from
    
    # Metadata
    verified: bool = False            # Registry verified this plugin
    signed: bool = False              # GPG signed by maintainer
    maintainer_email: Optional[str]   # Registry maintainer email
    
    def validate(self) -> tuple[bool, list[str]]:
        """Validate manifest completeness and format."""
        errors = []
        # Validation logic
        return len(errors) == 0, errors
    
    def is_compatible(self, mbb_version: str) -> bool:
        """Check if plugin is compatible with MBB version."""
        # Version comparison logic
        pass
    
    def resolve_dependencies(self) -> dict[str, str]:
        """Resolve all dependencies including transitive."""
        # Dependency resolution logic
        pass
```

### PluginCategory

Enum of supported plugin types:

```python
class PluginCategory(str, Enum):
    DIAGRAM_RENDERER = "diagram_renderer"
    IMAGE_PROVIDER = "image_provider"
    EXPORTER = "exporter"
    THEME = "theme"
    VALIDATOR = "validator"
    UNKNOWN = "unknown"
```

### PluginFeatures

Plugin capabilities:

```python
@dataclass
class PluginFeatures:
    caching: bool = False
    parallelizable: bool = False
    network_capable: bool = False
    configurable: bool = False
    async_support: bool = False
```

### RegistryPlugin

Plugin entry in the registry:

```python
@dataclass
class RegistryPlugin:
    id: str
    name: str
    description: str
    author: str
    category: PluginCategory
    
    latest_version: str
    versions: list[str]              # All available versions
    
    homepage: Optional[str]
    repository: Optional[str]
    documentation: Optional[str]
    
    rating: float                    # 1.0 to 5.0
    downloads: int
    installs: int
    
    verified: bool
    created_at: datetime
    updated_at: datetime
    
    def get_version_info(self, version: str) -> 'VersionInfo':
        """Get detailed info for specific version."""
        pass
    
    def get_release_history(self) -> list[tuple[str, datetime]]:
        """Get list of (version, release_date) tuples."""
        pass
```

### VersionInfo

Detailed information about a specific plugin version:

```python
@dataclass
class VersionInfo:
    version: str
    released_at: datetime
    
    # Download info
    download_url: str
    file_size: int
    checksum: str                    # SHA256
    checksum_algorithm: str = "sha256"
    
    # Metadata
    manifest: PluginManifest
    changelog: Optional[str]
    
    # Compatibility
    compatible_mbb_versions: list[str]
    python_requirement: str
    
    # Status
    yanked: bool = False             # Deprecated version
    yank_reason: Optional[str]
    
    def verify_checksum(self, file_path: Path) -> bool:
        """Verify downloaded file against checksum."""
        pass
```

### InstalledPlugin

Represents an installed plugin in the local system:

```python
@dataclass
class InstalledPlugin:
    id: str
    name: str
    version: str
    
    # Installation location
    location: Path
    scope: str                       # "system" or "project"
    
    # Metadata
    manifest: PluginManifest
    installed_at: datetime
    
    # Status
    enabled: bool = True
    update_available: Optional[str] = None
    
    def load_module(self) -> Any:
        """Load and return plugin module."""
        pass
    
    def uninstall(self) -> bool:
        """Remove plugin from system."""
        pass
    
    def check_update(self, registry: 'PluginRegistry') -> Optional[str]:
        """Check if update is available."""
        pass
```

---

## API Specifications

### REST API Endpoints

#### 1. Search Plugins

```
GET /api/v1/plugins/search

Query Parameters:
  q: string (search query)
  category: string (filter by category)
  tag: string (filter by tag, repeatable)
  limit: int (default: 50, max: 100)
  offset: int (default: 0)
  sort: string (default: "downloads", options: "rating", "updated", "name")

Response (200 OK):
{
  "total": 127,
  "limit": 50,
  "offset": 0,
  "results": [
    {
      "id": "diagram-mermaid",
      "name": "Mermaid Diagram Renderer",
      "version": "1.0.0",
      "author": "Team",
      "category": "diagram_renderer",
      "description": "...",
      "rating": 4.9,
      "downloads": 45123,
      "verified": true
    }
  ]
}
```

#### 2. Get Plugin Details

```
GET /api/v1/plugins/{plugin_id}

Response (200 OK):
{
  "id": "diagram-mermaid",
  "name": "Mermaid Diagram Renderer",
  "latest_version": "1.0.0",
  "author": "Team",
  "description": "...",
  "homepage": "https://...",
  "repository": "https://...",
  "documentation": "https://...",
  "category": "diagram_renderer",
  "tags": ["diagram", "visualization"],
  "rating": 4.9,
  "downloads": 45123,
  "verified": true,
  "versions": ["1.0.0", "0.9.0", "0.8.0"],
  "updated_at": "2024-03-20T10:30:00Z"
}

Response (404 Not Found):
{
  "error": "Plugin not found"
}
```

#### 3. Get Plugin Version

```
GET /api/v1/plugins/{plugin_id}/versions/{version}

Response (200 OK):
{
  "version": "1.0.0",
  "released_at": "2024-01-15T10:00:00Z",
  "download_url": "https://registry.mbb.dev/plugins/diagram-mermaid-1.0.0.tar.gz",
  "file_size": 524288,
  "checksum": "sha256:abc123def456...",
  "manifest": { ... },
  "compatible_mbb_versions": ["0.1.0", "1.0.0"],
  "python_requirement": ">=3.13",
  "yanked": false
}
```

#### 4. Download Plugin

```
GET /api/v1/plugins/{plugin_id}/versions/{version}/download

Response (302 Redirect):
Location: https://cdn.registry.mbb.dev/plugins/diagram-mermaid-1.0.0.tar.gz

Or (200 OK):
Content-Type: application/gzip
Content-Length: 524288
[Binary file contents]
```

#### 5. Verify Plugin

```
POST /api/v1/plugins/{plugin_id}/versions/{version}/verify

Request Body:
{
  "checksum": "sha256:abc123def456..."
}

Response (200 OK):
{
  "valid": true,
  "verified_at": "2024-03-20T10:30:00Z",
  "warnings": []
}

Response (400 Bad Request):
{
  "valid": false,
  "errors": ["Checksum mismatch"],
  "expected": "sha256:abc...",
  "received": "sha256:def..."
}
```

#### 6. List Categories

```
GET /api/v1/categories

Response (200 OK):
{
  "categories": [
    {
      "id": "diagram_renderer",
      "name": "Diagram Renderers",
      "count": 12,
      "description": "Convert diagrams to images"
    },
    {
      "id": "image_provider",
      "name": "Image Providers",
      "count": 8,
      "description": "Generate or fetch images"
    }
  ]
}
```

#### 7. Get Registry Metadata

```
GET /api/v1/registry

Response (200 OK):
{
  "version": "1.0",
  "last_updated": "2024-03-20T10:30:00Z",
  "total_plugins": 127,
  "total_downloads": 1234567,
  "cache_ttl_seconds": 3600
}
```

### Error Responses

```json
{
  "error": "Error message",
  "code": "ERROR_CODE",
  "details": {
    "key": "value"
  }
}
```

Common error codes:
- `PLUGIN_NOT_FOUND`: Plugin doesn't exist
- `VERSION_NOT_FOUND`: Specific version not available
- `INVALID_VERSION`: Version format is invalid
- `CHECKSUM_MISMATCH`: Downloaded file doesn't match checksum
- `NETWORK_ERROR`: Network connectivity issue
- `RATE_LIMIT`: Too many requests
- `MAINTENANCE`: Registry temporarily unavailable

---

## CLI Commands

### Plugin Management Commands

#### plugin list

```bash
mbb plugin list [OPTIONS]

Options:
  --installed            Show only installed plugins
  --category TEXT        Filter by category
  --sort TEXT           Sort by (default: downloads)
  --limit INT           Maximum results
  --format TEXT         Output format (table, json, yaml)

Examples:
  mbb plugin list
  mbb plugin list --category diagram_renderer
  mbb plugin list --installed --format json
```

Output:
```
ID                    Name                   Version  Category            Rating
diagram-mermaid       Mermaid Diagram        1.0.0    diagram_renderer    4.9★
image-openai          OpenAI Image Gen       2.1.0    image_provider      4.7★
validator-structure   Structure Validator    0.9.2    validator           4.5★
```

#### plugin search

```bash
mbb plugin search QUERY [OPTIONS]

Options:
  --category TEXT       Filter by category
  --tag TEXT           Filter by tag (repeatable)
  --sort TEXT          Sort by
  --limit INT          Maximum results
  --format TEXT        Output format

Examples:
  mbb plugin search diagram
  mbb plugin search --category image_provider openai
  mbb plugin search --tag mermaid --sort rating
```

#### plugin info

```bash
mbb plugin info PLUGIN_ID [OPTIONS]

Options:
  --version TEXT       Show specific version
  --format TEXT        Output format (text, json, yaml)

Examples:
  mbb plugin info diagram-mermaid
  mbb plugin info diagram-mermaid --version 0.9.0
```

Output:
```
Name: Mermaid Diagram Renderer
ID: diagram-mermaid
Version: 1.0.0
Author: Markdown Book Builder Team

Description:
Render Mermaid diagrams to PNG/SVG with high quality output.

Category: diagram_renderer
Tags: diagram, visualization, mermaid

Rating: 4.9★ (1,234 ratings)
Downloads: 45,123

Homepage: https://github.com/mordanov/mbb-plugin-mermaid
Repository: https://github.com/mordanov/mbb-plugin-mermaid
Documentation: https://github.com/mordanov/mbb-plugin-mermaid/blob/main/README.md

Compatibility:
  MBB: >=0.1.0
  Python: >=3.13

Requirements:
  mermaid-cli: >=10.0
  puppeteer: >=20.0
```

#### plugin install

```bash
mbb plugin install PLUGIN [OPTIONS]

Arguments:
  PLUGIN               Plugin identifier, URL, or local path

Options:
  --version TEXT       Specific version to install
  --force              Overwrite existing installation
  --no-deps            Don't install dependencies
  --scope TEXT         Installation scope (system|project)

Examples:
  mbb plugin install diagram-mermaid
  mbb plugin install diagram-mermaid@0.9.0
  mbb plugin install https://github.com/user/plugin/releases/download/v1.0.0/plugin.tar.gz
  mbb plugin install ./my-local-plugin-1.0.0.tar.gz
```

Output:
```
Resolving dependencies...
  ✓ diagram-mermaid 1.0.0
    ├─ mermaid-cli >=10.0
    └─ puppeteer >=20.0

Installing diagram-mermaid 1.0.0...
  [████████████████████] 100%  (2.3 MB / 2.3 MB)
  ✓ Verifying checksum
  ✓ Extracting files
  ✓ Installing dependencies
  ✓ Testing installation

Successfully installed diagram-mermaid 1.0.0
```

#### plugin update

```bash
mbb plugin update [PLUGIN] [OPTIONS]

Arguments:
  PLUGIN               Plugin to update (optional, all if not specified)

Options:
  --check-only         Only check for updates
  --force              Force update even if latest

Examples:
  mbb plugin update
  mbb plugin update diagram-mermaid
  mbb plugin update --check-only
```

Output:
```
Checking for updates...
  diagram-mermaid: 1.0.0 → 1.1.0 (available)
  image-openai: 2.1.0 (up to date)
  validator-structure: 0.9.2 → 1.0.0 (available)

Update 2 plugins? [y/N] y

Updating diagram-mermaid to 1.1.0...
  [████████████████████] 100%
  ✓ Successfully updated

Updating validator-structure to 1.0.0...
  [████████████████████] 100%
  ✓ Successfully updated

All plugins updated!
```

#### plugin uninstall

```bash
mbb plugin uninstall PLUGIN [OPTIONS]

Options:
  --force              Skip confirmation

Examples:
  mbb plugin uninstall diagram-mermaid
  mbb plugin uninstall diagram-mermaid --force
```

#### plugin status

```bash
mbb plugin status [OPTIONS]

Options:
  --format TEXT        Output format (table, json)

Output:
ID                    Status      Version   Enabled  Updates
diagram-mermaid       Installed   1.0.0     ✓        1.1.0 available
image-openai          Installed   2.1.0     ✓        (up to date)
validator-structure   Installed   0.9.2     ✓        1.0.0 available
```

---

## Database Schema

### Local Plugin Cache

File: `~/.markdown_book_builder/cache/plugins.json`

```json
{
  "schema_version": "1.0",
  "last_updated": "2024-03-20T10:30:00Z",
  "plugins": {
    "diagram-mermaid": {
      "id": "diagram-mermaid",
      "name": "Mermaid Diagram Renderer",
      "installed": true,
      "installed_version": "1.0.0",
      "installed_at": "2024-01-15T10:00:00Z",
      "location": "/Users/user/.markdown_book_builder/plugins/diagram-mermaid",
      "scope": "system",
      "enabled": true,
      "manifest": { ... },
      "available_version": "1.1.0",
      "check_updates_at": "2024-03-20T10:30:00Z"
    }
  }
}
```

### Project Plugin Configuration

File: `./plugins/plugins.toml`

```toml
[plugins.diagram-mermaid]
enabled = true
version = "1.0.0"
scope = "project"

[plugins.diagram-mermaid.options]
output_format = "png"
quality = "high"
```

---

## Configuration

### Global Configuration

File: `~/.markdown_book_builder/config/plugins.toml`

```toml
[registry]
# Primary registry URL
url = "https://registry.mbb.dev"

# Cache TTL in seconds (how long to cache registry data)
cache_ttl = 3600

# Allow custom registries
allow_custom = true

# Verify plugin checksums before installation
verify_checksums = true

# Require GPG signatures for installations
require_signatures = false

[plugins]
# Global plugin options (inherited by all plugins)
timeout = 30
retry_count = 3

[custom_registries]
# Custom registry example
# internal = "https://registry.company.com"
```

---

## Error Handling

### Installation Errors

1. **Plugin not found**
   - User error: Mistyped plugin ID
   - Action: Suggest similar plugin names

2. **Version not compatible**
   - User error: Plugin requires newer MBB version
   - Action: Show required version and current version

3. **Dependency conflict**
   - System error: Conflicting dependencies
   - Action: Show conflict details and suggest solutions

4. **Network error**
   - External error: Can't reach registry
   - Action: Try offline cache, suggest retry later

5. **Checksum mismatch**
   - Security error: File may be corrupted
   - Action: Don't install, suggest retry or contact support

### Recovery Strategies

```python
def install_with_retry(plugin_id: str, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            return install_plugin(plugin_id)
        except NetworkError as e:
            if attempt < max_retries - 1:
                logger.warning(f"Attempt {attempt+1} failed, retrying...")
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise
        except ChecksumError:
            # Don't retry checksum errors
            raise
```

---

## Testing Strategy

### Unit Tests

```python
# tests/plugins/test_plugin_manifest.py
def test_plugin_manifest_validation():
    manifest = PluginManifest(...)
    assert manifest.validate() == (True, [])

def test_plugin_manifest_compatibility():
    manifest = PluginManifest(min_mbb_version="0.1.0")
    assert manifest.is_compatible("0.2.0")
    assert not manifest.is_compatible("0.0.1")
```

### Integration Tests

```python
# tests/integration/test_plugin_registry.py
def test_registry_search():
    registry = PluginRegistry()
    results = registry.search("diagram")
    assert len(results) > 0

def test_plugin_installation():
    registry = PluginRegistry()
    plugin = registry.install("diagram-mermaid")
    assert plugin.enabled
```

### End-to-End Tests

```bash
# tests/e2e/test_plugin_workflow.sh

# Test search
mbb plugin search diagram
assert_exit_code 0

# Test install
mbb plugin install diagram-mermaid
assert_exit_code 0

# Test list installed
mbb plugin list --installed
assert_contains "diagram-mermaid"

# Test uninstall
mbb plugin uninstall diagram-mermaid --force
assert_exit_code 0
```

---

## Migration Path

For existing plugins without proper metadata:

1. Create `plugin.toml` in plugin directory
2. Run validation: `mbb plugin validate my-plugin/`
3. Fix any issues
4. Package: `tar czf my-plugin-1.0.0.tar.gz my-plugin/`
5. Install: `mbb plugin install ./my-plugin-1.0.0.tar.gz`

---

## Performance Considerations

### Caching Strategy

- Cache registry metadata for 1 hour (configurable)
- Cache plugin listings locally
- Support offline mode with stale cache

### Network Optimization

- Gzip compression for API responses
- CDN distribution for large plugin files
- Parallel downloads for dependencies

### Scalability

- Support for 1000+ plugins in registry
- Sub-second search performance
- Minimal memory footprint for CLI

---

## Security Considerations

### Verification

- SHA256 checksums for all files
- Optional GPG signatures
- Registry integrity checks

### Isolation

- Plugins run in restricted context (future)
- Filesystem sandbox for file access
- Network access controlled per plugin

### Trust Model

- Verified badge for trusted authors
- Code review before registry inclusion
- Transparency in approval process

---

## Related Documentation

- [PLUGIN_DEVELOPMENT.md](../PLUGIN_DEVELOPMENT.md)
- [PLUGIN_REGISTRY.md](../PLUGIN_REGISTRY.md)
- [ADR 006: Plugin Registry Architecture](adr/006-plugin-registry-architecture.md)


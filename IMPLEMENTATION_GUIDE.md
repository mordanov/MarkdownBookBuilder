# Markdown Book Builder - Implementation Guide

**Project Status**: Phase 1 Bootstrap Complete ✅  
**Current Branch**: `worktree-phase-1-bootstrap`  
**Date**: 2026-07-13

## Current State

### ✅ Completed
- Phase 1 Bootstrap (35 files, ~1,200 LOC scaffolding)
- Project structure (src-layout, src/markdown_book_builder/)
- Python dependencies configured
- CLI command structure (build, validate, init, config, images)
- Core infrastructure (logging, errors, types, config schema)
- AST models (Pydantic-based Book, Chapter, Section, etc.)
- Pre-commit hooks configured (Ruff, mypy)

## Getting Started

### 1. Merge to Main
```bash
git checkout main
git merge origin/worktree-phase-1-bootstrap
git push origin main
```

### 2. Install Dependencies
```bash
uv sync
pre-commit install
```

### 3. Verify
```bash
source .venv/bin/activate
python -m markdown_book_builder --help
pytest
```

## Roadmap

| Phase | Tasks | Status | Focus |
|-------|-------|--------|-------|
| 1 | T001-T007 | ✅ DONE | Setup, dependencies, project structure |
| 2 | T008-T017 | ⏳ TODO | Config loader, test fixtures |
| 3 | T018-T028 | ⏳ TODO | CLI environment validation |
| 4 | T029-T037 | ⏳ TODO | AST implementation & tests |
| 5 | T038-T044 | ⏳ TODO | Document discovery |
| 6 | T045-T054 | ⏳ TODO | Full CLI commands |
| 7 | T055-T061 | ⏳ TODO | Config integration |
| 8 | T062-T069 | ⏳ TODO | Testing infrastructure |
| 9 | T070-T078 | ⏳ TODO | ADRs, docs, validation |

## Key Commands

```bash
# Code quality
ruff format src/ tests/
ruff check . --fix
mypy src/

# Testing
pytest
pytest --cov
ptw

# CLI
python -m markdown_book_builder --help
python -m markdown_book_builder build .
```

## Next Steps

1. **Merge Phase 1 Bootstrap** to main
2. **Install & verify** with `uv sync && pytest`
3. **Start Phase 2** - Config loader implementation
4. **Continue incrementally** through phases 3-9

See README.md for detailed setup instructions.

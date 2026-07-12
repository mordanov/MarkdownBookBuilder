# Phase 1 Bootstrap - Merge Checklist

## Pre-Merge Verification

- [x] Phase 1 bootstrap branch created: `worktree-phase-1-bootstrap`
- [x] All Phase 1 tasks completed (T001-T007)
- [x] 35 files created (scaffolding complete)
- [x] Tests directory structure ready
- [x] CLI commands wired (build, validate, init, config, images)
- [x] Core infrastructure implemented (errors, logging, types)
- [x] AST models defined (Pydantic-based)
- [x] Configuration schema created
- [x] Pre-commit hooks configured
- [x] README.md documentation complete
- [x] Implementation guide created
- [x] Branch pushed to origin

## Merge Steps

### Step 1: Prepare Main Branch
```bash
git checkout main
git pull origin main
git log --oneline -5  # Verify current state
```

### Step 2: Merge Phase 1 Bootstrap
```bash
# Option A: Regular merge (preserves commit history)
git merge origin/worktree-phase-1-bootstrap

# Option B: Squash merge (clean single commit)
git merge --squash origin/worktree-phase-1-bootstrap
git commit -m "Phase 1 Bootstrap: Project foundation setup"
```

### Step 3: Verify Merge
```bash
git log --oneline -10      # Check commits
git status                 # Verify clean state
ls -la src/               # Verify files exist
```

### Step 4: Push to Remote
```bash
git push origin main
```

## Post-Merge Setup

### Step 1: Install Dependencies
```bash
uv sync
```

### Step 2: Verify Installation
```bash
source .venv/bin/activate  # macOS/Linux
# or: .venv\Scripts\activate  # Windows

python -m markdown_book_builder --help
# Should show: Usage, Commands (build, validate, init, config)
```

### Step 3: Set Up Pre-Commit
```bash
pre-commit install
pre-commit run --all-files
# Should pass: Ruff format, Ruff check, mypy
```

### Step 4: Run Tests
```bash
pytest
pytest --cov
# Framework is in place; minimal tests initially
```

### Step 5: Code Quality Checks
```bash
ruff check . && ruff format --check . && mypy src/
# Should pass with no errors
```

## Verification Checklist

After merge and setup, verify:

- [ ] `python -m markdown_book_builder --help` works
- [ ] `python -m markdown_book_builder --verbose build .` runs (shows placeholder)
- [ ] `pytest` passes (test framework ready)
- [ ] `ruff check .` passes (no lint errors)
- [ ] `mypy src/` passes (no type errors)
- [ ] `pre-commit run --all-files` passes (hooks work)
- [ ] `.venv/` directory created
- [ ] All imports resolve correctly
- [ ] README.md renders correctly on GitHub

## Success Criteria

✅ All 35 files present in merged main  
✅ CLI commands available and functional  
✅ Tests framework working  
✅ Code quality tools integrated  
✅ Documentation accessible  
✅ Team can start Phase 2 development  

## Next Steps After Merge

1. **Day 1**: Verify setup on team machines
2. **Day 2**: Start Phase 2 implementation (config loader, test fixtures)
3. **Day 3+**: Continue through phases 3-9

## Troubleshooting

### Issue: `ModuleNotFoundError: markdown_book_builder`
**Solution**: Run `uv sync` and activate venv: `source .venv/bin/activate`

### Issue: Pre-commit hooks failing
**Solution**: Run `pre-commit install` and `pre-commit run --all-files`

### Issue: Type checking errors
**Solution**: Ensure mypy is installed: `uv sync` then `mypy src/`

### Issue: Ruff format/lint errors
**Solution**: Run `ruff format src/ tests/ && ruff check . --fix`

---

**Status**: Ready for merge  
**Branch**: `worktree-phase-1-bootstrap`  
**Commits**: 2 (Phase 1 + Implementation guide)

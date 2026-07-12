---
description: "Task list for project foundation phase"
---

# Tasks: Project Foundation

**Input**: Design documents from `/specs/001-project-foundation/`  
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story. Setup and Foundational phases must complete first before any user story work can begin.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, etc.)
- Include exact file paths in descriptions

## Path Conventions

- Single Python package: `markdown_book_builder/` at repository root
- Tests organized by type: `tests/unit/`, `tests/integration/`, `tests/contract/`
- Configuration: `pyproject.toml` and `.pre-commit-config.yaml`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, Python environment, and repository structure

- [ ] T001 Create directory structure per implementation plan: `markdown_book_builder/`, `tests/`, `docs/adr/`, etc.
- [ ] T002 [P] Initialize Python project with `pyproject.toml`, `uv.lock`, and core metadata
- [ ] T003 [P] Configure linting with Ruff: `.pre-commit-config.yaml` and tool config in `pyproject.toml`
- [ ] T004 [P] Configure type checking with mypy in `pyproject.toml` with strict mode
- [ ] T005 [P] Setup pytest framework and fixtures structure in `tests/`
- [ ] T006 [P] Create README.md with setup instructions and quick-start commands
- [ ] T007 [P] Initialize test fixtures directory structure: `tests/fixtures/`, `tests/fixtures/golden/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure and shared abstractions that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T008 Define custom exception hierarchy in `markdown_book_builder/core/errors.py`
- [ ] T009 [P] Setup logging system in `markdown_book_builder/core/logging.py` with CLI-appropriate output
- [ ] T010 [P] Define type aliases and constants in `markdown_book_builder/core/types.py`
- [ ] T011 Setup TOML configuration schema in `markdown_book_builder/config/models.py` (Pydantic models)
- [ ] T012 [P] Implement configuration loader in `markdown_book_builder/config/loader.py` with env var override support
- [ ] T013 Create sample `book.toml` and `.book.env` templates
- [ ] T014 Setup Typer CLI entry point in `markdown_book_builder/__main__.py`
- [ ] T015 [P] Create test fixtures for AST samples in `tests/fixtures/ast_samples.py`
- [ ] T016 [P] Create test fixtures for Markdown samples in `tests/fixtures/markdown_samples.py`
- [ ] T017 [P] Create test fixtures for config samples in `tests/fixtures/config_samples.py`

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Project Setup & Repository Initialization (Priority: P1)

**Goal**: Developers can clone the repo, run setup commands, and have a fully functional dev environment with all tools ready

**Independent Test**: Clone repo → run `uv sync` → verify `python -m markdown_book_builder --help` works → verify linting/type-checking pass → verify pytest runs

### Tests for User Story 1

- [ ] T018 [P] [US1] Integration test for environment setup in `tests/integration/test_environment_setup.py` (verify uv, python version, imports)
- [ ] T019 [P] [US1] Test CLI help output in `tests/contract/test_cli_help.py` (verify `--help` response time <100ms)
- [ ] T020 [P] [US1] Test linting/type-checking passes in `tests/contract/test_code_quality.py`

### Implementation for User Story 1

- [ ] T021 [P] [US1] Create `markdown_book_builder/__init__.py` with version and public API
- [ ] T022 [US1] Implement `build` command skeleton in `markdown_book_builder/cli/build.py` (depends on T021)
- [ ] T023 [US1] Implement `validate` command skeleton in `markdown_book_builder/cli/validate.py` (depends on T021)
- [ ] T024 [US1] Implement `init` command skeleton in `markdown_book_builder/cli/init.py` (depends on T021)
- [ ] T025 [US1] Implement `images` subcommand group in `markdown_book_builder/cli/images.py` (depends on T021)
- [ ] T026 [US1] Implement `config` command in `markdown_book_builder/cli/config.py` (depends on T012, T021)
- [ ] T027 [US1] Implement main CLI app in `markdown_book_builder/cli/main.py` that binds all commands (depends on T022-T026)
- [ ] T028 [US1] Add success validation: running pytest passes with baseline coverage >80% on core modules

**Checkpoint**: Environment is set up, CLI is functional, all tools work, developer can start development

---

## Phase 4: User Story 2 - Core AST Definition & Transformation (Priority: P1)

**Goal**: Define the internal AST representation that all processing stages operate on; this is the central abstraction for the entire system

**Independent Test**: Create AST instances → serialize/deserialize → verify round-trip fidelity → test transformations apply correctly

### Tests for User Story 2

- [ ] T029 [P] [US2] Unit tests for AST models in `tests/unit/test_ast_models.py` (verify Pydantic validation)
- [ ] T030 [P] [US2] Snapshot test for AST serialization/deserialization in `tests/unit/test_ast_serialization.py`
- [ ] T031 [P] [US2] Test AST transformations in `tests/unit/test_ast_transform.py` (verify tree modification without corruption)

### Implementation for User Story 2

- [ ] T032 [P] [US2] Define Book, Chapter, Section, Paragraph entities in `markdown_book_builder/ast_/models.py` (Pydantic BaseModel)
- [ ] T033 [P] [US2] Define CodeBlock and Image entities in `markdown_book_builder/ast_/models.py` (code syntax, alt text, captions)
- [ ] T034 [P] [US2] Define FrontMatter (YAML metadata) in `markdown_book_builder/ast_/models.py`
- [ ] T035 [US2] Implement AST utility functions in `markdown_book_builder/ast_/transform.py` (tree traversal, node queries, modification helpers)
- [ ] T036 [US2] Implement AST serialization (to JSON/dict) in `markdown_book_builder/ast_/models.py` (depends on T032-T035)
- [ ] T037 [US2] Implement AST deserialization (from JSON/dict) in `markdown_book_builder/ast_/models.py` with validation

**Checkpoint**: AST model is stable and extensible; all downstream features can now build plugins

---

## Phase 5: User Story 3 - Document Discovery & Ordering (Priority: P1)

**Goal**: System automatically discovers and orders Markdown files from a directory; all content is accessible without manual configuration

**Independent Test**: Provide sample directory structure → run discovery → verify files are ordered correctly → verify metadata is extracted

### Tests for User Story 3

- [ ] T038 [P] [US3] Unit test for file scanner in `tests/unit/test_discovery_scanner.py` (lexicographic ordering, recursive traversal)
- [ ] T039 [P] [US3] Unit test for metadata extraction in `tests/unit/test_discovery_metadata.py` (YAML front matter parsing)
- [ ] T040 [P] [US3] Integration test for full discovery flow in `tests/integration/test_document_discovery.py`

### Implementation for User Story 3

- [ ] T041 [P] [US3] Implement file scanner in `markdown_book_builder/discovery/scanner.py` (recursive traversal, lexicographic ordering, filter `.md` files)
- [ ] T042 [P] [US3] Implement front matter parser in `markdown_book_builder/discovery/metadata.py` (YAML extraction)
- [ ] T043 [US3] Implement discovery orchestrator in `markdown_book_builder/discovery/__init__.py` that returns ordered list with metadata (depends on T041, T042)
- [ ] T044 [US3] Integrate discovery into CLI `build` command in `markdown_book_builder/cli/build.py` (depends on T043)

**Checkpoint**: Input pipeline is functional; system can discover and organize book content

---

## Phase 6: User Story 4 - CLI Command Structure (Priority: P1)

**Goal**: Provide a clean, extensible CLI interface following Typer conventions with all core commands working as specified

**Independent Test**: Invoke each command with valid/invalid args → verify output, exit codes, help text are correct

### Tests for User Story 4

- [ ] T045 [P] [US4] Contract test for `build` command in `tests/contract/test_cli_build.py` (valid/invalid args, exit codes)
- [ ] T046 [P] [US4] Contract test for `validate` command in `tests/contract/test_cli_validate.py`
- [ ] T047 [P] [US4] Contract test for `init` command in `tests/contract/test_cli_init.py`
- [ ] T048 [P] [US4] Contract test for error handling in `tests/contract/test_cli_errors.py` (bad args, non-existent dirs, machine-readable output)

### Implementation for User Story 4

- [ ] T049 [US4] Implement `build` command full behavior in `markdown_book_builder/cli/build.py` with progress reporting (depends on T043, T027)
- [ ] T050 [US4] Implement `validate` command to check book structure in `markdown_book_builder/cli/validate.py` (depends on T043)
- [ ] T051 [US4] Implement `init` command to scaffold new book projects in `markdown_book_builder/cli/init.py` (depends on T013)
- [ ] T052 [US4] Implement `images clean` subcommand to manage image cache in `markdown_book_builder/cli/images.py`
- [ ] T053 [US4] Add error handling that returns non-zero exit codes and machine-readable error reports across all commands (depends on T008, T009, T049-T052)
- [ ] T054 [US4] Verify all CLI commands support `--help` with clear documentation and respond within <100ms (depends on T049-T053)

**Checkpoint**: CLI is production-ready for all Phase 1 operations

---

## Phase 7: User Story 5 - Configuration System (Priority: P2)

**Goal**: Users can configure builds via a `book.toml` file with environment variable overrides for secrets; all settings apply correctly

**Independent Test**: Create valid `book.toml` → load config → verify all settings applied → test invalid TOML error reporting

### Tests for User Story 5

- [ ] T055 [P] [US5] Unit test for TOML loading in `tests/unit/test_config_loading.py` (valid/invalid TOML, error reporting with line numbers)
- [ ] T056 [P] [US5] Unit test for env var override behavior in `tests/unit/test_config_env_override.py` (secrets from env)
- [ ] T057 [P] [US5] Integration test for config in build flow in `tests/integration/test_config_build_integration.py`

### Implementation for User Story 5

- [ ] T058 [P] [US5] Extend config schema in `markdown_book_builder/config/models.py` with all Phase 1 settings (output format, theme hooks, API keys)
- [ ] T059 [US5] Enhance loader to handle env var overrides in `markdown_book_builder/config/loader.py` for secrets like OPENAI_API_KEY (depends on T012, T058)
- [ ] T060 [US5] Integrate config loading into `build` command in `markdown_book_builder/cli/build.py` to apply loaded settings (depends on T059, T049)
- [ ] T061 [US5] Create sample book.toml template with all Phase 1 options in project root

**Checkpoint**: Configuration system is fully integrated into the build pipeline

---

## Phase 8: User Story 6 - Testing Infrastructure & Golden Files (Priority: P2)

**Goal**: Testing framework is in place with fixtures, snapshot tests, and golden files; developers can write reliable deterministic tests

**Independent Test**: Create sample tests → run with snapshots → verify capture/comparison works → check coverage reporting

### Tests for User Story 6

- [ ] T062 [P] [US6] Verify test fixtures are reusable in `tests/fixtures/` (sample AST, Markdown, config)
- [ ] T063 [P] [US6] Test snapshot capture/comparison in `tests/unit/test_snapshot_example.py` (create, verify, update)
- [ ] T064 [P] [US6] Test golden file comparison in `tests/integration/test_golden_files.py` (verify outputs match golden files)

### Implementation for User Story 6

- [ ] T065 [P] [US6] Populate golden file directory `tests/fixtures/golden/` with sample outputs (CLI help text, config parsing results, AST serialization)
- [ ] T066 [US6] Document testing best practices in `docs/testing.md` (fixtures, snapshots, golden files, pytest commands)
- [ ] T067 [US6] Configure pytest snapshot plugin in `pyproject.toml` (syrupy or similar)
- [ ] T068 [US6] Add pytest coverage configuration to `pyproject.toml` and verify >80% on core modules (AST, discovery, CLI)
- [ ] T069 [US6] Create pytest-watch configuration for local development in `pyproject.toml`

**Checkpoint**: Complete testing infrastructure is available for all future development

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements affecting the entire system

- [ ] T070 [P] Create ADR for AST-centric architecture in `docs/adr/001-ast-centric-design.md`
- [ ] T071 [P] Create ADR for configuration system design in `docs/adr/002-configuration-system.md`
- [ ] T072 [P] Create ADR for plugin architecture for future phases in `docs/adr/003-plugin-architecture.md`
- [ ] T073 Create CONTRIBUTING.md with development setup and workflow guidelines
- [ ] T074 Create TESTING.md with test running and writing guidelines
- [ ] T075 Verify all code passes Ruff formatting and linting: `ruff check . && ruff format --check .`
- [ ] T076 Verify all code passes mypy type checking: `mypy .`
- [ ] T077 Verify test suite passes with coverage report: `pytest --cov`
- [ ] T078 Final validation: Run quickstart from README.md on fresh clone (simulate new developer experience)

**Checkpoint**: Project foundation is complete and ready for Phase 2 (diagram rendering, image generation, exporters)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - **BLOCKS all user stories**
- **User Stories (Phase 3-8)**: ALL depend on Foundational phase completion
  - User Stories 1-4 are P1 (critical path)
  - User Stories 5-6 are P2 (can follow P1 or run in parallel with adequate staffing)
  - Stories can proceed in parallel once Foundational completes
- **Polish (Phase 9)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1** (Setup): Can start after Foundational - No dependencies on other stories
- **User Story 2** (AST): Can start after Foundational - No dependencies on other stories
- **User Story 3** (Discovery): Can start after Foundational - Integrates with US1 CLI but independent
- **User Story 4** (CLI): Can start after Foundational - Integrates with US1/US3 but independently testable
- **User Story 5** (Config): Can start after Foundational - Integrates with US1 CLI but independent
- **User Story 6** (Testing): Can start after Foundational - Pure infrastructure, no dependencies

### Within Each User Story

- Tests (if included) MUST be written first and FAIL before implementation
- Models before services
- Services/utilities before CLI integration
- Core implementation before CLI integration
- Story complete and passing tests before moving to next

### Parallel Opportunities

**Setup phase (Phase 1)**:
- All [P] tasks can run in parallel (T002-T007 independent)

**Foundational phase (Phase 2)**:
- [P] tasks can run in parallel: T009, T010, T012, T015, T016, T017
- Sequential dependencies: T008 → T009; T011 → T012, T013

**User Story phases (Phase 3-8)**:
- Once Foundational completes, all user stories can start in parallel (4 developers × P1 stories + 2 developers × P2 stories)
- Within each story: tests marked [P] can run together, models/entities marked [P] can develop in parallel
- Different stories by different team members enables maximum parallelism

**Recommended parallel team execution**:
1. Team completes Setup (1-2 days)
2. Team completes Foundational (1-2 days) - **CRITICAL GATE**
3. Divide developers:
   - Developer A: User Story 1 (Setup)
   - Developer B: User Story 2 (AST)
   - Developer C: User Story 3 (Discovery)
   - Developer D: User Story 4 (CLI)
   - Developer E: User Story 5 (Config)
   - Developer F: User Story 6 (Testing)
4. Stories complete in parallel, integrate in Polish phase

---

## Parallel Example: User Story 2 (AST)

```bash
# Launch all tests together (they don't depend on implementation):
Task: T029 - Unit tests for AST models in tests/unit/test_ast_models.py
Task: T030 - Snapshot test for AST serialization in tests/unit/test_ast_serialization.py
Task: T031 - Test AST transformations in tests/unit/test_ast_transform.py

# Launch all entity definitions together (same file but no conflicts):
Task: T032 - Define Book, Chapter, Section, Paragraph in models.py
Task: T033 - Define CodeBlock, Image in models.py
Task: T034 - Define FrontMatter in models.py

# Then sequentially (dependencies):
Task: T035 - Implement transformation utilities (depends on T032-T034)
Task: T036 - Implement serialization (depends on T035)
Task: T037 - Implement deserialization (depends on T036)
```

---

## Implementation Strategy

### MVP First (User Stories 1-4 Only - Minimal Viable Product)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Setup)
4. Complete Phase 4: User Story 2 (AST)
5. Complete Phase 5: User Story 3 (Discovery)
6. Complete Phase 6: User Story 4 (CLI)
7. **STOP and VALIDATE**: Test all 4 stories together, run full pipeline
8. Deploy/demo MVP

### Incremental Delivery (Add P2 Stories)

1. Deliver MVP (all P1 stories above)
2. Add User Story 5 (Config) → Test independently → Integrate
3. Add User Story 6 (Testing) → Test independently → Integrate
4. Run Polish phase improvements
5. **FINAL**: All Phase 1 requirements met, ready for Phase 2

### Suggested Scope for MVP

- **In MVP**: Setup, AST, Discovery, CLI (Users can build books end-to-end)
- **Add in Phase 1.1**: Configuration, Testing infrastructure (improves dev experience)
- **Defer to Phase 2**: Image generation, diagram rendering, multiple exporters

---

## Success Criteria Checklist

After all tasks complete:

- [ ] All test suite passes with >80% code coverage on core modules (AST, discovery, CLI)
- [ ] CLI responds to `--help` within <100ms with accurate documentation
- [ ] Document discovery completes for 100+ files within <1 second
- [ ] Sample book with 10+ chapters can be initialized and validated
- [ ] Configuration loading succeeds with valid TOML in <50ms; invalid configs fail with clear errors
- [ ] Developers can set up project with `uv sync` and have all tools ready in <2 minutes
- [ ] AST serialization/deserialization is lossless (round-trip fidelity 100%)
- [ ] All code passes `ruff check .`, `ruff format --check .`, and `mypy .`
- [ ] README.md quickstart can be followed by a fresh developer on clean clone
- [ ] ADRs document all major architectural decisions

---

## Notes

- [P] tasks = different files with no dependencies on incomplete tasks
- [Story] label maps task to specific user story (US1-US6) for traceability
- Each user story is independently completable and testable
- Verify tests fail before implementing them
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts without proper sequencing, cross-story dependencies that break independence
- Configuration and testing infrastructure are P2 - can follow core P1 stories

# Tasks: PDF Document Formatting Control

**Input**: Design documents from `specs/005-pdf-formatting/`
**Prerequisites**: plan.md ✓, spec.md ✓, research.md ✓, data-model.md ✓, contracts/ ✓

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files or independent additions)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Exact file paths included in every description

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: No new project or dependencies needed — this feature modifies existing files only.

- [x] T001 Read and understand existing `src/markdown_book_builder/config/models.py` and `src/markdown_book_builder/rendering/pandoc.py` before making changes

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Scaffold the `FormattingConfig` container and wire it into `BookConfig` and the rendering pipeline. All user stories depend on this phase.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [x] T002 Add empty `FormattingConfig` Pydantic model with stub `headings`, `page`, and `toc` fields (all `None | ...`) to `src/markdown_book_builder/config/models.py`
- [x] T003 Add `formatting: FormattingConfig = Field(default_factory=FormattingConfig)` to `BookConfig` in `src/markdown_book_builder/config/models.py` (depends T002)
- [x] T004 Refactor `PandocRenderer._get_xelatex_preamble()` in `src/markdown_book_builder/rendering/pandoc.py` to accept `FormattingConfig` and delegate to three sub-methods: `_heading_preamble()`, `_page_layout_preamble()`, `_hyperref_preamble()` — each returning a `str` block (empty string if not configured); compose final preamble from these three blocks plus existing font/polyglossia lines (depends T002)

**Checkpoint**: `BookConfig` accepts `[formatting]` TOML section (defaults to empty/None fields) and renderer has the new structure — existing builds still pass.

---

## Phase 3: User Story 1 — Heading Style Customization (Priority: P1) 🎯 MVP

**Goal**: H1–H6 headings render with configurable font size, bold/italic, text color, and background color defined in `book.toml`.

**Independent Test**: Build a PDF from a sample book with `[formatting.headings.h1]` setting `color = "#FFFFFF"` and `background = "#1a3a5c"` — inspect that H1 headings appear styled. Also verify default theme applies when `[formatting]` is absent.

### Implementation for User Story 1

- [x] T005 [US1] Add `HeadingStyleConfig` Pydantic model (fields: `font_size: int`, `bold: bool`, `italic: bool`, `color: str`, `background: str | None`) with a `@field_validator` normalizing HEX colors (strip `#`, uppercase, validate 3 or 6 hex digits) and checking `font_size` ∈ [6, 144] in `src/markdown_book_builder/config/models.py`
- [x] T006 [US1] Define `DEFAULT_HEADING_STYLES: dict[str, HeadingStyleConfig]` constant (H1=22pt white/#1a3a5c, H2=16pt #1a3a5c no-bg, H3=13pt #2c5282, H4=11pt #333333, H5=10pt #555555, H6=10pt non-bold #777777) and `get_effective_headings(config: FormattingConfig) -> dict[str, HeadingStyleConfig]` function that merges user config over defaults in `src/markdown_book_builder/config/models.py` (depends T005)
- [x] T007 [US1] Update `FormattingConfig.headings` type from stub to `dict[str, HeadingStyleConfig] = Field(default_factory=dict)` in `src/markdown_book_builder/config/models.py` (depends T005, T006)
- [x] T008 [US1] Implement `PandocRenderer._heading_preamble(formatting: FormattingConfig) -> str` in `src/markdown_book_builder/rendering/pandoc.py`: call `get_effective_headings()`, then for each H1–H6 emit `\usepackage{titlesec}`, `\usepackage{xcolor}` (once), and a `\titleformat{...}` block — use `\colorbox[HTML]{BG}{\parbox...}` when background is set, plain `\color[HTML]{FG}` otherwise (depends T007)

### Tests for User Story 1

- [x] T009 [P] [US1] Write unit tests for `HeadingStyleConfig` in `tests/unit/test_config_formatting.py`: valid HEX with and without `#`, 3-digit HEX, invalid HEX raises `ValidationError`, `font_size` out-of-range raises `ValidationError`, uppercase normalization
- [x] T010 [P] [US1] Write unit tests for heading preamble in `tests/unit/test_rendering_pandoc.py`: preamble contains `\usepackage{titlesec}`, H1 block contains correct color codes, H2 block has no `\colorbox` when `background=None`, default theme applied when `FormattingConfig()` is empty

**Checkpoint**: User Story 1 fully functional — H1–H6 headings are styled in generated PDF.

---

## Phase 4: User Story 2 — Full A4 Page Width Text Layout (Priority: P2)

**Goal**: PDF text block spans full A4 width with configurable margins (default 2.5 cm each side), replacing the current narrow Markdown-style column.

**Independent Test**: Build a PDF, measure the text column width — should be ~176 mm (A4 210 mm minus 2×17 mm). Override margins in `book.toml` and verify the change is reflected.

### Implementation for User Story 2

- [x] T011 [US2] Add `PageLayoutConfig` Pydantic model (fields: `paper_size: str = "a4"`, `margin_top/bottom/left/right: str = "2.5cm"`) with a `@field_validator` ensuring margin strings match `^\d+(\.\d+)?(cm|mm|in|pt)$` and are `> 0` in `src/markdown_book_builder/config/models.py`
- [x] T012 [US2] Update `FormattingConfig.page` type from stub to `PageLayoutConfig = Field(default_factory=PageLayoutConfig)` in `src/markdown_book_builder/config/models.py` (depends T011)
- [x] T013 [US2] Implement `PandocRenderer._page_layout_preamble(formatting: FormattingConfig) -> str` in `src/markdown_book_builder/rendering/pandoc.py`: emit `\usepackage[{paper_size}paper, top={margin_top}, bottom={margin_bottom}, left={margin_left}, right={margin_right}]{geometry}` using `PageLayoutConfig` values (depends T012)

### Tests for User Story 2

- [x] T014 [P] [US2] Write unit tests for `PageLayoutConfig` in `tests/unit/test_config_formatting.py`: valid margin formats (`2.5cm`, `1in`, `20mm`), invalid format raises `ValidationError`, zero value raises `ValidationError`, default values
- [x] T015 [P] [US2] Write unit tests for page layout preamble in `tests/unit/test_rendering_pandoc.py`: preamble contains `\usepackage{geometry}`, correct `a4paper` keyword, correct margin values from config

**Checkpoint**: User Stories 1 AND 2 both work — headings styled, text fills A4 width.

---

## Phase 5: User Story 3 — Interactive PDF Table of Contents (Priority: P3)

**Goal**: TOC entries in the generated PDF are clickable hyperlinks that navigate to the correct page.

**Independent Test**: Open the generated PDF in a PDF reader, click a TOC entry — the viewer jumps to the referenced page. Verify links are absent when `interactive = false`.

### Implementation for User Story 3

- [x] T016 [US3] Add `TocConfig` Pydantic model (fields: `enabled: bool = True`, `depth: int = 3`, `interactive: bool = True`) with `depth` validator ∈ [1, 6] in `src/markdown_book_builder/config/models.py`
- [x] T017 [US3] Update `FormattingConfig.toc` type from stub to `TocConfig = Field(default_factory=TocConfig)` in `src/markdown_book_builder/config/models.py` (depends T016)
- [x] T018 [US3] Implement `PandocRenderer._hyperref_preamble(formatting: FormattingConfig) -> str` in `src/markdown_book_builder/rendering/pandoc.py`: return `\usepackage[hidelinks]{hyperref}` when `toc.interactive=True`, empty string otherwise; ensure `hyperref` is last in the composed preamble (after titlesec, geometry, xcolor) (depends T017)

### Tests for User Story 3

- [x] T019 [P] [US3] Write unit tests for `TocConfig` in `tests/unit/test_config_formatting.py`: default values, `depth` out-of-range raises `ValidationError`
- [x] T020 [P] [US3] Write unit tests for hyperref preamble in `tests/unit/test_rendering_pandoc.py`: preamble contains `\usepackage[hidelinks]{hyperref}` when `interactive=True`; preamble does NOT contain `hyperref` when `interactive=False`; `hyperref` appears after `titlesec` and `geometry` in the combined preamble

**Checkpoint**: All three user stories functional — styled headings, full-width A4, clickable TOC.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Integration tests, user-facing documentation, and template updates.

- [x] T021 [P] Add integration test for full build with all `[formatting]` sections configured in `tests/integration/test_cli_build.py`: book with `[formatting.headings.h1]`, `[formatting.page]`, `[formatting.toc]` builds without error and produces a PDF file
- [x] T022 [P] Add integration test for validation error on invalid HEX color in `tests/integration/test_cli_build.py`: `book.toml` with `color = "#ZZZZZZ"` causes build to exit with non-zero code and prints `ConfigurationError` message
- [x] T023 [P] Add commented `[formatting]` example block to `book.toml` template showing h1 style, page margins, and toc config with inline comments
- [x] T024 [P] Add "PDF Formatting" section to `USER_GUIDE.md` covering: default theme, customizing headings, changing margins, disabling interactive TOC, and error messages

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies — start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 — BLOCKS all user stories
  - T002 → T003 → T004 (sequential within phase)
- **Phase 3 (US1)**: Depends on Phase 2 completion
  - T005 → T006 → T007 → T008 (sequential chain)
  - T009, T010 can run in parallel once T008 exists
- **Phase 4 (US2)**: Depends on Phase 2 completion (independent of Phase 3)
  - T011 → T012 → T013 (sequential)
  - T014, T015 in parallel once T013 exists
- **Phase 5 (US3)**: Depends on Phase 2 completion (independent of US1, US2)
  - T016 → T017 → T018 (sequential)
  - T019, T020 in parallel once T018 exists
- **Phase 6 (Polish)**: Depends on Phases 3+4+5 completion
  - T021–T024 all parallelizable

### User Story Dependencies

- **US1 (P1)**: Can start after Foundational — no dependency on US2/US3
- **US2 (P2)**: Can start after Foundational — no dependency on US1/US3
- **US3 (P3)**: Can start after Foundational — no dependency on US1/US2

---

## Parallel Execution Examples

### Parallel after Phase 2: All Three Stories

```
Developer A: T005 → T006 → T007 → T008  (US1 implementation)
Developer B: T011 → T012 → T013         (US2 implementation)
Developer C: T016 → T017 → T018         (US3 implementation)
```

### Parallel Within User Story 1

```
After T008:
  Task T009: HeadingStyleConfig validation tests  (tests/unit/test_config_formatting.py)
  Task T010: Heading preamble tests               (tests/unit/test_rendering_pandoc.py)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 (T001)
2. Complete Phase 2 (T002–T004) — foundational wiring
3. Complete Phase 3 (T005–T010) — heading styles
4. **STOP and VALIDATE**: Build a real book, inspect H1–H6 styling in PDF
5. Optionally: T023 (update book.toml template) before sharing

### Incremental Delivery

1. Phase 1 + 2 → foundation ready, existing builds unchanged
2. Phase 3 → styled headings (US1 MVP) ✓
3. Phase 4 → full-width A4 layout (US2) ✓
4. Phase 5 → clickable TOC (US3) ✓
5. Phase 6 → polish, docs, integration tests ✓

---

## Notes

- [P] tasks = different files or logically independent additions — safe to parallelize
- Tasks T002–T004 must run sequentially (each depends on the previous)
- `hyperref` must be placed last in the composed preamble (T018) to avoid LaTeX package conflicts
- HEX colors in LaTeX use uppercase 6-digit format without `#` — normalizer in T005 handles conversion
- Existing `book.toml` files without `[formatting]` section will use default values — no breaking changes
- Total tasks: 24 | US1: 6 | US2: 5 | US3: 5 | Foundational: 3 | Setup: 1 | Polish: 4

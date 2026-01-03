# SpreadsheetDL v4.0 Refactoring Roadmap

**Created**: 2026-01-03
**Branch**: `refactor/v4.0-spreadsheetdl`
**Target**: Complete universal spreadsheet definition format with MCP server

---

## Overview

This roadmap implements SpreadsheetDL v4.0 through **incremental refactoring** of the existing v2.0.0 codebase.

**Decision**: REFACTOR (not rewrite) based on:
- 70%+ code is production-ready and reusable
- 1,275+ tests provide executable specification
- 500 KB documentation preserved
- Estimated effort: 95 hours (vs 300+ for rewrite)

---

## Phase 1: Foundation (Days 1-5)

### 1.1 Dataclass Modernization (Day 1-2)
**Files**: All schema/*.py, builder.py, charts.py
**Changes**:
- Add `frozen=True` to all value object dataclasses
- Add `__slots__=True` where beneficial
- Update any mutable default patterns
- Ensure all tests pass

**Modules to update**:
```
src/spreadsheet_dl/schema/styles.py      # 20+ dataclasses
src/spreadsheet_dl/schema/conditional.py # 15+ dataclasses
src/spreadsheet_dl/schema/advanced.py    # 10+ dataclasses
src/spreadsheet_dl/builder.py            # 9 dataclasses
src/spreadsheet_dl/charts.py             # 12 dataclasses
src/spreadsheet_dl/currency.py           # 3 dataclasses (Currency already frozen)
```

**Test command**: `uv run pytest tests/test_schema.py tests/test_builder.py -v`

### 1.2 YAML Loader Enhancement (Day 3-4)
**File**: `src/spreadsheet_dl/schema/loader.py`
**Changes**:
- Add PatternFill parsing
- Add GradientFill parsing
- Fix font weight/color parsing (use enums)
- Fix underline/strikethrough (use enums, not booleans)
- Add text rotation, wrap text, shrink to fit

**Test command**: `uv run pytest tests/test_themes.py -v`

### 1.3 Theme Variant Support (Day 5)
**Files**:
- `src/spreadsheet_dl/schema/loader.py`
- `src/spreadsheet_dl/themes/*.yaml`

**Changes**:
- Add theme variant loader (`variants:` section)
- Create dark mode variant for default theme
- Add variant switching in ThemeLoader

---

## Phase 2: Core Evolution (Days 6-15)

### 2.1 Builder Improvements (Day 6-8)
**File**: `src/spreadsheet_dl/builder.py`
**Changes**:
- Implement actual cell merge rendering (colspan/rowspan)
- Add named range integration to FormulaBuilder
- Add formula syntax validation
- Add circular reference detection

**Test command**: `uv run pytest tests/test_builder.py -v`

### 2.2 Conditional Format Application (Day 9-10)
**File**: `src/spreadsheet_dl/renderer.py`
**Changes**:
- Apply ConditionalFormat during render (not just store)
- Support color scales, data bars, icon sets
- Add rule priority handling

**Test command**: `uv run pytest tests/test_renderer.py -v`

### 2.3 Data Validation Application (Day 11-12)
**File**: `src/spreadsheet_dl/renderer.py`
**Changes**:
- Apply DataValidation during render
- Support all validation types (list, number, date, custom)
- Add input messages and error alerts

### 2.4 Chart Rendering (Day 13-15)
**Files**:
- `src/spreadsheet_dl/charts.py`
- `src/spreadsheet_dl/renderer.py`

**Changes**:
- Implement chart rendering to ODS
- Support 60+ chart types
- Add 3D chart rotation
- Add sparkline rendering

---

## Phase 3: MCP Expansion (Days 16-25)

### 3.1 MCP Tool Registry (Day 16-17)
**File**: `src/spreadsheet_dl/mcp_server.py`
**Changes**:
- Create MCPToolRegistry class
- Add decorator-based tool registration
- Implement tool discovery system

### 3.2 Cell/Style Tools (Day 18-20)
**New tools**:
```
cell_get, cell_set, cell_clear, cell_batch_update
style_list, style_get, style_apply
format_cells, format_number, format_font
```

### 3.3 Structure Tools (Day 21-23)
**New tools**:
```
row_insert, row_delete, column_insert, column_delete
merge_cells, unmerge_cells
freeze_set, freeze_clear
sheet_create, sheet_delete, sheet_copy
```

### 3.4 Advanced Tools (Day 24-25)
**New tools**:
```
chart_create, chart_update, sparkline_create
validation_create, cf_create
named_range_create, table_create
```

---

## Phase 4: New Capabilities (Days 26-35)

### 4.1 Streaming I/O (Day 26-28)
**New module**: `src/spreadsheet_dl/streaming.py`
**Changes**:
- StreamingReader for large files (100k+ rows)
- StreamingWriter for chunked output
- Memory-efficient cell iteration

### 4.2 Round-Trip Serialization (Day 29-32)
**New module**: `src/spreadsheet_dl/roundtrip.py`
**Changes**:
- ODS → Builder reconstruction
- Preserve styles, formulas, charts
- Semantic metadata restoration

### 4.3 Format Adapters (Day 33-35)
**New directory**: `src/spreadsheet_dl/adapters/`
**Files**:
```
adapters/__init__.py
adapters/base.py       # Abstract SpreadsheetAdapter
adapters/ods.py        # ODS-specific (extracted from ods_generator)
adapters/xlsx.py       # XLSX via openpyxl
adapters/csv.py        # CSV with type preservation
```

---

## Phase 5: Polish (Days 36-40)

### 5.1 Complete MCP Coverage (Day 36-37)
- Expand to 145 tools
- Add batch operations
- Add query tools

### 5.2 Documentation Update (Day 38-39)
- Update ARCHITECTURE.md for v4.0
- Update API documentation
- Create migration guide from v2.0

### 5.3 Performance Optimization (Day 40)
- Profile critical paths
- Optimize hot loops
- Add caching where beneficial

---

## Success Criteria

### Phase 1 Complete When:
- [ ] All dataclasses use frozen=True and __slots__
- [ ] YAML loader parses all style properties
- [ ] Dark mode theme variant works
- [ ] All existing tests pass

### Phase 2 Complete When:
- [ ] Cell merging renders correctly
- [ ] Conditional formats apply to output
- [ ] Data validation applies to output
- [ ] Charts render to ODS
- [ ] 60+ chart types supported

### Phase 3 Complete When:
- [ ] MCP tool registry operational
- [ ] 50+ new MCP tools implemented
- [ ] Cell/style/structure tools complete
- [ ] All tools have tests

### Phase 4 Complete When:
- [ ] Streaming handles 100k+ rows
- [ ] Round-trip preserves 95%+ fidelity
- [ ] Format adapters abstract ODS-specific code
- [ ] XLSX and CSV adapters functional

### Phase 5 Complete When:
- [ ] 145 MCP tools implemented
- [ ] Documentation updated
- [ ] Performance benchmarks pass
- [ ] v4.0 release ready

---

## Files to Preserve (Do Not Modify Without Reason)

These files are 95%+ reusable and should be touched minimally:

```
src/spreadsheet_dl/schema/styles.py      # Core style definitions
src/spreadsheet_dl/schema/units.py       # Unit handling
src/spreadsheet_dl/schema/validation.py  # Schema validation
src/spreadsheet_dl/themes/*.yaml         # Theme definitions
tests/*                                    # All test files
docs/*                                     # All documentation
.claude/*                                  # Agent/command configs
```

---

## Testing Strategy

1. **Run tests after every file change**
2. **Never commit with failing tests**
3. **Add tests for new functionality before implementation**
4. **Keep test coverage above 80%**

Commands:
```bash
uv run pytest                           # Full suite
uv run pytest tests/test_schema.py -v   # Schema tests
uv run pytest tests/test_builder.py -v  # Builder tests
uv run pytest tests/test_mcp_server.py  # MCP tests
uv run ruff check .                     # Linting
uv run mypy src/                        # Type checking
```

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Breaking existing functionality | Run full test suite after each change |
| ODS format compatibility | Keep odfpy dependency, test with LibreOffice |
| MCP protocol changes | Follow MCP spec strictly |
| Performance regression | Benchmark before/after Phase 5 |
| Documentation drift | Update docs in same PR as code changes |

---

## Notes

- All work on `refactor/v4.0-spreadsheetdl` branch
- Regular commits with conventional format
- PR to main after each phase complete
- Keep main branch stable at all times

# Finance Tracker - Dual-Audience Requirements (Human + AI/LLM)

**Document Version:** 1.0.0
**Date:** 2025-12-28
**Parent Document:** 2025-12-28-comprehensive-requirements.md
**Status:** Addendum

---

## Executive Summary

This addendum specifies requirements for dual-audience support, ensuring spreadsheets and financial data are optimally accessible to both human users (visual, formatted views) and AI/LLM systems (structured, semantic representations).

Modern finance applications must serve two distinct audiences with different needs:

| Audience | Needs | Optimal Format |
|----------|-------|----------------|
| **Humans** | Visual clarity, colors, charts, readable layouts | ODS with themes, conditional formatting, charts |
| **AI/LLMs** | Structure, semantics, relationships, context | JSON/YAML with metadata, natural language descriptions |

---

## Table of Contents

1. [AI/LLM Integration Requirements](#1-aillm-integration-requirements)
2. [Human Rendering Requirements](#2-human-rendering-requirements)
3. [Dual Export Requirements](#3-dual-export-requirements)
4. [Gap Analysis](#4-gap-analysis)
5. [Implementation Examples](#5-implementation-examples)

---

## 1. AI/LLM Integration Requirements

### FR-AI-001: AI-Optimized Data Export
**Priority:** P1 (High)
**Status:** Not Implemented

The system SHALL provide AI/LLM-optimized exports that preserve all semantic meaning:

**Capabilities:**
- Export spreadsheet content in structured JSON format
- Include explicit semantic metadata for every cell
- Preserve formula logic in both ODS syntax AND natural language
- Include formatting as structured attributes (not visual-only)
- Provide cell relationships and dependencies graph
- Include contextual descriptions of each section
- Tag data with business semantics

**Acceptance Criteria:**
- AC1: JSON export includes all data from ODS with zero loss
- AC2: Every formula has natural language description
- AC3: Cell semantic tags enable AI understanding of purpose
- AC4: Export validates against JSON Schema
- AC5: Round-trip conversion (ODS → JSON → ODS) preserves data

**Example Structure:**
```json
{
  "version": "1.0",
  "type": "budget_spreadsheet",
  "metadata": {
    "month": "2025-01",
    "year": 2025,
    "created": "2025-01-01T00:00:00Z",
    "template": "50-30-20",
    "theme": "default",
    "currency": "USD"
  },
  "sheets": [
    {
      "name": "Expense Log",
      "purpose": "Track individual expense transactions",
      "row_count": 50,
      "columns": [
        {
          "id": "A",
          "name": "Date",
          "semantic_type": "transaction_date",
          "data_type": "date",
          "format": "YYYY-MM-DD",
          "description": "Date when expense occurred"
        },
        {
          "id": "B",
          "name": "Category",
          "semantic_type": "expense_category",
          "data_type": "enum",
          "values": ["Housing", "Groceries", "Transportation"],
          "description": "Budget category for this expense"
        },
        {
          "id": "C",
          "name": "Description",
          "semantic_type": "transaction_description",
          "data_type": "string",
          "description": "Human-readable description of purchase"
        },
        {
          "id": "D",
          "name": "Amount",
          "semantic_type": "expense_amount",
          "data_type": "currency",
          "format": "$#,##0.00",
          "description": "Cost of this expense in USD"
        }
      ],
      "rows": [
        {
          "row_number": 2,
          "semantic_type": "expense_entry",
          "cells": {
            "A": {"value": "2025-01-15", "formatted": "2025-01-15"},
            "B": {"value": "Groceries", "formatted": "Groceries"},
            "C": {"value": "Whole Foods", "formatted": "Whole Foods"},
            "D": {
              "value": 127.53,
              "formatted": "$127.53",
              "currency": "USD",
              "semantic_note": "grocery_expense"
            }
          }
        }
      ],
      "formulas": [
        {
          "cell": "D50",
          "formula": "=SUM(D2:D49)",
          "natural_language": "Sum of all individual expense amounts for the month",
          "dependencies": ["D2:D49"],
          "result_type": "currency",
          "semantic_type": "monthly_total_expenses",
          "business_meaning": "Total amount spent across all categories this month"
        }
      ],
      "conditional_formatting": [
        {
          "range": "D2:D49",
          "rule": "cell_value > VLOOKUP(B2, Budget!A:B, 2)",
          "style": {"color": "red", "bold": true},
          "semantic_meaning": "over_budget_expense",
          "natural_language": "Highlight expenses that exceed their category budget"
        }
      ]
    }
  ],
  "relationships": [
    {
      "type": "budget_vs_actual",
      "source_sheet": "Expense Log",
      "source_cell": "D50",
      "target_sheet": "Budget",
      "target_cell": "B2",
      "relationship": "actual total is compared against budgeted amount"
    }
  ]
}
```

---

### FR-AI-002: Natural Language Formula Descriptions
**Priority:** P1 (High)
**Status:** Not Implemented

The system SHALL generate and maintain natural language descriptions for all formulas:

**Capabilities:**
- Auto-generate English descriptions of formulas
- Explain what each formula calculates
- Explain WHY the formula is needed (business purpose)
- Include formula dependencies in plain language
- Support bidirectional conversion:
  - Formula → Natural Language
  - Natural Language → Formula (AI-assisted)
- Localization support for multiple languages

**Acceptance Criteria:**
- AC1: Every formula has accurate natural language description
- AC2: Descriptions include business context, not just mechanics
- AC3: Complex nested formulas broken down step-by-step
- AC4: AI can generate formulas from natural language with >90% accuracy

**Examples:**

| Formula | Natural Language Description |
|---------|------------------------------|
| `=SUM(E2:E49)` | "Calculate the total of all expenses for the month by adding up individual expense amounts from rows 2 through 49" |
| `=SUMIF(B:B,"Groceries",D:D)` | "Find the total amount spent on Groceries by summing all amounts in column D where the category in column B equals 'Groceries'" |
| `=IF(E50>B2,"Over Budget","On Track")` | "Compare total monthly spending (E50) against the budgeted amount (B2). If spending exceeds budget, display 'Over Budget', otherwise show 'On Track'" |
| `=VLOOKUP(B2,Budget!A:B,2,FALSE)` | "Look up the budgeted amount for this expense's category by finding the category name (B2) in the Budget sheet's category list (A:B) and returning the corresponding budget amount (column 2)" |

---

### FR-AI-003: Semantic Cell Tagging
**Priority:** P1 (High)
**Status:** Not Implemented

The system SHALL tag every cell with semantic meaning:

**Semantic Tag Categories:**
- **Data Role**: `input`, `calculated`, `total`, `subtotal`, `header`, `label`
- **Business Type**: `expense_amount`, `budget_allocation`, `category_name`, `transaction_date`, `account_balance`
- **Temporal**: `current_month`, `ytd`, `historical`, `projected`
- **Financial**: `debit`, `credit`, `balance`, `income`, `expense`
- **Aggregate**: `sum`, `average`, `max`, `min`, `count`

**Capabilities:**
- Assign semantic tags during spreadsheet generation
- Export tags in AI-optimized JSON
- Enable semantic queries ("show me all expense_amount cells")
- Support custom tag vocabularies
- Validate tag consistency

**Acceptance Criteria:**
- AC1: 100% of data cells have semantic tags
- AC2: Tags follow controlled vocabulary
- AC3: AI can filter/query by semantic type
- AC4: Tags exported in all AI-friendly formats

---

### FR-AI-004: LLM-Friendly Diff Format
**Priority:** P2 (Medium)
**Status:** Not Implemented

The system SHALL generate human and AI-readable diffs of spreadsheet changes:

**Capabilities:**
- Semantic diff (not just cell-level diff)
- Natural language change descriptions
- Impact analysis ("this change affects 15 formulas")
- Category-level summaries
- Before/after comparisons with context

**Example Output:**
```markdown
## Budget Changes: January 2025

### Summary
- 3 categories updated
- 12 new expenses added
- 1 formula modified

### Category Changes
- **Groceries Budget**: Increased from $400 → $450 (+12.5%)
  - Impact: 8 existing expenses now under budget
- **Entertainment Budget**: Decreased from $200 → $150 (-25%)
  - Impact: 3 expenses now flagged as over budget

### New Expenses
1. 2025-01-15: Whole Foods (Groceries) - $127.53
2. 2025-01-16: Uber (Transportation) - $23.45
...

### Formula Changes
- Cell D50: Changed from `=SUM(D2:D49)` to `=SUM(D2:D60)`
  - Reason: Extended expense log from 48 to 59 rows
  - Impact: Monthly total now includes additional entries
```

**Acceptance Criteria:**
- AC1: Diff highlights semantic changes
- AC2: Impact analysis accurate
- AC3: Natural language descriptions clear
- AC4: JSON and Markdown output formats

---

### FR-AI-005: Conversational Query Interface
**Priority:** P2 (Medium)
**Status:** Not Implemented

The system SHALL support natural language questions about budgets:

**Example Queries:**
- "How much did I spend on groceries last month?"
- "Am I on track to meet my budget?"
- "What categories am I over budget in?"
- "Show me all expenses over $100"
- "What's my average daily spending?"
- "When was my last dining out expense?"
- "Compare this month to last month"

**Response Format:**
```json
{
  "query": "How much did I spend on groceries last month?",
  "understanding": {
    "intent": "category_total_query",
    "category": "Groceries",
    "time_period": "2024-12",
    "confidence": 0.95
  },
  "answer": {
    "value": 456.78,
    "formatted": "$456.78",
    "unit": "USD",
    "natural_language": "You spent $456.78 on groceries in December 2024"
  },
  "context": {
    "budget": 500.00,
    "variance": -43.22,
    "variance_percent": -8.6,
    "status": "under_budget"
  },
  "supporting_data": {
    "transaction_count": 12,
    "largest_expense": {
      "date": "2024-12-23",
      "description": "Costco",
      "amount": 187.32
    }
  }
}
```

**Acceptance Criteria:**
- AC1: Supports 50+ common query types
- AC2: Returns structured + natural language responses
- AC3: Handles ambiguity with clarifying questions
- AC4: Includes context and supporting data

---

### FR-AI-006: Visual + Semantic Dual Export
**Priority:** P1 (High)
**Status:** Not Implemented

The system SHALL generate paired outputs for every budget:

**Outputs:**
1. **Human Output**: `budget-2025-01.ods` (visual, formatted ODS)
2. **AI Output**: `budget-2025-01.ai.json` (structured JSON with semantics)

**Requirements:**
- 1:1 correspondence between representations
- Both generated simultaneously
- Consistency validation between formats
- Version synchronization
- Round-trip conversion support

**Acceptance Criteria:**
- AC1: Both formats generated in single operation
- AC2: Validator confirms consistency
- AC3: Changes to ODS trigger JSON regeneration
- AC4: No data loss in either direction

---

### FR-AI-007: Formatting Metadata Export
**Priority:** P2 (Medium)
**Status:** Not Implemented

The system SHALL export all formatting as structured metadata:

**Formatting Metadata Structure:**
```json
{
  "cell": "D25",
  "visual_formatting": {
    "font": {"family": "Arial", "size": 12, "bold": true},
    "background_color": "#FF0000",
    "text_color": "#FFFFFF",
    "border": {"style": "solid", "width": 1}
  },
  "semantic_formatting": {
    "meaning": "over_budget_warning",
    "reason": "expense exceeds category budget",
    "condition": "IF(D25 > VLOOKUP(B25, Budget!A:B, 2), RED, DEFAULT)",
    "natural_language": "This cell is highlighted red because the expense amount exceeds the budgeted amount for this category"
  }
}
```

**Acceptance Criteria:**
- AC1: All conditional formatting rules exported
- AC2: Color meanings documented
- AC3: Font/style semantics included
- AC4: Business logic behind formatting explained

---

### FR-AI-008: Context-Aware Data Serialization
**Priority:** P1 (High)
**Status:** Not Implemented

The system SHALL include comprehensive context with every export:

**Context Elements:**
- Time period (month, year, date range)
- User preferences and settings
- Template used
- Theme applied
- Data provenance (source CSV files, import dates)
- Version information
- Related files (previous months, YTD summaries)

**Example:**
```json
{
  "context": {
    "temporal": {
      "period_type": "monthly",
      "month": 1,
      "year": 2025,
      "fiscal_year": 2025,
      "is_current": true
    },
    "provenance": {
      "created": "2025-01-01T10:30:00Z",
      "last_modified": "2025-01-15T14:22:00Z",
      "source_files": [
        {"file": "chase-2025-01.csv", "imported": "2025-01-05", "rows": 23},
        {"file": "bofa-2025-01.csv", "imported": "2025-01-06", "rows": 15}
      ]
    },
    "configuration": {
      "template": "50-30-20",
      "theme": "default",
      "locale": "en_US",
      "currency": "USD"
    }
  }
}
```

---

### FR-AI-009: MCP Server Integration
**Priority:** P2 (Medium)
**Status:** Documented (setup guide exists, native server not implemented)

The system SHALL provide a native MCP server for AI/LLM integration:

**MCP Tools to Expose:**

1. **analyze_budget**
   ```json
   {
     "name": "analyze_budget",
     "description": "Analyze a budget file and return spending summary",
     "inputSchema": {
       "type": "object",
       "properties": {
         "file_path": {"type": "string"},
         "analysis_type": {"enum": ["summary", "detailed", "trends"]}
       }
     }
   }
   ```

2. **add_expense**
   ```json
   {
     "name": "add_expense",
     "description": "Add a new expense to the budget",
     "inputSchema": {
       "type": "object",
       "properties": {
         "date": {"type": "string", "format": "date"},
         "category": {"type": "string"},
         "description": {"type": "string"},
         "amount": {"type": "number"}
       }
     }
   }
   ```

3. **query_budget**
   ```json
   {
     "name": "query_budget",
     "description": "Answer natural language questions about budget",
     "inputSchema": {
       "type": "object",
       "properties": {
         "question": {"type": "string"},
         "file_path": {"type": "string"}
       }
     }
   }
   ```

4. **get_spending_trends**
5. **compare_periods**
6. **generate_report**

**Security:**
- File access restrictions (only configured budget directories)
- Authentication required
- Rate limiting
- Audit logging

**Acceptance Criteria:**
- AC1: MCP server runs as standalone process
- AC2: All 6+ tools implemented
- AC3: Returns structured responses
- AC4: Handles errors gracefully
- AC5: Works with Claude Desktop and other MCP clients

---

### FR-AI-010: AI Training Data Export
**Priority:** P3 (Low)
**Status:** Not Implemented

The system SHALL support privacy-preserving AI training data export:

**Capabilities:**
- Export anonymized budget patterns
- Provide example expense categorizations
- Generate synthetic budget data
- Remove PII while preserving structure
- Support differential privacy

**Use Cases:**
- Train auto-categorization models
- Generate test data
- Share example budgets
- Improve AI assistants

---

### FR-AI-011: Bidirectional AI Sync
**Priority:** P2 (Medium)
**Status:** Not Implemented

The system SHALL allow AI assistants to update budgets:

**Capabilities:**
- AI can add expenses via API
- AI can categorize transactions
- AI can suggest budget adjustments
- All changes validated before applying
- Audit log distinguishes AI vs human changes
- Collaborative editing support

**Example Flow:**
1. User tells AI: "I spent $45 on dinner at Olive Garden"
2. AI calls `add_expense` tool
3. System validates (date valid, amount positive, category exists)
4. Expense added with metadata: `{"added_by": "ai", "confidence": 0.95}`
5. User reviews AI changes in daily summary

---

## 2. Human Rendering Requirements

### FR-HUMAN-001: Optimized Visual Rendering
**Priority:** P0 (Critical)
**Status:** Implemented (ODS generation)

The system SHALL generate visually optimized ODS files for human viewing:

**Visual Features:**
- Professional themes with color palettes
- Conditional formatting for at-a-glance insights
- Cell borders and grouping for structure
- Bold headers and section titles
- Color-coded categories
- Charts and visualizations
- Responsive column widths
- Print-optimized layouts

**Acceptance Criteria:**
- AC1: ODS files rated 8+ out of 10 for visual appeal
- AC2: Critical information visible without scrolling
- AC3: Color scheme follows accessibility guidelines
- AC4: Prints correctly on standard paper

---

### FR-HUMAN-002: Interactive Features
**Priority:** P2 (Medium)
**Status:** Not Implemented

The system SHALL support interactive features in ODS:

**Features:**
- Dropdown menus for categories
- Data validation for amounts
- Comments and notes
- Cell protection (formulas locked, data editable)
- Named ranges for readability
- Sheet tabs with meaningful names

---

### FR-HUMAN-003: Dashboard View
**Priority:** P2 (Medium)
**Status:** Partial (analytics exist, not in ODS)

The system SHALL include a dashboard sheet in ODS:

**Dashboard Elements:**
- Monthly spending summary (total, by category)
- Budget vs actual comparison chart
- Top 5 expenses
- Spending trends (if historical data available)
- Key metrics (daily average, projected month-end)
- Status indicators (on track, over budget, etc.)

---

## 3. Dual Export Requirements

### FR-DUAL-001: Simultaneous Export
**Priority:** P1 (High)
**Status:** Not Implemented

When generating a budget, the system SHALL simultaneously create:
- `budget-YYYY-MM.ods` (human-optimized visual)
- `budget-YYYY-MM.ai.json` (AI-optimized semantic)
- `budget-YYYY-MM.meta.json` (metadata and context)

---

### FR-DUAL-002: Export Command
**Priority:** P1 (High)
**Status:** Not Implemented

CLI command: `finance-tracker export-dual <ods-file>`

**Options:**
- `--format`: `json`, `yaml`, `both` (default: `json`)
- `--include-formulas`: Include formula descriptions
- `--semantic-only`: Skip visual formatting metadata
- `--validate`: Validate consistency before export

**Output:**
```bash
$ finance-tracker export-dual budget-2025-01.ods
✓ Analyzing ODS file...
✓ Extracting 3 sheets, 487 cells, 23 formulas
✓ Generating semantic JSON
✓ Generating metadata
✓ Validating consistency

Exported:
  • budget-2025-01.ai.json (145 KB)
  • budget-2025-01.meta.json (8 KB)

Ready for AI/LLM consumption!
```

---

### FR-DUAL-003: Import from AI Format
**Priority:** P2 (Medium)
**Status:** Not Implemented

The system SHALL import from AI-optimized JSON to create ODS:

CLI: `finance-tracker import-ai <json-file> --output <ods-file>`

**Capabilities:**
- Parse semantic JSON
- Apply theme based on metadata
- Regenerate formulas from descriptions
- Apply conditional formatting rules
- Create visual ODS matching original

---

### FR-DUAL-004: Consistency Validation
**Priority:** P1 (High)
**Status:** Not Implemented

The system SHALL validate consistency between paired formats:

**Validation Checks:**
- All cells present in both formats
- Formula results match
- Semantic tags consistent
- No data loss in conversion
- Metadata synchronized

---

## 4. Gap Analysis

### Current State Assessment

| Feature | Human-Readable | AI-Readable | Status |
|---------|----------------|-------------|--------|
| ODS Generation | ✓ Excellent | ✗ Poor | Partial |
| JSON Export | ✗ None | ✗ None | Missing |
| Formula Descriptions | ✗ None | ✗ None | Missing |
| Semantic Tagging | ✗ None | ✗ None | Missing |
| MCP Integration | ~ Documented | ~ Setup guide only | Partial |
| Conversational Queries | ✗ None | ✗ None | Missing |
| Dual Export | ✗ None | ✗ None | Missing |

### Identified Gaps

#### G-AI-01: No Structured Export for AI Consumption
**Severity:** High
**Impact:** AI/LLM assistants cannot effectively understand budget data

Currently, budgets are only in ODS format, which LLMs struggle to parse. No machine-readable export exists.

**Related Requirements:** FR-AI-001, FR-AI-006, FR-DUAL-001

---

#### G-AI-02: No Natural Language Formula Descriptions
**Severity:** Medium
**Impact:** AI cannot explain formulas to users or generate similar formulas

Formulas exist only in spreadsheet syntax. Users and AIs cannot understand business logic.

**Related Requirements:** FR-AI-002

---

#### G-AI-03: No Semantic Cell Tagging
**Severity:** Medium
**Impact:** AI cannot distinguish data types and purposes

Without semantic tags, AI treats all cells equally and cannot perform intelligent queries.

**Related Requirements:** FR-AI-003

---

#### G-AI-04: No Conversational Query Interface
**Severity:** Medium
**Impact:** Users cannot ask natural language questions about their budget

No API or interface exists for natural language interaction.

**Related Requirements:** FR-AI-005, FR-AI-009

---

#### G-AI-05: MCP Server Not Implemented
**Severity:** Medium
**Impact:** No native integration with Claude or other AI assistants

While LibreOffice MCP setup is documented, no native finance-tracker MCP server exists.

**Related Requirements:** FR-AI-009

---

#### G-AI-06: No Formatting Metadata Export
**Severity:** Low
**Impact:** AI cannot understand why cells are formatted certain ways

Conditional formatting and colors exist but semantic meaning not exported.

**Related Requirements:** FR-AI-007

---

## 5. Implementation Examples

### 5.1 Side-by-Side Comparison

#### Human View (ODS):
```
┌─────────────────────────────────────────────────────┐
│           January 2025 Budget                       │
│                                                     │
│  Category      Budget    Actual    Remaining       │
│  ───────────────────────────────────────────────   │
│  Housing       $1,500    $1,500    $0              │
│  Groceries     $450      $456      -$6   ← Red     │
│  Transport     $200      $123      $77   ← Green   │
│                                                     │
│  TOTAL         $2,150    $2,079    $71             │
└─────────────────────────────────────────────────────┘
```

#### AI View (JSON):
```json
{
  "sheet": "Summary",
  "section": "category_comparison",
  "rows": [
    {
      "category": "Housing",
      "budget": {"value": 1500, "currency": "USD"},
      "actual": {"value": 1500, "currency": "USD"},
      "remaining": {"value": 0, "currency": "USD"},
      "status": "on_budget",
      "variance_percent": 0
    },
    {
      "category": "Groceries",
      "budget": {"value": 450, "currency": "USD"},
      "actual": {"value": 456, "currency": "USD"},
      "remaining": {"value": -6, "currency": "USD"},
      "status": "over_budget",
      "variance_percent": 1.3,
      "formatting": {"highlight": "red", "reason": "over_budget"}
    }
  ]
}
```

---

### 5.2 Formula Three Representations

#### ODS Formula:
```
=SUMIF(B:B,"Groceries",D:D)
```

#### Natural Language:
```
Calculate total grocery spending by finding all expenses
categorized as "Groceries" and summing their amounts.
```

#### Structured JSON:
```json
{
  "cell": "E5",
  "formula": {
    "syntax": "=SUMIF(B:B,\"Groceries\",D:D)",
    "function": "SUMIF",
    "arguments": [
      {
        "name": "range",
        "value": "B:B",
        "description": "Category column to search",
        "semantic_type": "expense_category_column"
      },
      {
        "name": "criteria",
        "value": "Groceries",
        "description": "Category to match",
        "semantic_type": "category_filter"
      },
      {
        "name": "sum_range",
        "value": "D:D",
        "description": "Amount column to sum",
        "semantic_type": "expense_amount_column"
      }
    ],
    "natural_language": "Calculate total grocery spending by finding all expenses categorized as 'Groceries' and summing their amounts",
    "business_purpose": "Track total spending in Groceries category for budget vs actual comparison"
  }
}
```

---

### 5.3 Formatting Metadata Example

#### Visual (in ODS):
- Cell D25: Red background, white text, bold

#### Semantic Metadata:
```json
{
  "cell": "D25",
  "value": 89.50,
  "formatted_value": "$89.50",
  "visual_formatting": {
    "background_color": "#FF0000",
    "text_color": "#FFFFFF",
    "font_weight": "bold"
  },
  "conditional_formatting": {
    "rule_id": "over_budget_warning",
    "condition": "D25 > VLOOKUP(B25, Budget!A:B, 2)",
    "natural_language": "Highlight if expense exceeds category budget",
    "is_triggered": true,
    "trigger_reason": "Expense ($89.50) exceeds Dining Out budget ($75.00)"
  },
  "semantic_meaning": "over_budget_expense",
  "business_context": "This individual expense exceeds the allocated budget for its category"
}
```

---

### 5.4 MCP Tool Definition Example

```json
{
  "name": "analyze_budget",
  "description": "Analyze a monthly budget spreadsheet and return spending insights",
  "inputSchema": {
    "type": "object",
    "properties": {
      "file_path": {
        "type": "string",
        "description": "Path to the ODS budget file"
      },
      "analysis_type": {
        "type": "string",
        "enum": ["summary", "detailed", "trends", "alerts"],
        "default": "summary",
        "description": "Type of analysis to perform"
      },
      "categories": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Optional: Specific categories to analyze"
      }
    },
    "required": ["file_path"]
  },
  "outputSchema": {
    "type": "object",
    "properties": {
      "summary": {
        "total_budget": "number",
        "total_spent": "number",
        "remaining": "number",
        "on_track": "boolean"
      },
      "categories": {
        "type": "array",
        "items": {
          "category": "string",
          "budget": "number",
          "spent": "number",
          "status": "enum[under|on|over]"
        }
      }
    }
  }
}
```

---

### 5.5 Natural Language Query Example

**User Query:**
"What categories am I over budget in?"

**System Response:**
```json
{
  "query": "What categories am I over budget in?",
  "interpretation": {
    "intent": "list_over_budget_categories",
    "time_period": "current_month",
    "confidence": 0.98
  },
  "natural_language_answer": "You are over budget in 2 categories: Groceries (by $6.00) and Entertainment (by $23.50).",
  "structured_answer": {
    "over_budget_count": 2,
    "categories": [
      {
        "name": "Groceries",
        "budget": 450.00,
        "actual": 456.00,
        "variance": -6.00,
        "variance_percent": -1.3
      },
      {
        "name": "Entertainment",
        "budget": 150.00,
        "actual": 173.50,
        "variance": -23.50,
        "variance_percent": -15.7
      }
    ],
    "total_overage": 29.50
  },
  "recommendations": [
    "Consider reducing entertainment spending for the rest of the month",
    "Your grocery overage is minor (1.3%)"
  ]
}
```

---

## 6. Prioritization & Implementation

### Phase Integration

These requirements integrate into the existing 5-phase plan:

#### Phase 2: Security & Reliability (Sprint 3-4)
- FR-DUAL-001: Simultaneous dual export
- FR-DUAL-002: Export command implementation

#### Phase 3: Enhanced Features (Sprint 5-8)
- FR-AI-001: AI-optimized data export
- FR-AI-002: Natural language formula descriptions
- FR-AI-003: Semantic cell tagging
- FR-AI-006: Visual + semantic dual export
- FR-AI-008: Context-aware serialization

#### Phase 4: Advanced Features (Sprint 9-12)
- FR-AI-005: Conversational query interface
- FR-AI-007: Formatting metadata export
- FR-AI-009: MCP server integration (native)
- FR-AI-011: Bidirectional AI sync
- FR-DUAL-003: Import from AI format
- FR-DUAL-004: Consistency validation

#### Phase 5: Future Enhancements (Backlog)
- FR-AI-010: AI training data export
- FR-HUMAN-002: Interactive features
- FR-HUMAN-003: Dashboard view

---

## 7. Success Metrics

### Human-Readable Success Metrics
- Visual appeal rating: 8+ / 10
- Time to understand budget: < 2 minutes
- Accessibility score: WCAG 2.1 AA compliant
- Print quality: Professional-grade

### AI-Readable Success Metrics
- Parsing accuracy: 100% (no data loss)
- Semantic understanding: >95% correct interpretation
- Query response accuracy: >90%
- Round-trip conversion: 100% fidelity

### Dual-Audience Success Metrics
- Export time: < 5 seconds for both formats
- Consistency validation: 0 discrepancies
- User satisfaction: 80%+ prefer dual export

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-12-28 | Claude | Initial dual-audience requirements |

---

*End of Dual-Audience Requirements Addendum*

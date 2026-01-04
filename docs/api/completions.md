# Completions API Reference

Shell completion script generation for multiple shells.

**Implements:** FR-UX-009 (Shell Completions)

## Overview

The Completions module provides tab completion for Bash, Zsh, and Fish shells, enabling rapid command entry and discovery of available options.

Features:

- Auto-detect current shell
- Generate completion scripts for Bash, Zsh, and Fish
- Install completions automatically to system locations
- Complete commands, subcommands, and options
- Smart file completion for file arguments
- Choice completion for enum options

## Command Structure

The module maintains a comprehensive command structure defining all CLI commands, subcommands, and options:

```python
from spreadsheet_dl.completions import COMMAND_STRUCTURE

# COMMAND_STRUCTURE is a dict mapping command names to their specs:
# {
#     "command_name": {
#         "description": "What this command does",
#         "options": {...},
#         "subcommands": {...}  # optional
#     }
# }
```

---

## Completion Generation Functions

### generate_bash_completions() -> str

Generate Bash completion script.

```python
from spreadsheet_dl.completions import generate_bash_completions

script = generate_bash_completions()
print(script)
# -> Bash completion function ready for installation
```

**Returns:** Complete Bash completion script for installation

---

### generate_zsh_completions() -> str

Generate Zsh completion script.

```python
from spreadsheet_dl.completions import generate_zsh_completions

script = generate_zsh_completions()
print(script)
# -> Zsh completion function with subcommand support
```

**Returns:** Complete Zsh completion script

---

### generate_fish_completions() -> str

Generate Fish completion script.

```python
from spreadsheet_dl.completions import generate_fish_completions

script = generate_fish_completions()
print(script)
# -> Fish completion commands
```

**Returns:** Complete Fish completion script

---

### print_completion_script(shell: str) -> str

Print completion script for manual installation.

```python
from spreadsheet_dl.completions import print_completion_script

# Get Bash completions
bash_script = print_completion_script("bash")

# Get Zsh completions
zsh_script = print_completion_script("zsh")

# Get Fish completions
fish_script = print_completion_script("fish")

# Save to file
with open("my_completions.sh", "w") as f:
    f.write(bash_script)
```

**Parameters:**

- `shell`: Shell type ("bash", "zsh", or "fish")

**Returns:** Completion script content

**Raises:** ValueError if unsupported shell

---

### detect_shell() -> str

Auto-detect the current shell.

```python
from spreadsheet_dl.completions import detect_shell

shell = detect_shell()
print(f"Detected shell: {shell}")
# -> "bash", "zsh", or "fish"

# Uses SHELL environment variable first, then falls back to
# process inspection for better detection
```

**Returns:** Shell name ("bash", "zsh", or "fish"), defaults to "bash"

---

## Installation Functions

### install_completions(shell: str | None = None) -> dict[str, Any]

Install shell completions automatically.

```python
from spreadsheet_dl.completions import install_completions

# Auto-detect shell and install
result = install_completions()
print(result["message"])
# -> "Completions installed to /home/user/.local/share/bash-completion..."

# Or specify a shell explicitly
result = install_completions("zsh")

if result["success"]:
    print(f"Installed to: {result['path']}")
else:
    print(f"Failed: {result['message']}")
```

**Parameters:**

- `shell`: Shell type ("bash", "zsh", "fish"). Auto-detects if None.

**Returns:** Dictionary with installation result:

```python
{
    "shell": "bash",
    "success": True,
    "path": "/home/user/.local/share/bash-completion/completions/spreadsheet-dl",
    "message": "Completions installed to ..."
}
```

---

### get_installation_instructions(shell: str) -> str

Get manual installation instructions for a shell.

```python
from spreadsheet_dl.completions import get_installation_instructions

# Get Bash instructions
bash_instructions = get_installation_instructions("bash")
print(bash_instructions)
```

Output:

```
Bash Completion Installation
============================

Option 1: Add to .bashrc (recommended)
    spreadsheet-dl completions bash >> ~/.bash_completion
    source ~/.bashrc

Option 2: System-wide (requires sudo)
    sudo spreadsheet-dl completions bash > /etc/bash_completion.d/spreadsheet-dl
...
```

**Parameters:**

- `shell`: Shell type ("bash", "zsh", or "fish")

**Returns:** Installation instructions as formatted text

---

## Supported Commands

The module provides completions for these main commands:

### Data Generation

- `generate` - Generate a new budget spreadsheet
  - Options: `--month`, `--year`, `--output`, `--template`, `--theme`, `--income`
  - Templates: 50_30_20, family, minimalist, zero_based, fire, high_income

### Data Entry & Modification

- `expense` - Add a quick expense entry
  - Options: `--file`, `--date`, `--category`, `--amount`, `--description`, `--dry-run`
- `import` - Import bank transactions
  - Options: `--bank`, `--output`, `--append`, `--categorize`
  - Banks: chase, chase_credit, bank_of_america, wells_fargo, capital_one, discover, amex, usaa, generic

### Analysis & Reporting

- `analyze` - Analyze budget spending
  - Options: `--file`, `--format`
- `report` - Generate spending report
  - Options: `--file`, `--format`, `--output`

### Account & Financial Management

- `account` - Manage accounts
  - Subcommands: add, list, balance, transfer, net-worth
  - Options: `--type`, `--json`
  - Types: checking, savings, credit_card, investment, loan, cash, other

- `currency` - Currency conversion
  - Subcommands: convert, list, rates
  - Options: `--from`, `--to`

- `goal` - Manage savings goals
  - Subcommands: add, list, progress, contribute
  - Categories: savings, emergency_fund, vacation, home_down_payment, car_purchase, education, retirement

- `debt` - Manage debt payoff
  - Subcommands: add, list, plan, payment, compare
  - Methods: snowball, avalanche

### Reminders & Notifications

- `bills` - Manage bill reminders
  - Subcommands: add, list, upcoming, overdue, pay, export-calendar
  - Options: `--days`

- `notify` - Send notifications
  - Subcommands: test, config, history
  - Channels: email, ntfy

- `recurring` - Manage recurring expenses
  - Subcommands: list, add, remove, generate
  - Options: `--json`

### Upload & Sync

- `upload` - Upload to Nextcloud
  - Options: `--remote-path`

### Configuration & Tools

- `config` - Manage configuration
  - Subcommands: show, init, set, get
  - Options: `--json`

- `completions` - Generate shell completions
  - Subcommands: bash, zsh, fish, install

---

## Expense Categories

Completable expense categories:

- housing
- utilities
- groceries
- transportation
- healthcare
- insurance
- entertainment
- dining_out
- clothing
- personal_care
- education
- savings
- debt_payment
- gifts
- subscriptions
- miscellaneous

---

## Complete Example

```python
from spreadsheet_dl.completions import (
    detect_shell,
    install_completions,
    generate_bash_completions,
    get_installation_instructions,
)

# Detect current shell
shell = detect_shell()
print(f"Your shell: {shell}")

# Install completions automatically
result = install_completions()
if result["success"]:
    print(f"Completions installed to: {result['path']}")
    print("Please reload your shell or source the completion file")
else:
    print(f"Automatic installation failed: {result['message']}")
    print("\nTry manual installation:")
    print(get_installation_instructions(shell))

# Or generate script manually
bash_script = generate_bash_completions()
with open("/tmp/spreadsheet-dl-completion.sh", "w") as f:
    f.write(bash_script)
print("Completion script saved to /tmp/spreadsheet-dl-completion.sh")
```

---

## Usage in Shell

After installation, use tab completion:

```bash
# Complete commands
$ spreadsheet-dl ge<TAB>
$ spreadsheet-dl generate --<TAB>
$ spreadsheet-dl generate --template <TAB>

# View available options with descriptions
$ spreadsheet-dl account --<TAB>
account           add               balance           list              net-worth         transfer
```

---

## Troubleshooting

If completions aren't working:

1. **Check installation location:**

   ```bash
   # Bash
   ls ~/.bash_completion.d/
   ls ~/.local/share/bash-completion/completions/

   # Zsh
   ls ~/.zsh/completions/
   ls ~/.local/share/zsh/site-functions/

   # Fish
   ls ~/.config/fish/completions/
   ```

2. **Reload shell configuration:**

   ```bash
   # Bash
   source ~/.bashrc

   # Zsh
   exec zsh

   # Fish
   exec fish
   ```

3. **Check for errors:**

   ```bash
   # Bash - test the completion file
   bash -n ~/.bash_completion.d/spreadsheet-dl

   # Fish - test the completion file
   fish -c "builtin complete -l test"
   ```

4. **Manual installation:** Use the instructions from `get_installation_instructions()`

# Notifications API Reference

Multi-channel notification system for alerts and summaries.

**Implements:** IR-NOTIF-001 (Alert Notifications)

## Overview

The Notifications module provides a flexible, multi-channel notification system supporting email and ntfy.sh (HTTP push notifications). It includes notification templates for common financial events and a notification manager for orchestrating delivery across channels.

Features:

- Email notifications via SMTP (Gmail, Outlook, custom servers)
- ntfy.sh push notifications
- HTML and plain text email templates
- Pre-built notification templates for financial events
- Notification history tracking
- Priority levels and semantic types
- Multi-channel delivery

## Enumerations

### NotificationPriority

Priority level for notifications.

```python
from spreadsheet_dl.notifications import NotificationPriority

# Priority levels
NotificationPriority.LOW       # Non-urgent information
NotificationPriority.NORMAL    # Standard notification
NotificationPriority.HIGH      # Requires attention
NotificationPriority.URGENT    # Immediate action needed
```

---

### NotificationType

Types of notifications available.

```python
from spreadsheet_dl.notifications import NotificationType

# Financial event types
NotificationType.BILL_DUE
NotificationType.BILL_OVERDUE
NotificationType.BUDGET_WARNING
NotificationType.BUDGET_EXCEEDED
NotificationType.GOAL_PROGRESS
NotificationType.GOAL_COMPLETED
NotificationType.LOW_BALANCE
NotificationType.RECURRING_REMINDER
NotificationType.WEEKLY_SUMMARY
NotificationType.MONTHLY_SUMMARY
NotificationType.CUSTOM
```

---

## Notification Class

### Notification

A notification to be sent through one or more channels.

```python
from spreadsheet_dl.notifications import (
    Notification,
    NotificationType,
    NotificationPriority,
)

notification = Notification(
    type=NotificationType.BUDGET_WARNING,
    title="Budget Alert: Groceries",
    message="You've used 85% of your grocery budget",
    priority=NotificationPriority.HIGH,
    data={
        "category": "groceries",
        "spent": "425.50",
        "budget": "500.00",
        "remaining": "74.50"
    },
    channels=["email", "ntfy"]
)

# Convert to dictionary
data = notification.to_dict()
```

**Attributes:**

- `type: NotificationType` - Type of notification
- `title: str` - Notification title
- `message: str` - Notification body
- `priority: NotificationPriority` - Priority level (default: NORMAL)
- `data: dict[str, Any]` - Additional data for templates
- `created_at: datetime` - Creation timestamp
- `sent_at: datetime | None` - When notification was sent
- `channels: list[str]` - Channels to send through

**Methods:**

#### `to_dict() -> dict[str, Any]`

Convert notification to dictionary.

```python
data = notification.to_dict()
# {
#     "type": "budget_warning",
#     "title": "Budget Alert: Groceries",
#     "message": "...",
#     "priority": "high",
#     "data": {...},
#     "created_at": "2024-01-15T10:30:00",
#     "sent_at": None,
#     "channels": ["email", "ntfy"]
# }
```

---

## Email Configuration

### EmailConfig

Email server configuration.

```python
from spreadsheet_dl.notifications import EmailConfig

config = EmailConfig(
    smtp_host="smtp.gmail.com",
    smtp_port=587,
    username="your-email@gmail.com",
    password="app-password",
    from_address="your-email@gmail.com",
    to_address="recipient@example.com",
    use_tls=True
)
```

**Attributes:**

- `smtp_host: str` - SMTP server address
- `smtp_port: int` - SMTP server port (default: 587)
- `username: str` - SMTP authentication username
- `password: str` - SMTP authentication password
- `from_address: str` - From email address
- `to_address: str` - To email address
- `use_tls: bool` - Use TLS encryption (default: True)

---

### EmailChannel

Send notifications via SMTP email.

```python
from spreadsheet_dl.notifications import EmailChannel, EmailConfig

config = EmailConfig(
    smtp_host="smtp.gmail.com",
    username="user@gmail.com",
    password="app-password",
    from_address="user@gmail.com",
    to_address="recipient@example.com"
)

channel = EmailChannel(config)

# Check configuration
if channel.is_configured():
    success = channel.send(notification)
```

**Methods:**

#### `is_configured() -> bool`

Check if email is properly configured.

#### `send(notification: Notification) -> bool`

Send notification via email.

Returns True on success, False on failure.

---

## Ntfy.sh Configuration

### NtfyConfig

Ntfy.sh server configuration.

```python
from spreadsheet_dl.notifications import NtfyConfig

config = NtfyConfig(
    server="https://ntfy.sh",
    topic="my-finance-alerts",
    access_token=""  # Optional authentication
)
```

**Attributes:**

- `server: str` - Ntfy.sh server URL (default: https://ntfy.sh)
- `topic: str` - Topic name for notifications
- `access_token: str` - Optional authentication token

---

### NtfyChannel

Send notifications via ntfy.sh.

```python
from spreadsheet_dl.notifications import NtfyChannel, NtfyConfig

config = NtfyConfig(
    topic="my-budget-alerts"
)

channel = NtfyChannel(config)

# Check configuration
if channel.is_configured():
    success = channel.send(notification)
```

**Methods:**

#### `is_configured() -> bool`

Check if ntfy is properly configured.

#### `send(notification: Notification) -> bool`

Send notification via ntfy.sh.

Returns True on success, False on failure.

---

## Notification Manager

### NotificationManager

Orchestrate notifications across multiple channels.

```python
from spreadsheet_dl.notifications import (
    NotificationManager,
    EmailConfig,
    NtfyConfig,
)

# Create manager with channels
email_config = EmailConfig(...)
ntfy_config = NtfyConfig(topic="budget-alerts")

manager = NotificationManager(
    email_config=email_config,
    ntfy_config=ntfy_config,
    log_path="/var/log/spreadsheet-dl/notifications.json"
)

# Send notification through specified channels
results = manager.send(notification, channels=["email", "ntfy"])
# -> {"email": True, "ntfy": True}

# Send through all configured channels
results = manager.send_all(notification)
# -> {"email": True, "ntfy": True}
```

**Methods:**

#### `__init__(...)`

Initialize notification manager.

```python
NotificationManager(
    email_config: EmailConfig | None = None,
    ntfy_config: NtfyConfig | None = None,
    log_path: Path | str | None = None
)
```

#### `add_channel(name: str, channel: NotificationChannel)`

Add a notification channel.

```python
manager.add_channel("custom", my_channel)
```

#### `remove_channel(name: str) -> bool`

Remove a notification channel.

```python
success = manager.remove_channel("email")
```

#### `list_channels() -> list[dict[str, Any]]`

List configured channels.

```python
channels = manager.list_channels()
# [
#     {"name": "email", "type": "EmailChannel", "configured": True},
#     {"name": "ntfy", "type": "NtfyChannel", "configured": True}
# ]
```

#### `send(notification: Notification, channels: list[str] | None = None) -> dict[str, bool]`

Send notification through specified channels.

```python
results = manager.send(notification, channels=["email"])
# -> {"email": True}

# Uses notification's channels if not specified
results = manager.send(notification)
```

#### `send_all(notification: Notification) -> dict[str, bool]`

Send through all configured channels.

```python
results = manager.send_all(notification)
```

#### `get_history(limit: int = 100, notification_type: NotificationType | None = None) -> list[Notification]`

Retrieve notification history.

```python
# Get last 100 notifications
history = manager.get_history()

# Get last 50 budget warnings
from spreadsheet_dl.notifications import NotificationType
history = manager.get_history(
    limit=50,
    notification_type=NotificationType.BUDGET_WARNING
)
```

---

## Notification Templates

### NotificationTemplates

Pre-built notification templates for common scenarios.

```python
from spreadsheet_dl.notifications import NotificationTemplates
from datetime import date
from decimal import Decimal

# Bill due reminder
notif = NotificationTemplates.bill_due(
    bill_name="Electric Bill",
    amount=Decimal("125.50"),
    due_date=date(2024, 1, 20),
    auto_pay=False
)

# Budget warning
notif = NotificationTemplates.budget_warning(
    category="Groceries",
    spent=Decimal("425.00"),
    budget=Decimal("500.00"),
    percent_used=85.0
)

# Goal progress
notif = NotificationTemplates.goal_progress(
    goal_name="Emergency Fund",
    current=Decimal("3500"),
    target=Decimal("10000"),
    percent_complete=35.0
)
```

**Available Templates:**

#### `bill_due(bill_name, amount, due_date, auto_pay=False)`

Reminder that a bill is due.

```python
notif = NotificationTemplates.bill_due(
    bill_name="Mortgage",
    amount=1500.00,
    due_date=date(2024, 1, 1),
    auto_pay=False
)
# Priority: HIGH if due today/tomorrow, NORMAL otherwise
```

#### `bill_overdue(bill_name, amount, due_date, days_overdue)`

Alert that a bill is overdue.

```python
notif = NotificationTemplates.bill_overdue(
    bill_name="Credit Card",
    amount=500.00,
    due_date=date(2024, 1, 1),
    days_overdue=5
)
# Priority: URGENT
```

#### `budget_warning(category, spent, budget, percent_used)`

Warning that budget is being exceeded.

```python
notif = NotificationTemplates.budget_warning(
    category="Entertainment",
    spent=450.00,
    budget=500.00,
    percent_used=90.0
)
# Priority: HIGH if >= 90%, NORMAL otherwise
```

#### `budget_exceeded(category, spent, budget, over_amount)`

Alert that budget has been exceeded.

```python
notif = NotificationTemplates.budget_exceeded(
    category="Dining Out",
    spent=300.00,
    budget=250.00,
    over_amount=50.00
)
# Priority: URGENT
```

#### `goal_progress(goal_name, current, target, percent_complete)`

Progress update on a savings goal.

```python
notif = NotificationTemplates.goal_progress(
    goal_name="Vacation Fund",
    current=2000.00,
    target=5000.00,
    percent_complete=40.0
)
# Priority: LOW, includes milestone detection
```

#### `goal_completed(goal_name, target, days_taken)`

Congratulations on reaching a goal.

```python
notif = NotificationTemplates.goal_completed(
    goal_name="New Laptop Fund",
    target=1500.00,
    days_taken=90
)
# Priority: HIGH
```

#### `weekly_summary(week_total, top_categories, budget_status)`

Weekly spending summary.

```python
notif = NotificationTemplates.weekly_summary(
    week_total=450.00,
    top_categories=[
        ("Groceries", 150.00),
        ("Dining Out", 120.00),
        ("Transportation", 80.00)
    ],
    budget_status="on track"
)
# Priority: LOW
```

#### `monthly_summary(month, total_spent, total_budget, savings, over_budget_categories)`

Monthly spending summary.

```python
notif = NotificationTemplates.monthly_summary(
    month="January 2024",
    total_spent=3500.00,
    total_budget=4000.00,
    savings=500.00,
    over_budget_categories=["Entertainment"]
)
# Priority: LOW
```

---

## Configuration Loading

### load_notification_config(config_path: Path | str) -> tuple[EmailConfig | None, NtfyConfig | None]

Load notification configuration from JSON file.

```python
from spreadsheet_dl.notifications import load_notification_config

email_config, ntfy_config = load_notification_config(
    "/etc/spreadsheet-dl/notifications.json"
)
```

**Configuration File Format:**

```json
{
  "email": {
    "smtp_host": "smtp.gmail.com",
    "smtp_port": 587,
    "username": "user@gmail.com",
    "password": "app-password",
    "from_address": "user@gmail.com",
    "to_address": "alerts@example.com",
    "use_tls": true
  },
  "ntfy": {
    "server": "https://ntfy.sh",
    "topic": "my-budget-alerts",
    "access_token": ""
  }
}
```

---

## Complete Example

```python
from spreadsheet_dl.notifications import (
    NotificationManager,
    EmailConfig,
    NtfyConfig,
    NotificationTemplates,
)
from datetime import date
from decimal import Decimal

# Configure channels
email_config = EmailConfig(
    smtp_host="smtp.gmail.com",
    username="alerts@example.com",
    password="app-password",
    from_address="alerts@example.com",
    to_address="user@example.com"
)

ntfy_config = NtfyConfig(
    topic="budget-alerts"
)

# Create manager
manager = NotificationManager(
    email_config=email_config,
    ntfy_config=ntfy_config,
    log_path="/home/user/.config/spreadsheet-dl/notifications.json"
)

# Send bill due reminder
notif = NotificationTemplates.bill_due(
    bill_name="Electric Bill",
    amount=Decimal("125.50"),
    due_date=date(2024, 1, 20),
    auto_pay=False
)
results = manager.send_all(notif)
print(f"Email: {results['email']}, Ntfy: {results['ntfy']}")

# Send budget warning
notif = NotificationTemplates.budget_warning(
    category="Groceries",
    spent=Decimal("425.00"),
    budget=Decimal("500.00"),
    percent_used=85.0
)
results = manager.send(notif, channels=["email"])

# View history
history = manager.get_history(limit=10)
for notif in history:
    print(f"{notif.title} ({notif.type.value})")
```

---

## Email Provider Setup

### Gmail

1. Enable 2-factor authentication
2. Generate app password: https://myaccount.google.com/apppasswords
3. Use app password in configuration:

```python
config = EmailConfig(
    smtp_host="smtp.gmail.com",
    smtp_port=587,
    username="your-email@gmail.com",
    password="your-app-password",  # 16-character password
    from_address="your-email@gmail.com",
    to_address="recipient@example.com"
)
```

### Outlook/Office 365

```python
config = EmailConfig(
    smtp_host="smtp.office365.com",
    smtp_port=587,
    username="your-email@outlook.com",
    password="your-password",
    from_address="your-email@outlook.com",
    to_address="recipient@example.com"
)
```

### Custom SMTP Server

```python
config = EmailConfig(
    smtp_host="mail.example.com",
    smtp_port=587,
    username="user",
    password="password",
    from_address="noreply@example.com",
    to_address="admin@example.com"
)
```

# Performance API Reference

Performance optimization utilities including caching, lazy loading, and batch processing.

## Overview

The performance module provides:

- LRU cache with TTL support
- Function-level caching decorator
- Lazy evaluation wrappers
- Batch processing for bulk operations
- Benchmarking utilities
- File-based persistent caching

## Caching

### LRUCache

Thread-safe Least Recently Used cache with optional TTL.

```python
from spreadsheet_dl import LRUCache

# Basic usage
cache: LRUCache[str, int] = LRUCache(maxsize=100)
cache.set("key", 42)
value = cache.get("key")  # 42
value = cache.get("missing", default=0)  # 0

# With time-to-live (1 hour)
cache = LRUCache(maxsize=1000, ttl=3600)

# Check membership
if "key" in cache:
    print("Found!")

# Delete and clear
cache.delete("key")
cache.clear()

# Get statistics
stats = cache.stats
print(f"Hit rate: {stats['hit_rate']:.1%}")
```

#### Constructor

```python
LRUCache(
    maxsize: int = 128,  # Maximum items
    ttl: float | None = None  # Time-to-live in seconds
)
```

#### Methods

| Method                   | Returns | Description                    |
| ------------------------ | ------- | ------------------------------ | -------------------- |
| `get(key, default=None)` | `V      | None`                          | Get value or default |
| `set(key, value)`        | `None`  | Store value                    |
| `delete(key)`            | `bool`  | Delete key, returns if existed |
| `clear()`                | `None`  | Clear all items                |
| `stats`                  | `dict`  | Cache statistics               |

---

### @cached

Decorator for caching function results.

```python
from spreadsheet_dl import cached

@cached(maxsize=100, ttl=3600)
def expensive_computation(x: int) -> int:
    # Only computed once per unique argument
    return x * 2

result = expensive_computation(5)  # Computed
result = expensive_computation(5)  # From cache

# Custom key function
@cached(key_func=lambda x, y: f"{x}:{y}")
def another_func(x: int, y: int) -> int:
    return x + y

# Access cache internals
expensive_computation.cache_clear()
stats = expensive_computation.cache_stats()
```

#### Parameters

| Parameter  | Type       | Default | Description                |
| ---------- | ---------- | ------- | -------------------------- | ----------------------- |
| `maxsize`  | `int`      | 128     | Maximum cached results     |
| `ttl`      | `float     | None`   | None                       | Time-to-live in seconds |
| `key_func` | `Callable` | None    | Custom cache key generator |

---

### FileCache

File-based persistent cache for expensive computations.

```python
from spreadsheet_dl import FileCache

cache = FileCache("~/.cache/spreadsheet-dl", ttl=3600)

# Store results
cache.set("analysis_result", {"data": [1, 2, 3]})

# Retrieve later (even after restart)
result = cache.get("analysis_result")

# Cleanup
cache.delete("analysis_result")
count = cache.clear()  # Clear all
count = cache.cleanup_expired()  # Remove expired only
```

---

## Lazy Loading

### Lazy

Lazy evaluation wrapper - value is only computed when accessed.

```python
from spreadsheet_dl import Lazy

def load_large_data():
    # Expensive operation
    return expensive_load()

lazy_data = Lazy(load_large_data)

# Not loaded yet
print(lazy_data.is_loaded)  # False

# Loaded on first access
data = lazy_data.value  # Loads now
data = lazy_data.value  # Uses cached value

# Reset to reload on next access
lazy_data.reset()
```

---

### LazyProperty

Lazy property descriptor for classes.

```python
from spreadsheet_dl import LazyProperty

class DataProcessor:
    @LazyProperty
    def expensive_data(self) -> list:
        # Only computed once per instance
        return compute_expensive_data()

processor = DataProcessor()

# Not computed yet
data = processor.expensive_data  # Computed now
data = processor.expensive_data  # Cached

# Each instance has its own cache
processor2 = DataProcessor()
data2 = processor2.expensive_data  # Computed for this instance
```

---

## Batch Processing

### BatchProcessor

Process items in batches with error handling and progress tracking.

```python
from spreadsheet_dl import BatchProcessor, BatchResult

def process_item(item: dict) -> dict:
    # Process single item
    return {"result": item["value"] * 2}

processor = BatchProcessor(
    processor=process_item,
    batch_size=100,
    on_error="continue"  # or "stop", "skip"
)

# Process all items
items = [{"value": i} for i in range(1000)]
result: BatchResult = processor.process_all(
    items,
    progress_callback=lambda done, total: print(f"{done}/{total}")
)

print(f"Success: {result.success_count}")
print(f"Errors: {result.error_count}")
print(f"Duration: {result.duration_ms:.1f}ms")

# Process in batches (generator)
for batch_result in processor.process_batches(items):
    print(f"Batch complete: {batch_result.success_count} items")
```

#### Constructor

```python
BatchProcessor(
    processor: Callable[[T], Any],  # Item processor
    batch_size: int = 100,
    max_workers: int | None = None,  # For parallel (future)
    on_error: str = "continue"  # "continue", "stop", "skip"
)
```

---

### batch_process

Convenience function for simple batch processing.

```python
from spreadsheet_dl import batch_process

result = batch_process(
    items=[1, 2, 3, 4, 5],
    processor=lambda x: x * 2,
    batch_size=2
)

print(result.items)  # [2, 4, 6, 8, 10]
```

---

### BatchResult

Result of batch processing operation.

```python
from spreadsheet_dl import BatchResult

# Attributes
result.items           # List of processed results
result.success_count   # Number of successful items
result.error_count     # Number of failed items
result.errors          # List of (index, exception) tuples
result.duration_ms     # Total processing time in ms
```

---

## Benchmarking

### Benchmark

Performance benchmarking utility.

```python
from spreadsheet_dl import Benchmark

bench = Benchmark("MyOperation")

# Run benchmark
result = bench.run(my_function, iterations=1000, warmup=5)
print(f"Average: {result.avg_time_ms:.3f}ms")
print(f"Ops/sec: {result.ops_per_second:.0f}")

# Compare implementations
results = bench.compare([
    ("impl_a", implementation_a),
    ("impl_b", implementation_b),
], iterations=100)

# Results sorted by speed (fastest first)
print(Benchmark.format_results(results))
```

---

### BenchmarkResult

Result of a benchmark run.

```python
from spreadsheet_dl import BenchmarkResult

# Attributes
result.name             # Benchmark name
result.iterations       # Number of iterations
result.total_time_ms    # Total time
result.avg_time_ms      # Average time per iteration
result.min_time_ms      # Minimum time
result.max_time_ms      # Maximum time
result.ops_per_second   # Operations per second
result.timestamp        # When benchmark was run

# Export
data = result.to_dict()
```

---

### @timed

Decorator to time function execution.

```python
from spreadsheet_dl import timed

@timed
def slow_function():
    time.sleep(1)

slow_function()
# Prints: slow_function took 1000.123ms
```

---

## Global Cache

### get_cache

Get the global cache instance (shared across modules).

```python
from spreadsheet_dl import get_cache, clear_cache

cache = get_cache()
cache.set("shared_data", value)

# Later, in another module
cache = get_cache()
value = cache.get("shared_data")

# Clear global cache
clear_cache()
```

---

## Complete Example

```python
from spreadsheet_dl import (
    LRUCache,
    cached,
    Lazy,
    LazyProperty,
    BatchProcessor,
    Benchmark,
    FileCache,
    timed,
)
import time


# 1. Function caching for expensive computations
@cached(maxsize=100, ttl=3600)
def analyze_budget(budget_id: str) -> dict:
    # Expensive analysis only done once per budget_id
    time.sleep(0.1)  # Simulate work
    return {"budget_id": budget_id, "analysis": "complete"}

# First call: computes
result1 = analyze_budget("budget-123")

# Second call: from cache
result2 = analyze_budget("budget-123")


# 2. Lazy loading for optional expensive data
class BudgetReport:
    def __init__(self, budget_id: str):
        self.budget_id = budget_id

    @LazyProperty
    def detailed_analysis(self) -> dict:
        # Only computed if accessed
        return analyze_budget(self.budget_id)

    @LazyProperty
    def chart_data(self) -> list:
        # Only computed if accessed
        return generate_chart_data(self.budget_id)

report = BudgetReport("budget-123")
# Nothing computed yet

if user_wants_details:
    print(report.detailed_analysis)  # Now computed


# 3. Batch processing for bulk operations
def process_expense(expense: dict) -> dict:
    # Validate, categorize, store
    return {"processed": True, "expense": expense}

processor = BatchProcessor(process_expense, batch_size=50)

expenses = [{"amount": i} for i in range(500)]
result = processor.process_all(
    expenses,
    progress_callback=lambda done, total: print(f"Progress: {done}/{total}")
)

print(f"Processed {result.success_count} expenses in {result.duration_ms:.0f}ms")


# 4. Benchmarking different implementations
def impl_list():
    return [i * 2 for i in range(1000)]

def impl_generator():
    return list(i * 2 for i in range(1000))

bench = Benchmark()
results = bench.compare([
    ("list_comp", impl_list),
    ("generator", impl_generator),
], iterations=1000)

print("\nBenchmark Results:")
print(Benchmark.format_results(results))


# 5. Persistent file cache
file_cache = FileCache("~/.cache/budget-analysis", ttl=86400)

# Cache expensive results to disk
file_cache.set("monthly_summary_2024", summary_data)

# Retrieve later (survives restarts)
cached_summary = file_cache.get("monthly_summary_2024")
if cached_summary is None:
    cached_summary = compute_monthly_summary()
    file_cache.set("monthly_summary_2024", cached_summary)
```

---

## Performance Tips

### When to Use Caching

- **Use `@cached`**: For pure functions with expensive computations
- **Use `LRUCache`**: For dynamic key-value storage with eviction
- **Use `FileCache`**: For data that should persist across restarts
- **Use `Lazy`**: For data that may not always be needed

### Cache Sizing

```python
# Rule of thumb: cache size = expected concurrent items * 1.5
# For budget analysis with ~100 active budgets:
@cached(maxsize=150)
def analyze(budget_id): ...

# For user sessions with ~1000 concurrent users:
session_cache = LRUCache(maxsize=1500, ttl=3600)
```

### Batch Size Tuning

```python
# Large items (complex objects): smaller batches
processor = BatchProcessor(func, batch_size=10)

# Small items (simple data): larger batches
processor = BatchProcessor(func, batch_size=500)

# With progress updates every ~1 second:
# batch_size = items_per_second * 1
```

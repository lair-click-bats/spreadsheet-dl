"""
Common handler utilities for MCP tools.

Provides shared functionality for parameter validation, error handling,
and response formatting used across all MCP tool categories.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

from spreadsheet_dl._mcp.exceptions import MCPSecurityError
from spreadsheet_dl.exceptions import FileError

if TYPE_CHECKING:
    import logging

    from spreadsheet_dl._mcp.config import MCPConfig
    from spreadsheet_dl._mcp.models import MCPToolResult


class HandlerUtils:
    """Common utilities for MCP tool handlers."""

    def __init__(self, config: MCPConfig, logger: logging.Logger) -> None:
        """Initialize handler utilities."""
        self.config = config
        self.logger = logger
        self._request_count = 0
        self._last_reset = datetime.now()

    def _validate_path(self, path: str | Path) -> Path:
        """
        Validate and resolve a file path.

        Args:
            path: Path to validate.

        Returns:
            Resolved Path object.

        Raises:
            MCPSecurityError: If path is not allowed.
            FileError: If file doesn't exist.
        """
        resolved = Path(path).resolve()

        # Check against allowed paths
        allowed = False
        for allowed_path in self.config.allowed_paths:
            try:
                resolved.relative_to(allowed_path.resolve())
                allowed = True
                break
            except ValueError:
                continue

        if not allowed:
            raise MCPSecurityError(
                f"Path not allowed: {path}. "
                f"Allowed paths: {[str(p) for p in self.config.allowed_paths]}"
            )

        if not resolved.exists():
            raise FileError(f"File not found: {resolved}")

        return resolved

    def _check_rate_limit(self) -> bool:
        """Check if rate limit is exceeded."""
        now = datetime.now()
        if (now - self._last_reset).seconds >= 60:
            self._request_count = 0
            self._last_reset = now

        self._request_count += 1
        return self._request_count <= self.config.rate_limit_per_minute

    def _log_audit(
        self,
        tool: str,
        params: dict[str, Any],
        result: MCPToolResult,
    ) -> None:
        """Log tool invocation for audit."""
        if not self.config.enable_audit_log:
            return

        entry = {
            "timestamp": datetime.now().isoformat(),
            "tool": tool,
            "params": {k: str(v) for k, v in params.items()},
            "success": not result.is_error,
        }

        self.logger.info(json.dumps(entry))

        if self.config.audit_log_path:
            with open(self.config.audit_log_path, "a") as f:
                f.write(json.dumps(entry) + "\n")

    # =========================================================================
    # Tool Handlers
    # =========================================================================


# Export utilities
__all__ = ["HandlerUtils"]

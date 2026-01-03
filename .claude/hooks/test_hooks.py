#!/usr/bin/env python3
"""
Comprehensive Hook Test Suite for Claude Code Configuration

Tests all hooks to verify they provide intended behavior:
1. cleanup_stale_files.py - Archives old files, removes empty files
2. validate_file_locations.py - Warns on misplaced intermediate files
3. check_stop.py - Prevents stopping with active work
4. check_subagent_stop.py - Validates subagent completion

Run with: python3 .claude/hooks/test_hooks.py
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path


class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


def print_header(text: str) -> None:
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.RESET}")


def print_test(name: str, passed: bool, details: str = "") -> None:
    status = (
        f"{Colors.GREEN}✓ PASS{Colors.RESET}"
        if passed
        else f"{Colors.RED}✗ FAIL{Colors.RESET}"
    )
    print(f"  {status} {name}")
    if details and not passed:
        print(f"    {Colors.YELLOW}{details}{Colors.RESET}")


def run_hook(
    hook_path: Path, input_data: dict, project_dir: Path
) -> tuple[int, str, str]:
    """Run a hook script with given input and return exit code, stdout, stderr."""
    env = os.environ.copy()
    env["CLAUDE_PROJECT_DIR"] = str(project_dir)

    try:
        result = subprocess.run(
            ["python3", str(hook_path)],
            input=json.dumps(input_data),
            capture_output=True,
            text=True,
            timeout=30,
            env=env,
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Timeout"
    except Exception as e:
        return -1, "", str(e)


class TestCleanupStaleFiles:
    """Tests for cleanup_stale_files.py hook."""

    def __init__(self, hooks_dir: Path):
        self.hook = hooks_dir / "cleanup_stale_files.py"
        self.results = []

    def run_all(self) -> list[tuple[str, bool, str]]:
        print_header("Testing cleanup_stale_files.py")

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            self._setup_test_files(project_dir)

            # Run the hook
            exit_code, stdout, stderr = run_hook(self.hook, {}, project_dir)

            # Test 1: Hook should succeed
            test1_pass = exit_code == 0
            print_test("Hook exits successfully", test1_pass, f"Exit code: {exit_code}")
            self.results.append(("Hook exits successfully", test1_pass, ""))

            # Test 2: Should return valid JSON
            try:
                output = json.loads(stdout)
                test2_pass = output.get("ok")
            except:
                test2_pass = False
                output = {}
            print_test("Returns valid JSON with ok=true", test2_pass, stdout)
            self.results.append(("Returns valid JSON", test2_pass, ""))

            # Test 3: Old coordination files should be archived
            archive_dir = project_dir / ".claude" / "agent-outputs" / "archive"
            old_file_archived = not (
                project_dir / ".coordination" / "old_swarm.json"
            ).exists()
            print_test("Archives old coordination files (>7 days)", old_file_archived)
            self.results.append(("Archives old files", old_file_archived, ""))

            # Test 4: Recent files should be kept
            recent_file_kept = (project_dir / ".coordination" / "recent.json").exists()
            print_test("Keeps recent files (<7 days)", recent_file_kept)
            self.results.append(("Keeps recent files", recent_file_kept, ""))

            # Test 5: Empty files should be removed
            empty_file_removed = not (
                project_dir / ".coordination" / "empty.json"
            ).exists()
            print_test("Removes empty files", empty_file_removed)
            self.results.append(("Removes empty files", empty_file_removed, ""))

            # Test 6: Archive directory should be created
            archive_exists = archive_dir.exists()
            print_test("Creates archive directory", archive_exists)
            self.results.append(("Creates archive directory", archive_exists, ""))

        return self.results

    def _setup_test_files(self, project_dir: Path) -> None:
        """Create test file structure."""
        coord_dir = project_dir / ".coordination"
        coord_dir.mkdir(parents=True)

        # Create old file (>7 days)
        old_file = coord_dir / "old_swarm.json"
        old_file.write_text('{"test": "old"}')
        old_time = datetime.now() - timedelta(days=10)
        os.utime(old_file, (old_time.timestamp(), old_time.timestamp()))

        # Create recent file (<7 days)
        recent_file = coord_dir / "recent.json"
        recent_file.write_text('{"test": "recent"}')

        # Create empty file
        empty_file = coord_dir / "empty.json"
        empty_file.touch()

        # Create agent-outputs dir
        outputs_dir = project_dir / ".claude" / "agent-outputs"
        outputs_dir.mkdir(parents=True)


class TestValidateFileLocations:
    """Tests for validate_file_locations.py hook."""

    def __init__(self, hooks_dir: Path):
        self.hook = hooks_dir / "validate_file_locations.py"
        self.results = []

    def run_all(self) -> list[tuple[str, bool, str]]:
        print_header("Testing validate_file_locations.py")

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            (project_dir / ".coordination").mkdir(parents=True)
            (project_dir / "src").mkdir()

            # Test 1: Non-Write tool should pass through
            input_data = {"tool_name": "Read", "tool_input": {"file_path": "/test.py"}}
            exit_code, stdout, stderr = run_hook(self.hook, input_data, project_dir)
            test1_pass = exit_code == 0 and json.loads(stdout).get("ok")
            print_test("Non-Write tool passes through", test1_pass)
            self.results.append(("Non-Write passes", test1_pass, ""))

            # Test 2: Normal file in src should pass
            input_data = {
                "tool_name": "Write",
                "tool_input": {"file_path": str(project_dir / "src" / "module.py")},
            }
            exit_code, stdout, stderr = run_hook(self.hook, input_data, project_dir)
            test2_pass = exit_code == 0 and "warning" not in stdout.lower()
            print_test("Normal source file passes", test2_pass, stdout)
            self.results.append(("Normal file passes", test2_pass, ""))

            # Test 3: Intermediate file in src should warn
            input_data = {
                "tool_name": "Write",
                "tool_input": {
                    "file_path": str(project_dir / "src" / "ANALYSIS_NOTES.md")
                },
            }
            exit_code, stdout, stderr = run_hook(self.hook, input_data, project_dir)
            output = json.loads(stdout)
            test3_pass = exit_code == 0 and output.get("warning") is not None
            print_test("Intermediate file in src/ triggers warning", test3_pass, stdout)
            self.results.append(("Warns on intermediate in src", test3_pass, ""))

            # Test 4: Intermediate file in .coordination should pass
            input_data = {
                "tool_name": "Write",
                "tool_input": {
                    "file_path": str(project_dir / ".coordination" / "ANALYSIS.md")
                },
            }
            exit_code, stdout, stderr = run_hook(self.hook, input_data, project_dir)
            test4_pass = exit_code == 0 and "warning" not in stdout.lower()
            print_test("Intermediate file in .coordination/ passes", test4_pass)
            self.results.append(("Allowed in .coordination", test4_pass, ""))

            # Test 5: Various intermediate patterns detected
            patterns_to_test = [
                "TROUBLESHOOT.md",
                "PLAN.md",
                "SUMMARY.md",
                "ROOT_CAUSE.md",
                "DEBUG_NOTES.md",
                "TODO.md",
            ]
            all_detected = True
            for pattern in patterns_to_test:
                input_data = {
                    "tool_name": "Write",
                    "tool_input": {"file_path": str(project_dir / pattern)},
                }
                exit_code, stdout, _ = run_hook(self.hook, input_data, project_dir)
                output = json.loads(stdout)
                if not output.get("warning"):
                    all_detected = False
                    break
            print_test("Detects various intermediate file patterns", all_detected)
            self.results.append(("Detects all patterns", all_detected, ""))

        return self.results


class TestCheckStop:
    """Tests for check_stop.py hook."""

    def __init__(self, hooks_dir: Path):
        self.hook = hooks_dir / "check_stop.py"
        self.results = []

    def run_all(self) -> list[tuple[str, bool, str]]:
        print_header("Testing check_stop.py")

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            coord_dir = project_dir / ".coordination"
            coord_dir.mkdir(parents=True)

            # Test 1: No active work - should allow stop
            input_data = {"project_dir": str(project_dir)}
            exit_code, stdout, stderr = run_hook(self.hook, input_data, project_dir)
            test1_pass = exit_code == 0 and json.loads(stdout).get("ok")
            print_test("Allows stop with no active work", test1_pass)
            self.results.append(("Allows stop no work", test1_pass, ""))

            # Test 2: Active work - should block stop
            active_work = coord_dir / "active_work.json"
            active_work.write_text(
                json.dumps({"current_task": "TASK-007", "agent": "spec-implementer"})
            )
            exit_code, stdout, stderr = run_hook(self.hook, input_data, project_dir)
            test2_pass = exit_code == 2
            print_test("Blocks stop with active work", test2_pass, f"Exit: {exit_code}")
            self.results.append(("Blocks with active work", test2_pass, ""))

            # Test 3: stop_hook_active prevents infinite loop
            input_data["stop_hook_active"] = True
            exit_code, stdout, stderr = run_hook(self.hook, input_data, project_dir)
            test3_pass = exit_code == 0
            print_test("stop_hook_active=True prevents infinite loop", test3_pass)
            self.results.append(("Prevents infinite loop", test3_pass, ""))

            # Test 4: Stale active work (>2 hours) should allow stop
            del input_data["stop_hook_active"]
            old_time = datetime.now() - timedelta(hours=3)
            os.utime(active_work, (old_time.timestamp(), old_time.timestamp()))
            exit_code, stdout, stderr = run_hook(self.hook, input_data, project_dir)
            test4_pass = exit_code == 0
            print_test("Allows stop with stale active work (>2 hours)", test4_pass)
            self.results.append(("Allows stale work", test4_pass, ""))

            # Test 5: Work queue noted but doesn't block
            active_work.unlink()
            work_queue = coord_dir / "work_queue.json"
            work_queue.write_text(json.dumps({"tasks": ["task1", "task2"]}))
            exit_code, stdout, stderr = run_hook(self.hook, input_data, project_dir)
            test5_pass = exit_code == 0
            print_test("Work queue noted but doesn't block", test5_pass)
            self.results.append(("Queue doesn't block", test5_pass, ""))

        return self.results


class TestCheckSubagentStop:
    """Tests for check_subagent_stop.py hook."""

    def __init__(self, hooks_dir: Path):
        self.hook = hooks_dir / "check_subagent_stop.py"
        self.results = []

    def run_all(self) -> list[tuple[str, bool, str]]:
        print_header("Testing check_subagent_stop.py")

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            outputs_dir = project_dir / ".claude" / "agent-outputs"
            outputs_dir.mkdir(parents=True)

            # Test 1: Always allows subagent stop (permissive)
            input_data = {"project_dir": str(project_dir)}
            exit_code, stdout, stderr = run_hook(self.hook, input_data, project_dir)
            test1_pass = exit_code == 0 and json.loads(stdout).get("ok")
            print_test("Allows subagent stop (permissive)", test1_pass)
            self.results.append(("Allows subagent stop", test1_pass, ""))

            # Test 2: Detects recent completion reports
            report = outputs_dir / "2025-12-21-test-complete.json"
            report.write_text('{"status": "complete"}')
            exit_code, stdout, stderr = run_hook(self.hook, input_data, project_dir)
            test2_pass = exit_code == 0 and "recent completion report" in stderr.lower()
            print_test("Detects recent completion reports", test2_pass, stderr)
            self.results.append(("Detects completion reports", test2_pass, ""))

            # Test 3: stop_hook_active prevents infinite loop
            input_data["stop_hook_active"] = True
            exit_code, stdout, stderr = run_hook(self.hook, input_data, project_dir)
            test3_pass = exit_code == 0
            print_test("stop_hook_active=True prevents infinite loop", test3_pass)
            self.results.append(("Prevents infinite loop", test3_pass, ""))

            # Test 4: Handles missing outputs directory gracefully
            shutil.rmtree(outputs_dir)
            del input_data["stop_hook_active"]
            exit_code, stdout, stderr = run_hook(self.hook, input_data, project_dir)
            test4_pass = exit_code == 0
            print_test("Handles missing outputs directory", test4_pass)
            self.results.append(("Handles missing dir", test4_pass, ""))

        return self.results


def run_all_tests() -> int:
    """Run all hook tests and return exit code."""
    print(f"\n{Colors.BOLD}Claude Code Hooks Test Suite{Colors.RESET}")
    print("Testing hooks in: .claude/hooks/")

    # Find hooks directory
    script_dir = Path(__file__).parent
    hooks_dir = script_dir

    if not hooks_dir.exists():
        print(f"{Colors.RED}Error: Hooks directory not found{Colors.RESET}")
        return 1

    all_results = []

    # Run all test suites
    test_suites = [
        TestCleanupStaleFiles(hooks_dir),
        TestValidateFileLocations(hooks_dir),
        TestCheckStop(hooks_dir),
        TestCheckSubagentStop(hooks_dir),
    ]

    for suite in test_suites:
        results = suite.run_all()
        all_results.extend(results)

    # Summary
    print_header("TEST SUMMARY")
    passed = sum(1 for _, p, _ in all_results if p)
    failed = sum(1 for _, p, _ in all_results if not p)
    total = len(all_results)

    print(f"\n  {Colors.GREEN}Passed: {passed}{Colors.RESET}")
    print(f"  {Colors.RED}Failed: {failed}{Colors.RESET}")
    print(f"  Total:  {total}")

    if failed == 0:
        print(f"\n{Colors.GREEN}{Colors.BOLD}All tests passed! ✓{Colors.RESET}")
        return 0
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}Some tests failed!{Colors.RESET}")
        print("\nFailed tests:")
        for name, passed, details in all_results:
            if not passed:
                print(f"  - {name}: {details}")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())

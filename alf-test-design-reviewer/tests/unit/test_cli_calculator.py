"""Subprocess integration tests for cli_calculator.py."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

CLI_PATH = str(
    Path(__file__).resolve().parents[2]
    / "skills"
    / "test-design-reviewer"
    / "lib"
    / "cli_calculator.py"
)


def run_cli(command, data):
    """Run the CLI calculator as a subprocess and return parsed JSON."""
    result = subprocess.run(
        [sys.executable, CLI_PATH, command, json.dumps(data)],
        capture_output=True,
        text=True,
    )
    if result.stdout.strip():
        return json.loads(result.stdout.strip()), result.returncode
    return None, result.returncode


class TestCLIErrors:
    def test_missing_args(self):
        result = subprocess.run(
            [sys.executable, CLI_PATH],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1
        output = json.loads(result.stdout.strip())
        assert output["ok"] is False
        assert "Usage" in output["error"]

    def test_unknown_command(self):
        output, code = run_cli("unknown-cmd", {})
        assert code == 1
        assert output["ok"] is False
        assert "Unknown command" in output["error"]

    def test_invalid_json(self):
        result = subprocess.run(
            [sys.executable, CLI_PATH, "compute-farley", "not-json"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1
        output = json.loads(result.stdout.strip())
        assert output["ok"] is False
        assert "Invalid JSON" in output["error"]

    def test_missing_required_field(self):
        output, code = run_cli("normalize-property", {"prop": "U"})
        assert code == 1
        assert output["ok"] is False
        assert "Missing required field" in output["error"]


class TestNormalizePropertyCLI:
    def test_base_score(self):
        output, code = run_cli("normalize-property", {
            "prop": "U", "neg_count": 0, "pos_count": 0, "total_methods": 10,
        })
        assert code == 0
        assert output["ok"] is True
        assert output["result"]["score"] == 5.0


class TestBlendScoresCLI:
    def test_default_blend(self):
        output, code = run_cli("blend-scores", {
            "static_score": 8.0, "llm_score": 6.0,
        })
        assert code == 0
        assert output["ok"] is True
        assert output["result"]["score"] == 7.2


class TestComputeFarleyCLI:
    def test_all_nines(self):
        data = {"U": 9, "M": 9, "R": 9, "A": 9, "N": 9, "G": 9, "F": 9, "T": 9}
        output, code = run_cli("compute-farley", data)
        assert code == 0
        assert output["ok"] is True
        assert output["result"]["farley_index"] == 9.0
        assert output["result"]["rating"] == "Exemplary"


class TestGetRatingCLI:
    def test_rating_lookup(self):
        output, code = run_cli("get-rating", {"farley_index": 7.5})
        assert code == 0
        assert output["ok"] is True
        assert output["result"]["rating"] == "Excellent"


class TestAggregateFileCLI:
    def test_single_method(self):
        method = {"U": 8.0, "M": 7.0, "R": 9.0, "A": 6.0, "N": 5.0, "G": 7.0, "F": 8.0, "T": 6.0}
        output, code = run_cli("aggregate-file", {"method_scores": [method]})
        assert code == 0
        assert output["ok"] is True
        assert output["result"]["U"] == 8.0


class TestAggregateSuiteCLI:
    def test_two_files(self):
        f1 = {"U": 8.0, "M": 8.0, "R": 8.0, "A": 8.0, "N": 8.0, "G": 8.0, "F": 8.0, "T": 8.0}
        f2 = {"U": 6.0, "M": 6.0, "R": 6.0, "A": 6.0, "N": 6.0, "G": 6.0, "F": 6.0, "T": 6.0}
        output, code = run_cli("aggregate-suite", {
            "file_scores": [f1, f2],
            "file_locs": [100, 100],
        })
        assert code == 0
        assert output["ok"] is True
        assert output["result"]["U"] == 7.0


class TestFullPipelineCLI:
    def test_end_to_end(self):
        data = {
            "properties": {
                "U": {"neg_count": 0, "pos_count": 0, "total_methods": 10},
                "M": {"neg_count": 0, "pos_count": 0, "total_methods": 10},
                "R": {"neg_count": 0, "pos_count": 0, "total_methods": 10},
                "A": {"neg_count": 0, "pos_count": 0, "total_methods": 10},
                "N": {"neg_count": 0, "pos_count": 0, "total_methods": 10},
                "G": {"neg_count": 0, "pos_count": 0, "total_methods": 10},
                "F": {"neg_count": 0, "pos_count": 0, "total_methods": 10},
                "T": {"neg_count": 0, "pos_count": 0, "total_methods": 10},
            }
        }
        output, code = run_cli("full-pipeline", data)
        assert code == 0
        assert output["ok"] is True
        assert output["result"]["farley_index"] == 5.0
        assert output["result"]["rating"] == "Fair"

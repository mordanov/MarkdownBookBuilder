"""Pytest configuration and shared fixtures."""
import sys
from pathlib import Path

import pytest

# Add src to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))


@pytest.fixture(scope="session")
def project_root_path() -> Path:
    """Return the project root directory."""
    return project_root


@pytest.fixture(scope="session")
def fixtures_dir() -> Path:
    """Return the fixtures directory."""
    return project_root / "tests" / "fixtures"


@pytest.fixture(scope="session")
def golden_dir() -> Path:
    """Return the golden files directory."""
    return project_root / "tests" / "fixtures" / "golden"

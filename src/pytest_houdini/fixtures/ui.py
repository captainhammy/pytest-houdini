"""Fixtures to support mocking Houdini UI related functionality."""

# Future
from __future__ import annotations

# Standard Library
import sys
from typing import TYPE_CHECKING

# Third Party
import pytest

# Houdini
import hou

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


# Fixtures


@pytest.fixture
def mock_hdefereval(monkeypatch: pytest.MonkeyPatch, mocker: MockerFixture) -> MockerFixture:
    """Mock hdefereval which isn't available when running tests via Hython."""
    mocked_hdefereval = mocker.MagicMock()

    monkeypatch.setitem(sys.modules, "hdefereval", mocked_hdefereval)

    return mocked_hdefereval


@pytest.fixture
def mock_hou_qt(monkeypatch: pytest.MonkeyPatch, mocker: MockerFixture) -> MockerFixture:
    """Mock the hou.qt module which isn't available when running tests via Hython."""
    mock_qt = mocker.MagicMock()

    monkeypatch.setattr(hou, "qt", mock_qt, raising=False)

    return mock_qt


@pytest.fixture
def mock_hou_ui(monkeypatch: pytest.MonkeyPatch, mocker: MockerFixture) -> MockerFixture:
    """Mock the hou.ui module which isn't available when running tests via Hython."""
    mock_ui = mocker.MagicMock()

    monkeypatch.setattr(hou, "ui", mock_ui, raising=False)

    return mock_ui


@pytest.fixture
def set_ui_available(monkeypatch: pytest.MonkeyPatch) -> None:
    """Fixture to set hou.isUIAvailable() to return True."""
    monkeypatch.setattr(hou, "isUIAvailable", lambda: True)

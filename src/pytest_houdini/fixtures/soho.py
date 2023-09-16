"""Fixtures to support mocking Mantra/SOHO related functionality."""

# Future
from __future__ import annotations

# Standard Library
import sys
from collections import namedtuple
from typing import TYPE_CHECKING, NamedTuple

# Third Party
import pytest

if TYPE_CHECKING:
    from collections.abc import Generator

    from pytest_mock import MockerFixture

# Fixtures


@pytest.fixture
def patch_soho(
    monkeypatch: pytest.MonkeyPatch, mocker: MockerFixture
) -> Generator[NamedTuple, None, None]:
    """Mock importing of mantra/soho related modules.

    Available mocked modules are available via their original names from the fixture provided named tuple.

    Available mocked modules:
        - IFDapi
        - IFDframe
        - IFDhooks
        - IFDsettings
        - mantra
        - soho

    >>> def test_soho_thing(patch_soho):
    ...     patch_soho.mantra.property.return_value = 3
    ...     # Test code

    """
    mock_api = mocker.MagicMock()
    mock_frame = mocker.MagicMock()
    mock_hooks = mocker.MagicMock()
    mock_mantra = mocker.MagicMock()
    mock_settings = mocker.MagicMock()
    mock_soho = mocker.MagicMock()

    monkeypatch.setitem(sys.modules, "IFDapi", mock_api)
    monkeypatch.setitem(sys.modules, "IFDframe", mock_frame)
    monkeypatch.setitem(sys.modules, "IFDhooks", mock_hooks)
    monkeypatch.setitem(sys.modules, "IFDsettings", mock_settings)
    monkeypatch.setitem(sys.modules, "mantra", mock_mantra)
    monkeypatch.setitem(sys.modules, "soho", mock_soho)

    MockSoho = namedtuple(
        "MockSoho", "IFDapi IFDframe IFDhooks IFDsettings mantra soho"
    )

    yield MockSoho(
        mock_api, mock_frame, mock_hooks, mock_settings, mock_mantra, mock_soho
    )

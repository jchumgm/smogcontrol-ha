"""Fixtures for Smog Control tests."""

from collections.abc import Generator
from unittest.mock import AsyncMock, patch

import pytest
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.smogcontrol.const import DOMAIN


@pytest.fixture
def mock_config_entry(hass: HomeAssistant) -> MockConfigEntry:
    """Return a mock config entry."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={"sensor_id": 21203},
        entry_id="test_entry",
        title="Test Address (21203)",
    )
    entry.add_to_hass(hass)
    return entry


@pytest.fixture
def mock_api_response() -> dict:
    """Return mock API response."""
    return [
        {
            "id": 32358271,
            "sponsor": "UM Grodzisk Mazowiecki",
            "address": "CK ul. Spółdzielcza 9",
            "sensor_logo": "/media/grodzisk_wHDNoEx.png",
            "sponsor_url": None,
            "sensor_id": 21203,
            "pm1": "0.0",
            "pm25": "2.0",
            "pm10": "3.0",
            "temperatureo": "6.0",
            "humidity": "100.0",
            "pressure": "998.0",
            "timestamp": "2026-05-12T06:30:16Z",
            "temperature": "9.0",
            "air_condition_icon": "fa fa-smile-o",
            "pm10_icon": "fa fa-smile-o",
            "pm10_color": "#96c11f",
            "pm10_percentage": "2",
            "pm25_icon": "fa fa-smile-o",
            "pm25_color": "#96c11f",
            "pm25_percentage": "2",
            "air_info": "Czyste powietrze. Możesz wyjść z domu",
            "air_info_color": "#96c11f",
            "sensor": 21203,
        }
    ]

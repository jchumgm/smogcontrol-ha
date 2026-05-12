"""Test coordinator for Smog Control integration."""

from unittest.mock import AsyncMock, patch

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import UpdateFailed

from custom_components.smogcontrol.api import (
    SmogControlConnectionError,
    SmogControlInvalidSensor,
)
from custom_components.smogcontrol.coordinator import SmogControlDataUpdateCoordinator
from custom_components.smogcontrol.const import CONF_SCAN_INTERVAL, CONF_SENSOR_ID


@pytest.mark.asyncio
async def test_coordinator_update_success(hass: HomeAssistant, mock_api_response) -> None:
    """Test coordinator updates successfully."""
    mock_api = AsyncMock()
    mock_api.async_get_sensor = AsyncMock(return_value=mock_api_response[0])

    mock_entry = AsyncMock()
    mock_entry.options = {CONF_SCAN_INTERVAL: 10}

    coordinator = SmogControlDataUpdateCoordinator(
        hass=hass,
        api=mock_api,
        sensor_id=21203,
        config_entry=mock_entry,
    )

    result = await coordinator._async_update_data()

    assert result["sensor_id"] == 21203
    assert result["pm25"] == 2.0
    assert result["temperature"] == 9.0


@pytest.mark.asyncio
async def test_coordinator_update_invalid_sensor(hass: HomeAssistant) -> None:
    """Test coordinator handles invalid sensor."""
    mock_api = AsyncMock()
    mock_api.async_get_sensor = AsyncMock(
        side_effect=SmogControlInvalidSensor("Invalid sensor")
    )

    mock_entry = AsyncMock()
    mock_entry.options = {CONF_SCAN_INTERVAL: 10}

    coordinator = SmogControlDataUpdateCoordinator(
        hass=hass,
        api=mock_api,
        sensor_id=21203,
        config_entry=mock_entry,
    )

    with pytest.raises(UpdateFailed, match="Invalid sensor"):
        await coordinator._async_update_data()


@pytest.mark.asyncio
async def test_coordinator_update_connection_error(hass: HomeAssistant) -> None:
    """Test coordinator handles connection error."""
    mock_api = AsyncMock()
    mock_api.async_get_sensor = AsyncMock(
        side_effect=SmogControlConnectionError("Connection error")
    )

    mock_entry = AsyncMock()
    mock_entry.options = {CONF_SCAN_INTERVAL: 10}

    coordinator = SmogControlDataUpdateCoordinator(
        hass=hass,
        api=mock_api,
        sensor_id=21203,
        config_entry=mock_entry,
    )

    with pytest.raises(UpdateFailed, match="Connection error"):
        await coordinator._async_update_data()

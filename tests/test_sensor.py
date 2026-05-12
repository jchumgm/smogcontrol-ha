"""Test sensor entities for Smog Control integration."""

from unittest.mock import AsyncMock

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.smogcontrol.coordinator import SmogControlDataUpdateCoordinator
from custom_components.smogcontrol.sensor import async_setup_entry, ENTITY_DESCRIPTIONS
from custom_components.smogcontrol.const import CONF_SCAN_INTERVAL, CONF_SENSOR_ID


@pytest.mark.asyncio
async def test_sensor_setup(hass: HomeAssistant, mock_config_entry) -> None:
    """Test sensor entities are set up."""
    mock_coordinator = AsyncMock(spec=SmogControlDataUpdateCoordinator)
    mock_coordinator.sensor_id = 21203
    mock_coordinator.data = {
        "sensor_id": 21203,
        "address": "Test Address",
        "pm1": 0.0,
        "pm25": 2.0,
        "pm10": 3.0,
        "temperature": 9.0,
        "humidity": 100.0,
        "pressure": 998.0,
        "air_info": "Czyste powietrze",
        "air_info_color": "#96c11f",
        "air_condition_icon": "fa fa-smile-o",
        "pm10_color": "#96c11f",
        "pm10_percentage": "2",
        "pm10_icon": "fa fa-smile-o",
        "pm25_color": "#96c11f",
        "pm25_percentage": "2",
        "pm25_icon": "fa fa-smile-o",
        "sponsor": "Test Sponsor",
        "sponsor_url": None,
        "timestamp": "2026-05-12T06:30:16Z",
    }
    mock_coordinator.last_update_success = True

    mock_entry = AsyncMock()
    mock_entry.options = {CONF_SCAN_INTERVAL: 10}

    async_add_entities: AddEntitiesCallback = AsyncMock()

    hass.data = {mock_config_entry.domain: {mock_config_entry.entry_id: mock_coordinator}}

    await async_setup_entry(hass, mock_config_entry, async_add_entities)

    assert async_add_entities.call_count == 1
    entities = async_add_entities.call_args[0][0]
    assert len(entities) == len(ENTITY_DESCRIPTIONS)


@pytest.mark.asyncio
async def test_sensor_properties(hass: HomeAssistant) -> None:
    """Test sensor entity properties."""
    mock_coordinator = AsyncMock(spec=SmogControlDataUpdateCoordinator)
    mock_coordinator.sensor_id = 21203
    mock_coordinator.data = {
        "sensor_id": 21203,
        "address": "Test Address",
        "pm25": 2.0,
        "pm25_color": "#96c11f",
        "pm25_percentage": "2",
        "pm25_icon": "fa fa-smile-o",
        "sponsor": "Test Sponsor",
        "sponsor_url": None,
        "timestamp": "2026-05-12T06:30:16Z",
    }
    mock_coordinator.last_update_success = True

    mock_entry = AsyncMock()
    mock_entry.options = {CONF_SCAN_INTERVAL: 10}

    from custom_components.smogcontrol.sensor import SmogControlSensor

    sensor = SmogControlSensor(
        coordinator=mock_coordinator,
        description=ENTITY_DESCRIPTIONS[1],  # pm25
    )

    assert sensor.unique_id == "21203_pm25"
    assert sensor.native_value == 2.0
    assert sensor.available is True

    attrs = sensor.extra_state_attributes
    assert attrs["color"] == "#96c11f"
    assert attrs["percentage"] == "2"
    assert attrs["icon"] == "fa fa-smile-o"
    assert attrs["attribution"] == "Data provided by Smog Control (smogcontrol.pl)"

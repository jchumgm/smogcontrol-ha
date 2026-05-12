"""Test config flow for Smog Control integration."""

from unittest.mock import AsyncMock, patch

import pytest
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from custom_components.smogcontrol.api import (
    SmogControlConnectionError,
    SmogControlInvalidSensor,
)
from custom_components.smogcontrol.const import CONF_SENSOR_ID, DOMAIN
from custom_components.smogcontrol.config_flow import validate_input


@pytest.mark.asyncio
async def test_form_user(hass: HomeAssistant, mock_api_response) -> None:
    """Test we get the form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": "user"}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {}

    with patch(
        "custom_components.smogcontrol.config_flow.validate_input",
        return_value={
            "title": "Test Address (21203)",
            "data": mock_api_response[0],
        },
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_SENSOR_ID: 21203},
        )
        await hass.async_block_till_done()

        assert result2["type"] == FlowResultType.CREATE_ENTRY
        assert result2["title"] == "Test Address (21203)"
        assert result2["data"] == {CONF_SENSOR_ID: 21203}


@pytest.mark.asyncio
async def test_form_invalid_sensor(hass: HomeAssistant) -> None:
    """Test we handle invalid sensor."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": "user"}
    )

    with patch(
        "custom_components.smogcontrol.config_flow.validate_input",
        side_effect=SmogControlInvalidSensor("Invalid sensor"),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_SENSOR_ID: 99999},
        )
        await hass.async_block_till_done()

        assert result2["type"] == FlowResultType.FORM
        assert result2["errors"] == {"base": "invalid_sensor"}


@pytest.mark.asyncio
async def test_form_cannot_connect(hass: HomeAssistant) -> None:
    """Test we handle connection error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": "user"}
    )

    with patch(
        "custom_components.smogcontrol.config_flow.validate_input",
        side_effect=SmogControlConnectionError("Connection error"),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_SENSOR_ID: 21203},
        )
        await hass.async_block_till_done()

        assert result2["type"] == FlowResultType.FORM
        assert result2["errors"] == {"base": "cannot_connect"}


@pytest.mark.asyncio
async def test_form_already_configured(hass: HomeAssistant, mock_api_response) -> None:
    """Test we handle already configured sensor."""
    entry = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": "user"},
        data={CONF_SENSOR_ID: 21203},
    )
    await hass.async_block_till_done()

    result2 = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": "user"}
    )

    with patch(
        "custom_components.smogcontrol.config_flow.validate_input",
        return_value={
            "title": "Test Address (21203)",
            "data": mock_api_response[0],
        },
    ):
        result3 = await hass.config_entries.flow.async_configure(
            result2["flow_id"],
            {CONF_SENSOR_ID: 21203},
        )
        await hass.async_block_till_done()

        assert result3["type"] == FlowResultType.ABORT
        assert result3["reason"] == "already_configured"

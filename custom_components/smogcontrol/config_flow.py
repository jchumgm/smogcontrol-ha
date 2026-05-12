"""Config flow for Smog Control integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from aiohttp import ClientError, ClientSession
from homeassistant.config_entries import ConfigEntry, ConfigFlow, OptionsFlow
from homeassistant.const import CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import SmogControlApiClient, SmogControlConnectionError, SmogControlInvalidSensor
from .const import (
    CONF_SENSOR_ID,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    MAX_SCAN_INTERVAL,
    MIN_SCAN_INTERVAL,
)


async def validate_input(hass: HomeAssistant, sensor_id: int) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    session = async_get_clientsession(hass)
    api = SmogControlApiClient(session)

    try:
        data = await api.async_get_sensor(sensor_id)
        return {"title": f"{data.get('address', 'Unknown')} ({sensor_id})", "data": data}
    except SmogControlInvalidSensor:
        raise
    except SmogControlConnectionError:
        raise
    except (ClientError, Exception) as err:
        raise SmogControlConnectionError(f"Unexpected error: {err}") from err


class SmogControlConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Smog Control."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            sensor_id = user_input[CONF_SENSOR_ID]
            await self.async_set_unique_id(str(sensor_id))
            self._abort_if_unique_id_configured()

            try:
                info = await validate_input(self.hass, sensor_id)
                return self.async_create_entry(title=info["title"], data=user_input)
            except SmogControlInvalidSensor:
                errors["base"] = "invalid_sensor"
            except SmogControlConnectionError:
                errors["base"] = "cannot_connect"
            except Exception:  # noqa: BLE001
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required(CONF_SENSOR_ID, default=21203): vol.Coerce(int)}
            ),
            errors=errors,
        )

    async def async_step_reauth(
        self, entry_data: dict[str, Any]
    ) -> FlowResult:
        """Handle re-authentication."""
        return await self.async_step_user()

    async def async_step_options(
        self, config_entry: ConfigEntry, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle options flow."""
        errors: dict[str, str] = {}

        if user_input is not None:
            scan_interval = user_input[CONF_SCAN_INTERVAL]
            if MIN_SCAN_INTERVAL <= scan_interval <= MAX_SCAN_INTERVAL:
                self.hass.config_entries.async_update_entry(
                    config_entry, options=user_input
                )
                await self.hass.config_entries.async_reload(config_entry.entry_id)
                return self.async_create_entry(title="", data={})
            errors["base"] = "invalid_interval"

        current_interval = config_entry.options.get(
            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
        )

        return self.async_show_form(
            step_id="options",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_SCAN_INTERVAL,
                        default=current_interval,
                    ): vol.All(vol.Coerce(int), vol.Range(min=MIN_SCAN_INTERVAL, max=MAX_SCAN_INTERVAL))
                }
            ),
            errors=errors,
        )

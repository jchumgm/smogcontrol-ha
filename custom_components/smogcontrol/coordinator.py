"""Data update coordinator for Smog Control."""

from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import SmogControlApiClient, SmogControlConnectionError, SmogControlInvalidSensor
from .const import (
    CONF_SCAN_INTERVAL,
    CONF_SENSOR_ID,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    MIN_SCAN_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)


class SmogControlDataUpdateCoordinator(DataUpdateCoordinator[dict]):
    """Coordinator to fetch data from Smog Control API."""

    def __init__(
        self,
        hass: HomeAssistant,
        api: SmogControlApiClient,
        sensor_id: int,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize coordinator."""
        self.api = api
        self.sensor_id = sensor_id
        self.config_entry = config_entry

        scan_interval = config_entry.options.get(
            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
        )

        super().__init__(
            hass,
            logger=_LOGGER,
            name=f"{DOMAIN}_{sensor_id}",
            update_interval=timedelta(minutes=scan_interval),
        )

    async def _async_update_data(self) -> dict:
        """Fetch data from API."""
        try:
            return await self.api.async_get_sensor(self.sensor_id)
        except SmogControlInvalidSensor as err:
            raise UpdateFailed(f"Invalid sensor: {err}") from err
        except SmogControlConnectionError as err:
            raise UpdateFailed(f"Connection error: {err}") from err

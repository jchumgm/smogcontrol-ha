"""Sensor entities for Smog Control integration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    UnitOfPressure,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, DOMAIN, MANUFACTURER
from .coordinator import SmogControlDataUpdateCoordinator

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity_platform import AddEntitiesCallback


@dataclass(frozen=True, kw_only=True)
class SmogControlSensorEntityDescription(SensorEntityDescription):
    """Describes Smog Control sensor entity."""

    icon: str | None = None


ENTITY_DESCRIPTIONS: list[SmogControlSensorEntityDescription] = [
    SmogControlSensorEntityDescription(
        key="pm1",
        device_class=SensorDeviceClass.PM1,
        native_unit_of_measurement="µg/m³",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SmogControlSensorEntityDescription(
        key="pm25",
        device_class=SensorDeviceClass.PM25,
        native_unit_of_measurement="µg/m³",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SmogControlSensorEntityDescription(
        key="pm10",
        device_class=SensorDeviceClass.PM10,
        native_unit_of_measurement="µg/m³",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SmogControlSensorEntityDescription(
        key="temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SmogControlSensorEntityDescription(
        key="humidity",
        device_class=SensorDeviceClass.HUMIDITY,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SmogControlSensorEntityDescription(
        key="pressure",
        device_class=SensorDeviceClass.ATMOSPHERIC_PRESSURE,
        native_unit_of_measurement=UnitOfPressure.HPA,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SmogControlSensorEntityDescription(
        key="air_info",
        icon="mdi:weather-hazy",
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Smog Control sensor entities."""
    coordinator: SmogControlDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        SmogControlSensor(
            coordinator=coordinator,
            description=description,
        )
        for description in ENTITY_DESCRIPTIONS
    )


class SmogControlSensor(CoordinatorEntity[SmogControlDataUpdateCoordinator], SensorEntity):
    """Representation of a Smog Control sensor."""

    entity_description: SmogControlSensorEntityDescription

    def __init__(
        self,
        coordinator: SmogControlDataUpdateCoordinator,
        description: SmogControlSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.sensor_id}_{description.key}"
        self._attr_has_entity_name = True

    @property
    def native_value(self) -> float | str | None:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None
        return self.coordinator.data.get(self.entity_description.key)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        if not self.coordinator.last_update_success:
            return False
        return self.coordinator.data is not None

    @property
    def extra_state_attributes(self) -> dict[str, str | None]:
        """Return additional state attributes."""
        if not self.coordinator.data:
            return {}

        data = self.coordinator.data
        attrs = {
            "attribution": ATTRIBUTION,
            "last_updated": data.get("timestamp"),
            "sponsor": data.get("sponsor"),
            "sponsor_url": data.get("sponsor_url"),
        }

        key = self.entity_description.key

        if key in ["pm10", "pm25"]:
            attrs["color"] = data.get(f"{key}_color")
            attrs["percentage"] = data.get(f"{key}_percentage")
            attrs["icon"] = data.get(f"{key}_icon")
        elif key == "air_info":
            attrs["color"] = data.get("air_info_color")
            attrs["icon"] = data.get("air_condition_icon")

        return attrs

    @property
    def device_info(self) -> dict[str, any]:
        """Return device information."""
        data = self.coordinator.data or {}
        return {
            "identifiers": {(DOMAIN, self.coordinator.sensor_id)},
            "name": data.get("address", f"Sensor {self.coordinator.sensor_id}"),
            "manufacturer": MANUFACTURER,
            "model": f"Sensor {self.coordinator.sensor_id}",
            "configuration_url": "https://smogcontrol.pl/",
        }

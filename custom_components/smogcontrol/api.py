"""API client for Smog Control."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aiohttp import ClientError, ClientResponseError, ClientSession
from datetime import datetime

if TYPE_CHECKING:
    from .const import CONF_SENSOR_ID


class SmogControlError(Exception):
    """Base exception for Smog Control errors."""


class SmogControlConnectionError(SmogControlError):
    """Exception raised when connection to Smog Control API fails."""


class SmogControlInvalidSensor(SmogControlError):
    """Exception raised when sensor ID is invalid or sensor not found."""


class SmogControlApiClient:
    """API client for Smog Control."""

    def __init__(self, session: ClientSession) -> None:
        """Initialize the API client."""
        self._session = session

    def _to_float(self, value: str | None) -> float | None:
        """Safely convert string to float."""
        if value is None:
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    async def async_get_sensor(self, sensor_id: int) -> dict:
        """Get sensor data from Smog Control API."""
        from .const import API_URL

        url = API_URL.format(sensor_id=sensor_id)

        try:
            async with self._session.get(
                url,
                headers={
                    "Accept": "application/json",
                    "User-Agent": "HomeAssistant-SmogControl/0.1.0",
                    "Referer": "https://smogcontrol.pl/",
                },
            ) as response:
                if response.status == 404:
                    raise SmogControlInvalidSensor(f"Sensor {sensor_id} not found")

                response.raise_for_status()
                data = await response.json()

                if not isinstance(data, list) or len(data) == 0:
                    raise SmogControlInvalidSensor(f"No data for sensor {sensor_id}")

                sensor_data = data[0]

                # Validate sensor_id matches
                if str(sensor_data.get("sensor")) != str(sensor_id):
                    raise SmogControlInvalidSensor(f"Sensor ID mismatch")

                # Parse and normalize data
                parsed = {
                    "id": sensor_data.get("id"),
                    "sponsor": sensor_data.get("sponsor"),
                    "address": sensor_data.get("address"),
                    "sensor_logo": sensor_data.get("sensor_logo"),
                    "sponsor_url": sensor_data.get("sponsor_url"),
                    "sensor_id": sensor_data.get("sensor"),
                    "pm1": self._to_float(sensor_data.get("pm1")),
                    "pm25": self._to_float(sensor_data.get("pm25")),
                    "pm10": self._to_float(sensor_data.get("pm10")),
                    "temperature": self._to_float(sensor_data.get("temperature")),
                    "humidity": self._to_float(sensor_data.get("humidity")),
                    "pressure": self._to_float(sensor_data.get("pressure")),
                    "timestamp": sensor_data.get("timestamp"),
                    "air_condition_icon": sensor_data.get("air_condition_icon"),
                    "pm10_icon": sensor_data.get("pm10_icon"),
                    "pm10_color": sensor_data.get("pm10_color"),
                    "pm10_percentage": sensor_data.get("pm10_percentage"),
                    "pm25_icon": sensor_data.get("pm25_icon"),
                    "pm25_color": sensor_data.get("pm25_color"),
                    "pm25_percentage": sensor_data.get("pm25_percentage"),
                    "air_info": sensor_data.get("air_info"),
                    "air_info_color": sensor_data.get("air_info_color"),
                }

                # Parse timestamp to datetime
                if parsed["timestamp"]:
                    try:
                        parsed["timestamp"] = datetime.fromisoformat(
                            parsed["timestamp"].replace("Z", "+00:00")
                        )
                    except (ValueError, AttributeError):
                        parsed["timestamp"] = None

                return parsed

        except ClientResponseError as err:
            if err.status == 404:
                raise SmogControlInvalidSensor(f"Sensor {sensor_id} not found") from err
            raise SmogControlConnectionError(f"API error: {err}") from err
        except ClientError as err:
            raise SmogControlConnectionError(f"Connection error: {err}") from err

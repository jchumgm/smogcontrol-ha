"""Constants for Smog Control integration."""

DOMAIN = "smogcontrol"
CONF_SENSOR_ID = "sensor_id"
CONF_SCAN_INTERVAL = "scan_interval"
DEFAULT_SCAN_INTERVAL = 10  # minutes
MIN_SCAN_INTERVAL = 5
MAX_SCAN_INTERVAL = 60
API_URL = "https://smogcontrol.pl/api/sensors/data/{sensor_id}/"
ATTRIBUTION = "Data provided by Smog Control (smogcontrol.pl)"
MANUFACTURER = "Smog Control"

# Smog Control Integration for Home Assistant

[![HACS Badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)

Custom Home Assistant integration for [Smog Control](https://smogcontrol.pl/) air quality sensors.

## Features

- Monitor PM1, PM2.5, PM10 particulate matter levels
- Temperature, humidity, and atmospheric pressure readings
- Air quality condition with color-coded status
- Multiple sensors support via UI configuration
- Configurable update interval (default 10 minutes)
- Polish and English translations

## Installation

### HACS Installation

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the three dots menu and select "Custom repositories"
4. Add this repository URL
5. Search for "Smog Control" and install it
6. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/smogcontrol` directory to your Home Assistant configuration directory
2. Restart Home Assistant
3. Go to Settings > Devices & services > Add integration
4. Search for "Smog Control"

## Configuration

### Finding Your Sensor ID

1. Visit [Smog Control Map](https://smogcontrol.pl/mapa/smog.html)
2. Find your desired sensor on the map
3. Note the sensor ID from the URL or sensor details

### Adding a Sensor

1. Go to Settings > Devices & services
2. Click "Add integration"
3. Search for "Smog Control"
4. Enter your sensor ID
5. The integration will validate the sensor and create entities

### Multiple Sensors

You can add multiple sensors by repeating the above process. Each sensor will create its own device with all entities.

### Update Interval

By default, the integration polls the API every 10 minutes. You can adjust this:

1. Go to Settings > Devices & services
2. Find your Smog Control integration
3. Click the three dots and select "Configure"
4. Adjust the scan interval (5-60 minutes)

## Entities

Each sensor creates the following entities:

| Entity | Description | Unit |
|--------|-------------|------|
| PM1 | Particulate matter 1µm | µg/m³ |
| PM2.5 | Particulate matter 2.5µm | µg/m³ |
| PM10 | Particulate matter 10µm | µg/m³ |
| Temperature | Ambient temperature | °C |
| Humidity | Relative humidity | % |
| Pressure | Atmospheric pressure | hPa |
| Air condition | Air quality status text | - |

### Attributes

- **PM sensors**: color, percentage, icon
- **Air condition**: color, icon
- **All entities**: attribution, last updated, sponsor, sponsor URL

## Development

This is an unofficial integration. Smog Control data is provided by [smogcontrol.pl](https://smogcontrol.pl/).

## License

MIT License

"""Data coordinator for IntuiTherm integration."""
from __future__ import annotations

import asyncio
from datetime import datetime, timezone, timedelta
import logging
from typing import Any

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DOMAIN,
    ENDPOINT_HEALTH,
    ENDPOINT_CONTROL_STATUS,
    ENDPOINT_METRICS,
    ENDPOINT_CONTROL_OVERRIDE,
    ENDPOINT_CONTROL_ENABLE,
    ENDPOINT_CONTROL_DISABLE,
    ENDPOINT_SENSORS,
    ENDPOINT_SENSOR_READINGS,
    CONF_SOLAR_SENSORS,
    CONF_BATTERY_DISCHARGE_SENSORS,
    CONF_BATTERY_CHARGE_SENSORS,
    CONF_GRID_IMPORT_SENSORS,
    CONF_GRID_EXPORT_SENSORS,
    CONF_BATTERY_SOC_ENTITY,
)

_LOGGER = logging.getLogger(__name__)


class IntuiThermCoordinator(DataUpdateCoordinator):
    """Coordinator to fetch data from IntuiTherm service."""

    def __init__(
        self,
        hass: HomeAssistant,
        session: aiohttp.ClientSession,
        service_url: str,
        api_key: str,
        update_interval: timedelta,
        entry: Any = None,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )
        self.service_url = service_url.rstrip("/")
        self.api_key = api_key
        self.session = session
        self.headers = {"Authorization": f"Bearer {api_key}"}
        self.entry = entry
        self._sensors_registered = False

        _LOGGER.info(
            "IntuiTherm coordinator initialized (service: %s, interval: %s)",
            self.service_url,
            update_interval,
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from IntuiTherm service."""
        _LOGGER.debug("Fetching data from IntuiTherm service")

        try:
            # Register sensors on first run
            if not self._sensors_registered and self.entry:
                await self._register_sensors()
                self._sensors_registered = True

            # Send sensor readings
            if self.entry:
                await self._send_sensor_readings()

            async with asyncio.timeout(10):
                # Fetch all endpoints in parallel for efficiency
                health_task = self._fetch_json(ENDPOINT_HEALTH)
                status_task = self._fetch_json(ENDPOINT_CONTROL_STATUS)
                metrics_task = self._fetch_json(ENDPOINT_METRICS, params={"period_hours": 1})

                health, status, metrics = await asyncio.gather(
                    health_task,
                    status_task,
                    metrics_task,
                    return_exceptions=True,
                )

            # Build response, handling individual failures gracefully
            data = {
                "last_update": datetime.now(timezone.utc).isoformat(),
            }

            if isinstance(health, Exception):
                _LOGGER.warning("Failed to fetch health: %s", health)
                data["health"] = None
            else:
                data["health"] = health

            if isinstance(status, Exception):
                _LOGGER.warning("Failed to fetch control status: %s", status)
                data["control"] = None
            else:
                data["control"] = status

            if isinstance(metrics, Exception):
                _LOGGER.warning("Failed to fetch metrics: %s", metrics)
                data["metrics"] = None
            else:
                data["metrics"] = metrics

            _LOGGER.debug("Data fetch complete")
            return data

        except asyncio.TimeoutError as err:
            raise UpdateFailed(f"Timeout fetching data from service: {err}") from err
        except Exception as err:
            raise UpdateFailed(f"Error communicating with service: {err}") from err

    async def _fetch_json(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Fetch JSON data from an endpoint."""
        url = f"{self.service_url}{endpoint}"

        try:
            async with self.session.get(
                url, headers=self.headers, params=params
            ) as response:
                response.raise_for_status()
                return await response.json()

        except aiohttp.ClientResponseError as err:
            if err.status == 401:
                _LOGGER.error(
                    "Authentication failed for %s - check API key", endpoint
                )
            raise
        except aiohttp.ClientError as err:
            _LOGGER.error("HTTP error fetching %s: %s", endpoint, err)
            raise
        except Exception as err:
            _LOGGER.error("Unexpected error fetching %s: %s", endpoint, err)
            raise

    async def _post_json(
        self,
        endpoint: str,
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Post JSON data to an endpoint."""
        url = f"{self.service_url}{endpoint}"

        try:
            async with self.session.post(
                url, headers=self.headers, json=data
            ) as response:
                response.raise_for_status()
                return await response.json()

        except aiohttp.ClientResponseError as err:
            if err.status == 401:
                _LOGGER.error(
                    "Authentication failed for %s - check API key", endpoint
                )
            elif err.status == 400:
                _LOGGER.error("Bad request to %s: %s", endpoint, await response.text())
            raise
        except aiohttp.ClientError as err:
            _LOGGER.error("HTTP error posting to %s: %s", endpoint, err)
            raise
        except Exception as err:
            _LOGGER.error("Unexpected error posting to %s: %s", endpoint, err)
            raise

    async def async_manual_override(
        self,
        action: str,
        power_kw: float | None = None,
        duration_minutes: int | None = None,
    ) -> dict[str, Any]:
        """Send manual control override command."""
        _LOGGER.info(
            "Sending manual override: action=%s, power=%s, duration=%s",
            action,
            power_kw,
            duration_minutes,
        )

        payload = {"action": action}
        if power_kw is not None:
            payload["power_kw"] = power_kw
        if duration_minutes is not None:
            payload["duration_minutes"] = duration_minutes

        try:
            result = await self._post_json(ENDPOINT_CONTROL_OVERRIDE, data=payload)
            _LOGGER.info("Manual override successful: %s", result.get("message"))
            return result
        except Exception as err:
            _LOGGER.error("Manual override failed: %s", err)
            return {"status": "failed", "detail": str(err)}

    async def async_enable_auto_control(self) -> dict[str, Any]:
        """Enable automatic battery control."""
        _LOGGER.info("Enabling automatic control")

        try:
            result = await self._post_json(ENDPOINT_CONTROL_ENABLE)
            _LOGGER.info("Automatic control enabled: %s", result.get("message"))
            return result
        except Exception as err:
            _LOGGER.error("Failed to enable automatic control: %s", err)
            return {"status": "failed", "detail": str(err)}

    async def async_disable_auto_control(self) -> dict[str, Any]:
        """Disable automatic battery control."""
        _LOGGER.info("Disabling automatic control")

        try:
            result = await self._post_json(ENDPOINT_CONTROL_DISABLE)
            _LOGGER.info("Automatic control disabled: %s", result.get("message"))
            return result
        except Exception as err:
            _LOGGER.error("Failed to disable automatic control: %s", err)
            return {"status": "failed", "detail": str(err)}

    async def _register_sensors(self) -> None:
        """Register sensors with the backend."""
        if not self.entry:
            return

        config = {**self.entry.data, **self.entry.options}
        
        # Note: Backend uses /sensors/data endpoint, so we don't need explicit registration
        # Sensors are auto-created when first data is sent
        _LOGGER.info("Sensors will be auto-registered on first data send")
        
    async def _send_sensor_readings(self) -> None:
        """Send current sensor readings to the backend."""
        if not self.entry:
            return

        config = {**self.entry.data, **self.entry.options}
        
        # Map our sensor categories to backend sensor types
        sensor_mappings = [
            (config.get(CONF_SOLAR_SENSORS, []), "solar"),
            (config.get(CONF_BATTERY_DISCHARGE_SENSORS, []), "soc"),  # Battery discharge correlates with SOC
            (config.get(CONF_BATTERY_CHARGE_SENSORS, []), "soc"),
            (config.get(CONF_GRID_IMPORT_SENSORS, []), "load"),  # Grid import indicates load
            (config.get(CONF_GRID_EXPORT_SENSORS, []), "load"),
        ]
        
        # Add battery SOC if configured
        if battery_soc := config.get(CONF_BATTERY_SOC_ENTITY):
            sensor_mappings.append(([battery_soc], "soc"))

        # Send data for each sensor type
        for entity_ids, sensor_type in sensor_mappings:
            for entity_id in entity_ids:
                state = self.hass.states.get(entity_id)
                if state and state.state not in ("unknown", "unavailable"):
                    try:
                        value = float(state.state)
                        timestamp = datetime.now(timezone.utc)
                        
                        # Send to backend using /sensors/data endpoint
                        await self._post_json(
                            "/api/v1/sensors/data",
                            data={
                                "sensor_type": sensor_type,
                                "entity_id": entity_id,
                                "readings": [
                                    {
                                        "timestamp": timestamp.isoformat(),
                                        "value": value,
                                    }
                                ],
                            }
                        )
                        _LOGGER.debug("Sent %s reading for %s: %s", sensor_type, entity_id, value)
                    except (ValueError, TypeError) as err:
                        _LOGGER.debug("Could not parse value for %s: %s", entity_id, state.state)
                    except Exception as err:
                        _LOGGER.debug("Failed to send reading for %s: %s", entity_id, err)


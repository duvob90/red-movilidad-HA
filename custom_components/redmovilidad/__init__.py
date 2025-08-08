"""Integración Red Movilidad – Inicialización del componente."""
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DOMAIN, PLATFORMS, CONF_STOP_CODE
from datetime import timedelta

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=30)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    stop_code = entry.data[CONF_STOP_CODE]
    session = async_get_clientsession(hass)

    async def async_update_data():
        url = f"https://red-api.chewy.workers.dev/stops/{stop_code}/next_arrivals"
        async with session.get(url) as response:
            if response.status != 200:
                raise UpdateFailed(f"API error: {response.status}")
            data = await response.json()
            results = data.get("results", [])
            next_buses = []
            for r in results:
                route = r.get("route_id")
                eta = r.get("arrival_estimation", "").strip()
                if route and eta:
                    next_buses.append({"route_id": route, "arrival_estimation": eta})
            text = " | ".join(f"{b['route_id']}: {b['arrival_estimation']}" for b in next_buses)
            return {
                "next_buses": next_buses,
                "next_buses_text": text
            }

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"redmovilidad_{stop_code}",
        update_method=async_update_data,
        update_interval=SCAN_INTERVAL
    )
    await coordinator.async_config_entry_first_refresh()

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unloaded

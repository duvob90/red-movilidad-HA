"""Sensor para Integración Red Movilidad."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, CONF_STOP_CODE

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([RedMovilidadSensor(coordinator, entry.data[CONF_STOP_CODE])])

class RedMovilidadSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, stop_code):
        super().__init__(coordinator)
        self._attr_name = f"Paradero {stop_code}"
        self._attr_unique_id = stop_code
        self._attr_icon = "mdi:bus"
        self._stop_code = stop_code

    @property
    def native_value(self):
        data = self.coordinator.data
        if data and data.get("next_buses"):
            bus = data["next_buses"][0]
            return f"{bus['route_id']}: {bus['arrival_estimation']}"
        return "Sin datos"

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data or {}
        return {
            "next_buses": data.get("next_buses", []),
            "next_buses_text": data.get("next_buses_text", "")
        }

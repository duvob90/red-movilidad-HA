"""Config flow para Integración Red Movilidad."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, CONF_STOP_CODE

class RedMovilidadConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            stop_code = user_input[CONF_STOP_CODE].strip().upper()
            await self.async_set_unique_id(stop_code)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=f"Paradero {stop_code}", data={CONF_STOP_CODE: stop_code})

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_STOP_CODE): str}),
            errors=errors
        )

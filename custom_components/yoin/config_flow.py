"""Config flow to configure the Yoin integration."""

from abc import ABC, abstractmethod
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry, ConfigFlow, OptionsFlow
from homeassistant.const import CONF_PASSWORD, CONF_SCAN_INTERVAL, CONF_USERNAME
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowHandler, FlowResult
from homeassistant.helpers.selector import (
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
    TextSelector,
    TextSelectorConfig,
    TextSelectorType,
)
from homeassistant.helpers.typing import UNDEFINED
import voluptuous as vol

from .client import YoinClient
from .const import COORDINATOR_MIN_UPDATE_INTERVAL, DOMAIN, NAME
from .exceptions import BadCredentialsException, YoinServiceException
from .models import YoinConfigEntryData

_LOGGER = logging.getLogger(__name__)

DEFAULT_ENTRY_DATA = YoinConfigEntryData(
    username=None,
    password=None,
    scan_interval=COORDINATOR_MIN_UPDATE_INTERVAL,
)


class YoinCommonFlow(ABC, FlowHandler):
    """Base class for Yoin flows."""

    def __init__(self, initial_data: YoinConfigEntryData) -> None:
        """Initialize YoinCommonFlow."""
        self.initial_data = initial_data
        self.new_entry_data = YoinConfigEntryData()
        self.new_title: str | None = None

    @abstractmethod
    def finish_flow(self) -> FlowResult:
        """Finish the flow."""

    def new_data(self):
        """Construct new data."""
        return DEFAULT_ENTRY_DATA | self.initial_data | self.new_entry_data

    async def async_validate_input(self, user_input: dict[str, Any]) -> None:
        """Validate user credentials."""

        client = YoinClient(
            username=user_input[CONF_USERNAME],
            password=user_input[CONF_PASSWORD],
        )
        profile = await self.hass.async_add_executor_job(client.login)

        return profile

    async def async_step_connection_init(
        self, user_input: dict | None = None
    ) -> FlowResult:
        """Handle connection configuration."""
        errors: dict = {}

        if user_input is not None:
            user_input = self.new_data() | user_input
            test = await self.test_connection(user_input)
            if not test["errors"]:
                self.new_title = user_input[CONF_USERNAME]
                self.new_entry_data |= user_input
                await self.async_set_unique_id(f"{DOMAIN}_" + user_input[CONF_USERNAME])
                self._abort_if_unique_id_configured()
                _LOGGER.debug(f"New account {self.new_title} added")
                return self.finish_flow()
            errors = test["errors"]
        fields = {
            vol.Required(CONF_USERNAME): TextSelector(
                TextSelectorConfig(type=TextSelectorType.EMAIL, autocomplete="username")
            ),
            vol.Required(CONF_PASSWORD): TextSelector(
                TextSelectorConfig(
                    type=TextSelectorType.PASSWORD, autocomplete="current-password"
                )
            ),
            vol.Required(
                CONF_SCAN_INTERVAL, default=COORDINATOR_MIN_UPDATE_INTERVAL
            ): NumberSelector(
                NumberSelectorConfig(
                    min=COORDINATOR_MIN_UPDATE_INTERVAL,
                    max=48,
                    step=1,
                    mode=NumberSelectorMode.BOX,
                )
            ),
        }
        return self.async_show_form(
            step_id="connection_init",
            data_schema=vol.Schema(fields),
            errors=errors,
        )

    async def test_connection(self, user_input: dict | None = None) -> dict:
        """Test the connection to Yoin."""
        errors: dict = {}
        profile: dict = {}

        if user_input is not None:
            user_input = self.new_data() | user_input
            try:
                profile = await self.async_validate_input(user_input)
            except AssertionError as exception:
                errors["base"] = "cannot_connect"
                _LOGGER.debug(f"[async_step_password|login] AssertionError {exception}")
            except ConnectionError:
                errors["base"] = "cannot_connect"
            except YoinServiceException:
                errors["base"] = "service_error"
            except BadCredentialsException:
                errors["base"] = "invalid_auth"
            except Exception as exception:
                errors["base"] = "unknown"
                _LOGGER.debug(exception)
        return {"profile": profile, "errors": errors}

    async def async_step_scan_interval(
        self, user_input: dict | None = None
    ) -> FlowResult:
        """Configure update interval."""
        errors: dict = {}

        if user_input is not None:
            self.new_entry_data |= user_input
            return self.finish_flow()

        fields = {
            vol.Required(
                CONF_SCAN_INTERVAL, default=COORDINATOR_MIN_UPDATE_INTERVAL
            ): NumberSelector(
                NumberSelectorConfig(
                    min=COORDINATOR_MIN_UPDATE_INTERVAL,
                    max=48,
                    step=1,
                    mode=NumberSelectorMode.BOX,
                )
            ),
        }
        return self.async_show_form(
            step_id="scan_interval",
            data_schema=self.add_suggested_values_to_schema(
                vol.Schema(fields),
                self.initial_data,
            ),
            errors=errors,
        )

    async def async_step_username_password(
        self, user_input: dict | None = None
    ) -> FlowResult:
        """Configure username & password."""
        errors: dict = {}

        if user_input is not None:
            user_input = self.new_data() | user_input
            test = await self.test_connection(user_input)
            if not test["errors"]:
                self.new_entry_data |= YoinConfigEntryData(
                    username=user_input[CONF_USERNAME],
                    password=user_input[CONF_PASSWORD],
                )
                return self.finish_flow()

        fields = {
            vol.Required(CONF_USERNAME): TextSelector(
                TextSelectorConfig(type=TextSelectorType.EMAIL, autocomplete="username")
            ),
            vol.Required(CONF_PASSWORD): TextSelector(
                TextSelectorConfig(
                    type=TextSelectorType.PASSWORD, autocomplete="current-password"
                )
            ),
        }
        return self.async_show_form(
            step_id="username_password",
            data_schema=self.add_suggested_values_to_schema(
                vol.Schema(fields),
                self.initial_data
                | YoinConfigEntryData(
                    password=None,
                ),
            ),
            errors=errors,
        )


class YoinOptionsFlow(YoinCommonFlow, OptionsFlow):
    """Handle Yoin options."""

    general_settings: dict

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize Yoin options flow."""
        self.config_entry = config_entry
        super().__init__(initial_data=config_entry.data)  # type: ignore[arg-type]

    @callback
    def finish_flow(self) -> FlowResult:
        """Update the ConfigEntry and finish the flow."""
        new_data = DEFAULT_ENTRY_DATA | self.initial_data | self.new_entry_data
        self.hass.config_entries.async_update_entry(
            self.config_entry,
            data=new_data,
            title=self.new_title or UNDEFINED,
        )
        self.hass.async_create_task(
            self.hass.config_entries.async_reload(self.config_entry.entry_id)
        )
        return self.async_create_entry(title="", data={})

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage Yoin options."""
        return self.async_show_menu(
            step_id="init",
            menu_options=[
                "username_password",
                "scan_interval",
            ],
        )


class YoinConfigFlow(YoinCommonFlow, ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Yoin."""

    VERSION = 3

    def __init__(self) -> None:
        """Initialize Yoin Config Flow."""
        super().__init__(initial_data=DEFAULT_ENTRY_DATA)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> YoinOptionsFlow:
        """Get the options flow for this handler."""
        return YoinOptionsFlow(config_entry)

    @callback
    def finish_flow(self) -> FlowResult:
        """Create the ConfigEntry."""
        title = self.new_title or NAME
        return self.async_create_entry(
            title=title,
            data=DEFAULT_ENTRY_DATA | self.new_entry_data,
        )

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        """Handle a flow initialized by the user."""
        return await self.async_step_connection_init()

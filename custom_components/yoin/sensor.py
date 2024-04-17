"""Yoin sensor platform."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CURRENCY_EURO, PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import YoinDataUpdateCoordinator
from .const import DOMAIN
from .entity import YoinEntity
from .models import YoinItem

_LOGGER = logging.getLogger(__name__)


@dataclass
class YoinSensorDescription(SensorEntityDescription):
    """Class to describe a Yoin sensor."""

    name_suffix: str | None = None
    available_fn: Callable | None = None
    value_fn: Callable | None = None
    attributes_fn: Callable | None = None
    unique_id_fn: Callable | None = None
    translation_key: str | None = None


SENSOR_DESCRIPTIONS: list[SensorEntityDescription] = [
    YoinSensorDescription(key="profile", icon="mdi:face-man"),
    YoinSensorDescription(key="subscription", icon="mdi:sim"),
    YoinSensorDescription(
        key="euro",
        icon="mdi:currency-eur",
        device_class=SensorDeviceClass.MONETARY,
        native_unit_of_measurement=CURRENCY_EURO,
        suggested_display_precision=0,
    ),
    YoinSensorDescription(
        key="usage_percentage_data",
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:signal-4g",
        suggested_display_precision=0,
    ),
    YoinSensorDescription(
        key="usage_percentage_voice_sms",
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:phone",
        suggested_display_precision=0,
    ),
    YoinSensorDescription(
        key="data",
        icon="mdi:signal-4g",
    ),
    YoinSensorDescription(
        key="voice_sms",
        icon="mdi:phone",
    ),
    YoinSensorDescription(
        key="remaining_days",
        icon="mdi:calendar-end-outline",
    ),
    YoinSensorDescription(
        key="coins",
        icon="mdi:hand-coin",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    YoinSensorDescription(
        key="coins_pending",
        icon="mdi:timer-sand",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    YoinSensorDescription(
        key="coins_proposition",
        icon="mdi:offer",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    YoinSensorDescription(key="sim", icon="mdi:sim"),
    YoinSensorDescription(key="address", icon="mdi:home"),
    YoinSensorDescription(key="voice", icon="mdi:phone"),
    YoinSensorDescription(key="sms", icon="mdi:message-processing"),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Yoin sensors."""
    _LOGGER.debug("[sensor|async_setup_entry|async_add_entities|start]")
    coordinator: YoinDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][
        "coordinator"
    ]
    # _LOGGER.debug(f"[sensor|async_setup_entry|async_add_entities|SUPPORTED_KEYS] {SUPPORTED_KEYS}")

    entities: list[YoinSensor] = []

    SUPPORTED_KEYS = {
        description.key: description for description in SENSOR_DESCRIPTIONS
    }
    if coordinator.data is not None:
        for _, item in coordinator.data.items():
            if description := SUPPORTED_KEYS.get(item.type):
                if item.native_unit_of_measurement is not None:
                    native_unit_of_measurement = item.native_unit_of_measurement
                else:
                    native_unit_of_measurement = (
                        description.native_unit_of_measurement
                    )
                sensor_description = YoinSensorDescription(
                    key=str(item.key),
                    name=item.name,
                    value_fn=description.value_fn,
                    native_unit_of_measurement=native_unit_of_measurement,
                    icon=description.icon,
                )

                _LOGGER.debug(f"[sensor|async_setup_entry|adding] {item.name}")
                entities.append(
                    YoinSensor(
                        coordinator=coordinator,
                        description=sensor_description,
                        item=item,
                    )
                )
            else:
                _LOGGER.debug(
                    f"[sensor|async_setup_entry|no support type found] {item.name}, type: {item.type}, keys: {SUPPORTED_KEYS.get(item.type)}",
                    True,
                )
    async_add_entities(entities)


class YoinSensor(YoinEntity, SensorEntity):
    """Representation of a Yoin sensor."""

    entity_description: YoinSensorDescription

    def __init__(
        self,
        coordinator: YoinDataUpdateCoordinator,
        description: EntityDescription,
        item: YoinItem,
    ) -> None:
        """Set entity ID."""
        super().__init__(coordinator, description, item)
        self.entity_id = f"sensor.{DOMAIN}_{self.item.key}"

    @property
    def native_value(self) -> str:
        """Return the status of the sensor."""
        state = self.item.state

        if self.entity_description.value_fn:
            return self.entity_description.value_fn(state)

        return state

    @property
    def extra_state_attributes(self):
        """Return attributes for sensor."""
        if not self.coordinator.data:
            return {}
        attributes = {
            "last_synced": self.last_synced,
        }
        if len(self.item.extra_attributes) > 0:
            for attr in self.item.extra_attributes:
                attributes[attr] = self.item.extra_attributes[attr]
        return attributes

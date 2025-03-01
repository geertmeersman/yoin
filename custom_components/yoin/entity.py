"""Base Yoin entity."""

from __future__ import annotations

from datetime import datetime
import logging

from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo, EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import YoinDataUpdateCoordinator
from .const import ATTRIBUTION, DOMAIN, NAME, VERSION, WEBSITE
from .models import YoinItem
from .utils import sensor_name

_LOGGER = logging.getLogger(__name__)


class YoinEntity(CoordinatorEntity[YoinDataUpdateCoordinator]):
    """Base Yoin entity."""

    _attr_attribution = ATTRIBUTION

    def __init__(
        self,
        coordinator: YoinDataUpdateCoordinator,
        description: EntityDescription,
        item: YoinItem,
    ) -> None:
        """Initialize Yoin entities."""
        super().__init__(coordinator)
        self.entity_description = description
        self._item = item
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, str(self.item.device_key))},
            name=f"{NAME} {self.item.device_name}",
            manufacturer=NAME,
            configuration_url=WEBSITE.replace("yoin.be", f"yoin.{item.country}"),
            entry_type=DeviceEntryType.SERVICE,
            model=self.item.device_model,
            sw_version=VERSION,
        )
        """
        extra attributes!
        """
        self._attr_unique_id = f"{DOMAIN}_{self.item.key}"
        self._key = self.item.key
        self.client = coordinator.client
        self.last_synced = datetime.now()
        self._attr_name = sensor_name(self.item.name)
        if self.entity_description.name_suffix is not None:
            self._attr_name += f" {self.entity_description.name_suffix}"
        self._item = item
        _LOGGER.debug(f"[YoinEntity|init] {self._key}")

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if len(self.coordinator.data):
            for item in self.coordinator.data:
                item = self.coordinator.data[item]
                if self._key == item.key:
                    self.last_synced = datetime.now()
                    self._item = item
                    self.async_write_ha_state()
                    return
        _LOGGER.debug(
            f"[YoinEntity|_handle_coordinator_update] {self._attr_unique_id}: async_write_ha_state ignored since API fetch failed or not found",
            True,
        )

    @property
    def item(self) -> YoinItem:
        """Return the product for this entity."""
        return self._item

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self._item is not None

    async def async_update(self) -> None:
        """Update the entity.  Only used by the generic entity update service."""
        return

"""Models used by Yoin."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypedDict


class YoinConfigEntryData(TypedDict):
    """Config entry for the Yoin integration."""

    username: str | None
    password: str | None
    scan_interval: int | None


@dataclass
class YoinEnvironment:
    """Class to describe a Yoin environment."""

    api_endpoint: str
    base_url: str


@dataclass
class YoinItem:
    """Yoin item model."""

    name: str = ""
    key: str = ""
    type: str = ""
    state: str = ""
    country: str = ""
    device_key: str = ""
    device_name: str = ""
    device_model: str = ""
    data: dict = field(default_factory=dict)
    extra_attributes: dict = field(default_factory=dict)
    native_unit_of_measurement: str = None

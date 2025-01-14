"""Constants used by Yoin."""

import json
from pathlib import Path
from typing import Final

from homeassistant.const import Platform

from .models import YoinEnvironment

PLATFORMS: Final = [Platform.SENSOR, Platform.BINARY_SENSOR]

ATTRIBUTION: Final = "Data provided by Yoin"

DEFAULT_YOIN_ENVIRONMENT = YoinEnvironment(
    api_endpoint="https://my.yoin.be/prov/MyYoufone/MyYOufone.Wcf/v2.0/Service.svc/json",
    base_url="https://my.yoin.be",
)

BASE_HEADERS = {
    "Content-Type": "application/json",
}

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"

COORDINATOR_MIN_UPDATE_INTERVAL = 2  # hours
WEBSITE = "https://my.yoin.be/"

manifestfile = Path(__file__).parent / "manifest.json"
with open(manifestfile) as json_file:
    manifest_data = json.load(json_file)

DOMAIN = manifest_data.get("domain")
NAME = manifest_data.get("name")
VERSION = manifest_data.get("version")
ISSUEURL = manifest_data.get("issue_tracker")
STARTUP = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom component
If you have any issues with this you need to open an issue here:
{ISSUEURL}
-------------------------------------------------------------------
"""

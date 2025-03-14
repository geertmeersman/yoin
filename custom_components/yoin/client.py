"""Yoin API Client."""

from __future__ import annotations

from calendar import monthrange
import copy
from datetime import datetime
import json
import logging
import time

import httpx

from .const import BASE_HEADERS, DEFAULT_YOIN_ENVIRONMENT
from .exceptions import BadCredentialsException, YoinServiceException
from .models import YoinEnvironment, YoinItem
from .utils import format_entity_name, mask_fields, str_to_float

_LOGGER = logging.getLogger(__name__)


class YoinClient:
    """Yoin client."""

    environment: YoinEnvironment

    def __init__(
        self,
        username: str | None = None,
        password: str | None = None,
        country: str | None = None,
        headers: dict | None = BASE_HEADERS,
        environment: YoinEnvironment = DEFAULT_YOIN_ENVIRONMENT,
    ) -> None:
        """Initialize YoinClient."""
        self.username = username
        self.password = password
        self.environment = environment
        self.country = country
        self._headers = headers
        self.securitykey = None
        self.user_details = None
        self.request_error = {}

    def request(
        self,
        url,
        caller="Not set",
        data=None,
        expected="200",
        log=False,
    ) -> dict:
        """Send a request to Yoin."""
        headers = self._headers
        headers.update(
            {
                "Referer": "https://my.yoin.be/login",
                "Origin": "https://my.yoin.be",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
            }
        )
        if self.securitykey is not None:
            headers.update(
                {
                    "securitykey": self.securitykey,
                }
            )

        client = httpx.Client(http2=True)

        # sleep 5 seconds, trying to avoid IP blacklisting
        time.sleep(5)

        if data is None:
            _LOGGER.debug(f"{caller} Calling GET {url}")
            response = client.get(url, headers=headers)
        else:
            data_copy = copy.deepcopy(data)
            json_data = json.loads(data_copy)
            mask_fields(json_data, ["Password"])
            _LOGGER.debug(f"{caller} Calling POST {url} with {json_data}")
            response = client.post(url, data=data, headers=headers)
        _LOGGER.debug(
            f"{caller} http status code = {response.status_code} (expecting {expected})"
        )
        _LOGGER.debug(f"{caller} Response:\n{response.text}")
        if expected is not None and response.status_code != expected:
            raise YoinServiceException(
                f"[{caller}] Expecting HTTP {expected} | Response HTTP {response.status_code}, Response: {response.text}, Url: {response.url}"
            )
        return response

    def login(self) -> dict:
        """Start a new Yoin session with a user & password."""
        """Login process"""
        if self.username is None or self.password is None:
            raise BadCredentialsException("Username or Password cannot be empty")
        response = self.request(
            f"{self.environment.api_endpoint}/login",
            "[YoinClient|login|authenticate]",
            '{"request": {"Login": "'
            + self.username
            + '", "Password": "'
            + self.password
            + '"}}',
            None,
        )
        result = response.json()
        if result.get("ResultCode") != 0:
            raise BadCredentialsException(response.text)
        self.user_details = result.get("Object")
        self.securitykey = response.headers.get("securitykey")
        return True

    def fetch_data(self):
        """Fetch Yoin data."""
        data = {}

        now = datetime.now()
        if not self.login():
            return False

        customer = self.user_details.get("Customer")
        customers = self.user_details.get("Customers")
        user_id = customer.get("Id")
        personal_info = self.personal_info(user_id)
        if not personal_info:
            return data

        device_key = format_entity_name(f"{user_id} user")
        device_name = f"{customer.get('FirstName')} {customer.get('LastName')} Account"
        device_model = "Useraccount"
        key = format_entity_name(f"{user_id} user")
        data[key] = YoinItem(
            country=self.country,
            name=device_name,
            key=key,
            type="profile",
            device_key=device_key,
            device_name=device_name,
            device_model=device_model,
            state=user_id,
            extra_attributes=personal_info,
        )
        """
        device_key = format_entity_name(f"{user_id} youcoins")
        device_name = f"{customer.get('FirstName')} {customer.get('LastName')} Youcoins"
        device_model = "Youcoins"

        youcoins_token = self.youcoins_token(user_id)
        if youcoins_token:
            balance = self.youcoins_balance(youcoins_token)
            if balance is not False:
                key = format_entity_name(f"{user_id} youcoins")
                data[key] = YoinItem(
                    country=self.country,
                    name="Youcoins",
                    key=key,
                    type="coins",
                    device_key=device_key,
                    device_name=device_name,
                    device_model=device_model,
                    state=balance.get("Current"),
                    extra_attributes=balance,
                )
                key = format_entity_name(f"{user_id} youcoins pending")
                data[key] = YoinItem(
                    country=self.country,
                    name="Youcoins pending",
                    key=key,
                    type="coins_pending",
                    device_key=device_key,
                    device_name=device_name,
                    device_model=device_model,
                    state=balance.get("Pending"),
                    extra_attributes=balance,
                )
                propositions = self.youcoins_propositions(youcoins_token)
                if propositions:
                    for proposition in propositions:
                        key = format_entity_name(
                            f"{user_id} youcoins proposition {proposition.get('Id')}"
                        )
                        data[key] = YoinItem(
                            country=self.country,
                            name=f"{proposition.get('DisplayName')}",
                            key=key,
                            type="coins_proposition",
                            device_key=device_key,
                            device_name=device_name,
                            device_model=device_model,
                            state=str_to_float(proposition.get("Price")),
                            extra_attributes=proposition,
                        )

        device_key = format_entity_name(f"{user_id} invoices")
        device_name = f"{customer.get('FirstName')} {customer.get('LastName')} Invoices"
        device_model = "Invoices"

        invoices = self.invoices(user_id)
        if not invoices:
            return data
        for invoice in invoices.get("Invoices"):
            key = format_entity_name(
                f"{user_id} invoice {invoice.get('InvoiceNumber')}"
            )
            data[key] = YoinItem(
                country=self.country,
                name=f"{invoice.get('InvoiceDateFormatted')} - {invoice.get('Status')}",
                key=key,
                type="euro",
                device_key=device_key,
                device_name=device_name,
                device_model=device_model,
                state=str_to_float(
                    invoice.get("InvoiceAmountFormatted").replace("€ ", "")
                ),
                extra_attributes=invoice,
            )
        """
        for customer_a in customers:
            msisdn = customer_a.get("Msisdn")
            if msisdn is None:
                continue
            msisdn_info = self.msisdn_info(msisdn)
            if not msisdn_info:
                return data
            abonnement_msisdn_info = self.abonnement_msisdn_info(msisdn)
            if not abonnement_msisdn_info:
                return data
            device_key = format_entity_name(f"msisdn {msisdn}")
            device_name = (
                f"{customer.get('FirstName')} {customer.get('LastName')} {msisdn}"
            )
            device_model = "Msisdn"

            period_percentage_completed = None
            for property in abonnement_msisdn_info + msisdn_info:
                properties = {}
                for property_list in property.get("Properties"):
                    properties.update(
                        {property_list.get("Key"): property_list.get("Value")}
                    )
                if property.get("SectionId") == 1:
                    key = format_entity_name(f"{msisdn} data")
                    if (
                        "_isUnlimited" in properties
                        and properties.get("_isUnlimited") == "1"
                    ):
                        state = 0
                    else:
                        state = round(
                            100
                            * str_to_float(properties.get("UsedAmount"))
                            / str_to_float(properties.get("BundleDurationWithUnits")),
                            1,
                        )

                    data[key] = YoinItem(
                        country=self.country,
                        name="Data",
                        key=key,
                        type="usage_percentage_data",
                        device_key=device_key,
                        device_name=device_name,
                        device_model=device_model,
                        state=state,
                        extra_attributes=properties,
                    )
                elif property.get("SectionId") == 2:
                    key = format_entity_name(f"{msisdn} voice sms")
                    if (
                        "_isUnlimited" in properties
                        and properties.get("_isUnlimited") == "1"
                    ):
                        state = 0
                    else:
                        state = round(
                            100
                            * str_to_float(properties.get("UsedAmount"))
                            / str_to_float(properties.get("BundleDurationWithUnits")),
                            1,
                        )
                    data[key] = YoinItem(
                        country=self.country,
                        name="Voice Sms",
                        key=key,
                        type="usage_percentage_voice_sms",
                        device_key=device_key,
                        device_name=device_name,
                        device_model=device_model,
                        state=state,
                        extra_attributes=properties,
                    )
                elif property.get("SectionId") == 3:
                    key = format_entity_name(f"{msisdn} remaining days")
                    days_in_month = monthrange(now.year, now.month)[1]
                    first_of_month = datetime(now.year, now.month, 1)
                    seconds_in_month = days_in_month * 86400
                    seconds_completed = (now - first_of_month).total_seconds()
                    period_percentage_completed = round(
                        100 * seconds_completed / seconds_in_month, 1
                    )
                    period_percentage_remaining = 100 - period_percentage_completed
                    _LOGGER.debug(f"days_in_month: {days_in_month}")
                    data[key] = YoinItem(
                        country=self.country,
                        name="Remaining days",
                        key=key,
                        type="remaining_days",
                        device_key=device_key,
                        device_name=device_name,
                        device_model=device_model,
                        state=properties.get("NumberOfRemainingDays"),
                        extra_attributes=properties
                        | {
                            "period_percentage_completed": period_percentage_completed,
                            "period_percentage_remaining": period_percentage_remaining,
                            "days_in_period": days_in_month,
                        },
                    )
                elif property.get("SectionId") == 21:
                    key = format_entity_name(f"{msisdn} abonnement type")
                    data[key] = YoinItem(
                        country=self.country,
                        name=properties.get("AbonnementType").replace("<br/>", " - "),
                        key=key,
                        type="euro",
                        device_key=device_key,
                        device_name=device_name,
                        device_model=device_model,
                        state=str_to_float(properties.get("Price")),
                        extra_attributes=properties,
                    )
                elif property.get("SectionId") == 23:
                    key = format_entity_name(f"{msisdn} sim info")
                    data[key] = YoinItem(
                        country=self.country,
                        name=properties.get("Msisdn"),
                        key=key,
                        type="sim",
                        device_key=device_key,
                        device_name=device_name,
                        device_model=device_model,
                        state=properties.get("MsisdnStatus"),
                        extra_attributes=properties,
                    )
                elif property.get("SectionId") == 24:
                    key = format_entity_name(f"{msisdn} data subscription")
                    data[key] = YoinItem(
                        country=self.country,
                        name="Data subscription",
                        key=key,
                        type="data",
                        device_key=device_key,
                        device_name=device_name,
                        device_model=device_model,
                        state=properties.get("DataSubscription"),
                    )
                elif property.get("SectionId") == 26:
                    key = format_entity_name(f"{msisdn} voice sms subscription")
                    data[key] = YoinItem(
                        country=self.country,
                        name="Voice Sms subscription",
                        key=key,
                        type="voice_sms",
                        device_key=device_key,
                        device_name=device_name,
                        device_model=device_model,
                        state=properties.get("VoiceSmsSubscription"),
                    )
            if period_percentage_completed is not None:
                for _, item in data.items():
                    item.extra_attributes["period_percentage_completed"] = (
                        period_percentage_completed
                    )
        return data

    def personal_info(self, customer_id):
        """Get personal info."""
        response = self.request(
            f"{self.environment.api_endpoint}/GetCustomerPersonalInfo",
            "personal_info",
            '{"request":{"CustomerId":' + str(customer_id) + "}}",
            200,
        )
        result = response.json()
        if result.get("ResultCode") != 0:
            return False
        return result.get("Object")

    def msisdn_info(self, msisdn):
        """Get personal info."""
        response = self.request(
            f"{self.environment.api_endpoint}/GetOverviewMsisdnInfo",
            "msisdn_info",
            '{"request":{"Msisdn":' + str(msisdn) + "}}",
            200,
        )
        result = response.json()
        if result.get("ResultCode") != 0:
            return False
        return result.get("Object")

    def abonnement_msisdn_info(self, msisdn):
        """Get personal info."""
        response = self.request(
            f"{self.environment.api_endpoint}/GetAbonnementMsisdnInfo",
            "abonnement_msisdn_info",
            '{"request":{"Msisdn":' + str(msisdn) + "}}",
            200,
        )
        result = response.json()
        if result.get("ResultCode") != 0:
            return False
        return result.get("Object")

    def invoices(self, customer_id):
        """Get personal info."""
        response = self.request(
            f"{self.environment.api_endpoint}/GetInvoicesByCustomerId",
            "invoices",
            '{"request":{"CustomerId":' + str(customer_id) + "}}",
            200,
        )
        result = response.json()
        if result.get("ResultCode") != 0:
            return False
        return result.get("Object")

    def youcoins_token(self, customer_id):
        """Get YouCoins Token."""
        response = self.request(
            f"{self.environment.api_endpoint}/GetYoucoinsToken",
            "youcoins",
            '{"request":{"CustomerId":' + str(customer_id) + "}}",
            200,
        )
        result = response.json()
        if result.get("ResultCode") != 0:
            return False
        return result.get("Object")

    def youcoins_balance(self, token):
        """Get Youcoins balance."""
        response = self.request(
            f"{self.environment.base_url}/prov/PartnerAPI/CustomerService.svc/customer?data={token}&connectId=1",
            "youcoins",
            None,
            None,
        )
        if response.status_code != 200:
            return False
        result = response.json()
        if result.get("Balance") is not None:
            return result.get("Balance")
        return False

    def youcoins_propositions(self, token):
        """Get Youcoins Propositions."""
        response = self.request(
            f"{self.environment.base_url}/prov/PartnerAPI/CustomerService.svc/propositions?data={token}&connectId=1",
            "youcoins",
            None,
            200,
        )
        result = response.json()
        if len(result):
            return result
        return False

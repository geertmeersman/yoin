<img src="https://github.com/geertmeersman/yoin/raw/main/images/brand/logo.png"
     alt="Yoin"
     align="right"
     style="width: 200px;margin-right: 10px;" />

# Yoin for Home Assistant

A Home Assistant integration allowing to monitor your Yoin usage

```text
In order to avoid IP blacklisting / DDOS identification, the update interval is set to a minimum of 2 hours (you can increase it in the configuration).
When Home Assistant restarts, it will fetch the data from the local storage and it will update the sensors after the configured interval.
When adding a hub of the integration, it might take 1 minute to complete the addition, due to a 5 seconds interval set between each API call to Yoin.
```

### Features

- 📱 Mobile data sensors
- 📞 Voice & sms sensors
- 💲 Youcoins balance
- 📈 Invoice sensors
- 👱 User account information

---

<!-- [START BADGES] -->
<!-- Please keep comment here to allow auto update -->

[![maintainer](https://img.shields.io/badge/maintainer-Geert%20Meersman-green?style=for-the-badge&logo=github)](https://github.com/geertmeersman)
[![buyme_coffee](https://img.shields.io/badge/Buy%20me%20an%20Omer-donate-yellow?style=for-the-badge&logo=buymeacoffee)](https://www.buymeacoffee.com/geertmeersman)
[![discord](https://img.shields.io/discord/1094977038269546576?style=for-the-badge&logo=discord)](https://discord.gg/JpjHptEN2D)

[![MIT License](https://img.shields.io/github/license/geertmeersman/yoin?style=flat-square)](https://github.com/geertmeersman/yoin/blob/master/LICENSE)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=flat-square)](https://github.com/hacs/integration)

[![Open your Home Assistant instance and open the repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg?style=flat-square)](https://my.home-assistant.io/redirect/hacs_repository/?owner=geertmeersman&repository=yoin&category=integration)

[![GitHub issues](https://img.shields.io/github/issues/geertmeersman/yoin)](https://github.com/geertmeersman/yoin/issues)
[![Average time to resolve an issue](http://isitmaintained.com/badge/resolution/geertmeersman/yoin.svg)](http://isitmaintained.com/project/geertmeersman/yoin)
[![Percentage of issues still open](http://isitmaintained.com/badge/open/geertmeersman/yoin.svg)](http://isitmaintained.com/project/geertmeersman/yoin)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg)](https://github.com/geertmeersman/yoin/pulls)

[![Hacs and Hassfest validation](https://github.com/geertmeersman/yoin/actions/workflows/validate.yml/badge.svg)](https://github.com/geertmeersman/yoin/actions/workflows/validate.yml)
[![Python](https://img.shields.io/badge/Python-FFD43B?logo=python)](https://github.com/geertmeersman/yoin/search?l=python)

[![manifest version](https://img.shields.io/github/manifest-json/v/geertmeersman/yoin/master?filename=custom_components%2Fyoin%2Fmanifest.json)](https://github.com/geertmeersman/yoin)
[![github release](https://img.shields.io/github/v/release/geertmeersman/yoin?logo=github)](https://github.com/geertmeersman/yoin/releases)
[![github release date](https://img.shields.io/github/release-date/geertmeersman/yoin)](https://github.com/geertmeersman/yoin/releases)
[![github last-commit](https://img.shields.io/github/last-commit/geertmeersman/yoin)](https://github.com/geertmeersman/yoin/commits)
[![github contributors](https://img.shields.io/github/contributors/geertmeersman/yoin)](https://github.com/geertmeersman/yoin/graphs/contributors)
[![github commit activity](https://img.shields.io/github/commit-activity/y/geertmeersman/yoin?logo=github)](https://github.com/geertmeersman/yoin/commits/main)

<!-- [END BADGES] -->

## Table of Contents

- [Yoin for Home Assistant](#yoin-for-home-assistant)
    - [Features](#features)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
    - [Using HACS (recommended)](#using-hacs-recommended)
    - [Manual](#manual)
  - [Contributions are welcome](#contributions-are-welcome)
  - [Troubleshooting](#troubleshooting)
    - [Enable debug logging](#enable-debug-logging)
    - [Disable debug logging and download logs](#disable-debug-logging-and-download-logs)
  - [Lovelace examples](#lovelace-examples)
    - [Voice, Sms \& Data overview](#voice-sms--data-overview)
    - [Subscription details + gauge](#subscription-details--gauge)
  - [Screenshots](#screenshots)
    - [Msisdn info](#msisdn-info)
    - [Useraccount](#useraccount)
    - [Youcoins](#youcoins)
    - [Invoices](#invoices)
    - [Config flow](#config-flow)
  - [Code origin](#code-origin)

## Installation

### Using [HACS](https://hacs.xyz/) (recommended)

**Click on this button:**

[![Open your Home Assistant instance and open the repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg?style=flat-square)](https://my.home-assistant.io/redirect/hacs_repository/?owner=geertmeersman&repository=yoin&category=integration)

**or follow these steps:**

1. Simply search for `Yoin` in HACS and install it easily.
2. Restart Home Assistant
3. Add the 'Yoin' integration via HA Settings > 'Devices and Services' > 'Integrations'
4. Provide your Yoin username and password

### Manual

1. Copy the `custom_components/yoin` directory of this repository as `config/custom_components/yoin` in your Home Assistant instalation.
2. Restart Home Assistant
3. Add the 'Yoin' integration via HA Settings > 'Devices and Services' > 'Integrations'
4. Provide your Yoin username and password

This integration will set up the following platforms.

| Platform  | Description                                           |
| --------- | ----------------------------------------------------- |
| `yoin` | Home Assistant component for Yoin services |

## Contributions are welcome

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

## Troubleshooting

### Enable debug logging

To enable debug logging, go to Settings -> Devices & Services and then click the triple dots for the Yoin integration and click Enable Debug Logging.

![enable-debug-logging](https://raw.githubusercontent.com/geertmeersman/yoin/main/images/screenshots/enable-debug-logging.gif)

### Disable debug logging and download logs

Once you enable debug logging, you ideally need to make the error happen. Run your automation, change up your device or whatever was giving you an error and then come back and disable Debug Logging. Disabling debug logging is the same as enabling, but now you will see Disable Debug Logging. After you disable debug logging, it will automatically prompt you to download your log file. Please provide this logfile.

![disable-debug-logging](https://raw.githubusercontent.com/geertmeersman/yoin/main/images/screenshots/disable-debug-logging.gif)

## Lovelace examples

### Voice, Sms & Data overview

![Lovelace overview.](https://github.com/geertmeersman/yoin/raw/main/images/screenshots/lovelace_overview.png)

<details><summary>Show markdown code</summary>

**Replace &lt;mobile_number&gt; by your mobile number**

```yaml
type: custom:button-card
variables:
  var_call: '[[[ return states["sensor.yoin_<mobile_number>_voice_sms"].attributes;]]]'
  var_internet: '[[[ return states["sensor.yoin_<mobile_number>_data"].attributes;]]]'
  var_remaining: >-
    [[[ return
    states["sensor.yoin_<mobile_number>_remaining_days"].attributes;]]]
styles:
  grid:
    - grid-template-areas: "'balance' 'product'"
    - grid-template-rows: 1fr
  card:
    - padding: 0px
custom_fields:
  balance:
    card:
      type: custom:button-card
      styles:
        grid:
          - grid-template-areas: "'minuten data sms'"
          - grid-template-columns: 1fr 1fr 1fr
        card:
          - padding: 0px
      custom_fields:
        minuten:
          card:
            show_name: true
            show_icon: false
            name: '[[[ return "belminuten" ]]]'
            type: custom:button-card
            tap_action:
              action: navigate
              navigation_path: /lovelace/abonnementen
            custom_fields:
              totaal: |
                [[[
                  return 'van de '+variables.var_call.BundleDurationWithUnits+' gebruikt'
                ]]]
              gebruikt: |
                [[[
                  return variables.var_call.UsedAmount+''
                ]]]
            styles:
              custom_fields:
                gebruikt:
                  - font-size: 20px
                totaal:
                  - font-size: 10px
              grid:
                - grid-template-areas: '"gebruikt" "n" "totaal"'
              label:
                - font-size: 20px
              card:
                - background: >-
                    [[[ return
                    variables.var_call.used_percentage>90?"red":"#398087" ]]]
                - background-size: cover
                - background-position: center
                - font-weight: bold
                - font-family: Helvetica
                - font-size: 13px
        data:
          card:
            show_name: true
            show_icon: false
            name: '[[[ return "mobiele data" ]]]'
            type: custom:button-card
            tap_action:
              action: navigate
              navigation_path: /lovelace/abonnementen
            custom_fields:
              totaal: |
                [[[
                  return 'van de '+variables.var_internet.BundleDurationWithUnits+' gebruikt'
                ]]]
              resterend: |
                [[[
                  return Math.ceil(variables.var_internet.Percentage)+'%'
                ]]]
            styles:
              custom_fields:
                resterend:
                  - font-size: 20px
                totaal:
                  - font-size: 10px
              grid:
                - grid-template-areas: '"resterend" "n" "totaal"'
              label:
                - font-size: 20px
              card:
                - background: >-
                    [[[ return
                    variables.var_internet.used_percentage>90?"red":"#00a5db"
                    ]]]
                - background-size: cover
                - background-position: center
                - font-weight: bold
                - font-family: Helvetica
                - font-size: 13px
        sms:
          card:
            show_name: true
            show_icon: false
            name: '[[[ return "sms''en" ]]]'
            type: custom:button-card
            tap_action:
              action: navigate
              navigation_path: /lovelace/abonnementen
            custom_fields:
              totaal: |
                [[[
                  return 'van de '+variables.var_call.BundleDurationWithUnits.replace(' Min', '')+' gebruikt'
                ]]]
              gebruikt: |
                [[[
                  return variables.var_call.UsedAmount+''
                ]]]
            styles:
              custom_fields:
                gebruikt:
                  - font-size: 20px
                totaal:
                  - font-size: 10px
              grid:
                - grid-template-areas: '"gebruikt" "n" "totaal"'
              label:
                - font-size: 20px
              card:
                - background: >-
                    [[[ return variables.var_call.Percentage>90?"red":"#8d7fdb"
                    ]]]
                - background-size: cover
                - background-position: center
                - font-weight: bold
                - font-family: Helvetica
                - font-size: 13px
  product:
    card:
      type: markdown
      content: >
        ###### Nog
        {{state_attr('sensor.yoin_<mobile_number>_remaining_days','NumberOfRemainingDays')|int}}
        dagen | Vervalt op
        {{state_attr('sensor.yoin_<mobile_number>_remaining_days','StartDate')}}
```

</details>

### Subscription details + gauge

![Lovelace Usage Gauge](https://github.com/geertmeersman/yoin/raw/main/images/screenshots/lovelace_usage_gauge.png)

<details><summary>Show markdown code</summary>

**Replace &lt;mobile_number&gt; by your mobile number**

```yaml
type: vertical-stack
cards:
  - type: markdown
    content: >
      # Username : {{ states["sensor.yoin_<mobile_number>_data"].state|int}}%

      Product: {{
      states["sensor.yoin_<mobile_number>_abonnement_type"].attributes.friendly_name
      }}

      Data verbruikt: {{
      states["sensor.yoin_<mobile_number>_data"].attributes.UsedAmount}}/{{
      states["sensor.yoin_<mobile_number>_data"].attributes.BundleDurationWithUnits}}

      Voice/sms verbruikt: {{
      states["sensor.yoin_<mobile_number>_voice_sms"].attributes.UsedAmount}}/{{
      states["sensor.yoin_<mobile_number>_voice_sms"].attributes.BundleDurationWithUnits}}

      Nog {{ states["sensor.yoin_<mobile_number>_remaining_days"].state }} dagen
      resterend in de huidige periode

      Laatste update:
      {{state_attr('sensor.yoin_<mobile_number>_sim_info','last_synced') |
      as_timestamp | timestamp_custom("%d-%m-%Y %H:%M")}}
    style: |
      ha-card {
        background: {% if(states.sensor.yoin_<mobile_number>_data.state|int > 90) %}red{% elif(states.sensor.yoin_<mobile_number>_data.state|int > 80) %}orange{% else %}green{%- endif %};
        background-image: url(https://github.com/geertmeersman/yoin/raw/main/images/brand/logo_text.png);
        background-size: cover;
        background-position: center;
        font-weight: bold;
        font-family: Helvetica;
        font-size: 13px;
      }
  - type: custom:dual-gauge-card
    title: Username
    min: 0
    max: 100
    shadeInner: true
    cardwidth: 350
    outer:
      entity: sensor.yoin_<mobile_number>_data
      label: gebruikt
      min: 0
      max: 100
      unit: "%"
      colors:
        - color: var(--label-badge-green)
          value: 0
        - color: var(--label-badge-yellow)
          value: 60
        - color: var(--label-badge-red)
          value: 80
    inner:
      entity: sensor.yoin_<mobile_number>_remaining_days
      label: period
      attribute: period_percentage_completed
      min: 0
      max: 100
      unit: "%"
```

</details>

## Screenshots

### Msisdn info

![Msisdn](https://github.com/geertmeersman/yoin/raw/main/images/screenshots/msisdn.png)

### Useraccount

![Useraccount](https://github.com/geertmeersman/yoin/raw/main/images/screenshots/useraccount.png)

### Youcoins

![Youcoins](https://github.com/geertmeersman/yoin/raw/main/images/screenshots/youcoins.png)

### Invoices

![Invoices](https://github.com/geertmeersman/yoin/raw/main/images/screenshots/invoices.png)

### Config flow

![Config flow](https://github.com/geertmeersman/yoin/raw/main/images/screenshots/config_flow.png)

![Config options](https://github.com/geertmeersman/yoin/raw/main/images/screenshots/config_options.png)

## Code origin

The code of this Home Assistant integration has been written by analysing the calls done by the Yoin website.

I have no link with Yoin

![hacs_badge](https://img.shields.io/badge/hacs-custom-orange.svg) [![BuyMeCoffee][buymecoffeebedge]][buymecoffee]

# Udemy Free Courses Sensor Component

![logo.jpg](logo.png)

Custom component for information about free courses available on udemy.com for home assistant

# Installation

## HACS

- Have [HACS](https://hacs.xyz/) installed, this will allow you to easily update.

- Add https://github.com/hudsonbrendon/sensor.udemy as a custom repository with Type: Integration
- Click Install under "Udemy.com" integration.
- Restart Home-Assistant.

## Manual

- Copy directory custom_components/udemy to your <config dir>/custom_components directory.
- Configure.
- Restart Home-Assistant.

# Configuration

Go to your account's [API configuration page](https://www.udemy.com/instructor/account/api/), and manage your client_id and client_secret.

```yaml
- platform: udemy
  client_id: your-client-id
  client_secret: your-client-secret
  category: your-category
```

# Integration with list card

you can display the list of courses with a [list card](https://github.com/iantrich/list-card), install the in your home asssistant, and in a manual card, add the following configuration:


```yaml
type: 'custom:list-card'
entity: sensor.udemy_free_courses
title: Udemy free courses
feed_attribute: courses
row_limit: 10
columns:
  - title: ''
    type: image
    add_link: url
    field: image
  - title: Title
    field: title
    style:
      - white-space: nowrap
```

![logo.jpg](example.png)

## Category list:

- Business
- Design
- Development
- Finance & Accounting
- Health & Fitness
- IT & Software
- Lifestyle
- Marketing
- Music
- Office Productivity
- Personal Development
- Photography & Video
- Teaching & Academics
- Udemy Free Resource Center
- Vodafone

# Debugging

```yaml
logger:
  default: info
  logs:
    custom_components.udemy: debug
```

[buymecoffee]: https://www.buymeacoffee.com/hudsonbrendon
[buymecoffeebedge]: https://camo.githubusercontent.com/cd005dca0ef55d7725912ec03a936d3a7c8de5b5/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6275792532306d6525323061253230636f666665652d646f6e6174652d79656c6c6f772e737667
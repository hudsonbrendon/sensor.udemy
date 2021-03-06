"""
A platform that provides information about courses in udemy.

For more details on this component, refer to the documentation at
https://github.com/hudsonbrendon/sensor.udemy
"""
import logging

import async_timeout
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from aiohttp import BasicAuth
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.helpers.entity import Entity

CONF_CLIENT_ID = "client_id"
CONF_CLIENT_SECRET = "client_secret"
CATEGORY = "category"

ICON = "mdi:video"

BASE_URL = "https://www.udemy.com/api-2.0/courses?page=1&page_size=100&category={}&price=price-free&ordering=newest"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_CLIENT_ID): cv.string,
        vol.Required(CONF_CLIENT_SECRET): cv.string,
        vol.Required(CATEGORY): cv.string,
    }
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Setup sensor platform."""
    client_id = config["client_id"]
    client_secret = config["client_secret"]
    category = config["category"]
    session = async_create_clientsession(hass)
    name = "Udemy Free Courses"
    async_add_entities([UdemySensor(client_id, client_secret, category, name, session)], True)


class UdemySensor(Entity):
    """Udemy.com Sensor class"""

    def __init__(self, client_id, client_secret, category, name, session):
        self._state = 0
        self._client_id = client_id
        self._client_secret = client_secret
        self._category = category
        self.session = session
        self._name = name
        self._courses = []

    async def async_update(self):
        """Update sensor."""
        _LOGGER.debug("%s - Running update", self._name)
        try:
            url = BASE_URL.format(self._category)
            async with async_timeout.timeout(10, loop=self.hass.loop):
                response = await self.session.get(BASE_URL.format(self._category), auth=BasicAuth(self._client_id, self._client_secret))
                courses = await response.json()

                self._state = len(courses["results"])

                for course in courses["results"]:
                    self._courses.append(
                        dict(
                            title=course["title"],
                            url=f"https://udemy.com{course['url']}",
                            instructor=course["visible_instructors"][0]["title"],
                            image=course["image_240x135"],
                        )
                    )

        except Exception as error:
            _LOGGER.debug("%s - Could not update - %s", self._name, error)

    @property
    def name(self):
        """Name."""
        return self._name

    @property
    def state(self):
        """State."""
        return self._state

    @property
    def courses(self):
        """Courses."""
        return [i for n, i in enumerate(self._courses) if i not in self._courses[n + 1 :]]

    @property
    def icon(self):
        """Icon."""
        return ICON

    @property
    def device_state_attributes(self):
        """Attributes."""
        return {
            "name": self.name,
            "courses": self.courses,
        }

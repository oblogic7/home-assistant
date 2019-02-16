"""Support for QVR Pro NVR software by QNAP"""

import logging

import voluptuous as vol

from homeassistant.const import CONF_HOST, CONF_USERNAME, \
    CONF_PASSWORD
import homeassistant.helpers.config_validation as cv

REQUIREMENTS = ['pyqvrpro==0.42']

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'qvrpro'

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string
    })
}, extra=vol.ALLOW_EXTRA)


def setup(hass, config):
    """Set up the QVR Pro component"""
    from pyqvrpro import Client

    user = config[DOMAIN].get(CONF_USERNAME)
    password = config[DOMAIN].get(CONF_PASSWORD)
    host = config[DOMAIN].get(CONF_HOST)

    try:
        qvrpro = Client(user, password, host)
    except Exception as e:
        msg = e

    channel_resp = qvrpro.get_channel_list()

    channels = []

    for channel in channel_resp['channels']:
        channels.append(QVRChannel(**channel))

    hass.data[DOMAIN] = {
        'channels': channels,
        'client': qvrpro
    }

    return True


class QVRChannel:
    """Representation of a QVR channel"""

    def __init__(self, name, model, brand, channel_index, guid):
        self.name = name
        self._model = model
        self.brand = brand
        self._index = channel_index
        self.guid = guid


"""
For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/binary_sensor.mind/
"""
import logging

from custom_components.mind import DATA_MIND
from homeassistant.components.binary_sensor import (
    BinarySensorEntity, PLATFORM_SCHEMA)

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['mind']

SENSOR_TYPES = {
    'ignition': ['Ignition', True, 'power', 'mdi:engine-off', 'mdi:engine'],
    'doors': ['Doors', False, 'lock', 'mdi:car-door-lock', 'mdi:car-door'],
    'parking_brake': ['Parking Brake', False, 'safety', 'mdi:car-brake-parking', 'mdi:car-brake-alert'],

    'trip_registration': ['Trip Registration', True, '', 'mdi:car-info', 'mdi:car-info'],
    'stolen': ['Stolen', True, '', 'mdi:car-info', 'mdi:car-info'],
    'movement_notification': ['Movement Notification', True, '', 'mdi:car-info', 'mdi:car-info'],
    'mil_abs': ['MIL ABS', True, 'problem', 'mdi:car-brake-abs', 'mdi:car-brake-abs'],
    'mil_airbag': ['MIL Airbag', True, 'problem', 'mdi:airbag', 'mdi:airbag'],
    'mil_battery_voltage_low': ['MIL Battery Voltage Low', True, 'problem', 'mdi:car-battery', 'mdi:car-battery'],
    'mil_oil_level_check': ['MIL Oil Level Check', True, 'problem', 'mdi:oil-level', 'mdi:oil-level'],
    'mil_oil_level_high': ['MIL Oil Level High', True, 'problem', 'mdi:oil-level', 'mdi:oil-level'],
    'mil_oil_level_low': ['MIL Oil Level Low', True, 'problem', 'mdi:oil-level', 'mdi:oil-level'],
    'mil_oil_pressure_low': ['MIL Oil Pressure Low', True, 'problem', 'mdi:oil', 'mdi:oil'],
    'mil_coolant_level_low': ['MIL Coolant Level Low', True, 'problem', 'mdi:car-coolant-level', 'mdi:car-coolant-level'],
    'mil_coolant_temp_high': ['MIL Coolant Temp High', True, 'problem', 'mdi:car-coolant-level', 'mdi:car-coolant-level'],
    'mil_breaking_system': ['MIL Breaking System', True, 'problem', 'mdi:car-brake-alert', 'mdi:car-brake-alert'],
    'mil_electronic_stability_program': ['MIL Electronic Stability Program', True, 'problem', 'mdi:car-esp', 'mdi:car-esp'],
    'mil_esc_system': ['MIL ESC System', True, 'problem', 'mdi:car-traction-control', 'mdi:car-traction-control'],
    'mil_brake_fluid_level_low': ['MIL Brake Fluid Level Low', True, 'problem', 'mdi:car-brake-alert', 'mdi:car-brake-alert'],
    'mil_check_engine': ['MIL Check Engine', True, 'problem', 'mdi:engine-outline', 'mdi:engine-outline'],
    'mil_electronic_power_control': ['MIL Electronic Power Control', True, 'problem', 'mdi:car-info', 'mdi:car-info'],
}

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up a Mind binary sensor."""
    if discovery_info is None:
        return

    devs = list()
    mind = hass.data[DATA_MIND]
    for vehicle in mind.vehicles():
        for type in SENSOR_TYPES:
            devs.append(MindBinarySensor(vehicle.license_plate, type, mind, vehicle))

    add_devices(devs, True)


class MindBinarySensor(BinarySensorEntity):
    """A Mind binary sensor."""

    def __init__(self, name, sensor_type, mind, vehicle):
        """Initialize sensors from the car."""
        self._name = name + ' ' + SENSOR_TYPES[sensor_type][0]
        self._type = sensor_type
        self._vehicle = vehicle
        self._mind = mind
        self._state = None
        self._on_state = SENSOR_TYPES[sensor_type][1]
        self._device_class = SENSOR_TYPES[sensor_type][2]
        self._icon_off = SENSOR_TYPES[sensor_type][3]
        self._icon_on = SENSOR_TYPES[sensor_type][4]
        self._mils = {}
        for mil in self._data.get('milEvents'):
            eventId = mil['id']
            eventStatus = 'off' if mil['status'] == 'false' else 'on'
            self._mils[eventId] = eventStatus

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def device_class(self):
        """Return the class of this sensor."""
        return self._device_class

    @property
    def icon(self):
        """Return the icon of this sensor."""
        if self.is_on:
            return self._icon_on
        else:
            return self._icon_off

    @property
    def is_on(self):
        """Return the state of the entity."""
        return self._state == self._on_state

    @property
    def _data(self):
        return self._vehicle._mind_api._vehicle(self._vehicle.vehicleId)

    def _mil(self, key):
        return self._mils.get(key)

    def update(self):
        """Retrieve sensor data from the car."""

        if self._type == 'ignition':
            self._state = self._vehicle.ignition
            if self._state == True:
                self._mind.cache_ttl = 30
            else:
                self._mind.cache_ttl = 60
        elif self._type == 'doors':
            self._state = self._vehicle.doors_locked
        elif self._type == 'parking_brake':
            self._state = self._vehicle.parking_brake

        elif self._type == 'trip_registration':
            self._state = self._data.get('tripRegistration')
        elif self._type == 'stolen':
            self._state = self._data.get('isStolen')
        elif self._type == 'movement_notification':
            self._state = self._data.get('movementNotificationEnabled')
        elif self._type == 'mil_abs':
            self._state = self._mil('abs')
        elif self._type == 'mil_airbag':
            self._state = self._mil('airbag')
        elif self._type == 'mil_battery_voltage_low':
            self._state = self._mil('battery_voltage_low')
        elif self._type == 'mil_oil_level_check':
            self._state = self._mil('oil_level_check')
        elif self._type == 'mil_oil_level_high':
            self._state = self._mil('oil_level_high')
        elif self._type == 'mil_oil_level_low':
            self._state = self._mil('oil_level_low')
        elif self._type == 'mil_oil_pressure_low':
            self._state = self._mil('oil_pressure_low')
        elif self._type == 'mil_coolant_level_low':
            self._state = self._mil('coolant_level_low')
        elif self._type == 'mil_coolant_temp_high':
            self._state = self._mil('coolant_temp_high')
        elif self._type == 'mil_breaking_system':
            self._state = self._mil('breaking_system')
        elif self._type == 'mil_electronic_stability_program':
            self._state = self._mil('electronic_stability_program')
        elif self._type == 'mil_esc_system':
            self._state = self._mil('esc_system')
        elif self._type == 'mil_brake_fluid_level_low':
            self._state = self._mil('brake_fluid_level_low')
        elif self._type == 'mil_check_engine':
            self._state = self._mil('check_engine')
        elif self._type == 'mil_electronic_power_control':
            self._state = self._mil('electronic_power_control')

        else:
            self._state = None
            _LOGGER.warning("Could not retrieve state from %s", self.name)

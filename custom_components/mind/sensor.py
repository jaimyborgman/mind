"""
For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/sensor.mind/
"""
import logging

from custom_components.mind import DATA_MIND
from homeassistant.const import (LENGTH_KILOMETERS, VOLUME_LITERS)
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['mind']

SENSOR_TYPES = {
    'mileage': ['Mileage', LENGTH_KILOMETERS, 'mdi:counter'],
    'mileage_left': ['Mileage Left', LENGTH_KILOMETERS, 'mdi:fuel'],
    'fuel_left': ['Fuel Left', VOLUME_LITERS, 'mdi:fuel'],
    'battery': ['Battery', 'V', 'mdi:car-battery'],

    'vin': ['Vin', '', 'mdi:car-info'],
    'registration_number': ['Registration Number', '', 'mdi:car-info'],
    'brand': ['Brand', '', 'mdi:car-info'],
    'model': ['Model', '', 'mdi:car-info'],
    'edition': ['Edition', '', 'mdi:car-info'],
    'production_year': ['Production Year', '', 'mdi:car-info'],
    'engine_type': ['Engine Type', '', 'mdi:car-info'],
    'engine_fuel_type': ['Engine Fuel Type', '', 'mdi:car-info'],
    'odometer': ['Odometer', '', 'mdi:car-info'],
    'remaining_days_until_maintenance': ['Remaining Days Until Maintenance', '', 'mdi:car-info'],
    'remaining_days_until_service': ['Remaining Days Until Service', '', 'mdi:car-info'],
    'model_year': ['Model Year', '', 'mdi:car-info'],
    'maintenance_date': ['Maintenance Date', '', 'mdi:car-info'],
    'service_date': ['Service Date', '', 'mdi:car-info'],
    'apk_date': ['APK Date', '', 'mdi:car-info'],
    'mil_warning_count': ['MIL Warning Count', '', 'mdi:car-info'],
    'mil_error_count': ['MIL Error Count', '', 'mdi:car-info'],
    'mil_count': ['MIL Count', '', 'mdi:car-info'],
}


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up a Mind sensor."""
    if discovery_info is None:
        return

    devs = list()
    for vehicle in hass.data[DATA_MIND].vehicles():
        for type in SENSOR_TYPES:
            devs.append(MindSensor(vehicle.license_plate, type, vehicle))

    add_devices(devs, True)


class MindSensor(Entity):
    """A Mind sensor."""

    def __init__(self, name, sensor_type, vehicle):
        """Initialize sensors from the car."""
        self._name = name + ' ' + SENSOR_TYPES[sensor_type][0]
        self._type = sensor_type
        self._vehicle = vehicle
        self._state = None
        self._unit_of_measurement = SENSOR_TYPES[sensor_type][1]
        self._icon = SENSOR_TYPES[sensor_type][2]

    @property
    def name(self):
        """Return the name of the car."""
        return self._name

    @property
    def state(self):
        """Return the current state."""
        return self._state

    @property
    def icon(self):
        return self._icon

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit_of_measurement

    @property
    def _data(self):
        return self._vehicle._mind_api._vehicle(self._vehicle.vehicleId)

    def update(self):
        """Retrieve sensor data from the car."""

        if self._type == 'mileage':
            self._state = self._vehicle.mileage / 1000
        elif self._type == 'mileage_left':
            self._state = self._vehicle.mileage_left
        elif self._type == 'fuel_left':
            self._state = self._vehicle.fuellevel
        elif self._type == 'battery':
            self._state = round(self._vehicle.batteryVoltage, 2)

        elif self._type == 'vin':
            self._state = self._data.get('vin')
        elif self._type == 'registration_number':
            self._state = self._data.get('registrationNumber')
        elif self._type == 'brand':
            self._state = self._data.get('brand')
        elif self._type == 'model':
            self._state = self._data.get('model')
        elif self._type == 'edition':
            self._state = self._data.get('edition')
        elif self._type == 'production_year':
            self._state = self._data.get('productionYear')
        elif self._type == 'engine_type':
            self._state = self._data.get('engineType')
        elif self._type == 'engine_fuel_type':
            self._state = self._data.get('engineFuelType')
        elif self._type == 'odometer':
            self._state = self._data.get('odometer')
        elif self._type == 'remaining_days_until_maintenance':
            self._state = self._data.get('remainingDaysUntilMaintenance')
        elif self._type == 'remaining_days_until_service':
            self._state = self._data.get('remainingDaysUntilService')
        elif self._type == 'model_year':
            self._state = self._data.get('modelYear')
        elif self._type == 'maintenance_date':
            self._state = self._data.get('maintenanceDate')
        elif self._type == 'service_date':
            self._state = self._data.get('serviceDate')
        elif self._type == 'apk_date':
            self._state = self._data.get('apkDate')
        elif self._type == 'mil_warning_count':
            self._state = self._data.get('milWarningCount')
        elif self._type == 'mil_error_count':
            self._state = self._data.get('milErrorCount')
        elif self._type == 'mil_count':
            self._state = self._data.get('milCount')

        else:
            self._state = None
            _LOGGER.warning("Could not retrieve state from %s", self.name)

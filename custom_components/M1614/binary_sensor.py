from . import DOMAIN 

import logging
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.sensor import SensorEntity
_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    global DOMAIN
    

    # Recuperar parámetros específicos de discovery_info
    if discovery_info is not None:
        DOMAIN_module = discovery_info.get('DOMAIN_module')        
        HR_I = discovery_info.get('HR_I')

    sensors = [SimpleBinarySensor(HR_I[i][0], HR_I[i][1] , DOMAIN_module +"."+ HR_I[i][2], discovery_info) for i in range(len(HR_I))]
    async_add_entities(sensors, True)
    
    for sensor1 in sensors:
        discovery_info["ObjBinarySensors"].append(sensor1)
    
    OSV_temp=CommDataState(discovery_info.get('DOMAIN_module')+".data", "Sensor_Data" , discovery_info)
    async_add_entities([OSV_temp],True)
    discovery_info["ObjSensorsValues"].append(OSV_temp)
    
    OSV_temp=CommDataState(discovery_info.get('DOMAIN_module')+".ComErrors", "Sensor_Errors", discovery_info)
    async_add_entities([OSV_temp],True)
    discovery_info["ObjSensorsValues"].append(OSV_temp)
    
    
    

class SimpleBinarySensor(BinarySensorEntity):
    def __init__(self,HR, pos, name, discovery_info):
        self._name = name
        
        self.pos=pos
        self.HR=HR
        self._state = False
        self._available=True
        # Recuperar parámetros específicos de discovery_info
        if discovery_info is not None:
            self.BinarySensorsValues=discovery_info.get('BinarySensorsValuesHA')

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._state

        
    async def async_update(self):
        # Aquí iría la lógica de actualización del estado
        self._state=self.BinarySensorsValues[self.HR*16+self.pos]

    @property
    def available(self):
        return self._available

    def disable(self):
        self._available = False
        self.async_write_ha_state()
        
    def enable(self):
        self._available = True
        self.async_write_ha_state() 
        
         ###########################################################################################################3

class CommDataState(SensorEntity):
    def __init__(self, name , var , discovery_info):
        self._name = name
        self.var=var
        self.value = 0
        self.discovery_info=discovery_info
        self._available=True
        #_LOGGER.info("paso --------------------------------------------------------aca")

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        self.value=self.discovery_info.get(self.var)
        return  self.value
        
    @property
    def unit_of_measurement(self):
        return "count"

    async def async_update(self):
        self.value=self.discovery_info.get(self.var)
        
   
    @property
    def available(self):
        return self._available

    def disable(self):
        self._available = False
        self.async_write_ha_state()
        
    def enable(self):
        self._available = True
        self.async_write_ha_state() 
        
            

  

        
        
# /config/custom_components/M1614/switch.py
import asyncio
import time
import logging
from homeassistant.components.switch import SwitchEntity

from . import DOMAIN 


_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    global DOMAIN
    
        # Recuperar parámetros específicos de discovery_info
    if discovery_info is not None:
        DOMAIN_module = discovery_info.get('DOMAIN_module')        
        HR_O = discovery_info.get('HR_O')
        SwitchValuesHA=discovery_info.get('SwitchValuesHA')
        ComModBus_Active=discovery_info.get('ComModBus_Active')
   

    switches = [SimpleSwitch(HR_O[i][0], HR_O[i][1] , DOMAIN_module+"."+HR_O[i][2], SwitchValuesHA) for i in range(len(HR_O))]
    async_add_entities(switches, True)
    
    for switch1 in switches:
        discovery_info["ObjSwitches"].append(switch1)
    
    async_add_entities([SwitchAssistant(DOMAIN_module+"_Active","Switch_ComModBus_Active",discovery_info)])
     

class SimpleSwitch(SwitchEntity):
    def __init__(self,HR, pos, name, SwitchValuesHA):
        self._name = name
        self.pos=pos
        self.HR=HR
        self._state = False
        self.SwitchValuesHA=SwitchValuesHA
        self._available = True  # Disponibilidad del switch
        #_LOGGER.info("Paso por aca - Se creo suiche")

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._state

    async def async_turn_on(self, **kwargs):
        
        self._state = True
        self.SwitchValuesHA[self.HR*16+self.pos]=True
        self.async_write_ha_state()
        #_LOGGER.info("boton pulsado True")        

    async def async_turn_off(self, **kwargs):
        
        self._state = False
        self.SwitchValuesHA[self.HR*16+self.pos]=False
        self.async_write_ha_state()
        #_LOGGER.info("boton pulsado False")

    async def async_update(self):
        #_LOGGER.info("Actualizo estado de boton ")
        if self._state != self.SwitchValuesHA[self.HR*16+self.pos]:
            self._state = self.SwitchValuesHA[self.HR*16+self.pos]
            self.async_write_ha_state()
            #_LOGGER.info("Paso por aca update actualizo boton ")
            #_LOGGER.info(str(self.HR)+"-"+str(self.pos))
    
    
    @property
    def available(self):
        return self._available

    def disable(self):
        self._available = False
        self.async_write_ha_state()
        

    def enable(self):
        self._available = True
        self.async_write_ha_state() 
        
            

#####################################################################################################33

class SwitchAssistant(SwitchEntity):
    """Representation of a custom switch."""

    def __init__(self, name , var , discovery_info ):
        """Initialize the switch."""
        self._name = name
        self.var=var
        self._state = discovery_info[var]
        self.discovery_info=discovery_info
        
    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def is_on(self):
        """Return true if the switch is on."""
        return self._state

    async def async_turn_on(self, **kwargs):
        
        """Turn the switch on."""
        self._state = True
        self.discovery_info[self.var]=self._state
        self.schedule_update_ha_state()

    async def async_turn_off(self, **kwargs):
        
        """Turn the switch off."""
        self._state = False
        self.discovery_info[self.var]=self._state
        self.schedule_update_ha_state()
       
        
    async def async_update(self):
        if self._state != self.discovery_info[self.var]:
            self._state = self.discovery_info[self.var]
            self.async_write_ha_state()













    
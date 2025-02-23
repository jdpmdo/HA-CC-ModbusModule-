# /config/custom_components/M1614/__init__.py
# corregido para core 2025.1.2
# 22-01-25 se cambia la version a un solo bloque de lectura escritura 
# toma de puerto al inicio y liberacion al final, el bloque no esta particionado
# Actualizado y en prueba para la version HA 2025.2.5 que cambio algunos argumentos de Pymodbus

import asyncio
import logging
import pymodbus
from pymodbus.client import AsyncModbusSerialClient as ModbusClient
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_NAME
import logging


from homeassistant.helpers.discovery import async_load_platform


# Candado global compartido por todas las instancias
MODBUS_LOCK = asyncio.Lock()

_LOGGER = logging.getLogger(__name__)

DOMAIN = "M1614"


CONF_MODULES = "modules"
CONF_SERIAL_PORT = "serial_port"
CONF_SERIAL_BAUDRATE = "serial_baudrate"
CONF_SERIAL_PARITY = "serial_parity"
CONF_SERIAL_STOPBITS = "serial_stopbits"
CONF_SERIAL_BYTESIZE = "serial_bytesize"
CONF_SERIAL_TIMEOUT = "serial_timeout"

CONF_SLAVE_ID = "slave_id"
CONF_REGISTER_ADDRESS = "register_address"
CONF_SERIAL_DELAY = "delay"
CONF_SERIAL_QUANTITY_HRO = "quantity_HRO"
CONF_SERIAL_QUANTITY_HRI = "quantity_HRI"
CONF_SERIAL_ERRORS = "serial_errors"
CONF_SERIAL_SLEEP = "serial_sleep"
CONF_HR_O = "HRO"
CONF_HR_I = "HRI"


DEFAULT_SERIAL_PORT = '/dev/ttyUSB0'
DEFAULT_SERIAL_BAUDRATE = 19200
DEFAULT_SERIAL_PARITY = 'E'
DEFAULT_SERIAL_STOPBITS = 1
DEFAULT_SERIAL_BYTESIZE = 8
DEFAULT_SERIAL_TIMEOUT = 1


DEFAULT_SLAVE_ID = 20
DEFAULT_REGISTER_ADDRESS = 100
DEFAULT_SERIAL_DELAY = 2
DEFAULT_SERIAL_QUANTITY_HRO = 2
DEFAULT_SERIAL_QUANTITY_HRI = 1
DEFAULT_SERIAL_ERRORS = 20 
DEFAULT_SERIAL_SLEEP = 40 

# Definimos el esquema para validar la configuración
MODULE_SCHEMA = vol.Schema({
    vol.Required(CONF_SERIAL_PORT, default=DEFAULT_SERIAL_PORT): cv.string,
    vol.Required(CONF_SERIAL_BAUDRATE, default=DEFAULT_SERIAL_BAUDRATE): cv.positive_int,
    vol.Required(CONF_SERIAL_PARITY, default=DEFAULT_SERIAL_PARITY): cv.string,
    vol.Required(CONF_SERIAL_STOPBITS, default=DEFAULT_SERIAL_STOPBITS): cv.positive_int,
    vol.Required(CONF_SERIAL_BYTESIZE, default=DEFAULT_SERIAL_BYTESIZE): cv.positive_int,
    vol.Required(CONF_SERIAL_TIMEOUT, default=DEFAULT_SERIAL_TIMEOUT): cv.positive_int,
    
    vol.Required(CONF_SLAVE_ID, default=DEFAULT_SLAVE_ID): cv.positive_int,
    vol.Required(CONF_REGISTER_ADDRESS, default=DEFAULT_REGISTER_ADDRESS): cv.positive_int,
    vol.Required(CONF_SERIAL_DELAY, default=DEFAULT_SERIAL_DELAY): cv.positive_int,
    vol.Required(CONF_SERIAL_QUANTITY_HRI, default=DEFAULT_SERIAL_QUANTITY_HRI): cv.positive_int,    
    vol.Required(CONF_SERIAL_QUANTITY_HRO, default=DEFAULT_SERIAL_QUANTITY_HRO): cv.positive_int,
    
    vol.Required(CONF_SERIAL_ERRORS, default=DEFAULT_SERIAL_ERRORS): cv.positive_int, 
    vol.Required(CONF_SERIAL_SLEEP, default=DEFAULT_SERIAL_SLEEP): cv.positive_int,
    vol.Required(CONF_HR_I): vol.All(cv.ensure_list, [vol.ExactSequence([cv.positive_int, cv.positive_int, cv.string])]),    
    vol.Required(CONF_HR_O): vol.All(cv.ensure_list, [vol.ExactSequence([cv.positive_int, cv.positive_int, cv.string])])
    

})

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_MODULES): vol.Schema({
            cv.string: MODULE_SCHEMA
        })
    })
}, extra=vol.ALLOW_EXTRA)

async def async_setup(hass, config):
    component_config = config.get(DOMAIN, {})
    
    modules = component_config.get(CONF_MODULES, {})

    # Guardamos la configuración de cada módulo en hass.data
    hass.data[DOMAIN] = modules

    for module, module_config in modules.items():
        _LOGGER.info(f"Setting up module: {module}")
        
        # Asignar variables internas
        serial_port = module_config[CONF_SERIAL_PORT]
        serial_baudrate = module_config[CONF_SERIAL_BAUDRATE]
        serial_parity = module_config[CONF_SERIAL_PARITY]
        serial_stopbits = module_config[CONF_SERIAL_STOPBITS]
        serial_bytesize = module_config[CONF_SERIAL_BYTESIZE]
        
        serial_timeout = module_config[CONF_SERIAL_TIMEOUT]        
        
        slave_id = module_config[CONF_SLAVE_ID]
        register_address = module_config[CONF_REGISTER_ADDRESS]
        serial_delay = module_config[CONF_SERIAL_DELAY]
        serial_quantity_HRO = module_config[CONF_SERIAL_QUANTITY_HRO]
        serial_quantity_HRI = module_config[CONF_SERIAL_QUANTITY_HRI]
        serial_errors = module_config[CONF_SERIAL_ERRORS]
        serial_sleep = module_config[CONF_SERIAL_SLEEP]        
        hr_o = module_config[CONF_HR_O]
        hr_i = module_config[CONF_HR_I]


        # Guardar las configuraciones específicas del módulo en hass.data
        hass.data[DOMAIN][module] = {
            CONF_SERIAL_PORT: serial_port,
            CONF_SERIAL_BAUDRATE: serial_baudrate,
            CONF_SERIAL_PARITY: serial_parity,
            CONF_SERIAL_STOPBITS: serial_stopbits,
            CONF_SERIAL_BYTESIZE: serial_bytesize,
            CONF_SERIAL_TIMEOUT: serial_timeout,
            
            CONF_SLAVE_ID: slave_id,
            CONF_REGISTER_ADDRESS: register_address,
            CONF_SERIAL_DELAY: serial_delay,
            CONF_SERIAL_QUANTITY_HRO: serial_quantity_HRO ,
            CONF_SERIAL_QUANTITY_HRI: serial_quantity_HRI , 
            CONF_SERIAL_ERRORS: serial_errors,
            CONF_SERIAL_SLEEP: serial_sleep,            
            CONF_HR_O: hr_o,
            CONF_HR_I: hr_i,
        }

        _LOGGER.info(f"module: {module}")
        _LOGGER.info(f"Serial Port: {serial_port}")
        _LOGGER.info(f"Serial Baudrate: {serial_baudrate}")
        _LOGGER.info(f"Serial Parity: {serial_parity}")
        _LOGGER.info(f"Serial Stopbits: {serial_stopbits}")
        _LOGGER.info(f"Serial Bytesize: {serial_bytesize}")
        _LOGGER.info(f"Serial Timeout: {serial_timeout}")       
        
        _LOGGER.info(f"Slave ID: {slave_id}")
        _LOGGER.info(f"Register Address: {register_address}")
        _LOGGER.info(f"delay: {serial_delay}")
        _LOGGER.info(f"quantity_HRO: {serial_quantity_HRO}")
        _LOGGER.info(f"quantity_HRI: {serial_quantity_HRI}")  
        _LOGGER.info(f"Serials errors: {serial_errors}")     
        _LOGGER.info(f"Serials sleep: {serial_sleep}")          
        _LOGGER.info(f"HR_O: {hr_o}")
        _LOGGER.info(f"HR_I: {hr_i}")

        ModuloM1416s=[]
        ModuloM1416 = ModuleComponent(hass ,DOMAIN , module ,  module_config , config)
        ModuloM1416s.append(ModuloM1416) 

    return True

# clase que crea un bucle de interrogacion al modulo especifico
class ModuleComponent:

    def __init__(self, hass, DOMAIN, module ,  module_config: dict , config ):
        
        self.hass = hass
        self.cont = 0
        self.DOMAIN=DOMAIN
        self.DOMAIN_module=module
        
        self.ComModBus_ReadErrors=0

        # Asignar variables internas
        serial_port = module_config[CONF_SERIAL_PORT]
        serial_baudrate = module_config[CONF_SERIAL_BAUDRATE]
        serial_parity = module_config[CONF_SERIAL_PARITY]
        serial_stopbits = module_config[CONF_SERIAL_STOPBITS]
        serial_bytesize = module_config[CONF_SERIAL_BYTESIZE]
        serial_timeout = module_config[CONF_SERIAL_TIMEOUT]
        
        self._client =ModbusClient(
                port=serial_port,
                baudrate=serial_baudrate,
                parity=serial_parity,
                stopbits=serial_stopbits,
                bytesize=serial_bytesize,
                timeout=serial_timeout
            )

        
        self.slave_id = module_config[CONF_SLAVE_ID]
        self.register_address = module_config[CONF_REGISTER_ADDRESS]-1
        self.serial_delay = module_config[CONF_SERIAL_DELAY]
        
        self.serial_quantity_HRO = module_config[CONF_SERIAL_QUANTITY_HRO]
        self.serial_quantity_HRI = module_config[CONF_SERIAL_QUANTITY_HRI]
        self.ComModBus_ReadErros = module_config[CONF_SERIAL_ERRORS] #serial_errors
        self.serial_sleep = module_config[CONF_SERIAL_SLEEP]        

        self.SwitchValuesHA = [False] * 16 * self.serial_quantity_HRO # valores de HA
        self.SwitchValuesHA_C = [False] * 16 * self.serial_quantity_HRO # copia valores de HA
        
        self.BinarySensorsValuesHA = [False] * 16 * self.serial_quantity_HRI
        
        # Aca estoy definiendo las listas donde de los objetos 
        self.ObjSwitches=[]
        self.ObjBinarySensors=[]
        self.ObjSensorsValues=[]
        
        hr_o = module_config[CONF_HR_O]
        hr_i = module_config[CONF_HR_I]
        
        self.ComModBus_Sleep=False
        
        # Configuración básica del componente
            # Parámetros específicos que deseas pasar a la plataforma
        
        discovery_info = {
            'DOMAIN_module': module,
            'HR_O': hr_o,
            'HR_I': hr_i,
            'SwitchValuesHA': self.SwitchValuesHA,
            'BinarySensorsValuesHA': self.BinarySensorsValuesHA,

            'ObjSwitches': self.ObjSwitches,
            'ObjBinarySensors': self.ObjBinarySensors,
            'ObjSensorsValues': self.ObjSensorsValues,
            
            'Switch_ComModBus_Active': True,
            'Sensor_Errors' : 0,
            'Sensor_Data' : 0

        }
        
        hass.async_create_task(async_load_platform(hass,'switch', self.DOMAIN, discovery_info, config))
        hass.async_create_task(async_load_platform(hass,'binary_sensor', self.DOMAIN, discovery_info, config))        
        hass.loop.create_task(self.my_async_function(hass,discovery_info))

    async def my_async_function(self , hass ,discovery_info ):
        
        sleep_count=0
        errors=0
        data=0
        cont1=0

        SwitchValuesReadModule = self.SwitchValuesHA[:]    #valores leidos del modulo
        SwitchValuesWriteModule = self.SwitchValuesHA[:]   #valores a escribir en modulo
        SwitchValuesM1614 = self.SwitchValuesHA[:]         #valor supuesto del modulo
        BinarySensorsValues1= self.SwitchValuesHA[:]       #valores leidos del modulo en scan anterior
        
        paso_enable=False
        
        # Espero 5 segundos antes de iniciar el bucle de comunicacion
        await asyncio.sleep(5)
        
        while True:
            
            if discovery_info["Switch_ComModBus_Active"] and not self.ComModBus_Sleep:
                
                if not paso_enable: #Rutina para habilitar componentes de pantalla
                    paso_enable=True
                    for obj in self.ObjSwitches : 
                        obj.enable()
                    for obj in self.ObjBinarySensors : 
                        obj.enable()
                    for obj in self.ObjSensorsValues : 
                        obj.enable()                  
                
                data+=1
                sleep_count+=1
                ReadOk=True
                
                async with MODBUS_LOCK:  # Adquiere el candado para esta configuración
                
                    try:

                        if not self._client.connected:
                            #_LOGGER.info("conecto modbus "+discovery_info["DOMAIN_module"])                        
                            await self._client.connect()
                            
                        result = await self._client.read_holding_registers(
                            address=self.register_address, 
                            count=(self.serial_quantity_HRO + self.serial_quantity_HRI),
                            slave=self.slave_id
                            )
                            

                        if not result.isError():
                            #_LOGGER.info("Modulo: %s - Lei modbus ->", self.DOMAIN_module)
    
                            #Cargo las entradas discretas        
                            for hr in range(self.serial_quantity_HRI):
                                for i in range(16):
                                    self.BinarySensorsValuesHA[i+16*hr]=bool(result.registers[hr] & (1 << i))        
    
                            #Cargo las salidas discretas
                            for hr in range(self.serial_quantity_HRO):
                                for i in range(16):
                                    SwitchValuesReadModule[i+16*hr]=bool(result.registers[hr+self.serial_quantity_HRI] & (1 << i))
    
                        else:
                            _LOGGER.error("Modulo: %s - Lectura no responde", self.DOMAIN_module)
                            ReadOk=False
                            
                    except Exception as e:
                        _LOGGER.error("Modulo: %s - Excepción al leer en los registros Modbus: %s", self.DOMAIN_module, str(e))
                        ReadOk=False
                        if self._client.connected:
                            self._client.close()   # Cierra si hay error para reiniciar en el próximo intento   

                    if ReadOk==False:
                        #_LOGGER.error("No lei modbuss")
                        errors+=1
    
                    ## si cambio algun valor de los sensores fuerzo su cambio en HA
                    if BinarySensorsValues1!=self.BinarySensorsValuesHA: 
                        for Sensor1 in self.ObjBinarySensors : #BinarySensor1:
                            Sensor1.schedule_update_ha_state(force_refresh=True)
                        
                        sleep_count=0
        
                    #Memorizo valores de sensores
                    BinarySensorsValues1[:]=self.BinarySensorsValuesHA[:]
                    
                    # Estrategia de tratamiento de cambios de salidas
                    if self.SwitchValuesHA!=SwitchValuesM1614 : #and self.SwitchValuesHA1!=self.SwitchValuesHA : # Cambio desde HA tiene prioridad 
                        SwitchValuesWriteModule[:]=self.SwitchValuesHA[:]
                        regChange=True
                        #_LOGGER.info("Cambio HA")
                    
                    elif SwitchValuesReadModule!=SwitchValuesM1614 and ReadOk==True  : # cambio detectado desde el modulo 
                    
                        regChange=True
                        SwitchValuesWriteModule[:]=SwitchValuesReadModule[:]
                        #_LOGGER.info("Cambio modulo")
                        
                    else:
                        regChange=False
                        #_LOGGER.info("Sin cambios")
        
                    # cargo los bits a escribir
                    reg=[0]*self.serial_quantity_HRO
                    for hr in range(self.serial_quantity_HRO):
                       for i in range(16):
                           if SwitchValuesWriteModule[i+16*hr]==True:
                               reg[hr] |= (1 <<  i)
                    
                    # si se detectan cambios se deben transmitir al modulo
                    if regChange:
                        WriteOk=True
                        try:
             
                            if not self._client.connected:
                                await self._client.connect()

                            result = await self._client.write_registers(self.register_address +self.serial_quantity_HRI , reg, slave=self.slave_id)
                                
                            # Verificar si la escritura fue exitosa
                            if result.isError():
                                WriteOk=False
                                
                                _LOGGER.error("Modulo: %s - Error al escribir en los registros Modbus: %s", self.DOMAIN_module, result)
                    
                        except Exception as e:
                            _LOGGER.error("Modulo: %s - Excepción al escribir en los registros Modbus: %s", self.DOMAIN_module, str(e))
                            WriteOk=False
                            if self._client.connected:
                                self._client.close() # Cierra si hay error para reiniciar en el próximo intento
                            
                        if WriteOk:
                            SwitchValuesM1614[:]=SwitchValuesWriteModule[:]
                            self.SwitchValuesHA[:]=SwitchValuesM1614[:]
                        else:
                            self.SwitchValuesHA[:]=SwitchValuesReadModule[:]
                            SwitchValuesM1614[:]=self.SwitchValuesHA[:]
                            errors+=1

                        # Acceder a los interruptores guardados en hass.data
                        #_LOGGER.info("intento actualizar botones ----------------- suiches")
                        #actualizo los suiches 
                        for switch in self.ObjSwitches : 
                            switch.schedule_update_ha_state(force_refresh=True)
                        sleep_count=0
                    else:
                        pass
                        #_LOGGER.info("sin cambio no escribo modbus ##################")

                    if self._client.connected:
                        self._client.close() # Cierra si hay error para reiniciar en el próximo intento

            else: # modulo desactivado
                
                errors=0
                data=0
                paso_enable=False
                ###self.client.close() verificar
                
                #Deshabilito todos los objetos por modulo desactivado
                for obj in self.ObjSwitches : 
                    obj.disable()
                for obj in self.ObjBinarySensors : 
                    obj.disable()
                for obj in self.ObjSensorsValues : 
                    obj.disable()                    

            if self.serial_sleep!=0:
                if sleep_count>=self.serial_sleep :
                    self.ComModBus_Sleep=False
                    
            #despues de n errores se desactiva el modulo
            if errors >= self.ComModBus_ReadErros and self.ComModBus_ReadErros != 0:
                discovery_info["Switch_ComModBus_Active"]=False
            
            # cargar los datos en sensor
            discovery_info["Sensor_Data"]=data
            discovery_info["Sensor_Errors"]=errors
            
            for obj in self.ObjSensorsValues : 
                obj.schedule_update_ha_state(force_refresh=True)            

            cont1+=1
    
            if cont1==10:
                cont1=0
                #_LOGGER.info("paso 10")
                #for i in range(16):
                #    SwitchValuesHA[i]= not SwitchValuesHA[i]
    
            await asyncio.sleep(self.serial_delay)
            
           

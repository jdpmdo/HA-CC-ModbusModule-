# /config/custom_components/M1614/__init__.py
import asyncio
import logging
import pymodbus
from pymodbus.client import ModbusSerialClient as ModbusClient
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_NAME
import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = "M1614"


com_busy=False

CONF_MODULES = "modules"
CONF_SERIAL_PORT = "serial_port"
CONF_SERIAL_BAUDRATE = "serial_baudrate"
CONF_SERIAL_PARITY = "serial_parity"
CONF_SERIAL_STOPBITS = "serial_stopbits"
CONF_SERIAL_BYTESIZE = "serial_bytesize"
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
            CONF_SLAVE_ID: slave_id,
            CONF_REGISTER_ADDRESS: register_address,
            CONF_SERIAL_DELAY: serial_delay,
            CONF_SERIAL_QUANTITY_HRO: serial_quantity_HRO ,
            CONF_SERIAL_QUANTITY_HRI: serial_quantity_HRI , 
            CONF_SERIAL_ERRORS: serial_errors,
            CONF_SERIAL_SLEEP: serial_sleep,            
            CONF_HR_O: hr_o,
            CONF_HR_I: hr_i
        }

        _LOGGER.info(f"module: {module}")
        _LOGGER.info(f"Serial Port: {serial_port}")
        _LOGGER.info(f"Serial Baudrate: {serial_baudrate}")
        _LOGGER.info(f"Serial Parity: {serial_parity}")
        _LOGGER.info(f"Serial Stopbits: {serial_stopbits}")
        _LOGGER.info(f"Serial Bytesize: {serial_bytesize}")
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
        
        self.client = ModbusClient(
                method='rtu',
                port=serial_port,
                baudrate=serial_baudrate,
                parity=serial_parity,
                stopbits=serial_stopbits,
                bytesize=serial_bytesize,
                timeout=1
                )        
        
        self.slave_id = module_config[CONF_SLAVE_ID]
        self.register_address = module_config[CONF_REGISTER_ADDRESS]-1
        self.serial_delay = module_config[CONF_SERIAL_DELAY]
        
        self.serial_quantity_HRO = module_config[CONF_SERIAL_QUANTITY_HRO]
        self.serial_quantity_HRI = module_config[CONF_SERIAL_QUANTITY_HRI]
        self.ComModBus_ReadErros = module_config[CONF_SERIAL_ERRORS] #serial_errors
        self.serial_sleep = module_config[CONF_SERIAL_SLEEP]        

        self.SwitchValuesHA = [False] * 16 * self.serial_quantity_HRO # valores de HA
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
        
        hass.async_create_task(hass.helpers.discovery.async_load_platform('switch', self.DOMAIN, discovery_info, config))
        hass.async_create_task(hass.helpers.discovery.async_load_platform('binary_sensor', self.DOMAIN, discovery_info, config))
        hass.loop.create_task(self.my_async_function(hass,discovery_info))


    async def my_async_function(self , hass ,discovery_info ):
        
        global com_busy
        
        sleep_count=0
        errors=0
        data=0
        cont1=0

        SwitchValuesReadModule = self.SwitchValuesHA[:]    #valores leidos del modulo
        SwitchValuesWriteModule = self.SwitchValuesHA[:]   #valores a escribir en modulo
        SwitchValuesM1614 = self.SwitchValuesHA[:]         #valor supuesto del modulo
        BinarySensorsValues1= self.SwitchValuesHA[:]       #valores leidos del modulo en scan anterior
        
        paso_enable=False
        while True:
            
            if discovery_info["Switch_ComModBus_Active"] and not self.ComModBus_Sleep:
                
                if not paso_enable:
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
                

                try:

                    while com_busy:
                        await asyncio.sleep(0.1)  # Espera 100ms antes de volver a comprobar la condición


                    if not self.client.connected:
                        #_LOGGER.info("conecto modbus "+discovery_info["DOMAIN_module"])                        
                        self.client.connect()
                        

                    com_busy=True
                    
                    result = await hass.async_add_executor_job(
                        lambda: self.client.read_holding_registers(self.register_address, 
                        (self.serial_quantity_HRO + self.serial_quantity_HRI),
                        slave=self.slave_id)
                        )
                        
                    self.client.close()      
                    com_busy=False  

                    if not result.isError():
                        #_LOGGER.info("Lei modbus ->")

                        #Cargo las entradas discretas        
                        for hr in range(self.serial_quantity_HRI):
                            for i in range(16):
                                self.BinarySensorsValuesHA[i+16*hr]=bool(result.registers[hr] & (1 << i))        



                        
                        #Cargo las salidas discretas
                        for hr in range(self.serial_quantity_HRO):
                            for i in range(16):
                                SwitchValuesReadModule[i+16*hr]=bool(result.registers[hr+self.serial_quantity_HRI] & (1 << i))



                    else:
                        #_LOGGER.error("Lectura no responde modulo")
                        ReadOk=False
                        
                except Exception as e:
                    #_LOGGER.error("Excepción al leer en los registros Modbus: %s", str(e))
                    ReadOk=False
                    self.client.close()      
                    com_busy=False  

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
                
                await asyncio.sleep((self.serial_delay/2))
    
                # Estrategia de tratamiento de camvios de salidas
                if self.SwitchValuesHA!=SwitchValuesM1614 : # Cambio desde HA tiene prioridad 
                    SwitchValuesWriteModule[:]=self.SwitchValuesHA[:]
                    regChange=True
                    #_LOGGER.info("algo cambio")
                
                elif SwitchValuesReadModule!=SwitchValuesM1614: # cambio detectado desde el modulo 
                
                    regChange=True
                    SwitchValuesWriteModule[:]=SwitchValuesReadModule[:]
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
                        while com_busy:
                            await asyncio.sleep(0.1)  # Espera 100ms antes de volver a comprobar la condición                       
                        
                        if not self.client.connected:
                            self.client.connect()
                            
                        com_busy=True
                        
                        result = await hass.async_add_executor_job(
                            lambda: self.client.write_registers(self.register_address +self.serial_quantity_HRI , reg, slave=self.slave_id)
                            )    
                            
                        self.client.close()
                        com_busy=False 

                        # Verificar si la escritura fue exitosa
                        if result.isError():
                            WriteOk=False
                            _LOGGER.error("Error al escribir en los registros Modbus: %s", result)
                
                    except Exception as e:
                        _LOGGER.error("Excepción al escribir en los registros Modbus: %s", str(e))
                        WriteOk=False
                        self.client.close()
                        com_busy=False 
    
                    if WriteOk:
                        self.SwitchValuesHA[:]=SwitchValuesWriteModule[:]    
                        SwitchValuesM1614[:]=SwitchValuesWriteModule[:]

                    else:
                      
                        self.SwitchValuesHA[:]=SwitchValuesReadModule[:]
                        SwitchValuesM1614[:]=SwitchValuesReadModule[:]
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
            
            else: # modulo desactivado
                errors=0
                data=0
                paso_enable=False
                self.client.close()
                
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
            if errors>=self.ComModBus_ReadErros:
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
    
            await asyncio.sleep((self.serial_delay/2))

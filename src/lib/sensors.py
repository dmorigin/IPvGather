
from typing import List, Any, Tuple
from goodwe import Sensor as GoodWeSensor, SensorKind


"""
This map contains the list of all sensors that will be processed
by the gatherer. Sensors that are not part of this list are
ignored.
"""    
_sensor_map = [
    "timestamp",#, "Timestamp" ], #2022-11-02 19:30:22 
    "vpv1",#PV1 Voltage" ], #0.0 V
    "ipv1",#PV1 Current" ], #0.0 A
    "ppv1",#PV1 Power" ], #0 W
    "vpv2",#PV2 Voltage" ], #0.0 V
    "ipv2",#PV2 Current" ], #0.0 A
    "ppv2",#PV2 Power" ], #0 W
    "ppv",#PV Power" ], #0 W
    "pv2_mode",#PV2 Mode code" ], #0 
    "pv2_mode_label",#PV2 Mode" ], #PV panels not connected 
    "pv1_mode",#PV1 Mode code" ], #0 
    "pv1_mode_label",#PV1 Mode" ], #PV panels not connected 
    "vgrid",#On-grid L1 Voltage" ], #244.2 V
    "igrid",#On-grid L1 Current" ], #0.8 A
    "fgrid",#On-grid L1 Frequency" ], #49.94 Hz
    "pgrid",#On-grid L1 Power" ], #138 W
    "vgrid2",#On-grid L2 Voltage" ], #238.6 V
    "igrid2",#On-grid L2 Current" ], #0.9 A
    "fgrid2",#On-grid L2 Frequency" ], #49.96 Hz
    "pgrid2",#On-grid L2 Power" ], #131 W
    "vgrid3",#On-grid L3 Voltage" ], #234.3 V
    "igrid3",#On-grid L3 Current" ], #0.9 A
    "fgrid3",#On-grid L3 Frequency" ], #49.98 Hz
    "pgrid3",#On-grid L3 Power" ], #138 W
    "grid_mode",#Grid Mode code" ], #1 
    "grid_mode_label",#Grid Mode" ], #Connected to grid 
    "total_inverter_power",#Total Power" ], #407 W
    "active_power",#Active Power" ], #8 W
    "grid_in_out",#On-grid Mode code" ], #0 
    "grid_in_out_label",#On-grid Mode" ], #Idle 
    "reactive_power",#Reactive Power" ], #0 var
    "apparent_power",#Apparent Power" ], #0 VA
    "backup_v1",#Back-up L1 Voltage" ], #244.2 V
    "backup_i1",#Back-up L1 Current" ], #0.4 A
    "backup_f1",#Back-up L1 Frequency" ], #49.93 Hz
    "load_mode1",#Load Mode L1" ], #1 
    "backup_p1",#Back-up L1 Power" ], #36 W
    "backup_v2",#Back-up L2 Voltage" ], #238.1 V
    "backup_i2",#Back-up L2 Current" ], #0.2 A
    "backup_f2",#Back-up L2 Frequency" ], #49.96 Hz
    "load_mode2",#Load Mode L2" ], #1 
    "backup_p2",#Back-up L2 Power" ], #12 W
    "backup_v3",#Back-up L3 Voltage" ], #234.3 V
    "backup_i3",#Back-up L3 Current" ], #0.5 A
    "backup_f3",#Back-up L3 Frequency" ], #49.98 Hz
    "load_mode3",#Load Mode L3" ], #1 
    "backup_p3",#Back-up L3 Power" ], #65 W
    "load_p1",#Load L1" ], #53 W
    "load_p2",#Load L2" ], #85 W
    "load_p3",#Load L3" ], #148 W
    "backup_ptotal",#Back-up Load" ], #128 W
    "load_ptotal",#Load" ], #271 W
    "ups_load",#Ups Load" ], #3 %
    "temperature_air",#Inverter Temperature (Air)" ], #36.1 C
    "temperature_module",#Inverter Temperature (Module)" ], #0.0 C
    "temperature",#Inverter Temperature (Radiator)" ], #31.8 C
    "function_bit",#Function Bit" ], #16416 
    "bus_voltage",#Bus Voltage" ], #654.2 V
    "nbus_voltage",#NBus Voltage" ], #325.1 V
    "vbattery1",#Battery Voltage" ], #319.4 V
    "ibattery1",#Battery Current" ], #1.0 A
    "pbattery1",#Battery Power" ], #319 W
    "battery_mode",#Battery Mode code" ], #2 
    "battery_mode_label",#Battery Mode" ], #Discharge 
    "warning_code",#Warning code" ], #0 
    "safety_country",#Safety Country code" ], #32 
    "safety_country_label",#Safety Country" ], #50Hz Grid Default 
    "work_mode",#Work Mode code" ], #1 
    "work_mode_label",#Work Mode" ], #Normal (On-Grid) 
    "operation_mode",#Operation Mode code" ], #0 
    "error_codes",#Error Codes" ], #0 
    "errors",#Errors" ], # 
    "e_total",#Total PV Generation" ], #337.3 kWh
    "e_day",#Today's PV Generation" ], #20.5 kWh
    "e_total_exp",#Total Energy (export)" ], #329.1 kWh
    "h_total",#Hours Total" ], #271 h
    "e_day_exp",#Today Energy (export)" ], #18.7 kWh
    "e_total_imp",#Total Energy (import)" ], #0.2 kWh
    "e_day_imp",#Today Energy (import)" ], #0.0 kWh
    "e_load_total",#Total Load" ], #224.7 kWh
    "e_load_day",#Today Load" ], #9.4 kWh
    "e_bat_charge_total",#Total Battery Charge" ], #53.4 kWh
    "e_bat_charge_day",#Today Battery Charge" ], #5.1 kWh
    "e_bat_discharge_total",#Total Battery Discharge" ], #24.7 kWh
    "e_bat_discharge_day",#Today Battery Discharge" ], #1.4 kWh
    "diagnose_result",#Diag Status Code" ], #33554496 
    "diagnose_result_label",#Diag Status" ], #Discharge Driver On, PF value set 
    "house_consumption",#House Consumption" ], #311 W
    "battery_bms",#Battery BMS" ], #255 
    "battery_index",#Battery Index" ], #402 
    "battery_status",#Battery Status" ], #1 
    "battery_temperature",#Battery Temperature" ], #23.7 C
    "battery_charge_limit",#Battery Charge Limit" ], #10 A
    "battery_discharge_limit",#Battery Discharge Limit" ], #25 A
    "battery_error_l",#Battery Error L" ], #0 
    "battery_soc",#Battery State of Charge" ], #92 %
    "battery_soh",#Battery State of Health" ], #100 %
    "battery_modules",#Battery Modules" ], #6 
    "battery_warning_l",#Battery Warning L" ], #0 
    "battery_protocol",#Battery Protocol" ], #290 
    "battery_error_h",#Battery Error H" ], #0 
    "battery_error",#Battery Error" ], # 
    "battery_warning_h",#Battery Warning H" ], #2 
    "battery_warning",#Battery Error" ], #err17 
    "battery_sw_version",#Battery Software Version" ], #1 
    "battery_hw_version",#Battery Hardware Version" ], #273 
    "battery_max_cell_temp_id",#Battery Max Cell Temperature ID" ], #531 
    "battery_min_cell_temp_id",#Battery Min Cell Temperature ID" ], #1041 
    "battery_max_cell_voltage_id",#Battery Max Cell Voltage ID" ], #1299 
    "battery_min_cell_voltage_id",#Battery Min Cell Voltage ID" ], #240 
    "battery_max_cell_temp",#Battery Max Cell Temperature" ], #23.5 C
    "battery_min_cell_temp",#Battery Min Cell Temperature" ], #331.6 C
    "battery_max_cell_voltage",#Battery Max Cell Voltage" ], #331.4 V
    "battery_min_cell_voltage",#Battery Min Cell Voltage" ], #0.0 V
    "commode",#Commode" ], #1 
    "rssi",#RSSI" ], #11 
    "manufacture_code",#Manufacture Code" ], #10 
    "meter_test_status",#Meter Test Status" ], #0 
    "meter_comm_status",#Meter Communication Status" ], #1 
    "active_power1",#Active Power L1" ], #47 W
    "active_power2",#Active Power L2" ], #34 W
    "active_power3",#Active Power L3" ], #-76 W
    "active_power_total",#Active Power Total" ], #5 W
    "reactive_power_total",#Reactive Power Total" ], #761 var
    "meter_power_factor1",#Meter Power Factor L1" ], #0.197 
    "meter_power_factor2",#Meter Power Factor L2" ], #0.094 
    "meter_power_factor3",#Meter Power Factor L3" ], #-0.289 
    "meter_power_factor",#Meter Power Factor" ], #0.008 
    "meter_freq",#Meter Frequency" ], #49.98 Hz
    "meter_e_total_exp",#Meter Total Energy (export)" ], #176.706 kWh
    "meter_e_total_imp",#Meter Total Energy (import)" ], #178.168 kWh
    "meter_active_power1",#Meter Active Power L1" ], #47 W
    "meter_active_power2",#Meter Active Power L2" ], #34 W
    "meter_active_power3",#Meter Active Power L3" ], #-76 W
    "meter_active_power_total",#Meter Active Power Total" ], #5 W
    "meter_reactive_power1",#Meter Reactive Power L1" ], #214 var
    "meter_reactive_power2",#Meter Reactive Power L2" ], #326 var
    "meter_reactive_power3",#Meter Reactive Power L2" ], #220 var
    "meter_reactive_power_total",#Meter Reactive Power Total" ], #761 var
    "meter_apparent_power1",#Meter Apparent Power L1" ], #247 VA
    "meter_apparent_power2",#Meter Apparent Power L2" ], #348 VA
    "meter_apparent_power3",#Meter Apparent Power L3" ], #-265 VA
    "meter_apparent_power_total",#Meter Apparent Power Total" ], #861 VA
    "meter_type",#Meter Type" ], #255 
    "meter_sw_version",#Meter Software Version" ], #2407 "
]


"""
"""
_ignore_map = [
    "timestamp",
    "grid_mode",
    "grid_mode_label",
    "grid_in_out",
    "grid_in_out_label",
    "reactive_power",
    "apparent_power",
    "load_mode1",
    "load_mode2",
    "load_mode3",
    "function_bit",
    "warning_code",
    "safety_country",
    "safety_country_label",
    "operation_mode",
    "error_codes",
    "errors",
    "h_total",
    "diagnose_result",
    "diagnose_result_label",
    "battery_bms",
    "battery_index",
    "battery_status",
    "battery_error_l",
    "battery_modules",
    "battery_warning_l",
    "battery_protocol",
    "battery_error_h",
    "battery_error",
    "battery_warning_h",
    "battery_warning",
    "battery_sw_version",
    "battery_hw_version",
    "battery_max_cell_temp_id",
    "battery_min_cell_temp_id",
    "battery_max_cell_voltage_id",
    "battery_min_cell_voltage_id",
    "commode",
    "rssi",
    "manufacture_code",
    "meter_test_status",
    "meter_comm_status",
    "reactive_power_total",
    "meter_power_factor",
    "meter_power_factor1",
    "meter_power_factor2",
    "meter_power_factor3",
    "meter_reactive_power1",
    "meter_reactive_power2",
    "meter_reactive_power3",
    "meter_reactive_power_total",
    "meter_type",
    "meter_sw_version",
]


"""
"""
class Sensor:
    def __init__(self, sensor: GoodWeSensor) -> None:
        self.id = sensor.id_
        self.name = sensor.name
        self.unit = sensor.unit
        self.kind = sensor.kind

    """
    Compare other object for the following types
        - string
        - Sensor
        - goodwe.SensorKind
        - goodwe.Sensor
    """
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, str):
            return self.id == __o
        elif isinstance(__o, Sensor):
            return self.id == __o.id
        elif isinstance(__o, SensorKind):
            return self.kind == __o
        elif isinstance(__o, GoodWeSensor):
            return self.id == __o.id_
        return False


def get(sensors: Tuple[GoodWeSensor, ...], append: List, ignore: List) -> List[Sensor]:
    global _sensor_map, _ignore_map

    # Filter sensor_map list
    result = list(filter(lambda sensor: sensor not in ignore and sensor not in _ignore_map, _sensor_map))

    # Append sensors from "append" list
    result.append(append)

    # Filter sensor list from inverter and map them to Sensor object
    return list(map(
        lambda sensor: Sensor(sensor),
        filter(lambda sensor: sensor.id_ in result, sensors)
    ))


"""
import asyncio

def connect_to_inverter():
    # Set the appropriate IP address
    IP_ADDRESS = "192.168.1.55"

    FAMILY = "ET"  # One of ET, EH, ES, EM, DT, NS, XS, BP or None to detect inverter family automatically
    COMM_ADDR = None  # Usually 0xf7 for ET/EH or 0x7f for DT/D-NS/XS, or None for default value
    TIMEOUT = 5
    RETRIES = 3

    inverter = asyncio.run(goodwe.connect(IP_ADDRESS, COMM_ADDR, FAMILY, TIMEOUT, RETRIES))
    print(
        f"Identified inverter\n"
        f"- Model: {inverter.model_name}\n"
        f"- SerialNr: {inverter.serial_number}\n"
        f"- Version: {inverter.software_version}"
    )

    return inverter

inverter = connect_to_inverter()
s = get(inverter.sensors(), [], [])
print(s)

print(kind_to_string(s[0].kind))
"""

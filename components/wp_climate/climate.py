import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import climate, sensor, binary_sensor, number, select
from esphome.const import CONF_ID, CONF_TYPE

DEPENDENCIES = ["wp_core"]

wp_climate_ns = cg.esphome_ns.namespace("wp_climate")
Heating = wp_climate_ns.class_("Heating", climate.Climate, cg.Component)
HotWater = wp_climate_ns.class_("HotWater", climate.Climate, cg.Component)
PresetClimate = wp_climate_ns.class_("PresetClimate", climate.Climate, cg.Component)

CONF_CURRENT_TEMP = "current_temp"
CONF_TARGET_TEMP = "target_temp"
CONF_HEATING = "heating"
CONF_COOLING = "cooling"
CONF_FAN = "fan"
CONF_TARGET_PROPERTY = "target_property"
CONF_COOL_PROPERTY = "cool_property"
CONF_CURRENT_HUMIDITY = "current_humidity"
CONF_COMFORT_TEMP = "comfort_temp"
CONF_ECO_TEMP = "eco_temp"
CONF_PRESET_SELECT = "preset_select"
CONF_COMFORT_OPTION = "comfort_option"
CONF_ECO_OPTION = "eco_option"
CONF_SETPOINT = "setpoint"
CONF_ALTERNATIVE = "alternative"
CONF_USE_ALTERNATIVE = "use_alternative"
CONF_WRITABLE = "writable"

HEATING_SCHEMA = climate.climate_schema(Heating).extend({
    cv.Required(CONF_CURRENT_TEMP): cv.use_id(sensor.Sensor),
    cv.Required(CONF_TARGET_TEMP): cv.use_id(sensor.Sensor), 
    cv.Required(CONF_HEATING): cv.use_id(binary_sensor.BinarySensor),
    cv.Optional(CONF_COOLING): cv.use_id(binary_sensor.BinarySensor),
    cv.Optional(CONF_FAN): cv.use_id(binary_sensor.BinarySensor),
    cv.Required(CONF_TARGET_PROPERTY): cv.string,
    cv.Optional(CONF_COOL_PROPERTY): cv.string,
}).extend(cv.COMPONENT_SCHEMA)

HOT_WATER_SCHEMA = climate.climate_schema(HotWater).extend({
    cv.Required(CONF_CURRENT_TEMP): cv.use_id(sensor.Sensor),
    cv.Required(CONF_TARGET_TEMP): cv.use_id(sensor.Sensor),
    cv.Required(CONF_HEATING): cv.use_id(binary_sensor.BinarySensor),
    cv.Required(CONF_TARGET_PROPERTY): cv.string,
}).extend(cv.COMPONENT_SCHEMA)

# Thermostat on top of existing entities: the target is the Komfort or Eco number, selected by a preset select.
PRESET_SOURCE_SCHEMA = cv.Schema({
    cv.Required(CONF_COMFORT_TEMP): cv.use_id(number.Number),
    cv.Required(CONF_ECO_TEMP): cv.use_id(number.Number),
    cv.Required(CONF_PRESET_SELECT): cv.use_id(select.Select),
    cv.Optional(CONF_COMFORT_OPTION, default="Komfort"): cv.string,
    cv.Optional(CONF_ECO_OPTION, default="Eco"): cv.string,
})

PRESET_SCHEMA = climate.climate_schema(PresetClimate).extend(PRESET_SOURCE_SCHEMA.schema).extend({
    cv.Required(CONF_CURRENT_TEMP): cv.use_id(sensor.Sensor),
    cv.Optional(CONF_CURRENT_HUMIDITY): cv.use_id(sensor.Sensor),
    cv.Optional(CONF_HEATING): cv.use_id(binary_sensor.BinarySensor),
    cv.Optional(CONF_SETPOINT): cv.use_id(sensor.Sensor),
    cv.Optional(CONF_ALTERNATIVE): PRESET_SOURCE_SCHEMA,
    cv.Optional(CONF_USE_ALTERNATIVE): cv.returning_lambda,
    cv.Optional(CONF_WRITABLE): cv.returning_lambda,
}).extend(cv.COMPONENT_SCHEMA)

CONFIG_SCHEMA = cv.typed_schema({
    "heating": HEATING_SCHEMA,
    "hot_water": HOT_WATER_SCHEMA,
    "preset": PRESET_SCHEMA,
})

async def preset_to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    cg.add(var.set_current_temperature_sensor(await cg.get_variable(config[CONF_CURRENT_TEMP])))
    if CONF_CURRENT_HUMIDITY in config:
        cg.add(var.set_current_humidity_sensor(await cg.get_variable(config[CONF_CURRENT_HUMIDITY])))
    cg.add(var.set_comfort_number(await cg.get_variable(config[CONF_COMFORT_TEMP])))
    cg.add(var.set_eco_number(await cg.get_variable(config[CONF_ECO_TEMP])))
    cg.add(var.set_preset_select(await cg.get_variable(config[CONF_PRESET_SELECT])))
    cg.add(var.set_options(config[CONF_COMFORT_OPTION], config[CONF_ECO_OPTION]))
    if CONF_HEATING in config:
        cg.add(var.set_heating_sensor(await cg.get_variable(config[CONF_HEATING])))
    if CONF_SETPOINT in config:
        cg.add(var.set_setpoint_sensor(await cg.get_variable(config[CONF_SETPOINT])))
    if CONF_ALTERNATIVE in config:
        alt = config[CONF_ALTERNATIVE]
        cg.add(var.set_alternative(
            await cg.get_variable(alt[CONF_PRESET_SELECT]),
            await cg.get_variable(alt[CONF_COMFORT_TEMP]),
            await cg.get_variable(alt[CONF_ECO_TEMP]),
            alt[CONF_COMFORT_OPTION],
            alt[CONF_ECO_OPTION],
        ))
    for key, setter in ((CONF_USE_ALTERNATIVE, var.set_use_alternative), (CONF_WRITABLE, var.set_writable)):
        if key in config:
            cg.add(setter(await cg.process_lambda(config[key], [], return_type=cg.bool_)))
    return var

async def to_code(config):
    if config[CONF_TYPE] == "preset":
        var = await preset_to_code(config)
        await cg.register_component(var, config)
        await climate.register_climate(var, config)
        return

    current_temp = await cg.get_variable(config[CONF_CURRENT_TEMP])
    target_temp = await cg.get_variable(config[CONF_TARGET_TEMP])
    heating_sens = await cg.get_variable(config[CONF_HEATING])
    target_prop = cg.RawExpression(f"Property::{config[CONF_TARGET_PROPERTY]}")

    if config[CONF_TYPE] == "heating":
        has_cool = CONF_COOLING in config
        has_fan = CONF_FAN in config
        
        if has_cool and has_fan and CONF_COOL_PROPERTY in config:
            cool_sens = await cg.get_variable(config[CONF_COOLING])
            fan_sens = await cg.get_variable(config[CONF_FAN])
            cool_prop = cg.RawExpression(f"Property::{config[CONF_COOL_PROPERTY]}")
            var = cg.new_Pvariable(config[CONF_ID], current_temp, target_temp, heating_sens, cool_sens, fan_sens, target_prop, cool_prop)
        elif has_fan and not has_cool:
            fan_sens = await cg.get_variable(config[CONF_FAN])
            var = cg.new_Pvariable(config[CONF_ID], current_temp, target_temp, heating_sens, fan_sens, target_prop)
        else:
            var = cg.new_Pvariable(config[CONF_ID], current_temp, target_temp, heating_sens, target_prop)
    else:
        var = cg.new_Pvariable(config[CONF_ID], current_temp, target_temp, heating_sens, target_prop)

    await cg.register_component(var, config)
    await climate.register_climate(var, config)

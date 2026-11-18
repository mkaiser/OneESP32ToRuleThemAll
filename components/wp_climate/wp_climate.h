#pragma once

#include <functional>
#include <optional>
#include <string>
#include "esphome.h"
#include "esphome/components/climate/climate.h"
#include "esphome/components/wp_core/communication.h"
#include "esphome/components/wp_core/property.h"

namespace esphome {
namespace wp_climate {

class CustomClimate : public Component, public climate::Climate {
   public:
    CustomClimate(esphome::climate::ClimateModeMask modes, esphome::climate::ClimatePresetMask presets,
                  const std::vector<std::pair<const CanNode*, const Property>> targetTemperatureProperties)
        : targetTemperatureProperties_(targetTemperatureProperties) {
        traits_.set_supported_modes(modes);
        traits_.set_supported_presets(presets);
        traits_.add_feature_flags(climate::CLIMATE_SUPPORTS_CURRENT_TEMPERATURE);
        update_mode();
    }

    void setup() override {}

    float get_setup_priority() const override { return esphome::setup_priority::LATE; }

    template <typename Sensor>
    void register_current_temperature_callback(Sensor* current_temperature_sensor) {
        if (current_temperature_sensor != nullptr) {
            current_temperature_sensor->add_on_state_callback([this](float temp) {
                this->current_temperature = temp;
                this->publish_state();
            });
        }
    }

    template <typename Sensor>
    void register_target_temperature_callback(Sensor* target_temperature_sensor) {
        if (target_temperature_sensor != nullptr) {
            target_temperature_sensor->add_on_state_callback([this](float temp) {
                this->target_temperature = temp;
                this->publish_state();
            });
        }
    }

    template <typename BinarySensor>
    void register_heating_callback(BinarySensor* heating_sensor) {
        if (heating_sensor != nullptr) {
            heating_sensor->add_on_state_callback([this](const bool value) {
                this->isHeating = value;
                this->update_mode();
            });
        }
    }

    template <typename BinarySensor>
    void register_cooling_callback(BinarySensor* cooling_sensor) {
        if (cooling_sensor != nullptr) {
            cooling_sensor->add_on_state_callback([this](const bool value) {
                this->isCooling = value;
                this->update_mode();
            });
        }
    }

    template <typename BinarySensor>
    void register_fan_callback(BinarySensor* fan_sensor) {
        if (fan_sensor != nullptr) {
            fan_sensor->add_on_state_callback([this](const bool value) {
                this->fanRunning = value;
                this->update_mode();
            });
        }
    }

    void update_mode() {
        if (isHeating) {
            this->mode = climate::CLIMATE_MODE_HEAT;
        } else if (isCooling) {
            this->mode = climate::CLIMATE_MODE_COOL;
        } else if (fanRunning) {
            this->mode = climate::CLIMATE_MODE_FAN_ONLY;
        } else {
            this->mode = climate::CLIMATE_MODE_OFF;
        }
        this->publish_state();
    }

    void control(const climate::ClimateCall& call) override {
        if (call.get_target_temperature().has_value()) {
            float temp = *call.get_target_temperature();
            this->target_temperature = temp;

            for (const auto& targetTemperatureProperty : targetTemperatureProperties_) {
                queueTransmission(targetTemperatureProperty.first, targetTemperatureProperty.second,
                                  static_cast<std::uint16_t>(temp * 10.0f));
            }
        }
        this->publish_state();
    }

    climate::ClimateTraits traits() override { return traits_; }

   protected:
    climate::ClimateTraits traits_{};

   private:
    const std::vector<std::pair<const CanNode*, const Property>> targetTemperatureProperties_;
    bool isHeating{false};
    bool isCooling{false};
    bool fanRunning{false};
};

class Heating : public CustomClimate {
   public:
    // Full features
    template <typename Sensor, typename BinarySensor>
    Heating(Sensor* current_temperature_sensor, Sensor* target_temperature_sensor, BinarySensor* heating_sensor,
            BinarySensor* cooling_sensor, BinarySensor* fan_sensor, const Property targetHeatingTemperature,
            const Property targetCoolingTemperature)
        : CustomClimate({climate::CLIMATE_MODE_COOL, climate::CLIMATE_MODE_HEAT, climate::CLIMATE_MODE_FAN_ONLY,
                         climate::CLIMATE_MODE_OFF},
                        {climate::CLIMATE_PRESET_NONE, climate::CLIMATE_PRESET_HOME, climate::CLIMATE_PRESET_AWAY},
                        {std::make_pair(CanNode::HK1, targetHeatingTemperature),
                         std::make_pair(CanNode::HK1, targetCoolingTemperature),
                         std::make_pair(CanNode::HK2, targetCoolingTemperature)}) {
        register_current_temperature_callback(current_temperature_sensor);
        register_target_temperature_callback(target_temperature_sensor);
        register_heating_callback(heating_sensor);
        register_cooling_callback(cooling_sensor);
        register_fan_callback(fan_sensor);
    }

    // Heating + Fan
    template <typename Sensor, typename BinarySensor>
    Heating(Sensor* current_temperature_sensor, Sensor* target_temperature_sensor, BinarySensor* heating_sensor,
            BinarySensor* fan_sensor, const Property targetHeatingTemperature)
        : CustomClimate({climate::CLIMATE_MODE_HEAT, climate::CLIMATE_MODE_FAN_ONLY, climate::CLIMATE_MODE_OFF},
                        {climate::CLIMATE_PRESET_NONE, climate::CLIMATE_PRESET_HOME, climate::CLIMATE_PRESET_AWAY},
                        {std::make_pair(CanNode::HK1, targetHeatingTemperature)}) {
        register_current_temperature_callback(current_temperature_sensor);
        register_target_temperature_callback(target_temperature_sensor);
        register_heating_callback(heating_sensor);
        register_fan_callback(fan_sensor);
    }

    // Basic Heating Only
    template <typename Sensor, typename BinarySensor>
    Heating(Sensor* current_temperature_sensor, Sensor* target_temperature_sensor, BinarySensor* heating_sensor,
            const Property targetHeatingTemperature)
        : CustomClimate({climate::CLIMATE_MODE_HEAT, climate::CLIMATE_MODE_OFF},
                        {climate::CLIMATE_PRESET_NONE, climate::CLIMATE_PRESET_HOME, climate::CLIMATE_PRESET_AWAY},
                        {std::make_pair(CanNode::HK1, targetHeatingTemperature)}) {
        register_current_temperature_callback(current_temperature_sensor);
        register_target_temperature_callback(target_temperature_sensor);
        register_heating_callback(heating_sensor);
    }
};

class HotWater : public CustomClimate {
   public:
    template <typename Sensor, typename BinarySensor>
    HotWater(Sensor* current_temperature_sensor, Sensor* target_temperature_sensor, BinarySensor* heating_sensor,
             const Property targetTemperature)
        : CustomClimate({climate::CLIMATE_MODE_HEAT, climate::CLIMATE_MODE_OFF},
                        {climate::CLIMATE_PRESET_COMFORT, climate::CLIMATE_PRESET_ECO, climate::CLIMATE_PRESET_AWAY},
                        {std::make_pair(CanNode::Kessel, targetTemperature)}) {
        register_current_temperature_callback(current_temperature_sensor);
        register_target_temperature_callback(target_temperature_sensor);
        register_heating_callback(heating_sensor);
    }
};

/// Thermostat built from existing entities: presets Komfort/Eco (a select), one temperature number per preset,
/// current temperature/humidity sensors and a "heating" binary sensor. Only the mode HEAT is offered.
/// Any other select option means "no preset": the target is then the optional setpoint sensor and is read only.
/// Optionally a second set of preset select and numbers ("alternative") is used while use_alternative() is true, and
/// changes are refused while writable() is false.
class PresetClimate : public Component, public climate::Climate {
   public:
    void setup() override;
    void dump_config() override;
    float get_setup_priority() const override { return setup_priority::LATE; }

    void set_current_temperature_sensor(sensor::Sensor* sensor) { current_temperature_sensor_ = sensor; }
    void set_current_humidity_sensor(sensor::Sensor* sensor) { current_humidity_sensor_ = sensor; }
    void set_comfort_number(number::Number* number) { comfort_number_ = number; }
    void set_eco_number(number::Number* number) { eco_number_ = number; }
    void set_preset_select(select::Select* select) { preset_select_ = select; }
    void set_options(const std::string& comfort, const std::string& eco) {
        comfort_option_ = comfort;
        eco_option_ = eco;
    }
    void set_heating_sensor(binary_sensor::BinarySensor* sensor) { heating_sensor_ = sensor; }
    void set_setpoint_sensor(sensor::Sensor* sensor) { setpoint_sensor_ = sensor; }
    void set_alternative(select::Select* select, number::Number* comfort, number::Number* eco,
                         const std::string& comfort_option, const std::string& eco_option) {
        alternative_ = Source{select, comfort, eco, comfort_option, eco_option};
    }
    void set_use_alternative(std::function<bool()>&& f) { use_alternative_ = std::move(f); }
    void set_writable(std::function<bool()>&& f) { writable_ = std::move(f); }

   protected:
    /// A preset select with its Komfort/Eco numbers and option names.
    struct Source {
        select::Select* select{nullptr};
        number::Number* comfort{nullptr};
        number::Number* eco{nullptr};
        std::string comfort_option{"Komfort"};
        std::string eco_option{"Eco"};
    };
    enum class Active { COMFORT, ECO, OTHER };

    void control(const climate::ClimateCall& call) override;
    climate::ClimateTraits traits() override;

    /// The source in use: the alternative while use_alternative() is true, else the primary one.
    const Source& source() const;
    bool writable() const { return !writable_ || writable_(); }
    /// Which preset the select shows; OTHER for any other option (or no state yet).
    Active active() const;
    /// The number of the active preset, nullptr for OTHER.
    number::Number* active_number() const;
    /// Reads all source entities and publishes the climate state if something changed.
    void refresh();

    sensor::Sensor* current_temperature_sensor_{nullptr};
    sensor::Sensor* current_humidity_sensor_{nullptr};
    number::Number* comfort_number_{nullptr};
    number::Number* eco_number_{nullptr};
    select::Select* preset_select_{nullptr};
    binary_sensor::BinarySensor* heating_sensor_{nullptr};
    sensor::Sensor* setpoint_sensor_{nullptr};
    std::string comfort_option_{"Komfort"};
    std::string eco_option_{"Eco"};
    Source primary_;  // filled in setup() from the fields above
    std::optional<Source> alternative_;
    std::function<bool()> use_alternative_;
    std::function<bool()> writable_;
};

}  // namespace wp_climate
}  // namespace esphome

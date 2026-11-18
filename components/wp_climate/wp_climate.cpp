#include "wp_climate.h"

#include <cmath>

#include "esphome/core/log.h"

namespace esphome {
namespace wp_climate {

static const char* const TAG = "wp_climate";

void PresetClimate::setup() {
    this->mode = climate::CLIMATE_MODE_HEAT;
    // Generic lambdas: the callback signatures differ between entity types and ESPHome versions.
    const auto refresh = [this](auto&&...) {
        this->refresh();
    };
    this->current_temperature_sensor_->add_on_state_callback(refresh);
    if (this->current_humidity_sensor_ != nullptr) {
        this->current_humidity_sensor_->add_on_state_callback(refresh);
    }
    this->primary_ = Source{this->preset_select_, this->comfort_number_, this->eco_number_, this->comfort_option_,
                            this->eco_option_};
    for (const auto* source : {&this->primary_, this->alternative_ ? &*this->alternative_ : nullptr}) {
        if (source != nullptr) {
            source->comfort->add_on_state_callback(refresh);
            source->eco->add_on_state_callback(refresh);
            source->select->add_on_state_callback(refresh);
        }
    }
    if (this->heating_sensor_ != nullptr) {
        this->heating_sensor_->add_on_state_callback(refresh);
    }
    if (this->setpoint_sensor_ != nullptr) {
        this->setpoint_sensor_->add_on_state_callback(refresh);
    }
    if (this->use_alternative_ || this->writable_) {
        // The conditions have no callbacks: check them regularly (refresh_ publishes only on a change).
        this->set_interval("conditions", 2000, [this]() { this->refresh(); });
    }
    this->refresh();
    this->publish_state();
}

const PresetClimate::Source& PresetClimate::source() const {
    if (this->alternative_ && this->use_alternative_ && this->use_alternative_()) {
        return *this->alternative_;
    }
    return this->primary_;
}

PresetClimate::Active PresetClimate::active() const {
    const auto& source = this->source();
    if (source.select == nullptr || !source.select->has_state()) {
        return Active::OTHER;
    }
    const std::string option(source.select->current_option().c_str());
    if (option == source.comfort_option) {
        return Active::COMFORT;
    }
    if (option == source.eco_option) {
        return Active::ECO;
    }
    return Active::OTHER;
}

number::Number* PresetClimate::active_number() const {
    switch (this->active()) {
        case Active::COMFORT:
            return this->source().comfort;
        case Active::ECO:
            return this->source().eco;
        default:
            return nullptr;
    }
}

void PresetClimate::refresh() {
    bool changed = false;
    const auto update = [&changed](float& field, float value) {
        if (!(std::isnan(field) && std::isnan(value)) && field != value) {
            field = value;
            changed = true;
        }
    };
    update(this->current_temperature, this->current_temperature_sensor_->state);
    if (this->current_humidity_sensor_ != nullptr) {
        update(this->current_humidity, this->current_humidity_sensor_->state);
    }
    const auto active = this->active();
    const auto* number = this->active_number();
    if (number != nullptr) {
        update(this->target_temperature, number->state);
    } else {
        update(this->target_temperature, this->setpoint_sensor_ != nullptr ? this->setpoint_sensor_->state : NAN);
    }

    if (active == Active::OTHER) {
        if (this->preset.has_value()) {
            this->preset.reset();
            changed = true;
        }
    } else {
        const auto preset = active == Active::ECO ? climate::CLIMATE_PRESET_ECO : climate::CLIMATE_PRESET_COMFORT;
        if (!this->preset.has_value() || *this->preset != preset) {
            this->preset = preset;
            changed = true;
        }
    }
    if (this->heating_sensor_ != nullptr) {
        const auto action = (this->heating_sensor_->has_state() && this->heating_sensor_->state)
                                ? climate::CLIMATE_ACTION_HEATING
                                : climate::CLIMATE_ACTION_IDLE;
        if (this->action != action) {
            this->action = action;
            changed = true;
        }
    }
    if (changed) {
        this->publish_state();
    }
}

void PresetClimate::control(const climate::ClimateCall& call) {
    const auto& source = this->source();
    if (!this->writable()) {
        ESP_LOGW(TAG, "Change refused: the thermostat is read only now");
        this->refresh();
        this->publish_state();
        return;
    }
    if (call.get_preset().has_value()) {
        const bool eco = *call.get_preset() == climate::CLIMATE_PRESET_ECO;
        const auto& option = eco ? source.eco_option : source.comfort_option;
        ESP_LOGI(TAG, "Preset -> %s", option.c_str());
        source.select->make_call().set_option(option).perform();
    }
    if (call.get_target_temperature().has_value()) {
        const float value = *call.get_target_temperature();
        auto* number = this->active_number();
        if (number == nullptr) {
            ESP_LOGW(TAG, "Target temperature %.1f refused: preset is neither %s nor %s", value,
                     source.comfort_option.c_str(), source.eco_option.c_str());
        } else {
            ESP_LOGI(TAG, "Target temperature (%s) -> %.1f",
                     this->active() == Active::ECO ? source.eco_option.c_str() : source.comfort_option.c_str(), value);
            number->make_call().set_value(value).perform();
        }
    }
    // Mode: only HEAT is offered, nothing to do.
    this->refresh();
    this->publish_state();
}

climate::ClimateTraits PresetClimate::traits() {
    auto traits = climate::ClimateTraits();
    traits.add_feature_flags(climate::CLIMATE_SUPPORTS_CURRENT_TEMPERATURE);
    if (this->current_humidity_sensor_ != nullptr) {
        traits.add_feature_flags(climate::CLIMATE_SUPPORTS_CURRENT_HUMIDITY);
    }
    if (this->heating_sensor_ != nullptr) {
        traits.add_feature_flags(climate::CLIMATE_SUPPORTS_ACTION);
    }
    traits.set_supported_modes({climate::CLIMATE_MODE_HEAT});
    traits.set_supported_presets({climate::CLIMATE_PRESET_COMFORT, climate::CLIMATE_PRESET_ECO});
    // Range and step of the Komfort number (both numbers share them in practice)
    traits.set_visual_min_temperature(this->comfort_number_->traits.get_min_value());
    traits.set_visual_max_temperature(this->comfort_number_->traits.get_max_value());
    traits.set_visual_target_temperature_step(this->comfort_number_->traits.get_step());
    traits.set_visual_current_temperature_step(0.1f);
    return traits;
}

void PresetClimate::dump_config() {
    LOG_CLIMATE("", "WP Preset Climate", this);
    ESP_LOGCONFIG(TAG, "  Presets: %s / %s", this->comfort_option_.c_str(), this->eco_option_.c_str());
    if (this->alternative_) {
        ESP_LOGCONFIG(TAG, "  Alternative presets: %s / %s", this->alternative_->comfort_option.c_str(),
                      this->alternative_->eco_option.c_str());
    }
}

}  // namespace wp_climate
}  // namespace esphome

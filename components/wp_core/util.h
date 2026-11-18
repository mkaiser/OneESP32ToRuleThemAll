#if !defined(UTIL_H)
#define UTIL_H

#include <string>
#include <unordered_map>
#include <unordered_set>
#include "esphome.h"

/**
 * @brief Synchronizes the time of the heat pump to the one received via Home Assistant time platform.
 */
void syncTime(esphome::time::RealTimeClock* time_obj);

/**
 * @brief Singleton access to whitelisted entities that shall be included in analytics.
 */
std::unordered_set<esphome::EntityBase*>& getWhitelistedEntities();

/**
 * @brief Names under which whitelisted entities are published in analytics (default: the entity name).
 *        Lets a device file with display names publish under the names other devices use.
 */
std::unordered_map<esphome::EntityBase*, std::string>& getAnalyticsNames();

/**
 * @brief Whitelist a set of entities that shall be included in analytics.
 */
template <typename... Args>
void addToWhitelist(Args... args) {
    (getWhitelistedEntities().insert(static_cast<esphome::EntityBase*>(args)), ...);
}

#endif

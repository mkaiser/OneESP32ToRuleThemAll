<!-- Source: header comments of yaml/ttf07.yaml on branch ttf07 (old implementation), copied 2026-11-15 -->
# General notes (Tecalor TTF* [C], (maybe) compatible with Stiebel Eltron WPF* )
# This configuration was created for a TTF07cool heatpump. 
#
# CHANGELOG
# 2026-01-09: Fixed datetime (property targets needs to be WPM2 instead of Kessel for TTF07)
# 
# NOTES
# - The FEK2 needs to be de-attached, because if connected, the FEK2 will take over control of the heatpump and set the target temperatures for
#   HK_SOLL. The heatpump stops controlling things in this case. 
# - My heatpump has an external pump (Heizkreispumpe). This has a constant power consumption of 41W (displayed on the device itself).
#   Set $static_leistung_heizkreispumpe in your heatpump.yaml to the power consumption of your pump, if applicable (else just 0).
# - HA Energy dashboard (>2025.12). Add as "individual devices", the prefix of the sensors might differ (mine is "heatpump_")
#     - Wärmepumpe: 
#         - Device energy consumption: Energie Summe (heatpump_energie_summe)
#         - Device power consumption: Leistung Summe (heatpump_leistung_summe)
#         - Display name: Wärmepumpe
#         - Upstream Device: -
#     - Warmwasser: 
#         - Device energy consumption: El Energieaufnahme Warmwasser (heatpump_el_energieaufnahme_warmwasser)
#         - Device power consumption: Leistung Warmwasserbereitung (heatpump_leistung_warmwasserbereitung)
#         - Display name: Warmwasser
#         - Upstream Device: Wärmepumpe
#     - Heizung: 
#         - Device energy consumption: El Energieaufnahme Heizen (heatpump_el_energieaufnahme_heizen)
#         - Device power consumption: Leistung Heizen (heatpump_leistung_heizen)
#         - Display name: Heizung
#         - Upstream Device: Wärmepumpe
#     - Heizkreispumpe: 
#         - Device energy consumption: Energie ext. Heizkreispumpe (heatpump_energie_ext_heizkreispumpe)
#         - Device power consumption: Leistung ext. Heizkreispumpe (heatpump_leistung_ext_heizkreispumpe)
#         - Display name: Heizkreispumpe
#         - Upstream Device: Heizung
#
# Working
#  - Set 'Betriebszustand' (Komfort, Eco, Warmwasser, Bereitschaft, Notbetrieb)
#  - Set temperatures for heating and hot water (Komfort and Eco modes)
#  - Read many sensors (temperatures, pressures, energy consumption, operation times, status flags, etc.)
#  - Control some settings like Verdichter Stillstand, Pumpenleistung (Heizkreis, Sole, Warmwasser), Reglerdynamik, Steigung HK1, Raumeinfluss
#  - Power and energy readings of the heatpump (heating, hot water, total) and the external heating circuit pump --> HA dashboard compatible
#
# ToDo / open issues
# - Create nice thermostats. Challenge: 
#   There are basically two modes: ECO and Komfort. Each has its own setpoint for heating and hot water. The same for HK1 temperature
#   I usually just have the heatpump in ECO mode and control the ECO temperatures.
#   If we have two thermostats, which can both switch between Eco and komfort, this will affect the other thermostat as well. 
#
# - naming: Is NHZ3 actually NHZ1_2?
# - Kühlen was not tested, yet (its currently winter...)
# - Test transmiting RAUMISTTEMP and RAUMFEUCHTE from HA to heatpump (code is currently commmented)

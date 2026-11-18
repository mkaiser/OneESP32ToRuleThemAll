#!/bin/bash
# 24 h passive CAN capture of heatpump-ttf07c (read-only: ESPHome API logs). Reconnects until END.
OUT=/share/heatpump-capture/2026-11-18-passive-24h.log
END=$(( $(date +%s) + 86400 ))
echo "# Passive capture start $(date '+%F %T %Z'), heatpump-ttf07c, log clock = local CET. Communication lines only." >> $OUT
while [ $(date +%s) -lt $END ]; do
  C=$(docker ps --format '{{.Names}}' | grep -m1 '_esphome$')
  REM=$(( END - $(date +%s) ))
  docker exec $C timeout $REM esphome logs --device 192.168.178.37 /config/esphome/heatpump-ttf07c.yaml 2>&1 \
    | python3 -I -u /share/heatpump-capture/filter.py >> $OUT
  [ $(date +%s) -lt $END ] && { echo "# reconnect $(date '+%F %T')" >> $OUT; sleep 30; }
done
echo "# Passive capture end $(date '+%F %T %Z')" >> $OUT

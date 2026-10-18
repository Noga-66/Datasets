#!/usr/bin/env bash
# يولّد ملف passwd لليوزرات.  الاستخدام: bash infra/mosquitto/make_passwd.sh
set -e
cd "$(dirname "$0")"; : > passwd
for u in bridge esp32_water_01 esp32_smoke_01 simulator; do
  read -rsp "password for $u: " p; echo
  docker run --rm -v "$PWD":/c eclipse-mosquitto:2 mosquitto_passwd -b /c/passwd "$u" "$p"
done

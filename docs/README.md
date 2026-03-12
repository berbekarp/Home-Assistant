# 🍄 Home Assistant Mushroom cards

Különböző kártyák érhetők el különböző entitások számára:

- 🔋 [Battery card](cards/battery.md)
- 💡 [Light card](cards/light.md)
- 🚪 [Door/Window Lock sensor card](cards/door_window_lock_sensor.md)
- 🌊 [Water sensor card](cards/water_sensor.md)

## 🐍⚙️ Python Szkriptek és Kiegészítők

Ez a repó egyedi Python szkripteket és javításokat (quirk) is tartalmaz az okosotthon rendszerhez, tematikusan mappákba rendezve:

### 📂 Geekworm-x1200
* **`x1200_mqtt.py`**: Ez a szkript a Geekworm X1200 (Raspberry Pi szünetmentes tápegység / UPS pajzs) felügyeletére szolgál. Kiolvassa az eszköz állapotát (pl. akkumulátor töltöttségi szintje, feszültség, hálózati áram állapota), és MQTT protokollon keresztül továbbítja ezeket az adatokat. Így a hardver információi szenzorként jelennek meg a Home Assistantban.
  * 📖 **[Részletes beállítási útmutató a Wikiben](https://github.com/berbekarp/Home-Assistant/wiki/Geekworm-x1200)**

### 📂 Zigbee
* **`snzb01m.py`**: Egyedi ZHA Quirk (javítófájl) a Sonoff SNZB-01M (Orb 4-in-1) vezeték nélküli okosgombhoz. Mivel a Home Assistant beépített ZHA integrációja alapértelmezetten nem értelmezi tökéletesen az eszköz egyedi adatcsatornáját (a 4-es gomb például egyáltalán nem működik nélküle), ez a fájl "fordítóként" funkcionál. Biztosítja, hogy mind a 4 fizikai gomb megbízhatóan, a megfelelő eseményekkel (pl. `remote_button_short_press`) működjön a rendszerben.
  * 📖 **[Részletes beállítási útmutató a Wikiben](https://github.com/berbekarp/Home-Assistant/wiki/Sonoff-SNZB-01M)**
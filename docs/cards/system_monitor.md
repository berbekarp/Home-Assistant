# 🍓 Raspberry Pi 5 Rendszerfelügyelet (System Monitor)

Ez a dokumentáció egy letisztult, animált fejléc-kártyát (Heading Card) mutat be, amely jelvények (badges) formájában jeleníti meg a Raspberry Pi 5 szerver legfontosabb hardveres adatait: a processzor hőmérsékletét, a CPU és memória használatát, valamint a lemezterület foglaltságát. 

A kártya érdekessége a `card-mod` segítségével lüktető (szívdobogás animációt végző), eredeti Málna-piros színű Raspberry Pi ikon. A kártyára kattintva a rendszer egy részletesebb `/system-monitor` aloldalra navigál.

## ⚠️ Előfeltételek a működéshez

### 1. Home Assistant Integrációk
* **System Monitor (Rendszerfigyelő):** A Home Assistant beépített integrációja. 
  * *Beállítás:* Beállítások -> Eszközök és szolgáltatások -> Integráció hozzáadása -> keresd meg a **System Monitor**-t, és add hozzá. Ez hozza létre a `sensor.system_monitor_...` entitásokat.
* **Card-mod (HACS):** Az ikon színének módosításához és a lüktető animációhoz szükséges.

### 2. Linux / Docker szintű beállítások (Fontos!)
Mivel a Home Assistant Docker konténerben fut az Ubuntun, alapértelmezetten a konténer a *saját* elszigetelt környezetét látja, nem pedig a teljes Raspberry Pi hardvert. Hogy a CPU hőmérséklet és a valós lemezhasználat megjelenjen, a `compose.yaml` fájlban a Home Assistant konténernek olvasási jogot kell adni a gazdagép (Host) bizonyos rendszerfájljaihoz.
*(Ha a szenzorok "Unknown" vagy "Unavailable" állapotúak, ellenőrizd, hogy a `compose.yaml` tartalmazza-e az alábbi volume csatolásokat:)*
```yaml
    volumes:
      # ... a config mappád csatolása ...
      - /sys/class/thermal/thermal_zone0/temp:/sys/class/thermal/thermal_zone0/temp:ro # CPU Hőfokhoz
      - /:/hostfs:ro # A teljes lemezterület olvasásához

```

---

## Előnézet

*(Ide feltölthetsz egy képet a dashboardod fejlécéről)*

A System Monitor integráció részletes nézete (amely a gazdagép minden paraméterét mutatja):

---

## YAML Konfiguráció

Ezt a kártyát a Dashboardodon egy új **Kézi (Manual)** kártyaként tudod hozzáadni. Ideális a nézet legtetejére vagy egy "Szerver állapot" szekció címeként.

```yaml
type: heading
heading: System
heading_style: title
icon: mdi:raspberry-pi
theme: Graphite
card_mod:
  style: |
    ha-icon {
      color: #E30B5C !important; /* Eredeti Raspberry Pi piros szín */
      animation: heartbeat 3s infinite;
    }
    @keyframes heartbeat {
      0% { transform: scale(1); }
      10% { transform: scale(1.15); }
      20% { transform: scale(1); }
      30% { transform: scale(1.15); }
      40% { transform: scale(1); }
      100% { transform: scale(1); }
    }
badges:
  - type: entity
    show_state: true
    show_icon: true
    entity: sensor.system_monitor_processzor_homerseklet
    tap_action:
      action: more-info
  - type: entity
    show_state: true
    show_icon: true
    color: red
    entity: sensor.system_monitor_processzor_hasznalat
    tap_action:
      action: more-info
  - type: entity
    show_state: true
    show_icon: true
    color: accent
    entity: sensor.system_monitor_memoriahasznalat
    tap_action:
      action: more-info
  - type: entity
    show_state: true
    show_icon: true
    color: blue
    entity: sensor.system_monitor_lemezhasznalat
    tap_action:
      action: more-info
tap_action:
  action: navigate
  navigation_path: /system-monitor

```

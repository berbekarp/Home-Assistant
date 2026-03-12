```markdown
# Sonoff SNZB-01M (Orb) beállítása Home Assistant ZHA alatt

A Sonoff SNZB-01M (más néven Sonoff Orb 4-in-1) egy kiváló vezeték nélküli Zigbee okosgomb. Azonban a Home Assistant beépített ZHA (Zigbee Home Automation) integrációjával használva "dobozból kivéve" problémák adódhatnak:
* A 4. gomb egyáltalán nem regisztrál eseményeket (`zha_event`).
* Az 1-3. gombok furcsa, nem szabványos parancsokat küldenek (`on/off`, `step`).

Ennek oka, hogy a Sonoff egy egyedi adatcsatornát (FC12 cluster) használ, amit a ZHA alapból nem tud tökéletesen értelmezni. Ez a dokumentáció bemutatja, hogyan lehet egy **Custom Quirk** (javítófájl) segítségével mind a 4 gombot 100%-osan működésre bírni.

## Előfeltételek
* Működő Home Assistant példány (akár Docker alatt, akár HA OS-ként).
* Beállított ZHA integráció.
* Valamilyen fájlkezelő kiegészítő (pl. **File editor** vagy **Studio Code Server**).

---

## 1. Custom Quirk (javítófájl) engedélyezése

Először meg kell mondanunk a Home Assistantnak, hogy töltse be az egyedi eszköz-definíciókat.

1. Nyisd meg a `configuration.yaml` fájlt a Home Assistant főkönyvtárában.
2. Add hozzá az alábbi sorokat:

```yaml
zha:
  enable_quirks: true
  custom_quirks_path: custom_zha_quirks

```

> **⚠️ Fontos megjegyzés Docker felhasználóknak:** Kifejezetten ajánlott a fenti **relatív útvonal** (`custom_zha_quirks`) használata a teljes (abszolút) útvonal helyett. Így a Home Assistant a konténeren belül automatikusan a `configuration.yaml` melletti mappában fogja keresni a fájlokat, elkerülve a mappafelfűzési (bind mount) anomáliákat.

## 2. A Quirk letöltése és telepítése

1. Hozz létre egy új mappát pontosan `custom_zha_quirks` néven a `configuration.yaml` fájl mellett (általában a `/config` vagy a befűzött host könyvtár).
2. Ezen a mappán belül hozz létre egy üres fájlt `snzb01m.py` néven.
3. Töltsd le a javítókódot, (https://raw.githubusercontent.com/Oniums/zha-device-handlers/dev/zhaquirks/sonoff/snzb01m.py)).*
4. Mentsd el a fájlt.
5. **Indítsd újra a Home Assistantot!** (Fejlesztői eszközök -> Újraindítás).

## 3. Az eszköz (újra)párosítása

Ahhoz, hogy a ZHA az új fájl alapján ismerje fel az eszközt, újra kell párosítani.

1. Menj a **Beállítások -> Eszközök és szolgáltatások -> Eszközök** menübe.
2. Keresd meg a Sonoff SNZB-01M gombot, és az eszköz adatlapján válaszd a **Törlés** lehetőséget.
3. Vidd a gombot közel a Zigbee koordinátorhoz.
4. Tedd az eszközt párosító módba.
5. Add hozzá új eszközként a ZHA integrációban.

**Ellenőrzés:** Az eszköz adatlapján a *Zigbee info* lenyíló fül alatt a **Quirk** sornál már nem egy "Generic" feliratnak kell lennie, hanem a betöltött fájlra/osztályra utaló névnek.

---

## 4. Automatizálások beállítása

A javítás telepítése után az eszköz már logikus, ember által is olvasható eseményeket küld (pl. `remote_button_short_press`).

### Események (zha_event) kinyerése

1. Menj a **Fejlesztői eszközök -> Események** menüpontba.
2. A "Figyelt esemény" (Event to subscribe to) mezőbe írd be: `zha_event`.
3. Kattints a **Figyelés indítása** gombra, majd nyomd meg az egyik gombot a Sonoff távirányítón.
4. A megjelenő JSON kódból másold ki a `device_id` értékét.

### Példa automatizálás (Világítás váltása / Toggle)

Az alábbi YAML kód egy példa arra, hogyan kapcsolhatunk fel/le egy izzót a **4-es gomb rövid megnyomásával**.

```yaml
alias: "Nappali: 4-es gomb - Lámpa kapcsolása"
description: "A Sonoff SNZB-01M 4-es gombjának megnyomásakor a lámpa állapotot vált."
mode: single
triggers:
  - trigger: event
    event_type: zha_event
    event_data:
      device_id: IDE_JON_A_TE_ESZKOZOD_AZONOSITOJA # Cseréld ki a saját device_id-dre!
      command: remote_button_short_press
      endpoint_id: 4 # Ez jelöli a fizikai gomb sorszámát (1, 2, 3 vagy 4)
conditions: []
actions:
  - action: light.toggle
    metadata: {}
    target:
      entity_id: light.A_TE_LAMPAD_NEVE # Cseréld ki a vezérelni kívánt entitásra
    data:
      color_temp_kelvin: 6500
      brightness_pct: 100

```

*Tipp: A többi gombhoz használd ugyanezt az alapot, csak változtasd meg az `endpoint_id` értékét a megfelelő gomb sorszámára (1-4), illetve igény szerint a `command` értékét (pl. `remote_button_double_press`).*

```

***

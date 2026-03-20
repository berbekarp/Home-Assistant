# 📈 Valuta Árfolyamok Dashboard (MNB)

Ez a dokumentáció bemutatja, hogyan hozhatsz létre egy letisztult, "bróker" stílusú árfolyamfigyelő kártyát a Home Assistantben. A kártya a felső részén a pontos aktuális értékeket (Euro és USD) mutatja, alatta pedig egy 1 hetes (vagy tetszőlegesen beállítható) közös, színátmenetes grafikonon ábrázolja a két deviza trendjét.

---

## ⚠️ Előfeltételek

A kártya működéséhez szükséges a megfelelő adatforrás és néhány vizuális kiegészítő.

### 1. HACS (Home Assistant Community Store) Kártyák
* **[Mini Graph Card](https://github.com/kalkih/mini-graph-card)**: Az alsó trendvonalak és a grafikon megrajzolásához.
* **[Vertical Stack In Card](https://github.com/ofekasass/vertical-stack-in-card)**: Az értékek és a grafikon keret nélküli, zökkenőmentes egybeolvasztásához.
* **[Card-mod](https://github.com/thomasloven/lovelace-card-mod)**: A kártya hátterének és a felesleges keretek eltüntetéséhez.

### 2. Adatforrás: MNB Integráció telepítése
Ahhoz, hogy a hivatalos középárfolyamokat lásd, a Magyar Nemzeti Bank (MNB) integrációjára lesz szükséged.

1. Lépj be a **HACS** -> **Integrációk** (Integrations) menübe.
2. Keress rá a **Magyar Nemzeti Bank (MNB)** integrációra, és töltsd le. *(Ha nem találod alapból, előfordulhat, hogy [Custom Repositoryként](https://github.com/dgyurics/homeassistant-mnb) kell hozzáadnod a HACS-hez).*
3. Indítsd újra a Home Assistantot.
4. Menj a **Beállítások** -> **Eszközök és szolgáltatások** -> **Integrációk hozzáadása** menübe.
5. Keress rá az MNB integrációra, és add hozzá a rendszeredhez.

### 3. Az EUR és USD szenzorok felvétele
Amikor az MNB integrációt konfigurálod, a rendszer megkérdezi, hogy milyen devizákat szeretnél követni.
1. A listából válaszd ki az **EUR** és az **USD** opciókat.
2. Ezzel a rendszer automatikusan létrehozza a `sensor.mnb_eur` és `sensor.mnb_usd` entitásokat, amiket a kártya használni fog.

---

## 💻 A Kártya Kódja

Hozz létre egy új, Kézi (Manual) kártyát a dashboardodon, és másold be az alábbi kódot. 

> **Tipp:** Az 1 hetes grafikonhoz a `hours_to_show: 168` értéket használtuk (7 nap * 24 óra). Ha inkább egy havi (30 napos) trendet szeretnél látni, írd át ezt az értéket `720`-ra!

```yaml
type: custom:vertical-stack-in-card
card_mod:
  style: |
    ha-card {
      border-radius: 12px;
      background-color: #1a1a1a;
    }
cards:
  # --- FELSŐ RÉSZ: Pontos értékek listája ---
  - type: entities
    title: Árfolyamok
    entities:
      - entity: sensor.mnb_eur
        name: Euro / Ft.
        icon: mdi:currency-eur
      - entity: sensor.mnb_usd
        name: USD / Ft.
        icon: mdi:currency-usd
    card_mod:
      style: |
        ha-card {
          background: transparent !important;
          box-shadow: none !important;
          border: none !important;
        }

  # --- ALSÓ RÉSZ: Közös Grafikon ---
  - type: custom:mini-graph-card
    entities:
      - entity: sensor.mnb_eur
        name: EUR
        color: '#3498db' # Kék szín az Eurónak
      - entity: sensor.mnb_usd
        name: USD
        color: '#2ecc71' # Zöld szín a Dollárnak
    hours_to_show: 168 # 1 hetes visszatekintés
    points_per_hour: 0.5 # 2 óránként 1 adatpont elég az árfolyamhoz
    line_width: 3
    show:
      name: false      # A nevet már fent kiírtuk
      icon: false      # Ikont is
      state: false     # Az aktuális értéket is
      legend: true     # A kis jelmagyarázat (EUR/USD) maradjon alul!
      fill: fade       # Szép színátmenetes kitöltés a vonal alatt
    card_mod:
      style: |
        ha-card {
          background: transparent !important;
          box-shadow: none !important;
          border: none !important;
          margin-top: -10px !important;
        }
````
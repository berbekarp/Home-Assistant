# 🌡️ Fűtés Vezérlés (Bubble Card Pop-up Rendszer)

Ez a dokumentáció egy komplett, több helyiséget átfogó fűtésvezérlő felületet mutat be. A rendszer egy elegáns, vízszintes gombsorból áll, amelyből a gombokra kattintva gyönyörűen animált felugró ablakok (pop-upok) nyílnak meg az adott szoba részletes termosztátjával és fűtési grafikonjaival.

## ⚠️ Előfeltételek a működéshez

A rendszer felépítéséhez az alábbi **HACS (Home Assistant Community Store)** kártyák és integrációk szükségesek:
1. **[Bubble Card](https://github.com/Clooos/Bubble-Card):** Ez felel a gombsorért és a pop-up ablakok működéséért.
2. **[Simple Thermostat](https://github.com/nervetattoos/simple-thermostat):** Letisztult, minimalista termosztát kártya a radiátorok vezérléséhez.
3. **[ApexCharts Card](https://github.com/RomRider/apexcharts-card):** A részletes, interaktív hőmérséklet- és fűtéstörténeti grafikonok megjelenítéséhez.
4. *(Opcionális)* **Custom Icons:** A kódban használt `phu:` (Philips Hue) ikonok megjelenítéséhez szükséges lehet egy egyedi ikoncsomag telepítése.

---

## 1. Főmenü (Vízszintes Gombsor)

Ez a kártya kerüljön a dashboardod látható részére (pl. a fűtés szekció tetejére). Ez tartalmazza a gombokat, amelyek meghívják a rejtett pop-up ablakokat a hash linkek (`#bedroom`, `#childroom`, `#livingroom`) segítségével. A CSS formázásnak köszönhetően a gombok átlátszó hátteret kapnak és balra igazodnak.

```yaml
type: custom:bubble-card
card_type: horizontal-buttons-stack
1_link: "#bedroom"
1_name: Hálószoba
1_icon: phu:thermostat-v2
2_link: "#childroom"
2_name: Gyerekszoba
2_icon: phu:thermostat-v2
3_link: "#livingroom"
3_name: Nappali
3_icon: phu:thermostat-v2
styles: |
  .bubble-horizontal-buttons-stack {
    background: none !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
  }
  .bubble-button-container {
    justify-content: flex-start; /* Középre igazításhoz használd a 'center' értéket */
    gap: 8px; /* A gombok közötti távolság */
  }

```

---

## 2. Felugró Ablakok (Pop-up Kártyák)

> **🚨 NAGYON FONTOS SZABÁLY:** > A Bubble Card pop-up logikája miatt az alábbi három `vertical-stack` kártyát a Home Assistant szerkesztőjében **szigorúan a nézet (View) legeslegutolsó pozíciójára kell helyezni!** Ha nem legalul vannak, elcsúszhat az elrendezésed! A felületen amúgy sem fognak látszani, csak akkor, ha a fenti gombokkal meghívod őket.

### 🛏️ Hálószoba Pop-up (`#bedroom`)

```yaml
type: vertical-stack
title: Hálószoba radiátor
cards:
  - type: custom:bubble-card
    card_type: pop-up
    hash: '#bedroom'
    show_header: true
    name: Hálószoba radiátor
    icon: phu:rooms-bedroom
    auto_close: '15000'
    force_icon: false
    show_name: true
    show_icon: true
    scrolling_effect: true
    show_last_changed: false
    show_attribute: false
    show_state: false
    use_accent_color: false
    trigger: []
    button_type: name
    sub_button:
      main: []
      bottom: []
  - type: grid
    square: false
    columns: 1
    cards:
      - type: thermostat
        entity: climate.fibaro_bedroom_valve
      - type: custom:simple-thermostat
        header: false
        layout:
          mode:
            headings: false
        entity: climate.fibaro_bedroom_valve
      - type: custom:apexcharts-card
        header:
          show: true
          title: Hálószoba Fűtés
          show_states: true
          colorize_states: true
        graph_span: 48h
        yaxis:
          - id: temp
            show: true
            decimals: 1
          - id: heat
            show: false
            min: 0
            max: 100
        series:
          - entity: climate.fibaro_bedroom_valve
            attribute: current_temperature
            name: Hőmérséklet
            type: line
            stroke_width: 3
            color: '#00b4d8'
            curve: smooth
            yaxis_id: temp
            group_by:
              func: last
              duration: 10min
          - entity: climate.fibaro_bedroom_valve
            attribute: temperature
            name: Célhőfok
            type: line
            stroke_width: 2
            color: '#ff9f1c'
            curve: stepline
            yaxis_id: temp
          - entity: sensor.haloszoba_radiator_muvelet
            name: Fűtés aktív
            type: area
            color: '#ff9f1c'
            opacity: 0.2
            stroke_width: 0
            yaxis_id: heat
            curve: stepline
            show:
              legend_value: false

```

### 🧸 Gyerekszoba Pop-up (`#childroom`)

```yaml
type: vertical-stack
title: Gyerekszoba radiátor
cards:
  - type: custom:bubble-card
    card_type: pop-up
    hash: '#childroom'
    show_header: true
    name: Gyerekszoba radiátor
    icon: phu:rooms-bedroom
    auto_close: '15000'
    force_icon: false
    show_name: true
    show_icon: true
    scrolling_effect: true
    show_last_changed: false
    show_attribute: false
    show_state: false
    use_accent_color: false
    trigger: []
  - type: grid
    square: false
    columns: 1
    cards:
      - type: thermostat
        entity: climate.fibaro_childroom_valve
      - type: custom:simple-thermostat
        entity: climate.fibaro_childroom_valve
        header: false
        layout:
          mode:
            headings: false
      - type: custom:apexcharts-card
        header:
          show: true
          title: Gyerekszoba Fűtés
          show_states: true
          colorize_states: true
        graph_span: 48h
        yaxis:
          - id: temp
            show: true
            decimals: 1
          - id: heat
            show: false
            min: 0
            max: 100
        series:
          - entity: climate.fibaro_childroom_valve
            attribute: current_temperature
            name: Hőmérséklet
            type: line
            stroke_width: 3
            color: '#00b4d8'
            curve: smooth
            yaxis_id: temp
            group_by:
              func: last
              duration: 10min
          - entity: climate.fibaro_childroom_valve
            attribute: temperature
            name: Célhőfok
            type: line
            stroke_width: 2
            color: '#ff9f1c'
            curve: stepline
            yaxis_id: temp
          - entity: sensor.gyerekszoba_radiator_muvelet
            name: Fűtés aktív
            type: area
            color: orange
            opacity: 0.2
            stroke_width: 0
            yaxis_id: heat
            curve: stepline
            show:
              legend_value: false

```

### 🛋️ Nappali Pop-up (`#livingroom`)

```yaml
type: vertical-stack
title: Nappali radiátor
cards:
  - type: custom:bubble-card
    card_type: pop-up
    hash: '#livingroom'
    show_header: true
    name: Nappali radiátor
    icon: phu:rooms-bedroom
    auto_close: '15000'
    force_icon: false
    show_name: true
    show_icon: true
    scrolling_effect: true
    show_last_changed: false
    show_attribute: false
    show_state: false
    use_accent_color: false
    trigger: []
    button_type: name
    sub_button:
      main: []
      bottom: []
  - type: grid
    square: false
    columns: 1
    cards:
      - type: thermostat
        entity: climate.fibaro_livingroom_valve
      - type: custom:simple-thermostat
        header: false
        layout:
          mode:
            headings: false
        entity: climate.fibaro_livingroom_valve
      - type: custom:apexcharts-card
        header:
          show: true
          title: Nappali Fűtés
          show_states: true
          colorize_states: true
        graph_span: 48h
        yaxis:
          - id: temp
            show: true
            decimals: 1
          - id: heat
            show: false
            min: 0
            max: 100
        series:
          - entity: climate.fibaro_livingroom_valve
            attribute: current_temperature
            name: Hőmérséklet
            type: line
            stroke_width: 3
            color: '#00b4d8'
            curve: smooth
            yaxis_id: temp
            group_by:
              func: last
              duration: 10min
          - entity: climate.fibaro_livingroom_valve
            attribute: temperature
            name: Célhőfok
            type: line
            stroke_width: 2
            color: '#ff9f1c'
            curve: stepline
            yaxis_id: temp
          - entity: sensor.nappali_radiator_muvelet
            name: Fűtés aktív
            type: area
            color: '#ff9f1c'
            opacity: 0.2
            stroke_width: 0
            yaxis_id: heat
            curve: stepline
            show:
              legend_value: false

```

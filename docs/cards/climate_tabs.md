# 🌡️ Hőmérséklet és Páratartalom Dashboard (Fülekkel)

Ez a dokumentáció egy prémium, "System Monitor" stílusú, helyiségekre bontott klíma (hőmérséklet és páratartalom) dashboard kártyát mutat be. A kártya különlegessége a kiemelkedő vizuális visszajelzés: az ikonok a mért értékektől függően dinamikusan változtatják a színüket és a pulzálásuk/hullámzásuk sebességét (pl. a hideg kék, a meleg piros, a száraz levegő lüktet, a normál szépen lélegzik). 

Mindez elegánsan egybe van olvasztva a 24 órás múltbeli adatokat mutató mini-grafikonokkal és a szegmentált akkumulátor kijelzéssel. A kód **YAML Horgonyokat (Anchors)** használ, így a komplex CSS animációkat csak egyszer kell definiálni, a többi szoba pedig automatikusan örökli azokat.

---

## 🎥 Előnézet

Így néz ki a helyiségekre bontott klíma panel:

*(A kártya animációi, a lüktető ikonok és az átlátszó grafikonok működés közben:)*

![Klíma Animáció](../images/climate_tabs.gif)

---

## ⚠️ Előfeltételek

A kártya működéséhez szükségesek az alábbi vizuális kiegészítők:

### 1. HACS (Home Assistant Community Store) Kártyák
* **[Mushroom Cards](https://github.com/piitaya/lovelace-mushroom)**: Az alap kártyákhoz és a navigációs gombokhoz.
* **[Mini Graph Card](https://github.com/kalkih/mini-graph-card)**: Az átlátszó, színváltós grafikonokhoz.
* **[Vertical Stack In Card](https://github.com/ofekasass/vertical-stack-in-card)**: A kártyák és grafikonok keret nélküli, zökkenőmentes egybeolvasztásához.
* **[Card-mod](https://github.com/thomasloven/lovelace-card-mod)**: A dinamikus szín- és pulzáló CSS animációkhoz elengedhetetlen!

### 2. Segédentitás (Helper) a váltáshoz
A helyiségek közötti léptetéshez hozz létre egy Szám (Number) segédentitást:
* **Név:** `tabs_homerseklet` (Azonosító: `input_number.tabs_homerseklet`)
* **Minimum:** 1 | **Maximum:** 6 | **Lépésköz:** 1

---

## 💻 A Teljes Dashboard Kódja

Hozz létre egy új, üres kártyát (Kézi / Manual) a dashboardodon, és másold be az alábbi kódot. 

*(Figyelem: Az entitás neveket cseréld le a saját hőmérséklet, páratartalom és akkumulátor szenzoraidra! Az első szoba (Fürdőszoba) tartalmazza a CSS horgonyokat (`&temp_style`, `&hum_style`, `&graph_style`, `&battery_style`), a többi szoba pedig csak hivatkozik rájuk (`*temp_style`, stb.), így a kód tiszta és könnyen karbantartható marad.)*

```yaml
type: custom:vertical-stack-in-card
cards:
  # ==========================================
  # FEJLÉC
  # ==========================================
  - type: custom:mushroom-template-card
    primary: Hőmérséklet
    icon: mdi:temperature-celsius
    color: "#E30B5C"
    features_position: bottom
    grid_options:
      columns: 12
      rows: 1
    card_mod:
      style: |
        ha-state-icon {
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

  # ==========================================
  # NAVIGÁCIÓS GOMBOK (TABS)
  # ==========================================
  - type: custom:mushroom-chips-card
    alignment: center
    card_mod:
      style: |
        ha-card { margin-bottom: 12px; }
        .chip-container { flex-wrap: wrap !important; justify-content: center !important; }
    chips:
      - type: template
        icon: mdi:temperature-celsius
        content: Fürdőszoba
        tap_action: { action: perform-action, perform_action: input_number.set_value, target: { entity_id: input_number.tabs_homerseklet }, data: { value: 1 } }
        card_mod:
          style: |
            ha-card { min-width: 140px !important; max-width: 140px !important; background-color: {{ '#E30B5C' if is_state('input_number.tabs_homerseklet', '1.0') else '#2C3E50' }} !important; position: relative !important; }
            .content { justify-content: center !important; }
            ha-state-icon { position: absolute !important; left: 12px !important; color: {{ '#1A1A1A' if is_state('input_number.tabs_homerseklet', '1.0') else '#FFFFFF' }} !important; animation: pulse 2s infinite ease-in-out !important; }
            span { color: {{ '#1A1A1A' if is_state('input_number.tabs_homerseklet', '1.0') else '#FFFFFF' }} !important; font-weight: {{ 'bold' if is_state('input_number.tabs_homerseklet', '1.0') else '500' }} !important; padding-left: 15px !important; }
            @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.3); } 100% { transform: scale(1); } }
      - type: template
        icon: mdi:temperature-celsius
        content: Előszoba
        tap_action: { action: perform-action, perform_action: input_number.set_value, target: { entity_id: input_number.tabs_homerseklet }, data: { value: 2 } }
        card_mod:
          style: |
            ha-card { min-width: 140px !important; max-width: 140px !important; background-color: {{ '#E30B5C' if is_state('input_number.tabs_homerseklet', '2.0') else '#2C3E50' }} !important; position: relative !important; }
            .content { justify-content: center !important; }
            ha-state-icon { position: absolute !important; left: 12px !important; color: {{ '#1A1A1A' if is_state('input_number.tabs_homerseklet', '2.0') else '#FFFFFF' }} !important; animation: pulse 2s infinite ease-in-out !important; }
            span { color: {{ '#1A1A1A' if is_state('input_number.tabs_homerseklet', '2.0') else '#FFFFFF' }} !important; font-weight: {{ 'bold' if is_state('input_number.tabs_homerseklet', '2.0') else '500' }} !important; padding-left: 15px !important; }
            @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.3); } 100% { transform: scale(1); } }
      - type: template
        icon: mdi:temperature-celsius
        content: Konyha
        tap_action: { action: perform-action, perform_action: input_number.set_value, target: { entity_id: input_number.tabs_homerseklet }, data: { value: 3 } }
        card_mod:
          style: |
            ha-card { min-width: 140px !important; max-width: 140px !important; background-color: {{ '#E30B5C' if is_state('input_number.tabs_homerseklet', '3.0') else '#2C3E50' }} !important; position: relative !important; }
            .content { justify-content: center !important; }
            ha-state-icon { position: absolute !important; left: 12px !important; color: {{ '#1A1A1A' if is_state('input_number.tabs_homerseklet', '3.0') else '#FFFFFF' }} !important; animation: pulse 2s infinite ease-in-out !important; }
            span { color: {{ '#1A1A1A' if is_state('input_number.tabs_homerseklet', '3.0') else '#FFFFFF' }} !important; font-weight: {{ 'bold' if is_state('input_number.tabs_homerseklet', '3.0') else '500' }} !important; padding-left: 15px !important; }
            @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.3); } 100% { transform: scale(1); } }
      - type: template
        icon: mdi:temperature-celsius
        content: Nappali
        tap_action: { action: perform-action, perform_action: input_number.set_value, target: { entity_id: input_number.tabs_homerseklet }, data: { value: 4 } }
        card_mod:
          style: |
            ha-card { min-width: 140px !important; max-width: 140px !important; background-color: {{ '#E30B5C' if is_state('input_number.tabs_homerseklet', '4.0') else '#2C3E50' }} !important; position: relative !important; }
            .content { justify-content: center !important; }
            ha-state-icon { position: absolute !important; left: 12px !important; color: {{ '#1A1A1A' if is_state('input_number.tabs_homerseklet', '4.0') else '#FFFFFF' }} !important; animation: pulse 2s infinite ease-in-out !important; }
            span { color: {{ '#1A1A1A' if is_state('input_number.tabs_homerseklet', '4.0') else '#FFFFFF' }} !important; font-weight: {{ 'bold' if is_state('input_number.tabs_homerseklet', '4.0') else '500' }} !important; padding-left: 15px !important; }
            @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.3); } 100% { transform: scale(1); } }
      - type: template
        icon: mdi:temperature-celsius
        content: Hálószoba
        tap_action: { action: perform-action, perform_action: input_number.set_value, target: { entity_id: input_number.tabs_homerseklet }, data: { value: 5 } }
        card_mod:
          style: |
            ha-card { min-width: 140px !important; max-width: 140px !important; background-color: {{ '#E30B5C' if is_state('input_number.tabs_homerseklet', '5.0') else '#2C3E50' }} !important; position: relative !important; }
            .content { justify-content: center !important; }
            ha-state-icon { position: absolute !important; left: 12px !important; color: {{ '#1A1A1A' if is_state('input_number.tabs_homerseklet', '5.0') else '#FFFFFF' }} !important; animation: pulse 2s infinite ease-in-out !important; }
            span { color: {{ '#1A1A1A' if is_state('input_number.tabs_homerseklet', '5.0') else '#FFFFFF' }} !important; font-weight: {{ 'bold' if is_state('input_number.tabs_homerseklet', '5.0') else '500' }} !important; padding-left: 15px !important; }
            @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.3); } 100% { transform: scale(1); } }
      - type: template
        icon: mdi:temperature-celsius
        content: Gyerekszoba
        tap_action: { action: perform-action, perform_action: input_number.set_value, target: { entity_id: input_number.tabs_homerseklet }, data: { value: 6 } }
        card_mod:
          style: |
            ha-card { min-width: 140px !important; max-width: 140px !important; background-color: {{ '#E30B5C' if is_state('input_number.tabs_homerseklet', '6.0') else '#2C3E50' }} !important; position: relative !important; }
            .content { justify-content: center !important; }
            ha-state-icon { position: absolute !important; left: 12px !important; color: {{ '#1A1A1A' if is_state('input_number.tabs_homerseklet', '6.0') else '#FFFFFF' }} !important; animation: pulse 2s infinite ease-in-out !important; }
            span { color: {{ '#1A1A1A' if is_state('input_number.tabs_homerseklet', '6.0') else '#FFFFFF' }} !important; font-weight: {{ 'bold' if is_state('input_number.tabs_homerseklet', '6.0') else '500' }} !important; padding-left: 15px !important; }
            @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.3); } 100% { transform: scale(1); } }

  # ==========================================
  # 1. FÜL: FÜRDŐSZOBA
  # ==========================================
  - type: conditional
    conditions: [{ condition: state, entity: input_number.tabs_homerseklet, state: "1.0" }]
    card:
      type: grid
      columns: 1
      square: false
      cards:
        # HŐMÉRSÉKLET (Itt definiáljuk a &temp_style és &graph_style horgonyokat)
        - type: custom:vertical-stack-in-card
          card_mod: &stack_style
            style: |
              ha-card { border-radius: 12px; overflow: hidden; }
          cards:
            - type: custom:mushroom-entity-card
              entity: sensor.xiaomi_temp_humidity_bathroom_01_homerseklet_2
              tap_action: { action: more-info }
              icon: mdi:thermometer
              name: Temperature
              primary_info: state
              secondary_info: name
              card_mod: &temp_style
                style:
                  mushroom-shape-icon$: >
                    .shape {
                      {% set temp = states(config.entity) | float(0) %}
                      {% set rgb = '0,140,255' %} {% set anim = 'temp-cold-breathe' %} {% set glow_anim = 'temp-cold-glow' %} {% set halo_anim = 'temp-cold-halo' %} {% set duration = 4.0 %} {% set intensity = 0.5 %}
                      {% if temp < 16 %} {% set duration = 4.4 %} {% set intensity = 0.4 %}
                      {% elif temp < 18 %} {% set rgb = '255,210,40' %} {% set anim = 'temp-cool-wave' %} {% set glow_anim = 'temp-cool-glow' %} {% set halo_anim = 'temp-cool-halo' %} {% set duration = 3.4 %} {% set intensity = 0.55 %}
                      {% elif temp < 20 %} {% set rgb = '255,150,40' %} {% set anim = 'temp-comfy-breathe' %} {% set glow_anim = 'temp-comfy-glow' %} {% set halo_anim = 'temp-comfy-halo' %} {% set duration = 3.0 %} {% set intensity = 0.6 %}
                      {% elif temp < 22 %} {% set rgb = '255,115,20' %} {% set anim = 'temp-warm-pulse' %} {% set glow_anim = 'temp-warm-glow' %} {% set halo_anim = 'temp-warm-halo' %} {% set duration = 2.4 %} {% set intensity = 0.8 %}
                      {% else %} {% set rgb = '255,40,40' %} {% set anim = 'temp-hot-shimmer' %} {% set glow_anim = 'temp-hot-glow' %} {% set halo_anim = 'temp-hot-halo' %} {% set duration = 2.0 %} {% set intensity = 1.0 %}
                      {% endif %}
                      --temp-rgb: {{ rgb }}; --temp-intensity: {{ intensity }}; --shape-animation: {{ anim }} {{ duration }}s ease-in-out infinite; --temp-glow-animation: {{ glow_anim }} {{ (duration * 0.9) | round(2) }}s ease-in-out infinite; --temp-halo-animation: {{ halo_anim }} {{ (duration * 1.15) | round(2) }}s ease-in-out infinite;
                      opacity: 1; --icon-color: rgba({{ rgb }}, 1); background-color: rgba(77, 77, 77,0.1) !important; box-shadow: none !important; border: 1px solid rgba(255,255,255,0.06); position: relative; animation: var(--shape-animation);
                    }
                    .shape::before, .shape::after { content: ''; position: absolute; border-radius: inherit; pointer-events: none; }
                    .shape::before { inset: -8px; animation: var(--temp-glow-animation); }
                    .shape::after { inset: -22px; animation: var(--temp-halo-animation); mix-blend-mode: screen; }
                    @keyframes temp-cold-breathe { 0%, 100% { transform: scale(0.96); } 50% { transform: scale(1.03); } }
                    @keyframes temp-cold-glow { 50% { box-shadow: 0 0 30px 4 rgba(var(--temp-rgb), 0.95), 0 0 50px 10px rgba(var(--temp-rgb), 0.85); } }
                    @keyframes temp-cold-halo { 50% { box-shadow: 0 0 130px 36px rgba(var(--temp-rgb), 0.5), 0 -34px 100px -8px rgba(240, 250, 255, 0.8); } }
                    @keyframes temp-cool-wave { 0%, 100% { transform: translateX(0); } 50% { transform: translateX(1px) translateY(-1px); } }
                    @keyframes temp-cool-glow { 50% { box-shadow: 0 0 28px 2 rgba(var(--temp-rgb), 0.95), 0 0 48px 12px rgba(var(--temp-rgb), 0.85); } }
                    @keyframes temp-cool-halo { 50% { box-shadow: 0 0 140px 42px rgba(var(--temp-rgb), 0.45), 0 30px 110px -10px rgba(0, 255, 255, 0.5); } }
                    @keyframes temp-comfy-breathe { 0%, 100% { transform: scale(0.98); } 50% { transform: scale(1.05); } }
                    @keyframes temp-comfy-glow { 50% { box-shadow: 0 0 26px 4 rgba(var(--temp-rgb), 0.9), 0 0 42px 10px rgba(var(--temp-rgb), 0.85); } }
                    @keyframes temp-comfy-halo { 50% { box-shadow: 0 0 120px 40px rgba(var(--temp-rgb), 0.45), 0 26px 80px -10px rgba(180,255,200,0.5); } }
                    @keyframes temp-warm-pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.07); } }
                    @keyframes temp-warm-glow { 50% { box-shadow: 0 0 30px 4 rgba(var(--temp-rgb), 0.95), 0 0 54px 14px rgba(var(--temp-rgb), 0.9); } }
                    @keyframes temp-warm-halo { 50% { box-shadow: 0 0 140px 48px rgba(var(--temp-rgb), 0.55), 0 26px 100px -10px rgba(255,210,150,0.5); } }
                    @keyframes temp-hot-shimmer { 0%, 100% { transform: scale(1); filter: blur(0); } 50% { transform: scale(1.08); filter: blur(0.6px); } }
                    @keyframes temp-hot-glow { 50% { box-shadow: 0 0 34px 6 rgba(var(--temp-rgb), 1), 0 0 62px 14px rgba(var(--temp-rgb), 0.95); } }
                    @keyframes temp-hot-halo { 50% { box-shadow: 0 0 160px 60px rgba(var(--temp-rgb), 0.6), 0 34px 120px -12px rgba(255,150,100,0.6); } }
                  .: |
                    mushroom-shape-icon { --icon-size: 50px; }
                    ha-card { background: none; box-shadow: none; border: none; }
            - type: custom:mini-graph-card
              entities:
                - sensor.xiaomi_temp_humidity_bathroom_01_homerseklet_2
              hours_to_show: 24
              line_width: 4
              show: { name: false, icon: false, state: false, labels: false, legend: false }
              color_thresholds:
                - value: 0
                  color: blue
                - value: 16
                  color: lightblue
                - value: 18
                  color: orange
                - value: 21
                  color: red
              card_mod: &graph_style
                style: |
                  ha-card { background: none !important; box-shadow: none !important; border: none !important; opacity: 0.6; margin-top: -30px !important; padding-bottom: 0px !important; }
        
        # PÁRATARTALOM (Itt definiáljuk a &hum_style horgonyt)
        - type: custom:vertical-stack-in-card
          card_mod: *stack_style
          cards:
            - type: custom:mushroom-entity-card
              entity: sensor.xiaomi_temp_humidity_bathroom_01_paratartalom_2
              tap_action: { action: more-info }
              icon: mdi:water-percent
              name: Humidity
              primary_info: state
              secondary_info: name
              card_mod: &hum_style
                style:
                  mushroom-shape-icon$: >
                    .shape {
                      {% set hum = states(config.entity) | float(0) %}
                      {% set rgb = '120,210,255' %} {% set anim = 'hum-good-breathe' %} {% set glow_anim = 'hum-good-glow' %} {% set halo_anim = 'hum-good-halo' %} {% set duration = 3.2 %}
                      {% if hum < 40 %} {% set rgb = '0,80,200' %} {% set anim = 'hum-bad-pulse' %} {% set glow_anim = 'hum-bad-glow' %} {% set halo_anim = 'hum-bad-halo' %} {% set duration = 2.8 %}
                      {% elif hum <= 60 %} {% set duration = 3.4 %}
                      {% else %} {% set rgb = '40,140,255' %} {% set anim = 'hum-mid-wave' %} {% set glow_anim = 'hum-mid-glow' %} {% set halo_anim = 'hum-mid-halo' %} {% set duration = 3.0 %} {% endif %}
                      --hum-rgb: {{ rgb }}; --shape-animation: {{ anim }} {{ duration }}s ease-in-out infinite; --hum-glow-animation: {{ glow_anim }} {{ (duration * 0.9) | round(2) }}s ease-in-out infinite; --hum-halo-animation: {{ halo_anim }} {{ (duration * 1.1) | round(2) }}s ease-in-out infinite;
                      --icon-color: rgba({{ rgb }}, 1); background-color: rgba(77,77,77,0.2) !important; box-shadow: none !important; border: 1px solid rgba(255,255,255,0.06); opacity: 1; position: relative; animation: var(--shape-animation);
                    }
                    .shape::before, .shape::after { content: ''; position: absolute; border-radius: inherit; pointer-events: none; }
                    .shape::before { inset: -8px; animation: var(--hum-glow-animation); }
                    .shape::after { inset: -22px; animation: var(--hum-halo-animation); mix-blend-mode: screen; }
                    @keyframes hum-good-breathe { 0%, 100% { transform: scale(0.98); } 50% { transform: scale(1.04); } }
                    @keyframes hum-good-glow { 50% { box-shadow: 0 0 24px 4 rgba(var(--hum-rgb), 0.9), 0 0 44px 10px rgba(var(--hum-rgb), 0.85); } }
                    @keyframes hum-good-halo { 50% { box-shadow: 0 0 120px 40px rgba(var(--hum-rgb), 0.45), 0 26px 90px -10px rgba(200,240,255,0.45); } }
                    @keyframes hum-mid-wave { 0%, 100% { transform: translateX(0); } 50% { transform: translateX(1px) translateY(-1px); } }
                    @keyframes hum-mid-glow { 50% { box-shadow: 0 0 28px 3 rgba(var(--hum-rgb), 0.95), 0 0 48px 10px rgba(var(--hum-rgb), 0.85); } }
                    @keyframes hum-mid-halo { 50% { box-shadow: 0 0 135px 42px rgba(var(--hum-rgb), 0.5), 0 28px 105px -10px rgba(100,210,255,0.5); } }
                    @keyframes hum-bad-pulse { 0%, 100% { transform: scale(0.97); } 40% { transform: scale(1.03); } }
                    @keyframes hum-bad-glow { 50% { box-shadow: 0 0 26px 4 rgba(var(--hum-rgb), 0.95), 0 0 44px 12px rgba(var(--hum-rgb), 0.9); } }
                    @keyframes hum-bad-halo { 50% { box-shadow: 0 0 130px 40px rgba(var(--hum-rgb), 0.6), 0 26px 100px -8px rgba(0,90,190,0.65); } }
                  .: |
                    mushroom-shape-icon { --icon-size: 50px; }
                    ha-card { background: none; box-shadow: none; border: none; }
            - type: custom:mini-graph-card
              entities:
                - sensor.xiaomi_temp_humidity_bathroom_01_paratartalom_2
              line_color: lightblue
              line_width: 4
              hours_to_show: 24
              show: { name: false, icon: false, state: false, labels: false, legend: false }
              card_mod: *graph_style
        
        # AKKUMULÁTOR (Itt definiáljuk a &battery_style horgonyt)
        - type: custom:mushroom-entity-card
          entity: sensor.xiaomi_temp_humidity_bathroom_01_elem_akku_2
          tap_action: { action: more-info }
          icon: mdi:battery-high
          icon_color: white
          primary_info: name
          secondary_info: state
          name: Battery
          card_mod: &battery_style
            style:
              .: |
                ha-card {
                  --card-primary-font-size: 15px !important; --card-secondary-font-size: 12px !important; --card-primary-font-weight: bold !important;
                  {% set level = states(config.entity) | float(0) %}
                  {% if level <= 20 %} {% set color = '244, 67, 54' %}  
                  {% elif level <= 60 %} {% set color = '255, 152, 0' %}  
                  {% else %} {% set color = '0, 255, 100' %}  {% endif %}
                  --custom-level: {{ level }}%; --custom-color: rgba({{ color }}, 0.8);
                  --text-color: {{ 'rgba(' ~ color ~ ', 1)' if level < 101 else 'rgba(255,255,255,0.7)' }};
                  background: #1c1c1c !important; border: none !important; border-radius: 12px; position: relative; overflow: hidden;
                  background-image: radial-gradient(circle at 24px 24px, rgba({{ color }}, 0.15) 0%, transparent 60%) !important;
                }
                mushroom-shape-icon { --icon-size: 55px; }
                ha-card::before { content: '{{ states(config.entity) | float(0) | round(0) }}%'; position: absolute; top: 12px; right: 12px; font-size: 1rem; font-weight: 700; color: var(--text-color); background: rgba(0, 0, 0, 0.3); border: 1px solid rgba(255, 255, 255, 0.1); padding: 2px 6px; border-radius: 4px; }
                ha-card::after { content: ''; position: absolute; bottom: 0; left: 0; height: 4px; width: var(--custom-level); background: linear-gradient(90deg, transparent, var(--custom-color)); box-shadow: 0 0 10px var(--custom-color); }
              mushroom-shape-icon$: >
                .shape { --liquid-level: var(--custom-level); --liquid-color: var(--custom-color); background: rgba(255, 255, 255, 0.05) !important; overflow: hidden !important; position: relative; border: 1px solid rgba(255,255,255,0.1); }
                .shape::before { content: ''; position: absolute; left: -50%; width: 200%; height: 200%; top: calc(100% - var(--liquid-level)); background: var(--liquid-color); border-radius: 40%; animation: liquid-wave 6s linear infinite; opacity: 0.8; }
                ha-icon { position: relative; z-index: 2; mix-blend-mode: overlay; color: white !important; }
                @keyframes liquid-wave { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

  # ==========================================
  # 2. FÜL: ELŐSZOBA
  # ==========================================
  - type: conditional
    conditions: [{ condition: state, entity: input_number.tabs_homerseklet, state: "2.0" }]
    card:
      type: grid
      columns: 1
      square: false
      cards:
        - type: custom:vertical-stack-in-card
          card_mod: *stack_style
          cards:
            - type: custom:mushroom-entity-card
              entity: sensor.xiaomi_temp_humidity_hall_01_homerseklet_2
              tap_action: { action: more-info }
              icon: mdi:thermometer
              name: Temperature
              primary_info: state
              secondary_info: name
              card_mod: *temp_style
            - type: custom:mini-graph-card
              entities:
                - sensor.xiaomi_temp_humidity_hall_01_homerseklet_2
              hours_to_show: 24
              line_width: 4
              show: { name: false, icon: false, state: false, labels: false, legend: false }
              color_thresholds:
                - value: 0
                  color: blue
                - value: 16
                  color: lightblue
                - value: 18
                  color: orange
                - value: 21
                  color: red
              card_mod: *graph_style
        - type: custom:vertical-stack-in-card
          card_mod: *stack_style
          cards:
            - type: custom:mushroom-entity-card
              entity: sensor.xiaomi_temp_humidity_hall_01_paratartalom_2
              tap_action: { action: more-info }
              icon: mdi:water-percent
              name: Humidity
              primary_info: state
              secondary_info: name
              card_mod: *hum_style
            - type: custom:mini-graph-card
              entities:
                - sensor.xiaomi_temp_humidity_hall_01_paratartalom_2
              line_color: lightblue
              line_width: 4
              hours_to_show: 24
              show: { name: false, icon: false, state: false, labels: false, legend: false }
              card_mod: *graph_style
        - type: custom:mushroom-entity-card
          entity: sensor.xiaomi_temp_humidity_hall_01_elem_akku_2
          tap_action: { action: more-info }
          icon: mdi:battery-high
          icon_color: white
          primary_info: name
          secondary_info: state
          name: Battery
          card_mod: *battery_style

  # ==========================================
  # 3. FÜL: KONYHA
  # ==========================================
  - type: conditional
    conditions: [{ condition: state, entity: input_number.tabs_homerseklet, state: "3.0" }]
    card:
      type: grid
      columns: 1
      square: false
      cards:
        - type: custom:vertical-stack-in-card
          card_mod: *stack_style
          cards:
            - type: custom:mushroom-entity-card
              entity: sensor.xiaomi_temp_humidity_kitchen_01_homerseklet_2
              tap_action: { action: more-info }
              icon: mdi:thermometer
              name: Temperature
              primary_info: state
              secondary_info: name
              card_mod: *temp_style
            - type: custom:mini-graph-card
              entities:
                - sensor.xiaomi_temp_humidity_kitchen_01_homerseklet_2
              hours_to_show: 24
              line_width: 4
              show: { name: false, icon: false, state: false, labels: false, legend: false }
              color_thresholds:
                - value: 0
                  color: blue
                - value: 16
                  color: lightblue
                - value: 18
                  color: orange
                - value: 21
                  color: red
              card_mod: *graph_style
        - type: custom:vertical-stack-in-card
          card_mod: *stack_style
          cards:
            - type: custom:mushroom-entity-card
              entity: sensor.xiaomi_temp_humidity_kitchen_01_paratartalom_2
              tap_action: { action: more-info }
              icon: mdi:water-percent
              name: Humidity
              primary_info: state
              secondary_info: name
              card_mod: *hum_style
            - type: custom:mini-graph-card
              entities:
                - sensor.xiaomi_temp_humidity_kitchen_01_paratartalom_2
              line_color: lightblue
              line_width: 4
              hours_to_show: 24
              show: { name: false, icon: false, state: false, labels: false, legend: false }
              card_mod: *graph_style
        - type: custom:mushroom-entity-card
          entity: sensor.xiaomi_temp_humidity_kitchen_01_elem_akku_2
          tap_action: { action: more-info }
          icon: mdi:battery-high
          icon_color: white
          primary_info: name
          secondary_info: state
          name: Battery
          card_mod: *battery_style

  # ==========================================
  # 4. FÜL: NAPPALI
  # ==========================================
  - type: conditional
    conditions: [{ condition: state, entity: input_number.tabs_homerseklet, state: "4.0" }]
    card:
      type: grid
      columns: 1
      square: false
      cards:
        - type: custom:vertical-stack-in-card
          card_mod: *stack_style
          cards:
            - type: custom:mushroom-entity-card
              entity: sensor.xiaomi_temp_humidity_livingroom_01_homerseklet_2
              tap_action: { action: more-info }
              icon: mdi:thermometer
              name: Temperature
              primary_info: state
              secondary_info: name
              card_mod: *temp_style
            - type: custom:mini-graph-card
              entities:
                - sensor.xiaomi_temp_humidity_livingroom_01_homerseklet_2
              hours_to_show: 24
              line_width: 4
              show: { name: false, icon: false, state: false, labels: false, legend: false }
              color_thresholds:
                - value: 0
                  color: blue
                - value: 16
                  color: lightblue
                - value: 18
                  color: orange
                - value: 21
                  color: red
              card_mod: *graph_style
        - type: custom:vertical-stack-in-card
          card_mod: *stack_style
          cards:
            - type: custom:mushroom-entity-card
              entity: sensor.xiaomi_temp_humidity_livingroom_01_paratartalom_2
              tap_action: { action: more-info }
              icon: mdi:water-percent
              name: Humidity
              primary_info: state
              secondary_info: name
              card_mod: *hum_style
            - type: custom:mini-graph-card
              entities:
                - sensor.xiaomi_temp_humidity_livingroom_01_paratartalom_2
              line_color: lightblue
              line_width: 4
              hours_to_show: 24
              show: { name: false, icon: false, state: false, labels: false, legend: false }
              card_mod: *graph_style
        - type: custom:mushroom-entity-card
          entity: sensor.xiaomi_temp_humidity_livingroom_01_elem_akku_2
          tap_action: { action: more-info }
          icon: mdi:battery-high
          icon_color: white
          primary_info: name
          secondary_info: state
          name: Battery
          card_mod: *battery_style

  # ==========================================
  # 5. FÜL: HÁLÓSZOBA
  # ==========================================
  - type: conditional
    conditions: [{ condition: state, entity: input_number.tabs_homerseklet, state: "5.0" }]
    card:
      type: grid
      columns: 1
      square: false
      cards:
        - type: custom:vertical-stack-in-card
          card_mod: *stack_style
          cards:
            - type: custom:mushroom-entity-card
              entity: sensor.xiaomi_temp_humidity_bedroom_01_homerseklet_2
              tap_action: { action: more-info }
              icon: mdi:thermometer
              name: Temperature
              primary_info: state
              secondary_info: name
              card_mod: *temp_style
            - type: custom:mini-graph-card
              entities:
                - sensor.xiaomi_temp_humidity_bedroom_01_homerseklet_2
              hours_to_show: 24
              line_width: 4
              show: { name: false, icon: false, state: false, labels: false, legend: false }
              color_thresholds:
                - value: 0
                  color: blue
                - value: 16
                  color: lightblue
                - value: 18
                  color: orange
                - value: 21
                  color: red
              card_mod: *graph_style
        - type: custom:vertical-stack-in-card
          card_mod: *stack_style
          cards:
            - type: custom:mushroom-entity-card
              entity: sensor.xiaomi_temp_humidity_bedroom_01_paratartalom_2
              tap_action: { action: more-info }
              icon: mdi:water-percent
              name: Humidity
              primary_info: state
              secondary_info: name
              card_mod: *hum_style
            - type: custom:mini-graph-card
              entities:
                - sensor.xiaomi_temp_humidity_bedroom_01_paratartalom_2
              line_color: lightblue
              line_width: 4
              hours_to_show: 24
              show: { name: false, icon: false, state: false, labels: false, legend: false }
              card_mod: *graph_style
        - type: custom:mushroom-entity-card
          entity: sensor.xiaomi_temp_humidity_bedroom_01_elem_akku_2
          tap_action: { action: more-info }
          icon: mdi:battery-high
          icon_color: white
          primary_info: name
          secondary_info: state
          name: Battery
          card_mod: *battery_style

  # ==========================================
  # 6. FÜL: GYEREKSZOBA
  # ==========================================
  - type: conditional
    conditions: [{ condition: state, entity: input_number.tabs_homerseklet, state: "6.0" }]
    card:
      type: grid
      columns: 1
      square: false
      cards:
        - type: custom:vertical-stack-in-card
          card_mod: *stack_style
          cards:
            - type: custom:mushroom-entity-card
              entity: sensor.xiaomi_temp_humidity_childroom_02_homerseklet
              tap_action: { action: more-info }
              icon: mdi:thermometer
              name: Temperature
              primary_info: state
              secondary_info: name
              card_mod: *temp_style
            - type: custom:mini-graph-card
              entities:
                - sensor.xiaomi_temp_humidity_childroom_02_homerseklet
              hours_to_show: 24
              line_width: 4
              show: { name: false, icon: false, state: false, labels: false, legend: false }
              color_thresholds:
                - value: 0
                  color: blue
                - value: 16
                  color: lightblue
                - value: 18
                  color: orange
                - value: 21
                  color: red
              card_mod: *graph_style
        - type: custom:vertical-stack-in-card
          card_mod: *stack_style
          cards:
            - type: custom:mushroom-entity-card
              entity: sensor.xiaomi_temp_humidity_childroom_02_paratartalom
              tap_action: { action: more-info }
              icon: mdi:water-percent
              name: Humidity
              primary_info: state
              secondary_info: name
              card_mod: *hum_style
            - type: custom:mini-graph-card
              entities:
                - sensor.xiaomi_temp_humidity_childroom_02_paratartalom
              line_color: lightblue
              line_width: 4
              hours_to_show: 24
              show: { name: false, icon: false, state: false, labels: false, legend: false }
              card_mod: *graph_style
        - type: custom:mushroom-entity-card
          entity: sensor.xiaomi_temp_humidity_childroom_02_elem_akku
          tap_action: { action: more-info }
          icon: mdi:battery-high
          icon_color: white
          primary_info: name
          secondary_info: state
          name: Battery
          card_mod: *battery_style

```

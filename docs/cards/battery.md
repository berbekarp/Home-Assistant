# 🔋 Akkumulátor Állapot Kártya (Animált Folyadékszinttel)

Ez a dokumentáció egy magasan testreszabott [Mushroom Entity Card](https://github.com/piitaya/lovelace-mushroom) beállítását mutatja be, amely egyedülálló, animált "folyadékszint" effektussal jelzi az eszközök akkumulátorának töltöttségét.

## Működés és Vizuális Visszajelzések

A kártya a `card-mod` segítségével komplex CSS animációkat használ, hogy a töltöttségi szintet folyadékként ábrázolja az ikonon belül.

### 1. Folyadékszint (Wave Animation)
Az ikonon belül hullámzó folyadék szintje pontosan követi a szenzor által jelentett százalékos értéket (pl. 20%-nál csak az alján hullámzik, 100%-nál teljesen kitölti). Az ikon alatt egy diszkrét, színben megegyező folyamatjelző csík (progress bar) is végigfut a kártya alján.

### 2. Színkódok (Töltöttségi Állapotok)
A kód logikája automatikusan változtatja a folyadék, a kártya háttérfénye (ambient glow) és a százalékos kijelző színét a töltöttség alapján:
* **Zöld (Green):** 61% - 100% (Magas töltöttség)
* **Narancssárga (Orange):** 21% - 60% (Közepes töltöttség)
* **Piros (Red):** 0% - 20% (Alacsony/Kritikus töltöttség)

### 3. Töltés Animáció (Cyan + Buborékok)
Ha a kód elején megadott entitás (pl. egy okoskonnektor vagy töltő szenzor) aktív (`on` állapot), a kártya azonnal vizuálisan is reagál a töltésre:
* A szín **Ciánkékre (Cyan)** vált.
* Az ikon körül egy pulzáló fénygömb (Icon Glow) jelenik meg.
* A folyadékon belül felszálló **buborékok animációja** indul el.

---

## Előnézet (Animáció)

Az alábbi animáción látható a kártya működés közben (a példán a Zöld és a Narancssárga állapotok látszanak).

![Akkumulátor animáció](../images/battery_status.gif)

*(Megjegyzés: A valóságban a piros és a ciánkék/töltés animációk is ugyanígy, a fent leírt logikának megfelelően aktiválódnak).*

---

## YAML Konfiguráció és CSS kód

A kártya létrehozásához hozz létre egy **Manual (Kézi)** kártyát a dashboardon, és másold be az alábbi kódot. 

> **Fontos beállítási lépések a használathoz:**
> 1. Írd át az `entity` mezőt (jelenleg `sensor.ikea_switch_kitchen_on_off_01_elem_akku_4`) a saját eszközöd akkumulátor szenzorjára.
> 2. Ha használni szeretnéd a "Töltés" animációt, írd át a `charging_entity` változót (jelenleg `binary_sensor.anasbox_is_charging`) a saját eszközöd töltését jelző bináris szenzorra (vagy switch-re).

```yaml
type: custom:mushroom-entity-card
tap_action:
  action: more-info
icon: ""
icon_color: white
primary_info: name
secondary_info: state
entity: sensor.ikea_switch_kitchen_on_off_01_elem_akku_4
grid_options:
  columns: 12
  rows: 2
name: Kitchen switch on/off 01
card_mod:
  style:
    .: |
      ha-card {
        /* ====== USER SETTINGS ===== */
        {% set charging_entity =
          'binary_sensor.anasbox_is_charging' %} 
        /* ========================= */

        /* ======= FONT SETTINGS ======= */
        --card-primary-font-size: 15px !important;
        --card-secondary-font-size: 12px !important;
        --card-primary-font-weight: bold !important;

        /* --- LOGIC --- */
        {% set level = states(config.entity) | float(0) %}
        {% set is_charging = is_state(charging_entity, 'on') %}
        
        /* 1. Determine Color */
        {% if is_charging %}
           {% set color = '0, 255, 255' %} /* Cyan (Charging) */
        {% elif level <= 20 %}
          {% set color = '244, 67, 54' %}  /* Red */
        {% elif level <= 60 %}
          {% set color = '255, 152, 0' %}  /* Orange */
        {% else %}
          {% set color = '0, 255, 100' %}  /* Green */
        {% endif %}

        /* --- PASS VARIABLES TO CSS --- */
        --custom-level: {{ level }}%;
        --custom-color: rgba({{ color }}, 0.8);
        --custom-bubble: {{ 'block' if is_charging else 'none' }};
        
        /* Icon Glow */
        --custom-icon-shadow: {{ '0 0 15px rgba(' ~ color ~ ', 0.6)' if is_charging else 'none' }};
        
        /* Text Color */
        --text-color: {{ 'rgba(' ~ color ~ ', 1)' if level < 101 else 'rgba(255,255,255,0.7)' }};

        /* --- CARD STYLING --- */
        background: #1c1c1c !important;
        border: none !important;
        border-radius: 12px;
        position: relative;
        overflow: hidden;
        transition: all 0.5s ease;
        
        /* Ambient Glow behind the liquid */
        background-image: radial-gradient(circle at 24px 24px, rgba({{ color }}, 0.15) 0%, transparent 60%) !important;
      }

      /* Icon Styling */
      mushroom-shape-icon {
        --icon-size: 65px;
        display: flex;
        padding-right: 15px;
        padding-bottom: 5px;
      }

      /* --- PERCENTAGE BADGE (Top Right) --- */
      ha-card::before {
        content: '{{ level | round(0) }}%';
        position: absolute;
        top: 12px; right: 12px;
        font-size: 1rem; font-weight: 700;
        color: var(--text-color);
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2px 6px; border-radius: 4px;
      }

      /* --- PROGRESS BAR TRACK --- */
      ha-card::after {
        content: '';
        position: absolute;
        bottom: 0; left: 0;
        height: 4px;
        width: {{ level }}%;
        background: linear-gradient(90deg, transparent, rgb({{ color }}));
        box-shadow: 0 0 10px rgb({{ color }});
        transition: width 0.5s ease;
      }
    mushroom-shape-icon$: |
      .shape {
        /* --- LOGIC INJECTION --- */
        --liquid-level: var(--custom-level);
        --liquid-color: var(--custom-color);
        --bubble-display: var(--custom-bubble);
        
        /* Container Setup */
        background: rgba(255, 255, 255, 0.05) !important;
        overflow: hidden !important; /* Keeps the liquid inside the circle */
        position: relative;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: var(--custom-icon-shadow) !important;
      }

      /* THE LIQUID (Wavy Fill) */
      .shape::before {
        content: '';
        position: absolute;
        left: -50%;
        width: 200%;
        height: 200%;
        
        /* The top is calculated based on battery level (100% - level) */
        top: calc(100% - var(--liquid-level));
        
        background: var(--liquid-color);
        border-radius: 40%; /* Creates the "Wave" shape when rotated */
        
        /* The Wave Animation */
        animation: liquid-wave 6s linear infinite;
        opacity: 0.8;
      }

      /* CHARGING BUBBLES */
      .shape::after {
        content: '';
        display: var(--bubble-display);
        position: absolute;
        inset: 0;
        background-image: 
          radial-gradient(2px 2px at 20% 80%, rgba(255,255,255,0.8), transparent),
          radial-gradient(2px 2px at 50% 70%, rgba(255,255,255,0.8), transparent),
          radial-gradient(3px 3px at 80% 90%, rgba(255,255,255,0.8), transparent);
        background-size: 100% 100%;
        animation: bubbles-rise 0.7s linear infinite;
      }

      /* Ensure the MDI Icon sits on top of the liquid */
      ha-icon {
        position: relative;
        z-index: 2;
        /* Blend the icon slightly so it looks submerged */
        mix-blend-mode: overlay; 
        color: white !important;
      }

      /* --- ANIMATIONS --- */
      @keyframes liquid-wave {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
      }

      @keyframes bubbles-rise {
        0% { transform: translateY(10px); opacity: 0; }
        50% { opacity: 1; }
        100% { transform: translateY(-20px); opacity: 0; }
      }

```

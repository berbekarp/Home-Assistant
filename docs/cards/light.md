# Konyha Világítás - Mushroom Light Card

Ez a dokumentáció bemutatja a konyhai világítás vezérléséhez használt [Mushroom Cards](https://github.com/piitaya/lovelace-mushroom) felület beállításait és a kártya különböző állapotait.

## YAML Konfiguráció

A kártya beállításához az alábbi kódot használjuk a Lovelace (Dashboard) felületen:

```yaml
type: custom:mushroom-light-card
entity: light.kitchen_lights
name: Konyha
icon: mdi:ceiling-light
show_brightness_control: true
show_color_temp_control: true
use_light_color: true
layout: horizontal

```

### A beállítások magyarázata:

* **`type: custom:mushroom-light-card`**: Meghatározza, hogy a Mushroom dizájncsalád világítás kártyáját használjuk.
* **`entity: light.kitchen_lights`**: A vezérelni kívánt Home Assistant entitás (a konyhai lámpák csoportja vagy főkapcsolója).
* **`name: Konyha`**: A kártyán megjelenő egyedi név (felülírja az entitás alapértelmezett nevét).
* **`icon: mdi:ceiling-light`**: A mennyezeti lámpa ikonjának beállítása.
* **`show_brightness_control: true`**: Megjeleníti a fényerőszabályzó csúszkát.
* **`show_color_temp_control: true`**: Megjeleníti a színhőmérséklet (hideg/meleg fehér) szabályozó csúszkát.
* **`use_light_color: true`**: A kártya ikonja és csúszkája felveszi az izzó aktuális színét/színhőmérsékletét.
* **`layout: horizontal`**: Vízszintes elrendezés (az ikon és a név egymás mellett jelenik meg a kompaktabb nézet érdekében).

---

## Megjelenés (Állapotok)

Az alábbi képeken látható, hogyan néz ki a kártya a Home Assistant felületén különböző állapotokban.

### 1. Kikapcsolt állapot

Amikor a lámpa le van kapcsolva, a kártya szürkén jelenik meg, jelezve az inaktív állapotot.

### 2. Bekapcsolt állapot

Felkapcsoláskor a kártya és az ikon színe megváltozik (`use_light_color`), alkalmazkodva a lámpa aktuális beállításaihoz.

### 3. Fényerő és Színhőmérséklet szabályozása

A bekapcsolt extráknak köszönhetően (`show_brightness_control` és `show_color_temp_control`) a kártya felületén közvetlenül állítható a fényerő és a színhőmérséklet.

---

## Feltételes Megjelenítés és Egyedi Animáció (Rejtett Kártya)

Ha szeretnéd tisztán tartani a műszerfalad (dashboard), beállíthatod, hogy egy részletes vezérlőkártya **csak akkor jelenjen meg, ha a lámpa be van kapcsolva** (`on` állapot). Kikapcsolt állapotban ez a kártya teljesen eltűnik a felületről.

Ez a megoldás két kártyát használ egymás mellett:

1. Egy fix **Navigációs kártyát** (Template card), ami mindig látszik.
2. Egy **Feltételes (Conditional) kártyát**, ami csak bekapcsolt lámpa esetén ugrik elő, kiegészítve egy egyedi, a lámpa aktuális színéhez igazodó pulzáló `card-mod` animációval.

### Működés közben:

Az alábbi animáción látható, ahogy a kártya dinamikusan előtűnik a felületen a lámpa felkapcsolásakor, majd lekapcsoláskor ismét elrejtőzik.

### YAML Konfiguráció a rejtett és animált kártyához:

A működéshez a Dashboardon két különálló kártyát kell létrehoznod (vagy beillesztheted őket egy grid/horizontal stack-be).

**1. A mindig látható navigációs kártya:**

```yaml
type: custom:mushroom-template-card
primary: Lámpák
icon: mdi:lamp
multiline_secondary: false
tap_action:
  action: navigate
  navigation_path: /dashboard-lightsl
color: blue
features_position: bottom
grid_options:
  columns: full

```

**2. A feltételes, animált lámpa kártya:**

```yaml
type: conditional
conditions:
  - condition: state
    entity: light.kitchen_lights
    state: "on"
card:
  type: custom:mushroom-light-card
  entity: light.kitchen_lights
  use_light_color: true
  show_color_temp_control: false
  show_brightness_control: false
  collapsible_controls: true
  show_color_control: true
  name: Konyha lámpa
  icon_color: white
  icon: phu:bulbs-classic
  card_mod:
    style:
      mushroom-shape-icon$: |
        .shape {
          {# ======== SZÍN LEKÉRDEZÉSE ======== #}
          {% set rgb = state_attr(config.entity, 'rgb_color') %}
          {% if rgb %}
            {% set r = rgb[0] %}
            {% set g = rgb[1] %}
            {% set b = rgb[2] %}
          {% else %}
            {% set r = 255 %}
            {% set g = 240 %}
            {% set b = 200 %}
          {% endif %}

          {# ======== ANIMÁCIÓ LETILTÁSA HA NEM 'ON' ======== #}
          {% if is_state(config.entity, 'on') %}
            --shape-animation: lamp-sweep 1.8s ease-in-out infinite !important;
            animation: lamp-sweep 1.8s ease-in-out infinite !important;
          {% else %}
            --shape-animation: none !important;
            animation: none !important;
            box-shadow: none !important;
          {% endif %}

          position: relative;
          transform-origin: 50% 60%;
        }

        @keyframes lamp-sweep {
          0% {
            filter: brightness(1.1);
            box-shadow:
              0 0 12px 4px rgba({{ r }}, {{ g }}, {{ b }}, 0.9),
              0 30px 40px -10px rgba({{ r }}, {{ g }}, {{ b }}, 0.0);
            transform: rotate(-4deg) scale(1);
          }
          25% {
            filter: brightness(1.4);
            box-shadow:
              0 0 18px 8px rgba({{ r }}, {{ g }}, {{ b }}, 1),
              -8px 35px 45px -12px rgba({{ r }}, {{ g }}, {{ b }}, 0.5);
            transform: rotate(3deg) scale(1.02);
          }
          50% {
            filter: brightness(1.2);
            box-shadow:
              0 0 24px 10px rgba({{ r }}, {{ g }}, {{ b }}, 0.9),
              8px 35px 45px -12px rgba({{ r }}, {{ g }}, {{ b }}, 0.5);
            transform: rotate(-2deg) scale(1.03);
          }
          75% {
            filter: brightness(1.5);
            box-shadow:
              0 0 18px 8px rgba({{ r }}, {{ g }}, {{ b }}, 1),
              -6px 30px 40px -12px rgba({{ r }}, {{ g }}, {{ b }}, 0.4);
            transform: rotate(2deg) scale(1.01);
          }
          100% {
            filter: brightness(1.1);
            box-shadow:
              0 0 12px 4px rgba({{ r }}, {{ g }}, {{ b }}, 0.8),
              0 30px 40px -10px rgba({{ r }}, {{ g }}, {{ b }}, 0.0);
            transform: rotate(-4deg) scale(1);
          }
        }
      .: |
        mushroom-shape-icon {
          --icon-size: 65px;
          display: flex;
          margin: -18px 0px 0px -18px !important;
        }
        ha-card {
          clip-path: inset(0 0 0 0 round var(--ha-card-border-radius, 12px));
        }

```
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

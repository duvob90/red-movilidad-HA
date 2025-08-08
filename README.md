# Integración Red Movilidad para Home Assistant

Esta integración personalizada te permite visualizar en Home Assistant los próximos buses que llegarán a un paradero del sistema de Red Movilidad de Santiago de Chile. Utiliza la API pública disponible en https://github.com/muZk/red-api para obtener información en tiempo real.

## 🚀 Características

- Sensores con tiempos de llegada estimados para cada recorrido.
- Configuración fácil desde la interfaz de Home Assistant (UI).
- Compatible con tarjetas estándar y tarjetas Mushroom para dashboards atractivos.
- Múltiples paraderos soportados.

---

## 🛠️ Instalación

1. Copia esta carpeta (`redmovilidad`) en `config/custom_components/` dentro de tu instalación de Home Assistant.
2. Reinicia Home Assistant.
3. Ve a **Ajustes > Dispositivos y servicios > Agregar integración**.
4. Busca `Red Movilidad` e ingresa el código de paradero (ej: `PD94`).

---

## 🧪 Sensor creado

Por cada paradero configurado se crea un sensor como:

```
sensor.paradero_pd94
```

- **Estado del sensor**: muestra el próximo bus y su tiempo estimado (ej: `119: 5-7 min`)
- **Atributos**:
  - `next_buses`: lista completa de próximos buses.
  - `next_buses_text`: resumen de llegadas (texto simple).
  - `friendly_name`: nombre del paradero.

---

## 🧩 Ejemplos de tarjetas Lovelace

### 📘 Tarjeta estándar

```yaml
type: entities
entities:
  - entity: sensor.paradero_pd94
    name: Paradero PD94
    icon: mdi:bus
```

### 📋 Tarjeta Markdown

```yaml
type: markdown
title: Próximos buses
content: >-
  **Próximos buses en PD94:**  
  {% set buses = state_attr('sensor.paradero_pd94', 'next_buses') %}
  {% if buses %}
    {% for bus in buses %}
      - **{{ bus.route_id }}:** {{ bus.arrival_estimation }}
    {% endfor %}
  {% else %}
    No hay datos disponibles.
  {% endif %}
```

### 🍄 Tarjeta Mushroom Template

```yaml
type: custom:mushroom-template-card
icon: mdi:bus
icon_color: green
layout: vertical
entity: sensor.paradero_pd94 // Debes cambiar esto por el codigo de paradero que configuraste en la UI al añadir la integración
primary: |
  {{ state_attr('sensor.paradero_pd94', 'friendly_name') }}
multiline_secondary: true
secondary: >
  {% set buses = state_attr('sensor.paradero_pd94', 'next_buses') %} {% set ns = // Debes cambiar esto por el codigo de paradero que configuraste en la UI al añadir la integración
  namespace(vistos=[], out='') %} {% for bus in buses %} 
    {% if bus.route_id not in ns.vistos %}
      {% set ns.out = ns.out + (bus.route_id ~ " - " ~ bus.arrival_estimation ~ "\n") %}
      {% set ns.vistos = ns.vistos + [bus.route_id] %}
    {% endif %}
  {% endfor %} {{ ns.out }}
```

---

## 🧾 Créditos

Basado en la API no oficial de Red Movilidad:  
https://github.com/muZk/red-api

---

¡Felices automatizaciones! 🚏🚌

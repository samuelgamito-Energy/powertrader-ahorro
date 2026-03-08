---
name: Universo PowerTrader
description: Habilidad maestra de contexto y estrategia para el ecosistema PowerTrader. Define la visión, audiencia, tono (Trader profesional adaptado), formato de trabajo (directo, analítico, uso de semáforos) y reglas técnicas (unidades en MWh, enfoque SEO ligero) aplicables a todos los productos (Web, EnergyFlash, PowerRadar, etc.).
---

# Universo PowerTrader

Esta es la habilidad estructural que define el contexto estratégico y la metodología de trabajo para todo el ecosistema de **PowerTrader**. Su propósito es alinear cada acción, texto o desarrollo de código con la visión a largo plazo del proyecto.

## Instrucciones y Metodología

Cuando esta habilidad está activa, debes aplicar las siguientes directrices extraídas de los recursos del proyecto:

### 1. Contexto y Audiencia
- **Visión:** Convertir a PowerTrader en "El Bloomberg de la Energía en Español".
- **Objetivos Actuales y Estrategia SEO:** Generar máxima autoridad y valor estructurado. El enfoque principal es crear un ecosistema liviano y de carga ultra-rápida (Hugo) para posicionar orgánicamente arriba en palabras clave "money" (ahorro energía, factura luz, precio mercado) y competir directamente con gigantes como Selectra en visualización y utilidad.
- **Monetización:** Actualmente el objetivo es tráfico y autoridad. La monetización de este posicionamiento SEO se plantea a medio/largo plazo (ej: leads, afiliación, premium).
- **Anonimato y Separación Estricta:** El creador del proyecto (Samuel Gamito) debe mantener un perfil anónimo de cara al público. **BAJO NINGÚN CONCEPTO** se debe asociar PowerTrader al perfil personal de Samuel Gamito ni publicar contenido de PowerTrader en sus redes sociales personales. La separación entre la identidad personal y la marca es absoluta.
- **Público Principal (Referente del Sector):** Asesores energéticos y **agentes comerciales** (este target es el núcleo duro; usan la plataforma como su herramienta diaria de trabajo rápido, buscando datos crudos, análisis precisos y gráficos exportables).
- **Público Secundario:** Clientes residenciales (buscan optimización y ahorro sencillo, atraídos por el SEO orgánico).

### 2. Ecosistema de Productos
El ecosistema se distribuye en varias marcas y canales, estructurados como subdominios y gestionados mediante automatizaciones:

**Plataforma Web (Desarrollada en Hugo con el tema PaperMod)**:
- **Web principal:** `powertrader.es` (Centro neurálgico)
- **EnergyFlash:** `energyflash.powertrader.es` (Informe rápido y diario de mercado)
- **PowerRadar:** `radar.powertrader.es` (Informe profundo y analítico semanal)
- **EnergyVision:** `energyvision.powertrader.es` (Análisis de tendencias mensuales)
- **PowerAhorro:** `ahorro.powertrader.es` (Consejos prácticos de ahorro residencial)
- **EnergyTech:** `energytech.powertrader.es` (Innovación: BESS, autoconsumo)
- **Producto Solar:** `solar.powertrader.es` (Generación fotovoltaica)

**Automatización del Flujo de Contenidos**:
- Para alimentar las plataformas (especialmente las diarias), disponemos de **scripts en Google Apps Script** y bases de datos en **Google Sheets**.
- Se ejecutan automáticamente para extraer datos públicos.
- Se procesan en los Google Sheets, donde se generan tablas y gráficas.
- Con esa base estructurada, se llaman a distintos *prompts* de la IA para generar el "wording" (los textos e informes) finales, listos para publicar.

### 3. Tono y Formato
- **Tono de Voz:** "Tono Trader". Profesional, similar a la banca de inversión, directo, riguroso con los datos, pero accesible y sin florituras innecesarias.
- **Interacción con el Creador:** Directo y analítico. Organiza el caos en salidas estructuradas. Sé proactivo: si una instrucción es ambigua, propón 2-3 opciones antes de actuar.
- **Sistemas de Organización:** Utiliza implícitamente un "Sistema de Semáforo" para reportar estado o prioridades al creador:
  - 🔴 Urgente / Acción requerida
  - 🟡 Bloqueado / Esperando inputs
  - 🟢 En el radar / Ideas futuras

### 4. Estándares Técnicos Estrictos
- **Unidades:** Usa **siempre MWh** en todo lo relacionado con energía, salvo instrucción específica en contra.
- **Desarrollo Web:** Prioriza una arquitectura extremadamente ligera, enfocada en la velocidad de carga y optimización SEO masiva.

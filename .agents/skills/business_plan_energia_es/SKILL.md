---
name: Business Plan Energía España (BESS)
description: Genera planes de negocio detallados para proyectos de baterías detrás del contador (behind-the-meter) en el sector doméstico español, con proyecciones mensuales y métricas financieras para inversores.
---

# Generador de Planes de Negocio BESS (España)

Esta habilidad permite crear estructuras de planes de negocio listas para inversores (VC/Project Finance), enfocándose en la venta o alquiler de baterías a clientes domésticos sin fotovoltaica propia.

## Estructura del Plan de Negocio

El plan generado debe seguir este esquema:

1.  **Resumen Ejecutivo**: Propuesta de valor y KPIs clave.
2.  **Solución Técnica**: Detalle del equipo (ej. Livoltek), capacidad (kWh) y modo de operación (arbitraje energético).
3.  **Modelo de Ingresos**:
    - Detalle mensual de ventas de unidades o cuotas de servicio.
    - Ingresos por arbitraje (compra en horas baratas, uso en horas caras).
4.  **Estructura de Costes (Mensual)**:
    - **CapEx**: Adquisición de baterías, logística, instalación.
    - **OpEx**: Mantenimiento, plataforma SaaS de gestión, seguros, atención al cliente.
5.  **Proyecciones Financieras (Investor-Ready)**:
    - **Cuenta de PyG**: Margen bruto y EBITDA mensual.
    - **Flujo de Caja (Cash Flow)**: Evolución de la tesorería.
    - **Análisis de Inversión**: TIR (IRR), VAN (NPV), Payback (mes de retorno).

## Lógica y Cálculos

Cuando se use esta habilidad, el asistente debe:

- **Detalle Mensual**: No presentar solo totales anuales. El flujo de caja debe mostrar la estacionalidad y el ritmo de despliegue.
- **Métricas Financieras**: Calcular el VAN usando una tasa de descuento coherente (ej. 8-10%) y la TIR basada en un horizonte de 10-15 años.
- **Sin Regulación Externa**: Al ser proyectos "behind-the-meter", ignorar trámites de acceso y conexión, centrándose en el contrato con la comercializadora y el cliente final.

## Tono y Estética

- Utilizar un lenguaje profesional y directivo.
- Si se genera un informe visual (HTML/Markdown), usar colores corporativos premium (granate/neutrales) similares a PowerTrader/Alumbra.

## Ejemplo de Entrada

"Genera un plan de negocio para desplegar 1000 baterías de 5kWh en el primer año, con un coste de adquisición de 2500€/unidad y un ahorro estimado para el cliente de 40€/mes."

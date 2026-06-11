---
name: Auditoría Cierres MEFF Alumbra
description: Especialista en auditar, procesar e inyectar datos de cierres y liquidaciones mayoristas de MEFF y REE (LCOST) para Alumbra Energía. Incorpora lógica de signos contables, unificaciones C1+C2 y teoría del mercado diario vs. desvíos.
---

# Auditoría Cierres MEFF Alumbra

Esta habilidad capacita al agente para procesar, auditar y compilar de manera experta los datos de facturación mayorista de MEFF y Red Eléctrica (REE) para Alumbra Energía, garantizando precisión contable, alineación matemática y coherencia en el dashboard de cierres.

## 🏛️ Contexto y Reglas de Mercado

### 1. Desviaciones vs. Consumo Real
*   Las facturas de **MEFF y REE (LCOST)** representan **desvíos de balance y coberturas financieras**, no el consumo real en bornes de consumidor de la cartera de clientes.
*   Para conocer la energía física facturada a los clientes, se deben cruzar las curvas de carga horaria (**archivos CCH / medidas F1 de distribuidora**).
*   La ecuación de compra física mayorista total es:
    $$\text{Energía Mayorista Total} = \text{Compra OMIE (Pool Diario)} \pm \text{Ajustes/Desvíos REE (C1/C2/C3)} \pm \text{MEFF}$$

### 2. Contratos Bilaterales Físicos (PPAs)
Si Alumbra cuenta con un contrato bilateral físico (ej. 10% del consumo):
*   **OMIE**: Ese 10% se deduce de la previsión de compra. Alumbra compra solo el 90% en el pool diario.
*   **REE**: Se realiza una nominación física. REE cobra peajes y costes regulados sobre el 100% de la energía consumida, pero no el precio base de ese 10%.
*   **Facturación**: El coste de ese 10% se factura de forma privada y directa entre el Generador y Alumbra, fuera de OMIE/REE/MEFF.

---

## ⚙️ Reglas Técnicas de Procesamiento de Invoices

### 1. Deduplicación Estricta
*   Para evitar la doble contabilización por discrepancias en nombres de carpetas (`DD.MM.YY` frente a `YY.MM.DD` en Windows), el parser debe implementar un set de facturas ya procesadas (`seen_invoices = set()`).
*   Si el número de factura ya ha sido visto, se debe omitir de forma silenciosa para asegurar que los totales (como la C3) coincidan perfectamente con los cierres reales.

### 2. El Bug de Signos Contables (XML Post-2026)
*   **Regla Crítica**: A partir de **2026**, MEFF emite las facturas del tipo `Cobrar` (ingreso para Alumbra / Energía Vendida / Generación) con importes y volúmenes **positivos** en el XML.
*   **Acción del Parser**: Para mantener la contabilidad neta coherente, el parser debe forzar signo **negativo** (`* -1`) a los siguientes campos en cualquier XML de tipo `Cobrar` (documento de cobro):
    *   `Base_Imponible`
    *   `IVA`
    *   `Total`
    *   `Volumen_MWh`

### 3. Unificaciones de Cierres
*   Los cierres provisionales **C1 y C2** deben unificarse bajo una única categoría combinada **`C1+C2 (Provisionales)`** para evitar la sobrecarga visual y simplificar las comparativas mensuales con los cierres definitivos (C3).

---

## 💻 Arquitectura de Visualización y Dashboard

### 1. Estructura de Pestañas (Tabs)
*   **Tab 1 (Evolución General)**: Muestra el histórico acumulado financiero de Euros con IVA. Debe mantenerse simple e íntegro, sin dropdowns de cambio de métrica para proteger la perspectiva ejecutiva histórica.
*   **Tab 2 (Consumos por Cierres)**: Permite comparar volúmenes (MWh) o importes (€) agrupados por mes de devengo (`PeriodMonth`), unificando `C1+C2` e imputando el `Neto Total` (Compras - Ventas con IVA) para coincidir exactamente con el Tab 1.

### 2. Prevención de Errores JavaScript/CSS
*   **Error de IDs de Footer**: Verificar siempre la correspondencia exacta entre las celdas de pie de tabla HTML (ej. `fc12MWh`) y su manipulación en JS (evitando buscar `fcC12MWh` inexistentes que aborten la renderización).
*   **ChartJS Responsive**: El canvas debe envolverse en un contenedor relativo con dimensiones fijas (ej. `.chart-wrapper` con `height: 250px;`) y establecer `maintainAspectRatio: false` para que la carga en cuadrículas dinámicas no colapse el tamaño del gráfico.

---

## 🛠️ Scripts del Entorno
Los scripts operativos para la base de datos `meff_data.json` y compilación se encuentran en `Cierres Alumbra/MEFF/scripts/`:
*   `process_meff_invoices.py` - Extractor y parser con control de duplicados y signos.
*   `generate_final_dashboard.py` - Compilador HTML dinámico.

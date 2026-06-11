---
name: Analista Pass-Through España
description: Conocimiento experto sobre la estructura, facturación y validación de contratos eléctricos Pass-Through (Indexados) en España. Incluye fórmulas matemáticas, manejo de desfases horarios UTC/CET y un glosario completo de componentes de OMIE y REE (COMPODEM).
---

# 📊 Habilidad: Analista Pass-Through España

Esta habilidad te proporciona el contexto y la lógica de negocio necesarios para auditar, calcular y validar contratos eléctricos indexados (Pass-Through) en el mercado español.

Un contrato **Pass-Through** es aquel donde el cliente paga exactamente el coste de la energía en el mercado mayorista (OMIE) más los costes del sistema regulados por Red Eléctrica de España (REE), a los que la comercializadora añade un *fee* (margen de gestión) transparente.

---

## 1. La Fórmula de Facturación Pass-Through (Detallada)

La estructura matemática exacta para validar la sábana de facturación horaria (basada en el modelo de Alumbra/PowerTrader) es la siguiente:

```python
Precio_Final_Energia = (
    (
        (
            omie_kwh + ree_secx + ree_ct3 + ree_rad3 + ree_bs3 + ree_rt3 + 
            ree_rt6 + ree_in7 + ree_cfp + ree_balx + ree_dsv + ree_exd + 
            ree_fp1 + boe_om + boe_os + boe_pc + tp_fnee + tp_gdo + 
            tp_cayd + pc_fee / 1000
        ) * (1 + ree_per)
    ) * (1 + tp_taxmun) + boe_atrte + boe_cargote
)
```

### ⚠️ Puntos Críticos en Auditorías:
- **Tributación Local**: La Tasa Municipal (`tp_taxmun`) suele ser del 1.5% y aplica sobre el coste de energía + pérdidas.
- **Pérdidas (`ree_per`)**: REE publica un coeficiente de pérdidas horarias por tarifa. Hay que aplicarlo siempre multiplicando `(1 + ree_per)` a la suma de componentes antes de la tasa municipal.
- **Peajes y Cargos (`boe_atrte`, `boe_cargote`)**: Estos costes regulados se suman al final de la fórmula, después de impuestos municipales. Si no están desglosados en columnas independientes, no podrás llegar al precio final `qx_precio` solo sumando energía.
- **Coste de Gestión (`pc_fee`)**: El fee de comercialización puede ir en €/MWh. En la fórmula, se divide entre 1000 (`pc_fee/1000`) para pasarlo a €/kWh y sumarlo a los costes horarios.
- **Multiplicador Fiscal (IE + IVA)**: Sobre este `Precio_Final_Energia` se aplica el Impuesto Eléctrico (IE: 5,11269% habitualmente) y el IVA (21%). El multiplicador directo es `1.0511269 * 1.21 = 1.27186`.

---

## 2. Manejo del Tiempo (UTC vs Local)
Este es el error número uno en las validaciones de facturas:

1. **Sistemas de Facturación**: Las bases de datos y sábanas exportadas (Excel/CSV) suelen guardar las marcas de tiempo en **UTC**.
2. **Mercado Ibérico (OMIE/REE)**: Publican sus archivos (como el `COMPODEM` o `marginalpdbc`) en **hora local española (CET/CEST)**.

Para poder cruzar ambos mundos:
*   En invierno (UTC+1): Las `23:00 UTC` corresponden a las `00:00 Local` del día siguiente.
*   En verano (UTC+2): Las `22:00 UTC` corresponden a las `00:00 Local` del día siguiente.
*   **Regla de Oro**: Convierte siempre el Excel del cliente (UTC) a la zona horaria `Europe/Madrid` antes de cruzarlo con los archivos públicos.

---

## 3. Archivos COMPODEM (REE)

Los archivos `C2_compodem_YYYYMMDD` son documentos CSV delimitados por punto y coma (`;`).

**Estructura clave**:
`Fecha; Hora; Componente; TipoPerfil; Coste_Total; Energia_Total; Precio_EUR_MWh`

**Tipos de Perfilaje (`TipoPerfil`)**:
*   `TOTAL`: Media ponderada del sistema para ese componente.
*   `NOCUR`: Perfil No Curable (habitual en contratos indexados puros sin gestión de la demanda activa).
*   `CUR`: Perfil Curable.

**Conversión de unidades**: El precio de la última columna de REE suele estar en `€/MWh`. Debes dividirlo entre `1000` para tener `€/kWh` antes de sumarlo a la factura del cliente.

---

## 4. Diccionario de Segmentos (OMIE y REE)

Usa este glosario oficial cuando tengas que mapear columnas de la base de datos de mercado con el sistema de facturación:

### 🟢 Mercado OMIE
*   `[OMIE_MD]`: OMIE Mercado Diario
*   `[OMIE_AJOM]`: OMIE Mecanismo de ajuste
*   `[OMIE_MD_AVG]`: Valor medio mensual de OMIE Mercado Diario compuesto.

### 🔴 Red Eléctrica de España (REE) - Peninsular
*   `[REE_PERD]`: REE Pérdidas de transporte.
*   `[REE_BALX]`: REE Segmento BALX; Asignación de gestión de desvíos y terciaria (Gestión de desvíos).
*   `[REE_BS3]`: REE Segmento BS3; Banda secundaria CF;
*   `[REE_BS3DV]`: REE Segmento BS3DV; Coste medio de la banda de regulación secundaria repercutido a los desvíos de BRP.
*   `[REE_CFP]`: REE Segmento CFP; Control del factor de potencia.
*   `[REE_CT3]`: REE Segmento CT3; Proyecto Control de tensión (coste).
*   `[REE_DSV]`: REE Segmento DSV; Desvíos.
*   `[REE_CODSVBAJ]`: REE Segmento CODSVBAJ; Coste de los desvíos por menor producción o por mayor consumo.
*   `[REE_CODSVSUB]`: REE Segmento CODSVSUB; Coste de los desvíos por mayor producción o por menor consumo.
*   `[REE_EXD]`: REE Segmento EXD; Saldo desvíos.
*   `[REE_FP1]`: REE Segmento FP1; Precio medio horario del componente fallo nominación en las Unidades de Programación Genéricas.
*   `[REE_IN7]`: REE Segmento IN7; Saldo desvíos sistemas.
*   `[REE_MAJ3]`: REE Segmento MAJ3; Mecanismo ajuste RD-L10/2022 – Coste OS.
*   `[REE_MI]`: REE Segmento Sobrecoste Mercados Intradiarios.
*   `[REE_PC3]`: REE Segmento PC3; Pagos capacidad (Financiación).
*   `[REE_PS3]`: REE Segmento PS3; Reserva Subir Boste.
*   `[REE_RAD3]`: REE Segmento RAD3; Coste de servicio de respuesta activa.
*   `[REE_RT3]`: REE Segmento RT3; Restricciones PBF Coste.
*   `[REE_RT4]`: REE Segmento RT4; Precio medio horario del componente de las restricciones en el intradiario.
*   `[REE_RT6]`: REE Segmento RT6; Restricciones tiempo real (SC).
*   `[REE_SI3]`: REE Segmento SI3; Coste servicio interrumpibilidad.

### 🔵 Sistemas Extrapeninsulares (SEIE)
*   `[REE_SPHDEM]`: REE Segmento extrapeninsular; Precio horario de adquisición Ph demanda SEIE.
*   `[REE_SPHVEN]`: REE Segmento extrapeninsular; Precio horario de venta Ph venta SEIE.
*   `[REE_SPRGP]`: REE Segmento extrapeninsular; Pagos capacidad.
*   `[REE_SCDSVDEM]`: REE Segmento extrapeninsular; Coste medio desvíos.

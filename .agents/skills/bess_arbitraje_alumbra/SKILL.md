---
name: Arbitraje de Baterías y Peak-Shaving Alumbra (BESS)
description: Habilidad experta para modelar, simular y calcular la viabilidad económica de sistemas de almacenamiento detrás del contador (BESS) para Alumbra en España. Cubre arbitraje horario de activa, peak-shaving de potencia, fiscalidad eléctrica completa, pérdidas de red y el catálogo estándar de costes y financiación.
---

# 🔋 Habilidad: Arbitraje de Baterías y Peak-Shaving Alumbra (BESS)

Esta habilidad proporciona el marco de cálculo, la lógica matemática y las condiciones comerciales estándar para evaluar proyectos de baterías detrás del contador (Behind-The-Meter, BTM) para clientes residenciales y comerciales en España bajo el ecosistema de Alumbra.

---

## 1. Lógica del Arbitraje de Energía Activa Horaria

El arbitraje de energía consiste en cargar la batería en horas con precios de energía baratos (valle) y descargarla para autoabastecer al cliente en horas de precios caros (punta).

### ⚠️ El Efecto de la Fiscalidad Completa
Un error común es calcular el beneficio neto del cliente usando solo la diferencia de precios mayoristas en punto frontera (sin impuestos ni pérdidas). La batería reduce el consumo de red en horas punta, por lo que **evita el pago de todos los impuestos y pérdidas variables asociados a ese consumo**.

Para calcular el ahorro real final para el cliente, se debe aplicar el **multiplicador fiscal acumulado** sobre la diferencia horaria de precios:

*   **Impuesto Especial de la Electricidad (IE)**: Multiplicador regulado de `1,0511269` (5,11269%).
*   **IVA**: Generalmente del `21%` (multiplicador `1,21`).
*   **Tasa Municipal**: Habitualmente del `1,5%` (multiplicador `1,015`), aplicable sobre la energía consumida con pérdidas y peajes.

#### Multiplicador Fiscal Combinado (Activa)
$$Factor\_Impuestos = 1,0511269 \times 1,21 \times 1,015 = 1,290954$$

> [!NOTE]
> Al simular los ahorros en el algoritmo horario, cada kWh evitado en la hora punta ahorra al cliente final un **~29,1% extra** sobre el precio base de facturación gracias a la evasión legal de impuestos y tasas variables.

### Coeficiente de Pérdidas de Red y Eficiencia de la Batería
1.  **Pérdidas de Red (`ree_per`)**: En las bases de datos de clientes (sábanas de distribuidora), el precio unitario horario (`qx_precio`) ya suele incluir el término de pérdidas de REE. Si no es así, o si se trabaja con precios marginales puros de OMIE, se debe multiplicar el consumo por `(1 + ree_per)` antes de aplicar impuestos.
2.  **Eficiencia de Ciclo (Batería)**: Ninguna batería es perfecta. Se debe considerar una pérdida física en el proceso de carga/descarga (típicamente del **85%** de eficiencia global o `Round-Trip Efficiency = 0,85`). Esto significa que para inyectar 1 kWh en el consumo del cliente, la batería debe extraer de la red `1 / 0,85 = 1,176 kWh` durante las horas baratas.

---

## 2. Modelado de Peak-Shaving (Control de Excesos de Potencia)

En tarifas comerciales (2.0TD con excesos o 3.0TD), los clientes pagan penalizaciones severas si su demanda supera la potencia contratada en un cuarto de hora.

Las baterías permiten realizar **peak-shaving**:
*   La batería monitoriza la demanda total en tiempo real.
*   Si la demanda supera el umbral contratado, la batería aporta energía instantáneamente para recortar el pico.
*   **Ahorro Extra**: Además del arbitraje de energía, el cliente evita penalizaciones por excesos de potencia contratada (`Excesos_Pot_Anual_EUR`).

> [!TIP]
> Este efecto es el responsable de que clientes con perfiles de consumo muy picudos y penalizaciones elevadas (como Comunidades de Propietarios con ascensores o bombas de agua, p.ej. **CCPP Carril del Conde**) resulten extremadamente viables, logrando paybacks inferiores a 4 años, mientras que clientes con consumo plano o sin excesos tienen retornos más lentos.

---

## 3. Catálogo Estándar de Costes y Financiación BESS (Alumbra)

Para garantizar la coherencia en todos los estudios comerciales y modelos financieros de Alumbra, se debe aplicar un desglose detallado de costes basado en la capacidad de almacenamiento de energía (en kWh) y la potencia del inversor (en kW). 

> [!IMPORTANT]
> Los costes de **Baterías** y del **Inversor Deye híbrido** mostrados en la siguiente tabla pertenecen **exclusivamente a la marca Deye**. Para otras marcas homologadas (como EcoFlow, Fox-ESS, Livoltek o Hoymiles), se deben utilizar sus costes de equipos específicos (detallados en sus respectivas fichas de producto de la Sección 5 o parametrizados de forma independiente). Los costes de **Cabinet**, **Protecciones** y **Mano de Obra** son fijos y se aplican a todas las instalaciones de forma transversal.

### A. Tabla de Costes Base de Referencia (Sistema Deye)
La siguiente tabla muestra la estructura de costes base desglosada por componentes para los sistemas Deye estándar de **5 kWh**, **10 kWh** y **20 kWh**:

| Concepto | 5 kWh (5 kW) | 10 kWh (8 kW) | 20 kWh (12 kW 3F) |
| :--- | :---: | :---: | :---: |
| **Baterías Deye** (700 € / 5 kWh) | 700,00 € | 1.400,00 € | 2.800,00 € |
| **Cabinet** (Fijo Transversal) | 400,00 € | 400,00 € | 400,00 € |
| **Inversor Deye híbrido** | 1.100,00 € | 1.900,00 € | 2.180,00 € |
| **Protecciones** (Fijo Transversal) | 250,00 € | 250,00 € | 250,00 € |
| **Subtotal Materiales** | **2.450,00 €** | **3.950,00 €** | **5.630,00 €** |
| **Mano de obra** (35 €/h - Transversal) | 350,00 € (10h) | 560,00 € (16h) | 910,00 € (26h) |
| **TOTAL Deye (Material + M.O.)** | **2.800,00 €** | **4.510,00 €** | **6.540,00 €** |

### B. Lógica de Costes Fijos y Variables
Cuando realices cualquier cálculo de viabilidad económica o actualices plantillas de Excel, debes separar los costes en dos categorías:

1.  **Componentes Variables de Mercado (Baterías e Inversor)**: Los costes unitarios de los equipos cambian según la marca instalada. Los precios del sistema Deye (inicialmente 700 € por cada 5 kWh de batería y los costes indicados de inversor) sirven como referencia Deye, pero se parametrizan y modifican según el fabricante elegido.
2.  **Componentes Fijos del Modelo (Cabinet, Protecciones y Mano de Obra)**: Son transversales e independientes de la marca de los equipos. El coste del cabinet (400 €) y de las protecciones (250 €) es constante. La mano de obra se basa en los tiempos de instalación fijos de Alumbra (tasados a 35 €/h), interpolándose linealmente según la capacidad.

### C. Lógica de Interpolación y Extrapolación Lineal
Para calcular el coste de sistemas con capacidades diferentes a las estándar (por ejemplo, **40 kWh** o cualquier otra energía intermedia/superior), se debe realizar una interpolación o extrapolación lineal en base a los puntos de referencia de capacidad $E$ (en kWh):

#### 1. Fórmulas de Cálculo por Componente ($E$ = Capacidad en kWh):
*   **Cabinet ($C_{\text{cab}}$)**: Fijo.
    $$C_{\text{cab}} = 400,00\ \text{€}$$
*   **Protecciones ($C_{\text{prot}}$)**: Fijo.
    $$C_{\text{prot}} = 250,00\ \text{€}$$
*   **Mano de Obra ($C_{\text{mo}}$)**:
    *   Si $5 \le E \le 10$: $C_{\text{mo}} = 350 + 42 \times (E - 5)\ \text{€}$
    *   Si $10 \le E \le 20$: $C_{\text{mo}} = 560 + 35 \times (E - 10)\ \text{€}$
    *   Si $E > 20$: $C_{\text{mo}} = 910 + 35 \times (E - 20)\ \text{€}$
*   **Baterías ($C_{\text{bat}}$)**:
    $$C_{\text{bat}} = 140 \times E\ \text{€}$$ (o valor unitario parametrizado $\times E$)
*   **Inversor ($C_{\text{inv}}$)**:
    *   Si $5 \le E \le 10$: $C_{\text{inv}} = 1.100 + 160 \times (E - 5)\ \text{€}$
    *   Si $10 \le E \le 20$: $C_{\text{inv}} = 1.900 + 28 \times (E - 10)\ \text{€}$
    *   Si $E > 20$: $C_{\text{inv}} = 2.180 + 28 \times (E - 20)\ \text{€}$

#### 2. Ejemplo práctico: Caso 40 kWh
Aplicando las fórmulas de extrapolación para un sistema de $E = 40\ \text{kWh}$:
*   $C_{\text{bat}} = 140 \times 40 = 5.600,00\ \text{€}$
*   $C_{\text{cab}} = 400,00\ \text{€}$
*   $C_{\text{inv}} = 2.180 + 28 \times (40 - 20) = 2.740,00\ \text{€}$
*   $C_{\text{prot}} = 250,00\ \text{€}$
*   $C_{\text{mo}} = 910 + 35 \times (40 - 20) = 1.610,00\ \text{€}$ (corresponde a 46 horas)
*   **TOTAL Base (Material + M.O.)** = 5.600 + 400 + 2.740 + 250 + 1.610 = **10.600,00 €**

### D. Margen Turnkey (Llave en Mano) y Financiación
Alumbra aplica un **15% de margen comercial** sobre el TOTAL (Material + M.O.) para entregar el servicio "Llave en Mano":

| Capacidad Batería | Coste Base (Material + M.O.) | Coste Llave en Mano (15% Margen) | Margen Alumbra |
| :---: | :---: | :---: | :---: |
| **5 kWh** | 2.800,00 € | **3.220,00 €** | 420,00 € |
| **10 kWh** | 4.510,00 € | **5.186,50 €** | 676,50 € |
| **20 kWh** | 6.540,00 € | **7.521,00 €** | 981,00 € |
| **40 kWh** | 10.600,00 € | **12.190,00 €** | 1.590,00 € |

#### Condiciones de Financiación (Amortización Francesa)
Para compra financiada a 5 años (`n = 5`) con un TIN del 8% (`r = 0,08`):
*   **Fórmula de Amortización**:
    $$Cuota\_Anual = Cap \times \frac{r \times (1+r)^n}{(1+r)^n - 1} \approx Cap \times 0,250456$$
*   **Cuotas Resultantes (Llave en Mano Financiado)**:
    *   **5 kWh**: **`806,47 €/año`** (`67,21 €/mes`).
    *   **10 kWh**: **`1.298,99 €/año`** (`108,25 €/mes`).
    *   **20 kWh**: **`1.883,68 €/año`** (`156,97 €/mes`).
    *   **40 kWh**: **`3.053,06 €/año`** (`254,42 €/mes`).

---

## 4. Efectos del Mercado y Estacionalidad (OMIE)

Al presentar estudios a los clientes, se debe tener en cuenta el impacto de la estacionalidad en la viabilidad del negocio:
*   **Primavera (Abril/Mayo)**: La alta generación hidráulica y solar en España suele deprimir y aplanar los precios diarios de OMIE (muchas horas a 0 €/MWh o muy cercanas). Esto **reduce la dispersión horaria** y, por ende, el margen del arbitraje.
*   **Invierno (Diciembre a Febrero)**: La menor generación solar y la mayor demanda térmica elevan y polarizan los precios, creando grandes diferencias entre el mediodía (solar) o la madrugada y las horas punta de tarde/noche. Aquí es donde el BESS captura su **máxima rentabilidad**.

---

## 5. Fichas Técnicas Evaluadas y Viabilidad de Equipos

Cuando evalúes equipos físicos de almacenamiento (BESS) para los estudios de Alumbra, utiliza los siguientes criterios técnicos y de integración derivados de las fichas de producto homologadas:

### A. EcoFlow PowerOcean Monofásico (Inversor Híbrido + Batería LFP)
*   **Módulos de Batería LFP (EF BD-5.1-S1)**: 5,1 kWh nominales por módulo. Capacidad útil de 4,8 kWh (95% DoD).
*   **Curva de Potencia Carga/Descarga**:
    *   **1 módulo**: Carga máx. 2,5 kW / Descarga máx. 3,3 kW.
    *   **2 módulos**: Carga máx. 5,0 kW / Descarga máx. 6,6 kW.
    *   **3 módulos**: Carga máx. 7,5 kW / Descarga máx. 9,9 kW.
*   **Inversor Híbrido (EF HD-P1-*)**: Modelos de 3 kW, 3,68 kW, 4,6 kW, 5 kW y 6 kW. Tensión nominal del sistema de batería de 790 VCC (Alta Tensión). Eficiencia máxima >96,5% / europea >96%.
*   **Escalabilidad**: Soporta hasta 15,3 kWh por inversor híbrido. Permite la **conexión en cascada de hasta 3 inversores** para alcanzar una capacidad total de hasta **45 kWh**.
*   **Viabilidad de Control (API)**: **100% Viable y Recomendado**. Su plataforma de comunicación (RS485, CAN, Wi-Fi, Bluetooth y WAN/4G integrado) y el portal Pro permiten la integración de APIs externas locales (Modbus TCP) y en la nube para enviar comandos de carga/descarga dinámica en tiempo real.
*   **Evaluación para Alumbra**: Es la opción idónea. Cubre perfectamente todos los escalones de potencia estudiados (5, 10, 20 y 40 kW) de manera modular y escalable.

### B. HYX-MS-3000AC (Hypontech / HYX Power - Acoplado en CA)
*   **Batería base**: Módulo LiFePO4 de 3.014,4 Wh (3,01 kWh) a 9,6 V de tensión nominal.
*   **Ciclo de Vida Extremo**: **≥10.000 ciclos** (@25°C, 60% EOL). Durabilidad sobresaliente para arbitraje diario intensivo.
*   **Inversor Bidireccional Integrado**: Salida máxima de 3.000 VA (3 kW) con batería de expansión (1.500 VA en módulo base).
*   **Instalación y Protección**: Plug & Play (acoplado en CA). Protección IP66 (ideal para exteriores). Batería autocalefactada para arranque y funcionamiento óptimo hasta -20°C.
*   **Escalabilidad**: Expansión física por apilamiento directo (sin cables externos) hasta **18,08 kWh** (6 módulos).
*   **Viabilidad de Control (API)**: **Parcialmente Viable**. Ofrece conectividad Wi-Fi y Bluetooth, además de integración con medidores externos (Shelly). Permite optimización de carga/descarga basada en precios de mercado a través de su plataforma en la nube, pero Alumbra debe verificar si el tiempo de respuesta de su API Cloud es lo suficientemente rápido para aplicaciones de peak-shaving rápido en excesos de potencia de red.
*   **Evaluación para Alumbra**: Excelente opción para proyectos residenciales y retrofits comerciales de tamaño pequeño o mediano. Sin embargo, su **límite físico de 18,08 kWh de capacidad y 3 kW de salida por sistema impide cubrir de forma integrada los escalones de 20 kW y 40 kW** sin recurrir a costosos sistemas en paralelo múltiple.

### C. Livoltek iPower AES1 (Monofásico - Acoplado en CA Todo en Uno)
*   **Batería**: Química LFP en baja tensión (40-60 V).
*   **Inversor Integrado**: Modelos de 3 kW, 3,68 kW, 4,6 kW y 5 kW nominales. Eficiencia máxima 94% / europea 93,50% (eficiencia inferior a EcoFlow).
*   **Respaldo (EPS)**: Tiempo de conmutación muy rápido (<10 ms) hasta 5 kW de carga de respaldo.
*   **Escalabilidad**: Limitada. La ficha técnica especifica un máximo de **1 unidad de inversor en paralelo**, lo que bloquea el escalado a potencias industriales o comerciales.
*   **Viabilidad de Control (API)**: **NO VIABLE (Descartado para control dinámico)**. Aunque tiene buenos componentes físicos y un excelente sistema de respaldo, la **imposibilidad de interactuar dinámicamente con el inversor a través de una API abierta** impide la automatización del arbitraje energético y el peak-shaving horario en Alumbra.
*   **Evaluación para Alumbra**: Útil únicamente como referencia de costes o para proyectos puramente autoconsumo solar pasivo sin gestión activa de la demanda.

### D. Fox-ESS (Inversores FV/Híbridos + Baterías de Litio LFP de Alta Tensión)
*   **Inversores Fotovoltaicos (FV)**:
    *   **Monofásicos (Serie S - G2, Serie G, Serie F - G2)**: Inversores residenciales compactos. Modelos como el S(G2) y F(G2) vienen con guías y manuales de usuario en español y certificados de red NTS Tipo A (p.ej. *2622_0287_1_CER_NTS_TypeA.pdf*).
    *   **Trifásicos (Serie T - G3, Serie R)**: Inversores residenciales e industriales trifásicos de alta eficiencia para conexión a red.
*   **Inversores Híbridos (Serie KH / KA)**: Inversores residenciales monofásicos preparados para almacenamiento acoplado en CC o CA en alta tensión.
*   **Baterías de Litio (Serie ECS - Energy Cube)**:
    *   **Modelos de Módulo**: ECS2800, ECS2900, ECS4100, ECS4300H y ECS4800.
    *   **Química y Estructura**: Celdas de LiFePO4 (LFP) con diseño modular apilable en torre, facilitando la instalación sin cableados externos de comunicación y fuerza entre módulos.
    *   **Garantía**: **10 años de garantía oficial del fabricante** (regulada bajo la póliza oficial *ES-ECS-warranty-20250704.pdf*).
*   **Cargadores de EV (Serie A)**: Cargador de coche eléctrico integrable para control de excedentes junto a la generación fotovoltaica.
*   **Viabilidad de Control (API)**: **100% Viable (Altamente Recomendado)**. Fox-ESS ofrece una API REST abierta (OpenAPI Cloud) y Modbus TCP para control local. A través de la API es posible monitorizar y comandar de forma dinámica parámetros como:
    *   **Lectura en tiempo real**:SOC, SOH, producción fotovoltaica (`pvPower`), cargas del hogar (`loadsPower`), potencia de batería (`batPower`) e importación/exportación de red (`gridPower`).
    *   **Configuración de SOC**: Modificación del SOC de reserva (`minSoc` y `minSocOnGrid`).
    *   **Carga Forzada (`ForceCharge`)**: Programación horaria para recarga obligatoria desde la red en periodos supervalle.
    *   **Descarga Forzada (`ForceDischarge`)**: Configuración de ventanas horarias con potencia de exportación o consumo objetivo determinada (`fdPwr` en vatios) ideal para arbitraje y peak-shaving en horas pico.
*   **Evaluación para Alumbra**: **Opción excelente**. Su modularidad y flexibilidad técnica son ideales para los escalones de baterías de Alumbra (5, 10, 20 y 40 kW) y la compatibilidad con su API permite integrar de forma óptima los algoritmos dinámicos de ahorro energético y peak-shaving.

---

## 6. Implementación del Algoritmo de Simulación Horaria (Python)

Cuando programes o refactors scripts de simulación horaria, utiliza esta lógica base para calcular la carga/descarga y el ahorro fiscalizado acumulado de la batería:

```python
import numpy as np

def simular_arbitraje_bess(curva_demanda, curva_precios, capacidad_kwh, potencia_kw, eficiencia=0.85):
    """
    Simulación simplificada de carga en horas más baratas y descarga en horas más caras.
    """
    n_horas = len(curva_demanda)
    bateria_soc = 0.0  # Estado de carga inicial (State of Charge)
    ahorro_energia_eur = 0.0
    coste_carga_eur = 0.0
    
    # Identificar percentiles para definir umbrales dinámicos de carga y descarga
    precio_umbral_carga = np.percentile(curva_precios, 25)  # 25% más barato
    precio_umbral_descarga = np.percentile(curva_precios, 75)  # 25% más caro
    
    # Factores fiscales combinados
    FACTOR_IMPUESTOS = 1.0511269 * 1.21 * 1.015  # IE * IVA * Tasa Municipal
    
    for t in range(n_horas):
        precio_t = curva_precios[t]  # Precio de la energía en €/kWh (incluye pérdidas de red)
        demanda_t = curva_demanda[t]
        
        # Modo Carga: Horas baratas y batería no llena
        if precio_t <= precio_umbral_carga and bateria_soc < capacidad_kwh:
            energia_cargar = min(potencia_kw, capacidad_kwh - bateria_soc)
            bateria_soc += energia_cargar * eficiencia  # Consideramos eficiencia en carga
            coste_carga_eur += energia_cargar * (precio_t * FACTOR_IMPUESTOS)
            
        # Modo Descarga: Horas caras, batería con carga y hay demanda
        elif precio_t >= precio_umbral_descarga and bateria_soc > 0 and demanda_t > 0:
            energia_descargar = min(potencia_kw, bateria_soc, demanda_t)
            bateria_soc -= energia_descargar
            # Ahorro neto al evitar consumir energía de la red a precio caro de punta
            ahorro_energia_eur += energia_descargar * (precio_t * FACTOR_IMPUESTOS)
            
    ahorro_neto_eur = ahorro_energia_eur - coste_carga_eur
    return ahorro_neto_eur
```


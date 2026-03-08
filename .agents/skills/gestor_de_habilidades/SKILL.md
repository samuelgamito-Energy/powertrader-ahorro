---
name: Gestor de Habilidades
description: Utiliza esta habilidad para crear, mejorar o refactorizar habilidades (skills) en el espacio de trabajo. Proporciona instrucciones detalladas sobre el ciclo de vida completo de una habilidad de Antigravity.
---

# Gestión de Habilidades en Antigravity

Esta habilidad guía al asistente en todo el ciclo de vida de las "Habilidades" (Skills): desde su creación inicial hasta su mejora continua y optimización.

## Estructura de una Habilidad

Cada habilidad debe residir en su propia carpeta dentro del directorio de habilidades del espacio de trabajo. La estructura estándar es:

```
nombre_de_la_habilidad/
├── SKILL.md           # Instrucciones y metadatos (Obligatorio)
├── scripts/           # Scripts de soporte (Python, JS, etc.)
└── resources/         # Archivos de datos, ejemplos o plantillas
```

### El Archivo SKILL.md

Este archivo es el núcleo de la habilidad. Debe contener:

1.  **Frontmatter YAML**: Delimitado por `---`.
    - `name`: Nombre descriptivo.
    - `description`: Cuándo y por qué usar esta habilidad.
2.  **Cuerpo del Markdown**: Instrucciones lógicas, ejemplos de entrada/salida y mejores prácticas.

---

## Flujo de Trabajo

### 1. Creación de una Nueva Habilidad
Cuando el usuario pida una nueva capacidad:
- **Planificación**: Define el alcance y las instrucciones necesarias.
- **Carpeta**: Crea la carpeta en `snake_case`.
- **SKILL.md**: Redacta instrucciones claras, manteniendo el idioma del usuario (español).
- **Modularidad**: Si hay lógica compleja, extráela a `scripts/`.

### 2. Mejora de una Habilidad Existente
Cuando se requiera optimizar o expandir una habilidad:
- **Análisis**: Lee el `SKILL.md` actual e identifica puntos de mejora (ambigüedades, falta de ejemplos, redundancias).
- **Refactorización**: Aplica el principio **DRY** (Don't Repeat Yourself). Consolida lógica si varias habilidades comparten reglas.
- **Expansión**: Añade nuevas secciones o capacidades manteniendo la coherencia con el patrón original.
- **Actualización de Versión**: Si existe un sistema de versiones, increméntalo.

---

## Mejores Prácticas y Patrones

- **Claridad Atómica**: Cada instrucción debe ser una acción clara. Evita párrafos densos.
- **Ejemplos Reales**: Incluye bloques de código o interacciones de ejemplo para que la IA entienda el contexto.
- **Jerarquía**: Usa encabezados `#`, `##`, `###` para organizar la complejidad.
- **Nomenclatura**: Carpetas en `snake_case`, archivos en `UPPER_CASE` o `snake_case` según consistencia.
- **Idioma**: Las instrucciones deben estar en el idioma en el que el asistente interactúa habitualmente con el usuario.

## Ejemplo de Frontmatter

```yaml
---
name: Analizador de Datos
description: Se activa cuando el usuario proporciona CSVs para análisis estadístico.
---
```

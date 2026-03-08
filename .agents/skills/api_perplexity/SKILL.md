---
name: API Perplexity
description: Capacidad para interactuar con la API de Perplexity. Proporciona instrucciones y scripts listos para usar para enviar consultas a los modelos de Perplexity y procesar sus respuestas.
---

# API de Perplexity

Esta habilidad establece el estándar para que interactuemos autónomamente o a petición del usuario con la API de Perplexity. Permite delegar tareas de búsqueda, razonamiento profundo y generación de contenido actualizado a los modelos de Perplexity (como `sonar-reasoning`, `sonar-pro`).

## Estructura de la Habilidad

```text
api_perplexity/
├── SKILL.md                 # Instrucciones y metadatos (este archivo)
└── scripts/
    └── perplexity_client.py   # Script en Python de ejemplo y utilidad
```

## Requisitos Previos

1.  **Clave de API (API Key)**: Es imprescindible contar con una API Key válida de Perplexity. Debe pasarse como parámetro o estar configurada como variable de entorno (`PERPLEXITY_API_KEY`).
2.  **Librerías (Python)**: Si se utiliza el script de Python, hay que asegurarse de que el entorno tenga instalada la librería `requests` (puedes instalarla temporalmente si hace falta: `pip install requests`).

## Flujo de Trabajo para Usar Perplexity

1.  **Definir el Prompt**: Establece el objetivo exacto de la consulta a Perplexity.
2.  **Selección de Modelo**:
    *   Usa `sonar-reasoning` para tareas que requieran pensamiento matemático, lógico o validación profunda.
    *   Usa `sonar-pro` o `sonar` para investigaciones generales en internet o consultas más sencillas y rápidas.
3.  **Ejecución**: Usa el script en Python proporcionado, o comandos directamente como `curl` a través de la interfaz de comandos para enviar la consulta usando la API Key.
4.  **Procesamiento**: Captura la salida estándar del terminal o lee el archivo de respuesta generado y utilízalo para continuar de manera autónoma con la tarea del usuario.

## Ejemplo de Petición cURL Nativa

Si necesitas hacer una prueba rápida o no tienes el entorno configurado:

```bash
curl --request POST \
  --url https://api.perplexity.ai/chat/completions \
  --header 'Authorization: Bearer <TU_API_KEY>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "sonar-pro",
    "messages": [
      {
        "role": "system",
        "content": "Eres un asistente de investigación preciso."
      },
      {
        "role": "user",
        "content": "¿Cuáles son las últimas novedades en IA generativa?"
      }
    ]
  }'
```

## Scripts Disponibles

En la carpeta `scripts/` encontrarás herramientas listas para ser ejecutadas:
- `perplexity_client.py`: Recibe el prompt como argumento de terminal y devuelve únicamente el string de respuesta (lo que facilita su uso programático o su envío a otras variables).

Uso:
```bash
python .agents/skills/api_perplexity/scripts/perplexity_client.py "¿Quién ganó la liga en 2024?" "tu_api_key_aqui (opcional si existe env var)" "sonar-pro"
```

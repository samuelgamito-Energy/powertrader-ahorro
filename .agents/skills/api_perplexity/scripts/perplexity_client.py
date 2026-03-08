import os
import requests
import sys

def query_perplexity(prompt, api_key, model="sonar-pro"):
    """Enviar una petición a la API de Perplexity y devolver la respuesta de texto."""
    url = "https://api.perplexity.ai/chat/completions"
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Eres un investigador avanzado. Proporciona respuestas precisas y estructuradas."},
            {"role": "user", "content": prompt}
        ]
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        error_info = e.response.text
        return f"ERROR HTTP {status_code}: {error_info}"
    except Exception as e:
        return f"ERROR: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python perplexity_client.py \"<prompt>\" [api_key] [model]")
        sys.exit(1)
        
    prompt = sys.argv[1]
    
    # Intentar obtener la API Key de los argumentos, o de la variable de entorno
    api_key = sys.argv[2] if len(sys.argv) > 2 else os.environ.get("PERPLEXITY_API_KEY")
    
    if not api_key:
        print("ERROR: No se encontró PERPLEXITY_API_KEY. Pásala como segundo argumento o configúrala en el entorno.")
        sys.exit(1)
        
    model = sys.argv[3] if len(sys.argv) > 3 else "sonar-pro"
    
    # Imprimir solo la respuesta para facilitar la captura desde bash/powershell
    respuesta = query_perplexity(prompt, api_key, model)
    print(respuesta)

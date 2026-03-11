import os
import re
import json
import asyncio
import glob
import requests
from playwright.async_api import async_playwright
from datetime import datetime

# Configuración desde variables de entorno (GitHub Secrets)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_latest_post_data():
    """Busca el último post de ahorro en el repo y extrae fecha y precios."""
    posts_dir = "content/posts"
    files = glob.glob(os.path.join(posts_dir, "*.md"))
    if not files:
        print("No se encontraron posts en", posts_dir)
        return None, None
    
    # Ordenar por fecha de modificación o nombre (los informes llevan fecha en el nombre)
    files.sort(reverse=True)
    latest_file = files[0]
    print(f"Usando datos de: {latest_file}")
    
    with open(latest_file, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Extraer fecha_tarjeta
    fecha_match = re.search(r'fecha_tarjeta:\s*"(.*?)"', content)
    fecha = fecha_match.group(1) if fecha_match else "Fecha desconocida"
    
    # Extraer precios_array (puede venir como literal [1,2] o como string "[1,2]" por errores de GAS)
    precios_match = re.search(r'precios_array:\s*\"?(\[.*?\])\"?', content)
    precios_json = precios_match.group(1) if precios_match else "[]"
    
    return fecha, precios_json

async def main():
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ Error: Faltan credenciales de Telegram.")
        return

    fecha, precios_json = get_latest_post_data()
    if not fecha or precios_json == "[]":
        print("⚠️ No hay datos válidos para procesar.")
        return

    # Ruta del template (suponemos que estamos en la raíz del repo)
    template_path = os.path.abspath("static/social-template.html")
    output_image = "social_card.png"

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Cargar el HTML local
        await page.goto(f"file://{template_path}")
        
        # Inyectamos los datos y disparamos el renderizado interno del HTML
        await page.evaluate(f'''() => {{
            const p = {precios_json};
            const f = "{fecha}";
            
            // Actualizar la fecha en el badge
            const badge = document.querySelector('.badge');
            if (badge) badge.innerText = f;
            
            // Llamar a la función de renderizado unificada del HTML
            if (typeof updateAllData === 'function') {{
                updateAllData(p);
            }}
        }}''')
        
        # Esperar un momento para el render de Chart.js
        await asyncio.sleep(2)
        
        # Capturar el contenedor
        container = page.locator(".container")
        await container.screenshot(path=output_image)
        await browser.close()
        print(f"✅ Imagen generada: {output_image}")

    # Enviar a Telegram
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    caption = f"<b>⚡ Guía de Ahorro Diaria</b>\n\nAquí tienes la tarjeta para las Redes Sociales de mañana ({fecha}).\n\n#PowerAhorro #PVPC"
    
    with open(output_image, "rb") as photo:
        files = {"photo": photo}
        data = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption, "parse_mode": "HTML"}
        r = requests.post(url, files=files, data=data)
        
    if r.status_code == 200:
        print("🚀 ¡Tarjeta enviada a Telegram con éxito!")
    else:
        print(f"❌ Error al enviar a Telegram: {r.text}")

if __name__ == "__main__":
    asyncio.run(main())

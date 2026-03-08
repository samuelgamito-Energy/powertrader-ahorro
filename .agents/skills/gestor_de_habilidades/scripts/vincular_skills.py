import os
import subprocess

# Localización central de skills en Antigravity
ROOT_SKILLS = r"c:\Users\SAMUEL\Desktop\Antigravity\.agents\skills"
BASE_DIR = r"c:\Users\SAMUEL\Desktop\Antigravity"
SITIOS_DIR = os.path.join(BASE_DIR, "sitios_powertrader")

def vincular_carpeta(target_path):
    """Crea una unión de directorio (junction) hacia las skills centrales."""
    if target_path.lower() == ROOT_SKILLS.lower() or target_path.lower() == os.path.dirname(ROOT_SKILLS).lower():
        return
    if ".agents" in os.path.split(target_path)[1]:
        return

    target_agents = os.path.join(target_path, ".agents")
    target_skills = os.path.join(target_agents, "skills")
    
    if not os.path.exists(target_agents):
        os.makedirs(target_agents, exist_ok=True)

    if os.path.exists(target_skills):
        # Verificar si ya apunta al sitio correcto
        try:
            cmd = ['cmd', '/c', 'dir', '/al', target_skills]
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
            if ROOT_SKILLS.lower() in result.stdout.lower():
                return # Ya está correcto
        except:
            pass
        
        # Si no es correcto, borrar para recrear
        try:
            subprocess.run(['cmd', '/c', 'rmdir', '/s', '/q', target_skills], check=True)
        except:
            try: os.remove(target_skills)
            except: pass

    try:
        # mklink /j es el comando estándar para juntas de directorio en Windows
        subprocess.run(['cmd', '/c', 'mklink', '/j', target_skills, ROOT_SKILLS], check=True, capture_output=True)
        print(f"Vinculado: {target_path}")
    except Exception as e:
        print(f"Error vinculando {target_path}: {e}")

def sincronizar_todo():
    """Escanea y vincula todas las carpetas conocidas del ecosistema."""
    # Carpetas directas en Antigravity
    for item in os.listdir(BASE_DIR):
        p = os.path.join(BASE_DIR, item)
        if os.path.isdir(p) and item.lower() != ".agents":
            vincular_carpeta(p)

    # Subcarpetas en sitios_powertrader
    if os.path.exists(SITIOS_DIR):
        for item in os.listdir(SITIOS_DIR):
            p = os.path.join(SITIOS_DIR, item)
            if os.path.isdir(p):
                vincular_carpeta(p)

if __name__ == "__main__":
    sincronizar_todo()

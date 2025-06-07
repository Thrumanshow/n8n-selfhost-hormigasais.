import os
import requests
import subprocess
from datetime import datetime, timedelta

# Configuración - ajustar según cada repo
WEBHOOK_URL = "http://localhost:5678/webhook"  # ejemplo, cambia al endpoint real
LOG_FILE_PATH = "./logs/n8n.log"  # ruta de log a verificar
SERVICE_NAME = "n8n"  # servicio a revisar

def check_service_running(service_name):
    """Verifica si un proceso está activo en el sistema."""
    try:
        output = subprocess.check_output(['pgrep', '-f', service_name]).decode()
        if output.strip():
            return True
        return False
    except subprocess.CalledProcessError:
        return False

def check_log_for_errors(log_path, minutes=10):
    """Revisa el log para encontrar errores en los últimos 'minutes' minutos."""
    if not os.path.exists(log_path):
        return False, "Archivo de log no encontrado."

    cutoff_time = datetime.now() - timedelta(minutes=minutes)
    errors = []
    with open(log_path, 'r') as f:
        for line in f:
            # Suponiendo que el log tiene timestamp al inicio tipo: '2025-06-07T12:34:56 ...'
            if line.strip():
                try:
                    timestamp_str = line.split()[0]
                    timestamp = datetime.fromisoformat(timestamp_str)
                    if timestamp >= cutoff_time and ("error" in line.lower() or "fail" in line.lower()):
                        errors.append(line.strip())
                except Exception:
                    # Si no puede parsear, ignora la línea
                    pass
    return (len(errors) == 0), errors

def check_webhook(url):
    """Hace un ping simple al webhook para verificar disponibilidad."""
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200, response.status_code
    except requests.RequestException as e:
        return False, str(e)

def main():
    print("----- Monitor HormigasAIS -----")

    # Check servicio
    running = check_service_running(SERVICE_NAME)
    print(f"[Servicio {SERVICE_NAME}] {'Activo' if running else 'No activo'}")

    # Check logs
    logs_ok, errors = check_log_for_errors(LOG_FILE_PATH)
    if logs_ok:
        print(f"[Logs] Sin errores recientes.")
    else:
        print(f"[Logs] Errores detectados:\n" + "\n".join(errors))

    # Check webhook
    webhook_ok, detail = check_webhook(WEBHOOK_URL)
    if webhook_ok:
        print(f"[Webhook] Respondiendo correctamente (Status {detail}).")
    else:
        print(f"[Webhook] Problema detectado: {detail}")

    # Conclusión
    if running and logs_ok and webhook_ok:
        print("\n✅ Estado: TODO FUNCIONA CORRECTAMENTE")
    else:
        print("\n⚠️ Estado: HAY PROBLEMAS QUE REVISAR")

if __name__ == "__main__":
    main()

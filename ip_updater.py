import requests
import json
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

# Configura tus credenciales y datos
load_dotenv()
IONOS_API_KEY = os.getenv("IONOS_API_KEY")
IONOS_API_URL = "https://api.hosting.ionos.com/dns/v1"
DOMAIN = "infinitwheelsinline.es"  # El dominio que tienes en IONOS
DNS_TYPE = "A"
LOG_DIR = os.getenv("LOG_DIR")
LAST_IP_FILE = "/home/roman/Workspace/ip_updater/.ultima_ip"
IP_QUERY_SERVER = "http://ipv4.icanhazip.com"  # Servidor para obtener la IP pública
DEFAULT_HEADER = {
    "X-API-Key": IONOS_API_KEY,
    "Content-Type": "application/json"
}

def configurar_logging():
    # Configura el directorio de logs
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    # Configura el nombre del archivo de log
    log_filename = os.path.join(LOG_DIR, f"ip_updater_{datetime.now().strftime('%Y-%m-%d')}.log")
    
    # Configura el logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )

# Función para obtener la IP pública
def obtener_ip_publica():
    response = requests.get(IP_QUERY_SERVER)
    return response.text.strip()

# Verifica si la IP ha cambiado desde la última actualización
def obtener_ultima_ip_archivo():
    if os.path.isfile(LAST_IP_FILE):
        with open(LAST_IP_FILE, "r") as f:
            return f.read().strip()
    else:
        return None

def obtener_ultima_ip():
    id_zona = obtener_id_zona()
    # Realiza la solicitud GET para obtener las zonas DNS
    url_zonas_registro = f"{IONOS_API_URL}/zones/{id_zona}?recordType={DNS_TYPE}"
    response = requests.get(url_zonas_registro, headers=DEFAULT_HEADER)
    ip = response.json()["records"][0]["content"]
    return ip

def diferente_ip():
    return obtener_ip_publica() != obtener_ultima_ip()

# Función para obtener el identificador de la zona DNS
def obtener_id_zona():
    # Realiza la solicitud GET para obtener las zonas DNS
    url_zonas = f"{IONOS_API_URL}/zones"
    response = requests.get(url_zonas, headers=DEFAULT_HEADER)
    if response.status_code == 200:
        zonas = response.json()
        for zona in zonas:
            if zona['name'] == DOMAIN:
                return zona['id']
    else:
        logging.error(f"Error al obtener las zonas: {response.status_code} - {response.text}")
        return None

# Función para obtener el identificador de registro DNS
def obtener_id_registro(id_zona):
    # Realiza la solicitud GET para obtener las zonas DNS
    url_zonas_registro = f"{IONOS_API_URL}/zones/{id_zona}?recordType={DNS_TYPE}"
    response = requests.get(url_zonas_registro, headers=DEFAULT_HEADER)

    registros = []
    if response.status_code == 200:
        zona = response.json()
        for registro in zona["records"]:
            registros.append(registro['id'])

        return registros
    else:
        logging.error(f"Error al obtener los registros DNS: {response.status_code} - {response.text}")
        return None

# Función para actualizar el DNS en IONOS
def actualizar_registro(ip_publica, id_zona, id_registro):
    # Datos de la actualización
    data = {        
        "disabled": "false",
        "content": ip_publica,
        "ttl": 3600,
        "prio": 0
    }

    # URL de la API usando el identificador de la zona
    url = f"{IONOS_API_URL}/zones/{id_zona}/records/{id_registro}"
    response = requests.put(url, headers=DEFAULT_HEADER, data=json.dumps(data))
    
    # Log de la respuesta completa para depuración
    logging.info(f"URL: {url}")
    logging.info(f"Response Status Code: {response.status_code}")
    logging.info(f"Response Text: {response.text}")
    
    if response.status_code == 200:
        logging.info(f"DNS actualizado correctamente a la IP {ip_publica}")
        # Guarda la nueva IP
        with open(LAST_IP_FILE, "w") as f:
            f.write(ip_publica)
    else:
        logging.error(f"Error al actualizar el DNS: {response.status_code} - {response.text}")

def actualizar_dns():
    id_zona = obtener_id_zona()
    ip_publica = obtener_ip_publica()

    if id_zona:
        for id_registro in obtener_id_registro(id_zona):
            actualizar_registro(ip_publica, id_zona, id_registro)
    else:
        logging.error("No se pudo obtener el identificador de la zona.")


def main():
    configurar_logging()
    ip_publica = obtener_ip_publica()
    ultima_ip = obtener_ultima_ip()

    if diferente_ip():
        logging.info(f"La IP ha cambiado de {ultima_ip} a {ip_publica}. Actualizando DNS en IONOS...")
        actualizar_dns()

    else:
        logging.info(f"La IP sigue siendo la misma: {ip_publica}")

if __name__ == "__main__":
    main()

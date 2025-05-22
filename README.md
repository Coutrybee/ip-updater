# ip_updater

Este proyecto es una herramienta para actualizar de forma automática los registros DNS de un dominio en IONOS con la dirección IP pública actual de tu red local, utilizando una Raspberry Pi o cualquier dispositivo similar.

## Características

- Actualiza automáticamente la dirección IP pública en los registros DNS de IONOS.
- Utiliza una Raspberry Pi como servidor para ejecutar el script.
- Guarda registros de actividad en archivos de log diarios.
- Maneja el almacenamiento de logs y la eliminación automática de logs antiguos.

## Requisitos

- Raspberry Pi o dispositivo similar con Linux.
- Python 3.x.
- Acceso a la API de IONOS (requiere una clave API válida).
- Dependencias necesarias de Python: `requests`.

## Instalación

### 1. Clona el repositorio

Para obtener una copia local del proyecto, clona el repositorio:

```bash
git clone https://github.com/tu_usuario/ip_updater.git
cd ip_updater

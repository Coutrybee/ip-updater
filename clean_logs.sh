#!/bin/bash
PROJECT_DIR="$( dirname "$( realpath "${BASH_SOURCE[0]}" )" )"
source "$PROJECT_DIR/tools/bash/env_loader.sh"

# Cargar variables desde .env
LOG_DIR=$(load_env_var "LOG_DIR" "$PROJECT_DIR/.env")

# Borra archivos con más de 7 días
find "$LOG_DIR" -type f -name "*.log" -mtime +7 -exec rm {} \;
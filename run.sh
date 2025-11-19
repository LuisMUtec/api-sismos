#!/bin/bash
# Script de ejecución rápida del scraper

echo "🌎 Ejecutando Scraper de Sismos IGP..."
echo ""

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Entorno virtual activado"
else
    echo "⚠️  No se encontró entorno virtual"
    echo "   Ejecuta primero: ./install.sh"
    exit 1
fi

# Ejecutar el scraper
python scraper_sismos.py

echo ""
echo "✅ Scraping completado!"

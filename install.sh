#!/bin/bash
# Script de instalación rápida para el scraper de sismos IGP

echo "🌎 Instalación del Scraper de Sismos IGP"
echo "========================================"
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    exit 1
fi

echo "✅ Python 3 encontrado: $(python3 --version)"
echo ""

# Crear entorno virtual
echo "📦 Creando entorno virtual..."
python3 -m venv venv

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install -q --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Instalación completada!"
echo ""
echo "Para usar el scraper:"
echo "  1. Activar entorno: source venv/bin/activate"
echo "  2. Ejecutar scraper: python scraper_sismos.py"
echo ""

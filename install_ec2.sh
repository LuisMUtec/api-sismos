#!/bin/bash
# Script de instalación y ejecución para EC2 AWS Linux
# Scraper de Sismos IGP

echo "🌎 INSTALACIÓN EN AWS EC2 - SCRAPER SISMOS IGP"
echo "=============================================="
echo ""

# 1. Actualizar sistema
echo "📦 Actualizando sistema..."
sudo yum update -y

# 2. Instalar Python 3 y pip
echo "🐍 Instalando Python 3..."
sudo yum install -y python3 python3-pip

# 3. Instalar Google Chrome
echo "🌐 Instalando Google Chrome..."
sudo yum install -y wget
wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
sudo yum install -y ./google-chrome-stable_current_x86_64.rpm
rm google-chrome-stable_current_x86_64.rpm

# 4. Instalar ChromeDriver
echo "🚗 Instalando ChromeDriver..."
sudo yum install -y unzip
CHROME_DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget -N https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
rm chromedriver_linux64.zip

# 5. Crear directorio del proyecto
echo "📁 Creando directorio del proyecto..."
mkdir -p ~/api-sismos
cd ~/api-sismos

# 6. Crear entorno virtual
echo "🔧 Creando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

# 7. Instalar dependencias
echo "📥 Instalando dependencias Python..."
pip install --upgrade pip
pip install selenium webdriver-manager requests beautifulsoup4 boto3

echo ""
echo "✅ INSTALACIÓN COMPLETADA!"
echo ""
echo "Ahora sube tus archivos Python a ~/api-sismos/"
echo "Y ejecuta: source venv/bin/activate && python scraper_sismos.py"

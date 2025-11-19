# 🌎 API Web Scraping - Sismos IGP

Sistema de web scraping para extraer datos de sismos reportados del **Instituto Geofísico del Perú (IGP)**.

**URL:** https://ultimosismo.igp.gob.pe/ultimo-sismo/sismos-reportados

## 📁 Estructura del Proyecto

```
api-sismos/
├── test_scraping_sismos_selenium.py  # ⭐ Script principal (funcional)
├── scrap_sismos_igp.py               # Versión AWS Lambda
├── serverless-sismos-igp.yml         # Config Serverless Framework
├── requirements.txt                   # Dependencias Python
├── README.md                          # Este archivo
├── README_SISMOS_IGP.md              # Documentación detallada
└── RESUMEN_PROYECTO_SISMOS.md        # Resumen técnico
```

## 🚀 Instalación y Uso

### 1. Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate  # En Linux/Mac
# o
venv\Scripts\activate  # En Windows
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar el scraper

```bash
python test_scraping_sismos_selenium.py
```

## 📊 Resultado

El script genera un archivo JSON con los sismos extraídos:

```json
{
  "fecha_extraccion": "2025-11-18T23:43:54.222515",
  "total_sismos": 12,
  "url_origen": "https://ultimosismo.igp.gob.pe/ultimo-sismo/sismos-reportados",
  "metodo": "Selenium WebDriver",
  "sismos": [
    {
      "numero": 1,
      "tipo_reporte": "IGP/CENSIS/RS",
      "codigo_reporte": "2025-0763",
      "referencia": "19 km al SE de Zorritos...",
      "fecha_hora_local": "18/11/2025 11:02:13",
      "magnitud": "4.1",
      "enlace_reporte": "https://ultimosismo.igp.gob.pe/evento/2025-0763"
    }
  ]
}
```

## ⚙️ Tecnologías

- **Python 3.12+**
- **Selenium WebDriver** - Navegador headless para JavaScript
- **Chrome/Chromium** - Navegador automatizado
- **webdriver-manager** - Gestión automática del driver
- **AWS Lambda + DynamoDB** (opcional, para producción)

## 📚 Documentación

- **[README_SISMOS_IGP.md](README_SISMOS_IGP.md)** - Guía completa de uso
- **[RESUMEN_PROYECTO_SISMOS.md](RESUMEN_PROYECTO_SISMOS.md)** - Detalles técnicos

## 🔍 ¿Por qué Selenium?

La página del IGP es una aplicación **Angular** que carga datos dinámicamente con JavaScript. Selenium ejecuta un navegador real que puede procesar JavaScript y obtener los datos completos.

## ☁️ Despliegue en AWS

Ver instrucciones en [README_SISMOS_IGP.md](README_SISMOS_IGP.md)

## 📝 Licencia

Proyecto educativo - Uso libre

---

**Autor:** Luis M.  
**Fecha:** Noviembre 2025

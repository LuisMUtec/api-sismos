# 🌎 Web Scraping - Sismos IGP (Instituto Geofísico del Perú)

Script de web scraping para extraer datos de sismos reportados del Instituto Geofísico del Perú.

**URL objetivo:** https://ultimosismo.igp.gob.pe/ultimo-sismo/sismos-reportados

## 📋 Archivos del Proyecto

- **`scrap_sismos_igp.py`** - Función Lambda para AWS con DynamoDB
- **`test_scraping_sismos.py`** - Script de prueba local (sin AWS)
- **`serverless-sismos-igp.yml`** - Configuración de Serverless Framework
- **`requirements.txt`** - Dependencias de Python

## 🚀 Prueba Local (Sin AWS)

### 1. Instalar dependencias

```bash
pip install requests beautifulsoup4
```

### 2. Ejecutar el script de prueba

```bash
python test_scraping_sismos.py
```

Este script:
- ✅ Extrae los datos de sismos de la página del IGP
- ✅ Los guarda en un archivo JSON con timestamp
- ✅ Muestra un resumen en consola
- ❌ **NO requiere** AWS Lambda ni DynamoDB

### Ejemplo de salida:

```
🌎 SCRAPER DE SISMOS - INSTITUTO GEOFÍSICO DEL PERÚ
============================================================

🔄 Obteniendo datos de: https://ultimosismo.igp.gob.pe/ultimo-sismo/sismos-reportados
✅ Status Code: 200
✅ Tabla encontrada
📊 Filas encontradas: 12

🌍 Sismo #1:
   Código: 2025-0763
   Fecha: 18/11/2025 11:02:13
   Magnitud: 4.1
   Referencia: 19 km al SE de Zorritos, Contralmirante Villar...

✅ Total de sismos extraídos: 12
💾 Datos guardados en: sismos_igp_20251118_153045.json
```

## ☁️ Despliegue en AWS Lambda

### 1. Configurar Serverless Framework

```bash
npm install -g serverless
serverless config credentials --provider aws --key YOUR_KEY --secret YOUR_SECRET
```

### 2. Desplegar

```bash
serverless deploy --config serverless-sismos-igp.yml
```

### 3. Invocar la función

```bash
# Vía Serverless
serverless invoke --function scrape_sismos_igp --config serverless-sismos-igp.yml

# Vía HTTP
curl https://YOUR_API_GATEWAY_URL/scrape/sismos-igp
```

## 📊 Estructura de Datos Extraídos

Cada sismo contiene:

```json
{
  "tipo_reporte": "IGP/CENSIS/RS",
  "codigo_reporte": "2025-0763",
  "referencia": "19 km al SE de Zorritos, Contralmirante Villar - Tumbes",
  "fecha_hora_local": "18/11/2025 11:02:13",
  "magnitud": "4.1",
  "enlace_reporte": "https://ultimosismo.igp.gob.pe/evento/2025-0763"
}
```

## ⚠️ Consideraciones Importantes

### Problema: Carga Dinámica con JavaScript

La página web del IGP es una **aplicación Angular** que carga datos dinámicamente. Esto significa:

- ✅ El HTML descargado **SÍ contiene** la tabla (como viste en tu archivo)
- ⚠️ Un `curl` simple **NO verá** los datos porque no ejecuta JavaScript
- ✅ BeautifulSoup **PUEDE funcionar** si el HTML ya está renderizado en el servidor (SSR)
- ❌ Si los datos se cargan 100% en cliente, necesitarás **Selenium** o **Playwright**

### Si el script no funciona:

1. **Opción A: Usar Selenium (navegador real)**
   ```bash
   pip install selenium webdriver-manager
   ```

2. **Opción B: Buscar la API REST**
   - Abre las DevTools del navegador (F12)
   - Ve a la pestaña "Network"
   - Recarga la página
   - Busca llamadas XHR/Fetch que traigan datos JSON
   - Usa esa API directamente

3. **Opción C: Usar Playwright (más moderno que Selenium)**
   ```bash
   pip install playwright
   playwright install
   ```

## 🔍 Comparación con el Script Original

| Característica | Script Original (Bomberos) | Script Nuevo (IGP Sismos) |
|----------------|---------------------------|---------------------------|
| URL | sgonorte.bomberosperu.gob.pe | ultimosismo.igp.gob.pe |
| Tecnología | HTML estático | Angular (dinámico) |
| Tabla DynamoDB | `TablaWebScrapping` | `TablaSismosIGP` |
| Campos | Simple | Más detallado |
| Timeout | 20s | 30s |
| Headers | Básicos | Simula navegador |

## 📝 Próximos Pasos

Si el scraping con BeautifulSoup no funciona (por JavaScript), puedo crear:

1. ✅ Script con **Selenium** para navegador real
2. ✅ Script que busque la **API REST** del IGP
3. ✅ Script con **Playwright** (alternativa moderna)

¿Quieres que implemente alguna de estas opciones? 🚀

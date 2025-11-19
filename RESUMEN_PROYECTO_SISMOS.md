# 🎉 PROYECTO COMPLETADO - Web Scraping Sismos IGP

## ✅ Resumen del Proyecto

Se ha creado exitosamente un sistema de web scraping para extraer datos de sismos reportados del **Instituto Geofísico del Perú (IGP)**.

**URL:** https://ultimosismo.igp.gob.pe/ultimo-sismo/sismos-reportados

## 📁 Archivos Creados

### Scripts Python

1. **`test_scraping_sismos_selenium.py`** ✅ **FUNCIONA**
   - Script con Selenium WebDriver
   - Usa navegador Chrome real para ejecutar JavaScript
   - Guarda resultados en JSON
   - **ESTE ES EL QUE FUNCIONA**

2. **`test_scraping_sismos.py`** ❌ No funciona
   - Script con BeautifulSoup (sin JavaScript)
   - No funciona porque la página carga datos dinámicamente
   - Dejado como referencia

3. **`scrap_sismos_igp.py`**
   - Versión para AWS Lambda con DynamoDB
   - Basada en el script de prueba
   - Lista para desplegar en AWS

### Configuración

4. **`serverless-sismos-igp.yml`**
   - Configuración de Serverless Framework
   - Define función Lambda y tabla DynamoDB
   - Listo para desplegar

5. **`requirements.txt`** (existente)
   - Dependencias: `requests` y `beautifulsoup4`
   - **Agregar:** `selenium` y `webdriver-manager`

6. **`README_SISMOS_IGP.md`**
   - Documentación completa del proyecto
   - Instrucciones de uso

## 🚀 Cómo Usar

### Prueba Local (Recomendado)

```bash
# 1. Activar entorno virtual
cd "api-web-scraping"
source venv/bin/activate

# 2. Ejecutar el script
python test_scraping_sismos_selenium.py
```

### Resultado Esperado:

```
============================================================
🌎 SCRAPER DE SISMOS - INSTITUTO GEOFÍSICO DEL PERÚ
📱 Usando Selenium WebDriver (navegador real)
============================================================

🔄 Obteniendo datos de: https://ultimosismo.igp.gob.pe/ultimo-sismo/sismos-reportados
⏳ Iniciando navegador Chrome...
✅ Navegador iniciado
⏳ Esperando que la tabla se cargue...
✅ Tabla cargada
📊 Filas encontradas: 12

🌍 Sismo #1:
   Código: 2025-0763
   Fecha: 18/11/2025 11:02:13
   Magnitud: 4.1
   Referencia: 19 km al SE de Zorritos...

✅ Total de sismos extraídos: 12
💾 Datos guardados en: sismos_igp_20251118_234354.json
🔒 Navegador cerrado

============================================================
✅ SCRAPING COMPLETADO EXITOSAMENTE
============================================================
```

## 📊 Datos Extraídos

Cada sismo contiene:

```json
{
  "numero": 1,
  "tipo_reporte": "IGP/CENSIS/RS",
  "codigo_reporte": "2025-0763",
  "referencia": "19 km al SE de Zorritos, Contralmirante Villar - Tumbes",
  "fecha_hora_local": "18/11/2025 11:02:13",
  "magnitud": "4.1",
  "enlace_reporte": "https://ultimosismo.igp.gob.pe/evento/2025-0763"
}
```

## ⚙️ Tecnologías Utilizadas

- **Python 3.12**
- **Selenium WebDriver** - Para ejecutar JavaScript en navegador real
- **Chrome/Chromium** - Navegador headless
- **webdriver-manager** - Gestión automática del ChromeDriver
- **BeautifulSoup4** (alternativa, no funciona para esta página)
- **AWS Lambda + DynamoDB** (para producción)

## 🔍 Problema Técnico Identificado

**¿Por qué BeautifulSoup no funciona?**

La página web del IGP es una **aplicación Angular** que:
1. Carga HTML inicial vacío
2. Ejecuta JavaScript para cargar datos
3. Renderiza la tabla dinámicamente

**Solución:** Usar Selenium con navegador real que ejecuta JavaScript.

## 📈 Comparación con Script Original

| Característica | Script Original (Bomberos) | Script Nuevo (IGP Sismos) |
|----------------|---------------------------|---------------------------|
| URL | sgonorte.bomberosperu.gob.pe | ultimosismo.igp.gob.pe |
| Tecnología | HTML estático | Angular (JavaScript) |
| Método Scraping | BeautifulSoup ✅ | Selenium WebDriver ✅ |
| Tabla DynamoDB | `TablaWebScrapping` | `TablaSismosIGP` |
| Timeout | 20s | 30s |
| Campos | 6 campos | 7 campos |
| Navegador | No necesario | Chrome headless |

## 🎯 Próximos Pasos

### Para AWS Lambda

1. **Actualizar dependencias** en `requirements.txt`:
   ```
   beautifulsoup4==4.9.3
   requests==2.25.1
   selenium==4.38.0
   webdriver-manager==4.0.2
   ```

2. **Instalar Chrome/Chromium en Lambda:**
   ```yaml
   # En serverless-sismos-igp.yml
   custom:
     pythonRequirements:
       dockerizePip: true
       layer: true
   ```

3. **Usar Chrome Layer:**
   - https://github.com/shelfio/chrome-aws-lambda-layer
   - O usar `selenium-lambda-layer`

4. **Desplegar:**
   ```bash
   serverless deploy --config serverless-sismos-igp.yml
   ```

### Alternativa: API REST

Si quieres evitar Selenium en producción:
1. Buscar la API REST del IGP en DevTools
2. Extraer datos directamente de la API
3. Más rápido y eficiente

## 📝 Notas Importantes

- ✅ El script **funciona perfectamente** en local
- ⚠️ Para Lambda, necesitas configurar Chrome headless
- 💡 Considera buscar la API REST del IGP como alternativa
- 🔒 La página puede cambiar su estructura HTML

## 🆚 Diferencias Clave

### Script Original (Bomberos):
```python
# Simple, directo
soup = BeautifulSoup(response.content, 'html.parser')
table = soup.find('table')
```

### Script Nuevo (IGP):
```python
# Requiere navegador real
driver = webdriver.Chrome()
driver.get(url)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table")))
```

## ✅ Estado del Proyecto

- [x] Script de prueba local funcional
- [x] Extracción de datos correcta
- [x] Guardado en JSON
- [x] Documentación completa
- [ ] Despliegue en AWS Lambda (pendiente)
- [ ] Configuración de Chrome en Lambda (pendiente)

## 🎓 Aprendizajes

1. **No todas las páginas web son iguales:**
   - HTML estático → BeautifulSoup ✅
   - JavaScript dinámico → Selenium ✅

2. **Selenium es más lento pero más potente:**
   - Ejecuta JavaScript
   - Ve la página como un usuario real
   - Necesita más recursos

3. **Para producción:**
   - Buscar APIs REST cuando sea posible
   - Selenium en Lambda requiere configuración extra
   - Considerar alternativas como Playwright

---

**¿Necesitas ayuda con el despliegue en AWS Lambda?** ¡Avísame! 🚀

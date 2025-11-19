"""
Script de scraping de sismos del IGP usando Selenium
Usa un navegador real para ejecutar JavaScript

Instalación:
    pip install selenium webdriver-manager

Uso:
    python test_scraping_sismos_selenium.py
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
from datetime import datetime
import time

def scrape_sismos_igp_selenium():
    """
    Extrae datos de sismos reportados del IGP usando Selenium.
    URL: https://ultimosismo.igp.gob.pe/ultimo-sismo/sismos-reportados
    """
    
    url = "https://ultimosismo.igp.gob.pe/ultimo-sismo/sismos-reportados"
    
    print(f"🔄 Obteniendo datos de: {url}")
    print("⏳ Iniciando navegador Chrome...")
    
    # Configurar opciones de Chrome
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Ejecutar sin ventana visible
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    
    driver = None
    
    try:
        # Inicializar el driver de Chrome
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("✅ Navegador iniciado")
        
        # Cargar la página
        driver.get(url)
        
        # Esperar a que la tabla se cargue (hasta 30 segundos)
        print("⏳ Esperando que la tabla se cargue...")
        wait = WebDriverWait(driver, 30)
        
        # Esperar a que aparezca la tabla con datos
        table = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr"))
        )
        
        print("✅ Tabla cargada")
        
        # Pequeña pausa adicional para asegurar que todos los datos estén cargados
        time.sleep(2)
        
        # Extraer los datos de la tabla
        sismos = []
        
        # Encontrar todas las filas del tbody
        rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        print(f"📊 Filas encontradas: {len(rows)}")
        
        for idx, row in enumerate(rows, 1):
            try:
                cells = row.find_elements(By.TAG_NAME, "td")
                
                if len(cells) >= 4:
                    # Extraer el código del reporte
                    reporte_text = cells[0].text.strip()
                    reporte_lines = reporte_text.split('\n')
                    codigo_reporte = reporte_lines[-1] if reporte_lines else 'N/A'
                    tipo_reporte = '\n'.join(reporte_lines[:-1]) if len(reporte_lines) > 1 else 'N/A'
                    
                    # Extraer otros datos
                    referencia = cells[1].text.strip()
                    fecha_hora = cells[2].text.strip()
                    magnitud = cells[3].text.strip()
                    
                    # Extraer enlace del reporte sísmico si existe
                    enlace_reporte = ''
                    if len(cells) >= 5:
                        try:
                            link = cells[4].find_element(By.TAG_NAME, "a")
                            enlace_reporte = link.get_attribute('href')
                        except:
                            pass
                    
                    sismo = {
                        'numero': idx,
                        'tipo_reporte': tipo_reporte,
                        'codigo_reporte': codigo_reporte,
                        'referencia': referencia,
                        'fecha_hora_local': fecha_hora,
                        'magnitud': magnitud,
                        'enlace_reporte': enlace_reporte
                    }
                    
                    sismos.append(sismo)
                    
                    # Mostrar primeros 3 sismos como ejemplo
                    if idx <= 3:
                        print(f"\n🌍 Sismo #{idx}:")
                        print(f"   Código: {codigo_reporte}")
                        print(f"   Fecha: {fecha_hora}")
                        print(f"   Magnitud: {magnitud}")
                        print(f"   Referencia: {referencia[:50]}...")
            
            except Exception as e:
                print(f"⚠️  Error procesando fila {idx}: {e}")
                continue
        
        if not sismos:
            print("❌ No se encontraron datos de sismos en la tabla")
            return None
        
        print(f"\n✅ Total de sismos extraídos: {len(sismos)}")
        
        # Guardar en archivo JSON
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'sismos_igp_{timestamp}.json'
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'fecha_extraccion': datetime.now().isoformat(),
                'total_sismos': len(sismos),
                'url_origen': url,
                'metodo': 'Selenium WebDriver',
                'sismos': sismos
            }, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Datos guardados en: {filename}")
        
        return sismos
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None
        
    finally:
        # Cerrar el navegador
        if driver:
            driver.quit()
            print("🔒 Navegador cerrado")


if __name__ == "__main__":
    print("=" * 60)
    print("🌎 SCRAPER DE SISMOS - INSTITUTO GEOFÍSICO DEL PERÚ")
    print("📱 Usando Selenium WebDriver (navegador real)")
    print("=" * 60)
    print()
    
    sismos = scrape_sismos_igp_selenium()
    
    if sismos:
        print("\n" + "=" * 60)
        print("✅ SCRAPING COMPLETADO EXITOSAMENTE")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ SCRAPING FALLÓ")
        print("=" * 60)

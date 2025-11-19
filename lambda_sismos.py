import requests
from bs4 import BeautifulSoup
import boto3
import uuid
import json

def lambda_handler(event, context):
    """
    Función Lambda para extraer datos de sismos reportados del IGP.
    URL: https://ultimosismo.igp.gob.pe/ultimo-sismo/sismos-reportados
    
    Esta página web es una aplicación Angular que carga datos dinámicamente,
    por lo que necesitamos extraer los datos del HTML renderizado.
    """
    
    url = "https://ultimosismo.igp.gob.pe/ultimo-sismo/sismos-reportados"
    
    # Headers para simular un navegador real
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
    }
    
    try:
        # Realizar la solicitud HTTP a la página web
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code != 200:
            return {
                'statusCode': response.status_code,
                'body': json.dumps({
                    'error': f'Error al acceder a la página web. Status: {response.status_code}'
                })
            }
        
        # Parsear el contenido HTML de la página web
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Buscar la tabla en el HTML
        table = soup.find('table')
        
        if not table:
            return {
                'statusCode': 404,
                'body': json.dumps({
                    'error': 'No se encontró la tabla en la página web',
                    'message': 'La página podría estar cargando datos dinámicamente'
                })
            }
        
        # Extraer los datos de la tabla
        sismos = []
        
        # Encontrar todas las filas del tbody
        tbody = table.find('tbody')
        if tbody:
            rows = tbody.find_all('tr')
            
            for row in rows:
                cells = row.find_all('td')
                
                if len(cells) >= 4:
                    # Extraer el código del reporte
                    reporte_cell = cells[0]
                    reporte_lines = reporte_cell.get_text(strip=True).split()
                    codigo_reporte = ' '.join(reporte_lines[-1:]) if reporte_lines else 'N/A'
                    tipo_reporte = ' '.join(reporte_lines[:-1]) if len(reporte_lines) > 1 else 'N/A'
                    
                    # Extraer otros datos
                    referencia = cells[1].get_text(strip=True)
                    fecha_hora = cells[2].get_text(strip=True)
                    magnitud = cells[3].get_text(strip=True)
                    
                    # Extraer enlace del reporte sísmico si existe
                    enlace_reporte = ''
                    if len(cells) >= 5:
                        link = cells[4].find('a')
                        if link and link.get('href'):
                            enlace_reporte = link.get('href')
                            # Si es relativo, convertirlo a absoluto
                            if enlace_reporte.startswith('/'):
                                enlace_reporte = f"https://ultimosismo.igp.gob.pe{enlace_reporte}"
                    
                    sismo = {
                        'id': str(uuid.uuid4()),
                        'tipo_reporte': tipo_reporte,
                        'codigo_reporte': codigo_reporte,
                        'referencia': referencia,
                        'fecha_hora_local': fecha_hora,
                        'magnitud': magnitud,
                        'enlace_reporte': enlace_reporte
                    }
                    
                    sismos.append(sismo)
        
        if not sismos:
            return {
                'statusCode': 404,
                'body': json.dumps({
                    'error': 'No se encontraron datos de sismos en la tabla',
                    'message': 'La tabla existe pero no contiene filas con datos'
                })
            }
        
        # Guardar los datos en DynamoDB
        dynamodb = boto3.resource('dynamodb')
        table_db = dynamodb.Table('TablaSismosIGP')
        
        # Eliminar todos los elementos de la tabla antes de agregar los nuevos
        scan = table_db.scan()
        with table_db.batch_writer() as batch:
            for each in scan['Items']:
                batch.delete_item(
                    Key={
                        'id': each['id']
                    }
                )
        
        # Insertar los nuevos datos
        with table_db.batch_writer() as batch:
            for sismo in sismos:
                batch.put_item(Item=sismo)
        
        # Retornar el resultado como JSON
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Se extrajeron {len(sismos)} sismos correctamente',
                'total_sismos': len(sismos),
                'sismos': sismos
            }, ensure_ascii=False)
        }
        
    except requests.exceptions.Timeout:
        return {
            'statusCode': 408,
            'body': json.dumps({
                'error': 'Timeout al intentar acceder a la página',
                'message': 'La solicitud tardó demasiado tiempo'
            })
        }
    except requests.exceptions.RequestException as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Error en la solicitud HTTP',
                'message': str(e)
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Error interno del servidor',
                'message': str(e)
            })
        }

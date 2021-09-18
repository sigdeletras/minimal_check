import urllib.request
import psycopg2

from PyQt5.QtWidgets import QMessageBox
from qgis.core import Qgis, QgsProject


def check():
    """Función que realiza una serie de comprobaciones y muestra el resultado en un mensaje
    """

    check_message = 'RESULTADO:\n\n'

    # P01 Busca una capa y devuelve su nombre
    LAYER = 'points'

    try:
        print('Check 01 Start')
        points_layer = QgsProject.instance().mapLayersByName(LAYER)[0]
        check_message += f'01 - La capa \'{points_layer.name()}\' se encuentra cargada.\n'
        print('Check 01 - OK')

    except Exception as error:
        # 1 - Usamos print
        print(
            f'Check 01 - FAIL - La capa {LAYER} no se encuentra en el proyecto')
        print(f'Error: {error}')
        return

    # P02 Realiza una conexión a una DB
    conn = None

    try:
        print('Check 02 Start')
        conn = psycopg2.connect(host='localhost', port=5432, database='vse',
                                user='postgres', password='postgres')
        cur = conn.cursor()
        cur.close()

        check_message += f'02 - Conexión correcta a la db\n'
        print('Check 02 - OK')

    except Exception as error:
        error_message = 'Check 02 - FAIL No se ha podido establecer la conexión a la DB'
        print(error_message)

        return

    finally:
        if conn is not None:
            conn.close()

    # P03 Consulta una API
    URL_NOMINATIM = 'https://nominatim.openstreetmap.org/reverse?'
    COORDINATES = [37.87893, -4.772846]

    try:
        print('Check 03 Start')
        url = f'{URL_NOMINATIM}format=jsonv2&lat={COORDINATES[0]}&lon={COORDINATES[1]}'

        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')
            print(data)

        check_message += f'03 - Consulta a la API relizada\n'
        print('Check 03 - OK')

    except urllib.error.URLError as e:
        error_message = 'Check 03 - FAIL Consulta a la API no relizada'
        print(error_message)
        print(e.reason)
        return

    QMessageBox.information(None, 'Chek plugin', check_message)
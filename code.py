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
        points_layer = QgsProject.instance().mapLayersByName(LAYER)[0]
        check_message += f'01 - La capa \'{points_layer.name()}\' se encuentra cargada.\n'

    except Exception as error:
        return

    # P02 Realiza una conexión a una DB
    conn = None

    try:
        conn = psycopg2.connect(host='localhost', port=5432, database='vse',
                                user='postgres', password='postgres')
        cur = conn.cursor()
        cur.close()

        check_message += f'02 - Conexión correcta a la db\n'

    except Exception as error:
        return

    finally:
        if conn is not None:
            conn.close()

    # P03 Consulta una API
    URL_NOMINATIM = 'https://nominatim.openstreetmap.org/reverse?'
    COORDINATES = [37.87893, -4.772846]

    try:
        url = f'{URL_NOMINATIM}format=jsonv2&lat={COORDINATES[0]}&lon={COORDINATES[1]}'

        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')
            print(data)

        check_message += f'03 - Consulta a la API relizada\n'

    except urllib.error.URLError as e:
        return

    QMessageBox.information(None, 'Chek plugin', check_message)
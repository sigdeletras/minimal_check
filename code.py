import logging
import os
import urllib.request
from pathlib import Path

import psycopg2
from PyQt5.QtWidgets import QMessageBox
from qgis.core import Qgis, QgsMessageLog, QgsProject
from qgis.utils import iface


def create_loging_file():
    """Crear y configura un fichero logger de registro
    """

    log_path_save = Path(__file__).parent.absolute()
    log_filename = str(log_path_save)+"/log/logfile.log"
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    logging.basicConfig(
        level=logging.DEBUG,   # Nivel de los eventos que se registran en el logger
        filename=log_filename,  # Fichero de  logs
        format=log_format      # Formato de registro
    )

    if os.path.isfile(log_filename):
        with open(log_filename, 'a') as file:
            pass

    logging.info("############### START LOGGING ###############")


def check():
    """Función que realiza una serie de comprobaciones y muestra el resultado en un mensaje
    """

    create_loging_file()

    check_message = 'RESULTADO:\n\n'

    # P01 Busca una capa y devuelve su nombre
    LAYER = 'points'

    try:
        print('Check 01 Start')
        points_layer = QgsProject.instance().mapLayersByName(LAYER)[0]
        check_message += f'01 - La capa \'{points_layer.name()}\' se encuentra cargada.\n'
        print('Check 01 - OK')

    except Exception as error:
        error_message = f'Check 01 - FAIL - La capa {LAYER} no se encuentra en el proyecto'

        # 1 - Usamos print
        print(error_message)
        print(f'Error: {error}')

        # 2 - QgsMessageLog
        QgsMessageLog.logMessage(error_message, level=Qgis.Critical)
        QgsMessageLog.logMessage(
            f'Error: {error}', level=Qgis.Critical)

        # 3 - messageBar()
        iface.messageBar().pushMessage("ERROR", error_message, level=Qgis.Critical)

        # 4 - logging
        logging.error(error_message)

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

        # 1 - Usamos print
        print(error_message)

        # 2 - QgsMessageLog
        QgsMessageLog.logMessage(error_message, level=Qgis.Critical)

        # 3 - messageBar()
        iface.messageBar().pushMessage("ERROR", error_message, level=Qgis.Critical)

        # 4 - logging
        logging.error('Check 02 - FAIL')

        return

    finally:
        if conn is not None:
            conn.close()

    # P03 Consulta una API
    URL_NOMINATIM = 'https://nominatim.openstreetmap.org/reverse?'
    COORDINATES = [37.87893, -4.772846]

    try:
        print('Check 03 Start')
        logging.info('Check 03 Start')
        url = f'{URL_NOMINATIM}format=jsonv2&lat={COORDINATES[0]}&lon={COORDINATES[1]}'

        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')
            print(data)

        check_message += f'03 - Consulta a la API relizada\n'
        print('Check 03 - OK')
        logging.info('Check 03 - OK')

    except urllib.error.URLError as error:
        error_message = 'Check 03 - FAIL Consulta a la API no relizada'

        # 1 - Usamos print
        print(error_message)
        print(error.reason)

        # 2 - QgsMessageLog
        QgsMessageLog.logMessage(error_message, level=Qgis.Critical)
        QgsMessageLog.logMessage(
            f'Error: {error.reason}', level=Qgis.Critical)

        # 3 - messageBar()
        iface.messageBar().pushMessage("ERROR", error_message, level=Qgis.Critical)

        # 4 - logging
        logging.error('Check 03 - FAIL')
        logging.error(error.reason)

        return

    QMessageBox.information(None, 'Chek plugin', check_message)
    logging.info('############### END LOGGING ###############')

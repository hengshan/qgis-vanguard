from qgis.gui import QgisInterface
from qgis.core import (
    QgsTask,
    QgsMessageLog,
    Qgis,
    QgsRasterLayer,
    QgsProject,
    QgsNetworkAccessManager,
    QgsNetworkReplyContent,
    QgsGeometry,
)
from qgis.utils import iface
from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtWidgets import QMessageBox

import pandas as pd
from datetime import datetime
import json
from pandas import json_normalize
import requests

MESSAGE_CATEGORY = 'Download Rainfall Data'

class DownloadRainfallTask(QgsTask):
    """This shows how to subclass QgsTask"""

    def __init__(self, description, datelist):
        super().__init__(description, QgsTask.CanCancel)
        self.datelist = datelist
        self.exception = None

    def run(self):
        """Here you implement your heavy lifting.
        Should periodically test for isCanceled() to gracefully
        abort.
        This method MUST return True or False.
        Raising exceptions will crash QGIS, so we handle them
        internally and raise them in self.finished
        """
        QgsMessageLog.logMessage('Started task "{}"'.format(
                                     self.description()),
                                 MESSAGE_CATEGORY, Qgis.Info)
        
        for i,dt in enumerate(self.datelist):
            self.setProgress((i+1)*100/len(self.datelist))

            response = requests.get('https://api.data.gov.sg/v1/environment/rainfall?date='+dt.strftime("%Y-%m-%d"))
            
            if str(response.status_code) != '200':
                # DO NOT raise Exception('bad value!')
                # this would crash QGIS
                print(str(response.status_code))
                self.exception = Exception('The request was failed.')
                return False
            
            if self.isCanceled():
                return False

            with open(f'Data/Rainfall_Download/test{i}.json', 'w') as f:
                json.dump(response.json(), f)

            print(f'Data/Rainfall_Download/test{i}.json',' downloaded')

        return True


    def finished(self, result):
        """
        This function is automatically called when the task has
        completed (successfully or not).
        You implement finished() to do whatever follow-up stuff
        should happen after the task is complete.
        finished is always called from the main thread, so it's safe
        to do GUI operations and raise Python exceptions here.
        result is the return value from self.run.
        """
        if result:
            QgsMessageLog.logMessage(
                f'Task "{self.description()}" completed',
              MESSAGE_CATEGORY, Qgis.Success)
        else:
            if self.exception is None:
                QgsMessageLog.logMessage(
                    'Task "{name}" not successful but without '\
                    'exception (probably the task was manually '\
                    'canceled by the user)'.format(
                        name=self.description()),
                    MESSAGE_CATEGORY, Qgis.Warning)
            else:
                QgsMessageLog.logMessage(
                    'Task "{name}" Exception: {exception}'.format(
                        name=self.description(),
                        exception=self.exception),
                    MESSAGE_CATEGORY, Qgis.Critical)
                raise self.exception

    def cancel(self):
        QgsMessageLog.logMessage(
            'Download Rainfall Task "{name}" was canceled'.format(
                name=self.description()),
            MESSAGE_CATEGORY, Qgis.Info)
        super().cancel()
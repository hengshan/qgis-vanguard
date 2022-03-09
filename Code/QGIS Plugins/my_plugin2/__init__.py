# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MyPlugin2
                                 A QGIS plugin
 Facility Site Selection
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2022-03-07
        copyright            : (C) 2022 by WOG
        email                : wog@wog.gov.sg
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load MyPlugin2 class from file MyPlugin2.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .my_plugin2 import MyPlugin2
    return MyPlugin2(iface)
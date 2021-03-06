# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MyPlugin2DockWidget
                                 A QGIS plugin
 Facility Site Selection
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2022-03-07
        git sha              : $Format:%H$
        copyright            : (C) 2022 by WOG
        email                : wog@wog.gov.sg
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from qgis.PyQt import QtGui, QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal,QThread,Qt
from qgis.core import *
from qgis.utils import iface

import geopandas as gpd
import seaborn as sb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

# Facility Site selection
from pulp import *
from shapely import wkt
from shapely.geometry import Polygon,LineString
import re

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'my_plugin2_dockwidget_base.ui'))


class MyPlugin2DockWidget(QtWidgets.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(MyPlugin2DockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://doc.qt.io/qt-5/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        
        # change curent work directory to the qgis-vanguard folder
        os.chdir(r'C:\Users\user\Desktop\Projects\qgis-vanguard')

        #facility location
        self.mMapLayerComboBox_Customer.setFilters(QgsMapLayerProxyModel.VectorLayer)
        self.mMapLayerComboBox_Customer.layerChanged['QgsMapLayer*'].connect(self.mFieldComboBox_Customer_ID.setLayer)
        self.mMapLayerComboBox_Customer.layerChanged['QgsMapLayer*'].connect(self.mFieldComboBox_Customer_Demand.setLayer)

        self.mMapLayerComboBox_Facility.setFilters(QgsMapLayerProxyModel.VectorLayer)
        self.mMapLayerComboBox_Facility.layerChanged['QgsMapLayer*'].connect(self.mFieldComboBox_Facility_ID.setLayer)
        self.mMapLayerComboBox_Facility.layerChanged['QgsMapLayer*'].connect(self.mFieldComboBox_Facility_Cost.setLayer)
        self.mMapLayerComboBox_Facility.layerChanged['QgsMapLayer*'].connect(self.mFieldComboBox_Facility_Capacity.setLayer)
        self.btn_Site.clicked.connect(self.site_selection)

    @staticmethod
    def compute_distance(loc1, loc2):
        import math
        dx = loc1[0] - loc2[0]
        dy = loc1[1] - loc2[1]
        return math.sqrt(dx*dx + dy*dy)

    def site_selection(self):
        if self.mFieldComboBox_Customer_ID.currentField() =="":
            return
        if self.mFieldComboBox_Customer_Demand.currentField() =="":
            return
        if self.mFieldComboBox_Facility_ID.currentField() =="":
            return
        if self.mFieldComboBox_Facility_Cost.currentField() =="":
            return
        if self.mFieldComboBox_Facility_Capacity.currentField() =="":
            return
        
        Supermarkets_shp = self.convertToGeoPandas(self.mMapLayerComboBox_Customer.currentLayer())
        Warehouses_shp = self.convertToGeoPandas(self.mMapLayerComboBox_Facility.currentLayer())

        # SETS
        SUPERMARKETS = list(Supermarkets_shp[self.mFieldComboBox_Customer_ID.currentField()])
        WAREHOUSES =  list(Warehouses_shp[self.mFieldComboBox_Facility_ID.currentField()])
        demand = dict(zip(SUPERMARKETS,Supermarkets_shp[self.mFieldComboBox_Customer_Demand.currentField()]))
        actcost = dict(zip(WAREHOUSES,Warehouses_shp[self.mFieldComboBox_Facility_Cost.currentField()]))
        maxam = dict(zip(WAREHOUSES,Warehouses_shp[self.mFieldComboBox_Facility_Capacity.currentField()]))
        SUPERMARKETS_XY = list(zip(Supermarkets_shp.geometry.x,Supermarkets_shp.geometry.y))
        WAREHOUSES_XY = list(zip(Warehouses_shp.geometry.x,Warehouses_shp.geometry.y))
        cost_per_km = 0.02

        transp={}
        for i, wh in enumerate(WAREHOUSES):
            dist=[]
            for j, _ in enumerate(SUPERMARKETS):
                dist.append(cost_per_km * self.compute_distance(WAREHOUSES_XY[i],SUPERMARKETS_XY[j])) # warning: distance is weighted by cost
            transp[wh] = dict(zip(SUPERMARKETS,dist))
        
        prob = LpProblem("FacilityLocation",LpMinimize)
        serv_vars = LpVariable.dicts("Service", [(i,j) for i in SUPERMARKETS for j in WAREHOUSES],0)
        use_vars = LpVariable.dicts("UseLocation",WAREHOUSES,lowBound=0, upBound=1, cat=LpBinary)
        prob += lpSum(actcost[j] * use_vars[j] for j in WAREHOUSES) +\
            lpSum(transp[j][i] * serv_vars[(i,j)] for j in WAREHOUSES for i in SUPERMARKETS)

        for i in SUPERMARKETS:
            prob += lpSum(serv_vars[(i,j)] for j in WAREHOUSES) == demand[i]

        for j in WAREHOUSES:
            prob += lpSum(serv_vars[(i,j)] for i in SUPERMARKETS) <=maxam[j] * use_vars[j]

        for i in SUPERMARKETS:
            for j in WAREHOUSES:
                prob += serv_vars[(i,j)] <= demand[i] * use_vars[j]

        # The problem is solved using PuLP's choice of Solver
        prob.solve()
        print("Status:", LpStatus[prob.status])

        TOL = 0.0001
        results=[]
        for i in WAREHOUSES:
            if use_vars[i].varValue > TOL:
                print(f"Establish warehouse at: {i}.")
                results.append(i)

        for v in prob.variables():
            if v.varValue>0:
                print(v.name, "=", v.varValue)

        # select all optimal sites
        layer = self.mMapLayerComboBox_Facility.currentLayer()
        values = ','.join(str(x) for x in results)
        layer.selectByExpression('\"'+ self.mFieldComboBox_Facility_ID.currentField() +'\" IN (' + values + ')', QgsVectorLayer.SetSelection)

        # create a new line layer
        customer_id = []
        facility_id = []
        values = []
        for v in prob.variables():
            if v.varValue>0 and v.name.startswith("Service"):
                print(v.name, "=", v.varValue)
                customer_id.append(int(re.findall('\d+', v.name)[0]))
                facility_id.append(int(re.findall('\d+', v.name)[1]))
                values.append(v.varValue)



        lines = [LineString([Supermarkets_shp.query(f"{self.mFieldComboBox_Customer_ID.currentField()} == {i}").geometry.values[0], 
            Warehouses_shp.query(f"{self.mFieldComboBox_Facility_ID.currentField()} == {j}").geometry.values[0]]) for i,j in zip(customer_id,facility_id)]

        facility_id_unique = set(facility_id)

        Warehouses_shp[self.mFieldComboBox_Facility_ID.currentField()] = Warehouses_shp[self.mFieldComboBox_Facility_ID.currentField()].astype(int)

        # result_wh = Warehouses_shp.query(f"{self.mFieldComboBox_Facility_ID.currentField()} == @facility_id_unique")
        result_wh = Warehouses_shp[Warehouses_shp[self.mFieldComboBox_Facility_ID.currentField()].isin(facility_id_unique)]

        vl_result_wh = QgsVectorLayer(result_wh.to_json(),"Facility_Site_results","ogr")
        projectCrs = QgsCoordinateReferenceSystem.fromEpsgId(3414)
        vl_result_wh.setCrs(projectCrs)
        QgsProject.instance().addMapLayer(vl_result_wh)
        vl_result_wh.loadNamedStyle("Resources/result_wh_style.qml")
        vl_result_wh.triggerRepaint()


        result_value = pd.DataFrame({"customer_id":customer_id,"facility_id":facility_id,"value":values})
        result_lines = gpd.GeoDataFrame(result_value,geometry=lines)

        vl_result_lines = QgsVectorLayer(result_lines.to_json(),"Result_Line","ogr")
        projectCrs = QgsCoordinateReferenceSystem.fromEpsgId(3414)
        vl_result_lines.setCrs(projectCrs)
        QgsProject.instance().addMapLayer(vl_result_lines)
        vl_result_lines.loadNamedStyle("Resources/result_line_style.qml")
        vl_result_lines.triggerRepaint()   

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

    def convertToPandas(self, layer):
        columns = [f.name() for f in layer.fields()] + ['geometry']
        columns_types = [f.typeName() for f in layer.fields()] # We exclude the geometry. Human readable
        # or
        # columns_types = [f.type() for f in layer.fields()] # QVariant type
        row_list = []
        for f in layer.getFeatures():
            row_list.append(dict(zip(columns, f.attributes() + [f.geometry().asWkt()])))

        df = pd.DataFrame(row_list, columns=columns)
        df['geometry'] = gpd.GeoSeries.from_wkt(df['geometry'])
        return df

    def convertToGeoPandas(self, layer):
        if layer is not None:
            gdf = gpd.GeoDataFrame(self.convertToPandas(layer), geometry='geometry')
            gdf = gdf.set_crs(crs=layer.crs().toWkt())
            return gdf
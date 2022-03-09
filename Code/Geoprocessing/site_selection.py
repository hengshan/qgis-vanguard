# -*- coding: utf-8 -*-

"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingFeedback,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterField,
                       QgsProcessingParameterFeatureSink,
                       QgsCoordinateReferenceSystem,
                       QgsFields,QgsField,QgsWkbTypes,QgsFeature,QgsGeometry,QgsPointXY)
from qgis import processing
from PyQt5.QtCore import QVariant
import geopandas as gpd
import pandas as pd
from pulp import *
from shapely import wkt
from shapely.geometry import LineString
import re
import math

class SiteSelectionProcessingAlgorithm(QgsProcessingAlgorithm):
    """
    This is an example algorithm that takes a vector layer and
    creates a new identical one.

    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.

    All Processing algorithms should extend the QgsProcessingAlgorithm
    class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    INPUT_C = 'INPUT_C'
    INPUT_F ='INPUT_F'
    C_ID = 'C_ID'
    C_DEMAND = 'C_DEMAND'

    F_ID = 'F_ID'
    F_COST ='F_COST'
    F_CAP = 'F_CAP'
    OUTPUT = 'OUTPUT'
    OUTPUT_LINES ='OUTPUT_LINES'

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return SiteSelectionProcessingAlgorithm()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'siteselection'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Facility Site Selection')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('scripts')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'scripts'

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return self.tr("Example algorithm short description")

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_C,
                self.tr('Input customer layer'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                    self.C_ID,
                    'Choose customer ID Field',
                    'Shop_ID',
                    self.INPUT_C))

        self.addParameter(
            QgsProcessingParameterField(
                self.C_DEMAND,
                'Choose customer Demand Field',
                'Demand',
                self.INPUT_C
            )
        )
        
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_F,
                self.tr('Input facility layer'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                    self.F_ID,
                    'Choose facility ID Field',
                    'WH_ID',
                    self.INPUT_F))

        self.addParameter(
            QgsProcessingParameterField(
                self.F_COST,
                'Choose facility cost Field',
                'Fixed_Cost',
                self.INPUT_F
            )
        )
        
        self.addParameter(
            QgsProcessingParameterField(
                self.F_CAP,
                'Choose facility capacity Field',
                'Capacity',
                self.INPUT_F
            )
        )

        # We add a feature sink in which to store our processed features (this
        # usually takes the form of a newly created vector layer when the
        # algorithm is run in QGIS).
        
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Output Facility layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_LINES,
                self.tr('Output Connectivity layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        c_layer = self.parameterAsVectorLayer(
            parameters,
            self.INPUT_C,
            context
        )

        f_layer = self.parameterAsVectorLayer(
            parameters,
            self.INPUT_F,
            context
        )
        
        C_ID = self.parameterAsString(
            parameters,
            self.C_ID,
            context
        )
        
        C_Demand = self.parameterAsString(
            parameters,
            self.C_DEMAND,
            context
        )
        
        F_ID = self.parameterAsString(
            parameters,
            self.F_ID,
            context
        )
        
        F_Cost = self.parameterAsString(
            parameters,
            self.F_COST,
            context
        )
        
        F_Cap = self.parameterAsString(
            parameters,
            self.F_CAP,
            context
        )

        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            f_layer.fields(),
            f_layer.wkbType(),
            f_layer.sourceCrs()
        )

        fields = QgsFields()
        fields.append(QgsField('customer_id', QVariant.String))
        fields.append(QgsField('facility_id', QVariant.String))
        fields.append(QgsField('value', QVariant.Double))

        (sink_lines, dest_id_lines) = self.parameterAsSink(
            parameters,
            self.OUTPUT_LINES,
            context,
            fields,
            QgsWkbTypes.LineString,
            f_layer.sourceCrs()
        )


        # ######################## use pulp for site selection
        if feedback is None:
            feedback = QgsProcessingFeedback()

        Supermarkets_shp = self.convertToGeoPandas(c_layer, feedback)
        Warehouses_shp = self.convertToGeoPandas(f_layer, feedback)
        feedback.pushInfo(f"customer layer: {c_layer.name()}, facility layer: {f_layer.name()}")
        
        # SETS
        SUPERMARKETS = list(Supermarkets_shp[C_ID])
        WAREHOUSES =  list(Warehouses_shp[F_ID])
        demand = dict(zip(SUPERMARKETS,Supermarkets_shp[C_Demand]))
        actcost = dict(zip(WAREHOUSES,Warehouses_shp[F_Cost]))
        maxam = dict(zip(WAREHOUSES,Warehouses_shp[F_Cap]))
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
        feedback.pushInfo(f"Status:: {LpStatus[prob.status]}")

        TOL = 0.0001
        results=[]
        for i in WAREHOUSES:
            if use_vars[i].varValue > TOL:
                feedback.pushInfo(f"Establish warehouse at: {i}.")
                results.append(i)

        for v in prob.variables():
            if v.varValue>0:
                feedback.pushInfo(f"{v.name} = {v.varValue}")

        feedback.pushInfo(f"Create a new line layer")
        # create a new line layer
        customer_id = []
        facility_id = []
        values = []
        for v in prob.variables():
            if v.varValue>0 and v.name.startswith("Service"):
                feedback.pushInfo(f"{v.name} = {v.varValue}")
                customer_id.append(int(re.findall('\d+', v.name)[0]))
                facility_id.append(int(re.findall('\d+', v.name)[1]))
                values.append(v.varValue)

        # create optimal facility site layer
        features = f_layer.getFeatures()
        for current, feature in enumerate(features):
            idx = feature.fieldNameIndex(F_ID)
            if (feature.attributes()[idx] in facility_id):
                sink.addFeature(feature, QgsFeatureSink.FastInsert)


        # create connectivity layer
        # lines = [LineString([Supermarkets_shp.query(f"Shop_ID == {i}").geometry.values[0], Warehouses_shp.query(f"WH_ID == {j}").geometry.values[0]]) for i,j in zip(customer_id,facility_id)]
        # result_value = pd.DataFrame({"customer_id":customer_id,"facility_id":facility_id,"value":values})
        # result_lines = gpd.GeoDataFrame(result_value,geometry=lines)
        # print(result_lines.to_json())

        for i,j,value in zip(customer_id,facility_id,values):
            feat = QgsFeature()
            feat.setGeometry(QgsGeometry.fromPolylineXY([QgsPointXY(Supermarkets_shp.query(f"{C_ID} == {i}").geometry.values[0].x, 
                                                                    Supermarkets_shp.query(f"{C_ID} == {i}").geometry.values[0].y),
                                                            QgsPointXY(Warehouses_shp.query(f"{F_ID} == {j}").geometry.values[0].x, 
                                                                    Warehouses_shp.query(f"{F_ID} == {j}").geometry.values[0].y)]))
            feat.setAttributes([i, j, value])
            sink_lines.addFeature(feat, QgsFeatureSink.FastInsert)

        return {self.OUTPUT:dest_id, self.OUTPUT_LINES:dest_id_lines}

    def compute_distance(self,loc1, loc2):
        dx = loc1[0] - loc2[0]
        dy = loc1[1] - loc2[1]
        return math.sqrt(dx*dx + dy*dy)
        
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

    def convertToGeoPandas(self, layer, feedback):
        try:
            if layer is not None:
                gdf = gpd.GeoDataFrame(self.convertToPandas(layer), geometry='geometry')
                gdf = gdf.set_crs(crs=layer.crs().toWkt())
                return gdf
        except Exception as e:
            feedback.reportError(e.message)
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
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink)
from qgis import processing
from qgis.core import QgsProcessingParameterField, QgsProcessingUtils
from qgis.core import QgsField, QgsFields, QgsFeature,QgsFeatureRequest
from PyQt5.QtCore import QVariant

# Networkx
import networkx as nx

class TspProcessingAlgorithm(QgsProcessingAlgorithm):
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

    INPUT_NETWORK = 'INPUT_NETWORK'
    INPUT_LOCATIONS = 'INPUT_LOCATIONS'
    
    LOCATION_ID_FIELD = "LOCATION_ID_FIELD"

    
    OUTPUT = 'OUTPUT'
    
    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return TspProcessingAlgorithm()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'tsp'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Traveling salesman problem')

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
        return self.tr("Returns an approximate solution to the traveling salesman problem using networkx")

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_NETWORK,
                self.tr('Input Road Network Layer'),
                [QgsProcessing.TypeVectorLine]))
        
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_LOCATIONS,
                self.tr('Input Point Location Layer'),
                [QgsProcessing.TypeVectorPoint]))
                
        self.addParameter(
            QgsProcessingParameterField(
                    self.LOCATION_ID_FIELD,
                    'Choose Point Location ID',
                    '',
                    self.INPUT_LOCATIONS))
                    
        # We add a feature sink in which to store our processed features
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Output layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        
        outputs = {}
        results = {}
        # Retrieve the feature source and sink. The 'dest_id' variable is used
        # to uniquely identify the feature sink, and must be included in the
        # dictionary returned by the processAlgorithm function.

        
        source_network = self.parameterAsSource(
            parameters,
            self.INPUT_NETWORK,
            context
        )
        
        source_locations = self.parameterAsSource(
            parameters,
            self.INPUT_LOCATIONS,
            context
        )

        # If source was not found, throw an exception to indicate that the algorithm
        # encountered a fatal error. The exception text can be any string, but in this
        # case we use the pre-built invalidSourceError method to return a standard
        # helper text for when a source cannot be evaluated

        if source_network is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT_NETWORK))
            
        if source_locations is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT_LOCATIONS))
            
            
        location_id_field = self.parameterAsString(
                parameters,
                self.LOCATION_ID_FIELD,
                context)
        
        # for the final sink fields
        fields = QgsFields()
        fields.append(QgsField('ID', QVariant.Int))
        fields.append(QgsField('Origin', QVariant.String))
        fields.append(QgsField('Destination', QVariant.String))
        fields.append(QgsField('Cost', QVariant.String))
                
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            source_network.wkbType(),
            source_network.sourceCrs()
        )

        # Send some information to the user
        feedback.pushInfo('CRS is {}'.format(source_network.sourceCrs().authid()))

        # If sink was not created, throw an exception to indicate that the algorithm
        # encountered a fatal error. The exception text can be any string, but in this
        # case we use the pre-built invalidSinkError method to return a standard
        # helper text for when a sink cannot be evaluated
        if sink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))
        
        # generate OD Matrix
        # OD-Matrix from Points as CSV (n:n)
        
        alg_params = {
            'DEFAULT_DIRECTION': 2,  # Both directions
            'DEFAULT_SPEED': 5,
            'DIRECTION_FIELD': '',
            'ENTRY_COST_CALCULATION_METHOD': 1,  # planar
            'ID_FIELD': location_id_field,
            'INPUT': parameters['INPUT_NETWORK'],
            'POINTS': parameters['INPUT_LOCATIONS'],
            'SPEED_FIELD': '',
            'STRATEGY': 0,  # Shortest Path (distance optimization)
            'TOLERANCE': 0,
            'VALUE_BACKWARD': '',
            'VALUE_BOTH': '',
            'VALUE_FORWARD': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        algresult = processing.run('qneat3:OdMatrixFromPointsAsCsv', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        csv = QgsProcessingUtils.mapLayerFromString(algresult['OUTPUT'],context)
        
        # create a networkx graph
        G = nx.Graph()
        
        # Compute the number of steps to display within the progress bar and
        # get features from source

        features = csv.getFeatures()
        for current, feature in enumerate(features):
            if (feature['total_cost'] == None) or (feature['total_cost'] == 0): 
                feedback.pushInfo(f"origin_id is {feature['origin_id']}, destination_id is {feature['destination_id']}, cost is {feature['total_cost']}")
                continue
            if (feature['origin_id'] != feature['destination_id']):
                G.add_edge(str(feature['origin_id']), str(feature['destination_id']), weight=float(feature['total_cost']))
        
        feedback.pushInfo("method 1: simulated annealing")
        path_sa = nx.approximation.simulated_annealing_tsp(G, "greedy")
        cost_sa = sum(G[n][nbr]["weight"] for n, nbr in nx.utils.pairwise(path_sa))
        feedback.pushCommandInfo(str(path_sa))
        feedback.pushInfo("total cost of method 1 is: " + str(cost_sa))
        
        feedback.pushInfo("method 2: christofides")
        tsp = nx.approximation.traveling_salesman_problem
        path = tsp(G)
        feedback.pushCommandInfo(str(path))
        cost_tsp = sum(G[n][nbr]["weight"] for n, nbr in nx.utils.pairwise(path))
        feedback.pushInfo("total cost of method 2 is: " + str(cost_tsp))
        
        # To run another Processing algorithm as part of this algorithm, you can use
        # processing.run(...). Make sure you pass the current context and feedback
        # to processing.run to ensure that all temporary layer outputs are available
        # to the executed algorithm, and that the executed algorithm can send feedback
        # reports to the user (and correctly handle cancellation and progress reports!)
        featID = 0
        i = 0
        for n, nbr in nx.utils.pairwise(path):
            i += 1
            feedback.setProgressText(f"processing {i} out of {len(path)-1} segments")

            #get point locations
            query_start = '"ID" = \''+ str(n) +'\''
            query_to = '"ID" = \''+ str(nbr) +'\''
            features_start_loc = source_locations.getFeatures(QgsFeatureRequest().setFilterExpression(query_start))
            features_to_loc = source_locations.getFeatures(QgsFeatureRequest().setFilterExpression(query_to))
            feat_start = QgsFeature()
            feat_to = QgsFeature()
            features_start_loc.nextFeature(feat_start)
            features_to_loc.nextFeature(feat_to)

            alg_params = {
                'DEFAULT_DIRECTION': 2,  # Both directions
                'DEFAULT_SPEED': 5,
                'DIRECTION_FIELD': '',
                'END_POINT': str(feat_to.geometry().asPoint().x()) +','+ str(feat_to.geometry().asPoint().y())+ ' [EPSG:3414]',
                'ENTRY_COST_CALCULATION_METHOD': 1,  # planar
                'INPUT': parameters['INPUT_NETWORK'],
                'SPEED_FIELD': '',
                'START_POINT': str(feat_start.geometry().asPoint().x()) +','+ str(feat_start.geometry().asPoint().y())+ ' [EPSG:3414]',
                'STRATEGY': 0,  # Shortest Path (distance optimization)
                'TOLERANCE': 0,
                'VALUE_BACKWARD': '',
                'VALUE_BOTH': '',
                'VALUE_FORWARD': '',
                'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            }
            algresult2 = processing.run('qneat3:shortestpathpointtopoint', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            layer = QgsProcessingUtils.mapLayerFromString(algresult2['OUTPUT'],context)
            features = layer.getFeatures()

            # the shortest path between two points should be one polyline feature
            # Note: there is only one feature here, thus featID = 0 is put outside of the if

            for _, feature in enumerate(features):
                # Add a feature in the sink
                featID +=1
                feat = QgsFeature(fields)
                feat.setAttributes([featID,str(n),str(nbr),G[n][nbr]["weight"]])
                feat.setGeometry(feature.geometry())
                sink.addFeature(feat, QgsFeatureSink.FastInsert)
        
        # Return the results of the algorithm. In this case our only result is
        # the feature sink which contains the processed features, but some
        # algorithms may return multiple feature sinks, calculated numeric
        # statistics, etc. These should all be included in the returned
        # dictionary, with keys matching the feature corresponding parameter
        # or output names.
        return {self.OUTPUT: dest_id}

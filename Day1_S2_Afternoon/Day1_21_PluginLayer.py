class WatermarkLayerRenderer(QgsMapLayerRenderer):

    def __init__(self, layerId, rendererContext):
        super().__init__(layerId, rendererContext)

    def render(self):
        image = QImage("Day1_S1_Morning/icon_sla.gif")
        painter = self.renderContext().painter()
        painter.save()
        painter.setOpacity(0.1)
        painter.drawImage(2, 2, image)
        painter.restore()
        return True

class WatermarkPluginLayer(QgsPluginLayer):

    LAYER_TYPE = "watermark"

    def __init__(self):
        super().__init__(WatermarkPluginLayer.LAYER_TYPE, "Watermark plugin layer")
        self.setValid(True)

    def createMapRenderer(self, rendererContext):
        return WatermarkLayerRenderer(self.id(), rendererContext)

    def setTransformContext(self, ct):
        pass

    # Methods for reading and writing specific information to the project file can
    # also be added:

    def readXml(self, node, context):
        pass

    def writeXml(self, node, doc, context):
        pass

# When loading a project containing such a layer, a factory class is needed
# class WatermarkPluginLayerType(QgsPluginLayerType):

#     def __init__(self):
#         super().__init__(WatermarkPluginLayer.LAYER_TYPE)

#     def createLayer(self):
#         return WatermarkPluginLayer()

#     # You can also add GUI code for displaying custom information
#     # in the layer properties
#     def showLayerProperties(self, layer):
#         pass

# Keep a reference to the instance in Python so it won't
# be garbage collected
# plt =  WatermarkPluginLayerType()
# assert(QgsApplication.pluginLayerRegistry().addPluginLayerType(plt))

# add layer
plugin_layer = WatermarkPluginLayer()
QgsProject.instance().addMapLayer(plugin_layer)

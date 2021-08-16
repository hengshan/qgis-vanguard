import random
from qgis.core import QgsWkbTypes, QgsSymbol, QgsFeatureRenderer
from qgis.gui import QgsRendererWidget, QgsColorButton
from qgis.core import (
  QgsRendererAbstractMetadata,
  QgsRendererRegistry,
  QgsApplication
)

#  shows a simple custom renderer that creates two marker symbols 
# and chooses randomly one of them for every feature
class RandomRenderer(QgsFeatureRenderer):
    def __init__(self, syms=None):
        # each renderer has a unique name
        super().__init__("RandomRenderer")
        self.syms = syms if syms else [QgsSymbol.defaultSymbol(QgsWkbTypes.geometryType(QgsWkbTypes.Point)),QgsSymbol.defaultSymbol(QgsWkbTypes.geometryType(QgsWkbTypes.Point))]

    #decides what symbol will be used for a particular feature. 
    def symbolForFeature(self, feature, context):
        return random.choice(self.syms)

    #initialization of symbol rendering. 
    def startRender(self, context, fields):
        super().startRender(context, fields)
        for s in self.syms:
         s.startRender(context, fields)

    #finalization of symbol rendering. 
    def stopRender(self, context):
        super().stopRender(context)
        for s in self.syms:
         s.stopRender(context)

    #return a list of field names that the renderer expects to be present.
    def usedAttributes(self, context):
        return []

    def clone(self):
        return RandomRenderer(self.syms)



class RandomRendererWidget(QgsRendererWidget):
    # The constructor receives instances of the active layer (QgsVectorLayer),
    # the global style (QgsStyle)
    # and the current renderer.
    def __init__(self, layer, style, renderer):
        super().__init__(layer, style)
        if renderer is None or renderer.type() != "RandomRenderer":
            self.r = RandomRenderer()
        else:
            self.r = renderer

        # setup UI
        self.btn1 = QgsColorButton()
        self.btn1.setColor(self.r.syms[0].color())
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.btn1)
        self.setLayout(self.vbox)
        self.btn1.colorChanged.connect(self.setColor1)

    def setColor1(self):
        color = self.btn1.color()
        if not color.isValid(): 
            return
        self.r.syms[0].setColor(color)

    def renderer(self):
        return self.r

class RandomRendererMetadata(QgsRendererAbstractMetadata):

    def __init__(self):
        super().__init__("RandomRenderer", "Random renderer", QIcon('Recourses/icon_sla.gif'))

    # passes a QDomElement instance that can be used to restore the renderer’s state from the DOM tree. 
    def createRenderer(self, element):
        return RandomRenderer()

    def createRendererWidget(self, layer, style, renderer):
        return RandomRendererWidget(layer, style, renderer)

rrmetadata = RandomRendererMetadata()
QgsApplication.rendererRegistry().addRenderer(rrmetadata)
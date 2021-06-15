from qgis.core import QgsMarkerSymbolLayer
from qgis.PyQt.QtGui import QColor
from qgis.gui import QgsSymbolLayerWidget
from qgis.core import QgsSymbol, QgsSymbolLayerAbstractMetadata, QgsSymbolLayerRegistry

# You can create your own symbol layer class that will draw the features exactly as you wish. 
# Here is an example of a marker that draws red circles with specified radius
class FooSymbolLayer(QgsMarkerSymbolLayer):

  def __init__(self, radius=10.0):
      QgsMarkerSymbolLayer.__init__(self)
      self.radius = radius
      self.color = QColor(255,0,0)

  # The layerType() method determines the name of the symbol layer; 
  # it has to be unique among all symbol layers. 
  def layerType(self):
     return "FooMarker"

  #The properties() method is used for persistence of attributes. 
  def properties(self):
      return { "radius" : str(self.radius) }

  #startRender() is called before rendering the first feature
  def startRender(self, context):
    pass

  #stopRender() when the rendering is done
  def stopRender(self, context):
      pass

  #renderPoint() is called to do the rendering.
  def renderPoint(self, point, context):
      # Rendering depends on whether the symbol is selected (QGIS >= 1.5)
      color = context.selectionColor() if context.selected() else self.color
      p = context.renderContext().painter()
      p.setPen(color)
      p.drawEllipse(point, self.radius, self.radius*2)

  #return a copy of the symbol layer with all attributes being exactly the same. 
  def clone(self):
      return FooSymbolLayer(self.radius)


#This widget can be embedded into the symbol properties dialog. 
#When the symbol layer type is selected in symbol properties dialog, 
# it creates an instance of the symbol layer and an instance of the symbol layer widget. 
class FooSymbolLayerWidget(QgsSymbolLayerWidget):
    def __init__(self, parent=None):
        QgsSymbolLayerWidget.__init__(self, parent)

        self.layer = None

        # setup a simple UI
        self.label = QLabel("Radius:")
        self.spinRadius = QDoubleSpinBox()
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.label)
        self.hbox.addWidget(self.spinRadius)
        self.setLayout(self.hbox)
        self.connect(self.spinRadius, SIGNAL("valueChanged(double)"), \
            self.radiusChanged)

    # to assign the symbol layer to the widget. 
    # In that method the widget should update the UI to reflect the attributes of the symbol layer. 
    def setSymbolLayer(self, layer):
        if layer.layerType() != "FooMarker":
            return
        self.layer = layer
        self.spinRadius.setValue(layer.radius)
    
    #The symbolLayer() method is used to retrieve the symbol layer again by the properties dialog to use it for the symbol.
    def symbolLayer(self):
        return self.layer

    #On every change of attributes, the widget should emit the changed() signal to let the properties dialog update the symbol preview.
    def radiusChanged(self, value):
        self.layer.radius = value
        self.emit(SIGNAL("changed()"))


class FooSymbolLayerMetadata(QgsSymbolLayerAbstractMetadata):

  def __init__(self):
    super().__init__("FooMarker", "My new Foo marker", QgsSymbol.Marker)

  def createSymbolLayer(self, props):
    radius = float(props["radius"]) if "radius" in props else 10.0
    return FooSymbolLayer(radius)

  def createSymbolLayerWidget(self, layer):
    return FooSymbolLayerWidget()

fslmetadata = FooSymbolLayerMetadata()
QgsApplication.symbolLayerRegistry().addSymbolLayerType(fslmetadata)
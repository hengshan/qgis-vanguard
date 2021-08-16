import pandas as pd
import numpy as np
import random

myVectorLayer = iface.activeLayer()

myTargetField = 'size'

myOpacity = 1
groups = 20
# the range of the field
size = QgsVectorLayerUtils.getValues(myVectorLayer, myTargetField)
size[0] # is the list of values

size_cut = pd.cut(size[0], bins=np.linspace(np.min(size[0]), np.max(size[0]), groups+1))

myRangeList = []
# Make a list of symbols and ranges...
for i in range(1,groups+1):
     myMin = size_cut.unique()[i].left
     myMax = size_cut.unique()[i].right
     myLabel = 'Group '+str(i)
     myColour = QtGui.QColor("#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])) # generate a random color
     mySymbol = QgsSymbol.defaultSymbol(myVectorLayer.geometryType())
     mySymbol.setColor(myColour)
     mySymbol.setWidth(1)
     mySymbol.setOpacity(myOpacity)
     myRange = QgsRendererRange(myMin, myMax, mySymbol, myLabel)
     myRangeList.append(myRange)

# create a Graduated Symbol Renderer
myRenderer = QgsGraduatedSymbolRenderer('', myRangeList)
myClassificationMethod = QgsApplication.classificationMethodRegistry().method("EqualInterval")

myRenderer.setClassificationMethod(myClassificationMethod)
myRenderer.setClassAttribute(myTargetField)

myVectorLayer.setRenderer(myRenderer)
myVectorLayer.triggerRepaint()
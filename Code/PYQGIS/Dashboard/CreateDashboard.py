a = QgsHtmlAnnotation()
a.fillSymbol().symbolLayer(0).setStrokeColor(QColor(0, 0, 0))
a.setFrameSize(QSizeF(200, 440)) #dashboard size
a.setRelativePosition(QPointF(0, 0)) # dashboard relative location
#a.setRelativePosition(QPointF(0, 0.25)) # dashboard relative location
a.setHasFixedMapPosition(False)
html = "Code/PYQGIS/Dashboard/dashboard.html"
a.setSourceFile(html)

QgsProject.instance().annotationManager().addAnnotation(a)

######## parse html and update
from bs4 import BeautifulSoup

with open(html) as f:
    #read File
    content = f.read()
    print(content)
    #parse HTML
    soup = BeautifulSoup(content, 'html.parser')

# add feature selection change event
lyr=iface.activeLayer()
def myFunction(selFeatures):
    soup.find('div', id = "value1").string = str(len(selFeatures))
    print(str(len(selFeatures)) + " features were selected: " + str(selFeatures))
    with open(html,'w', encoding='utf-8') as infile:
        infile.write(str(soup))  # OR infile.write(a.prettify())
    a.setSourceFile(html)
    
lyr.selectionChanged.connect(myFunction)
myFunction(lyr.selectedFeatures()) # clean 
# Construct Geometry from coordinates
gPnt = QgsGeometry.fromPointXY(QgsPointXY(1,1)) 
print(gPnt) 
print(gPnt.wkbType())

gLine = QgsGeometry.fromPolyline([QgsPoint(1, 1), QgsPoint(2, 2)]) 
print(gLine) 
print(gLine.wkbType())

gPolygon = QgsGeometry.fromPolygonXY([[QgsPointXY(1, 1), QgsPointXY(2, 2), QgsPointXY(2, 1)]]) 
print(gPolygon)
print(gPolygon.wkbType())

# Construct Geometry from well known text
geom = QgsGeometry.fromWkt("POINT(3 4)")
print(geom)

# Construct Geometry from from well-known binary (WKB)
g = QgsGeometry()
wkb = bytes.fromhex("010100000000000000000045400000000000001440")
g.fromWkb(wkb)

# print WKT representation of the geometry
print(g.asWkt())
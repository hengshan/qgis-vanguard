layer = iface.activeLayer()
my_list = [2, 5, 9, 17, 21, 26, 31, 32, 36]
values = ','.join(str(x) for x in my_list)
layer.selectByExpression('\"WH_ID\" IN (' + values + ')', QgsVectorLayer.SetSelection)
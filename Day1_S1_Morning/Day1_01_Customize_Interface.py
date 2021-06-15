import os
from datetime import datetime

# change curent work directory to the pyqgis folder
os.chdir("/Users/hs/Projects/pyqgis")

icon_name = 'Day1_S1_Morning/icon_sla.gif'

def show_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    iface.messageBar().pushMessage('Time is {}'.format(current_time))
    
action = QAction('Show Time')
action.triggered.connect(show_time)

action.setIcon(QIcon(icon_name))
iface.addToolBarIcon(action)

# you can delete it using the following command
# iface.removeToolBarIcon(action)

#change app icon
iface.mainWindow().setWindowIcon(QIcon(icon_name))

# change title
title = iface.mainWindow().windowTitle()
new_title = "QGIS Vanguard"
iface.mainWindow().setWindowTitle(new_title)

# you can change the canvas color using the following commands
#iface.mapCanvas().setCanvasColor(Qt.black)
#iface.mapCanvas().refresh()

############ add menu
import webbrowser

#SLA website
def open_website():
    webbrowser.open('https://www.sla.gov.sg/')

#Onemap website
def open_website2():
    webbrowser.open('https://www.onemap.sg/home/index.html')

#Geospace website    
def open_website3():
    webbrowser.open('https://geospace.gov.sg/jsapp/index.jsp')
    
website_action = QAction('Go to SLA website')
website_action.triggered.connect(open_website)

website_action2 = QAction('Go to OneMap website')
website_action2.triggered.connect(open_website2)

website_action3 = QAction('Go to Geospace website')
website_action3.triggered.connect(open_website3)

myMenu = QMenu( "&Hello SLA", iface.mainWindow().menuBar())
actions = iface.mainWindow().menuBar().actions()
lastAction = actions[-1]
iface.mainWindow().menuBar().insertMenu(lastAction, myMenu)

myMenu.addAction(website_action)
myMenu.addSeparator()
myMenu.addAction(website_action2)
myMenu.addSeparator()
myMenu.addAction(website_action3)

#!/usr/bin/env python
  
import math,inspect
# import sys
from PyQt4 import QtGui, QtOpenGL, QtCore
  #import Image, ImageOps
from config import *
from shapes import *
#import gizehlib
from stories import *
#import time
#  import argparse
  
from OpenGlApplication import OpenGlApplication

story_parts = ["key","summary","assigned","storyPoints", "state","progress"]

  
# This is the main PyQt controls window that will allow the user to access the 
# OpenGL displayed circles, as well as configure progress, dependencies and the title
class MainWindow(QtGui.QWidget):
 
    storyModified = QtCore.pyqtSignal()
  
    def __init__(self,stories):
        super(MainWindow, self).__init__()
        self.stories = stories
        self.message = "Click on a circle for story information"
        self.uiinit()
  
    def uiinit(self):
       # Top main drawing area 
        self.widget = OpenGlApplication(self.stories)
        self.widget.show()
        self.widget.circleSelected.connect(self.circle_selected)
        self.storyModified.connect(self.widget.repaint)
        self.storyModified.connect(self.circle_selected)
 
#        buttonLayout= QtGui.QGridLayout()
        buttonLayout = QtGui.QSplitter(QtCore.Qt.Vertical)
  
        titleLabel = QtGui.QLabel("Story Title")

        titleSplitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.titleField = QtGui.QLineEdit()
        self.setTitleButton = QtGui.QPushButton("Set as Story Title")
        self.setTitleButton.clicked.connect(self.set_title)
        titleSplitter.addWidget(self.titleField)
        titleSplitter.addWidget(self.setTitleButton)

        buttonLayout.addWidget(titleLabel)
        buttonLayout.addWidget(titleSplitter)
  
        progressSplitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.progressSpinbox = QtGui.QSpinBox()
        self.progressSpinbox.setValue(0)
        self.progressSpinbox.setRange(0,100)
        self.progressSpinbox.setSingleStep(25)
        self.progressSpinbox.setFixedWidth(100)
        progressSplitter.addWidget(self.progressSpinbox)

        setProgress = QtGui.QPushButton("Set Progress")
        setProgress.clicked.connect(self.setProgressAction)
        progressSplitter.addWidget(setProgress)

        buttonLayout.addWidget(progressSplitter)
#        buttonLayout.addWidget(setProgress)
  
  #        self.stateSelector=QtGui.QListWidget()
        self.stateSelector=QtGui.QComboBox()
        for x in story_states:
              self.stateSelector.addItem(story_states[x])
        buttonLayout.addWidget(self.stateSelector)
        self.stateSelector.activated.connect(self.combo_activate)


        sideLayout = QtGui.QSplitter(QtCore.Qt.Horizontal)
  #        sideLayout.SetMinAndMaxSize
  
  
  
        infoLayout = QtGui.QSplitter(QtCore.Qt.Vertical)
#        infoLayout.setMargin(5)
  
  
        self.infoBox = QtGui.QTextEdit()
        self.infoBox.setText(self.message)
        infoLayout.addWidget(self.infoBox)

        exportFileLabel = QtGui.QLabel("Export to image file")
        infoLayout.addWidget(exportFileLabel)

        imageLayout = QtGui.QSplitter(QtCore.Qt.Horizontal)
        selectFileButton = QtGui.QPushButton("Select File")
        selectFileButton.clicked.connect(self.select_file)
        imageLayout.addWidget(selectFileButton)

        self.imageField = QtGui.QLineEdit()
        self.imageField.setText("image1.bmp")
        imageLayout.addWidget(self.imageField)

        framebufferButton = QtGui.QPushButton("Framebuffer image")
        framebufferButton.clicked.connect(self.framebufferAction)
        imageLayout.addWidget(framebufferButton)
  
#        gizehButton = QtGui.QPushButton("Gizeh image")
#        gizehButton.clicked.connect(self.gizehImageAction)
#        imageLayout.addWidget(gizehButton)
  
  
        self.imageExportLabel = QtGui.QLabel()
  
        infoLayout.addWidget(imageLayout)
        infoLayout.addWidget(self.imageExportLabel)
  
        sideLayout.addWidget(infoLayout)
        sideLayout.addWidget(buttonLayout)
  
  
        self.dependencyList = QtGui.QListWidget()
        self.dependencyList.setFixedWidth(100)
  
        dependencyButtonLayout = QtGui.QSplitter(QtCore.Qt.Vertical)
        depTitle = QtGui.QLabel("Dependency links")
        addDepButton = QtGui.QPushButton("<-Add ")
        addDepButton.clicked.connect(self.addDependency)
        removeDepButton = QtGui.QPushButton("Remove->")
        removeDepButton.clicked.connect(self.removeDependency)
  
        dependencyButtonLayout.addWidget(depTitle)
        dependencyButtonLayout.addWidget(addDepButton)
        dependencyButtonLayout.addWidget(removeDepButton)
  
        self.candidateList = QtGui.QListWidget()
        self.candidateList.setFixedWidth(100)
  
        sideLayout.addWidget(self.dependencyList)
        sideLayout.addWidget(dependencyButtonLayout)
        sideLayout.addWidget(self.candidateList)

        graphic_splitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        graphic_splitter.addWidget(self.widget)
        graphic_splitter.addWidget(sideLayout)
        graphic_splitter.setStretchFactor(0,1)
        graphic_splitter.setStretchFactor(1,0)

        finalLayout = QtGui.QVBoxLayout()
        finalLayout.addWidget(graphic_splitter)
#        finalLayout.addWidget(sideLayout)
        self.setLayout(finalLayout)
        self.setWindowTitle("Main window")
  #      self.setGeometry(300,300,300,300)
        self.show()
  
    def set_text_message(self):
        self.infoBox.setText(self.message)



    def setProgressAction(self):
  #        print "setProgress"
        target = self.stories[self.widget.focus]
        new_progress = self.progressSpinbox.value()
        target.update_progress(new_progress)
        self.storyModified.emit()
  
    def set_title(self):
        newtitle = self.titleField.text()
        target = self.stories[self.widget.focus]
        target.set_title(str(newtitle))
        self.storyModified.emit()
  
    def combo_activate(self, text):
  #        target = self.stories[self.widget.focus]
        new_state =  story_states.keys().index(text)
        self.stories[self.widget.focus].update_state(new_state)
        self.storyModified.emit()
  
    def circle_selected(self):
        self.message = ""
        if self.widget.focus != None:
            target = self.stories[self.widget.focus]
            self.progressSpinbox.setValue(target.progress)
            self.stateSelector.setCurrentIndex(target.state)
  #        print "button clicked: ", x,y
            for x in story_parts:
                pp = getattr(target, x)
                if not ((pp == None  or inspect.ismethod(pp))):
                    self.message = self.message + x + ":  " + str(pp) + "\n"
  # populate dependency and candidate lists
            self.titleField.setText(target.title)
  
            self.dependencyList.clear()
  #            self.dependencyList.addItems(["blah","mah"])
            for x in target.dependencies:
                self.dependencyList.addItem(str(x))
  #            print set(self.stories), set(target.dependencies), set([target.key])
            candidates = set(self.stories.keys()) -  set(target.dependencies)  - set([target.key])
  #            print candidates
            self.candidateList.clear()
            for y in list(candidates):
                self.candidateList.addItem(str(y))
        self.set_text_message()
  
   
    def addDependency(self):
        target = self.stories[self.widget.focus]
  #      print "add Dependency"
        addItemds = self.candidateList.selectedItems()
        for x in addItemds:
            target.set_dependency(str(x.text()))
        self.storyModified.emit()
        self.circle_selected()
   
  
    def removeDependency(self):
  #      print"remove Dependency"
        target = self.stories[self.widget.focus]
  #      print "Remove Dependency"
        remItems = self.dependencyList.selectedItems()
        for x in remItems:
            target.remove_dependency(str(x.text()))
        self.storyModified.emit()
        self.circle_selected()


    def select_file(self):
        selectedFile = QtGui.QFileDialog(icaption="export image file", directory="./images")
        self.imageField.setText(selectedFile)

    def framebufferAction(self):
        if len(self.stories) == 0:
            self.infoText.setText("No stories loaded")
        elif self.imageField.text == " ":
            self.infoText.setText("No filename specified")
        else:
            filename = str(self.imageField.text())
            try:
                self.widget.output_to_file(filename)
                self.imageExportLabel.setText("Image exported to " + filename)
            except:
                self.imageExportLabel.setText("exception raised")


            

#    def gizehImageAction(self):
#        if len(self.stories) == 0:
#            self.infoText.setText("No stories loaded")
#        elif self.imageField.text == " ":
#            self.infoText.setText("No filename specified")
#        else:
#          filename = str(self.imageField.text())
#          self.stories = self.widget.stories
#          gizehlib.output_to_file(self.stories, filename, self.widget.width*2/3, self.widget.height)
  

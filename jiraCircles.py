#!/usr/bin/env python

import math,sys, inspect
from PyQt4 import QtGui, QtOpenGL, QtCore
#import Image, ImageOps
from config import *
from shapes import *
#import gizehlib
from stories import *
import time
import argparse

from OpenGlApplication import OpenGlApplication
from MainWindow import MainWindow



class ConfigWidget(QtGui.QWidget):
    """This pyqt widget allows the user to choose to load the stories from 
    Jira, JSOn file or stubs"""

    storiesLoaded = QtCore.pyqtSignal()
    updateStories = QtCore.pyqtSignal()

    def __init__(self):
        super(ConfigWidget, self).__init__()
        self.initUI()
        self.stories ={} 
#        self.storiesLoaded.connect(self.connectStoriesLoaded)

    def initUI(self):
        loadLayout = QtGui.QHBoxLayout()

# All the labels
        leftLabelLayout = QtGui.QVBoxLayout()
        
        leftLabelLayout.setMargin(2)
    
        fileName = QtGui.QLabel("File name")
        leftLabelLayout.addWidget(fileName)

        jiraServer = QtGui.QLabel("Jira server")
        leftLabelLayout.addWidget(jiraServer)

        login = QtGui.QLabel("Login")
        leftLabelLayout.addWidget(login)

        password = QtGui.QLabel("Password")
        leftLabelLayout.addWidget(password)


        filter_label = QtGui.QLabel("Jira filter")
        leftLabelLayout.addWidget(filter_label)

# All the load fields
        leftFieldsLayout = QtGui.QVBoxLayout()

        loadFileLayout = QtGui.QHBoxLayout()
        loadFileButton = QtGui.QPushButton("select file")
        loadFileButton.clicked.connect(self.loadFileAction)
        loadFileLayout.addWidget(loadFileButton)

        self.fileNameField = QtGui.QLineEdit()
        loadFileLayout.addWidget(self.fileNameField)
        leftFieldsLayout.addLayout(loadFileLayout)


        self.jiraServerField = QtGui.QLineEdit()
        self.jiraServerField.setText('http://jira.vsl.com.au')
#        self.jiraServerField.setText('hardcoded')
        leftFieldsLayout.addWidget(self.jiraServerField)
        
        self.loginField = QtGui.QLineEdit()
        leftFieldsLayout.addWidget(self.loginField)

        self.passwordField = QtGui.QLineEdit()
        self.passwordField.setEchoMode(QtGui.QLineEdit.Password)
        leftFieldsLayout.addWidget(self.passwordField)

        self.storyFilterField = QtGui.QLineEdit()
        self.storyFilterField.setMinimumSize(300,10)
        self.storyFilterField.setText('project = TSM AND sprint = 405 AND type != "Technical task" AND status != Rejected')
        leftFieldsLayout.addWidget(self.storyFilterField)


        # layout on the right: load source selector, and save
        rightLayout = QtGui.QVBoxLayout()


        self.loadRadioBox = QtGui.QButtonGroup()
        fromfile = QtGui.QRadioButton("from file")
        self.loadRadioBox.addButton(fromfile, 0)
#        fromStub = QtGui.QRadioButton("from Stub")
#        self.loadRadioBox.addButton(fromStub, 1)
        fromJira = QtGui.QRadioButton("from Jira")
        self.loadRadioBox.addButton(fromJira, 2)
#        fromFileJira = QtGui.QRadioButton("from FileJira")
#        self.loadRadioBox.addButton(fromFileJira, 3)

        rightLayout.addWidget(fromfile)
#        rightLayout.addWidget(fromStub)
        rightLayout.addWidget(fromJira)
#        rightLayout.addWidget(fromFileJira)

        loadStoriesButton = QtGui.QPushButton("Load stories")
        loadStoriesButton.clicked.connect(self.loadStoriesAction)
        rightLayout.addWidget(loadStoriesButton)

        loadLayout.addLayout(rightLayout, 1)
        loadLayout.addLayout(leftLabelLayout)
        loadLayout.addLayout(leftFieldsLayout, 3)

# Saving stuff
        saveLayout = QtGui.QHBoxLayout()
       
#        saveFileLayout = QtGui.QHBoxLayout()
        saveFileButton = QtGui.QPushButton("select file")
        saveFileButton.clicked.connect(self.saveFileAction)
        saveLayout.addWidget(saveFileButton)

        self.saveFileNameField = QtGui.QLineEdit()
        saveLayout.addWidget(self.saveFileNameField)

        saveStories = QtGui.QPushButton("Save stories")
        saveStories.clicked.connect(self.saveStoriesAction)
        saveLayout.addWidget(saveStories)


# Assemble them: load layout, load info, save layout, save info
        finalLayout = QtGui.QVBoxLayout()

        load_title = QtGui.QLabel()
        load_stories_title = "<b> Load Stories </b>"
        load_title.setText(load_stories_title)
        finalLayout.addWidget(load_title)
        finalLayout.addLayout(loadLayout)

#        self.loadInfoText = QtGui.QLabel()
#        finalLayout.addWidget(self.loadInfoText)

        save_title = QtGui.QLabel()
        save_stories_title = "<b> Save Stories </b>"
        save_title.setText(save_stories_title)
        finalLayout.addWidget(save_title)
        finalLayout.addLayout(saveLayout)

        self.loadInfoText = QtGui.QLabel()
        finalLayout.addWidget(self.loadInfoText)

        self.setLayout(finalLayout)
        self.show()

    def loadFileAction(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, "Load file", "./json_files")
        self.fileNameField.setText(filename)

    def saveFileAction(self):
        filename = QtGui.QFileDialog.getOpenFileName(self,  "save file", "./json_files")
        self.saveFileNameField.setText(filename)

        
    def loadStoriesAction(self):
        radioButtonIndex = self.loadRadioBox.checkedId()
#        print radioButtonIndex
        if radioButtonIndex == 0 : # "From file"
#                print "m"+self.fileNameField.text()+"m"
            if self.fileNameField.text() == "":
                self.loadInfoText.setText("No filename specified")
            else:
                try:
                    story_dict=load_objects(self.fileNameField.text())
                    self.stories = load_stories_from_dict(story_dict)
                    self.loadInfoText.setText("Stories loaded from file:" + self.fileNameField.text())
                    self.storiesLoaded.emit()
                except ValueError:
                    self.loadInfoText.setText("No JSON object could be decoded")
        elif radioButtonIndex == 1: # From stub":
            self.stories = populate_stories_stub()
            self.loadInfoText.setText("Stories loaded from stub")
            self.storiesLoaded.emit()

        elif radioButtonIndex == 2 : # "From Jira":
            login = self.loginField.text()
            password= self.passwordField.text()
            server=str(self.jiraServerField.text())
            story_filter = str(self.storyFilterField.text())
            if (login=="" or password=="" or server=="" or story_filter==""):
                self.loadInfoText.setText("To load stories form Jira, please provide login, password, server and filter")
            else:
                self.stories = populate_stories_jira(login, password,server,story_filter)
                self.loadInfoText.setText("Stories loaded from jira")
                self.storiesLoaded.emit()
         
        elif radioButtonIndex == 3: # "Jira + File resolved":
            self.loadInfoText.setText("under construction")

	else:
            self.loadInfoText.setText("nothing selected")

#        parent.stories = self.stories
#        if len(self.stories)>0:
#            for nn in self.stories:
#                for mm in ["xCoord","yCoord","progress","state", "dependencies", "key"]:
#                    print mm,": ", getattr(self.stories[nn],mm," ")

    def saveStoriesAction(self):
        self.updateStories.emit()
        self.output_stories()

    def output_stories(self):
        if len(self.stories) == 0:
            self.loadInfoText.setText("No stories loaded")
        else:
            filename = self.saveFileNameField.text()
#            print "file name: ",filename
            if filename == "": 
                self.loadInfoText.setText("No filename specified")
            else:
                file_output(self.stories, filename)
                self.loadInfoText.setText("Saved to file: "+filename)

#    def connectStoriesLoaded(self):
#       parent.stories = self.stories
#       self.storiesLoaded.emit()
#       parent.circleSelected.emit()
        
class TabbWidget(QtGui.QMainWindow):

    def __init__(self):
        super(TabbWidget, self).__init__()
        self.stories ={} 
        self.initui()

    def initui(self):
        self.configWindow = ConfigWidget()
#        self.addTab(self.configWindow, "Configuration")
        self.setCentralWidget(self.configWindow)
        self.configWindow.storiesLoaded.connect(self.loadImageTab)
        self.setWindowTitle("jiraCircles")
#        self.setGeometry(300,300,window_width,window_height)
        self.show()

        
    def loadImageTab(self):
        self.stories = self.configWindow.stories
        self.newWindow = MainWindow(self.stories)
        self.configWindow.updateStories.connect(self.update_stories)
#        self.addTab(self.newWindow,"Main GUI")
#        self.show()
        
    def update_stories(self):
        self.configWindow.stories = self.newWindow.stories


if __name__ == "__main__":   
    parser=argparse.ArgumentParser(description="Start the jiracircles program with a pre-config if any arguments are specified")
    parser.add_argument("--stub", help=" start with stub stories loaded")
    parser.add_argument("--file", help="start program with stories loaded from this JSON file")

    args = parser.parse_args()

    
    app = QtGui.QApplication(sys.argv)
    tabbed = TabbWidget()

    if args.stub:
#        tabbed.configWindow.loadRadioBox.
        tabbed.configWindow.stories = populate_stories_stub()
        tabbed.configWindow.loadInfoText.setText("Stories loaded from stub")
        tabbed.configWindow.storiesLoaded.emit()
    elif args.file:
        try:
            tabbed.configWindow.fileNameField.setText(args.file)
            stories_dict=load_objects(args.file)
            tabbed.configWindow.stories = load_stories_from_dict(stories_dict)
            tabbed.configWindow.loadInfoText.setText("Stories loaded from file:" + args.file)
            tabbed.configWindow.storiesLoaded.emit()
        except ValueError:
            tabbed.configWindow.loadInfoText.setText("No JSON object could be decoded")


    app.exec_()
    sys.exit(app.quit())

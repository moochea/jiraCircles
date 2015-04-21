#!/usr/bin/env python

import math,sys
#import inspect
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PyQt4 import QtGui, QtOpenGL, QtCore
import Image, ImageOps
from config import *
from shapes import *
#import gizehlib
from stories import *

dep_links = {
            "curve" : draw_dependency_curve,
            "line" : draw_dependency_line,
            "fancy" : draw_dependency_fancy_lines,
            }

class OpenGlApplication(QtOpenGL.QGLWidget):
    """This is a class docstring"""

    circleSelected = QtCore.pyqtSignal()

    def __init__(self, stories):
        super(OpenGlApplication, self).__init__()
        self.width = WINDOW_WIDTH
        self.height=WINDOW_HEIGHT
        self.setMinimumSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.stories = stories
        self.circleSelected.connect(self.repaint)
        self.focus= None

    def initializeGL(self):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
        glClearColor(1.0,1.0,1.0,1.0)
        glClearDepth(1.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, self.width, 0.0, self.height, -1.0, 1.0)
#        glClear(GL_COLOR_BUFFER_BIT )


    def resizeGL(self, width, height):
        glViewport(0,0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, width, 0.0, height,-1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
#        glClearColor(1, 1, 1, 1)
        self.width=width
        self.height=height

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glEnable(GL_LINE_SMOOTH)
        self.define_output_area()
#        self.resizeGL(window_width, window_height)
        for x in self.stories:
            self.draw_circle(self.stories[x])
        glDisable(GL_LINE_SMOOTH)
        glFlush()
#        glutMakeCurrent()
#        self.swapBuffers()

    def define_output_area(self):
        glLineWidth(1)
        glColor3fv(GREY)
        glBegin(GL_LINE_LOOP)
        glVertex2f(1,1)
        glVertex2f(self.width*2/3, 1)
        glVertex2f(self.width*2/3, self.height)
        glVertex2f(1, self.height-1)
        glEnd()

    def output_to_file(self, filename):
        newstuff = glReadPixels(0, 0, (self.width*2/3), self.height, GL_RGB, GL_UNSIGNED_BYTE)
#        print len(newstuff)
        #Insert something to draw to bitmap
        newimage = Image.frombuffer("RGB", ((self.width*2/3), self.height), newstuff, "raw", "RGB", 0, 0)
        newimageFlipped = ImageOps.flip(newimage)
        newimageFlipped.save(filename)

    def mousePressEvent(self,mouse_event):
        x,y =  mouse_event.x(), mouse_event.y()
#        parent.buttonClicked.emit()
        change = False
        old_focus=self.focus
        if mouse_event.MouseButtonPress:
#            print "button pressed", x,y
            for xx in self.stories:
                xpos = self.stories[xx].xCoord
                ypos = self.height - self.stories[xx].yCoord
#                radius = math.sqrt(self.stories[xx].storyPoints)*SCALE
                radius = calculate_radius(self.stories[xx].storyPoints)

#            print xx, xpos, ypos, radius
                if math.sqrt((x - xpos)**2 + (y-ypos)**2)<radius:
                    self.focus = xx
                    if old_focus != self.focus:
#                        print old_focus, self.focus
                        self.circleSelected.emit()
                    change = True
#                print focus
#        print "released", x,y
        if change == False:
            self.focus= None
            if old_focus != self.focus:
#                print old_focus, self.focus
                self.circleSelected.emit()

    def mouseMoveEvent(self,mouse_move):
        x,y = mouse_move.x(), mouse_move.y()
#        print "mouseMotion called:", x,y
        if self.focus != None:
#            print focus
            story = self.stories[self.focus]
            if (x-story.xCoord> 3) or (x-story.xCoord<-3) or (y-story.yCoord>3) or (y-story.yCoord<-3):
                self.stories[self.focus].move_to(x,self.height-y)
                self.repaint()
#            glutPostRedisplay()

    def text_wrap(self, xCoord, yCoord, text, font, font_size, wrap_size=0):
        new_line = text.split(" ")

# This part pre-calculates how many lines will be wrapped to so that the Y-coordinate displacement is readied in advance
        number_lines = 0
        comparison_line=""
        for x in new_line:
            if len(comparison_line+x+" ") >= wrap_size:
                number_lines+=1
                comparison_line = ""
            comparison_line+=x+" "
        xprint = xCoord
        yprint = yCoord - (font_size+INTER_PAD)*(number_lines)
#        print text, len(text),wrap_size, number_lines, xprint, yprint
        text_to_be_rendered = ""
        for x in new_line:
            if len(text_to_be_rendered+x+" ")>=wrap_size and wrap_size>0:
                self.renderText(xprint, yprint, text_to_be_rendered.rstrip(), QtGui.QFont(font,font_size ))
                yprint = yprint + font_size + INTER_PAD
#                print new_line, number_lines, xprint, yprint
                text_to_be_rendered = ""
            text_to_be_rendered = text_to_be_rendered + x.rstrip() + " "
        self.renderText(xprint, yprint, text_to_be_rendered.rstrip(), QtGui.QFont(font, font_size))

    def draw_circle(self, story):
        state_colour = colour[story.state]

#        radius = SCALE*math.sqrt(story.storyPoints)
        radius = calculate_radius(story.storyPoints)


        # draw the solid bits representing progress
        glColor3fv(state_colour)
        angle = story.progress*twopi/100
        if angle > 0:
#            glColor3fv(state_colour)
            glBegin(GL_TRIANGLE_FAN)
            if story.progress != 100:
                glVertex2f(story.xCoord ,story.yCoord)
            generate_circle_vertices(radius, angle, story.xCoord, story.yCoord, delta=radius/4)
            glVertex2f(radius*math.sin(angle)+story.xCoord ,radius*math.cos(angle) + story.yCoord)
            glEnd()


        # draw the outline
        glColor3fv(BLACK)
        glLineWidth(3.0)
        glBegin(GL_LINE_LOOP)
        generate_circle_vertices(radius, twopi, story.xCoord, story.yCoord, delta=radius/4)
#        generate_circle_vertices(radius, twopi*0.75, story.xCoord, story.yCoord)
        glEnd()

        # Draw lines linking dependencies
        if len(story.dependencies) > 0 :
            for dep_key in story.dependencies:
                dep_links[DEPENDENCY_LINK](story, self.stories[dep_key])
#                draw_dependency_line(story, self.stories[dep_key])

        # Text showing the story Key
        glColor3fv(FONT_COLOUR_KEY)
        displayText = str(story.key)
        self.text_wrap(story.xCoord, self.height-story.yCoord-radius, displayText, FONT_TYPE, FONT_SIZE_KEY, wrap_size=FONT_WRAP_TITLE)
#        self.renderText(story.xCoord, self.height-story.yCoord-radius, displayText, QtGui.QFont("Times", FONT_SIZE_SUMMARY))


# Set place for Title
        glColor3fv(FONT_COLOUR_TITLE)
        self.text_wrap(story.xCoord, self.height-story.yCoord-radius-FONT_SIZE_KEY-FONT_PAD, story.title, FONT_TYPE, FONT_SIZE_TITLE, FONT_WRAP_TITLE)
#        self.renderText(story.xCoord, self.height-story.yCoord-radius-FONT_SIZE_SUMMARY, story.title, QtGui.QFont("Times", FONT_SIZE_TITLE))

        # if the current story has been selected, indicate so by printing the summary too
        if self.focus == story.key:
            glColor3fv(FONT_COLOUR_SUMMARY)
            self.text_wrap(story.xCoord+radius, self.height-story.yCoord+radius, story.summary, FONT_TYPE, FONT_SIZE_SUMMARY, FONT_WRAP_SUMMARY)
#            self.renderText(story.xCoord, (self.height-story.yCoord+20), story.summary, QtGui.QFont("Times", FONT_SIZE_SUMMARY))

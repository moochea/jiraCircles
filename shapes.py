#!/usr/bin/env python

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PyQt4 import QtGui, QtOpenGL, QtCore
import math,sys, inspect
from config import *

def calculate_radius(storyPoints):
    return SCALE*(storyPoints**2)**(1/3.0)
#    return SCALE*math.sqrt(storyPoints)

def generate_circle_vertices(radius,angle, x0, y0, delta, angle_start=0):
#    print "angle: ",angle/(2*math.pi)
    #print "circle centre: \t", x0,y0
#    delta = int(300/radius)
    for i in range(int(angle_start*delta), int(angle*delta)):
        x_pos = radius * math.sin(i/delta) + x0
        y_pos = radius * math.cos(i/delta) + y0
#        print "circle vertices: ", (x_pos, y_pos)
        glVertex2f(x_pos, y_pos)


def arrow(size, x0, y0, vx, vy):
    glColor3fv(BLACK)
    coordinates = [ (0, 0), (-size/2, -size/2), (0, size),(size/2, -size/2)]
    glBegin(GL_TRIANGLE_FAN)
#    print vx,vy
    for (x1, y1) in coordinates:
        x = x0 - size*vx + x1*vy + y1*vx
        y = y0 - size*vy - x1*vx + y1*vy
#        x = x0 + x1*vx + y1*vy
#        y = y0 + x1*vy + y1*vx
#        print (x,y)
        glVertex2f(x,y)
    glEnd()

def find_angle(vector):
    """
    Given a vector, return the correct angle from default vector 0,1) in radians
    """
#    starting_point_vector = ((story_point[0]- circle_centre[0]), (story_point[1]- circle_centre[1]))
    point_tan = vector[0]/vector[1]
    angle_raw = math.sqrt(math.atan(point_tan)**2)
    if vector[0]>0:
        if vector[1]>0:
           angle = angle_raw
        else:
           angle =  math.pi-angle_raw
    else:
        if vector[1]>0:
           angle = -angle_raw 
        else:
           angle =  math.pi+angle_raw

    return angle

def find_normal_downward(vector):
    x_ver = vector[0]
    y_ver = vector[1]
    if x_ver ==0:
#            normal = (-y_ver, 0)
        normal = (y_ver, 0)
    elif y_ver == 0:
        normal = (0, -x_ver)
    elif x_ver >0:
        if y_ver < 0:
            normal = (y_ver, -x_ver)
        else:
            normal = (y_ver, -x_ver)
    else:
        if y_ver < 0:
            normal = (-y_ver, x_ver)
        else:
            normal = (-y_ver, x_ver)
    return normal

def draw_dependency_line(story, dependency):
#    radius = SCALE*math.sqrt(story.storyPoints)
    radius = calculate_radius(story.storyPoints)
    # calculate the unit direction vertex
    length = math.sqrt((dependency.xCoord - story.xCoord)**2 + (dependency.yCoord - story.yCoord)**2 )
    x_ver = (dependency.xCoord - story.xCoord) / length
    y_ver = (dependency.yCoord - story.yCoord) /length
#                print x_ver, y_ver, length

#    radius_dep = math.sqrt(dependency.storyPoints)*SCALE
    radius_dep = calculate_radius(dependency.storyPoints)

    glLineWidth(2.0)
#                for x in story.dependencies:
    glColor3fv(BLACK)
    glBegin(GL_LINES)
    glVertex2f(story.xCoord + x_ver*radius, story.yCoord + y_ver*radius)
    glVertex2f(dependency.xCoord-x_ver*radius_dep, dependency.yCoord-y_ver*radius_dep)
    glEnd()

    arrow(20,dependency.xCoord-x_ver*radius_dep, dependency.yCoord-y_ver*radius_dep, x_ver, y_ver)

def draw_dependency_fancy_lines(story, dependency):
#    radius = SCALE*math.sqrt(story.storyPoints)
    radius =calculate_radius(story.storyPoints)
    # calculate the unit direction vertex
    length = math.sqrt((dependency.xCoord - story.xCoord)**2 + (dependency.yCoord - story.yCoord)**2 )
    x_ver = (dependency.xCoord - story.xCoord) / length
    y_ver = (dependency.yCoord - story.yCoord) /length
    normal = (-y_ver, x_ver)
#    print normal
#                print x_ver, y_ver, length

#    radius_dep = math.sqrt(dependency.storyPoints)*SCALE
    radius_dep = calculate_radius(dependency.storyPoints)

    glLineWidth(5.0)
    pad=2.5
#                for x in story.dependencies:
    glBegin(GL_TRIANGLE_STRIP)

    glColor3fv(WHITE)
    glVertex2f(story.xCoord + x_ver*radius-pad*normal[0], story.yCoord + y_ver*radius-pad*normal[1])
    glVertex2f(dependency.xCoord-x_ver*radius_dep-pad*normal[0], dependency.yCoord-y_ver*radius_dep-pad*normal[1])

    glColor3fv(BLACK)
    glVertex2f(story.xCoord + x_ver*radius, story.yCoord + y_ver*radius)
    glVertex2f(dependency.xCoord-x_ver*radius_dep, dependency.yCoord-y_ver*radius_dep)

    glColor3fv(WHITE)
    glVertex2f(story.xCoord + x_ver*radius+pad*normal[0], story.yCoord + y_ver*radius+pad*normal[1])
    glVertex2f(dependency.xCoord-x_ver*radius_dep+pad*normal[0], dependency.yCoord-y_ver*radius_dep+pad*normal[1])

    glEnd()

    arrow(20,dependency.xCoord-x_ver*radius_dep, dependency.yCoord-y_ver*radius_dep, x_ver, y_ver)

def calculate_dependency_curve_attributes(story, dependency):
    # angle = pi/2, therefore calculate radius
    # start and end point known!
    # generate_circle_vertices(radius, 90, x0, y0)
#    radius_story = SCALE*math.sqrt(story.storyPoints)
    radius_story = calculate_radius(story.storyPoints)
    # calculate the unit direction vertex
    length = math.sqrt((dependency.xCoord - story.xCoord)**2 + (dependency.yCoord - story.yCoord)**2 )
    x_ver = (dependency.xCoord - story.xCoord) / length
    y_ver = (dependency.yCoord - story.yCoord) /length
#                print x_ver, y_ver, length

#    radius_dep = math.sqrt(dependency.storyPoints)*SCALE
    radius_dep = calculate_radius(dependency.storyPoints)
    normal = find_normal_downward((x_ver, y_ver))

            
    story_point = (story.xCoord + x_ver*radius_story, story.yCoord + y_ver*radius_story)
    dependency_point = (dependency.xCoord - x_ver*radius_dep, dependency.yCoord - y_ver*radius_dep)

    halfway = ((story_point[0] + dependency_point[0])/2, (story_point[1] + dependency_point[1])/2)

    circle_centre = (halfway[0] + normal[0]*length/2, halfway[1]+normal[1]*length/2)

    starting_point_vector = ((story_point[0]- circle_centre[0]), (story_point[1]- circle_centre[1]))
    starting_angle_raw = find_angle(starting_point_vector)

    ending_angle_vector = ((dependency_point[0]-circle_centre[0]), (dependency_point[1] - circle_centre[1]))
    ending_angle_raw=find_angle(ending_angle_vector)
    ending_vec_length = math.sqrt(ending_angle_vector[0]**2 + ending_angle_vector[1]**2)
#    ending_normal = find_normal_downward(ending_angle_vector)
    ending_normal = (ending_angle_vector[1]/ending_vec_length, -ending_angle_vector[0]/ending_vec_length)

    R=math.sqrt((story_point[0] - circle_centre[0])**2 + (story_point[1] - circle_centre[1])**2)

    if ending_angle_raw <0 and starting_angle_raw > math.pi:
        ending_angle_raw += 2*math.pi

    if starting_angle_raw<0 and ending_angle_raw > math.pi:
        starting_angle_raw+=2*math.pi

    if ending_angle_raw < starting_angle_raw:
        temp_angle = starting_angle_raw
        starting_angle_raw = ending_angle_raw
        ending_angle_raw = temp_angle
        ending_normal = (-ending_normal[0], -ending_normal[1])
#        print "flip"
#    else:
#        print "no flip"

    starting_angle = starting_angle_raw 
    ending_angle = ending_angle_raw 


#    print R, 180*starting_angle/math.pi, 180*ending_angle/math.pi, circle_centre
    return R, starting_angle, ending_angle, circle_centre, dependency_point, ending_normal

def draw_dependency_curve(story, dependency):
    R, starting_angle, ending_angle, circle_centre, dependency_point, ending_normal = calculate_dependency_curve_attributes(story, dependency)

    glLineWidth(5.0)

#    glColor3fv(WHITE)
#    glBegin(GL_LINES)
#    generate_circle_vertices(R,ending_angle, circle_centre[0], circle_centre[1]-2, delta = R*SCALE, angle_start=starting_angle)
#    glEnd()
#    glBegin(GL_LINES)
    glColor3fv(BLACK)
    glBegin(GL_LINES)

    generate_circle_vertices(R,ending_angle, circle_centre[0], circle_centre[1], delta = R*SCALE, angle_start=starting_angle)
    glEnd()
#    glColor3fv(WHITE)
#    glBegin(GL_LINES)
#    generate_circle_vertices(R,ending_angle, circle_centre[0], circle_centre[1]+2, delta = R*SCALE, angle_start=starting_angle)
#    glEnd()

    arrow(15, dependency_point[0],dependency_point[1], ending_normal[0], ending_normal[1])

# This arrow jsut marks the circle centre from which the curve is drawn
#    arrow(10,circle_centre[0], circle_centre[1], 1,1)


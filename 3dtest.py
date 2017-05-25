import random
import pygame
import sys
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

vertices = (
    (0, -1.5, 0), #0
    (-1, 0, 0),#1
    (1, 0, 0), #2
    (0, 0, -1),#3
    (0, 0, 1), #4
    (0, 1.5, 0),  #5
    )

edges = (
    (0,1),
    (0,2),
    (0,3),
    (0,4),
    (1,3),
    (1,4),
    (2,3),
    (2,4),
    (5,1),
    (5,2),
    (5,3),
    (5,4),
    )

surfaces = (
    (0,1,3),
    (0,1,4),
    (0,2,3),
    (0,2,4),
    (5,1,3),
    (5,1,4),
    (5,2,3),
    (5,2,4),
)


def set_vertices(max_distance, min_distance = -20):
    x_value_change = random.randrange(-10,10)
    y_value_change = random.randrange(-10,10)
    z_value_change = random.randrange(-1*max_distance, min_distance)

    new_vertices = []

    for vert in vertices:
        new_vert = []

        new_x = vert[0] + x_value_change
        new_y = vert[1] + y_value_change
        new_z = vert[2] + z_value_change

        new_vert.append(new_x)
        new_vert.append(new_y)
        new_vert.append(new_z)

        new_vertices.append(new_vert)

    return new_vertices

def Crystal(vertices):
    glBegin(GL_QUADS)
    for surface in surfaces:
        for vertex in surface:
            glColor3fv((1,1,1))
            glVertex3fv(vertices[vertex])
    glEnd()


    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()
    
def main():
    pygame.init()
    display = (800,600)
    screen = pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    max_distance = 100
    
    gluPerspective(45, (display[0]/display[1]), 0.1, max_distance)

    glTranslatef(random.randrange(-5,5),random.randrange(-2,2), -40)

    x_move = 0
    y_move = 0

    crystal_dict = {}

    for x in range(3):
        crystal_dict[x] = set_vertices(max_distance)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                glClear(GL_COLOR_BUFFER_BIT)
                data = glReadPixels(pos[0],pos[1],1,1,GL_RGB,GL_FLOAT)
                print (data[0][0])
                
        
        x = glGetDoublev(GL_MODELVIEW_MATRIX)

        camera_x = x[3][0]
        camera_y = x[3][1]
        camera_z = x[3][2]
        
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glTranslatef(x_move,y_move,.25)
        #glRotatef(1,0,1,0)
        for each_crystal in crystal_dict:
            Crystal(crystal_dict[each_crystal])
        
        for each_crystal in crystal_dict:
            if camera_z <= crystal_dict[each_crystal][0][2]:
                #delete_list.append(each_crystal)
                new_max = int(-1*(camera_z-max_distance))

                crystal_dict[each_crystal] = set_vertices(new_max,int(camera_z))
        pygame.display.flip()
        pygame.time.wait(10)
        
main()
pygame.quit()
quit()

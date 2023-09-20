import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math

pygame.init()
display = (800, 600)
screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

glEnable(GL_DEPTH_TEST)

sphere = gluNewQuadric()  # Create new sphere

glMatrixMode(GL_PROJECTION)
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

glMatrixMode(GL_MODELVIEW)
gluLookAt(0, -8, 0, 0, 0, 0, 0, 0, 1)
viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
glLoadIdentity()

def main(num_spheres):
    global viewMatrix
    # Initial sphere positions and velocities
    spheres = []
    for _ in range(num_spheres):
        sphere_position = [random.uniform(-2, 2), random.uniform(-2, 2), random.uniform(2, 4)]
        sphere_velocity = [random.uniform(-0.05, 0.05), 0, random.uniform(-0.05, 0.05)]
        spheres.append((sphere_position, sphere_velocity))

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    run = False

        keypress = pygame.key.get_pressed()

        # Calculate the time elapsed since the last frame (for smooth animation)
        time_passed = pygame.time.get_ticks() / 1000.0

       # Inside the main loop's sphere update section
        for i in range(num_spheres):
            sphere_position, sphere_velocity = spheres[i]

            # Calculate gravity-based movement
            

            # Calculate new y-coordinate based on sine function
            current_x = sphere_position[0]
            floor_height = math.sin(current_x)-1
            desired_y = floor_height  # Adjust this value as needed
            if desired_y < -2.0:
                desired_y = -2.0
            y_diff = desired_y - sphere_position[2]
            sphere_velocity[2] += y_diff * 0.01  # Adjust this value for desired rolling effect

            # Calculate new x-coordinate based on slope of sine function
            slope = math.cos(current_x) * 1.5  # Derivative of the sine function
            desired_x = current_x - slope * 0.01  # Adjust this value for desired rolling effect
            x_diff = desired_x - sphere_position[0]
            sphere_velocity[0] += x_diff * 0.01  # Adjust this value for desired rolling effect
            if sphere_position[2]<floor_height:
                sphere_position[2]=floor_height
            if sphere_position[2]<=floor_height+0.01:
                sphere_velocity[0]*=0.99
            sphere_position[2] += sphere_velocity[2] * time_passed
            sphere_position[0] += sphere_velocity[0] * time_passed
            sphere_position[1] += sphere_velocity[1] * time_passed
            if sphere_position[2]<=floor_height:
                sphere_position[2]=floor_height
            else:
                sphere_velocity[2] -= 0.01 * time_passed  # Gravity constant
            # Reflect spheres off the walls
            for j in range(3):
                if abs(sphere_position[j]) > 3.8:
                    sphere_velocity[j] *= -0.7


        # Init model view matrix
        glLoadIdentity()

        # Init the view matrix
        glPushMatrix()
        glLoadIdentity()

        # Apply movement
        if keypress[pygame.K_w]:
            glTranslatef(0, 0, 0.1)
        if keypress[pygame.K_s]:
            glTranslatef(0, 0, -0.1)
        if keypress[pygame.K_d]:
            glTranslatef(-0.1, 0, 0)
        if keypress[pygame.K_a]:
            glTranslatef(0.1, 0, 0)

        # Multiply the current matrix by the view matrix and store the final view matrix
        glMultMatrixf(viewMatrix)
        viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

        # Apply view matrix
        glPopMatrix()
        glMultMatrixf(viewMatrix)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear the screen

        for i in range(num_spheres):
            sphere_position, _ = spheres[i]

            glPushMatrix()

            # Apply sphere position
            glTranslatef(sphere_position[0], sphere_position[1], sphere_position[2])

            glColor4f(1, 0, 0, 0.5)  # Put color
            gluSphere(sphere, 0.1, 32, 16)  # Draw sphere

            glPopMatrix()

        pygame.display.flip()  # Update the screen
        pygame.time.wait(10)

    pygame.quit()
if __name__=='__main__':
    main(1000)

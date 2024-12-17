# Import neccesary libraries
import tkinter as tk
from createBodyWindow import open_secondary_window
import math
import ast

# Define window and title
window = tk.Tk()
window.title("3D Space")

# Define the screen through the Canvas object
screen = tk.Canvas(window, width=800, height=360, bg="white")
screen.grid(row=0, column=0, sticky="nsew")

shape_map = {"Cube": [[[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],[-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]], [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]],
             "Pyramid": [[[1,1,-1],[-1,1,-1],[1,1,1],[-1,1,1],[0,0,0]],[(0,1),(0,2),(1,3),(2,3),(0,4),(1,4),(2,4),(3,4)]]}

class Body:
    def __init__(self, vertices, edges, position=[0,0,0], angular_velocity=[0,0,0], translational_velocity=[0,0,0], angular_acceleration=[0,0,0], translational_acceleration=[0,0,0], mass=1):
        self.vertices = vertices
        self.edges = edges
        self.position = position
        self.angular_velocity = angular_velocity
        self.translational_velocity = translational_velocity
        self.angular_acceleration = angular_acceleration
        self.translational_acceleration = translational_acceleration
        self.mass = mass
        if angular_velocity!=[0,0,0] or translational_acceleration!=[0,0,0] or angular_acceleration!=[0,0,0] or translational_velocity!=[0,0,0]:
            self.is_moving = True
        else:
            self.is_moving = False
    def draw(self):
        for edge in self.edges:
            vertex1 = self.vertices[edge[0]]
            vertex2 = self.vertices[edge[1]]
            x1, y1, draw1 = self.projectVertex(vertex1[0]+self.position[0],vertex1[1]+self.position[1],vertex1[2]+self.position[2], camera)
            x2, y2, draw2 = self.projectVertex(vertex2[0]+self.position[0],vertex2[1]+self.position[1],vertex2[2]+self.position[2], camera)
            if draw1 and draw2:
                screen.create_line(x1, y1, x2, y2, fill="black", width=0.5)
    def updateRotation(self):
        if self.is_moving:
            self.angular_velocity = [self.angular_velocity[0]+self.angular_acceleration[0],self.angular_velocity[1]+self.angular_acceleration[1],self.angular_velocity[2]+self.angular_acceleration[2]]
            self.vertices = [self.rotateVertex(vertex[0],vertex[1],vertex[2],self.angular_velocity[0],self.angular_velocity[1],self.angular_velocity[2]) for vertex in self.vertices]
    def updatePosition(self):
        if self.is_moving:
            self.translational_velocity = [self.translational_velocity[0]+self.translational_acceleration[0],self.translational_velocity[1]+self.translational_acceleration[1],self.translational_velocity[2]+self.translational_acceleration[2]]
            self.position = [self.position[0]+self.translational_velocity[0],self.position[1]+self.translational_velocity[1],self.position[2]+self.translational_velocity[2]]
    @staticmethod
    def rotateVertex(x, y, z, angle_x, angle_y, angle_z):
        # z axis
        cosz, sinz = math.cos(angle_z), math.sin(angle_z)
        x_rot = x * cosz - y * sinz
        y_rot = y * cosz + x * sinz

        # y axis
        cosy, siny = math.cos(angle_y), math.sin(angle_y)
        x_rot2 = x_rot * cosy - z * siny
        z_rot = z * cosy + x_rot * siny

        # x axis
        cosx, sinx = math.cos(angle_x), math.sin(angle_x)
        y_rot2 = y_rot * cosx - z_rot * sinx
        z_rot = z_rot * cosx + y_rot * sinx

        # 8 decimals of precision
        return (round(x_rot2, 8), round(y_rot2, 8), round(z_rot, 8))
    @staticmethod
    def projectVertex(x,y,z,camera):
        x_relative = x-camera.position[0]
        y_relative = y-camera.position[1]
        z_relative = z-camera.position[2]
        
        x_relative, y_relative, z_relative = Body.rotateVertex(x_relative, y_relative, z_relative, -camera.pitch, -camera.yaw, -camera.roll)
        if z_relative<=0:
            return 0, 0, False

        x_projected = camera.scale*(x_relative*camera.focal_length)/(z_relative)
        y_projected = camera.scale*(y_relative*camera.focal_length)/(z_relative)
        
        return x_projected+400, y_projected+180, True
    def applyForce(self, fx, fy, fz, coords, time):
        self.translational_velocity[0] += time*fx/self.mass
        self.translational_velocity[1] += time*fy/self.mass
        self.translational_velocity[2] += time*fz/self.mass
class Camera:
    def __init__(self, position=[0,0,0], focal_length=5, scale=100, pitch=0, yaw=0, roll=0):
        self.position = position
        self.focal_length = focal_length
        self.scale = scale # zoom? (?)
        self.pitch = pitch # x-axis rotation (up/down)
        self.yaw = yaw # y-axis rotation (left/right)
        self.roll = roll # z-axis rotation (yeah that's hard to conceptualize huh)
    def move(self, dx, dy, dz):
        self.position[0] += dz*-math.sin(self.yaw) + dx*math.cos(self.yaw)
        self.position[1] += dy
        self.position[2] += dz*math.cos(self.yaw) + dx*math.sin(self.yaw)

    def rotate(self, d_pitch, d_yaw, d_roll):
        self.pitch += d_pitch
        self.yaw += d_yaw
        self.roll += d_roll

camera = Camera()
bodies = []

def updateScreen():
    screen.delete("all")
    for body in bodies:
        body.updatePosition()
        body.updateRotation()
        body.draw()
    window.after(16, updateScreen) # Slightly above 60 FPS

# Calls the function a 1st time to initialize the loop
updateScreen()

def on_key_press(event):
    global bodies, sensitivity_x, sensitivity_y
    if event.keysym == "Up":
        camera.move(0, 0, 0.1)  # Move camera forward
    elif event.keysym == "Down":
        camera.move(0, 0, -0.1)  # Move camera backward
    elif event.keysym == "Left":
        camera.move(-0.1, 0, 0)  # Move camera left
    elif event.keysym == "Right":
        camera.move(0.1, 0, 0)  # Move camera right
    elif event.keysym == "s":
        camera.move(0,0.1,0) # Move camera downward
    elif event.keysym == "w":
        camera.move(0,-0.1,0) # Move camera upward
    elif event.keysym=="z":
        camera.rotate(0.05,0,0)
    elif event.keysym=="x":
        camera.rotate(-0.05,0,0)
    elif event.keysym=="c":
        camera.rotate(0,0.05,0)
    elif event.keysym=="v":
        camera.rotate(0,-0.05,0)
    elif event.keysym=="b":
        camera.rotate(0,0,0.05)
    elif event.keysym=="m":
        camera.rotate(0,0,-0.05)
    elif event.keysym=="plus":
        camera.scale*=1.3
        sensitivity_x/=1.3
        sensitivity_y/=1.3
    elif event.keysym=="minus":
        camera.scale/=1.3
        sensitivity_x*=1.3
        sensitivity_y*=1.3
    elif event.keysym == "n":
        values = open_secondary_window(window)
        if "Vertices" in values.keys():
            vertices = ast.literal_eval("["+values["Vertices"]+"]")
            edges = ast.literal_eval("["+values["Edges"]+"]")
            if vertices==[] or edges==[]:
                print("No body created.")
                return
        else:
            vertices, edges = shape_map[values["Shape"]]
        new_body = Body(vertices=vertices, edges=edges, position=values["Position"], angular_velocity=values["Angular Velocity"], angular_acceleration=values["Angular Acceleration"], translational_acceleration=values["Translational Acceleration"], translational_velocity=values["Translational Velocity"])
        bodies.append(new_body)
    elif event.keysym == "r":
        camera.position = [0,0,0] # Reset camera's position
        camera.pitch, camera.yaw, camera.roll = 0,0,0 # Reset camera's rotations
    elif event.keysym == "p":
        # Delete the lastly-added body
        try:
            bodies.pop()
        except IndexError:
            print("No bodies to delete.")

# Bind the key events
window.bind('<Key>', on_key_press)

def on_mouse_release(event):
    global tracking_mouse
    tracking_mouse = False
def on_mouse_move(event):
    global last_x, last_y
    if not tracking_mouse:
        return
    dx = event.x - last_x
    dy = event.y - last_y
    last_x, last_y = event.x, event.y
    camera.rotate(dy * sensitivity_y, dx * sensitivity_x, 0)
def on_mouse_press(event):
    global tracking_mouse, last_x, last_y
    tracking_mouse = True
    last_x, last_y = event.x, event.y

tracking_mouse = False
last_x, last_y = 0, 0
sensitivity_x, sensitivity_y = 0.001, 0.001

# Bind the mouse events
window.bind("<ButtonRelease-1>", on_mouse_release)  # Left mouse button released
window.bind("<Motion>", on_mouse_move)  # Mouse movement
window.bind("<ButtonPress-1>", on_mouse_press)  # Left mouse button pressed

# The mainloop
window.mainloop()
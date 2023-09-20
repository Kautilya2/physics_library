import tkinter as tk
import math
import random
def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle
class FallingCirclesApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('3000x3000')
        self.canvas = tk.Canvas(self.root, height=3000, width=3000)
        self.canvas.pack()
        
    def run(self):
        objects = []
        self.canvas.update()

        for _ in range(5):
            objects.append(Circle(100, [random.randint(0, self.canvas.winfo_width() - 100), random.randint(0, self.canvas.winfo_height() - 100)], 3, 0.1, False))
        print('created')
        while any(touching(i,objects)[0] for i in objects):
            objects = []
            for _ in range(5):
                objects.append(Circle(100, [random.randint(0, self.canvas.winfo_width()), random.randint(0, self.canvas.winfo_height())], 3, 0.1, False))

        while True:
            for ci in objects:
                ci.show(self.canvas)
                ci.update(objects,self.canvas)
            self.canvas.update()
            self.canvas.delete('all')

class Circle:
    def __init__(self, radius, centre, width, gravity, static):
        self.pos = centre
        self.rad = radius
        self.w = width
        self.ag = gravity
        self.fh = 0
        self.fh2 = 0
        self.fw = 0
        self.flag = 0
        

    def update(self,objects,c):
        self.pos[1]+=self.fh
        self.pos[0]+=self.fw
        self.fh+=self.ag
        self.fh2+=self.ag*0.5
        self.fw=0
        if self.pos[1]+self.rad>c.winfo_height() and self.fh>0:
            self.pos[1]=c.winfo_height()-self.rad
            self.fh*=-0.8
            self.fw*=0.8
        mn=touching(self,objects)
        if mn[0]:
            self.fh*=math.sin(mn[1]-180)*0.9
            self.fw*=math.cos(mn[1]-180)*0.9
            self.flag=1
            # Check if another circle is directly below and in the path of least resistance
            mn = touching(self,objects)
            if mn[0] and abs(self.pos[1]) < abs(mn[2].pos[1]):
                if abs(self.pos[0]) < abs(mn[2].pos[0]):
                    self.fw -=(self.fh2)
                    self.fh2*=0.8
                else:
                    self.fw +=(self.fh2)
                    self.fh2*=0.8
       
    def show(self,c):
        c.create_circle(self.pos[0],self.pos[1],self.rad,width=self.w)


def touching(obj,objects):
    for i in objects:
        if obj != i:
            distance = math.sqrt((obj.pos[0] - i.pos[0])**2 + (obj.pos[1] - i.pos[1])**2)
            if distance < obj.rad + i.rad:
                return (True, math.atan2(i.pos[1] - obj.pos[1], i.pos[0] - obj.pos[0]),i)
    return (False, 0)

if __name__ == "__main__":
    app = FallingCirclesApp()
    app.run()


import time, random
import math
from collections import deque

start = time.time()

class RealTimePlot:
    def __init__(self, axes, max_entries = 100):
        self.axis_x = deque(maxlen=max_entries)
        self.axis_y = deque(maxlen=max_entries)
        self.axes = axes
        self.max_entries = max_entries

        self.lineplot, = axes.plot([], [], "ro-")
        self.axes.set_autoscaley_on(True)

    def add(self, x, y):
        self.axis_x.append(x)
        self.axis_y.append(y)
        self.lineplot.set_data(self.axis_x, self.axis_y)
        self.axes.set_xlim(self.axis_x[0], self.axis_x[-1] + 1e-15)
        self.axes.relim(); self.axes.autoscale_view() # rescale the y-axis

    def animate(self, figure, callback, interval = 50):
        import matplotlib.animation as animation
        def wrapper(frame_index):
            self.add(*callback(frame_index))
            self.axes.relim(); self.axes.autoscale_view() # rescale the y-axis
            return self.lineplot
        animation.FuncAnimation(figure, wrapper, interval=interval)

class RealTimePlot3D:
    def __init__(self, axes, max_entries = 100):
        self.axis_x = deque(maxlen=max_entries)
        self.axis_y = deque(maxlen=max_entries)
        self.axis_z = deque(maxlen=max_entries)
        self.axes = axes
        self.max_entries = max_entries

        self.lineplot, = axes.plot([], [], [], "ro-")
        #import pdb; pdb.set_trace()
        #self.axes.set_autoscaley_on(True)

    def add(self, x, y, z):
        self.axis_x.append(x)
        self.axis_y.append(y)
        self.axis_z.append(z)
        self.lineplot.set_data(self.axis_x, self.axis_y)
        #self.lineplot.set_data(self.axis_x, self.axis_y, self.axis_z)
        self.axes.set_xlim(self.axis_x[0], self.axis_x[-1] + 1e-15)
        self.axes.set_ylim(self.axis_y[0], self.axis_y[-1] + 1e-15)
        self.axes.set_zlim(self.axis_z[0], self.axis_z[-1] + 1e-15)
        self.axes.relim(); self.axes.autoscale_view() # rescale the y-axis

    def animate(self, figure, callback, interval = 50):
        import matplotlib.animation as animation
        def wrapper(frame_index):
            self.add(*callback(frame_index))
            self.axes.relim(); self.axes.autoscale_view() # rescale the y-axis
            return self.lineplot
        animation.FuncAnimation(figure, wrapper, interval=interval)

class RealTimePlot3X:
    def __init__(self, axesX, axesY, axesZ, max_entries = 100):
        self.axis_t = deque(maxlen=max_entries)
        self.axis_x = deque(maxlen=max_entries)
        self.axis_y = deque(maxlen=max_entries)
        self.axis_z = deque(maxlen=max_entries)
        self.axesX = axesX
        self.axesY = axesY
        self.axesZ = axesZ
        self.max_entries = max_entries

        self.lineplotX, = axesX.plot([], [], "ro-")
        self.lineplotY, = axesY.plot([], [], "ro-")
        self.lineplotZ, = axesZ.plot([], [], "ro-")
        self.axesX.set_autoscaley_on(True)
        self.axesY.set_autoscaley_on(True)
        self.axesZ.set_autoscaley_on(True)

    def add(self, t, x, y, z):
        self.axis_t.append(t)
        self.axis_x.append(x)
        self.axis_y.append(y)
        self.axis_z.append(z)
        self.lineplotX.set_data(self.axis_t, self.axis_x)
        self.lineplotY.set_data(self.axis_t, self.axis_y)
        self.lineplotZ.set_data(self.axis_t, self.axis_z)
        self.axesX.set_xlim(self.axis_x[0], self.axis_x[-1] + 1e-15)
        self.axesX.relim(); self.axesX.autoscale_view() # rescale the y-axis

        self.axesY.set_xlim(self.axis_y[0], self.axis_y[-1] + 1e-15)
        self.axesY.relim(); self.axesY.autoscale_view() # rescale the y-axis

        self.axesZ.set_xlim(self.axis_z[0], self.axis_z[-1] + 1e-15)
        self.axesZ.relim(); self.axesZ.autoscale_view() # rescale the y-axis

    def animate(self, figure, callback, interval = 50):
        import matplotlib.animation as animation
        def wrapper(frame_index):
            self.add(*callback(frame_index))
            self.axesX.relim(); self.axesX.autoscale_view() # rescale the y-axis
            self.axesY.relim(); self.axesY.autoscale_view() # rescale the y-axis
            self.axesZ.relim(); self.axesZ.autoscale_view() # rescale the y-axis
            return self.lineplotX, self.lineplotY, self.lineplotZ
        animation.FuncAnimation(figure, wrapper, interval=interval)



def main():
    from matplotlib import pyplot as plt

    fig, axes = plt.subplots()
    display = RealtimePlot(axes)
    display.animate(fig, lambda frame_index: (time.time() - start, random.random() * 100))
    plt.show()

    fig, axes = plt.subplots()
    display = RealtimePlot(axes)
    while True:
        display.add(time.time() - start, random.random() * 100)
        plt.pause(0.001)

if __name__ == "__main__":

    main()

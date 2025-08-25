import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from math import atan2
from random import randint  # Importing randint
import time
points = []
anchor = None

def leftmost_point(points):
    min_point = points[0]
    for point in points:
        if point[0] < min_point[0]:
            min_point = point
    return min_point

def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0  # colinear
    elif val > 0:
        return 1  # clockwise
    else:
        return 2  # counterclockwise


def jarvis_march(points, show_progress=False):
    if len(points) < 3:
        return []  # Convex hull is not possible

    hull = []

    left_point = leftmost_point(points)
    p = left_point
    while True:
        hull.append(p)
        # Ensure q is not the same as p
        q = points[0] if points[0] != p else points[1]

        for r in points:
            if orientation(p, q, r) == 2:
                q = r

        if show_progress:
            yield hull + [q]

        p = q
        if p == left_point:
            break

    yield hull

def on_plot_click(event):
    if event.xdata is not None and event.ydata is not None:
        points.append((event.xdata, event.ydata))
        ax.plot(event.xdata, event.ydata, 'ro')
        canvas.draw()
def on_submit():
    start_time = time.perf_counter()
    if len(points) > 2:
        for current_hull in jarvis_march(points, True):
            scatter_plot(points, current_hull)
            canvas.draw_idle()  # Non-blocking update
            root.update()  # Process events
            time.sleep(0.5)

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"Execution Time: {execution_time} seconds")
    ax.text(1, 48, f"Time: {execution_time:.2f} sec", fontsize=9, color='blue')
    canvas.draw_idle()

def scatter_plot(coords, convex_hull=None):
    ax.clear()
    ax.set_xlim(0, 60)
    ax.set_ylim(0, 60)
    xs, ys = zip(*coords)
    ax.scatter(xs, ys)

    if convex_hull is not None:
        for i in range(1, len(convex_hull) + 1):
            if i == len(convex_hull): i = 0
            p0 = convex_hull[i - 1]
            p1 = convex_hull[i]
            ax.plot((p0[0], p1[0]), (p0[1], p1[1]), 'r')
    canvas.draw()

# Tkinter setup
root = tk.Tk()
root.title("JARVIS MARCH")

# Matplotlib figure and subplot
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)
ax.set_xlim(0, 60)
ax.set_ylim(0, 60)


# Matplotlib canvas
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
canvas.mpl_connect('button_press_event', on_plot_click)

# Submit button
submit_button = tk.Button(master=root, text="Submit", command=on_submit)
submit_button.pack(side=tk.BOTTOM)

root.mainloop()

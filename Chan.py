import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import math
from random import randint  # Importing randint
import time
# Global variables
points = []
anchor = None

def orientation(p, q, r): # another variation of jarvis just flipped the signs
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0  # colinear
    elif val > 0:
        return 1  # clockwise
    else:
        return 2  # counterclockwise


def polar_angle(p0, p1=None): # used for sort the coordinates by the angle with respect to anchor
    if p1 == None: p1 = anchor
    y_span = p0[1] - p1[1]
    x_span = p0[0] - p1[0]
    return math.atan2(y_span, x_span)


def distance(p0, p1=None): #if
    if p1 == None: p1 = anchor
    y_span = p0[1] - p1[1]
    x_span = p0[0] - p1[0]
    return y_span**2 + x_span**2


def det(p1, p2, p3): #determinant
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) \
           - (p2[1] - p1[1]) * (p3[0] - p1[0]) # > 0 is CCW


def quicksort(points):
    if len(points) <= 1: return points
    smaller, equal, larger = [], [], []
    piv_ang = polar_angle(points[randint(0, len(points) - 1)])
    for pt in points:
        pt_ang = polar_angle(pt)
        if pt_ang < piv_ang:
            smaller.append(pt)
        elif pt_ang == piv_ang:
            equal.append(pt)
        else:
            larger.append(pt)
    return quicksort(smaller) \
           + sorted(equal, key=distance) \
           + quicksort(larger)  #points which are equal to pivot are sorted through distance


def graham_scan(points):
    global anchor

    min_idx = None
    for i, (x, y) in enumerate(points):
        if min_idx == None or y < points[min_idx][1]:
            min_idx = i
        if y == points[min_idx][1] and x < points[min_idx][0]:
            min_idx = i

    anchor = points[min_idx]

    sorted_pts = quicksort(points)
    del sorted_pts[sorted_pts.index(anchor)]

    hull = [anchor, sorted_pts[0]]
    for s in sorted_pts[1:]:
        while len(hull) > 1 and det(hull[-2], hull[-1], s) <= 0: # it is not CCW
            del hull[-1]  # backtrack
        hull.append(s)
    return hull

def chans_algorithm(points, h):
    m = int(math.ceil(math.sqrt(h)))

    while True:
        subsets = [points[i:i + m] for i in range(0, len(points), m)]
        convex_hulls = [graham_scan(subset) for subset in subsets]

        point_on_hull = min(points, key=lambda p: p[0])
        hull = [point_on_hull]

        while True:
            endpoint = None
            for partial_hull in convex_hulls:
                for candidate in partial_hull:
                    if candidate == point_on_hull:
                        continue
                    if endpoint is None or orientation(point_on_hull, endpoint, candidate) == 2:
                        endpoint = candidate

            if endpoint == hull[0]:
                return hull

            hull.append(endpoint)
            point_on_hull = endpoint

        m *= 2



def on_plot_click(event):
    if event.xdata is not None and event.ydata is not None:
        points.append((event.xdata, event.ydata))
        ax.plot(event.xdata, event.ydata, 'ro')
        canvas.draw()


def on_submit():
    # Start measuring time
    start_time = time.perf_counter()
    if len(points) > 2:
        min_idx = None
        for i, (x, y) in enumerate(points):
            if min_idx is None or y < points[min_idx][1]:
                min_idx = i
            if y == points[min_idx][1] and x < points[min_idx][0]:
                min_idx = i

        anchor = points[min_idx]

        hull = chans_algorithm(points, len(points))

        # Stop measuring time
        end_time = time.perf_counter()

        # Calculate execution time
        execution_time = end_time - start_time
        print("Hull:", hull)
        print(f"Execution Time: {execution_time} seconds")

        # Display results
        scatter_plot(points, hull)

        # Display execution time on the canvas
        ax.text(1, 48, f"Time: {execution_time:.2f} sec", fontsize=9, color='blue')
        canvas.draw()


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
root.title("MR CHAN'S IS HAPPY")

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

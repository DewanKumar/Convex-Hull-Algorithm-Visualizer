import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import time
import math

points = []
anchor = None
def angle(p1, p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])

def find_distance(p1, p2, p3): # this is relative distance

    # Using the formula ax + by + c = 0
    a = p1[1] - p2[1]
    b = p2[0] - p1[0]
    c = p1[0]*p2[1] - p2[0]*p1[1]

    # Use dot product to find distance between a line and a point
    return abs(a*p3[0] + b*p3[1] + c) / math.sqrt(a*a + b*b)


def create_seg(p1, p2, points):

  above = []
  below = []

  if p2[0] == p1[0]: # lies on the same x-coord
    return above, below

  m = (p2[1] - p1[1]) / (p2[0] - p1[0]) #gradient
  c = -m * p1[0] + p1[1] #y intercept

  for coordinate in points:
        # If y > mx + c, it means it is above the line
        if coordinate[1] > m * coordinate[0] + c:
            above.append(coordinate)
        # If y < mx + c, it means it is below the line
        elif coordinate[1] < m * coordinate[0] + c:
            below.append(coordinate)

  return above, below

def quickhull2(p1, p2, segment, flag):
    #base condition
    if segment == [] or p1 is None or p2 is None:
        return []

    convex_hull = []
    farthest_distance = -1
    farthest_point = None

    for point in segment:
        distance = find_distance(p1, p2, point)
        if distance > farthest_distance:
            farthest_distance = distance
            farthest_point = point

    convex_hull.append(farthest_point)
    segment.remove(farthest_point)

    point1above, point1below = create_seg(p1, farthest_point, segment)
    point2above, point2below = create_seg(p2, farthest_point, segment)

    if flag == "above":
        convex_hull = convex_hull + quickhull2(p1, farthest_point, point1above, "above")
        convex_hull = convex_hull + quickhull2(farthest_point, p2, point2above, "above")
    else:
        convex_hull = convex_hull + quickhull2(p1, farthest_point, point1below, "below")
        convex_hull = convex_hull + quickhull2(farthest_point, p2, point2below, "below")

    return convex_hull


def quick_hull(points):
  if(len(points) < 3):
    return points
  hull =[]
  sort = sorted(points, key = lambda x:x[0]) #sort based on the x-coord
  print(sort)

  min_x = sort[0]
  max_x = sort[-1]

  hull.append(min_x)
  hull.append(max_x)

  sort.pop(0)
  sort.pop(-1)

  above, below = create_seg(min_x, max_x, sort)
  hull = hull + quickhull2(min_x, max_x, above, "above")
  hull = hull + quickhull2(min_x, max_x , below, "below")

  lowest_point = min(hull, key=lambda p: (p[1], p[0])) #sort according to y-coord and then x-coord

  # Sort the points in hull by polar angle with lowest_point
  sorted_hull = sorted(hull, key=lambda p: angle(lowest_point, p))

  return sorted_hull

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

        hull = quick_hull(points)

        # Stop measuring time
        end_time = time.perf_counter()

        # Calculate execution time
        execution_time = end_time - start_time
        print("Hull:", hull)
        print(f"Execution Time: {execution_time} seconds")

        # Display results
        scatter_plot(points, hull)

        # Display execution time on the canvas
        ax.text(1, 48, f"Time: {execution_time:.7f} sec", fontsize=9, color='blue')
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
root.title("QUICK ELIMINATION(QUICK HULL)")

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


import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from math import atan2
import math
from random import randint
import time
# Global variables
points = []
anchor = None

def polar_angle(p0, p1=None): # used for finding angles
    if p1 is None: p1 = anchor
    y_span = p0[1] - p1[1]
    x_span = p0[0] - p1[0]
    return atan2(y_span, x_span)

def distance(p0, p1=None): #used to find relative distance when equal angles
    if p1 is None: p1 = anchor
    y_span = p0[1] - p1[1]
    x_span = p0[0] - p1[0]
    return y_span**2 + x_span**2

def det(p1, p2, p3): #determinant
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

def quicksort(points): #to sort the points having O(nlogn) time complexity
    if len(points) <= 1: return points
    smaller, equal, larger = [], [], []
    piv_ang = polar_angle(points[randint(0, len(points) - 1)]) # choose a random pivot and take it angle
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


def graham_scan(points, show_progress=False): # having quick sort + loop  and hull to sore points

# loop through points find the point with lowest y coord if 2 points have same y coord
# find with lowest x coord
    sorted_pts = quicksort(points)
    del sorted_pts[sorted_pts.index(anchor)] #deleted anchor

    hull = [anchor, sorted_pts[0]] # push anchor and first point from sorted into hull
    for s in sorted_pts[1:]:
        while len(hull) > 1 and det(hull[-2], hull[-1], s) <= 0: #if doesnt make ccw
            del hull[-1]  # backtrack
        hull.append(s)
        if show_progress: #function to iterate through and show progress graph didnt use
            scatter_plot(points, hull)

    return hull


#jarvis match

def leftmost_point(points): #self explaintory
    min_point = points[0]
    for point in points:
        if point[0] < min_point[0]:
            min_point = point
    return min_point


def orientation(p, q, r): #varaiation of determinant with signs flipped
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0  # colinear
    elif val > 0:
        return 1  # clockwise
    else:
        return 2  # counterclockwise


def jarvis_march(points):
    if len(points) < 3:
        return []  # Convex hull is not possible

    hull = []

    left_point = leftmost_point(points)
    p = left_point
    while True:
        hull.append(p)
        # Ensure q is not the same as p
        q = points[0] if points[0] != p else points[1]
        #take q it doesn't matter which point then check if p q and r make ccw angle
        #if they do change q to r so at the end of loop we would have a point which
        #makes ccw with no one, so it part of hull
        #note that it make no ccw when p q r so when p is updated to q we would have our next point
        #and so on
        for r in points:
            if orientation(p, q, r) == 2:
                q = r
        p = q
        if p == left_point:
            break

    return hull


#quick hull
def angle(p1, p2): #used for sorting the final output to show correct graph
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])

def find_distance(p1, p2, p3): # this is relative distance
    #we use this to find the furthurest point from segment
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

    for point in segment: #loop to find the furthurest point from segement above or below
        distance = find_distance(p1, p2, point)
        if distance > farthest_distance:
            farthest_distance = distance
            farthest_point = point

    convex_hull.append(farthest_point) #max point part of hull
    segment.remove(farthest_point)

    point1above, point1below = create_seg(p1, farthest_point, segment) #create segments
    point2above, point2below = create_seg(p2, farthest_point, segment)
    #  .
    # /  \
    #.----.

    #recusrion
    if flag == "above": #above points  from p1 to max_point and max to p2
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
  #print(sort)

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


#brute force
def which_side_of_line(line_endpt_a, line_endpt_b, pt_subject): # same version as orientataion with different name
    return (pt_subject[0] - line_endpt_a[0]) * (line_endpt_b[1] - line_endpt_a[1]) - (
                pt_subject[1] - line_endpt_a[1]) * (line_endpt_b[0] - line_endpt_a[0])

def compute_convex_hull():
    ax.clear()
    ax.set_xlim(0, 60)
    ax.set_ylim(0, 60)

    for i in range(len(points)):
        for j in range(len(points)):
            if i == j:
                continue

            pt_i = points[i]
            pt_j = points[j]

            all_points_on_the_right = True
            for k in range(len(points)):
                if k == i or k == j:
                    continue

                if which_side_of_line(pt_i, pt_j, points[k]) < 0: #if it lies on the left of the line then that edge is not part of hull
                    all_points_on_the_right = False
                    break

            if all_points_on_the_right:
                ax.plot([pt_i[0], pt_j[0]], [pt_i[1], pt_j[1]], 'b-')  # Draw line in blue
                #instead of storing it i am just drawing the edge

    # Plot the points
    x_coords, y_coords = zip(*points)
    ax.scatter(x_coords, y_coords, color='r') #giving coords a red color
    canvas.draw()

#chan's algorithm

def graham_scan_chan(points):
    global anchor

    min_idx = None
    for i, (x, y) in enumerate(points):
        if min_idx is None or y < points[min_idx][1]:
            min_idx = i
        if y == points[min_idx][1] and x < points[min_idx][0]:
            min_idx = i

    anchor = points[min_idx]

    sorted_pts = quicksort(points)
    if anchor in sorted_pts:
        sorted_pts.remove(anchor)  # Safely remove anchor if it exists in sorted_pts

    if not sorted_pts:
        return [anchor]  # Return just the anchor if no other points are left

    hull = [anchor, sorted_pts[0]]
    for s in sorted_pts[1:]:
        while len(hull) > 1 and det(hull[-2], hull[-1], s) <= 0:  # it is not CCW
            del hull[-1]  # backtrack
        hull.append(s)
    return hull

def chans_algorithm(points, h):
    m = int(math.ceil(math.sqrt(h))) # m can be user input as well just an estimate to divide into subsection

    while True:
        subsets = [points[i:i + m] for i in range(0, len(points), m)] #divide into subsets with m size
        convex_hulls = [graham_scan_chan(subset) for subset in subsets] #find the convex hulls of that subsets

        point_on_hull = min(points, key=lambda p: p[0]) #point with min x-coord
        hull = [point_on_hull]

        while True:
            endpoint = None
            #now will only perform the jarvis march on the partial hull reducing the number of points

            for partial_hull in convex_hulls:
                for candidate in partial_hull:
                    if candidate == point_on_hull: #if candidate already on hull no need to put it again man
                        continue
                    if endpoint is None or orientation(point_on_hull, endpoint, candidate) == 2:# endpoint is that candidate who doesnt form ccw with anyone because if it did then then it wont be part of hull
                        #going from left hand side the points on hull only perform cw angle with all the other points
                        endpoint = candidate

            if endpoint == hull[0]: #wrapped
                return hull

            hull.append(endpoint)
            point_on_hull = endpoint

        m *= 2 #if that m chosen doesnt work then double it and give it to loop again




def on_plot_click(event):
    if event.xdata is not None and event.ydata is not None:
        points.append((event.xdata, event.ydata))
        ax.plot(event.xdata, event.ydata, 'ro')
        canvas.draw()

def on_submit():
    global anchor
    selected_algo = algo_var.get()  # Get the selected algorithm from the dropdown
    root.title(f"Convex Hull - {selected_algo}")  # Update the window title

    # Start measuring time
    start_time = time.perf_counter()

    if len(points) > 2:
        min_idx = None
        for i, (x, y) in enumerate(points):
            if min_idx is None or y < points[min_idx][1]:
                min_idx = i
            if y == points[min_idx][1] and x < points[min_idx][0]:
                min_idx = i

        anchor = points[min_idx] #already finding the anchor

        # Choose the algorithm based on the selection
        if selected_algo == 'Graham Scan':
            hull = graham_scan(points, False)
        elif selected_algo == 'Jarvis March':
            hull = jarvis_march(points)
        elif selected_algo == 'Quick Hull':
            hull = quick_hull(points)
        elif selected_algo == 'Brute Force':
            hull = compute_convex_hull()
        elif selected_algo == "Chan's Algorithm- HAPPY MR CHAN":
            hull = chans_algorithm(points, len(points))  # guessing h is the number of points

        # Stop measuring time
        end_time = time.perf_counter()

        # Calculate execution time
        execution_time = end_time - start_time
        print("Hull:", hull)
        print(f"Execution Time: {execution_time} seconds")

        # Display results
        if selected_algo != 'Brute Force':
            scatter_plot(points, hull)

        # Display execution time on the canvas
        ax.text(1, 63, f"Time: {execution_time:.7f} sec", fontsize=10, color='cyan')
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
            ax.plot((p0[0], p1[0]), (p0[1], p1[1]), 'r') #red line between points
    canvas.draw()

# Tkinter setup
root = tk.Tk()
root.title("Convex Hull - Select Algorithm")

# Dropdown menu for algorithm selection
algo_var = tk.StringVar()
algo_dropdown = ttk.Combobox(root, textvariable=algo_var, state='readonly')
algo_dropdown['values'] = ('Graham Scan', 'Jarvis March', 'Quick Hull', 'Brute Force', "Chan's Algorithm- HAPPY MR CHAN")
algo_dropdown.current(0)  # Default to Graham Scan
algo_dropdown.pack(side=tk.TOP)

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

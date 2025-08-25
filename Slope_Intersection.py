import tkinter as tk

def calculate_slope(p1, p2):
    if p2[0] - p1[0] == 0:
        return None  # vertical line
    return (p2[1] - p1[1]) / (p2[0] - p1[0])

def calculate_y_intercept(p, m):
    if m is None:
        return p[0]  # For vertical lines, return x-coordinate
    else:
        return p[1] - (m * p[0])

def is_between(a, b, c):
    return min(a, b) <= c <= max(a, b)

def do_lines_intersect(p1, p2, p3, p4):
    slope1 = calculate_slope(p1, p2)
    slope2 = calculate_slope(p3, p4)

    if slope1 == slope2:
        return False  # Parallel or coincident lines

    c1 = calculate_y_intercept(p1, slope1)
    c2 = calculate_y_intercept(p3, slope2)

    if slope1 is None:  # First line vertical
        x = c1
        y = slope2 * x + c2
    elif slope2 is None:  # Second line vertical
        x = c2
        y = slope1 * x + c1
    else:
        x = (c2 - c1) / (slope1 - slope2)
        y = slope1 * x + c1

    return is_between(p1[0], p2[0], x) and is_between(p1[1], p2[1], y) and \
           is_between(p3[0], p4[0], x) and is_between(p3[1], p4[1], y)

def on_canvas_click(event):
    global points, canvas
    points.append((event.x, event.y))
    canvas.create_oval(event.x-2, event.y-2, event.x+2, event.y+2, fill="black")

    if len(points) % 2 == 0:
        p1, p2 = points[-2], points[-1]
        canvas.create_line(p1[0], p1[1], p2[0], p2[1])

    if len(points) == 4:
        intersect = do_lines_intersect(points[0], points[1], points[2], points[3])
        result.set("The line segments intersect: " + str(intersect))
        points = []  # Reset the points for new line segments

# Set up the main application window
root = tk.Tk()
root.title("Line Segment Intersection")

# Global variables
points = []

# Create a canvas for drawing
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()
canvas.bind("<Button-1>", on_canvas_click)

# Label for displaying the result
result = tk.StringVar()
result_label = tk.Label(root, textvariable=result)
result_label.pack()

root.mainloop()

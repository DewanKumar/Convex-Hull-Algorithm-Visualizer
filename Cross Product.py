import tkinter as tk

# Function to calculate direction
def direction(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

# Function to determine if segments intersect
def segments_intersect(p1, p2, p3, p4):
    d1 = direction(p3, p4, p1)
    d2 = direction(p3, p4, p2)
    d3 = direction(p1, p2, p3)
    d4 = direction(p1, p2, p4)

    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True
    else:
        return False

# Event handler for canvas click
def on_canvas_click(event):
    global points
    points.append((event.x, event.y))

    # Draw the point on the canvas
    canvas.create_oval(event.x - 3, event.y - 3, event.x + 3, event.y + 3, fill="cyan")

    # When two points are clicked, draw a line segment
    if len(points) % 2 == 0:
        canvas.create_line(points[-2], points[-1], fill="red")

    # When four points are clicked, check for intersection
    if len(points) == 4:
        if segments_intersect(points[0], points[1], points[2], points[3]):
            result.set("The line segments intersect.")
        else:
            result.set("The line segments do not intersect.")
        points = []  # Clear points to allow for new line segments

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

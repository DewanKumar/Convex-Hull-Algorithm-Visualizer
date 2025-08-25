import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

points = []  # List of points, where each point is a tuple (x, y)


def which_side_of_line(line_endpt_a, line_endpt_b, pt_subject):
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

                if which_side_of_line(pt_i, pt_j, points[k]) < 0:
                    all_points_on_the_right = False
                    break

            if all_points_on_the_right:
                ax.plot([pt_i[0], pt_j[0]], [pt_i[1], pt_j[1]], 'b-')  # Draw line in blue

    # Plot the points
    x_coords, y_coords = zip(*points)
    ax.scatter(x_coords, y_coords, color='r')
    canvas.draw()


def on_plot_click(event):
    if event.xdata is not None and event.ydata is not None:
        points.append((event.xdata, event.ydata))
        ax.plot(event.xdata, event.ydata, 'ro')
        canvas.draw()


# Tkinter setup
root = tk.Tk()
root.title("Convex Hull Visualization")

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

# Compute button
compute_button = tk.Button(master=root, text="Compute Convex Hull", command=compute_convex_hull)
compute_button.pack(side=tk.BOTTOM)

root.mainloop()


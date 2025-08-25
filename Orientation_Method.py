import tkinter as tk
from PIL import Image, ImageTk
from itertools import count, cycle
import pygame

# Initialize pygame mixer
pygame.mixer.init()

class ImageLabel(tk.Label):
    def load(self, im, resize=None, sound=None):
        if isinstance(im, str):
            im = Image.open(im)
        frames = []

        try:
            while True:
                if resize:
                    frame = im.copy()
                    frame = frame.resize(resize)
                else:
                    frame = im.copy()
                frames.append(ImageTk.PhotoImage(frame))
                im.seek(im.tell() + 1)
        except EOFError:
            pass

        self.frames = cycle(frames)

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()

        # Play sound if provided
        if sound:
            pygame.mixer.music.load(sound)
            pygame.mixer.music.play()

    def unload(self):
        self.config(image=None)
        self.frames = None
        pygame.mixer.music.stop()  # Stop playing the sound

    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)

def ccw(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

def do_lines_intersect(l1_p1, l1_p2, l2_p1, l2_p2):
    test1 = ccw(l1_p1, l1_p2, l2_p1) * ccw(l1_p1, l1_p2, l2_p2)
    test2 = ccw(l2_p1, l2_p2, l1_p1) * ccw(l2_p1, l2_p2, l1_p2)
    return test1 <= 0 and test2 <= 0

def on_canvas_click(event):
    global points, canvas, lbl
    points.append((event.x, event.y))
    canvas.create_oval(event.x-3, event.y-3, event.x+3, event.y+3, fill="black")

    if len(points) % 2 == 0:
        p1, p2 = points[-2], points[-1]
        canvas.create_line(p1[0], p1[1], p2[0], p2[1])

    if len(points) == 4:
        intersect = do_lines_intersect(points[0], points[1], points[2], points[3])
        if intersect:
            lbl.load('chika.gif', resize=(200, 200), sound=r'oh-my-gah.mp3')  # Add your sound file here
        else:
            lbl.unload()
        points = []

# Set up the main application window
root = tk.Tk()
root.title("Line Segment Intersection")

points = []

canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()
canvas.bind("<Button-1>", on_canvas_click)

lbl = ImageLabel(root)
lbl.pack()

root.mainloop()

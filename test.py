import tkinter as tk

def draw_up(canvas, x, y, color = "lightblue",  arrow_size = 10, line_width = 7):
    canvas.create_line(x, y, x, y - 50, fill=color, width=line_width)
    canvas.create_polygon(x, y - 50 - 4, x - arrow_size, y - 50 + arrow_size, x + arrow_size, y - 50 + arrow_size, fill=color)

def draw_down(canvas, x, y, color = "lightblue",  arrow_size = 10, line_width = 7):       
    canvas.create_line(x, y, x, y + 50, fill=color, width=line_width)
    canvas.create_polygon(x, y + 50 + 4, x - arrow_size, y + 50 - arrow_size, x + arrow_size, y + 50 - arrow_size, fill=color)  

def draw_left(canvas, x, y, color = "lightblue",  arrow_size = 10, line_width = 7):
    canvas.create_line(x, y, x - 50, y, fill=color, width=line_width)
    canvas.create_polygon(x - 50 - 4, y, x - 50 + arrow_size, y - arrow_size, x - 50 + arrow_size, y + arrow_size, fill=color)

def draw_right(canvas, x, y, color = "lightblue",  arrow_size = 10, line_width = 7):
    canvas.create_line(x, y, x + 50, y, fill=color, width=line_width)
    canvas.create_polygon(x + 50 + 4, y, x + 50 - arrow_size, y - arrow_size, x + 50 - arrow_size, y + arrow_size, fill=color)


# 0: Up, 1: Right, 2: Down, 3: Left
def draw_all_direction(canvas, x, y, color = "lightblue"):
    draw_up(canvas, x, y, color=color)
    draw_down(canvas, x, y, color=color)
    draw_left(canvas, x, y, color=color)
    draw_right(canvas, x, y, color=color)



# Create the main window
root = tk.Tk()
root.title("Draw Arrows in 4 Directions")

# Create canvas
canvas = tk.Canvas(root, width=400, height=400, bg="white")
canvas.pack()

# Draw arrows
draw_all_direction(canvas, 100, 100)  # Arrow pointing up
draw_up(canvas, 100, 100, "red")

# Run the application
root.mainloop()

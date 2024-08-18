import tkinter as tk

def draw_up(canvas, x, y, color = "lightblue",  arrow_size = 10, line_width = 8):
    tail = line_width/2
    canvas.create_line(x , y-tail, x, y - 50, fill=color, width=line_width)
    canvas.create_polygon(x, y - 50 - 4, x - arrow_size, y - 50 + arrow_size, x + arrow_size, y - 50 + arrow_size, fill=color)
    # canvas.create_polygon(x, y -tail , x -tail, y -tail , x, y + tail/2, x + tail, y - tail , fill=color)

def draw_down(canvas, x, y, color = "lightblue",  arrow_size = 10, line_width = 7):       
    tail = line_width/2
    canvas.create_line(x, y+tail, x, y + 50, fill=color, width=line_width)
    canvas.create_polygon(x, y + 50 + 4, x - arrow_size, y + 50 - arrow_size, x + arrow_size, y + 50 - arrow_size, fill=color)

def draw_left(canvas, x, y, color = "lightblue",  arrow_size = 10, line_width = 7):
    tail = line_width/2
    canvas.create_line(x - tail, y, x - 50, y, fill=color, width=line_width)
    canvas.create_polygon(x - 50 - 4, y, x - 50 + arrow_size, y - arrow_size, x - 50 + arrow_size, y + arrow_size, fill=color)

def draw_right(canvas, x, y, color = "lightblue",  arrow_size = 10, line_width = 7):
    tail = line_width/2
    canvas.create_line(x + tail, y, x + 50, y, fill=color, width=line_width)
    canvas.create_polygon(x + 50 + 4, y, x + 50 - arrow_size, y - arrow_size, x + 50 - arrow_size, y + arrow_size, fill=color)

def draw_HP(canvas, x, y, size, HP = 100, width = 20):
    len = float(size / 100)
    color = ""
    if HP >75: color = "green"
    elif HP >50: color = "yellow"
    elif HP >25: color ="orange" 
    else: color ="red"  

    canvas.create_line(x, y, x + len * HP, y, fill=color, width=width)

    for i in range (1,5):
        x1 = x - 1
        x2 = x + 25*i *len
        y1 = y - width/2
        y2 = y + width/2
        canvas.create_rectangle(x1, y1, x2, y2, fill="", outline="black")

# 0: Up, 1: Right, 2: Down, 3: Left
def draw_all_direction(canvas, x, y, color = "lightblue"):
    draw_up(canvas, x, y, color=color)
    draw_down(canvas, x, y, color=color)
    draw_left(canvas, x, y, color=color)
    draw_right(canvas, x, y, color=color)


def draw_potion(canvas):
    # Hình dạng bình
    canvas.create_polygon(
        150, 10,  # Đỉnh của nắp bình
        130, 40,  # Góc trái trên cùng của thân bình
        130, 140, # Góc trái dưới cùng của thân bình
        170, 140, # Góc phải dưới cùng của thân bình
        170, 40,  # Góc phải trên cùng của thân bình
        fill="lightpink", outline="black"
    )
    
    # Chất lỏng trong bình
    canvas.create_polygon(
        135, 45, 
        135, 135, 
        165, 135, 
        165, 45, 
        fill="red", outline="darkred"
    )
    
    # Nắp bình
    canvas.create_polygon(
        140, 0,  # Đỉnh của nắp bình
        130, 20,  # Góc trái dưới của nắp bình
        170, 20,  # Góc phải dưới của nắp bình
        160, 0,  # Đỉnh của nắp bình
        fill="gray", outline="black"
    )

    # Thêm chi tiết trang trí
    canvas.create_oval(135, 10, 165, 40, outline="gold", width=2)

def main():
    root = tk.Tk()
    root.title("Healing Potion")
    
    canvas = tk.Canvas(root, width=300, height=200, bg="darkslateblue")
    canvas.pack()
    
    draw_potion(canvas)
    
    root.mainloop()

if __name__ == "__main__":
    main()

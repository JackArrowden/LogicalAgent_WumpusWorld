import tkinter as tk
import file
from PIL import Image, ImageTk

def checkOpenFile(file):
    try:
        with open(file, 'r') as cur:
            return True
    except:
        return False

class SystemGUI():
    def __init__(self, root):
        self.root = root
        self.root.geometry('1200x720')
        self.root.title("Delivery system")
        self.font1 = ("Bahnschrift Light SemiCondensed", 12)
        self.font2 = ("Bahnschrift Light SemiCondensed", 20)
        self.root.option_add("*Font", self.font1)
        
        self.default_text = "Enter input file..."
        self.text1 = "The file's name must not be left blank!"
        self.text2 = "An error occur while opening input file\nPlease enter another file's name..."
        # self.root.protocol("WM_DELETE_WINDOW", self.exit)    
        self.width = 0
        self.height = 0
        self.edge = 0
            
        self.fileName = ""

        
        self.frame1 = tk.Frame(self.root)
        self.frame2 = tk.Frame(self.root)
        # self.frame3 = tk.Frame(self.root)
        # self.frame4 = tk.Frame(self.root)
        # self.frame5 = tk.Frame(self.root)
        
        self.resetBtn = [True, True, True]
        self.images= []

        self.listColorSs = [["#0B77A0", "#074761"], ["#0D8B9C", "#085660"], 
                            ["#109994", "#0D7D78"], ["#11A28C", "#0D8170"], 
                            ["#12AD7F", "#0D795A"], ["#14B66E", "#12A261"], 
                            ["#14BD5C", "#0F8F46"], ["#15C247", "#109235"], 
                            ["#15C62E", "#12A627"], ["#16C80D", "#11980A"]]
        self.listColorCurSs = [["#09B354", "black"], ["#30BE66", "black"],
                               ["#47C570", "black"], ["#5FCC7B", "black"],
                               ["#78D387", "black"], ["#89D88E", "black"],
                               ["#99DD96", "black"], ["#A7E19C", "black"],
                               ["#AFE4A0", "black"], ["#B4E5A2", "black"]]
        self.listColorGs = [["#E83E2A", "#BC2414"], ["#ED5F36", "#C43812"],
                            ["#F0743E", "#EC5512"], ["#F38544", "#F06A18"],
                            ["#F59449", "#E1680D"], ["#F7A34F", "#E4770A"],
                            ["#F9B053", "#EE8B08"], ["#FBB957", "#E48A06"],
                            ["#FCBF59", "#FBA00D"], ["#FCC25A", "#F6A004"]]
        self.listColorFs = [["#F3F595", "black"], ["#F6F791", "black"], 
                            ["#F7F98B", "black"], ["#F9FA81", "black"], 
                            ["#FBFB75", "black"], ["#FCFD64", "black"], 
                            ["#FDFD54", "black"], ["#FEFE3B", "black"], 
                            ["#FFFF27", "black"], ["#FFFF10", "black"]]
        self.listColorLines = ["#FF0000", "#00B050", "#163E64", "#78206E", "#3A3A3A", "#0070C0", "#FFC000", "#C00000", "#7030A0", "#7F7F7F"]
        
        self.showFrame2()

    def mainFrame(self): #### Frame 1  
        ## Input frame
        self.entry = tk.Text(self.frame1, fg = "gray", width = 50, height = 2, padx = 10, bg = "white", highlightbackground = "#2F4F4F")
        self.entry.insert("1.0", self.default_text)
        self.entry.pack(pady = 5)
        self.entry.bind("<FocusIn>", self.entryOnFocus)
        self.entry.bind("<FocusOut>", self.entryOnBlur)  
        self.entry.bind("<KeyPress>", self.resetText)

        ### SubFrame
        self.subFrame = tk.Frame(self.frame1)
        self.subFrame.pack(pady = (20, 10))

        ## Enter button
        self.enterBtn = tk.Button(self.subFrame, text = "Enter", command = self.getFileName, bg = "#323232", fg = "#FAFAFA", width = 40, height = 2, cursor = "hand2")
        self.enterBtn.pack(pady = (5, 10))
        
        ## Exit button
        self.exitBtn1 = tk.Button(self.subFrame, text = "Exit", command = self.exit, bg = "#323232", fg = "#FAFAFA", width = 40, height = 2, cursor = "hand2")
        self.exitBtn1.pack(pady = (5, 10))

    def entryOnFocus(self, event):
        if self.entry.get("1.0", tk.END).strip() == self.default_text:
            self.entry.delete("1.0", tk.END)

    def entryOnBlur(self, event):
        if self.entry.get("1.0", tk.END).strip() == "":
            self.entry.insert("1.0", self.default_text)
        else:
            self.entry.delete("1.0", tk.END)
                
    def resetText(self, event):
        if event.keysym == 'BackSpace' and len(self.entry.get("1.0", tk.END).strip()) == 1:
            self.entry.delete("1.0", tk.END)
            self.entry.insert("1.0", self.default_text)
            self.entry.mark_set("insert", "1.0")
        elif self.entry.get("1.0", tk.END).strip() == self.default_text or self.entry.get("1.0", tk.END).strip() == self.text1 or self.entry.get("1.0", tk.END).strip() == self.text2:
            self.entry.delete("1.0", tk.END)
    
    def getFileName(self):
        self.fileName = self.entry.get("1.0", tk.END).strip()

        if self.fileName == "" or self.fileName == self.default_text or self.fileName == self.text1 or self.fileName == self.text2:
            self.entry.delete("1.0", tk.END)
            self.entry.insert("1.0", self.text1)
            self.entry.mark_set("insert", "1.0")
        elif checkOpenFile(self.fileName) == False:
            self.entry.delete("1.0", tk.END)
            self.entry.insert("1.0", self.text2)  
            self.entry.mark_set("insert", "1.0")
        else:
            resultRead = file.readF(self.fileName)
            self.col = len(resultRead[0])
            self.row = len(resultRead)
            self.showFrame2()
    
    def clearFrame(self, frame):
        for widget in frame.winfo_children():
            try:
                widget.destroy()
            except tk.TclError as e:
                pass

    def unshowAllFrames(self):
        self.frame1.pack_forget()
        self.frame2.pack_forget()
        # self.frame3.pack_forget()
        # self.frame4.pack_forget()
        # self.frame5.pack_forget()

    def showFrame1(self):
        self.isResetList = True
        self.unshowAllFrames()
        self.root.title("Wumpus world")
        self.frame1.pack(expand=True, anchor='center') 
        self.clearFrame(self.frame1)  
        self.mainFrame()

    def create_grid(self,canvas, rows, cols, cell_size):
        for i in range(rows):
            for j in range(cols):
                x1 = j * cell_size
                y1 = i * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")

    def add_image(self,canvas, image_path, row, col, image_size=65, x=0, y=0 ):
        image = Image.open(image_path)
        image = image.resize((image_size, image_size), Image.Resampling.LANCZOS)
        
        photo = ImageTk.PhotoImage(image)
        self.images.append(photo)  

        x = col * self.cell_size + x
        y = row * self.cell_size + y
        canvas.create_image(x, y, anchor='nw', image=photo)
        canvas.image = photo


    def draw_dot(self, canvas, row, col, color="red", radius=10, m = 10, n=10):
        x = col * self.cell_size + m
        y = row * self.cell_size + n

        # Calculate the coordinates for the circle
        x1 = x - radius
        y1 = y - radius
        x2 = x + radius
        y2 = y + radius

        # Draw the circle
        canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color)
    
    def drawElements(self, canvas, mapElement):
        filePath = ["wumpus.jnp", "pit.jnp", "gas.jnp","HPotion.jnp", "gold.jpn"]

            
        return
    
    def drawPerceps(self, canvas, mapPerceps):  
        color = ["#3CB371","#8EE5EE","#8E388E","#FFF68F"] #  stench, breeze,whiff, glow 
        for i in range(10):
            for j in range(10):
                N = 10
                for k in range(4):
                    if mapPerceps[i][j][k]:
                        self.draw_dot(canvas,i,j,color[k],radius = 4.5, m = 9,n=N)
                    N +=15
        return
    
    def showFrame2(self):
        self.unshowAllFrames()
        self.frame2.pack(expand=True, fill=tk.BOTH) 
        self.clearFrame(self.frame2)
        
        A = [
            [[True, True, True , True], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False]],
            [[False,False, False, False], [True,True, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False]],
            [[False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False]],
            [[False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False]],
            [[False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False]],
            [[False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False]],
            [[False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False]],
            [[False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False]],
            [[False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False]],
            [[False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False], [False,False, False, False]]
        ]

        self.col = 10
        self.row = 10
        self.cell_size = 65

        # Add the greeting label at the top-left of the frame

        # Create subFrame2a and subFrame2b to split the frame2
        self.subFrame2a = tk.Frame(self.frame2, bg="lightgrey")
        self.subFrame2a.pack(side=tk.LEFT, expand=True)

        # cell_size = 50
        canvas_width = self.cell_size * self.col
        canvas_height = self.cell_size * self.row

        canvas = tk.Canvas(self.subFrame2a, width=canvas_width, height=canvas_height)
        canvas.pack(expand=True)

        self.create_grid(canvas, self.row, self.col, self.cell_size)
        self.drawPerceps(canvas, A)
        self.add_image(canvas, "wumpus.png", 0 , 0, 21, 16, 2)
        self.add_image(canvas, "wumpus.png", 0 , 0, 21, 42, 2)
        self.add_image(canvas, "wumpus.png", 0 , 0, 21, 16, 2+20)
        self.add_image(canvas, "wumpus.png", 0 , 0, 21, 42, 2+20)
        self.add_image(canvas, "wumpus.png", 0 , 0, 21, 16, 2+40)
        self.add_image(canvas, "wumpus.png", 0 , 0, 21, 42, 2+40)
        # self.drawElements(canvas, B)
        
        self.subFrame2b = tk.Frame(self.frame2, bg="lightblue")

        self.subFrame2b.pack(side=tk.RIGHT, expand=True, anchor='nw', padx=(0, 300), pady=(30, 0))
        greeting = tk.Label(self.subFrame2b, text="Path")
        greeting.pack(padx=10, pady=10)

        return

    def exit(self):
        try:
            self.root.destroy()
        except:
            try:
                self.root.destroy()
            except:
                pass
    


if __name__ == "__main__":
    root = tk.Tk()
    app = SystemGUI(root)
    root.mainloop()
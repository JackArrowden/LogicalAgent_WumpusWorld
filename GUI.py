import tkinter as tk
import file
from Program import *
from Agent import Agent
from PIL import Image, ImageTk

class SystemGUI():
    def __init__(self, root):
        self.root = root
        self.root.geometry('1200x720')
        self.root.title("Delivery system")
        self.font1 = ("Bahnschrift Light SemiCondensed", 12)
        self.font2 = ("Bahnschrift Light SemiCondensed", 20)
        self.font3 = ("Bahnschrift Light SemiCondensed", 15)
        self.root.option_add("*Font", self.font1)
        
        self.default_text = "Enter input file..."
        self.text1 = "The file's name must not be left blank!"
        self.text2 = "An error occur while opening input file\nPlease enter another file's name..."
        # self.root.protocol("WM_DELETE_WINDOW", self.exit)
            
        self.width = 0
        self.height = 0
        self.row = 10 
        self.col = 10
        self.cell_size = 65
        self.HP = 100

        self.program = GUIProgram()

        self.fileName = ""
        self.idAfter = set()
        self.map = [[0]]
        self.isSolvable = True
        
        self.isHead = True
        self.isTail = False
        self.isResetList = True
        
        self.curNumState = 0
        self.listCells = []
        self.listRemainCells = []
        self.tempCells = []
        self.tempRemainCells = []
        self.isNext = True

        self.frame1 = tk.Frame(self.root)
        self.frame2 = tk.Frame(self.root)
        self.frame3 = tk.Frame(self.root)
        # self.frame4 = tk.Frame(self.root)
        # self.frame5 = tk.Frame(self.root)
        
        self.autoRunTime = [1, {1: 1000, 2: 600, 3: 400, 4: 200, 5: 100}]
        self.images= []
        
        self.showFrame1()

    def mainFrame(self): #### Frame 1  
        ## Input frame
        self.entry = tk.Text(self.frame1, fg = "gray", width = 50, height = 2, padx = 10, bg = "white", highlightbackground = "#2F4F4F")
        self.entry.insert("1.0", self.default_text)
        self.entry.pack(pady = 5)
        self.entry.bind("<FocusIn>", self.entryOnFocus)
        self.entry.bind("<FocusOut>", self.entryOnBlur)  
        self.entry.bind("<KeyPress>", self.resetText)
        self.entry.bind('<Return>', lambda event: self.enterBtn.invoke())

        ### SubFrame
        self.subFrame = tk.Frame(self.frame1)
        self.subFrame.pack(pady = (20, 10))

        ## Enter button
        self.enterBtn = tk.Button(self.subFrame, text = "Enter", command = self.getFileName, bg = "#323232", fg = "#FAFAFA", width = 40, height = 2, cursor = "hand2")
        self.enterBtn.pack(pady = (5, 10))

        # self.subFrame.focus_set()
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
    
    def resetAllContent(self):
        self.HP = 100

        self.idAfter = set()
        self.map = [[0]]
        self.isSolvable = True
        
        self.isHead = True
        self.isTail = False
        self.isResetList = True
        
        self.curNumState = 0
        self.listCells = []
        self.listRemainCells = []
        self.tempCells = []
        self.tempRemainCells = []
        self.isNext = True
        
        self.autoRunTime = [1, {1: 1000, 2: 600, 3: 400, 4: 200, 5: 100}]
        self.images = []
    
    def getFileName(self):
        self.fileName = self.entry.get("1.0", tk.END).strip()

        if self.fileName == "" or self.fileName == self.default_text or self.fileName == self.text1 or self.fileName == self.text2:
            self.entry.delete("1.0", tk.END)
            self.entry.insert("1.0", self.text1)
            self.entry.mark_set("insert", "1.0")
        elif file.checkOpenFile(f"{self.fileName}.txt") == False:
            self.entry.delete("1.0", tk.END)
            self.entry.insert("1.0", self.text2)  
            self.entry.mark_set("insert", "1.0")
        else:
            _ = self.resetAllContent()
            environment = Program(f"{self.fileName}.txt")
            agent = Agent()
            agent.init(environment)
            file.writeF(f"{self.fileName}_result.txt", agent.explore_world())
            self.program.getMap(f"{self.fileName}.txt")
            self.listRemainCells = file.readOutputFile(f"{self.fileName}_result.txt")
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
        self.frame3.pack_forget()
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
                canvas.create_rectangle(x1, y1, x2, y2, fill="#CCCCCC", outline="black")

        for cell in self.listCells:
            canvas.create_rectangle(cell[0][1]*cell_size, cell[0][0]*cell_size, (cell[0][1]+1)*cell_size, (cell[0][0]+1)*cell_size, fill="white", outline="black")

        hht = rows * cell_size
        wth = cols * cell_size

        canvas.create_line([(2, 0), (2, hht)], fill='black')
        canvas.create_line([(wth, 0), (wth, hht)], fill='black')
        canvas.create_line([(0, 2), (wth, 2)], fill='black')
        canvas.create_line([(0, hht), (wth, hht)], fill='black')

    def add_image(self,canvas, image_path, row=0, col=0, image_size=65, x=0, y=0 ):
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
    
    def drawElements(self, canvas):
        TEXT = ["W", 'P', 'G', 'H', 'T']
        for i in range(10):
            for j in range(10):
                for k in range(5):
                    if self.mapElements[i][j][k]:
                        x = j*self.cell_size +  29 + (23 if k%2 else 0)
                        y = i*self.cell_size + 12 +(20* int(k/2)) 
                        canvas.create_text(x, y,  text=TEXT[k], font=("Arial", 15), fill="Red")
    
    def drawPercepts(self, canvas):  
        color = ["#3CB371","#8EE5EE","#8E388E","#FFF68F"] #  stench, breeze,whiff, glow 
        for i in range(10):
            for j in range(10):
                N = 10
                for k in range(4):
                    if self.mapPercepts[i][j][k]:
                        self.draw_dot(canvas, i, j, color[k], radius = 5.5, m = 9, n=N)
                    N +=15
    
    def draw_map(self, canvas):
        self.mapPercepts = getAllPercepts(self.program)
        self.mapElements = getAllElements(self.program)
        self.create_grid(canvas, self.row, self.col, self.cell_size)
        self.drawPercepts(canvas)
        self.drawElements(canvas)

        curPos = self.listCells[len(self.listCells)-1]
        self.add_image(canvas, "GUI_imagine/asd.jpg", curPos[0][0], curPos[0][1], 18, 41, 44)

    def draw_HP(self, canvas, x, y, size, HP = 100, width = 10):
        len = float(size / 100)
        
        color = ""
        if HP >75: color = "green"
        elif HP >50: color = "yellow"
        elif HP >25: color ="orange" 
        else: color ="red"  

        canvas.create_line(x, y, x + size, y, fill='white', width=width)
        canvas.create_line(x, y, x + len * HP, y, fill=color, width=width)

        for i in range (1,5):
            x1 = x - 1
            x2 = x + 25*i *len
            y1 = y - width/2
            y2 = y + width/2
            canvas.create_rectangle(x1, y1, x2, y2, fill="", outline="black")

    def chooseViewFrame(self):
        self.subFrame2a = tk.Frame(self.frame2)
        self.subFrame2a.pack(expand=True, anchor='center', pady = (0, 80)) 

        ## Step by step manually
        self.stepByStepManuBtn = tk.Button(self.subFrame2a, text = "Show step by step manually", command = self.showFrame3, bg = "#323232", fg = "#FAFAFA", width = 40, height = 2, cursor = "hand2")
        self.stepByStepManuBtn.pack(pady = (10, 10))
        
        ## Step by step automatically
        self.stepByStepAutoBtn = tk.Button(self.subFrame2a, text = "Show step by step automatically", command = lambda: self.showFrame3(True), bg = "#323232", fg = "#FAFAFA", width = 40, height = 2, cursor = "hand2")
        self.stepByStepAutoBtn.pack(pady = (10, 10))

        ### Frame b
        self.subFrame2b = tk.Frame(self.frame2)
        self.subFrame2b.pack(expand=True, anchor='center', pady = (20, 0)) 
            
        ## Back button 1
        self.backBtn1 = tk.Button(self.subFrame2b, text = "Back", command = self.showFrame1, bg = "#323232", fg = "#FAFAFA", width = 25, height = 2, cursor = "hand2")
        self.backBtn1.pack(side = tk.LEFT, pady = (10, 10), padx = (0, 30))
        
        ## Exit button 2
        self.exitBtn2 = tk.Button(self.subFrame2b, text = "Exit", command = self.exit, bg = "#323232", fg = "#FAFAFA", width = 25, height = 2, cursor = "hand2")
        self.exitBtn2.pack(side = tk.LEFT, pady = (10, 10), padx = (30, 0))

    def moveContent(self, listA, listB):
        while listA:
            cur = listA.pop()
            listB.insert(0, cur)
            
    def moveContentRev(self, listA, listB):
        while listA:
            cur = listA.pop(0)
            listB.append(cur)
    
    def move2DContent(self, listA, listB):
        listLen = len(listA)
        for index in range(listLen):
            self.moveContent(listA[index], listB[index])

    def showFrame2(self):
        for after_id in self.idAfter:
            self.root.after_cancel(after_id)
        self.idAfter.clear()
        
        self.program.getMap(f"{self.fileName}.txt")

        self.isResetList = True
        self.isHead = True
        self.isTail = False
        self.unshowAllFrames()
        self.root.title("Choose view frame")
        self.frame2.pack(expand=True, anchor='center')  
        self.clearFrame(self.frame2) 
        self.program.getMap(f"{self.fileName}.txt")
        self.program.agentHealth = 100
        self.chooseViewFrame()

    def showFrame3(self, isAuto = False):
        self.unshowAllFrames()
        self.root.title("Step by step")
        self.frame3.pack(expand=True, anchor='center')
        
        self.moveContent(self.listCells, self.listRemainCells)
        self.move1Item(self.listRemainCells, self.listCells)
        
        self.program.handleNextAction(self.listCells[0][1], self.listCells[0][0])

        self.clearFrame(self.frame3)  
        self.curNumState = 0
        self.stepByStepFrame(isAuto)

    def draw_up(self, canvas, x, y, color = "lightblue",  arrow_size = 10, line_width = 7):
        canvas.create_line(x, y, x, y - 50, fill=color, width=line_width)
        canvas.create_polygon(x, y - 50 - 4, x - arrow_size, y - 50 + arrow_size, x + arrow_size, y - 50 + arrow_size, fill=color)

    def draw_down(self, canvas, x, y, color = "lightblue",  arrow_size = 10, line_width = 7):       
        canvas.create_line(x, y, x, y + 50, fill=color, width=line_width)
        canvas.create_polygon(x, y + 50 + 4, x - arrow_size, y + 50 - arrow_size, x + arrow_size, y + 50 - arrow_size, fill=color)  

    def draw_left(self, canvas, x, y, color = "lightblue",  arrow_size = 10, line_width = 7):
        canvas.create_line(x, y, x - 50, y, fill=color, width=line_width)
        canvas.create_polygon(x - 50 - 4, y, x - 50 + arrow_size, y - arrow_size, x - 50 + arrow_size, y + arrow_size, fill=color)

    def draw_right(self, canvas, x, y, color = "lightblue",  arrow_size = 10, line_width = 7):
        canvas.create_line(x, y, x + 50, y, fill=color, width=line_width)
        canvas.create_polygon(x + 50 + 4, y, x + 50 - arrow_size, y - arrow_size, x + 50 - arrow_size, y + arrow_size, fill=color)

    def getTotalScore(self):
        self.score = 0
        scoreDict = {
            'move forward': -10,
            'turn left': -10,
            'turn right': -10,
            'shoot': -100,
            'climb': 10,
            'heal': -10,
            'grab': -10
        }
        self.score += getNumGold(self.program) * 5000
        for index, action in enumerate(self.listCells):
            if index != len(self.listCells) - 1:
                self.score += scoreDict[action[1]]

    # 0: Up, 1: Right, 2: Down, 3: Left
    def draw_all_direction(self, canvas, x, y, color = "lightblue"):
        self.draw_up(canvas, x, y, color=color)
        self.draw_down(canvas, x, y, color=color)
        self.draw_left(canvas, x, y, color=color)
        self.draw_right(canvas, x, y, color=color)

    def add_Healing_potion(self,canvas, image_size = 30, x=0, y=0, quantity = 6):
        image_path = "GUI_imagine/Healing_potion.png"
        image = Image.open(image_path)

        original_width, original_height = image.size

        scale_factor = image_size

        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)

        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        photo = ImageTk.PhotoImage(resized_image)
        self.images.append(photo)  

        canvas.create_image(x , y, anchor='nw', image=photo)
        canvas.image = photo
    
        canvas.create_text( x + 19, y + new_height - 33, text = f" x {quantity} ", font=("Arial", 15), fill="Red", anchor ='nw')

    def add_Wumpus_Kill(self,canvas, image_size = 30, x=0, y=0, quantity = 6):
        image_path = "GUI_imagine/wumpus.png"
        image = Image.open(image_path)

        original_width, original_height = image.size

        scale_factor = image_size

        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)

        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        photo = ImageTk.PhotoImage(resized_image)
        self.images.append(photo)  

        canvas.create_image(x , y, anchor='nw', image=photo)
        canvas.image = photo
    
        canvas.create_text( x + 47, y + new_height - 36, text = f" x {quantity} ", font=("Arial", 15), fill="Red", anchor ='nw')

    def stepByStepFrame(self, isAuto): #### Frame 3        
        # if self.isResetList:
        #     self.isResetList = False
        #     self.move2DContent(self.listCells, self.listRemainCells)
        #     # self.move1Item(self.listRemainCells, self.listCells)

        self.width = self.cell_size * self.col
        self.height = self.cell_size * self.row
        self.edge = self.cell_size
        self.curTxtID = 0
        
        ### Sub frame 3 a
        self.subFrame3a = tk.Frame(self.frame3)
        self.subFrame3a.pack(side = tk.LEFT,expand=True, anchor='center', pady = (5, 15), padx = (5, 25))  
        
        ## Sub frame 3 a1
        self.subFrame3a1 = tk.Frame(self.subFrame3a, width = 200)
        self.subFrame3a1.pack(expand=False, anchor='center', pady = (5, 2))  
        
        self.backBtn3a1 = tk.Button(self.subFrame3a1, text = "Back", command = self.showFrame2, bg = "#323232", fg = "#FAFAFA", width = 20, height = 2, cursor = "hand2")
        self.backBtn3a1.pack(pady = (0, 3))
        
        ## Sub frame 3 a2
        self.subFrame3a2 = tk.Frame(self.subFrame3a, width = 200)
        self.subFrame3a2.pack(expand=False, anchor='center', pady = (5, 2)) 
        
        self.exitBtn3 = tk.Button(self.subFrame3a2, text = "Exit", command = self.exit, bg = "#323232", fg = "#FAFAFA", width = 20, height = 2, cursor = "hand2")
        self.exitBtn3.pack(pady = (0, 50))
        
        if not isAuto:
            self.prevBtn1 = tk.Button(self.subFrame3a, state = "disabled", text = "Previous", bg = "lightgray", fg = "white", width = 20, height = 2)
            self.prevBtn2 = tk.Button(self.subFrame3a, text = "Previous", command = lambda: self.prevMap(kwargs = [self.subFrame3b, self.prevBtn1, self.prevBtn2, self.nextBtn1, self.nextBtn2, self.subFrame3c1, self.subFrame3c2]), bg = "#323232", fg = "#FAFAFA", width = 20, height = 2, cursor = "hand2")
            self.prevBtn1.pack(pady = (5, 5)) 
                
            self.nextBtn1 = tk.Button(self.subFrame3a, state = "disabled", text = "Next", bg = "lightgray", fg = "white", width = 20, height = 2)
            self.nextBtn2 = tk.Button(self.subFrame3a, text = "Next", command = lambda: self.nextMap(isAuto = False, kwargs = [self.subFrame3b, self.prevBtn1, self.prevBtn2, self.nextBtn1, self.nextBtn2, self.subFrame3c1, self.subFrame3c2]), bg = "#323232", fg = "#FAFAFA", width = 20, height = 2, cursor = "hand2")
            self.nextBtn2.pack(pady = (5, 5))
            def on_next_press(event):
                self.nextBtn1.invoke()
                self.nextBtn2.invoke()

            def on_prev_press(event):
                self.prevBtn1.invoke()
                self.prevBtn2.invoke()

            self.subFrame3a.focus_set()
            self.subFrame3a.bind('<Right>', on_next_press)
            self.subFrame3a.bind('<Left>', on_prev_press)
        else:
            self.slowDown1 = tk.Button(self.subFrame3a, text = "Slow down", command = lambda: self.slowDownFunc(kwargs = [self.slowDown1, self.slowDown2, self.speedUp1, self.speedUp2]), bg = "#323232", fg = "#FAFAFA", width = 20, height = 2, cursor = "hand2")
            self.slowDown2 = tk.Button(self.subFrame3a, state = "disabled", text = "Slow down", bg = "lightgray", fg = "white", width = 20, height = 2)
            if self.autoRunTime[0] == 1:
                self.slowDown2.pack(pady = (5, 5))  
            else:
                self.slowDown1.pack(pady = (5, 5))  
            
            self.speedUp1 = tk.Button(self.subFrame3a, text = "Speed up", command = lambda: self.speedUpFunc(kwargs = [self.slowDown1, self.slowDown2, self.speedUp1, self.speedUp2]), bg = "#323232", fg = "#FAFAFA", width = 20, height = 2, cursor = "hand2")
            self.speedUp2 = tk.Button(self.subFrame3a, state = "disabled", text = "Speed up", bg = "lightgray", fg = "white", width = 20, height = 2)
            if self.autoRunTime[0] != len(self.autoRunTime[1]):
                self.speedUp1.pack(pady = (5, 5))  
            else:
                self.speedUp2.pack(pady = (5, 5))  
            
        
        ### Sub frame 3 b
        self.subFrame3b = tk.Canvas(self.frame3, bg = "white", width = self.width, height = self.height)
        self.subFrame3b.pack(side = tk.LEFT, expand=True, anchor='center', pady = (0, 0), padx = (0, 15))  
        
        self.draw_map(self.subFrame3b)

        ### Sub frame 3 c
        self.subFrame3c = tk.Frame(self.frame3)
        self.subFrame3c.pack(side = tk.LEFT,expand=True, anchor='center', padx = (5, 25))    

        ### Sub frame 3 c1
        self.subFrame3c1 = tk.Canvas(self.subFrame3c, bg = "white", width = 220, height = self.height * 0.07)
        self.subFrame3c1.pack(anchor='center', padx = (25, 5))

        ## Cur state
        curStep = "Iteration: " + str(self.curNumState)
        self.subFrame3c1.create_text(110, 22, text = curStep, fill = "black", font = self.font2)
        
        ### Sub frame 3 c2
        self.subFrame3c2 = tk.Canvas(self.subFrame3c, bg = "white", width = 220, height = self.height * 0.5)
        self.subFrame3c2.pack(anchor='center', padx = (25, 5))

        self.subFrame3c2.create_text(110, 20,  text="AGENT: ", font = self.font2, fill="Red")
        self.subFrame3c2.create_text(30, 55,  text="HP: ", font =("Arial", 16), fill="Red")
        self.draw_HP(self.subFrame3c2, 10, 78, 190, HP = self.program.agentHealth, width = 15)

        self.add_Healing_potion(self.subFrame3c2, 0.12, 20, 95, self.program.numPotion)
        # self.add_Healing_potion(self.subFrame3c2, 0.12, 10, 95, 100)

        self.add_Wumpus_Kill(self.subFrame3c2, 0.27, 100, 95, getNumDeadWumpus(self.program))
        # self.add_Wumpus_Kill(self.subFrame3c2, 0.27, 95, 95, 100)

        self.subFrame3c2.create_text(50, 165, text="Scores: ", font =("Arial", 16), fill="Red")
        _ = self.getTotalScore()
        self.subFrame3c2.create_text(135, 165, text=f"{self.score}", font =("Arial", 18), fill="Red")

        self.subFrame3c2.create_text(60, 198,  text="Direction: ", font =("Arial", 16), fill="Red")
        # 0: Up, 1: Right, 2: Down, 3: Left
        direction = self.listCells[len(self.listCells)-1][2]
        self.draw_all_direction(self.subFrame3c2, 102, 267)
        if direction == 0:
            self.draw_up(self.subFrame3c2, 102, 267, color = 'red')
        elif direction == 1:
            self.draw_right(self.subFrame3c2, 102, 267, color = 'red')       
        elif direction == 2:
            self.draw_down(self.subFrame3c2, 102, 267, color = 'red')
        elif direction == 3:
            self.draw_left(self.subFrame3c2, 102, 267, color = 'red')

        ### Sub frame 3 c3
        self.subFrame3c3 = tk.Canvas(self.subFrame3c, bg = "white", width = 220, height = self.height * 0.42)
        self.subFrame3c3.pack(anchor='center', padx = (25, 5))  

        ## Percepts
        perTitle = "Percepts:"     
        self.subFrame3c3.create_text(110, 20, text = perTitle, fill = "black", font = self.font2)

        ## Percepts 1
        perA = "Stench"
        self.draw_dot(self.subFrame3c3, 0.85, 0.12, "#3CB371", 5.5, 9, 10)     
        self.subFrame3c3.create_text(55, 65, text = perA, fill = "black", font = self.font3)

        ## Percepts 1
        perA = "Breeze"  
        self.draw_dot(self.subFrame3c3, 0.625, 1.7, "#8EE5EE", 5.5, 9, 25)  
        self.subFrame3c3.create_text(160, 65, text = perA, fill = "black", font = self.font3)

        ## Percepts 2
        perA = "Whiff" 
        self.draw_dot(self.subFrame3c3, 0.85, 0.12, "#8E388E", 5.5, 9, 40)    
        self.subFrame3c3.create_text(51, 95, text = perA, fill = "black", font = self.font3)

        ## Percepts 2
        perA = "Glow"
        self.draw_dot(self.subFrame3c3, 0.625, 1.7, "#FFF68F", 5.5, 9, 55)     
        self.subFrame3c3.create_text(155, 95, text = perA, fill = "black", font = self.font3)

        ## Objects
        objTitle = "Objects:"
        self.subFrame3c3.pack( expand=True, anchor='center')     
        self.subFrame3c3.create_text(110, 150, text = objTitle, fill = "black", font = self.font2)

        ## Objects 1
        objA = "Wumpus"
        self.subFrame3c3.create_text(20, 190,  text='W', font=("Arial", 15), fill="Red")
        self.subFrame3c3.create_text(72, 190, text = objA, fill = "black", font = self.font3)

        ## Objects 1
        objA = "Pit"
        self.subFrame3c3.create_text(135, 190,  text='P', font=("Arial", 15), fill="Red")
        self.subFrame3c3.create_text(160, 190, text = objA, fill = "black", font = self.font3)

        ## Objects 2
        objA = "Poison"
        self.subFrame3c3.create_text(20, 220,  text='G', font=("Arial", 15), fill="Red")
        self.subFrame3c3.create_text(65, 220, text = objA, fill = "black", font = self.font3)

        ## Objects 2
        objA = "Health"
        self.subFrame3c3.create_text(135, 220,  text='H', font=("Arial", 15), fill="Red")
        self.subFrame3c3.create_text(175, 220, text = objA, fill = "black", font = self.font3)

        ## Objects 3
        objA = "Treasure (Gold)"
        self.subFrame3c3.create_text(20, 250,  text='T', font=("Arial", 15), fill="Red")
        self.subFrame3c3.create_text(100, 250, text = objA, fill = "black", font = self.font3)

        if isAuto:
            curID = self.root.after(self.autoRunTime[1][self.autoRunTime[0]], lambda: self.nextMap(isAuto = True, kwargs = [self.subFrame3b, self.subFrame3a, self.subFrame3c1]))
            self.idAfter.add(curID)

    def prevMap(self, kwargs = []):
        self.curNumState = self.curNumState - 1
        curStep = "Iteration: " + str(self.curNumState)
        self.clearCanvas(kwargs[5])
        kwargs[5].create_text(110, 22, text = curStep, fill = "black", font = self.font2)
            
        cur = (0, 0)
            
        if len(self.listCells) >= 2:
            cur = self.listCells.pop()
            self.listRemainCells.insert(0, cur)
            
        self.clearCanvas(kwargs[0])

        cur_agent = self.listRemainCells[0]

        if self.isNext:
            self.tempRemainCells.clear()
            if cur_agent[1] in ['shoot', 'grab', 'climb', 'heal']:
                self.program.handlePrevAction(cur_agent[1], cur_agent[0])
                self.program.curStep += 1
            self.isNext = False
        
        action = self.listCells[len(self.listCells) - 1]
        if cur_agent[1] in ['move forward', 'turn left', 'turn right']:
            self.program.handlePrevAction(cur_agent[1], cur_agent[0])

        if action[1] in ['shoot', 'grab', 'climb', 'heal']:
            self.program.handlePrevAction(action[1], action[0])

        self.draw_map(kwargs[0])

        self.draw_HP(self.subFrame3c2, 10, 78, 190, HP = self.program.agentHealth, width = 15)
       
        self.subFrame3c2.create_rectangle(20, 95, 219, 150, fill="white", outline="white")
        self.add_Healing_potion(self.subFrame3c2, 0.12, 20, 95, self.program.numPotion)
        self.add_Wumpus_Kill(self.subFrame3c2, 0.27, 100, 95,  getNumDeadWumpus(self.program))

        self.subFrame3c2.create_rectangle(100, 150, 170, 180, fill="white", outline="white")
        _ = self.getTotalScore()
        self.subFrame3c2.create_text(135, 165,  text=f"{self.score}", font =("Arial", 18), fill="Red")

        x_soud = cur_agent[0][0] 
        y_soud = cur_agent[0][1]
        # 0: Up, 1: Right, 2: Down, 3: Left
        direction = cur_agent[2]
        self.draw_all_direction(self.subFrame3c2, 102, 267)
        if direction == 0:
            self.draw_up(self.subFrame3c2, 102, 267, color = 'red')
            x_soud -= 1
        elif direction == 1:
            self.draw_right(self.subFrame3c2, 102, 267, color = 'red')       
            y_soud += 1
        elif direction == 2:
            self.draw_down(self.subFrame3c2, 102, 267, color = 'red')
            x_soud += 1
        elif direction == 3:
            self.draw_left(self.subFrame3c2, 102, 267, color = 'red')
            y_soud -= 1

        if self.program.isSound:
            kwargs[0].create_text( y_soud*65, x_soud*65, text = "Grraaahh!", fill = "red", font = ('Courier', 18, 'bold'), anchor='nw')

        if len(self.listCells) <= 1:
            kwargs[1].pack(pady = (5, 5))
            kwargs[2].pack_forget()
        if not len(self.listRemainCells) == 0:
            kwargs[3].pack_forget()
            kwargs[4].pack_forget()
            kwargs[4].pack(pady = (5, 5))
        else:
            kwargs[3].pack_forget()
            kwargs[4].pack_forget()
            kwargs[3].pack(pady = (5, 5))
            
    def nextMap(self, isAuto = False, kwargs = []):
        self.curNumState = self.curNumState + 1
        curStep = "Iteration: " + str(self.curNumState)
        if isAuto:
            self.clearCanvas(kwargs[2])
            kwargs[2].create_text(110, 22, text = curStep, fill = "black", font = self.font2)
        else:
            self.clearCanvas(kwargs[5])
            kwargs[5].create_text(110, 22, text = curStep, fill = "black", font = self.font2)
        
        # cur = (0, 0)
        if len(self.listRemainCells) > 0:
            cur = self.listRemainCells.pop(0)
            self.listCells.append(cur)
            
        self.clearCanvas(kwargs[0])

        if not self.isNext:
            self.tempCells.clear()
            self.isNext = True

        cur_agent = self.listCells[len(self.listCells)-1]
        while self.tempCells:
            action = self.tempCells[0]
            self.program.handleNextAction(action[1], action[0])
            self.tempCells.pop(0)
            
        print(cur_agent[1])
        if cur_agent[1] in ['shoot', 'grab', 'climb', 'heal']:
            self.tempCells.append(cur_agent)
        else:
            self.program.handleNextAction(cur_agent[1], cur_agent[0])
        
        
        self.draw_map(kwargs[0])

        # cols = 10
        # rows = 50
        # cell_size = 20
        # for i in range(rows):
        #     for j in range(cols):
        #         x1 = j * cell_size
        #         y1 = i * cell_size
        #         x2 = x1 + cell_size
        #         y2 = y1 + cell_size
        #         self.subFrame3c2.create_rectangle(x1, y1, x2, y2, fill="", outline="black")

        self.draw_HP(self.subFrame3c2, 10, 78, 190, HP = self.program.agentHealth, width = 15)

        self.subFrame3c2.create_rectangle(0, 95, 219, 150, fill="white", outline="white")
        self.add_Healing_potion(self.subFrame3c2, 0.12, 20, 95, self.program.numPotion)
        self.add_Wumpus_Kill(self.subFrame3c2, 0.27, 100, 95, getNumDeadWumpus(self.program))

        self.subFrame3c2.create_rectangle(100, 150, 170, 180, fill="white", outline="white")
        _ = self.getTotalScore()
        self.subFrame3c2.create_text(135, 165,  text=f"{self.score}", font =("Arial", 18), fill="Red")
        
        x_soud = cur_agent[0][0] 
        y_soud = cur_agent[0][1]
        # 0: Up, 1: Right, 2: Down, 3: Left
        direction = cur_agent[2]
        self.draw_all_direction(self.subFrame3c2, 102, 267)
        if direction == 0:
            self.draw_up(self.subFrame3c2, 102, 267, color = 'red')
            x_soud -= 1
        elif direction == 1:
            self.draw_right(self.subFrame3c2, 102, 267, color = 'red')       
            y_soud += 1
        elif direction == 2:
            self.draw_down(self.subFrame3c2, 102, 267, color = 'red')
            x_soud += 1
        elif direction == 3:
            self.draw_left(self.subFrame3c2, 102, 267, color = 'red')
            y_soud -= 1

        if self.program.isSound:
            kwargs[0].create_text( y_soud*65, x_soud*65, text = "Grraaahh!", fill = "red", font = ('Courier', 18, 'bold'), anchor='nw')

        if self.program.isGameWin:
            # kwargs[0].create_rectangle(3*65-9, 4*65-9, 7*65+9, 6*65+9, fill="white", outline="white")
            self.add_You_won(kwargs[0], 0.1, 3*65 + 5, 3*65 + 5)

        if not isAuto:
            if not len(self.listCells) == 0:
                kwargs[1].pack_forget()
                kwargs[2].pack(pady = (5, 5))
            if len(self.listRemainCells) == 0:
                kwargs[4].pack_forget()
                kwargs[3].pack(pady = (5, 5))
            else:
                kwargs[3].pack_forget()
                kwargs[4].pack_forget()
                kwargs[4].pack(pady = (5, 5))
           
        else:
            if len(self.listRemainCells) != 0:
                temp = kwargs
                curid = kwargs[1].after(self.autoRunTime[1][self.autoRunTime[0]], lambda: self.nextMap(isAuto = True, kwargs = temp))
                self.idAfter.add(curid)

    def add_You_won(self,canvas, image_size = 1, x=0, y=0):
        image_path = "GUI_imagine/You_won.png"
        image = Image.open(image_path)

        original_width, original_height = image.size

        scale_factor = image_size

        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)

        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        photo = ImageTk.PhotoImage(resized_image)
        self.images.append(photo)  

        canvas.create_image(x , y, anchor='nw', image=photo)
        canvas.image = photo

    def clearCanvas(self, canvas):
        for item in canvas.find_all():
            canvas.delete(item)

    def move1Item(self, listA, listB):
        listB.append(listA.pop(0))
    
    def slowDownFunc(self, kwargs = []):
        if self.autoRunTime[0] > 1:
            self.autoRunTime[0] = self.autoRunTime[0] - 1
        if self.autoRunTime[0] == 1:
            kwargs[0].pack_forget()
            kwargs[1].pack(pady = (5, 5))  
        if self.autoRunTime[0] != len(self.autoRunTime[1]):
            kwargs[2].pack_forget()
            kwargs[3].pack_forget()
            kwargs[2].pack(pady = (5, 5))  
        else:
            kwargs[2].pack_forget()
            kwargs[3].pack_forget()
            kwargs[3].pack(pady = (5, 5))    
    
    def speedUpFunc(self, kwargs = []):
        if self.autoRunTime[0] < len(self.autoRunTime[1]):
            self.autoRunTime[0] = self.autoRunTime[0] + 1
        if self.autoRunTime[0] != 1:
            kwargs[1].pack_forget()
            kwargs[0].pack(pady = (5, 5))  
        if self.autoRunTime[0] == len(self.autoRunTime[1]):
            kwargs[2].pack_forget()
            kwargs[3].pack_forget() 
            kwargs[3].pack(pady = (5, 5)) 
        else:
            kwargs[2].pack_forget()
            kwargs[3].pack_forget() 
            kwargs[2].pack(pady = (5, 5)) 

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
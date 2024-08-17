import tkinter as tk
import file
from Program import *
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

        self.fileName = ""
        self.idAfter = set()
        self.map = [[0]]
        self.isSolvable = True
        
        self.isHead = True
        self.isTail = False
        self.isResetList = True
        
        self.curNumState = 0
        self.listCells = []
        self.listRemainCells = [[(0, 1), 'move forward', 0], [(1, 1), 'move forward', 0], [(1, 2), 'turn right', 1], [(1, 2), 'shoot', 1]]

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
        elif file.checkOpenFile(self.fileName) == False:
            self.entry.delete("1.0", tk.END)
            self.entry.insert("1.0", self.text2)  
            self.entry.mark_set("insert", "1.0")
        else:
            resultRead = file.readF(self.fileName)
            self.col = len(resultRead[0])
            self.row = len(resultRead)
            # self.mapPercepts = Program.getAllPercepts
            program = Program("test.txt")
            self.mapPercepts = getAllPercepts(program)
            self.mapElements = getAllElements(program)
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
                canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")

        for cell in self.listCells:
            canvas.create_rectangle(cell[0][0]*cell_size, cell[0][1]*cell_size, (cell[0][0]+1)*cell_size, (cell[0][1]+1)*cell_size, fill="#BBBBBB", outline="black")

        hht = rows * cell_size
        wth = cols * cell_size

        canvas.create_line([(2, 0), (2, hht)], fill='black')
        canvas.create_line([(wth, 0), (wth, hht)], fill='black')
        canvas.create_line([(0, 2), (wth, 2)], fill='black')
        canvas.create_line([(0, hht), (wth, hht)], fill='black')

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
    
    def drawElements(self, canvas):
        # filePath = ["test/wumpus.jpg", "test/pit.jpg", "test/poisonGas.jpg","test/healing.jpg", "test/gold.jpg"]
        # filePath = ["wumpus.png", "test/2.png", "test/3.png", "test/4.png", "test/5.png"]
        TEXT = ["W", 'P', 'G', 'H', 'T']
        for i in range(10):
            for j in range(10):
                for k in range(5):
                    if self.mapElements[i][j][k]:
                        # self.add_image(canvas, filePath[k], i, j, 20, 19 + (22 if k%2 else 0), 4 +(20* int(k/2)) )
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
        self.create_grid(canvas, self.row, self.col, self.cell_size)
        self.drawPercepts(canvas)
        self.drawElements(canvas)
        curPos = self.listCells[len(self.listCells)-1]
        self.add_image(canvas, "asd.jpg", curPos[0][1], curPos[0][0], 18, 41, 44)

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
        
        self.isResetList = True
        self.isHead = True
        self.isTail = False
        self.unshowAllFrames()
        self.root.title("Choose view frame")
        self.frame2.pack(expand=True, anchor='center')  
        self.clearFrame(self.frame2) 
        # self.move2DContent(self.listCells, self.listRemainCells)
        self.chooseViewFrame()

    def showFrame3(self, isAuto = False):
        self.unshowAllFrames()
        self.root.title("Step by step")
        self.frame3.pack(expand=True, anchor='center')
        
        self.moveContent(self.listCells, self.listRemainCells)
        self.move1Item(self.listRemainCells, self.listCells)
        
        self.clearFrame(self.frame3)  
        self.curNumState = 0
        self.stepByStepFrame(isAuto)

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
            self.prevBtn2 = tk.Button(self.subFrame3a, text = "Previous", command = lambda: self.prevMap(kwargs = [self.subFrame3b, self.prevBtn1, self.prevBtn2, self.nextBtn1, self.nextBtn2, self.subFrame3c1]), bg = "#323232", fg = "#FAFAFA", width = 20, height = 2, cursor = "hand2")
            self.prevBtn1.pack(pady = (5, 5)) 
                
            self.nextBtn1 = tk.Button(self.subFrame3a, state = "disabled", text = "Next", bg = "lightgray", fg = "white", width = 20, height = 2)
            self.nextBtn2 = tk.Button(self.subFrame3a, text = "Next", command = lambda: self.nextMap(isAuto = False, kwargs = [self.subFrame3b, self.prevBtn1, self.prevBtn2, self.nextBtn1, self.nextBtn2, self.subFrame3c1]), bg = "#323232", fg = "#FAFAFA", width = 20, height = 2, cursor = "hand2")
            self.nextBtn2.pack(pady = (5, 5))
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
        self.subFrame3b.pack(side = tk.LEFT, expand=True, anchor='center', pady = (0, 30), padx = (0, 15))  
        
        self.draw_map(self.subFrame3b)

        ### Sub frame 3 c
        self.subFrame3c = tk.Frame(self.frame3)
        self.subFrame3c.pack(side = tk.LEFT,expand=True, anchor='center', padx = (5, 25))    

        ### Sub frame 3 c1
        self.subFrame3c1 = tk.Canvas(self.subFrame3c, bg = "white", width = 200, height = self.height * 0.1)
        self.subFrame3c1.pack(anchor='center', padx = (25, 5))

        ### Sub frame 3 c2
        self.subFrame3c2 = tk.Canvas(self.subFrame3c, bg = "white", width = 200, height = self.height * 0.6)
        self.subFrame3c2.pack(anchor='center', padx = (25, 5))  

        ## Cur state
        curStep = "Iteration: " + str(self.curNumState)
        self.subFrame3c1.pack( expand=True, anchor='center')     
        self.subFrame3c1.create_text(100, 30, text = curStep, fill = "black", font = self.font2)

        ## Percepts
        perTitle = "Percepts:"
        self.subFrame3c2.pack( expand=True, anchor='center')     
        self.subFrame3c2.create_text(100, 20, text = perTitle, fill = "black", font = self.font2)

        ## Percepts 1
        perA = "Stench"
        self.subFrame3c2.pack( expand=True, anchor='center', pady = (100, 0))
        self.draw_dot(self.subFrame3c2, 0.85, 0.05, "#3CB371", 5.5, 9, 10)     
        self.subFrame3c2.create_text(50, 65, text = perA, fill = "black", font = self.font3)

        ## Percepts 1
        perA = "Breeze"
        self.subFrame3c2.pack( expand=True, anchor='center', pady = (100, 0))  
        self.draw_dot(self.subFrame3c2, 0.625, 1.6, "#8EE5EE", 5.5, 9, 25)  
        self.subFrame3c2.create_text(150, 65, text = perA, fill = "black", font = self.font3)

        ## Percepts 2
        perA = "Whiff"
        self.subFrame3c2.pack( expand=True, anchor='center', pady = (100, 0)) 
        self.draw_dot(self.subFrame3c2, 0.85, 0.05, "#8E388E", 5.5, 9, 40)    
        self.subFrame3c2.create_text(50, 95, text = perA, fill = "black", font = self.font3)

        ## Percepts 2
        perA = "Glow"
        self.subFrame3c2.pack( expand=True, anchor='center', pady = (100, 0))
        self.draw_dot(self.subFrame3c2, 0.625, 1.6, "#FFF68F", 5.5, 9, 55)     
        self.subFrame3c2.create_text(150, 95, text = perA, fill = "black", font = self.font3)

        ## Objects
        objTitle = "Objects:"
        self.subFrame3c2.pack( expand=True, anchor='center')     
        self.subFrame3c2.create_text(100, 150, text = objTitle, fill = "black", font = self.font2)

        ## Objects 1
        objA = "Wumpus"
        self.subFrame3c2.pack( expand=True, anchor='center', pady = (100, 0))
        self.subFrame3c2.create_text(20, 190,  text='W', font=("Arial", 15), fill="Red")
        self.subFrame3c2.create_text(72, 190, text = objA, fill = "black", font = self.font3)

        ## Objects 1
        objA = "Pit"
        self.subFrame3c2.pack( expand=True, anchor='center', pady = (100, 0))
        self.subFrame3c2.create_text(120, 190,  text='P', font=("Arial", 15), fill="Red")
        self.subFrame3c2.create_text(145, 190, text = objA, fill = "black", font = self.font3)

        ## Objects 2
        objA = "Poison"
        self.subFrame3c2.pack( expand=True, anchor='center', pady = (100, 0))
        self.subFrame3c2.create_text(20, 220,  text='G', font=("Arial", 15), fill="Red")
        self.subFrame3c2.create_text(65, 220, text = objA, fill = "black", font = self.font3)

        ## Objects 2
        objA = "Health"
        self.subFrame3c2.pack( expand=True, anchor='center', pady = (100, 0))
        self.subFrame3c2.create_text(120, 220,  text='H', font=("Arial", 15), fill="Red")
        self.subFrame3c2.create_text(160, 220, text = objA, fill = "black", font = self.font3)

        ## Objects 3
        objA = "Treasure (Gold)"
        self.subFrame3c2.pack( expand=True, anchor='center', pady = (100, 0))
        self.subFrame3c2.create_text(20, 250,  text='T', font=("Arial", 15), fill="Red")
        self.subFrame3c2.create_text(100, 250, text = objA, fill = "black", font = self.font3)

        if isAuto:
            curID = self.root.after(self.autoRunTime[1][self.autoRunTime[0]], lambda: self.nextMap(isAuto = True, kwargs = [self.subFrame3b, self.subFrame3a, self.subFrame3c1]))
            self.idAfter.add(curID)

    def prevMap(self, kwargs = []):
        self.curNumState = self.curNumState - 1
        curStep = "Iteration: " + str(self.curNumState)
        self.clearCanvas(kwargs[5])
        kwargs[5].create_text(100, 30, text = curStep, fill = "black", font = self.font2)
            
        cur = (0, 0)
            
        if len(self.listCells) >= 2:
            cur = self.listCells.pop()
            self.listRemainCells.insert(0, cur)
            
        self.clearCanvas(kwargs[0])
        self.draw_map(kwargs[0])
        
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
            kwargs[2].create_text(100, 30, text = curStep, fill = "black", font = self.font2)
        else:
            self.clearCanvas(kwargs[5])
            kwargs[5].create_text(100, 30, text = curStep, fill = "black", font = self.font2)
        
        # cur = (0, 0)
        if len(self.listRemainCells) > 0:
            cur = self.listRemainCells.pop(0)
            self.listCells.append(cur)
            
        self.clearCanvas(kwargs[0])
        self.draw_map(kwargs[0])
            
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
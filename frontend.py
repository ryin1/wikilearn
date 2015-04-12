import math
import eventBasedAnimation
from app import *
import code
import webbrowser

class Graph(object):
    def __init__(self, lst, x, y, r, centerTxt):
        self.x, self.y, self.r = x, y, r
        self.centerTxt = centerTxt #text for the center 
        self.numNodes = len(lst)
        self.angle = math.radians(360/self.numNodes)
        self.nodes = []
        self.step = 0
        self.createNodes(lst)

        for node in self.nodes:
            print('{}: txt, {}: message'.format(node.txt, node.message))


    def createNodes(self, lst):
        for nodeIndex in range(len(lst)):
            r = float(self.r)/2 + lst[nodeIndex][1]*self.r
            linkLength = 3*r
            x = self.x+linkLength*math.cos(self.angle*nodeIndex+math.radians(self.step))
            y = self.y+linkLength*math.sin(self.angle*nodeIndex+math.radians(self.step))
            fillcolor = "black" if (nodeIndex%2==1) else "dark orange"
            txtcolor = "white" if (nodeIndex%2==1) else "black"

            message = lst[nodeIndex][2]
            url = lst[nodeIndex][3]
            self.nodes.append(Node(x,y,r,lst[nodeIndex][0],fillcolor,txtcolor,message,url))

    def rotate(self):
        self.step = (self.step + 1) % 360
        linkLength = 5*self.r
        for nodeIndex in range(len(self.nodes)):
            x = self.x+linkLength*math.cos(self.angle*nodeIndex+math.radians(self.step))
            y = self.y+linkLength*math.sin(self.angle*nodeIndex+math.radians(self.step))
            self.nodes[nodeIndex].x, self.nodes[nodeIndex].y = x, y

    def draw(self, canvas):
        canvas.create_rectangle(0,0,1000,800,fill='lightblue')
        linkLength = 5*self.r
        for node in self.nodes:
            canvas.create_line(self.x,self.y,node.x,node.y)
            node.draw(canvas)
        canvas.create_oval(self.x-self.r,self.y-self.r,self.x+self.r,self.y+self.r,fill="grey")
        canvas.create_text(self.x,self.y,text=self.centerTxt)


class Node(object):
    def __init__(self, x, y, r, txt, fillcolor, txtcolor, message, url):
        self.x, self.y, self.r = x, y, r
        self.txt = txt
        self.step = 0
        self.fillcolor = fillcolor
        self.txtcolor = txtcolor
        self.message = message
        self.url = url
        self.box = False

    def clicked(self, x, y):
        if ((x-self.x)**2+(y-self.y)**2)**0.5 <= self.r:
            webbrowser.open(self.url)
            #fill this in once decided what todo

    def hover(self, x, y):
        self.step=0
        if ((x-self.x)**2+(y-self.y)**2)**0.5 <= self.r:
            self.box = True
            return
        self.box = False

    def draw(self, canvas):
        canvas.create_oval(self.x-self.r,self.y-self.r,self.x+self.r,self.y+self.r,fill=self.fillcolor)
        approxCircleLen = 6
        margin = 12
        row = 0
        titleList = (self.txt).split()
        title = ""
        for i in range(len(titleList)):
            if i == len(titleList)-1:
                if row >= 3:
                    row -= 1
                if row == 0:
                    row = 0
                title += titleList[i]
                canvas.create_text(self.x,self.y+(row)*margin,text=str(title),fill=self.txtcolor)
            elif len(title) + len(titleList[i]) < approxCircleLen:
                title += titleList[i] + ' '
            else:
                title += titleList[i]
                canvas.create_text(self.x,self.y+(row)*margin,text=str(title),fill=self.txtcolor)
                row += 1
                title = ""
        if self.box == True:
            boxWidth, boxHeight = 200, 80
            boxFont = "Arial 12 bold"
            approxLen = 60
            margin = 25
            counter=0
            row=''
            splitMessage=self.message.split()
            canvas.create_rectangle(self.x-boxWidth,self.y-boxHeight,self.x+boxWidth,self.y+boxHeight,fill="grey")
            index = 0
            for i in splitMessage:
                if index==0:
                    if len(self.message)/approxLen>=4:
                        counter-=1
                if index == len(splitMessage)-1:
                    if counter==0:
                        counter=1
                    row += i 
                    canvas.create_text(self.x,self.y+margin*(counter-1),text=row,font=boxFont)
                    break
                if len(row)+len(i)+1<approxLen:
                    j = i + ' '
                    row += j
                else:
                    row+=i+ ' '
                    canvas.create_text(self.x,self.y+margin*(counter-1),text=row,font=boxFont)
                    row=''
                    counter+=1
                index += 1
                 #   if len(splitMessage)==0:
                 #       canvas.create_text(self.x,self.y+counter*margin-60,font=row)
                #        break
                #counter+=1
            
            


class Display(eventBasedAnimation.Animation):
    def onInit(self):
        pass

    def onMouse(self, event):
        for graph in self.graphs:
            for node in graph.nodes:
                node.clicked(event.x,event.y)

    def onMouseMove(self, event):
        for graph in self.graphs:
            for node in graph.nodes:
                node.hover(event.x, event.y)

    def onStep(self):
        for graph in self.graphs:
            graph.rotate()

    def onDraw(self,canvas):
        for graph in self.graphs:
            graph.draw(canvas)


import tkinter as tk
from tkinter import *
import string

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)            
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        self.master.geometry(self._geom)
        self._geom=geom

def keyReleased(event):
    canvas = event.widget.canvas
    ignore=[ "BackSpace", "Return", "Shift_L", "Shift_R", "Control_L", "Control_R", "Caps_Lock", "Tab", 'semicolon','quoteright','quoteleft','colon','period','comma','Alt_L','App','Left','Right','Down','Up','backslash','bracketright','bracketleft','braceleft','braceright','equal','plus','minus','underscore','parenright','parenleft','asterisk','ampersand','at','dollar','percent','exclam','asciitilde','asciicircum','asciicircumpercent','tab','F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12','Alt_L','numbersign','less','greater','bar','slash','question','quotedbl','Pause','Insert','Delete','Escape','Win_L'] 
    if event.keysym in string.ascii_letters or event.keysym=='space' and canvas.condition==False and canvas.pressed==True:
        if event.keysym=='space':
            canvas.message+=' '
        else:
            canvas.message+=event.keysym
        return redrawAll(canvas)
    if event.keysym == 'BackSpace' and canvas.condition==False:
        if len(canvas.message)!=0:
            canvas.message=canvas.message[:len(canvas.message)-1]
        return redrawAll(canvas)
    if event.keysym == 'Return' and canvas.condition==False:
        learning(canvas)
        canvas.boxes=[canvas.message]
        return drawStateTwo(canvas)

def leftMousePressed(event):
    canvas = event.widget.canvas
    x,y=event.x,event.y
    if inSearchBox(x,y):
        canvas.pressed=False
        canvas.pressed=True
        canvas.message=''
        canvas.boxes=[]
        return redrawAll(canvas)

def inBox(x,y):
    if 200<=x<=800 and 250<=y<=650:
        return True
    return False
    
def drawBoxes(canvas):
    if canvas.condition==True:
        return drawStateTwo(canvas)
    else:
        return drawStateOne(canvas)
    
def inSearchBox(x,y):
    if 200<=x<=800 and 100<=y<=150:
        return True
    return False

def drawStateOne(canvas):
    #width/5,width/10,height+300,width/8
    canvas.create_rectangle(200,100,800,150)
    font2=("Arial",14)
    canvas.create_text(500,125,text=canvas.message,font=font2)
    if len(canvas.boxes)==1:
        canvas.create_rectangle(200,250,800,650,)
        msg=canvas.boxes[0]
        #width/2,width/2-50        
        font1=("Arial",40,"bold")
        if len(msg)>14:
            for i in range(len(msg)/15):
                if i==len(msg)/15:
                    canvas.create_text(500,400+i*50,text=msg[i*15:],font=font1)
                else:
                    canvas.create_text(500,400+i*50,text=msg[0+i*15:15+i*15],font=font1)
        #width/2,width/8
        
            
def drawStateTwo(canvas):
    #canvas.message is the string that they will search
    #take in canvas.message into your function and return list to pass into display
    title, origin_url, urls, count = setup(canvas.message)
    disp = Display(width=1000,height=800)
    disp.graphs=[]
    disp.lst = rank_links(origin_url, urls, count)[0]
    graph1 = Graph(disp.lst, 500, 400, 60, title)
    disp.graphs.append(graph1)
    disp.run()
    
def learning(canvas):
    canvas.create_text(canvas.width/2, canvas.height/2, text="Processing/scraping data...")


def redrawAll(canvas):
    canvas.delete(ALL)
    #canvas.create_rectangle(-100,-100,1100,1100,fill='lightblue')
    font = ("Arial", 16, "bold")
    if canvas.condition==False:
        msg="What would you like to learn about today?"
    canvas.create_text(canvas.width/2,50,text=msg,font=font)
    drawBoxes(canvas)
    
def init(canvas):
    canvas.pressed=False
    canvas.message=''
    canvas.boxes=[]
    canvas.condition=False
    canvas.width=1000
    canvas.height=1000
    redrawAll(canvas)
    
def run():
    #root=tk.Tk()
    #app=FullScreenApp(root)
    root=Tk()
    canvas=Canvas(root,width=1000,height=1000)
    canvas.pack()
    root.canvas = canvas.canvas = canvas
    init(canvas)
    root.bind("<KeyRelease>",keyReleased)
    root.bind("<Button-1>",leftMousePressed)

    T = Text(root, height=5, width=15)
    T.pack()
    mainloop()
    
    root.mainloop()

run()





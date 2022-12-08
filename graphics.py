from tkinter import *
import time

# create cells for graph
def createGraph(root, graphNum, graphs, actions, points):
    if 'my_canvas' in locals():
        my_canvas.delete('all')
    graphNum = int(graphNum.get()) - 1
    my_canvas = Canvas(root, height=1500, width=1500, bg="white")

    #control simulation buttons
    label = Label(root, width=50, text="Select Ground Truth Path #1-10")
    entry = Entry(root, width=50)
    simOne = Button(root, width=20, text="Next Step", command= lambda: nextPoint(my_canvas, points, 1, entry, graphNum))
    simTen = Button(root, width=20, text="Next 10 Steps", command= lambda: nextPoint(my_canvas, points, 10, entry, graphNum))
    simEnd = Button(root, width=20, text="To End", command= lambda: nextPoint(my_canvas, points, 100, entry, graphNum))
    label.pack()
    entry.pack()
    simOne.pack()
    simTen.pack()
    simEnd.pack()

    my_canvas.pack(pady=20)
    
    #create cells
    for x in range(100):
        for y in range(50):
            tempx = x + 20
            tempy = y + 10
            if(x == 0 and y == 0):
                print(tempx*10, tempy*10)
            # fill cells with color based on type
            if(graphs[graphNum][x][y] == 'H'):
                my_canvas.create_rectangle(tempx*10, tempy*10, (tempx+1)*10, (tempy+1)*10, outline='grey', fill='green')
            if(graphs[graphNum][x][y] == 'T'):
                my_canvas.create_rectangle(tempx*10, tempy*10, (tempx+1)*10, (tempy+1)*10, outline='grey', fill='orange')
            if(graphs[graphNum][x][y] == 'B'):
                my_canvas.create_rectangle(tempx*10, tempy*10, (tempx+1)*10, (tempy+1)*10, outline='grey', fill='red')
            else:
                my_canvas.create_rectangle(tempx*10, tempy*10, (tempx+1)*10, (tempy+1)*10, outline='grey')
    
    return
    

counter = 0
# simulate ground truth points
def nextPoint(my_canvas, points, simStep, simNum, graphNum):
    global counter
    if not isinstance(simNum, int):
        simNum = int(simNum.get()) - 1
    if(simStep == 1):
        x1 = ((points[graphNum][simNum][counter][0])+20.25)*10
        y1 = ((points[graphNum][simNum][counter][1])+10.25)*10
        x2 = ((points[graphNum][simNum][counter][0])+20.75)*10
        y2 = ((points[graphNum][simNum][counter][1])+10.75)*10 
        my_canvas.create_oval(x1, y1, x2, y2, fill='purple')
        counter+=1
        return
    elif(simStep == 10):
        temp = counter
        while temp < counter+11 and temp < 100:
            x1 = ((points[graphNum][simNum][temp][0])+20.25)*10
            y1 = ((points[graphNum][simNum][temp][1])+10.25)*10
            x2 = ((points[graphNum][simNum][temp][0])+20.75)*10
            y2 = ((points[graphNum][simNum][temp][1])+10.75)*10 
            my_canvas.create_oval(x1, y1, x2, y2, fill='purple')
            temp+=1
        counter+=10
        return
    elif(simStep == 100):
        temp = counter
        while temp < 100:
            x1 = ((points[graphNum][simNum][temp][0])+20.25)*10
            y1 = ((points[graphNum][simNum][temp][1])+10.25)*10
            x2 = ((points[graphNum][simNum][temp][0])+20.75)*10
            y2 = ((points[graphNum][simNum][temp][1])+10.75)*10 
            my_canvas.create_oval(x1, y1, x2, y2, fill='purple')
            temp+=1
        counter+=100
        return



def graphics(graphs, points, actions):
    root = Tk()
    root.title('Part 5')
    root.geometry("500x500")
    #create entry and button for graph selection
    label = Label(root, width=100, text="normal: white, highway: green, hard to traverse: orange, blocked: red")
    label2 = Label(root, width=50, text="pick a graph file #1-10")
    graph = Entry(root, width=50)
    button = Button(root, width=20, text="Create Graph", command= lambda: createGraph(root, graph, graphs, actions, points))
    label.pack()
    label2.pack()
    graph.pack()
    button.pack()
    root.mainloop()
from tkinter import *

def createGraph(root, graphNum, graphs):
    graphNum = int(graphNum.get()) - 1
    #if(graphNum > 10 or graphNum < 1):
    #   print("no graph at that value")
    #    root.withdraw()
    #    graphics(graphs)
    #else:
    my_canvas = Canvas(root, height=1500, width=1500, bg="white")
    my_canvas.pack(pady=20)
    for x in range(100):
        for y in range(50):
            #if(graphs[graphNum][x][y] == N):
            tempx = x + 20
            tempy = y + 10
            if(graphs[graphNum][y][x] == 'H'):
                my_canvas.create_rectangle(tempx*10, tempy*10, (tempx+1)*10, (tempy+1)*10, outline='grey', fill='green')
            if(graphs[graphNum][y][x] == 'T'):
                my_canvas.create_rectangle(tempx*10, tempy*10, (tempx+1)*10, (tempy+1)*10, outline='grey', fill='orange')
            if(graphs[graphNum][y][x] == 'B'):
                my_canvas.create_rectangle(tempx*10, tempy*10, (tempx+1)*10, (tempy+1)*10, outline='grey', fill='red')
            else:
                my_canvas.create_rectangle(tempx*10, tempy*10, (tempx+1)*10, (tempy+1)*10, outline='grey')

def graphics(graphs):
    root = Tk()
    root.title('Part 5')
    root.geometry("500x500")
    #creat entry and button for graph selection
    label = Label(root, width=100, text="normal: white, highway: green, hard to traverse: orange, blocked: red")
    label2 = Label(root, width=50, text="pick a graph file #1-10")
    graph = Entry(root, width=50)
    button = Button(root, width=20, text="Create Graph", command= lambda: createGraph(root, graph, graphs))
    label.pack()
    label2.pack()
    graph.pack()
    button.pack()
    root.mainloop()
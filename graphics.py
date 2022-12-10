from tkinter import *
import time

#create cells for graph
def createGraph(root, graphNum, graphs, actions, points, readings):
    global prevProbs, currProbs
    #convert graphNum input to integer
    graphNum = int(graphNum.get()) - 1

    #initialize the prevProbs array based on graphNum (creating equal probabilities without knowledge of start location)
    openCount = 0
    for x in range(100):
        for y in range(50):
            if not (graphs[graphNum][x][y] == 'B'):
                openCount+=1
    startProb = 1/openCount
    for x in range(100):
        for y in range(50):
            if not (graphs[graphNum][x][y] == 'B'):
                prevProbs[x][y] = startProb
            else:
                prevProbs[x][y] = 0

    #reset the canvas
    if 'my_canvas' in locals():
        my_canvas.delete('all')
    
    #initialize canvas
    my_canvas = Canvas(root, height=1500, width=1500, bg="white")

    #control simulation buttons
    label = Label(root, width=50, text="Select Ground Truth Path #1-10")
    entry = Entry(root, width=50)
    simOne = Button(root, width=20, text="Next Step", command= lambda: nextPoint(my_canvas, points, 1, entry, graphNum, actions, readings, graphs))
    simTen = Button(root, width=20, text="Next 10 Steps", command= lambda: nextPoint(my_canvas, points, 10, entry, graphNum, actions, readings, graphs))
    simEnd = Button(root, width=20, text="To End", command= lambda: nextPoint(my_canvas, points, 100, entry, graphNum, actions, readings, graphs))
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
            # fill cells with color based on starting probability
            if(prevProbs[x][y] == 0):
                my_canvas.create_rectangle(tempx*10, tempy*10, (tempx+1)*10, (tempy+1)*10, outline='grey')
            elif(prevProbs[x][y] >= .01):
                my_canvas.create_rectangle(tempx*10, tempy*10, (tempx+1)*10, (tempy+1)*10, outline='grey', fill='#940000')
            elif(prevProbs[x][y] >= .004):
                my_canvas.create_rectangle(tempx*10, tempy*10, (tempx+1)*10, (tempy+1)*10, outline='grey', fill='#941e00')
            elif(prevProbs[x][y] >= .002):
                my_canvas.create_rectangle(tempx*10, tempy*10, (tempx+1)*10, (tempy+1)*10, outline='grey', fill='#943900')
            elif(prevProbs[x][y] >= .0002):
                my_canvas.create_rectangle(tempx*10, tempy*10, (tempx+1)*10, (tempy+1)*10, outline='grey', fill='#947400')
            else:
                my_canvas.create_rectangle(tempx*10, tempy*10, (tempx+1)*10, (tempy+1)*10, outline='grey', fill='#c7c263')
    
    return
    

#calculate previous prob * transition model
def tranModel(action, left, up, right, down, graph, x, y):
    tranProb = 0
    if(graph[x][y] == 'B'):
        return 0
    
    #left action
    if(action == 'L'):
        if (left == 0 and right == 1):
            tranProb = prevProbs[x][y] + ((prevProbs[x+1][y])*.9)
        elif(left == 0 and right == 0):
            tranProb = prevProbs[x][y]
        elif(left == 1 and right == 0):
            tranProb = prevProbs[x][y]*.1
        else:
            tranProb = (prevProbs[x][y]*.1) + (prevProbs[x+1][y]*.9)
    
    #right action
    elif(action == 'R'):
        if (left == 0 and right == 1):
            tranProb = prevProbs[x][y]*.1
        elif(left == 0 and right == 0):
            tranProb = prevProbs[x][y]
        elif(left == 1 and right == 0):
            tranProb = prevProbs[x][y] + (prevProbs[x-1][y]*.9)
        else:
            tranProb = (prevProbs[x][y]*.1) + (prevProbs[x-1][y]*.9)

    #up action
    elif(action == 'U'):
        if(up == 1 and down == 1):
            tranProb = (prevProbs[x][y]*.1) + (prevProbs[x][y+1]*.9)
        elif(up == 0 and down == 0):
            tranProb = prevProbs[x][y]
        elif(up == 1 and down == 0):
            tranProb = prevProbs[x][y]*.1
        else:
            tranProb = prevProbs[x][y] + (prevProbs[x][y-1]*.9)
    
    #down action
    else:
        if(up == 1 and down == 1):
            tranProb = (prevProbs[x][y]*.1) + (prevProbs[x][y-1]*.9)
        elif(up == 0 and down == 0):
            tranProb = prevProbs[x][y]
        elif(up == 1 and down == 0):
            tranProb = prevProbs[x][y] + prevProbs[x][y-1]*.9
        else:
            tranProb = prevProbs[x][y]*.1

    return tranProb



def filtering(graphNum, simNum, actions, readings, graphs, counter):
    # get graph, actions and readings based on user inputted graphNum and simNum
    graph = graphs[graphNum]
    action = actions[graphNum][simNum][counter]
    reading = readings[graphNum][simNum][counter]


    # calculate probability for each cell
    for x in range(100):
        for y in range(50):
            # calculate probability based on action and location

            # determine openings around given cell
            left = 1
            up = 1
            right = 1
            down = 1
            if(x == 0):
                left = 0
            if(x != 0):
                if graph[x-1][y] == 'B':
                    left = 0
            if(x == 99):
                right = 0
            if(x != 99):
                if(graph[x+1][y] == 'B'):
                    right = 0
            if(y == 0):
                up = 0
            if(y != 0):
                if(graph[x][y-1] == 'B'):
                    up = 0
            if(y == 49):
                down = 0
            if(y != 49):
                if(graph[x][y+1] == 'B'):
                    down = 0
            
            # calculate based on transition model
            tranProb = tranModel(action, left, up, right, down, graph, x, y)

            # calculate based on observation model
            observProb = 0
            if(reading == graph[x][y]):
                observProb = .9
            else:
                observProb = .1

            #combine
            totalProb = tranProb*observProb
            currProbs[x][y] = totalProb 

    #noramlize
    total = 0
    for x in range(100):
        for y in range(50):
            total+=currProbs[x][y]
    normFactor = 1/total
    #put normalized values back in currProbs
    for x in range(100):
        for y in range(50):
            currProbs[x][y] = normFactor*currProbs[x][y]
    return



# draw board
def drawBoard(my_canvas):
    my_canvas.delete("all")
    #create cells
    for x in range(100):
        for y in range(50):
            tempx = x + 20
            tempy = y + 10
            if(x == 0 and y == 0):
                print(tempx*10, tempy*10)
            # fill cells with color based on starting probability
            if(currProbs[x][y] == 0):
                my_canvas.create_rectangle(tempx*10, tempy*10, (tempx+1)*10, (tempy+1)*10, outline='grey')
            elif(currProbs[x][y] >= .5):
                my_canvas.create_rectangle(tempx*10, tempy*10, (tempx+1)*10, (tempy+1)*10, outline='grey', fill='#ff0303')
            elif(currProbs[x][y] >= .2):
                my_canvas.create_rectangle(tempx*10, tempy*10, (tempx+1)*10, (tempy+1)*10, outline='grey', fill='#ff3103')
            elif(currProbs[x][y] >= .01):
                my_canvas.create_rectangle(tempx*10, tempy*10, (tempx+1)*10, (tempy+1)*10, outline='grey', fill='#ff4f03')
            elif(currProbs[x][y] >= .001):
                my_canvas.create_rectangle(tempx*10, tempy*10, (tempx+1)*10, (tempy+1)*10, outline='grey', fill='#ff8103')
            elif(currProbs[x][y] >= .0001):
                my_canvas.create_rectangle(tempx*10, tempy*10, (tempx+1)*10, (tempy+1)*10, outline='grey', fill='#ffa703')
            else:
                my_canvas.create_rectangle(tempx*10, tempy*10, (tempx+1)*10, (tempy+1)*10, outline='grey', fill='#ffe603')

    return my_canvas



counter = 0
# keep track of previous and current filtering probabilites
prevProbs = [[0.0 for y in range(50)] for x in range(100)]
currProbs = [[0.0 for y in range(50)] for x in range(100)]

# simulate ground truth points
def nextPoint(my_canvas, points, simStep, simNum, graphNum, actions, readings, graphs):
    global counter, prevProbs, currProbs

    # convert user input for simulation number to integer
    if not isinstance(simNum, int):
        simNum = int(simNum.get()) - 1

    # simulate 1 step
    if(simStep == 1):
        # do filtering
        filtering(graphNum, simNum, actions, readings, graphs, counter)
        my_canvas = drawBoard(my_canvas)
        prevProbs = currProbs

        # draw oval
        x1 = ((points[graphNum][simNum][counter][0])+20.25)*10
        y1 = ((points[graphNum][simNum][counter][1])+10.25)*10
        x2 = ((points[graphNum][simNum][counter][0])+20.75)*10
        y2 = ((points[graphNum][simNum][counter][1])+10.75)*10 
        my_canvas.create_oval(x1, y1, x2, y2, fill='purple')
        counter+=1
        return
    # simulate 10 steps
    elif(simStep == 10):
        temp = counter
        while temp < counter+11 and temp < 100:
            # do filtering
            filtering(graphNum, simNum, actions, readings, graphs, temp)
            my_canvas = drawBoard(my_canvas)
            prevProbs = currProbs


            # draw oval
            x1 = ((points[graphNum][simNum][temp][0])+20.25)*10
            y1 = ((points[graphNum][simNum][temp][1])+10.25)*10
            x2 = ((points[graphNum][simNum][temp][0])+20.75)*10
            y2 = ((points[graphNum][simNum][temp][1])+10.75)*10
            my_canvas.create_oval(x1, y1, x2, y2, fill='purple')
            temp+=1
        counter+=10
        return
    # simulate through last action
    elif(simStep == 100):
        temp = counter
        while temp < 100:
            # do filtering
            filtering(graphNum, simNum, actions, readings, graphs, temp)
            my_canvas = drawBoard(my_canvas)
            prevProbs = currProbs

            # draw oval
            x1 = ((points[graphNum][simNum][temp][0])+20.25)*10
            y1 = ((points[graphNum][simNum][temp][1])+10.25)*10
            x2 = ((points[graphNum][simNum][temp][0])+20.75)*10
            y2 = ((points[graphNum][simNum][temp][1])+10.75)*10 
            my_canvas.create_oval(x1, y1, x2, y2, fill='purple')
            temp+=1
        counter+=100
        print(max(map(max, prevProbs)))
        return


def graphics(graphs, points, actions, readings):
    root = Tk()
    root.title('Part 5')
    root.geometry("500x500")
    #create entry and button for graph selection
    label = Label(root, width=100, text="blocked cells are white, colors grow closer to red the higher the probability")
    label2 = Label(root, width=50, text="pick a graph file #1-10")
    graph = Entry(root, width=50)
    button = Button(root, width=20, text="Create Graph", command= lambda: createGraph(root, graph, graphs, actions, points, readings))
    label.pack()
    label2.pack()
    graph.pack()
    button.pack()
    root.mainloop()
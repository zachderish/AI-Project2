import random
import graphics

graphs = [[["0" for y in range (100)] for x in range(50)] for i in range(10)]


def genGraph():
    for i in range(10):
        for x in range(50):
            for y in range(100):
                num = random.random()
                if(num <= .5):
                    graphs[i][x][y] = "N"
                elif(num <= .7):
                    graphs[i][x][y] = "H"
                elif(num <= .9):
                    graphs[i][x][y] = "T"
                else:
                    graphs[i][x][y] = "B"


def reading(location):
    num = random.random()
    if location == 'N':
        if(num <= .9):
            return 'N'
        elif(num <= .5):
            return 'T'
        else:
            return 'H'
    elif location == 'H':
        if(num <= .9):
            return 'H'
        elif(num <= .5):
            return 'T'
        else:
            return 'N'
    else:
        if(num <= .9):
            return 'T'
        elif(num <= .5):
            return 'N'
        else:
            return 'H'


def nextMove():
    move = random.randint(1,4)
    moveOdds = random.random()
    if(moveOdds >= .9):
        move = 0
        return move
    else:
        return move

def sequence(start, j):
    readings = [None] * 100
    actions = [None] * 100
    sequence = [None] * 100
    for i in range(99):
        move = nextMove()
        #west move
        if (move == 1):
            actions[i] = 'L'
            if(start[0] == 0):
                sequence[i] = start
                readings[i] = graphs[j][start[0]][start[1]]
            elif (graphs[j][start[0]-1][start[1]] == 'B'):
                sequence[i] = start
                readings[i] = reading(graphs[j][start[0]][start[1]])
            else:
                sequence[i] = ((start[0]-1),start[1])
                readings[i] = reading(graphs[j][start[0]-1][start[1]])
                start = ((start[0]-1),start[1])

        #north move
        elif (move == 2):
            actions[i] = 'U'
            if(start[1] == 0):
                sequence[i] = start
                readings[i] = reading(graphs[j][start[0]][start[1]])
            elif(graphs[j][start[0]][start[1]-1] == 'B'):
                sequence[i] = start
                readings[i] = reading(graphs[j][start[0]][start[1]])
            else:
                sequence[i] = (start[0],(start[1]-1))
                readings[i] = reading(graphs[j][start[0]][start[1]-1])
                start = (start[0],(start[1]-1))
        
        #east move 
        elif (move == 3):
            actions[i] = 'R'
            if(start[0] == 49):
                sequence[i] = start
                readings[i] = reading(graphs[j][start[0]][start[1]])
            elif(graphs[j][start[0]+1][start[1]] == 'B'):
                sequence[i] = start
                readings[i] = reading(graphs[j][start[0]][start[1]])
            else:
                sequence[i] = ((start[0]+1),start[1])
                readings[i] = reading(graphs[j][start[0]+1][start[1]])
                start = ((start[0]+1),start[1])
        
        #south move
        elif(move == 4):
            actions[i] = 'D'
            if(start[1] == 99):
                sequence[i] = start
                readings[i] = reading(graphs[j][start[0]][start[1]])
            elif(graphs[j][start[0]][start[1]+1] == 'B'):
                sequence[i] = start
                readings[i] = reading(graphs[j][start[0]][start[1]])
            else:
                sequence[i] = (start[0],(start[1]+1))
                readings[i] = reading(graphs[j][start[0]][start[1]+1])
                start = (start[0],(start[1]+1))
        
        #no move
        else:
            sequence[i] = start
            readings[i] = reading(graphs[j][start[0]][start[1]])

    return sequence, actions, readings

        


        
        
        




def start(i):
    x = random.randint(0, 49)
    y = random.randint(0, 99)
    while(graphs[i][x][y] == 'B'):
        x = random.randint(0, 49)
        y = random.randint(0, 99)
    return (x,y)

def main():
    genGraph()
    for j in range(10):
        for i in range(10):
            name = "groundTruthFiles\graph" + str(j+1) + "-" + str(i+1) + ".txt"
            with open(name, "w") as f:
                startpoint = start(j)
                path, actions, readings = sequence(startpoint, j)
                path.insert(0,startpoint)
                f.write(str(startpoint) + "\n")
                f.write(str(path) + "\n")
                f.write(str(actions) + "\n")
                f.write(str(readings) + "\n")
    graphics.graphics(graphs)


main()
import random
import graphics

graphs = [[["0" for y in range (50)] for x in range(100)] for i in range(10)]


# generate graphs
def genGraph():
    for i in range(10):
        for x in range(100):
            for y in range(50):
                num = random.random()
                if(num <= .5):
                    graphs[i][x][y] = "N"
                elif(num <= .7):
                    graphs[i][x][y] = "H"
                elif(num <= .9):
                    graphs[i][x][y] = "T"
                else:
                    graphs[i][x][y] = "B"


# generate readings
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


# get random next move
def nextMove():
    move = random.randint(1,4)
    return move

# generate path
def sequence(start, j):
    readings = [None] * 100
    actions = [None] * 100
    sequence = [None] * 100
    for i in range(100):
        move = nextMove()
        # determine whether move is actually enacted
        moveOdds = random.random()
        #west move
        if (move == 1 and moveOdds <= .9):
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
        elif (move == 2 and moveOdds <= .9):
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
        elif (move == 3 and moveOdds <= .9):
            actions[i] = 'R'
            if(start[0] == 99):
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
        elif(move == 4 and moveOdds <= .9):
            actions[i] = 'D'
            if(start[1] == 49):
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
            if(move == 1):
                actions[i] = 'L'
            elif(move == 2):
                actions[i] = 'U'
            elif(move == 3):
                actions[i] = 'R'
            else:
                actions[i] = 'D'

    return sequence, actions, readings

        


        
        
        




def start(i):
    x = random.randint(0, 99)
    y = random.randint(0, 49)
    while(graphs[i][x][y] == 'B'):
        x = random.randint(0, 99)
        y = random.randint(0, 49)
    return (x,y)

def main():
    # populate graphs array
    genGraph()
    # write graphs
    for i in range(10):
        name = "graph" + str(i+1) + ".txt"
        with open(name, "w") as f:
            for y in range(50):
                for x in range(100):
                    f.write(str(graphs[i][x][y]) + " ")
                f.write("\n")

    # points to be used in simulations
    points = [["" for x in range(10)] for y in range(10)]
    # actions to be used in simulations
    moves = [["" for x in range(10)] for y in range(10)]
    # readings to be used in simulations
    observations = [["" for x in range(10)] for y in range(10)]
    for j in range(10):
        for i in range(10):
            # write ground truth files
            name = "groundTruthFiles\graph" + str(j+1) + "-" + str(i+1) + ".txt"
            with open(name, "w") as f:
                startpoint = start(j)
                path, actions, readings = sequence(startpoint, j)
                points[j][i] = path
                moves[j][i] = actions
                observations[j][i] = readings
                path.insert(0,startpoint)
                f.write(str(startpoint) + "\n")
                f.write(str(path) + "\n")
                f.write(str(actions) + "\n")
                f.write(str(readings) + "\n")
        
    # call graphics program
    graphics.graphics(graphs, points, moves, observations)


main()
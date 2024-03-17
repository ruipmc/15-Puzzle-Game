import sys
from collections import deque
import tkinter as tk
import queue
import heapq
import time
from sys import argv

# how to call the algorithms
#A* algorithm with the mannhatan distance heuristic -> A*-Manhattan
#A* algorithm with the sum of all pieces out of place heuristic -> A*-misplaced
#Greedy algorithm with the mannhatan distance heuristic -> Greedy-Manhattan
#Greedy algorithm with the sum of all pieces out of place heuristic -> Greedy-misplaced
#Iterative deepening search -> IDFS
#Depth first search -> DFS (takes too long to reach the answer)
#Depth first search -> depth (alternative to DFS)
#Breadth first search -> BFS

# create a 4x4 grid with the numbers 1 to 15 and a blank tile represented by 0
grid = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]

# get input from user for initial state
input_string = input("Enter input separated by spaces: ")
input_list = input_string.split()
matrix = []
for i in range(4):
    row = []
    for j in range(4):
        row.append(int(input_list[i * 4 + j]))
    matrix.append(row)
grid = matrix

output_string = input("Enter output separated by spaces: ")
output_list = output_string.split()
final = []
for i in range(4):
    line = []
    for j in range(4):
        line.append(int(output_list[i * 4 + j]))
    final.append(line)


# verify if the puzzle is solvable from the initial state
def inversions(board):
    list = []
    for i in range(4):
        for j in range(4):
            list.append(board[i][j])
    cont = 0
    for i in range(15):
        for j in range(i+1,16):
                if list[i]!=0 and list[j]!=0 and list[i] > list[j]:
                    cont += 1
    return cont

def solvable(board):
    num = inversions(board)
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                if (i % 2 == 0 and num % 2 != 0) or (i % 2 != 0 and num % 2 == 0):
                    return True
                return False

def reachable():
    return solvable(grid) == solvable(final)

if not reachable():
    print("It is impossible to reach a solution")
    exit()

try:
    alg = argv[1]
except:
    alg = input("Algoritmo:")

# function to update the grid display
def update_grid():
    for row in range(4):
        for col in range(4):
            label = labels[row][col]
            label.config(text=str(grid[row][col]))
            if grid[row][col] == 0:
                label.config(bg='white')
            else:
                label.config(bg='light gray')
    moves_label.config(text='Moves: {}'.format(moves))
    time_label.config(text='Time: {}'.format(time))

# function to handle button clicks
def button_click(row, col):
    global grid, moves, time
    if row > 0 and grid[row-1][col] == 0:
        grid[row][col], grid[row-1][col] = grid[row-1][col], grid[row][col]
        moves += 1
    elif row < 3 and grid[row+1][col] == 0:
        grid[row][col], grid[row+1][col] = grid[row+1][col], grid[row][col]
        moves += 1
    elif col > 0 and grid[row][col-1] == 0:
        grid[row][col], grid[row][col-1] = grid[row][col-1], grid[row][col]
        moves += 1
    elif col < 3 and grid[row][col+1] == 0:
        grid[row][col], grid[row][col+1] = grid[row][col+1], grid[row][col]
        moves += 1
    update_grid()
    check_win()

# function to check if the player has won
def check_win():
    global timer
    if grid == final:
        label = tk.Label(root, text='You win in {} moves and {} seconds!'.format(moves, time), font=('Helvetica', 16))
        label.grid(row=5, column=0, columnspan=4, padx=5, pady=5)
        root.after_cancel(timer)


# function to update the timer
def update_timer():
    global time
    if grid != final:
        time += 1
        update_grid()
        root.after(1000, update_timer)

# calculate the Manhattan distance between two points on the grid
def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# calculate the total Manhattan distance for the current state
def heuristic(state):
    total_distance = 0
    for i in range(4):
        for j in range(4):
            if state[i][j] != 0:
                final_pos = ((state[i][j]-1) // 4, (state[i][j]-1) % 4)
                total_distance += manhattan_distance((i, j), final_pos)
    return total_distance

def heuristic_outofplace(state):
    sum = 0
    for i in range(4):
        for j in range(4):
            if state[i][j] != final[i][j]:
                sum +=1
    return sum

# generate the successor states for the current state
def generate_successors(state):
    successors = []
    for i in range(4):
        for j in range(4):
            if state[i][j] == 0:
                if i > 0:
                    new_state = [row[:] for row in state]
                    new_state[i][j], new_state[i-1][j] = new_state[i-1][j], new_state[i][j]
                    successors.append(new_state)
                if i < 3:
                    new_state = [row[:] for row in state]
                    new_state[i][j], new_state[i+1][j] = new_state[i+1][j], new_state[i][j]
                    successors.append(new_state)
                if j > 0:
                    new_state = [row[:] for row in state]
                    new_state[i][j], new_state[i][j-1] = new_state[i][j-1], new_state[i][j]
                    successors.append(new_state)
                if j < 3:
                    new_state = [row[:] for row in state]
                    new_state[i][j], new_state[i][j+1] = new_state[i][j+1], new_state[i][j]
                    successors.append(new_state)
                return successors

# solve the puzzle using the A* search algorithm
def solve_astar(initial_state, final_state,h):
    s_time = time.time()
    max_nodes = 0
    queue = []
    heapq.heappush(queue, (h(initial_state), initial_state, []))
    visited = set()
    while queue:
        max_nodes = max(max_nodes,len(queue))
        _, state, path = heapq.heappop(queue)
        if state == final_state:
            e_time = time.time()
            return (path,e_time-s_time,max_nodes)
        if str(state) in visited:
            continue
        visited.add(str(state))
        for successor in generate_successors(state):
            heapq.heappush(queue, (len(path)+1+h(successor), successor, path+[(successor, len(path)+1)]))
    return None

# solve the puzzle using the greedy search algorithm
def solve_greedy(initial_state,final_state,h):
    s_time = time.time()
    max_nodes = 0
    queue = []
    heapq.heappush(queue, (h(initial_state), initial_state, []))
    visited = set()
    while queue:
        max_nodes = max(max_nodes, len(queue))
        _, state, path = heapq.heappop(queue)
        if state == final_state:
            e_time = time.time()
            return (path, e_time-s_time, max_nodes)
        if str(state) in visited:
            continue
        visited.add(str(state))
        for successor in generate_successors(state):
            heapq.heappush(queue, (h(successor),successor, path+[(successor,len(path)+1)]))
    return None

def depth_limited_search(state, goal_state, depth_limit):
    if state == goal_state:
        return []
    elif depth_limit == 0:
        return None
    else:
        for successor in generate_successors(state):
            path = depth_limited_search(successor, goal_state, depth_limit-1)
            if path is not None:
                return [successor] + path
        return None

def iterative_deepening_search(initial_state, goal_state, max_depth):
    s_time = time.time()
    max_nodes = 0
    for depth in range(max_depth+1):
        max_nodes=max(max_nodes,2**depth)
        path = depth_limited_search(initial_state, goal_state, depth)
        if path is not None:
            e_time = time.time()
            return path,e_time-s_time,max_nodes
    return None

def solve_depthfirst(state, goal_state, maxdepth):
    s_time = time.time()
    visited = set()
    max_nodes = 0
    if state == goal_state:
        return [], time.time()-s_time, max_nodes
    elif maxdepth == 0:
        return None, 0, max_nodes
    else:
        for successor in generate_successors(state):
            path, t, nodes = solve_depthfirst(successor, goal_state, maxdepth-1)
            max_nodes = max(max_nodes, nodes+1)
            if path is not None:
                e_time = time.time()
                return [successor] + path, e_time-s_time, max_nodes
            if str(successor) in visited:
                continue
            visited.add(str(successor))
        return None, 0, max_nodes


def DFS(initial_state, final_state):
    s_time = time.time()
    max_nodes = 0
    stack = []
    stack.append([initial_state])
    visited = set()
    while stack:
        max_nodes=max(max_nodes,len(stack))
        path = stack.pop()
        state = path[-1]
        if state == final_state:
            e_time=time.time()
            return path,e_time-s_time,max_nodes
        if str(state) in visited:
            continue
        visited.add(str(state))
        for successor in generate_successors(state):
            new_path = path + [successor]
            stack.append(new_path)
    return None

def BFS(initial_state, final_state):
    s_time = time.time()
    max_nodes = 0
    queue = deque()
    queue.appendleft([initial_state])
    visited = set()
    while queue:
        max_nodes=max(max_nodes,len(queue))
        path = queue.pop()
        state = path[-1]
        if state == final_state:
            e_time=time.time()
            return path,e_time-s_time,max_nodes
        if str(state) in visited:
            continue
        visited.add(str(state))
        for successor in generate_successors(state):
            new_path = path + [successor]
            queue.appendleft(new_path)
    return None

tam,_, __ = solve_astar(grid, final, heuristic)
min = len(tam)


# chooses which algorithm we want to use
def switch(alg):
    if alg == "Greedy-Manhattan":
        (path,ex_time,nodes) = solve_greedy(grid, final,heuristic)
        if path:
            print("Solution found in", len(path), "moves:")
            for state, move in path:
                print(move, ":", state)
            print("Execution time:", ex_time,"s")
            print("Number of max nodes in memory:", nodes)
        else:
            print("No solution found.")

    if alg == "Greedy-misplaced":
        (path,ex_time,nodes) = solve_greedy(grid, final,heuristic_outofplace)
        if path:
            print("Solution found in", len(path), "moves:")
            for state, move in path:
                print(move, ":", state)
            print("Execution time:", ex_time,"s")
            print("Number of max nodes in memory:", nodes)
        else:
            print("No solution found.")

    elif alg == "A*-Manhattan":
        (path, ex_time, nodes) = solve_astar(grid, final, heuristic)
        if path:
            print("Solution found in", len(path), "moves:")
            for state, move in path:
                print(move, ":", state)
            print("Execution time:", ex_time,"s")
            print("Number of max nodes in memory:", nodes)
        else:
            print("No solution found.")

    elif alg == "A*-misplaced":
        (path, ex_time, nodes) = solve_astar(grid, final, heuristic_outofplace)
        if path:
            print("Solution found in", len(path), "moves:")
            for state, move in path:
                print(move, ":", state)
            print("Execution time:", ex_time,"s")
            print("Number of max nodes in memory:", nodes)
        else:
            print("No solution found.")

    elif alg == "IDFS":
        path,ex_time,nodes = iterative_deepening_search(grid, final, sys.maxsize)
        if path:
            print("Solution found in", len(path), "moves:")
            move = 1
            for state in path:
                print(move, ":",state)
                move += 1
            print("Execution time:", ex_time,"s")
            print("Number of max nodes in memory:", nodes)
        else:
            print("No solution found.")

    elif alg == "depth":
        path,ex_time,nodes = solve_depthfirst(grid,final,min)
        if path:
            print("Solution found in", len(path), "moves:")
            move = 1
            for state in path:
                print(move, ":", state)
                move += 1
            print("Execution time:", ex_time,"s")
            print("Number of max nodes in memory:", nodes)
        else:
            print("No solution found.")

    elif alg == "DFS":
        path,ex_time,nodes = DFS(grid,final)
        if path:
            print("Solution found in", len(path)-1, "moves:")
            move = 1
            for state in path:
                if state!=grid:
                    print(move, ":", state)
                    move += 1
            print("Execution time:", ex_time,"s")
            print("Number of max nodes in memory:", nodes)
        else:
            print("No solution found.")


    elif alg == "BFS":
        path,ex_time,nodes = BFS(grid,final)
        if path:
            print("Solution found in",len(path)-1,"moves:")
            move = 1
            for state in path:
                if state != grid:
                    print(move,":",state)
                    move += 1
            print("Execution time:", ex_time,"s")
            print("Number of max nodes in memory:", nodes)
        else:
            print("No solution found")

    exit()


switch(alg)

# initialize the moves and time counters
moves = 0
time = 0
'''
# create the GUI
root = tk.Tk()
root.title('Game of 15')

# create the grid
labels = []
for row in range(4):
    label_row = []
    for col in range(4):
        label = tk.Label(root, text=str(grid[row][col]), font=('Helvetica', 24), width=3, relief='raised', bg='light gray')
        label.grid(row=row, column=col, padx=5, pady=5)
        label.bind('<Button-1>', lambda e, row=row, col=col: button_click(row, col))
        label_row.append(label)
    labels.append(label_row)
    
# create the moves and time labels
moves_label = tk.Label(root, text='Moves: 0', font=('Helvetica', 16))
moves_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
time_label = tk.Label(root, text='Time: 0', font=('Helvetica', 16))
time_label.grid(row=4, column=2, columnspan=2, padx=5, pady=5)

# start the timer
timer = root.after(1000, update_timer)

# start the GUI main loop
root.mainloop()
'''

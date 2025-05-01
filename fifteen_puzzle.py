import heapq
 
N = 4

goal_state_4 = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 0]
]

goal_state_3 = [
    [1,2,3],
    [4,5,6],
    [7,8,0]
]

goal_state_2 = [
    [1,2],
    [3,0]
]

def misplaced_tiles(board, N):
    match N:
        case 4:
            goal_state = goal_state_4
        case 3:
            goal_state = goal_state_3
        case 2:
            goal_state = goal_state_2
    misplaced = 0
    for i in range(N):
        for j in range(N):
            if board[i][j] != 0 and board[i][j] != goal_state[i][j]:
                misplaced += 1
    return misplaced

def find_blank(board, N):
    for i in range(N):
        for j in range(N):
            if board[i][j] == 0:
                return i, j

def is_solvable(board, N):
    flat = [num for row in board for num in row if num != 0]
    inversions = 0
    row = 0
    blankRow = 0
    for i in range (len(flat)):
        row = i // N + 1
        if flat[i] == 0:
            blankRow = row
            continue
        for j in range(i+1, len(flat)):
            if flat[i] > flat[j] and flat[j] != 0:
                inversions += 1  
    if N % 2 == 0:
        if blankRow % 2 == 0:
            return inversions % 2 == 0
        else:
            return inversions % 2 != 0
    else:
        return inversions % 2 == 0

def is_valid(x, y, N):
    return 0 <= x < N and 0 <= y < N

def board_to_tuple(board):
    return tuple(tuple(row) for row in board)

def get_neighbors(board, N):
    x, y = find_blank(board, N)
    moves = [(-1,0), (1, 0), (0,-1), (0,1)]
    neighbors = []

    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if is_valid(nx, ny, N):
            new_board = [row[:] for row in board]
            new_board[x][y], new_board[nx][ny] = new_board[nx][ny], new_board[x][y]
            neighbors.append((new_board, nx, ny))
    return neighbors

def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.append(current)
    return path[::-1]

def a_star(start_board, N):
    start = board_to_tuple(start_board)

    match N:
        case 4:
            goal = board_to_tuple(goal_state_4)
        case 3:
            goal = board_to_tuple(goal_state_3)
        case 2:
            goal = board_to_tuple(goal_state_2)

    g_cost = {start: 0}
    f_cost = {start: misplaced_tiles(start_board, N)}

    came_from = {}

    open_set = []
    heapq.heappush(open_set, (f_cost[start], start))

    visited = set()

    while open_set:
        _, current_tuple =  heapq.heappop(open_set)

        if current_tuple == goal:
            print("Goal Reached")
            path = reconstruct_path(came_from, current_tuple)
            print(f"Moves required: {len(path) - 1}")
            for state in path:
                print_board(state)
            return
        
        if current_tuple in visited:
            continue
        visited.add(current_tuple)

        current_board = [list(row) for row in current_tuple]
        for neighbor_board, _, _ in get_neighbors(current_board, N):
            neighbor_tuple = board_to_tuple(neighbor_board)
            tentative_g = g_cost[current_tuple] + 1

            if neighbor_tuple not in g_cost or tentative_g < g_cost[neighbor_tuple]:
                came_from[neighbor_tuple] = current_tuple
                g_cost[neighbor_tuple] = tentative_g
                f = tentative_g + misplaced_tiles(neighbor_board, N)
                f_cost[neighbor_tuple] = f
                heapq.heappush(open_set, (f, neighbor_tuple))

    print("No solution found")

def print_board(board):
    for row in board:
        print(" ".join(str(num) if num != 0 else " " for num in row))
    print("-----")

if __name__ == '__main__':
    start_board = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 12, 10, 11],
        [0, 13, 14, 15]
    ]

    # start_board = [
    #     [2,3],
    #     [1,0]
    # ]

    # start_board = [
    #     [3,1,2],
    #     [5,4,6],
    #     [8,7,0]
    # ]

    N = 4

    print("Starting board: ")
    print_board(start_board)

    if is_solvable(start_board, N):
        a_star(start_board, N)
    else:
        print("Puzzle not solvable")
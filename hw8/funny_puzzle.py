import heapq

def get_manhattan_distance(from_state, to_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    distance = 0
    for i in range(9):
        if from_state[i] != to_state[i] and from_state[i] != 0:
            j = to_state.index(from_state[i])
            x_dif = abs((j % 3) - (i % 3))
            y_dif = abs(int((j / 3)) - int((i / 3)))
            distance += (x_dif + y_dif)
    return distance

def print_succ(state):
    succ_states = get_succ(state)

    for succ_state in succ_states:
        print(succ_state, "h={}".format(get_manhattan_distance(succ_state)))

def get_succ(state):
    succ_states = []
    blank_occurences = []
    for i in range(9):
        if state[i] == 0:
            blank_occurences.append(i)
    for occurence in blank_occurences:
        if occurence >= 1:
            copy = state.copy()
            copy[occurence] = copy[occurence - 1]
            copy[occurence - 1] = 0
            if copy not in succ_states and copy != state:
                succ_states.append(copy)
        if occurence <= 7:
            copy = state.copy()
            copy[occurence] = copy[occurence + 1]
            copy[occurence + 1] = 0
            if copy not in succ_states and copy != state:
                succ_states.append(copy)
        if occurence >= 3:
            copy = state.copy()
            copy[occurence] = copy[occurence - 3]
            copy[occurence - 3] = 0
            if copy not in succ_states and copy != state:
                succ_states.append(copy)
        if occurence <= 5:
            copy = state.copy()
            copy[occurence] = copy[occurence + 3]
            copy[occurence + 3] = 0
            if copy not in succ_states and copy != state:
                succ_states.append(copy)
    return sorted(succ_states)


def solve(state, goal_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):

    def calc_f(successor, distance = 0):
        g = get_manhattan_distance(successor)
        h = 0
        for i in range(9):
            if successor[i] != goal_state[i]:
                h += 1
        f = g + h + distance
        return f, g, h

    f, g, h = calc_f(state)
    queue = []
    heapq.heappush(queue, (f, state, (g, h, -1)))
    max_len = 1
    visited = []
    while queue:
        c, s, other_infor = heapq.heappop(queue)
        visited.append(s)
        visited.append(other_infor)
        if s == goal_state:
            parent = other_infor[2] * 2
            moves = 1
            result = []
            while visited[parent] != goal_state:
                result.append(f'{visited[parent]} h={visited[parent + 1][1]} moves={moves}')
                parent = visited[(parent * 2) + 1][2] * 2
                moves += 1
            result.append(f'{visited[parent]} h={visited[parent + 1][1]} moves={moves}')
            for result in result:
                print(result)
            print(f'Max queue length: {max_len}')
            break
        succ_state = get_succ(s)
        for successor in succ_state:
            if successor not in visited:
                f, g, h = calc_f(successor, c)
                heapq.heappush(queue, (f, successor, (g, h, other_infor[2] + 1)))
        max_len += 1

if __name__ == "__main__":
    """
    Feel free to write your own test code here to exaime the correctness of your functions. 
    Note that this part will not be graded.
    """
    print_succ([2,5,1,4,0,6,7,0,3])
    print()

    print(get_manhattan_distance([2,5,1,4,0,6,7,0,3], [1, 2, 3, 4, 5, 6, 7, 0, 0]))
    print()

    solve([4,3,0,5,1,6,7,2,0])
    print()

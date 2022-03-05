import numpy as np
import math
import heapq as hq
import queue

action_set = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1))

obstacle_space = np.full((250, 400), np.inf)

r = 40
h = 300
k = 185


def inside_circle(x, y):
    if np.square(x - h) + np.square(y - k) <= np.square(r):
        print("In circle")
        return True
    else:
        return False


# in_circle = inside_circle(x, y)
def in_irreg(x, y):
    ir_ln1 = (x - 105) * ((185 - 100) / (36 - 105)) + 100
    ir_ln2 = (x - 36) * ((210 - 185) / (115 - 36)) + 185
    ir_ln3 = (x - 80) * ((210 - 180) / (115 - 80)) + 180
    ir_ln4 = (x - 105) * ((180 - 100) / (80 - 105)) + 100

    if (ir_ln1 <= y <= ir_ln2) and (ir_ln3 <= y <= ir_ln4):
        print("In polygon")
        return True
    else:
        return False


def in_hex(x, y):
    #   hx_ln1 = (x - 160)*((120 - 80)/(65 - 165)) + 80
    hx_ln1 = 165
    hx_ln2 = (x - 65) * ((140 - 120) / (200 - 65)) + 120
    hx_ln3 = (x - 200) * ((120 - 140) / (235 - 200)) + 140
    #   hx_ln4 = (x - 235)*((80 - 120)/(235 - 235)) + 120
    hx_ln4 = 235
    hx_ln5 = (x - 235) * ((60 - 80) / (200 - 235)) + 80
    hx_ln6 = (x - 200) * ((80 - 60) / (165 - 200)) + 60

    if hx_ln2 >= y >= x >= y >= hx_ln5 and hx_ln3 >= y >= hx_ln6:
        print("In hexagon")
        return True
    else:
        return False


def backtrack(path, ClosedList, idx):
    print("Backtracking")

    for i in range(0, len(ClosedList)):
        if ClosedList[i][2] == idx:
            idx = i
            break
    if ClosedList[idx][1] == -1:
        path.append(ClosedList[idx][3])
        return path
    else:
        path.append(ClosedList[idx][3])
        backtrack(path, ClosedList, ClosedList[idx][1])


def check_closedlist(node, closedlst):
    for l in range(0, len(closedlst)):

        if closedlst[l][3] == node[3]:
            print("Closed")
            return True
    return False


def check_openlist(node, openlst):

    for j in range(0, len(openlst)):
        if openlst[j][3] == node[3]:
            # openlst[j] = node
            print("Open")
            return True
    return False


if __name__ == '__main__':
    goal_reached = False
    open_q = []
    closed_list = []

    initial_node = [0, -1, 0, [0, 0]]  #### [Cost, Paerent index, Current index, (x, y)] ###

    hq.heappush(open_q, initial_node)
    hq.heapify(open_q)
    Nope = True
    x = 0
    y = 0
    while Nope:
        x = int(input("Enter X coordinate of Goal: "))
        y = int(input("Enter Y coordinate of Goal: "))
        if 0 < x < 400 and 0 < y < 250:
            Nope = False
        print("Enter a Valid Goal Position")
    goal = [x, y]
    index = 0
    while len(open_q) != 0 and goal_reached == False:

        if len(open_q) == 0:
            print("No Solution Found **")
            print("Please Enter a Valid Goal position")
            break

        first = hq.heappop(open_q)

        closed_list.append(first)

        if first[3] == goal:
            goal_reached = True
            # return goal_reached
            print("Goal Found")
            # backtrack(closed_list)
            path = []
            path.append(closed_list[len(closed_list) - 1][3])
            backtrack(path, closed_list, closed_list[len(closed_list) - 1][1])
            print(path)
            break
            # Backtrack

        else:
            for i in range(0, 8):
                cost = 1.4
                if 0 <= first[3][0] <= 400 and 0 <= first[3][1] <= 250:
                    if i < 4:
                        cost = 1
                    new_node = [0, 0, 0, [0, 0]]
                    new_node[0] = first[0] + cost
                    new_node[1] = first[2]
                    new_node[2] = index + 1
                    new_node[3][0] = first[3][0] + action_set[i][0]
                    new_node[3][1] = first[3][1] + action_set[i][1]

                    in_circle = inside_circle(new_node[3][0], new_node[3][1])
                    in_poly = in_irreg(new_node[3][0], new_node[3][1])
                    in_hexagon = in_hex(new_node[3][0], new_node[3][1])

                    index += 1

                    in_closed_list = check_closedlist(new_node, closed_list)
                    in_open_list = check_openlist(new_node, open_q)

                    if (in_poly == True) or (in_hexagon == True) or (in_circle == True):
                        index -= 1
                        continue  # Skip Node
                    if 0 > new_node[3][0] and 0 > new_node[3][1]:
                        index -= 1
                        continue  # Skip Node

                    if in_closed_list:
                        index -= 1
                        continue  # Skip Node

                    if in_open_list:
                        for i in range(0, len(open_q)):
                            if open_q[i][3] == new_node[3] and open_q[i][0] > new_node[0]:
                                open_q[i] = new_node
                                print("Cost Update")
                        index -= 1
                        continue  # Skip Node
                    # Was here
                    if (0 <= new_node[3][0] <= 400) and (0 <= new_node[3][1] <= 250) and (in_open_list == False) and (in_closed_list == False):
                        hq.heappush(open_q, new_node)

    # print(closed_list)

#  elif :
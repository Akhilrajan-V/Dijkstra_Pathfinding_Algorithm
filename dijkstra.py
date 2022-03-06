"""
ENPM661: Project 2

Akhilrajan Vethirajan (v.akhilrajan@gmail.com)

University of Maryland, College Park

"""

import numpy as np
import math
import heapq as hq
import cv2
import matplotlib.pyplot as plt
import matplotlib

action_set = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1))

r = 40
h = 300
k = 185


def obstacle_space():
    map = np.zeros((250,400))
    for y in range(1,map.shape[0]+1):
        for x in range(1, map.shape[1]+1):
            if x>=165 and x<=235 and ((map.shape[0]-140-map.shape[0]+120)/(200-235))*(x-235)+map.shape[0]-120<=y and\
                    ((map.shape[0]-140-map.shape[0]+120)/(200-165))*(x-165)+map.shape[0]-120<=y and\
                    ((map.shape[0]-80-map.shape[0]+60)/(165-200))*(x-200)+map.shape[0]-60>=y and\
                    ((map.shape[0]-80-map.shape[0]+60)/(235-200))*(x-200)+map.shape[0]-60>=y:
                map[y-1][x-1]=1
            if ((map.shape[0]-210-map.shape[0]+185)/(115-36))*(x-36)+map.shape[0]-185<=y and\
                    ((map.shape[0]-100-map.shape[0]+185)/(105-36))*(x-36)+map.shape[0]-185>=y and\
                    (((map.shape[0]-210-map.shape[0]+180)/(115-75))*(x-75)+map.shape[0]-180>=y or\
                     ((map.shape[0]-180-map.shape[0]+100)/(75-105))*(x-105)+map.shape[0]-100<=y):
                map[y-1][x-1]=1
            if (x-300)**2+(y-map.shape[0]+185)**2<=40**2:
                map[y-1][x-1]=1
    return map


def backtrack(path, ClosedList, idx):

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


def check_openlist(node, openlst):

    for j in range(0, len(openlst)):
        if openlst[j][3] == node[3]:
            # openlst[j] = node
            # print("Open")
            return True
    return False


if __name__ == '__main__':
    goal_reached = False
    open_q = []
    closed_list = []
    count = 1
    map = obstacle_space()
    map_color_r = np.zeros((250, 400))
    map_color_b = np.zeros((250, 400))
    map_color_g = np.zeros((250, 400))
    map_color1 = np.zeros((250, 400, 3))
    Nope = True
    while Nope:
        x_i = int(input("Enter X coordinate of Start position: "))
        y_i = int(input("Enter Y coordinate of Start position: "))

        x_g = int(input("Enter X coordinate of Goal: "))
        y_g = int(input("Enter Y coordinate of Goal: "))
        if 0 <= x_i < 400 and 0 <= y_i < 250 and 0 <= x_g < 400 and 0 <= y_g < 250:
            Nope = False

        elif map[y_i][x_i] != 0:
            print("No solution can be found")

        elif map[y_g][x_g] != 0:
            print("No solution can be found")
        else:
            print("Enter a Valid Position")
    # XY = 250 - y_g
    goal = [x_g, y_g]
    index = 0
    initial_node = [0, -1, 0, [x_i, y_i]]  # [Cost, Parent index, Current index, (x, y)]
    hq.heappush(open_q, initial_node)
    hq.heapify(open_q)

    while len(open_q) != 0 and goal_reached == False:
        if count == 1:
            print("Running Dijkstra Algorithm ---")
            count = 2

        first = hq.heappop(open_q)

        map[first[3][1]][first[3][0]] = 5
        closed_list.append(first)

        if first[3] == goal:
            goal_reached = True
            print("Goal Found")  # return goal_reached
            path = []
            path.append(closed_list[len(closed_list) - 1][3])
            backtrack(path, closed_list, closed_list[len(closed_list) - 1][1])  # Backtrack

            for i in range(0, len(closed_list)):
                map[closed_list[i][3][1]][closed_list[i][3][0]] = 0.7
                map_color = map

                map_color_r[map_color == 0] = 1
                map_color_b[map_color == 0.7] = 1
                map_color_g[map_color == 1] = 1
                map_color1[:, :, 1] = map_color_r * 255
                map_color1[:, :, 2] = map_color_b * 255
                map_color1[:, :, 0] = map_color_g * 55

                cv2.imshow("Dijkstra", map_color1)
                cv2.waitKey(1)

            map_color_r1 = np.zeros((250, 400))
            map_color_b1 = np.zeros((250, 400))
            map_color_g1 = np.zeros((250, 400))
            map_color2 = np.zeros((250, 400, 3))

            for i in range(0, len(path)):
                map[path[len(path) - i - 1][1]][path[len(path) - i - 1][0]] = 0.2
                map_color = map
                map_color_r1[map_color == 0] = 1
                map_color_b1[map_color == 0.2] = 1
                map_color_g1[map_color == 1] = 1
                map_color2[:, :, 1] = map_color_r1 * 0
                map_color2[:, :, 2] = map_color_b1 * 255
                map_color2[:, :, 0] = map_color_g1 * 255
                cv2.imshow("Path", map_color2)
                cv2.waitKey(100)

            break

        else:
            for i in range(0, 8):
                cost = 1.4
                if 0 <= first[3][0] < 400 and 0 <= first[3][1] < 250:
                    if i < 4:
                        cost = 1
                    new_node = [0, 0, 0, [0, 0]]
                    new_node[0] = first[0] + cost
                    new_node[1] = first[2]
                    new_node[2] = index + 1
                    new_node[3][0] = first[3][0] + action_set[i][0]
                    new_node[3][1] = first[3][1] + action_set[i][1]

                    index += 1

                    in_open_list = check_openlist(new_node, open_q)

                    # if 0 > new_node[3][0] and 0 > new_node[3][1]:
                    if 0 <= new_node[3][0] < 400 and 0 <= new_node[3][1] < 250:
                        # index -= 1
                        # continue # Skip Node

                        if map[new_node[3][1]][new_node[3][0]] != 0:  # shifting X and Y
                            continue

                        if in_open_list:
                            for i in range(0, len(open_q)):
                                if open_q[i][3] == new_node[3] and open_q[i][0] > new_node[0]:
                                    open_q[i] = new_node
                                    # print("Cost Update")
                            index -= 1
                            continue  # Skip Node

                        if (0 <= new_node[3][0] < 400) and (0 <= new_node[3][1] < 250) and (in_open_list == False):
                            hq.heappush(open_q, new_node)

    if len(open_q) == 0:
        print("No Solution Found **")
        print("Please Enter a Valid Goal position")
        print("Goal maybe in obstacle space")
        quit()

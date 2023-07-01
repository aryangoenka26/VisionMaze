from math import sqrt
import numpy as np
import cv2
from collections import deque
import timeit

#colors...
white = (255,255,255)
black = (0,0,0)
grey = (127,127,127)
#red = (0,0,255)
red = (63,62,255)
#green = (0,255,0)
green = (60,255,60)
blue = (255,0,0)
orange = (0,128,255)

#assumptions...
# start_col = red #color of start node
# end_col = green #color of end node
open_col = white #color of open path
obs_col = black #color of obsacle
visited_col = blue #color to show visited nodes (pixels)
path_col = orange #color to show the path found



class Node:
    def __init__(self,index,parent):
        self.x = index[0]
        self.y = index[1]
        self.parent = parent #parent node
        self.g = np.inf #cost of path from start to current node
        self.h = np.inf #heuristic estimated cost from current to end (goal) node
        self.f = np.inf # f = g + h

    def __eq__(self,other):
        return (self.x==other.x and self.y==other.y)


def bfs_path(start,end,image):
    start_time = timeit.default_timer()

    path_found = False #flag

    q = deque() #queue
    q.append(start)
    image[start.x][start.y] = visited_col

    child_index = [(-1,0),(0,-1),(1,0),(0,1)] #for travsersing through indices of child nodes of the current node
    cv2.namedWindow('Path-finding_BFS',cv2.WINDOW_NORMAL)
    while (len(q)>0):
        cv2.imshow("Path-finding_BFS", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Program terminated midway!")
            break

        current = q.popleft()
        i, j = current.x, current.y

        for index in child_index:
            new_ind = (i+index[0],j+index[1])

            # invalid index(out of image check)
            if (new_ind[0]<0 or new_ind[1]<0 or new_ind[0]>=image.shape[0] or new_ind[1]>=image.shape[1]):
                continue

            if (image[new_ind[0], new_ind[1]] != obs_col).any() and (image[new_ind[0], new_ind[1]]!= visited_col).any():
                if (i == end.x and j == end.y):
                    path_found = True
                    break

                image[new_ind[0]][new_ind[1]] = visited_col
                newNode = Node((new_ind[0],new_ind[1]),current)
                q.append(newNode)
        if(path_found):
            break
    cv2.destroyAllWindows()


    if (path_found):  
        end_time = timeit.default_timer()
        print("          ---------------")
        print('Time taken (s) :',end_time-start_time)
        path_length = show_path(current, start, image)
        print("          ---------------")

        return ['Breadth-First search',path_length,end_time-start_time]
    else:
        print('No path found!')
        return ['Breadth-First search','NO PATH FOUND','NO PATH FOUND']


def dfs_path(start,end,image):
    #start -> starting node for path finding
    #end -> goal node for path finding
    start_time = timeit.default_timer()

    path_found = False #flag

    stack = deque()

    stack.append(start)
    image[start.x][start.y] = visited_col

    cv2.namedWindow('Path-finding_DFS',cv2.WINDOW_NORMAL)

    child_index = [(-1,0),(0,-1),(1,0),(0,1)] #for travsersing through indices of child nodes of the current node

    while(len(stack)>0):
        cv2.imshow('Path-finding_DFS',image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print('Program terminated midway!')
            break
        
        current = stack.pop() #current node
        i,j = current.x, current.y

        for index in child_index:
            new_ind = (i+index[0],j+index[1])

            if(new_ind[0]>0 and new_ind[0]<image.shape[0] and new_ind[1]>0 and new_ind[1]<image.shape[1]):
                if ((image[new_ind[0]][new_ind[1]]!=obs_col).any() and (image[new_ind[0]][new_ind[1]]!=visited_col).any()):
                    if((new_ind[0],new_ind[1])==(end.x,end.y)):
                        image[new_ind[0]][new_ind[1]] = visited_col
                        current = Node((new_ind[0],new_ind[1]),current)
                        path_found = True
                        break
                    stack.append(Node((new_ind[0],new_ind[1]),current))
                    image[new_ind[0]][new_ind[1]] = visited_col
        if(path_found):
            break

    cv2.destroyAllWindows()


    if(path_found):
        end_time = timeit.default_timer()
        print('Time taken (s) :',end_time-start_time)
        path_length = show_path(current,start,image)
        return ['Depth-First search',path_length,end_time-start_time]
    else:
        print("No path found!")
        return ['Depth-First search','NO PATH FOUND','NO PATH FOUND']

def greedy_path(start,end,image):
    #start -> starting node for path finding
    #end -> goal node for path finding
    start_time = timeit.default_timer()

    path_found = False #flag

    nodes = [] #will function as the priority queue for the nodes
    start.h = calc_dist(start,end)
    nodes.append(start)


    cv2.namedWindow('Path-finding_GREEDY',cv2.WINDOW_NORMAL)

    child_index = [(-1,0),(0,-1),(1,0),(0,1)] #for travsersing through indices of child nodes of the current node

    while(len(nodes)>0):
        cv2.imshow('Path-finding_GREEDY',image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print('Program terminated midway!')
            break

        current = get_node_greedy(nodes) #current node
        nodes.remove(current)
        i,j = current.x,current.y
        image[i][j] = visited_col

        for index in child_index:
            new_ind = (i+index[0],j+index[1])

            if (new_ind[0]>0 and new_ind[0]<image.shape[0] and new_ind[1]>0 and new_ind[1]<image.shape[1]):
                if ((image[new_ind[0]][new_ind[1]]!=obs_col).any() and (image[new_ind[0]][new_ind[1]]!=visited_col).any()):
                    if((new_ind[0],new_ind[1])==(end.x,end.y)):
                        image[new_ind[0]][new_ind[1]] = visited_col
                        current = Node((new_ind[0],new_ind[1]),current)
                        path_found = True
                        break
                    new_node = Node((new_ind[0],new_ind[1]),current)
                    new_node.h = calc_dist(new_node,end)
                    nodes.append(new_node)
                    image[new_ind[0]][new_ind[1]] = visited_col
        if(path_found):
            break
    cv2.destroyAllWindows()


    if(path_found):
        end_time = timeit.default_timer()
        print('Time taken (s) :',end_time-start_time)
        path_length = show_path(current,start,image)
        return ['Best-First search',path_length,end_time-start_time]
    else:
        print("No path found!")
        return ['Best-First search','NO PATH FOUND','NO PATH FOUND']

def dijkstra_path(start,end,image):
    start_time = timeit.default_timer()

    path_found = False #flag

    q = []
    start.g = 0
    q.append(start)

    child_index = [(-1, 0), (0, -1), (1, 0), (0, 1)]

    cv2.namedWindow('Path-finding_DIJKSTRA',cv2.WINDOW_NORMAL)
    while(len(q)):
        cv2.imshow('Path-finding_DIJKSTRA', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Program terminated midway!")
            break

        current = get_min_node_dijkstra(q)
        image[current.x, current.y] = visited_col
        i, j = current.x, current.y
        q.remove(current)

        if (current == end):
            path_found = True
            break

        for index in child_index:
            newIndex = (i + index[0], j+ index[1])
            if newIndex[0]< 0 or newIndex[1]< 0 or newIndex[0]>= image.shape[0] or newIndex[1]>= image.shape[1]:
                continue
            
            if (image[newIndex[0], newIndex[1]]!= obs_col).any() and (image[newIndex[0], newIndex[1]] != visited_col).any():

                child = Node(newIndex,current)
                child.g = current.g + 1       #(unweighted graph) instead of using calc_dist using 1 as each child is going to be adjacent to its parent

                if child in q:
                    for node in q:
                        if node == child:
                            if child.g< node.g:
                                node.g = child.g
                                node.parent = child.parent
                                break
                            else:
                                break
                else:
                    q.append(child)
    cv2.destroyAllWindows()


    if (path_found):
        end_time = timeit.default_timer()
        print('Time taken (s) :',end_time-start_time)
        path_length = show_path(current, start, image)
        return ["Dijkstra's algorithm",path_length,end_time-start_time]
    else:
        print('No path found!')
        return ["Dijkstra's algorithm",'NO PATH FOUND','NO PATH FOUND']

def astar_path(start,end,image):
    #start -> starting node for path finding
    #end -> goal node for path finding
    start_time = timeit.default_timer()

    path_found = False #flag

    nodes = [] #will function as the priority queue for the nodes
    start.g, start.h = 0, calc_dist(start,end)
    start.f = start.g + start.h
    nodes.append(start)

    cv2.namedWindow('Path-finding_A*',cv2.WINDOW_NORMAL)

    child_index = [(-1,0),(0,-1),(1,0),(0,1)] #for travsersing through indices of child nodes of the current node

    while(len(nodes)>0):
        cv2.imshow('Path-finding_A*',image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print('Program terminated midway!')
            break

        current = get_node_astar(nodes) #current node
        nodes.remove(current)
        i,j = current.x,current.y
        image[i][j] = visited_col

        if(current==end):
            path_found = True
            break
        
        children = []

        for index in child_index:
            new_ind = (i+index[0],j+index[1])

            if (new_ind[0]<0 or new_ind[0]>=image.shape[0] or new_ind[1]<0 or new_ind[1]>=image.shape[1]):
                continue
            if((image[new_ind[0]][new_ind[1]]==obs_col).all() or (image[new_ind[0]][new_ind[1]]==visited_col).all()):
                continue
            children.append(Node((new_ind[0],new_ind[1]),current))

        for child in children:
            child.g = current.g + calc_dist(child,current)
            child.h = calc_dist(child,end)
            child.f = child.g + child.h

            for node in nodes:
                if child==node:
                    if (child.g < node.g):
                        node.g = child.g
                        node.f = child.f
                        node.parent = current
                        break
                    break
            else:
                nodes.append(child)
    cv2.destroyAllWindows()


    if(path_found):
        end_time = timeit.default_timer()
        print('Time taken (s) :',end_time-start_time)
        path_length = show_path(current,start,image)
        return ['A* algorithm',path_length,end_time-start_time]
    else:
        print("No path found!")
        return ['A* algorithm','NO PATH FOUND','NO PATH FOUND']

def show_path(end,start,image):
    #end -> end node
    #start -> start node
    cv2.namedWindow('PATH',cv2.WINDOW_AUTOSIZE)

    current = end #current node
    path_len = 0
    while(current!=start):
        cv2.imshow('PATH',image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print('Program terminated midway!')
            break
        image[current.x][current.y] = path_col
        current = current.parent
        path_len += 1
    print("         ----------")
    print("Path length (in pixels) :", path_len)
    print('Press q to close the window')
    if cv2.waitKey(0) & 0xFF==ord('q'):
        cv2.destroyAllWindows()
    return path_len


def calc_dist(node1,node2):
    #node1 and node2 are the two nodes between which EUCLIDEAN distance is to be calculated
    dist = sqrt((node1.x - node2.x)**2 + (node1.y-node2.y)**2)
    return dist


def get_node_greedy(nodes_list):
    min_dist = np.inf
    req_node = None
    for node in nodes_list:
        if (node.h < min_dist):
            req_node = node
            min_dist = node.h
    return req_node

def get_node_astar(nodes_list):
    min_dist = np.inf
    req_node = None
    for node in nodes_list:
        if (node.f < min_dist):
            req_node = node
            min_dist = node.f
    return req_node

def get_min_node_dijkstra(q):
    min_dist = np.inf
    min = None
    for node in q:
        if node.g < min_dist:
            min_dist = node.g
            min = node
    return min

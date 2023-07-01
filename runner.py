from algorithms import *
from maze_generator import *
from locality_map import *
import os
import csv

#colors
maze_start = (127,127,127)
maze_end = (127,127,127)
kgp_start = (63,62,255)
kgp_end = (60,255,60)
locality_start = (0,0,255)
locality_end = (0,255,0)

def find_start_end(start_col, end_col, image):
    height, width = image.shape[0], image.shape[1]
    req_coordinates = []
    esc=False
    for i in range(0, height):
        for j in range(0, width):
            if (image[i][j]==start_col).all():
                req_coordinates.append(Node((i,j),None))
                esc=True
                break
        if (esc):
            break
    esc=False
    for i in range(height-1,-1,-1):
        for j in range(width-1, -1,-1):
            if (image[i][j]==end_col).all():
                req_coordinates.append(Node((i,j),None))
                esc=True
                break
        if(esc):
            break

    return req_coordinates


if __name__=='__main__':
    try:
        print('WELCOME!!!')

        with open('logs.csv','a',newline='') as file:
            file_not_exist = os.stat('logs.csv').st_size == 0
            writer = csv.writer(file, delimiter=',')
            if file_not_exist:
                writer.writerow(['MAZE/MAP','ALGORITHM','PATH LENGTH (in pixels)','TIME TAKEN (in s)'])

            while True:
                print("*******************************")
                print('What would you like to work on?')
                print('For a (newly generated) maze, enter 1')
                print('For the KGP map (Map 1), enter 2')
                print('For another map (Map 2), enter 3')
                print('To quit, enter q')
                prog = input('Enter your (maze/map) choice : ')
                while (prog not in ['1','2','3','q','Q']):
                    prog = input('Please give a valid input : ')
                
                if (prog == '1'):
                    img_orig = maze_generate()
                    map = 'Maze'
                    start_col = maze_start
                    end_col = maze_end  
                elif (prog == '2'):
                    img_orig = cv2.imread('KGP_map.png')
                    map = 'Map 1'
                    start_col = kgp_start
                    end_col = kgp_end
                elif (prog == '3'):
                    img_orig = get_locality_map('Locality.png')
                    map = 'Map 2'
                    start_col = locality_start
                    end_col = locality_end
                else:
                    break

                cv2.namedWindow('MAZE/MAP', cv2.WINDOW_NORMAL)
                cv2.imshow('MAZE/MAP',img_orig)
                print("This is the maze/map we'll be working on...")
                print('Press any key to continue...')
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                
                print('Which algorithm would you like to use for the path-finding?')
                print('To use breadth-first search, enter 1')
                print('To use depth-first search, enter 2')
                print('To use best-first search, enter 3')
                print("To use Dijkstra's algorithm, enter 4")
                print('To use A* algorithm, enter 5')
                print('To go back to maze/map choice, enter b')
                print('To quit, enter q')
                while True:
                    algo = input('Enter your (algorithm) choice : ')
                    while (algo not in ['1','2','3','4','5','b','B','q','Q']):
                        algo = input('Please give a valid input : ')

                    if (algo=='b' or algo=='B' or algo=='q' or algo=='Q'):
                        break
                    img = img_orig.copy()
                    start, end = find_start_end(start_col, end_col, img)
                    if algo=='1':
                        row = bfs_path(start, end, img)
                        row.insert(0,map)
                        writer.writerow(row)
                    elif algo=='2':
                        row = dfs_path(start, end, img)
                        row.insert(0,map)
                        writer.writerow(row)
                    elif algo=='3':
                        row = greedy_path(start, end, img)
                        row.insert(0,map)
                        writer.writerow(row)
                    elif algo=='4':
                        row = dijkstra_path(start, end, img)
                        row.insert(0,map)
                        writer.writerow(row)
                    elif algo=='5':
                        row = astar_path(start, end, img)
                        row.insert(0,map)
                        writer.writerow(row)

                    algo_cont = input('Would you like to continue working on the same maze/map? (y/n) : ')
                    if (algo_cont!='y' and algo_cont!='Y'):
                        break
                    else:
                        print("******************")

                if (algo == 'b' or algo=='B'):
                    continue
                elif (algo=='q' or algo=='Q'):
                    break
            cv2.destroyAllWindows()
            print('Program ended...')
    except:
        print("Oops! The program terminated due to an unexpected error...")
    


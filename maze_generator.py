import numpy as np
import cv2
import random

def maze_generate():

    #colors
    white = (255,255,255)
    black = (0,0,0)
    grey = (127,127,127)

    init_size = (20,20)
    upscale_fact = 1
    #fin_size = (init_size[0]*upscale_fact, init_size[1]*upscale_fact) = (200,200)

    maze_init = np.full((init_size[0],init_size[1],3), 255, dtype = np.uint8)

    #start and end nodes...
    maze_init[2,2] = grey
    maze_init[init_size[1]-3,init_size[0]-3] = grey

    prob = random.uniform(0.2,0.3)
    black_pix = int(prob*init_size[0]*init_size[1])

    count=0 #loop variable
    while(count<black_pix):
        i=random.randint(0,init_size[0]-1)
        j=random.randint(0,init_size[1]-1)
        if ((maze_init[i][j] == white).all()):
            maze_init[i][j] = black
            count+=1

    # maze_fin = cv2.resize(maze_init,None,fx=upscale_fact,fy=upscale_fact,interpolation=cv2.INTER_NEAREST)

    return maze_init

if __name__=='__main__':
    maze = maze_generate()
    
    #cv2.imwrite('maze.png',maze)
    
    cv2.namedWindow('MAZE',cv2.WINDOW_NORMAL)
    cv2.imshow('MAZE',maze)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

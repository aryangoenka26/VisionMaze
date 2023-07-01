import cv2
import numpy as np

def get_locality_map(img_path):
    #Colors
    red = (0, 0, 255)
    green = (0, 255, 0)

    img = cv2.imread(img_path)

    #creating mask based on color
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_color = np.array([0, 0, 250])
    higher_color = np.array([1, 1, 255])

    mask = cv2.inRange(hsv, lower_color, higher_color)

    #applying mask on original image
    masked = cv2.bitwise_and(img, img, None, mask)

    kernel = np.ones((2,2),np.uint8) #for erosion and dilation
    #erosion
    result = cv2.erode(masked,kernel, iterations=1)
    #dilation
    result = cv2.dilate(result,kernel, iterations=1)

    #setting start and end points
    result[78, 725] = red
    result[517, 68] = green

    result = cv2.resize(result, None, fx = 0.7, fy = 0.7, interpolation = cv2.INTER_NEAREST)

    return result

if __name__=='__main__':
    local_map = get_locality_map('Locality.png')

    #cv2.imwrite("req_locality_map.png", local_map)
    
    cv2.namedWindow('LOCALITY MAP', cv2.WINDOW_NORMAL)
    cv2.imshow("LOCALITY MAP", local_map)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
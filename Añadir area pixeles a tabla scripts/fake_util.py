import cv2
from cv2 import waitKey
import numpy as np



def greet(name):
    """This function takes a name as input and prints a greeting."""
    print(f"Hello, {name}!")

# Example usage:
def get_area( mangoe_name ):
    route = "../"+"mangoes/"+mangoe_name
    img = cv2.imread( route )
    img_rgb = img.copy()
    original_image = img_rgb
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    

    lower = np.array([0, 52, 126])
    upper = np.array([255, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    kernel = np.ones((3, 3), np.uint8)
    erosion = cv2.erode(mask, kernel, iterations=0)
    dilatacion = cv2.dilate(erosion, kernel, iterations=6)
    #closing = cv2.morphologyEx( dilatacion , cv2.MORPH_CLOSE , kernel )
    closing = dilatacion
     # ======================= Contirun ================================
    contours, hierarchy = cv2.findContours(closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    area_total = 0
    area_spots = 0
    contourTouched = []
    if contours and hierarchy is not None and len(hierarchy[0]) > 0:
            
            for i in range(len(contours)):
                if not(i in contourTouched) :
                    contour = contours[i]
                    hierarchy_info = hierarchy[0][i]
                    #print("hierarchy_info: " + str(i))
                    #print(hierarchy_info)
                    if hierarchy_info[2] > -1: #tiene hijo
                        area_father = cv2.contourArea( contour )
                        cv2.drawContours( original_image , [contour],  -1 , (255,0,0), 1, cv2.LINE_AA)
                        #extraer todos los contornos cuyo padre es el anterior
                        brothers_area = 0
                        for j in range(len(contours)):
                            hierarchy_brother = hierarchy[0][j]
                            if hierarchy_brother[3] == i : 
                                brother_contour = contours[j]
                                brothers_area +=  cv2.contourArea( brother_contour )
                                cv2.drawContours( original_image , [brother_contour],  -1 , (0,255,0), 1, cv2.LINE_AA)
                                contourTouched.append( j )
                        #endForbrother
                        #simple way:
                        """ area_child = cv2.contourArea(  contours[ hierarchy_info[2]  ] )
                        cv2.drawContours( original_image , [contours[ hierarchy_info[2] ]],  -1 , (0,255,0), 1, cv2.LINE_AA) """
                        #Tiene hermano? next
                        area_spots = brothers_area
                        area = area_father - brothers_area
                        area_total += area
                    else:
                        #print("No tiene hijo!!!")
                        area_child = cv2.contourArea( contour )
                        cv2.drawContours( original_image , [contour],  -1 , (255,255,255), 1, cv2.LINE_AA)
                        area_total += area_child
    return closing,area_total,area_spots  



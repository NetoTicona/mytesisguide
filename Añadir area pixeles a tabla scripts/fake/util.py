import cv2 
from cv2 import waitKey
import numpy as np 
import json

def process_frame( frame ,hue_min,sat_min,val_min,hue_max,sat_max,val_max , sumframe ):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([hue_min, sat_min, val_min])
    upper_red = np.array([hue_max, sat_max, val_max])
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    kernel_s = 3

    kernel = np.ones( (kernel_s,kernel_s) , np.uint8 )
    #(blur)erosion = cv2.erode( imgBlur , kernel , iterations=2 )
    #(blur)dilatacion = cv2.dilate( erosion , kernel , iterations=3 )
    

    erosion = cv2.erode( mask_red , kernel , iterations=1 )
    dilatacion = cv2.dilate( erosion , kernel , iterations=2 )
    closing = cv2.morphologyEx( dilatacion , cv2.MORPH_CLOSE , kernel )

    contours, hierarchy = cv2.findContours(closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    area_total = 0
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
                        cv2.drawContours( sumframe , [contour],  -1 , (255,0,0), 1, cv2.LINE_AA)
                        #extraer todos los contornos cuyo padre es el anterior
                        brothers_area = 0
                        for j in range(len(contours)):
                            hierarchy_brother = hierarchy[0][j]
                            if hierarchy_brother[3] == i : 
                                brother_contour = contours[j]
                                brothers_area +=  cv2.contourArea( brother_contour )
                                cv2.drawContours( sumframe , [brother_contour],  -1 , (0,255,0), 1, cv2.LINE_AA)
                                contourTouched.append( j )
                        #endForbrother
                        #simple way:
                        """ area_child = cv2.contourArea(  contours[ hierarchy_info[2]  ] )
                        cv2.drawContours( sumframe , [contours[ hierarchy_info[2] ]],  -1 , (0,255,0), 1, cv2.LINE_AA) """
                        #Tiene hermano? next
                        area = area_father - brothers_area
                        area_total += area
                    else:
                        #print("No tiene hijo!!!")
                        area_child = cv2.contourArea( contour )
                        cv2.drawContours( sumframe , [contour],  -1 , (255,255,255), 1, cv2.LINE_AA)
                        area_total += area_child
                    #print("\n")
                
                   # print("El contorno tocado {}".format(i)  )
            #fin For
           # print( "El área total es: {}".format( area_total )  )

    #--------------------------------------------------------------//

    return sumframe , area_total

 

def getBigArea(  object_v , object_a , object_r ):
    color = ""
    object_v = json.loads(object_v)
    object_a = json.loads(object_a)
    object_r = json.loads(object_r)

    if( (object_v["weight"] >= object_a["weight"]) and ( object_v["weight"] >= object_r["weight"] )  ):
        color = object_v["description"]
    elif( (object_a["weight"] >= object_v["weight"]) and ( object_a["weight"] >= object_r["weight"] ) ):
        color = object_a["description"]
    else:
        color = object_r["description"]

    return color
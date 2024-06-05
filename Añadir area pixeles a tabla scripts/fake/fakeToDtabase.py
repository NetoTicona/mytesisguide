import pymysql
import util
import os
import cv2
from decimal import Decimal
import json

class DataBase:
    def __init__(self , config):
        self.connection = pymysql.connect(**config)
        self.cursor = self.connection.cursor()

    def execute_query( self, query , data= None ):
        if data:
            self.cursor.execute( query , data )
        else:
            self.cursor.execute( query )

    def fetch_all(self):
        return self.cursor.fetchall()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()



db_config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'db_image_hsv'
}

db = DataBase(db_config)

#-----------------iterar atravez de las imagenes-----------//
for filename in os.listdir('.'):
    if filename.endswith('.jpg'):
        print(filename)
        name_components = filename.split("_")
        print( name_components )
        id = name_components[1]
        nasty = name_components[3]
        weight = '.'.join(nasty.rsplit('.', 1)[:-1])

        img = cv2.imread( filename )
        frame = img
        #frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        frame_red = frame.copy()
        frame_green = frame.copy()
        frame_yellow = frame.copy()

        r_hue_min = 0
        r_hue_max = 18
        r_sat_min = 43
        r_sat_max = 255
        r_val_min = 99
        r_val_max = 255
        _frame_red,_weight_red = util.process_frame( frame_red , r_hue_min,r_sat_min,r_val_min,r_hue_max,r_sat_max,r_val_max , frame  )

        g_hue_min = 27
        g_hue_max = 41
        g_sat_min = 21
        g_sat_max = 255
        g_val_min = 99
        g_val_max = 231
        _frame_green,_weight_green = util.process_frame( frame_green , g_hue_min,g_sat_min,g_val_min,g_hue_max,g_sat_max,g_val_max , _frame_red  )

        y_hue_min = 19
        y_hue_max = 26
        y_sat_min = 83
        y_sat_max = 255
        y_val_min = 50
        y_val_max = 255
        _frame_yellow,_weight_yellow = util.process_frame( frame_yellow , y_hue_min,y_sat_min,y_val_min,y_hue_max,y_sat_max,y_val_max , _frame_green )


        t_hue_min = 0
        t_hue_max = 255
        t_sat_min = 83
        t_sat_max = 255
        t_val_min = 50
        t_val_max = 255
        _frame,_total = util.process_frame( frame_yellow , t_hue_min,t_sat_min,t_val_min,t_hue_max,t_sat_max,t_val_max , _frame_green )

        obj_g = { "id":1, "weight":_weight_green,"description":"Verde" }
        obj_r = { "id":2, "weight":_weight_red,"description":"Rojo" }
        obj_y = { "id":3, "weight":_weight_yellow,"description":"Amarillo" }

        color_g = json.dumps( obj_g )
        color_r = json.dumps( obj_r )
        color_y = json.dumps( obj_y )
        predominant = util.getBigArea( color_g,color_y,color_r )
        print("predomenate: " , predominant )

        font = cv2.FONT_HERSHEY_COMPLEX
        cv2.putText( _frame_yellow, f"El área rojo es: {str(_weight_red)}" , (30, 350), font, 0.68 , (255,255,255),1,cv2.LINE_AA  )
        cv2.putText( _frame_yellow, f"El área verde es: {str(_weight_green)}" , (30,370), font, 0.68 , (255,255,255),1,cv2.LINE_AA  )
        cv2.putText( _frame_yellow, f"El área amarillo es: {str(_weight_yellow)}" , (30,390), font, 0.68 , (255,255,255),1,cv2.LINE_AA  )
        cv2.putText( _frame_yellow, f"El área total  es: { _total } " , (30,450), font, 0.68 , (255,255,255),1,cv2.LINE_AA )

        root_path = "fake_mangoes_view/"  
        save_path = os.path.join(root_path, 'mangoe_'+str(id)+'_pesop'+str(weight)+'.jpg')
        cv2.imwrite(save_path, _frame_yellow)

        dataTraining_sql = "insert into mangoe_training (peso , img_url , red_area, green_area , yellow_area , predominant_color , exportable , area_total , area_spot , manpulated ) values ( %s , %s ,%s , %s ,%s , %s , %s, %s , %s , %s ) "
        values = ( str( weight ), str( filename ) ,str(_weight_red) , str( _weight_green ) , str( _weight_yellow ) , str( predominant ) , str( 1 ) , str( _total) , str( 0 ) , str(1) )
        db.execute_query( dataTraining_sql , values )



db.commit()
db.close()










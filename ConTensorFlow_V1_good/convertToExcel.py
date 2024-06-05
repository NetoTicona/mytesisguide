import pymysql
import pandas as pd
import os
import cv2
from decimal import Decimal

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

    def save_to_excel(self, rows, file_name):
        df = pd.DataFrame(rows, columns=['id', 'weight', 'img_url' ,'red_area', 'green_area', 'yellow_area','predominant_color', 'exportable', 'area_total','area_spot' , 'manpulated' ])
        df.to_excel(file_name, index=False)

#-------------------------------------------#

#-------------------------------------------#
db_config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'db_image_hsv'
}

db = DataBase(db_config)

db.execute_query( "select * from mangoe_training" )
rows =db.fetch_all()
db.save_to_excel(rows, 'output.xlsx')
""" for row in rows:
    print(row)
    id = row[0]
    weight =row[1]
    red_area = row[3]
    green_area = row[4]
    yellow_area = row[5]
    exportable = row[7]
    area_spot = row[9] """






db.commit()
db.close()














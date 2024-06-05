import pymysql
import utils
import os
import cv2


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
for row in rows:
    #print(row)
    id = row[0]
    mangoe_path = row[2]
    mangoe_parts = mangoe_path.split("\\")
    mangoe_name = mangoe_parts[1]

    _frame,area_total,area_spot = utils.get_area( mangoe_name )

    print(" ${} es el area total del mango con id: ${} con un area de manchas de: ${}".format(area_total , id , area_spot  )  )
    sql_update = "update mangoe_training set area_total = %s , area_spot= %s where id=%s  "
    db.execute_query( sql_update , (area_total,area_spot, id    ) )
    root_path = ""  
    save_path = os.path.join(root_path, 'mangoe_image'+str(id)+'.jpg')
    cv2.imwrite(save_path, _frame)

db.commit()
db.close()






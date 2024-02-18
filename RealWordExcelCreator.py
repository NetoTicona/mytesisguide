import pymysql
import openpyxl
import random


class MySQLConnection:
    def __init__(self):
        self.connect = pymysql.connect(
            host="localhost",
            user="root",
            passwd="",
            database="db_image_hsv"
        )
        self.cursor = self.connect.cursor()

    def execute_query(self, query):
        self.cursor.execute(query)
        self.connect.commit()
        return self.cursor.fetchall()

    def close(self):
        self.connect.close()

    def random_value(self):
        return random.uniform(-0.2, 0.0)

    def save_to_excel(self, result, file_name):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        color_mapping = {"Rojo": 0.5, "Verde": 0.1, "Amarillo": 1}
        header = ["peso", "predominant_color", "encode"]
        sheet.append(header)
        
        for row in result:
            color = row[1]
            encode = color_mapping.get(color, 0)  
            row = list(row)
            random_noise = self.random_value()
            row.append(encode +  random_noise )
            sheet.append(row)
            
        workbook.save(file_name)




connection = MySQLConnection()
query = "select peso,predominant_color from mangoe_training"
result = connection.execute_query(query)
connection.save_to_excel(result, "output.xlsx")
print(result)
connection.close()
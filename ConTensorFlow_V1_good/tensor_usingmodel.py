import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
import tensorflow as tf 

""" Model training  """
path_json = "model_trainig.json"
path_h5 = "model_trainig.h5"

""" WEIGHT TRainig """
""" path_json = "model_weight_trainig.json"
path_h5 = "model_weight_trainig.h5" """

with open(path_json, "r") as json_file:
    loaded_model_json = json_file.read()

loaded_model = tf.keras.models.model_from_json(loaded_model_json)
loaded_model.load_weights(path_h5)

#========= predict ==================
""" df=pd.DataFrame({ "area_spot":[974.00] , "weight": [53400] , "red_area":[0.0] , "green_area":[95710.5] , "yellow_area":[386.50]  })
predic = loaded_model.predict( df )
print("La prediccion es: ", predic ) """

#============= predict 2=============
#path="training_weights.xlsx"
path="training_percentages.xlsx"
#path="Mangoe_training.xlsx"
#path="only_colors.xlsx"
raw_data=pd.read_excel(path, sheet_name="Sheet1")
dataset=raw_data.copy()
data_train = dataset.sample( frac=0.01 , random_state=0 )

data_test = dataset.drop( data_train.index )
data_test_copy = data_test.copy()
#test_output = data_test.pop( "exportable" )
test_output = data_test.pop( "exportable" )
weights = data_test_copy.pop("weight")

mean = 458.238095
std = 73.411787



def escala(x):
    return ( x- mean )/std

#test_input = escala(data_test)
test_input = data_test
print("test Input: ")
print( test_input )


print("Entradas: \n" , data_test )
output_Est = loaded_model.predict( test_input )

df = pd.DataFrame({ "Reales" : test_output }) 
#df["weights"] = weights
df["Estimados"] = output_Est
print(df)

plt.scatter( test_output , output_Est )
plt.xlabel("Valores Reales")
plt.ylabel("Valores Estimados")

plt.grid()
plt.show()